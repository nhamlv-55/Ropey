from ExprDb import ExprDb
import z3
import logging
import argparse
import glob
import os
import json
import time
from itertools import chain, combinations
from termcolor import colored
import copy

import Doping.utils.utils as Du
class SpacerSolverProxyDb(object):
    def __init__(self, proxies_db):
        #map from proxy_lit to expr. Note that there maybe duplicated exprs
        self._proxies_db = proxies_db
    def size(self):
        return len(self._proxies_db)

    def find_lit(self, proxy_lit):
        '''
        return the constraint implied by the proxy literal
        '''
        return self._proxies_db[proxy_lit]

    def find_expr(self, e):
        '''
        return the first proxy that implies the constraint
        '''
        for (p,expr) in self._proxies_db.items():
            if e== expr:
                return p
        return None

    def add(self, e):
        # log.info("CURRENT SIZE", self.size())
        """Adds proxy and returns its literal"""
        new_lit = self.find_expr(e)
        if new_lit is not None:
            return new_lit
        else:
            new_lit = z3.Bool("spacer_proxy!#{}".format(self.size()))
            self._proxies_db[new_lit] = e
            return new_lit

    def dump(self):
        log.info("SIZE: %d", self.size())
        for (k,v) in self._proxies_db.items():
            log.info("%s <- %s", str(k), str(v))

    def push(self):
        pass
    def pop(self):
        pass

class SpacerSolver(object):
    def __init__(self, zsolver, edb):
        self._edb = edb
        self._zsolver = zsolver
        self._lvls = []
        self._proxies_db = SpacerSolverProxyDb(edb.proxies_db())
        self._active_lvl = None
    def add(self, e):
        """Add background assertion to the solver"""
        self._zsolver.add(e)

    def add_proxy(self, e):
        """Adds an assertion guarded by a Boolean literal and rerturns it"""
        # XXX if e is already a proxy return
        # XXX if e is a Bool constant return e and don't create a proxy
        proxy_lit = self._proxies_db.add(e)
        self._zsolver.add(z3.Implies(proxy_lit, e))
        # log.info("ADDING:\n", e, "<-", proxy_lit)
        return proxy_lit

    def get_proxy(self, lit):
        return self._proxies_db.find_lit(lit)

    def find_expr(self, e):
        return self._proxies_db.find_expr(e)
    def add_lvled(self, lvl, e):
        """Add an assertion at a specified lvl"""
        self.ensure_lvl(lvl)
        lvl_lit = self._mk_lvl_lit(lvl)
        self._zsolver.add(z3.Implies(lvl_lit, e))

    def ensure_lvl(self, lvl):
        log.info("LEN SELF._LVLS %d", len(self._lvls))
        """Ensure that solver has lvl number of lvls"""
        while (len(self._lvls) <= lvl):
            self._lvls.append(self._mk_lvl_lit(len(self._lvls)))

    def _mk_lvl_lit(self, lvl):
        if lvl < len(self._lvls):
            return self._lvls[lvl]

        lit = z3.Bool("lvl#{}".format(lvl))
        return z3.Not(lit)

    def activate_lvl(self, lvl):
        """Activate specified lvl"""
        self._active_lvl = lvl

    def get_active_lvl(self):
        """Return currently active lvl"""
        return self._active_lvl

    def lvls(self):
        """Return number of lvls"""
        return len(self._lvls)

    def check(self, _assumptions):
        assumptions = list()
        log.info("SELF.LVLS %s", self._lvls)
        log.info(self.get_active_lvl())
        if self.get_active_lvl() is not None:
            i = -1
            for i in range(0, min(len(self._lvls), self.get_active_lvl())):
                log.info("DISABLE lvl %d", i)
                assumptions.append(z3.mk_not(self._lvls[i]))
            for j in range(i+1, len(self._lvls)):
                log.info("ACTIVATE lvl %d", j)
                assumptions.append(self._lvls[j])

        #activate solver
        #FIXME
        solver_lit  = self._edb.get_solver_lit()
        ext_0_n_lit = z3.Not(self._edb.get_ext_lit())
        assumptions.append(solver_lit)
        assumptions.append(ext_0_n_lit)
        assumptions.extend(_assumptions)
        log.info("ASSUMPTIONs:\n%s", str(assumptions))
        res =  self._zsolver.check(*assumptions)

        # log.info("CHECKING:\n", self._zsolver)
        return res

    def unsat_core(self):
        core = self._zsolver.unsat_core()
        #return [v for v in core if v is not a lvl atom]
        return core

    def model(self):
        try:
            return self._zsolver.model()
        except Exception as e:
            return None

    def get_solver(self):
        return self._zsolver

    def push(self):
        assert(False)
        pass
    def pop(self):
        assert(False)
        pass


