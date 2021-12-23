/*++
Copyright (c) 2017 Microsoft Corporation and Arie Gurfinkel

Module Name:

    spacer_generalizers.h

Abstract:

    Generalizer plugins.

Author:

    Nikolaj Bjorner (nbjorner) 2011-11-22.
    Arie Gurfinkel
Revision History:

--*/

#ifndef _SPACER_GENERALIZERS_H_
#define _SPACER_GENERALIZERS_H_

#include "ast/arith_decl_plugin.h"
#include "muz/spacer/spacer_context.h"

#include "muz/spacer/spacer_grpc_bridge.h"
namespace spacer {

// can be used to check whether produced core is really implied by
// frame and therefore valid TODO: or negation?
class lemma_sanity_checker : public lemma_generalizer {
  public:
    lemma_sanity_checker(context &ctx) : lemma_generalizer(ctx) {}
    ~lemma_sanity_checker() override {}
    void operator()(lemma_ref &lemma) override;
};

/**
 * Boolean inductive generalization by dropping literals
 */
class lemma_bool_inductive_generalizer : public lemma_generalizer {

    struct stats {
        unsigned count;
        unsigned num_failures;
        stopwatch watch;
        stats() { reset(); }
        void reset() {
            count = 0;
            num_failures = 0;
            watch.reset();
        }
    };

    unsigned m_failure_limit;
    bool m_array_only;
    stats m_st;
    bool m_use_expansion; // whether to try literal expansion or not. Default = True
    bool m_1st_query = true; //we need to dump a seed smt2 file. After dumping, set this flag to false
  public:
    lemma_bool_inductive_generalizer(context &ctx, unsigned failure_limit,
                                     bool use_expansion = true,
                                     bool array_only = false )
        : lemma_generalizer(ctx), m_failure_limit(failure_limit),
          m_array_only(array_only), m_use_expansion(use_expansion) {}
    ~lemma_bool_inductive_generalizer() override {}
    void operator()(lemma_ref &lemma) override;

    void collect_statistics(statistics &st) const override;
    void reset_statistics() override { m_st.reset(); }
};

/**
 * Heuristic-based Boolean inductive generalization by dropping literals
 */
class h_inductive_generalizer : public lemma_generalizer {

    struct stats {
        unsigned count;
        unsigned num_failures;
        stopwatch watch;
        stopwatch outside_time_watch;
        stopwatch ind_gen_q_watch;
        stats() { reset(); }
        void reset() {
            count = 0;
            num_failures = 0;
            watch.reset();
        }
    };

  struct literal_stats {
    unsigned fst_seen_can_drop;
    unsigned fst_seen_cannot_drop;

    literal_stats() { reset(); }

    void reset() {
      fst_seen_can_drop = 0;
      fst_seen_cannot_drop = 0;
    }

    double fst_seen_success_rate() {
      if ((fst_seen_can_drop + fst_seen_cannot_drop) == 0) {
        return 0;
      }
      return double(fst_seen_can_drop) /
             double(fst_seen_can_drop + fst_seen_cannot_drop);
    }

    unsigned n_lits() { return fst_seen_can_drop + fst_seen_cannot_drop; }
  };

    struct lit_info {
        unsigned seen;
        unsigned success;
        unsigned index;

        lit_info() { reset(); }

        void reset() {
            seen = 1;
            success = 0;
            index = -1;
        }

        double success_rate() { return double(success) / double(seen); }

    };

    struct grpc_info {
        unsigned total_requests;
        unsigned dirty_requests;
        unsigned unsuccessful_answers;

        grpc_info(){reset();}

        void reset(){
            total_requests = 0;
            dirty_requests = 0;
            unsuccessful_answers = 0;
        }

        void dump(){
            std::cerr<<"total_requests:"<<total_requests<<"\n";
            std::cerr<<"dirty_requests:"<<dirty_requests<<"\n";
            std::cerr<<"unsuccessful_answers:"<<unsuccessful_answers<<"\n";

        }

    };


  // to flip a coin
  random_gen m_random;
  // first value in the vector is how many times we have seen the lit so far.
  // second value is how many times we were able to drop it
  obj_map<expr, lit_info*> m_lit2count;
  ast_manager &m;
  expr_ref_vector m_lits;
  // unsigned m_lemma_counter = 0; // How many lemmas have we generalized so
  // far. Looks like we can piggyback on m_st.count

  unsigned m_heu_index; // What heuristic to use

  unsigned m_threshold; // How many lemmas should we have seen before activating
                        // the heuristic

  const float SUCCESS_THRES = 0.7;

  unsigned m_lemmas_sent = 0;
  bool m_1st_query = true; //we need to dump a seed smt2 file. After dumping, set this flag to false
  unsigned m_failure_limit;
  bool m_array_only;
  stats m_st;
  
  literal_stats m_lit_st;
  GrpcClient m_grpc_conn;
    grpc_info m_grpc_info;
public:
  h_inductive_generalizer(context &ctx, unsigned failure_limit,
                          unsigned threshold, unsigned heu_index,
                          unsigned random_seed, symbol host_port)
      : lemma_generalizer(ctx), m_failure_limit(failure_limit),
        m(ctx.get_ast_manager()), m_lits(m), m_threshold(threshold),
        m_random(random_seed), m_heu_index(heu_index),
        m_grpc_conn(grpc::CreateChannel(host_port.str(), grpc::InsecureChannelCredentials())){
    STRACE("spacer.h_ind_gen", tout << "Create h_indgen"
                                    << "\n";);
    STRACE("spacer.h_ind_gen", tout << "Connecting to grpc server at"<<host_port.str()
           << "\n";);


  }
  ~h_inductive_generalizer() override {}
  void operator()(lemma_ref &lemma) override;

