/*++
Copyright (c) 2017 Microsoft Corporation and Arie Gurfinkel

Module Name:

    spacer_generalizers.cpp

Abstract:

    Lemma generalizers.

Author:

    Nikolaj Bjorner (nbjorner) 2011-11-20.
    Arie Gurfinkel

Revision History:

--*/


#include "muz/spacer/spacer_context.h"
#include "muz/spacer/spacer_generalizers.h"
#include "ast/ast_util.h"
#include "ast/expr_abstract.h"
#include "ast/rewriter/var_subst.h"
#include "ast/for_each_expr.h"
#include "ast/rewriter/factor_equivs.h"
#include "ast/rewriter/expr_safe_replace.h"
#include "ast/substitution/matcher.h"
#include "ast/expr_functors.h"
#include "smt/smt_solver.h"
#include "qe/qe_term_graph.h"



namespace spacer {
void lemma_sanity_checker::operator()(lemma_ref &lemma) {
    unsigned uses_level;
    expr_ref_vector cube(lemma->get_ast_manager());
    cube.append(lemma->get_cube());
    ENSURE(lemma->get_pob()->pt().check_inductive(lemma->level(),
                                                  cube, uses_level,
                                                  lemma->weakness()));
}

namespace{
    class contains_array_op_proc : public i_expr_pred {
        ast_manager &m;
        family_id m_array_fid;
    public:
        contains_array_op_proc(ast_manager &manager) :
            m(manager), m_array_fid(m.mk_family_id("array"))
            {}
        bool operator()(expr *e) override {
            return is_app(e) && to_app(e)->get_family_id() == m_array_fid;
        }
    };
}

// ------------------------
// lemma_bool_inductive_generalizer
/// Inductive generalization by dropping and expanding literals
void lemma_bool_inductive_generalizer::operator()(lemma_ref &lemma) {
    if (lemma->get_cube().empty()) return;
    TRACE("spacer.ind_gen", tout<<"LEMMA:\n"<<mk_and(lemma->get_cube())<<"\n";);
    // STRACE("spacer.ind_gen", tout<<"POB:\n"<<lemma->get_pob()<<"\n";);       

    // STRACE("spacer.ind_gen", tout<<"USE LIT EXPANSION?\n"<<m_use_expansion<<"\n";);
    m_st.count++;
    scoped_watch _w_(m_st.watch);

    unsigned uses_level;
    pred_transformer &pt = lemma->get_pob()->pt();
    ast_manager &m = pt.get_ast_manager();

    contains_array_op_proc has_array_op(m);
    check_pred has_arrays(has_array_op, m);

    expr_ref_vector cube(m);
    cube.append(lemma->get_cube());

    bool dirty = false;
    expr_ref true_expr(m.mk_true(), m);
    ptr_vector<expr> processed;
    expr_ref_vector extra_lits(m);

    unsigned weakness = lemma->weakness();

    unsigned i = 0, num_failures = 0;

    //bootstrapping to get a pool_solver smt2 file. Should only run once
    if(m_1st_query && cube.size() > 1){
        TRACE("spacer.ind_gen", tout << "Bootstrapping...\n";);

        pt.check_inductive(lemma->level(), cube, uses_level, weakness, true);
        m_1st_query = false;
    }
    //FOR DEBUGGING ONLY
    // pt.check_inductive(lemma->level(), cube, uses_level, weakness, true);
    while (i < cube.size() &&
           (!m_failure_limit || num_failures < m_failure_limit)) {
        std::time_t start = std::time(nullptr);
        expr_ref lit(m);
        lit = cube.get(i);
        
        if (m_array_only && !has_arrays(lit)) {
            processed.push_back(lit);
            ++i;
            continue;
        }
        // STRACE("spacer.ind_gen", tout<<"CUBE:\n"<<mk_and(cube)<<"\n";);       
        // STRACE("spacer.ind_gen", tout<<"trying to drop \n:"<<lit<<"\n";);

        cube[i] = true_expr;

        if (cube.size() > 1 &&
            pt.check_inductive(lemma->level(), cube, uses_level, weakness)) {
            std::time_t after_check_ind = std::time(nullptr);
            // TRACE("spacer.ind_gen", tout<<"\tpassed check_ind in:"<<after_check_ind - start <<"\n";);
            num_failures = 0;
            dirty = true;
            for (i = 0; i < cube.size() &&
                     processed.contains(cube.get(i)); ++i);
        } else {
            std::time_t after_check_ind = std::time(nullptr);
            // TRACE("spacer.ind_gen", tout<<"\tfailed check_ind in:"<<after_check_ind - start <<"\n";);
             // check if the literal can be expanded and any single bb
            // literal in the expansion can replace it

            if(m_use_expansion){
                extra_lits.reset();
                extra_lits.push_back(lit);
                expand_literals(m, extra_lits);
                SASSERT(extra_lits.size() > 0);
                bool found = false;
                if (extra_lits.get(0) != lit && extra_lits.size() > 1) {
                    for (unsigned j = 0, sz = extra_lits.size(); !found && j < sz; ++j) {
                        cube[i] = extra_lits.get(j);
                        if (pt.check_inductive(lemma->level(), cube, uses_level, weakness)) {
                            num_failures = 0;
                            dirty = true;
                            found = true;
                            processed.push_back(extra_lits.get(j));
                            for (i = 0; i < cube.size() &&
                                     processed.contains(cube.get(i)); ++i);
                        }
                    }
                }
                if (!found) {
                    cube[i] = lit;
                    processed.push_back(lit);
                    ++num_failures;
                    ++m_st.num_failures;
                    ++i;
                }
                std::time_t after_expand_lits = std::time(nullptr);
                // TRACE("spacer.ind_gen", tout<<"\t\tfinished expand lit in:"<<after_expand_lits - after_check_ind <<"\n";);
            }else{
                cube[i] = lit;
                processed.push_back(lit);
                ++num_failures;
                ++m_st.num_failures;
                ++i;
            }
         }
    }

    if(cube.size()>1){ // do not dump data if there is no final "pair"
        TRACE("spacer.ind_gen",
              tout << "Generalized from:\n" << mk_and(lemma->get_cube())
              << "\ninto\n" << mk_and(cube) << "\n";);
    }
    if (dirty) {
        lemma->update_cube(lemma->get_pob(), cube);
        SASSERT(uses_level >= lemma->level());
        lemma->set_level(uses_level);
        //lemma->get_expr() is scary. Comment out the following line for now
        //TRACE("spacer.ind_gen", tout<<"SUCCESS. new lemma:"<<lemma->get_expr()->get_id()<<"\n";);
    }
}

void lemma_bool_inductive_generalizer::collect_statistics(statistics &st) const
{
    st.update("time.spacer.solve.reach.gen.bool_ind", m_st.watch.get_seconds());
    st.update("bool inductive gen", m_st.count);
    st.update("bool inductive gen failures", m_st.num_failures);
}

// ------------------------
// h_inductive_generalizer
/// Inductive generalization by dropping and expanding literals with some heuristics
// void h_inductive_generalizer::operator()(lemma_ref &lemma) {
//   if (lemma->get_cube().empty())
//     return;
//   TRACE("spacer.h_ind_gen", tout << "LEMMA:\n"
//                                  << mk_and(lemma->get_cube()) << "\n";);


//   STRACE("spacer.h_ind_gen",
//          tout << "1st_seen_can_drop:" << m_lit_st.fst_seen_can_drop << ", "
//               << "1st_seen_cannot_drop:" << m_lit_st.fst_seen_cannot_drop
//               << ", "
//               << "ratio:" << m_lit_st.fst_seen_success_rate() << "\n";);
//   scoped_watch _w_(m_st.watch);

//   unsigned uses_level;
//   pred_transformer &pt = lemma->get_pob()->pt();
//   ast_manager &m = pt.get_ast_manager();

//   expr_ref_vector cube(m);
//   cube.append(lemma->get_cube());

//   bool dirty = false;
//   expr_ref true_expr(m.mk_true(), m);
//   ptr_vector<expr> processed;
//   expr_ref_vector extra_lits(m);

//   unsigned weakness = lemma->weakness();

//   unsigned i = 0, num_failures = 0;

//   std::vector<int> kept_lits{};
//   std::vector<int> to_be_checked_lits{};

//   expr_ref_vector final_cube(m);
//   //init to_be_checked_lits to be [0...lemma->get_cube.size()]
//   for(int idx = 0; idx < lemma->get_cube().size(); idx++){
//       to_be_checked_lits.push_back(idx);
//   }


//   //Bootstrapping to generate the first pool_solver.smt2 file
//   if(m_1st_query && cube.size() > 1){
//       TRACE("spacer.h_ind_gen", tout << "Bootstrapping...\n";);

//       pt.check_inductive(lemma->level(), cube, uses_level, weakness, true);
//       m_1st_query = false;
//   }

//   // std::cout<<"kept_lits: [";
//   // for(int it: kept_lits){
//   //     std::cout<<it<<" ";
//   // }
//   // std::cout<<"]"<<std::endl;
//   // std::cout<<"to_be_checked_lits: [";
//   // for(int it: to_be_checked_lits){
//   //     std::cout<<it<<" ";
//   // }
//   // std::cout<<"]"<<std::endl;
//   int checking_lit;
//   //new ind gen loop
//   while (to_be_checked_lits.size()>0 && // not done yet
//          (!m_failure_limit || num_failures < m_failure_limit)) {
//       //pop left
//       checking_lit = to_be_checked_lits.front();
//       to_be_checked_lits.erase(to_be_checked_lits.begin());

//       if (should_try_drop(lemma->get_cube(), kept_lits, checking_lit, to_be_checked_lits)){
//           //****Build the cube to check for inductive****

//           //the new cube is the masked version of the original cube
//           expr_ref_vector new_cube(m);
//           new_cube.append(lemma->get_cube());
//           //Mask the new_cube.
//           //If the lits is not in kept_lits, and not in to_be_checked_lits, set it to True
//           for(int idx = 0; idx < lemma->get_cube().size(); idx++){
//               //is it in kept_lits?
//               bool in_kept_lits = false;
//               for(int it: kept_lits){
//                   if(idx==it){
//                       in_kept_lits = true;
//                       break;
//                   }
//               }

//               //is it in to_be_checked_lits
//               bool in_to_be_checked_lits = false;
//               for(int it: to_be_checked_lits){
//                   if(idx==it){
//                       in_to_be_checked_lits = true;
//                       break;
//                   }
//               }
//               if(!in_to_be_checked_lits && !in_kept_lits){
//                   new_cube[idx] = true_expr;
//               }
//           }
//           //set the checking_lit to true
//           new_cube[checking_lit] = true_expr;

//           //****Finish building the new_cube to be checked****

//           STRACE("spacer.h_ind_gen", tout << "new cube:" << mk_and(new_cube) <<"\n";);
//           //check inductiveness of the new_cube
//           bool dropped = pt.check_inductive(lemma->level(), new_cube, uses_level, weakness);

//           if(dropped){
//               STRACE("spacer.h_ind_gen", tout << "drop successfully" <<"\n";);
//               dirty = true;
//               num_failures = 0;
//               //new_cube should be smaller or stay the same.
//               //try to not update kept_lits and to_be_checked_lits first
//               //update kept_lits
//               std::vector<int> new_kept_lits{};
//               for (int it: kept_lits){
//                   if(new_cube.contains(lemma->get_cube()[it])){
//                       new_kept_lits.push_back(it);
//                   }
//               }

//               kept_lits = new_kept_lits;

//               //update to_be_checked_lits
//               std::vector<int> new_to_be_checked_lits{};
//               for (int it: to_be_checked_lits){
//                   if(new_cube.contains(lemma->get_cube()[it])){
//                       new_to_be_checked_lits.push_back(it);
//                   }
//               }
//               to_be_checked_lits = new_to_be_checked_lits;
//           }else{
//               kept_lits.push_back(checking_lit);
//               ++num_failures;
//           }
//       }else{
//           //push checking_lit to kept_lits
//           kept_lits.push_back(checking_lit);
//           //remove from 
//       }
      
//   }

//   if(dirty){
//       //final cube should be kept_lits
//       for(int it: kept_lits){
//           final_cube.push_back(lemma->get_cube()[it]);
//       }

//       TRACE("spacer.h_ind_gen", tout << "Generalized from:\n"
//                                        << mk_and(lemma->get_cube()) << "\ninto\n"
//                                        << mk_and(final_cube) << "\n";);
//       SASSERT(uses_level >= lemma->level());
//       lemma->update_cube(lemma->get_pob(), final_cube);
//       lemma->set_level(uses_level);
//   }

//   //OLD LOOP
//   // while (i < cube.size() &&
//   //        (!m_failure_limit || num_failures < m_failure_limit)) {
//   //   expr_ref lit(m);
//   //   lit = cube.get(i);
//   //   increase_lit_count(lit);

//   //   //generally we want to drop lit that can be drop in the past
    


//   //   if (should_try_drop(lemma->get_cube(), kept_lits, i, to_be_checked_lits)) {
//   //     cube[i] = true_expr;
//   //     if (cube.size() > 1 &&
//   //         pt.check_inductive(lemma->level(), cube, uses_level, weakness)) {
//   //       num_failures = 0;
//   //       dirty = true;
//   //       for (i = 0; i < cube.size() && processed.contains(cube.get(i)); ++i)
//   //         ;
//   //       // // drop successful. check and increase fst_seen_can_drop
//   //       // if (m_lit2count[lit]->seen == 1) {
//   //       //   m_lit_st.fst_seen_can_drop++;
//   //       // }
//   //       // // increase the success counter
//   //       // m_lit2count[lit]->success++;


//   //     } else {
//   //       // drop unsuccessful. check and increase fst_seen_cannot_drop
//   //       // if (m_lit2count[lit]->seen == 1) {
//   //       //   m_lit_st.fst_seen_cannot_drop++;
//   //       // }
//   //       //push i to kept_lits
//   //       kept_lits.push_back(i);

//   //       cube[i] = lit;
//   //       processed.push_back(lit);
//   //       ++num_failures;
//   //       ++m_st.num_failures;
//   //       ++i;
//   //     }
//   //   } else {
//   //       //push i to kept_lits
//   //       kept_lits.push_back(i);
//   //       // skip dropping this literal
//   //       ++i;
//   //       TRACE("spacer.h_ind_gen", tout << lit << ": "
//   //                                      << "Do not try to drop."
//   //                                      << "\n";);
//   //       // should we decrease seen_counter?
//   //       m_lit2count[lit]->seen --;
//   //   }
//   // }
//   // if (dirty) {
//   //   TRACE("spacer.h_ind_gen", tout << "Generalized from:\n"
//   //                                  << mk_and(lemma->get_cube()) << "\ninto\n"
//   //                                  << mk_and(cube) << "\n";);
//   //   lemma->update_cube(lemma->get_pob(), cube);
//   //   SASSERT(uses_level >= lemma->level());
//   //   lemma->set_level(uses_level);
//   // }
//   // TRACE("spacer.h_ind_gen", tout << "m_1sT_query:"<<m_1st_query<<"\n";);
//   //send datapoint to server
//   // if(m_lemmas_sent < 1000 ){
//   //     std::stringstream ss_lemma_before;
//   //     std::stringstream ss_lemma_after;
//   //     ss_lemma_before<<mk_and(lemma->get_cube());
//   //     ss_lemma_after<<mk_and(cube);
//   //     m_grpc_conn.SendLemma(ss_lemma_before.str(), ss_lemma_after.str());
//   //     m_lemmas_sent ++;
//   // }
//   // dump_lit_count();
// }