class InductiveGeneralizer(object):
    def __init__(self, solver, post_to_pre, use_unsat_core = True, lits_to_keep = []):
        self._solver = solver
        self._core = None
        self._post_to_pre = post_to_pre
        self._use_unsat_core = use_unsat_core
        self.lits_to_keep = lits_to_keep
        self.useful_time = 0
        self.wasted_time = 0
    def free_arith_vars(self, fml):
        '''Returns the set of all integer uninterpreted constants in a formula'''
        seen = set([])
        vars = set([])

        def fv(seen, vars, f):
            # log.info("F\t:\n", f)
            # log.info("SEEN\t:\n", seen)
            if f in seen:
                return
            seen |= { f }
            # log.info("FREE_ARITH_CHECK:\n\t". f, f.sort(), f.decl().kind())
            if f.decl().kind() == z3.Z3_OP_UNINTERPRETED:
                vars |= { f }
            for ch in f.children():
                fv(seen, vars, ch)
                fv(seen, vars, fml)
        fv(seen, vars, fml)
        return vars


    def _mk_pre(self, post_lit):
        # XXX Implement renaming
        # log.info("_MK_PRE", post_lit)
        post_vs = self.free_arith_vars(post_lit)
        # log.info("_MK_PRE post_vs", post_vs)
        # log.info(self._post_to_pre)
        submap = [(post_v, self._post_to_pre[post_v]) for post_v in post_vs]
        # log.info("_MK_PRE submap:\n", submap)
        pre_lit = z3.substitute(post_lit, submap)
        
        return pre_lit

    def check_inductive(self, cube, lvl):
        if len(cube)==0:
            return z3.sat
        saved_lvl = self._solver.get_active_lvl()
        self._solver.activate_lvl(lvl)

        log.info("checking inductive for cube:\n%s at lvl %s", cube, lvl)
        pre_lemma = [z3.mk_not(self._mk_pre(v)) for v in cube]

        pre_lemma_lit = self._solver.add_proxy(z3.Or(*pre_lemma))

        cube_lits = [self._solver.add_proxy(lit) for lit in cube]
        # self._solver._proxies_db.dump()
        log.debug("CUBE_LITS:\n")
        for proxy_lit in cube_lits:
            log.debug("%s : %s", proxy_lit, self._solver.get_proxy(proxy_lit))
        log.debug("PRE_LEMMA_LIT:\n %s : %s", pre_lemma_lit, self._solver.get_proxy(pre_lemma_lit))


        res = self._solver.check([pre_lemma_lit] + cube_lits)

        if res == z3.unsat:
            self._core = self._solver.unsat_core()

        # restore solver lvl for additional queries
        self._solver.activate_lvl(saved_lvl)

        return res


    def generalize(self, cube, lvl):
        """Inductive generalization of a cube given as a list"""
        #reorder cube
        # myorder = [12, 13, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        # cube = [cube[i] for i in myorder]
        # log.info("REORDERED CUBE:%s", cube)
        for i in range(0, len(cube)):
            if i in self.lits_to_keep:
                log.info("KEEP THIS LIT")
                continue
            log.info("TRYING TO DROP:%s", cube[i])
            saved_lit = cube[i]
            cube[i] = z3.BoolVal(True)
            t1 = time.time()
            res = self.check_inductive([v for v in cube if not z3.is_true(v)], lvl)
            t2 = time.time()
            if res == z3.unsat:
                self.useful_time += (t2-t1)
                # generalized
                # only keep literals in the cube if they are also in the unsat core
                # literals that are not in the unsat core are not needed for unsat
                log.info("DROP SUCCESSFUL. New cube is:")
                log.info([v for v in cube if not z3.is_true(v)])
                log.debug("UNSAT CORE:\n %s", self._solver.unsat_core())
                # use the unsat core
                for j in range(0, len(cube)):
                    if cube[j]==z3.BoolVal(True): continue
                    p = self._solver.find_expr(cube[j])
                    if p not in self._solver.unsat_core():
                        log.debug("%s <- %s is not in the UNSAT CORE. Drop"%(cube[j], p))
                        cube[j] = z3.BoolVal(True)
            else:
                # print("somehow wasted", i )
                self.wasted_time +=(t2-t1)
                # generalization failed, restore the literal
                cube[i] = saved_lit
                log.info("DROP FAILED")
                log.debug("WAS CHECKING:\n %s", self._solver.get_solver().sexpr())
                log.debug("MODEL: %s", self._solver.model())
                # compute generalized cube
                #safe to add because if i is in lits_to_keep, i has already been skipped earilier
                self.lits_to_keep.append(i)
        print("CANNOT DROP:", self.lits_to_keep)
        return [v for v in cube if not z3.is_true(v)]