  void collect_statistics(statistics &st) const override;
  void reset_statistics() override { m_st.reset(); }
  void increase_lit_count(expr_ref &lit);
  double lit_success_rate(
      expr_ref &lit); // return -1 if this is the first time we see
                      // the lit. Other wise return the success rate
  void dump_lit_count();
  bool should_try_drop(const expr_ref_vector &cube, const std::vector<unsigned> &kept_lits, const unsigned &checking_lit, const std::vector<unsigned> &to_be_checked_lits); 
    bool query_mask(const expr_ref_vector &cube, std::vector<unsigned> &kept_lits, std::vector<unsigned> &to_be_checked_lits, std::vector<unsigned> &checking_lits, std::vector<unsigned> &mask, const bool last_ans_success, const bool first_query);
  bool yesno(float prob); // return true with probability prob
};

class unsat_core_generalizer : public lemma_generalizer {
  struct stats {
    unsigned count;
    unsigned num_failures;
    stopwatch watch;
    stats() { reset(); }
    void reset() {
      count = 0;
      num_failures = 0;
      watch.reset();
    }
  };

  stats m_st;

public:
  unsat_core_generalizer(context &ctx) : lemma_generalizer(ctx) {}
  ~unsat_core_generalizer() override {}
  void operator()(lemma_ref &lemma) override;

  void collect_statistics(statistics &st) const override;
  void reset_statistics() override { m_st.reset(); }
};

class lemma_array_eq_generalizer : public lemma_generalizer {
  private:
    bool is_array_eq(ast_manager &m, expr *e);

  public:
    lemma_array_eq_generalizer(context &ctx) : lemma_generalizer(ctx) {}
    ~lemma_array_eq_generalizer() override {}
    void operator()(lemma_ref &lemma) override;
};

class lemma_eq_generalizer : public lemma_generalizer {
  public:
    lemma_eq_generalizer(context &ctx) : lemma_generalizer(ctx) {}
    ~lemma_eq_generalizer() override {}
    void operator()(lemma_ref &lemma) override;
};

class lemma_quantifier_generalizer : public lemma_generalizer {
    struct stats {
        unsigned count;
        unsigned num_failures;
        stopwatch watch;
        stats() { reset(); }
        void reset() {
            count = 0;
            num_failures = 0;
            watch.reset();
        }
    };

    ast_manager &m;
    arith_util m_arith;
    stats m_st;
    expr_ref_vector m_cube;

    bool m_normalize_cube;
    int m_offset;

  public:
    lemma_quantifier_generalizer(context &ctx, bool normalize_cube = true);
    ~lemma_quantifier_generalizer() override {}
    void operator()(lemma_ref &lemma) override;

    void collect_statistics(statistics &st) const override;
    void reset_statistics() override { m_st.reset(); }

  private:
    bool generalize(lemma_ref &lemma, app *term);

    void find_candidates(expr *e, app_ref_vector &candidate);
    bool is_ub(var *var, expr *e);
    bool is_lb(var *var, expr *e);
    void mk_abs_cube(lemma_ref &lemma, app *term, var *var,
                     expr_ref_vector &gnd_cube, expr_ref_vector &abs_cube,
                     expr *&lb, expr *&ub, unsigned &stride);

    bool match_sk_idx(expr *e, app_ref_vector const &zks, expr *&idx, app *&sk);
    void cleanup(expr_ref_vector &cube, app_ref_vector const &zks,
                 expr_ref &bind);

    bool find_stride(expr_ref_vector &c, expr_ref &pattern, unsigned &stride);
};

class limit_num_generalizer : public lemma_generalizer {

    struct stats {
        unsigned count;
        unsigned num_failures;
        stopwatch watch;
        stats() { reset(); }
        void reset() {
            count = 0;
            num_failures = 0;
            watch.reset();
        }
    };

    unsigned m_failure_limit;
    stats m_st;

    bool limit_denominators(expr_ref_vector &lits, rational &limit);

  public:
    limit_num_generalizer(context &ctx, unsigned failure_limit);
    ~limit_num_generalizer() override {}

    void operator()(lemma_ref &lemma) override;

    void collect_statistics(statistics &st) const override;
    void reset_statistics() override { m_st.reset(); }
};

/* To snap values to a sticky points */
class snap_val_generalizer : public lemma_generalizer {

    struct stats {
        unsigned count;
        unsigned num_failures;
        stopwatch watch;
        stats() { reset(); }
        void reset() {
            count = 0;
            num_failures = 0;
            watch.reset();
        }
    };

    unsigned m_failure_limit;
    stats m_st;

    bool snap_vals(expr_ref_vector &lits, int sticky_point, double epsilon);

public:
    snap_val_generalizer(context &ctx, unsigned failure_limit);
    ~snap_val_generalizer() override {}

    void operator()(lemma_ref &lemma) override;

    void collect_statistics(statistics &st) const override;
    void reset_statistics() override { m_st.reset(); }
};
} // namespace spacer

#endif