    //NEW () using both positive model and negative model
void h_inductive_generalizer::operator()(lemma_ref &lemma) {
  if (lemma->get_cube().empty())
    return;
  TRACE("spacer.h_ind_gen", tout << "LEMMA:\n"
                                 << mk_and(lemma->get_cube()) << "\n";);


  STRACE("spacer.h_ind_gen",
         tout << "1st_seen_can_drop:" << m_lit_st.fst_seen_can_drop << ", "
              << "1st_seen_cannot_drop:" << m_lit_st.fst_seen_cannot_drop
              << ", "
              << "ratio:" << m_lit_st.fst_seen_success_rate() << "\n";);
  scoped_watch _w_(m_st.watch);

  unsigned uses_level;
  pred_transformer &pt = lemma->get_pob()->pt();
  ast_manager &m = pt.get_ast_manager();

  expr_ref_vector cube(m);
  cube.append(lemma->get_cube());

  bool dirty = false;
  expr_ref true_expr(m.mk_true(), m);
  ptr_vector<expr> processed;
  expr_ref_vector extra_lits(m);

  unsigned weakness = lemma->weakness();

  unsigned i = 0, num_failures = 0;

  std::vector<unsigned> kept_lits;
  std::vector<unsigned> to_be_checked_lits;

  expr_ref_vector final_cube(m);
  //init to_be_checked_lits to be [0...lemma->get_cube.size()]
  for(int idx = 0; idx < lemma->get_cube().size(); idx++){
      to_be_checked_lits.push_back(idx);
  }


  //Bootstrapping to generate the first pool_solver.smt2 file
  if(m_1st_query && cube.size() > 1){
      TRACE("spacer.h_ind_gen", tout << "Bootstrapping...\n";);

      pt.check_inductive(lemma->level(), cube, uses_level, weakness, true);
      m_1st_query = false;
  }

  unsigned checking_lit;
  bool query_model = false;
  std::vector<unsigned> mask;
  std::vector<unsigned> new_kept_lits;
  std::vector<unsigned> new_to_be_checked_lits;
  std::vector<unsigned> checking_lits;
  bool model_dirty;
  bool last_ans_success = false;
  bool first_query = true;
  //new ind gen loop
  while (to_be_checked_lits.size()>0){ // not done yet
      m_st.count++;
      //made_progress is false iff the cube constructed from the returned mask is not inductive (a wasted round)
      //if made_progress is true, attempt to use the model
      //if made_progress is false, try to drop it the old way
      //the new cube is the masked version of the original cube
      expr_ref_vector new_cube(m);
      new_cube.append(lemma->get_cube());

      //delegate all new cube masking to the model
      model_dirty = query_mask(lemma->get_cube(), kept_lits, to_be_checked_lits, checking_lits, mask, last_ans_success, first_query);
      if(first_query){first_query = false;}

      if(model_dirty){m_grpc_info.dirty_requests++;};
      // std::cout<<"mask:";
      // for(unsigned i: mask){
      //     std::cout<<i<<",";
      // }
      // std::cout<<"\n";
      //std::cout<<"checking_lits:";
      //for(unsigned i: checking_lits){
      //    std::cout<<i<<",";
      //}
      //std::cout<<"\n";      //mask the new cube using the mask returned by the model
      for(int idx=0; idx < lemma->get_cube().size(); idx++){
          if(mask[idx]==0){
              new_cube[idx] = true_expr;
          }
      }
      //std::cout<<"new_cube from model:"<< mk_and(new_cube)<<"\n";

      m_st.ind_gen_q_watch.start();
      bool dropped = pt.check_inductive(lemma->level(), new_cube, uses_level, weakness);
      m_st.ind_gen_q_watch.stop();
      TRACE("spacer.ind_gen_timer", tout << "Checking from:\n"
            
            << mk_and(lemma->get_cube()) << "\ninto\n"
            << mk_and(new_cube) << " takes\n"
            <<m_st.ind_gen_q_watch.get_seconds() << "\n";);

      if(dropped){
          last_ans_success = true;
          STRACE("spacer.h_ind_gen", tout << "drop successfully" <<"\n";);
          //set query_model to true to try using the model for the next round
          //std::cout<<"Drop successfully. New cube is:"<<mk_and(new_cube)<<"\n";
          //new_cube should be smaller or stay the same.
          //try to not update kept_lits and to_be_checked_lits first
          //update kept_lits. It has to be updated because there are lits in here that were caused by the P_model, not by failing to drop in the past
          new_kept_lits.clear();
          new_to_be_checked_lits.clear();
          for (int it: kept_lits){
              if(new_cube.contains(lemma->get_cube()[it])){
                  new_kept_lits.push_back(it);
              }
          }

          kept_lits = new_kept_lits;

          //update to_be_checked_lits
          std::vector<unsigned> new_to_be_checked_lits;
          for (int it: to_be_checked_lits){
              if(new_cube.contains(lemma->get_cube()[it])){
                  new_to_be_checked_lits.push_back(it);
              }
          }
          to_be_checked_lits = new_to_be_checked_lits;
          dirty = true;

          if(m_heu_index==2 && model_dirty){
            break;
          }

      }else{
          last_ans_success = false;
          //update kept_lits
          //only update kept_lits and to_be_checked_lits if checking_lits size is 1.
          //There is nothing we can conclude if we fail to drop more than 1 lits at a time
          if(model_dirty){m_grpc_info.unsuccessful_answers++;}

          if(checking_lits.size()==1){
              //std::cout<<"failed to drop 1 lit. Move it to kept_lits and remove it from to_be_checked_lits"<<"\n";
              kept_lits.push_back(checking_lits[0]);
              auto it = find(to_be_checked_lits.begin(),to_be_checked_lits.end(), checking_lits[0]);

              if ( it != to_be_checked_lits.end() )
                  to_be_checked_lits.erase(it);
          }
          m_st.num_failures++;
      }
  }

  if(dirty){
      //final cube should be kept_lits
      for(int it: kept_lits){
          final_cube.push_back(lemma->get_cube()[it]);
      }

      //std::cout<<"FINAL CUBE:"<<mk_and(final_cube)<<"\n";
      TRACE("spacer.ind_gen", tout << "Generalized from:\n"
                                       << mk_and(lemma->get_cube()) << "\ninto\n"
                                       << mk_and(final_cube) << "\n";);
      SASSERT(uses_level >= lemma->level());
      lemma->update_cube(lemma->get_pob(), final_cube);
      lemma->set_level(uses_level);
  }
  m_grpc_info.dump();
}

