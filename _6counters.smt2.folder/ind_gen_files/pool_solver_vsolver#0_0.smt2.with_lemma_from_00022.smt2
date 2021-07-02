(set-info :status unsat)
(declare-fun state_8_n () Int)
(declare-fun state_3_n () Int)
(declare-fun state_12_n () Bool)
(declare-fun state_11_n () Bool)
(declare-fun state_10_n () Bool)
(declare-fun state_9_n () Bool)
(declare-fun state_0_n () Bool)
(declare-fun state_1_n () Bool)
(declare-fun state_2_n () Bool)
(declare-fun state_4_n () Bool)
(declare-fun state_5_n () Bool)
(declare-fun state_7_n () Bool)
(declare-fun state_6_n () Bool)
(declare-fun |vsolver#0| () Bool)
(declare-fun state__tr1 () Bool)
(declare-fun state_3_0 () Int)
(declare-fun state_2_0 () Bool)
(declare-fun state_1_0 () Bool)
(declare-fun state_0_0 () Bool)
(declare-fun state_7_0 () Bool)
(declare-fun state_12_0 () Bool)
(declare-fun state_9_0 () Bool)
(declare-fun state_11_0 () Bool)
(declare-fun state_10_0 () Bool)
(declare-fun state_8_0 () Int)
(declare-fun state_6_0 () Bool)
(declare-fun state_5_0 () Bool)
(declare-fun state_4_0 () Bool)
(declare-fun state_14_n () Int)
(declare-fun state__tr0 () Bool)
(declare-fun |state#level_0!3| () Bool)
(declare-fun |state#reach_tag_0_0| () Bool)
(declare-fun spacer_proxy!0 () Bool)
(declare-fun |state#level_1!7| () Bool)
(declare-fun spacer_proxy!1 () Bool)
(declare-fun spacer_proxy!2 () Bool)
(declare-fun spacer_proxy!3 () Bool)
(declare-fun spacer_proxy!4 () Bool)
(declare-fun spacer_proxy!5 () Bool)
(declare-fun spacer_proxy!6 () Bool)
(declare-fun spacer_proxy!7 () Bool)
(declare-fun spacer_proxy!8 () Bool)
(declare-fun spacer_proxy!9 () Bool)
(declare-fun spacer_proxy!10 () Bool)
(declare-fun |state#level_2!8| () Bool)
(declare-fun spacer_proxy!11 () Bool)
(declare-fun spacer_proxy!12 () Bool)
(declare-fun state_ext0_n () Bool)
(declare-fun |state#level_3!9| () Bool)
(declare-fun |state#level_4!11| () Bool)
(declare-fun |state#level_5!13| () Bool)
(assert (let ((a!1 (not (or state_6_n
                    state_7_n
                    state_5_n
                    state_4_n
                    state_2_n
                    state_1_n
                    state_0_n
                    state_9_n
                    state_10_n
                    state_11_n
                    (not state_12_n)
                    (not (= state_3_n 0))
                    (not (= state_8_n 0))))))
  (or (not state__tr1) (not |vsolver#0|) a!1)))
(assert (let ((a!1 (or (not (or (not state_1_0) (not state_2_0)))
               (not (or state_2_0 (not state_0_0)))))
      (a!2 (or (not (or state_2_0 (not state_1_0)))
               (not (or state_0_0 state_1_0 (not state_2_0)))))
      (a!3 (or (= state_3_0 5) (= (+ state_3_n (* (- 1) state_3_0)) 1)))
      (a!4 (not (or (not (= state_3_0 5)) (= state_3_n 1)))))
(let ((a!5 (or (= (not state_4_n) state_0_n)
               (= (not state_5_n) state_1_n)
               (= (not state_6_n) state_2_n)
               (not (= state_8_n state_3_n))
               (= (not state_10_n) state_7_n)
               (= (not state_11_n) state_9_n)
               (not (= state_14_n state_3_n))
               (= (not state_4_0) state_0_0)
               (= (not state_5_0) state_1_0)
               (= (not state_6_0) state_2_0)
               (not (= state_8_0 state_3_0))
               (= (not state_10_0) state_7_0)
               (= (not state_11_0) state_9_0)
               (= (not (= state_3_n 5)) state_9_n)
               (= (not (= state_3_0 5)) state_9_0)
               (= (= (not state_7_0) state_9_0) state_12_0)
               (= (= (not state_7_n) state_9_n) state_12_n)
               (= (or (not state_0_n) (not state_2_n)) state_7_n)
               (= (or (not state_0_0) (not state_2_0)) state_7_0)
               (= (not state_0_n) a!1)
               (= (not state_1_n) a!2)
               (= state_2_n state_2_0)
               (not a!3)
               a!4)))
  (or (not state__tr0) (not |vsolver#0|) (not a!5)))))
(assert (or (not state__tr0) |state#level_0!3| (not |vsolver#0|)))
(assert (let ((a!1 (not (or state_2_0
                    state_6_0
                    state_10_0
                    state_0_0
                    state_1_0
                    state_4_0
                    state_5_0
                    state_7_0
                    state_9_0
                    state_11_0
                    (not state_12_0)
                    (not (= state_3_0 0))
                    (not (= state_8_0 0))))))
  (or (not state__tr0) |state#reach_tag_0_0| a!1 (not |vsolver#0|))))
(assert (or (not state__tr0) (not |vsolver#0|) (not spacer_proxy!0)))
(assert (or state_12_n |state#level_0!3| (not |vsolver#0|)))
(assert (or state_12_0 (not state__tr0) (not |vsolver#0|) |state#level_1!7|))
(assert (or (not |vsolver#0|) (not spacer_proxy!1) (not (>= state_3_n 4))))
(assert (or (= state_6_n state_2_n) (not |vsolver#0|) (not spacer_proxy!2)))
(assert (or (not |vsolver#0|) (not (>= state_3_n 5)) (not spacer_proxy!3)))
(assert (or (= state_7_n state_9_n) (not |vsolver#0|) (not spacer_proxy!4)))
(assert (or (not |vsolver#0|)
    (not spacer_proxy!5)
    (= (+ state_3_n (* (- 1) state_8_n)) 0)))
(assert (or (= state_4_n state_0_n) (not |vsolver#0|) (not spacer_proxy!6)))
(assert (or (= state_11_n state_9_n) (not |vsolver#0|) (not spacer_proxy!7)))
(assert (or (= state_5_n state_1_n) (not |vsolver#0|) (not spacer_proxy!8)))
(assert (or (= state_10_n state_7_n) (not |vsolver#0|) (not spacer_proxy!9)))
(assert (or (not state_0_n) |state#level_0!3| (not |vsolver#0|)))
(assert (or (not state_0_0) (not state__tr0) (not |vsolver#0|) |state#level_1!7|))
(assert (or (not |vsolver#0|) (= state_3_n 4) (not spacer_proxy!10)))
(assert (or |state#level_0!3| (not |vsolver#0|) (not (= state_3_n 4))))
(assert (or (not state__tr0) (not |vsolver#0|) |state#level_1!7| (not (= state_3_0 4))))
(assert (or state_12_n (not |vsolver#0|) |state#level_1!7|))
(assert (or state_12_0 (not state__tr0) (not |vsolver#0|) |state#level_2!8|))
(assert (or (not |vsolver#0|) (not spacer_proxy!11) (= state_3_n 3)))
(assert (or (not state_1_n) |state#level_0!3| (not |vsolver#0|)))
(assert (or (not state_1_0) (not state__tr0) (not |vsolver#0|) |state#level_1!7|))
(assert (or (not state_2_0)
    (not state_1_0)
    (not state__tr0)
    (not |vsolver#0|)
    (not spacer_proxy!12)))
;; extra clause
(assert (or state_ext0_n state__tr0 state__tr1 ))
(check-sat |vsolver#0|
 spacer_proxy!12
 (not state_ext0_n)
 |state#level_0!3|
 (not |state#level_1!7|)
 (not |state#level_2!8|)
 (not |state#level_3!9|)
 (not |state#level_4!11|)
 (not |state#level_5!13|)
 state_2_n
 state_1_n
)
(act-lvl -1)
(ind-gen (and state_1_n state_0_n (not state_2_n))
)
(exit)
(:added-eqs                      166
 :arith-eq-adapter               41
 :arith-bound-propagations-cheap 79
 :arith-bound-propagations-lp    21
 :arith-conflicts                1
 :arith-diseq                    71
 :arith-lower                    94
 :arith-make-feasible            47
 :arith-max-columns              12
 :arith-max-rows                 5
 :arith-propagations             79
 :arith-rows                     70
 :arith-upper                    72
 :conflicts                      22
 :decisions                      210
 :del-clause                     67
 :final-checks                   12
 :mk-bool-var                    259
 :mk-clause                      430
 :num-checks                     25
 :propagations                   1520)
(params arith.solver 6 random_seed 0 dump_benchmarks true dump_threshold -10 mbqi true arith.ignore_int true array.weak true)