def gen_datapoints(cube, inducted_cube, vocab, filename):
    for i in range(len(cube)):
        for j in range(i+1, len(cube)):
            '''4 possible labels: both lits are dropped 0, only one is dropped 1, non is dropped 2'''
            if cube[i] in inducted_cube and cube[j] in inducted_cube:
                label = 0
            elif cube[i] not in inducted_cube and cube[j] not in inducted_cube:
                label = 2
            else:
                label = 1

            C_tree = Du.ast_to_tree(z3.And(cube), vocab)
            L_a_tree = Du.ast_to_tree(cube[i], vocab)
            L_b_tree = Du.ast_to_tree(cube[j], vocab)

            datapoint = {"C_tree": C_tree.to_json(), "L_a_tree": L_a_tree.to_json(), "L_b_tree": L_b_tree.to_json(), "label": label}
            dp_filename = filename+ "."+ str(i)+ "."+ str(j)+ ".dp.json"
            with open(dp_filename, "w") as f:
                json.dump(datapoint, f)
    return vocab

def ind_gen(filename, lits_to_keep , vocab, drop_all = False, vis = False):
    '''
    lits_to_keep: a list of literal that we skip checking (== will be kept unless they are not in the unsat core)
    drop_all: whether we drop literals one by one or all at once
    vis: whether to dump a ind_gen visualization
    '''
    assert('zsolver' not in globals())
    zsolver = z3.Solver()
    zsolver.set('arith.solver', 6)
    edb = ExprDb(filename)
    cube = edb.get_cube()
    active_lvl = edb.get_active_lvl()
    log.info("PARSED CUBE:\n %s", cube)
    log.info("ACTIVATE LVL:\n %d", active_lvl)
    # log.info("POST2PRE: %s", edb.post2pre())
    s = SpacerSolver(zsolver, edb)
    for e in edb.get_others():
        s.add(e)
    lvls = edb.get_lvls()
    for lvl_lit in lvls:
        log.info("ADDING LEMMAS AT LVL %s", lvl_lit)
        for (lvl, e_lvl) in lvls[lvl_lit]:
            log.info("\t %s %s", lvl, e_lvl)
            s.add_lvled(lvl, e_lvl)

    generalizer = InductiveGeneralizer(s, edb.post2pre(), use_unsat_core = False, lits_to_keep = lits_to_keep)
    if drop_all:
        inducted_cube = []
        for i in range(len(cube)):
            if i in lits_to_keep:
                inducted_cube.append(cube[i])
        #validate
        log.info("FINAL CUBE:\n%s", z3.And(inducted_cube))
        before_gen = time.time()
        res = generalizer.check_inductive(inducted_cube, active_lvl)
        after_gen = time.time()
        log.info(res)
        assert(res==z3.unsat)
    else:
        before_gen = time.time()
        inducted_cube = generalizer.generalize(copy.deepcopy(cube), active_lvl)
        after_gen = time.time()
        #validate
        log.info("FINAL CUBE:\n%s", z3.And(inducted_cube))
        res = generalizer.check_inductive(inducted_cube, active_lvl)
        log.info(res)
        assert(res==z3.unsat)

    #visualization
    if vis:
        for l in cube:
            if l in inducted_cube:
                print(colored("||\t"+str(l), 'green'))
            else:
                print(colored("||\t"+str(l), 'red'))
    #generate dataset
    if vocab is not None:
        if len(cube)>1:
            vocab = gen_datapoints(cube, inducted_cube, vocab, filename)

    del edb
    del zsolver
    return {"useful": generalizer.useful_time, "wasted": generalizer.wasted_time, "lits_to_keep": generalizer.lits_to_keep, "ind_gen_time": after_gen - before_gen}