  // bool dropped = pt.check_inductive(lemma->level(), new_cube, uses_level, weakness);
    bool h_inductive_generalizer::query_mask(const expr_ref_vector &cube, std::vector<unsigned> &kept_lits, std::vector<unsigned> &to_be_checked_lits, std::vector<unsigned> &checking_lits, std::vector<unsigned> &mask, const bool last_ans_success, const bool first_query) {
    scoped_watch _w_(m_st.outside_time_watch);
    std::stringstream ss_lem;
    if(first_query){
        TRACE("spacer.h_ind_gen", tout << "cube"<<mk_and(cube)<<"\n";);
        ss_lem<<mk_and(cube);
        m_grpc_info.total_requests++;
    }
    else{
        ss_lem<<"";
    }
    return m_grpc_conn.QueryMask(ss_lem.str(),//the string repr of the original lemma
                                 cube.size(),
                                 kept_lits,// the lits that are checked and kept, (a list of int)
                                 to_be_checked_lits,
                                 checking_lits,
                                 mask,
                                 last_ans_success);
}

void h_inductive_generalizer::collect_statistics(statistics &st) const {
  st.update("time.spacer.solve.reach.gen.bool_ind", m_st.watch.get_seconds());
  st.update("time.spacer.solve.reach.gen.bool_ind.outside_spacer", m_st.outside_time_watch.get_seconds());
  st.update("bool inductive gen", m_st.count);
  st.update("bool inductive gen failures", m_st.num_failures);
}

bool h_inductive_generalizer::yesno(float prob){
    /*
      return true with probability prob
     */
    float flipped_value = float(m_random()) / float(m_random.max_value());
    return flipped_value < prob;
}

bool h_inductive_generalizer::should_try_drop(const expr_ref_vector &cube, const std::vector<unsigned> &kept_lits, const unsigned &checking_lit, const std::vector<unsigned> &to_be_checked_lits) {
    expr_ref lit(m);
    lit = cube.get(checking_lit);
    // not enough data. Try to drop.
    // if (m_lit_st.n_lits() < m_threshold) {
    //     return true;
    // }
    // has only 1 lit, return false
    if (cube.size()==1){
        return false;
    }

    // enough data, use heuristics
    switch (m_heu_index) {
    case 1: {
        // temporary change to >=1 to see if it matches no heuristics
        return m_lit2count[lit]->seen >= 1;
    } break;
    case 2:
        /*keep the ratio of 1st seen lits that can be drop, and make a guess
         * based on that*/
        {
            if (m_lit2count[lit]->seen > 1) {
                return true;
            }
            return yesno(m_lit_st.fst_seen_success_rate());
        }
        break;
    case 3: {
        /*
          if not a new lit, use the success rate of dropping the lit so far
          if a new lit, use 2nd heuristic.
        */
        double l_success_rate = lit_success_rate(lit);

        if (l_success_rate == -1) {
            // is a new lit. use 2nd heuristic
            return yesno(m_lit_st.fst_seen_success_rate());
        } else {
            // not a new lit.was dropping it successful in the past?
            return l_success_rate > SUCCESS_THRES;
        }

        // this line should never be reached;
        SASSERT(false);
    } break;
    case 4: {
        // was dropping it successful in the past?
        return lit_success_rate(lit) > SUCCESS_THRES;
    } break;
    case 5: {
        /*
          like heu 3, but stochastic
        */
        double l_success_rate = lit_success_rate(lit);

        if (l_success_rate == -1) {
            // is a new lit. use 2nd heuristic
            return yesno(m_lit_st.fst_seen_success_rate());
        } else {
            // not a new lit. was dropping it successful in the past?
            return yesno(l_success_rate);
        }

        // this line should never be reached;
        SASSERT(false);
        return true;
    } break;
    case 6: {
        /*

         */
        if (m_lit2count[lit]->index < 10 &&
            m_lit2count[lit]->success_rate() < 0.2) {
            return false;
        }

        return true;
    } break;
    case 7: {
        /*

         */
        if (m_lit2count[lit]->index < 10 &&
            m_lit2count[lit]->success_rate() < 0.2) {
            return yesno(m_lit2count[lit]->success_rate());
        }

        return true;
    } break;
    case 42: {
        return true;
        /*
          query the model
          Need to send:
          lemma
          kept_lits
          checking_lit
          to_be_checked_lits
        */
        //No lits being kept yet. Always try to drop
        // if(kept_lits.size()==0){
        //     std::cout << "answer:" << "true" <<"\n";
        //     return true;
        // }

        // std::stringstream ss_lem;
        // ss_lem<<mk_and(cube);
        // const bool answer = m_grpc_conn.QueryModel(ss_lem.str(),//the string repr of the original lemma
        //                                            kept_lits,// the lits that are checked and kept, (a list of int)
        //                                            checking_lit,// the lit that we are checking (one int)
        //                                            to_be_checked_lits);//not using this for now
      
        // std::cout << "answer:" << answer <<"\n";
        // STRACE("spacer.h_ind_gen", tout << "answer:" << answer <<"\n";);
        // return answer;
    }
    }
    // default value
    return true;
}

void h_inductive_generalizer::increase_lit_count(expr_ref &lit) {
  if (m_lit2count.contains(lit)) {
    STRACE("spacer.h_ind_gen", tout << "LIT:" << lit << " exists."
                                    << "\n";);
    m_lit2count[lit]->seen++;
  } else {
    STRACE("spacer.h_ind_gen", tout << "LIT:" << lit
                                    << " doesnt exist. Adding to lit2time"
                                    << "\n";);
    lit_info *l_i = alloc(lit_info);
    l_i->seen = 1;
    l_i->success = 0;
    l_i->index = m_lit2count.size();

    m_lit2count.insert(lit, l_i);
    m_lits.push_back(lit);
  }
}

double h_inductive_generalizer::lit_success_rate(expr_ref &lit) {
  /*
    return -1 if this is the first time we see the lit
    otherwise returns it success rate of dropping this lit so far
   */

  double seen = m_lit2count[lit]->seen;
  double success = m_lit2count[lit]->success;

  if (seen == 1) {
    return -1;
  }
  return success / seen;
}

void h_inductive_generalizer::dump_lit_count() {
  for (obj_map<expr, lit_info *>::iterator it = m_lit2count.begin();
       it != m_lit2count.end(); it++) {
    float seen = it->m_value->seen;
    float success = it->m_value->success;
    float ratio = it->m_value->success_rate();
    STRACE("spacer.h_ind_gen", tout << mk_pp(it->m_key, m) << "\n"
                                    << ": index:" << it->m_value->index
                                    << ": seen: " << seen << ", "
                                    << "drop successfully: " << success << ", "
                                    << "success ratio:" << ratio << "\n";);
  }
}

void unsat_core_generalizer::operator()(lemma_ref &lemma) {
  m_st.count++;
  scoped_watch _w_(m_st.watch);
  ast_manager &m = lemma->get_ast_manager();

  pred_transformer &pt = lemma->get_pob()->pt();

  unsigned old_sz = lemma->get_cube().size();
  unsigned old_level = lemma->level();
  (void)old_level;

  unsigned uses_level;
  expr_ref_vector core(m);
  VERIFY(pt.is_invariant(lemma->level(), lemma.get(), uses_level, &core));

  CTRACE("spacer", old_sz > core.size(),
         tout << "unsat core reduced lemma from: " << old_sz << " to "
              << core.size() << "\n";);
  CTRACE("spacer", old_level < uses_level,
         tout << "unsat core moved lemma up from: " << old_level << " to "
              << uses_level << "\n";);
  if (old_sz > core.size()) {
    lemma->update_cube(lemma->get_pob(), core);
    lemma->set_level(uses_level);
  }
}

void unsat_core_generalizer::collect_statistics(statistics &st) const
{
    st.update("time.spacer.solve.reach.gen.unsat_core", m_st.watch.get_seconds());
    st.update("gen.unsat_core.cnt", m_st.count);
    st.update("gen.unsat_core.fail", m_st.num_failures);
}

namespace {
class collect_array_proc {
    array_util m_au;
    func_decl_set &m_symbs;
    sort *m_sort;
public:
    collect_array_proc(ast_manager &m, func_decl_set& s) :
        m_au(m), m_symbs(s), m_sort(nullptr) {}

