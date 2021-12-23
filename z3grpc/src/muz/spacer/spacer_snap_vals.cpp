/*++
  Copyright (c) 2019 Microsoft Corporation and Arie Gurfinkel

  Module Name:

  spacer_snap_vals.cpp

  Abstract:

  Arithmetic-related generalizers

  Author:

  Arie Gurfinkel

  Revision History:

  --*/

#include<cmath>
#include "ast/rewriter/rewriter.h"
#include "ast/rewriter/rewriter_def.h"
#include "muz/spacer/spacer_generalizers.h"
#include "smt/smt_solver.h"

namespace spacer {

namespace {
/* Snap all values those are close enough to the sticky point*/
struct snap_val_rewriter_cfg : public default_rewriter_cfg {
    ast_manager &m;
    arith_util m_arith;
    int m_sticky_point;
    double m_epsilon;

  snap_val_rewriter_cfg(ast_manager &manager, int sticky_point, double epsilon)
    : m(manager), m_arith(m), m_sticky_point(sticky_point), m_epsilon(epsilon) {}

    bool is_numeral(func_decl *f, rational &val, bool &is_int) {
        if (f->get_family_id() == m_arith.get_family_id() &&
            f->get_decl_kind() == OP_NUM) {
            val = f->get_parameter(0).get_rational();
            is_int = f->get_parameter(1).get_int() != 0;
            return true;
        }
        return false;
    }

    bool snap_val(rational &num) {
        if (std::fabs(num.get_double() - m_sticky_point) < m_epsilon) {
            num = m_sticky_point / 1;
            return true;
        }
        return false;
    }

    br_status reduce_app(func_decl *f, unsigned num, expr *const *args,
                         expr_ref &result, proof_ref &result_pr) {
        bool is_int;
        rational val;

        if (is_numeral(f, val, is_int) && !is_int) {
            if (snap_val(val)) {
                result = m_arith.mk_numeral(val, false);
                return BR_DONE;
            }
        }
        return BR_FAILED;
    }
};
} // namespace
snap_val_generalizer::snap_val_generalizer(context &ctx,
                                             unsigned failure_limit)
    : lemma_generalizer(ctx), m_failure_limit(failure_limit) {}

bool snap_val_generalizer::snap_vals(expr_ref_vector &lits,
                                      int sticky_point, double epsilon) {
  ast_manager &m = m_ctx.get_ast_manager();
  snap_val_rewriter_cfg rw_cfg(m, sticky_point, epsilon);
  rewriter_tpl<snap_val_rewriter_cfg> rw(m, false, rw_cfg);

  expr_ref lit(m);
  bool dirty = false;
  for (unsigned i = 0, sz = lits.size(); i < sz; ++i) {
    rw(lits.get(i), lit);
    dirty |= (lits.get(i) != lit.get());
    lits[i] = lit;
  }
  return dirty;
}


void snap_val_generalizer::operator()(lemma_ref &lemma) {
    if (lemma->get_cube().empty()) return;

    m_st.count++;
    scoped_watch _w_(m_st.watch);

    unsigned uses_level;
    pred_transformer &pt = lemma->get_pob()->pt();
    ast_manager &m = pt.get_ast_manager();

    expr_ref_vector cube(m);
    int sticky_point = 0;
    double epsilon = 0.01;
    // create a solver to check whether updated cube is in a generalization
    ref<solver> sol = mk_smt_solver(m, params_ref::get_empty(), symbol::null);
    SASSERT(lemma->has_pob());
    sol->assert_expr(lemma->get_pob()->post());
    unsigned weakness = lemma->weakness();
    cube.reset();
    cube.append(lemma->get_cube());
    // try to limit denominators
    //        if (!limit_denominators(cube, limit)) return;
    // try to snap coefficient
    if(!snap_vals(cube, sticky_point, epsilon)) return;
    bool failed = false;
    // check that pob->post() ==> cube
    for (auto *lit : cube) {
        solver::scoped_push _p_(*sol);
        expr_ref nlit(m);
        nlit = m.mk_not(lit);
        sol->assert_expr(nlit);
        lbool res = sol->check_sat(0, nullptr);
        if (res == l_false) {
            // good
            TRACE("spacer.snap", tout << "Successfully generalize: "
                << lemma->get_cube()
                << "\ninto\n"
                << cube << "\n";);
        } else {
            failed = true;
            TRACE("spacer.snap", tout << "Failed to generalize: "
                    << lemma->get_cube()
                    << "\ninto\n"
                    << cube << "\n";);
            break;
        }
    }

    // check that !cube & F & Tr ==> !cube'
    if (!failed && pt.check_inductive(lemma->level(), cube, uses_level, weakness)) {
        TRACE("spacer",
                tout << "Reduced fractions from:\n"
                << lemma->get_cube() << "\n\nto\n"
                << cube << "\n";);
        lemma->update_cube(lemma->get_pob(), cube);
        lemma->set_level(uses_level);
        // done
        return;
    }
    ++m_st.num_failures;
}

void snap_val_generalizer::collect_statistics(statistics &st) const {
    st.update("time.spacer.solve.reach.gen.snap_val", m_st.watch.get_seconds());
    st.update("snap val", m_st.count);
    st.update("snap val failures", m_st.num_failures);
}
} // namespace spacer