def powerset(policy):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    return chain.from_iterable(combinations(policy, r) for r in range(len(policy)+1))

def ind_gen_folder(folder, policy_file, use_powerset, vis, vocab):
    total_useful = 0
    total_wasted = 0
    running_times = []
    policy = {}
    if policy_file is not None:
        with open(policy_file, "r") as f:
            policy = json.load(f)
    queries = glob.glob(folder+"/*.smt2")
    for q in queries[:40]:
        print(q)
        if q in policy:
            base_policy = policy[q]
            print("BASE POLICY:%s"%str(base_policy))
            res = ind_gen(q, base_policy, drop_all = True)
            print("DROPPING ALL AT ONE:", res["ind_gen_time"])
            if use_powerset:
                power_policies  = list(powerset(base_policy))
                print(power_policies)
                results = {}
                for p in power_policies:
                    lits_to_keep = sorted(list(p))
                    #has to parse a copy of the lits_to_keep
                    res = ind_gen(q, lits_to_keep[:], vocab = vocab, vis = vis)
                    log.info("Trying %s in %s"%(str(lits_to_keep), str(res["ind_gen_time"])))
                    total_useful += res["useful"]
                    total_wasted += res["wasted"]
                    results[tuple(lits_to_keep)] = res["ind_gen_time"]
                #sort res to check if dropping all dropable lits is the best policy
                sorted_res = [(k, v) for k, v in sorted(results.items(), key=lambda item: item[1])]
                print(sorted_res)
                base_policy = tuple(sorted(base_policy))
                best_policy = sorted_res[0][0]
                running_times.append({"query": q, "best": sorted_res[0][1], "best_policy": sorted_res[0][0], "base_policy": base_policy, "drop_all": drop_all_runtime, "full_run": str(sorted_res)})
                if base_policy != best_policy:
                    print("WARNING: not the best policy. Best: %s. Base: %s"%(best_policy, base_policy))

            else:
                res = ind_gen(q, policy[q], vis = vis)
                total_useful += res["useful"]
                total_wasted +=res["wasted"]
                policy[q] = res["lits_to_keep"]

        else:
            res = ind_gen(q, [], vocab = vocab, vis = vis)
            total_useful += res["useful"]
            total_wasted +=res["wasted"]
            policy[q] = res["lits_to_keep"]
    print("Total useful:", total_useful)
    print("Total wasted:", total_wasted)
    with open(os.path.join(folder, "policy.json"), "w") as f:
        json.dump(policy, f, indent = 4)
    with open(os.path.join(folder, "running_times.json"), "w") as f:
        json.dump(running_times, f, indent = 4)
    if vocab is not None:
        vocab.save(os.path.join(folder, "vocab.json"))
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-input', help='could be a smt2 file or a folder')
    parser.add_argument('-policy', help='a json policy file')
    parser.add_argument("-l", "--log", dest="logLevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='CRITICAL', help="Set the logging level")
    parser.add_argument('-powerset', action='store_true')
    parser.add_argument('-vis', action='store_true')
    parser.add_argument('-gen_dataset', action='store_true')
    args = parser.parse_args()
    print(args.logLevel)
    print(getattr(logging, args.logLevel))
    log = logging.getLogger(__name__)
    log.setLevel(getattr(logging, args.logLevel))
    # logging.basicConfig(level=getattr(logging, args.logLevel))
    if args.gen_dataset:
        vocab = Du.Vocab()
    else:
        vocab = None
    if os.path.isdir(args.input):
        ind_gen_folder(args.input, args.policy, args.powerset, args.vis, vocab = vocab)
    elif os.path.isfile(args.input):
        ind_gen(filename = args.input, lits_to_keep = [] , vocab = vocab, drop_all = False, vis = args.vis)
    else:
        print("not a file or folder")
   
