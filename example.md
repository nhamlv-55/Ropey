---
layout: page
title: "MOTIVATING EXAMPLE"
permalink: /example/
---


Here is the running time of solving chc-lra-0055.smt2 from CHC-COMP 2018
```
(:SPACER-inductive-level                              1
 :SPACER-max-depth                                    4
 :SPACER-max-query-lvl                                4
 :SPACER-num-active-lemmas                            229
 :SPACER-num-invariants                               317
 :SPACER-num-is_invariant                             257
 :SPACER-num-lemma-jumped                             3
 :SPACER-num-lemmas                                   440
 :SPACER-num-pobs                                     376
 :SPACER-num-propagations                             87
 :SPACER-num-queries                                  435
 :added-eqs                                           5072742
 :arith-eq-adapter                                    1109764
 :arith-bound-propagations-cheap                      3307914
 :arith-bound-propagations-lp                         56280
 :arith-conflicts                                     2820
 :arith-diseq                                         5477260
 :arith-fixed-eqs                                     4312
 :arith-lower                                         2864554
 :arith-make-feasible                                 497618
 :arith-max-columns                                   1350
 :arith-max-rows                                      1044
 :arith-propagations                                  3307914
 :arith-rows                                          127276
 :arith-upper                                         3164062
 :bool-inductive-gen                                  1806
 :bool-inductive-gen-failures                         789
 :conflicts                                           162218
 :decisions                                           2504392
 :del-clause                                          1401612
 :final-checks                                        2788
 :iuc_solver.num_proxies                              1940
 :minimized-lits                                      1515864
 :mk-bool-var                                         931146
 :mk-clause                                           4937822
 :num-checks                                          7138
 :pool_solver.checks                                  3569
 :pool_solver.checks.sat                              1394
 :propagations                                        37778920
 :restarts                                            1000
 :time.iuc_solver.get_iuc                             37.27
 :time.iuc_solver.get_iuc.hyp_reduce1                 5.07
 :time.iuc_solver.get_iuc.hyp_reduce2                 26.27
 :time.iuc_solver.get_iuc.learn_core                  1.18
 :time.pool_solver.proof                              7.29
 :time.pool_solver.smt.total                          573.56
 :time.pool_solver.smt.total.sat                      281.45
 :time.spacer.ctp                                     0.07
 :time.spacer.init_rules                              0.02
 :time.spacer.init_rules.pt.init                      0.01
 :time.spacer.mbp                                     1.23
 :time.spacer.solve                                   621.91
 :time.spacer.solve.propagate                         25.15
 :time.spacer.solve.reach                             596.76
 :time.spacer.solve.reach.children                    5.70
 :time.spacer.solve.reach.gen.bool_ind                223.30
 :time.spacer.solve.reach.gen.bool_ind.outside_spacer 1.96)
```
There are a lot of information, but we only need to care about the following lines
```
 :time.spacer.solve                                   621.91
 :time.spacer.solve.reach.gen.bool_ind                223.30
```
The first line measures the total solving time, and the second line measures time spent on doing `inductive generalization`. As we can see, more than one third of the time
is spent in inductive generalization.

Plotting the P+ and P- matrices, as described in the paper, we get

![](/XP.svg)

Top to bottom, we have P+ (brighter the cell, bigger the value), P+ normalized (all non-zero cells are equally bright), P-, P- normalized.

There are some patterns in it, and we started this project by implementing handcrafted heuristics that we thought could capture the patterns, but unfortunately they
didn't work consistantly.