    void operator()(app* a)
    {
        if (a->get_family_id() == null_family_id && m_au.is_array(a)) {
            if (m_sort && m_sort != get_sort(a)) { return; }
            if (!m_sort) { m_sort = get_sort(a); }
            m_symbs.insert(a->get_decl());
        }
    }
    void operator()(var*) {}
    void operator()(quantifier*) {}
};
}

bool lemma_array_eq_generalizer::is_array_eq (ast_manager &m, expr* e) {

    expr *e1 = nullptr, *e2 = nullptr;
    if (m.is_eq(e, e1, e2) && is_app(e1) && is_app(e2)) {
        app *a1 = to_app(e1);
        app *a2 = to_app(e2);
        array_util au(m);
        if (a1->get_family_id() == null_family_id &&
            a2->get_family_id() == null_family_id &&
            au.is_array(a1) && au.is_array(a2))
            return true;
    }
    return false;
}

void lemma_array_eq_generalizer::operator() (lemma_ref &lemma)
{

    ast_manager &m = lemma->get_ast_manager();


    expr_ref_vector core(m);
    expr_ref v(m);
    func_decl_set symb;
    collect_array_proc cap(m, symb);


    // -- find array constants
    core.append (lemma->get_cube());
    v = mk_and(core);
    for_each_expr(cap, v);

    CTRACE("core_array_eq", symb.size() > 1 && symb.size() <= 8,
          tout << "found " << symb.size() << " array variables in: \n"
          << v << "\n";);

    // too few constants or too many constants
    if (symb.size() <= 1 || symb.size() > 8) { return; }


    // -- for every pair of constants (A, B), check whether the
    // -- equality (A=B) generalizes a literal in the lemma

    ptr_vector<func_decl> vsymbs;
    for (auto * fdecl : symb) {vsymbs.push_back(fdecl);}

    // create all equalities
    expr_ref_vector eqs(m);
    for (unsigned i = 0, sz = vsymbs.size(); i < sz; ++i) {
        for (unsigned j = i + 1; j < sz; ++j) {
            eqs.push_back(m.mk_eq(m.mk_const(vsymbs.get(i)),
                                  m.mk_const(vsymbs.get(j))));
        }
    }

    // smt-solver to check whether a literal is generalized.  using
    // default params. There has to be a simpler way to approximate
    // this check
    ref<solver> sol = mk_smt_solver(m, params_ref::get_empty(), symbol::null);
    // literals of the new lemma
    expr_ref_vector lits(m);
    lits.append(core);
    expr *t = nullptr;
    bool dirty = false;
    for (unsigned i = 0, sz = core.size(); i < sz; ++i) {
        // skip a literal is it is already an array equality
        if (m.is_not(lits.get(i), t) && is_array_eq(m, t)) continue;
        solver::scoped_push _pp_(*sol);
        sol->assert_expr(lits.get(i));
        for (auto *e : eqs) {
            solver::scoped_push _p_(*sol);
            sol->assert_expr(e);
            lbool res = sol->check_sat(0, nullptr);

            if (res == l_false) {
                TRACE("core_array_eq",
                      tout << "strengthened " << mk_pp(lits.get(i), m)
                      << " with " << mk_pp(mk_not(m, e), m) << "\n";);
                lits[i] = mk_not(m, e);
                dirty = true;
                break;
            }
        }
    }

    // nothing changed
    if (!dirty) return;

    TRACE("core_array_eq",
           tout << "new possible core " << mk_and(lits) << "\n";);


    pred_transformer &pt = lemma->get_pob()->pt();
    // -- check if the generalized result is consistent with trans
    unsigned uses_level1;
    if (pt.check_inductive(lemma->level(), lits, uses_level1, lemma->weakness())) {
        TRACE("core_array_eq", tout << "Inductive!\n";);
        lemma->update_cube(lemma->get_pob(), lits);
        lemma->set_level(uses_level1);
    }
    else
    {TRACE("core_array_eq", tout << "Not-Inductive!\n";);}
}

void lemma_eq_generalizer::operator() (lemma_ref &lemma)
{
    TRACE("core_eq", tout << "Transforming equivalence classes\n";);

    if (lemma->get_cube().empty()) return;

    ast_manager &m = m_ctx.get_ast_manager();
    qe::term_graph egraph(m);
    egraph.add_lits(lemma->get_cube());

    // -- expand the cube with all derived equalities
    expr_ref_vector core(m);
    egraph.to_lits(core, true);

    // -- if the core looks different from the original cube
    if (core.size() != lemma->get_cube().size() ||
        core.get(0) != lemma->get_cube().get(0)) {
        // -- update the lemma
        lemma->update_cube(lemma->get_pob(), core);
    }
}
};
