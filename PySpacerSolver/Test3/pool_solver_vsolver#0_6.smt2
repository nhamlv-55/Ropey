(set-info :status sat)
(declare-fun |vsolver#0| () Bool)
(declare-fun BwdInv__tr1 () Bool)
(declare-fun BwdInv_4_n () Bool)
(declare-fun aux!5_n () Real)
(declare-fun aux!8_n () Real)
(declare-fun aux!6_n () Real)
(declare-fun BwdInv_5_0 () Bool)
(declare-fun BwdInv_1_n () Real)
(declare-fun aux!7_n () Real)
(declare-fun BwdInv_2_n () Real)
(declare-fun BwdInv_5_n () Bool)
(declare-fun BwdInv_0_n () Real)
(declare-fun BwdInv_3_n () Bool)
(declare-fun aux!2_n () Real)
(declare-fun BwdInv_2_0 () Real)
(declare-fun aux!4_n () Real)
(declare-fun BwdInv_0_0 () Real)
(declare-fun aux!3_n () Real)
(declare-fun BwdInv_1_0 () Real)
(declare-fun BwdInv_4_0 () Bool)
(declare-fun BwdInv_3_0 () Bool)
(declare-fun BwdInv__tr0 () Bool)
(declare-fun |BwdInv#level_0!9| () Bool)
(declare-fun |BwdInv#reach_tag_0_0| () Bool)
(declare-fun spacer_proxy!0 () Bool)
(declare-fun spacer_proxy!1 () Bool)
(declare-fun spacer_proxy!2 () Bool)
(declare-fun spacer_proxy!3 () Bool)
(declare-fun |BwdInv#level_1!13| () Bool)
(declare-fun spacer_proxy!4 () Bool)
(declare-fun spacer_proxy!5 () Bool)
(declare-fun spacer_proxy!6 () Bool)
(declare-fun spacer_proxy!7 () Bool)
(declare-fun spacer_proxy!8 () Bool)
(declare-fun spacer_proxy!9 () Bool)
(declare-fun spacer_proxy!10 () Bool)
(declare-fun spacer_proxy!11 () Bool)
(declare-fun spacer_proxy!12 () Bool)
(declare-fun spacer_proxy!13 () Bool)
(declare-fun spacer_proxy!14 () Bool)
(declare-fun spacer_proxy!15 () Bool)
(declare-fun spacer_proxy!16 () Bool)
(declare-fun BwdInv_ext0_n () Bool)
(declare-fun |BwdInv#level_2!14| () Bool)
(declare-fun |BwdInv#level_3!15| () Bool)
(declare-fun |BwdInv#level_4!17| () Bool)
(assert (or BwdInv_4_n (not BwdInv__tr1) (not |vsolver#0|)))
(assert (let ((a!1 (<= (+ (* (/ 1.0 16.0) aux!5_n)
                  (* (/ 9.0 8.0) aux!6_n)
                  (* (- (/ 11.0 32.0)) aux!7_n)
                  (* (- (/ 1.0 4.0)) aux!8_n))
               (/ 1.0 16.0)))
      (a!2 (<= (+ (* (/ 5.0 16.0) aux!5_n)
                  (* (- (/ 29.0 32.0)) aux!6_n)
                  (* (/ 3.0 32.0) aux!7_n)
                  (* (/ 5.0 16.0) aux!8_n))
               (/ 1.0 32.0)))
      (a!5 (>= (+ (* (/ 3.0 32.0) aux!5_n)
                  (* (/ 7.0 8.0) aux!6_n)
                  (* (- (/ 5.0 16.0)) aux!8_n))
               0.0)))
(let ((a!3 (ite a!2
                (= (+ BwdInv_1_0
                      (* (/ 5.0 16.0) aux!5_n)
                      (* (- (/ 29.0 32.0)) aux!6_n)
                      (* (/ 3.0 32.0) aux!7_n)
                      (* (/ 5.0 16.0) aux!8_n))
                   (/ 1.0 32.0))
                (= BwdInv_1_0 aux!3_n)))
      (a!4 (ite a!1
                (= (+ BwdInv_0_0
                      (* (/ 1.0 16.0) aux!5_n)
                      (* (/ 9.0 8.0) aux!6_n)
                      (* (- (/ 11.0 32.0)) aux!7_n)
                      (* (- (/ 1.0 4.0)) aux!8_n))
                   (/ 1.0 16.0))
                (= BwdInv_0_0 aux!4_n)))
      (a!6 (ite a!5
                (= (+ BwdInv_2_0
                      (* (- (/ 3.0 32.0)) aux!5_n)
                      (* (- (/ 7.0 8.0)) aux!6_n)
                      (* (/ 5.0 16.0) aux!8_n))
                   0.0)
                (= BwdInv_2_0 aux!2_n))))
(let ((a!7 (or (= BwdInv_3_0 a!1)
               (= BwdInv_4_0 a!2)
               (not a!3)
               (not a!4)
               (not a!6)
               (not (ite BwdInv_3_n (= aux!8_n 0.0) (= aux!8_n BwdInv_0_n)))
               (not (ite BwdInv_5_n (= aux!6_n 0.0) (= aux!6_n BwdInv_2_n)))
               (not (ite BwdInv_4_n (= aux!7_n 0.0) (= aux!7_n BwdInv_1_n)))
               (= BwdInv_5_0 a!5)
               (not (>= aux!5_n (/ 3.0 32.0)))
               (not (<= aux!5_n (/ 1.0 8.0))))))
  (or (not BwdInv__tr0) (not |vsolver#0|) (not a!7))))))
(assert (or (not BwdInv__tr0) |BwdInv#level_0!9| (not |vsolver#0|)))
(assert (or BwdInv_4_0 (not BwdInv__tr0) |BwdInv#reach_tag_0_0| (not |vsolver#0|)))
(assert (or (= BwdInv_2_n (/ 3.0 32.0)) (not spacer_proxy!0) (not |vsolver#0|)))
(assert (or (= BwdInv_1_n (/ 3.0 32.0)) (not spacer_proxy!1) (not |vsolver#0|)))
(assert (or (= BwdInv_0_n 0.0) (not spacer_proxy!2) (not |vsolver#0|)))
(assert (or BwdInv_4_0 (not BwdInv__tr0) (not |vsolver#0|) (not spacer_proxy!3)))
(assert (or BwdInv_4_n |BwdInv#level_0!9| (not |vsolver#0|)))
(assert (or BwdInv_4_0 (not BwdInv__tr0) |BwdInv#level_1!13| (not |vsolver#0|)))
(assert (or BwdInv_4_0
    BwdInv_5_0
    BwdInv_3_0
    (not BwdInv__tr0)
    (not (= BwdInv_0_0 0.0))
    (not (= BwdInv_1_0 (/ 3.0 32.0)))
    (not (= BwdInv_2_0 (/ 3.0 32.0)))
    (not |vsolver#0|)
    (not spacer_proxy!4)))
(assert (or BwdInv_4_0
    BwdInv_5_0
    (not BwdInv__tr0)
    (not (= BwdInv_0_0 0.0))
    (not (= BwdInv_1_0 (/ 3.0 32.0)))
    (not (= BwdInv_2_0 (/ 3.0 32.0)))
    (not |vsolver#0|)
    (not spacer_proxy!5)))
(assert (or BwdInv_5_0
    (not BwdInv__tr0)
    (not (= BwdInv_0_0 0.0))
    (not (= BwdInv_1_0 (/ 3.0 32.0)))
    (not (= BwdInv_2_0 (/ 3.0 32.0)))
    (not |vsolver#0|)
    (not spacer_proxy!6)))
(assert (or BwdInv_4_0
    (not BwdInv__tr0)
    (not (= BwdInv_0_0 0.0))
    (not (= BwdInv_1_0 (/ 3.0 32.0)))
    (not (= BwdInv_2_0 (/ 3.0 32.0)))
    (not |vsolver#0|)
    (not spacer_proxy!7)))
(assert (or BwdInv_4_0
    BwdInv_5_0
    (not BwdInv__tr0)
    (not (= BwdInv_0_0 0.0))
    (not (= BwdInv_1_0 (/ 3.0 32.0)))
    (not |vsolver#0|)
    (not spacer_proxy!8)))
(assert (or (not |vsolver#0|) (<= BwdInv_2_n (/ 3.0 32.0)) (not spacer_proxy!9)))
(assert (or BwdInv_4_0
    BwdInv_5_0
    (not BwdInv__tr0)
    (not (= BwdInv_0_0 0.0))
    (not (= BwdInv_1_0 (/ 3.0 32.0)))
    (not |vsolver#0|)
    (not spacer_proxy!10)
    (not (<= BwdInv_2_0 (/ 3.0 32.0)))))
(assert (or (not |vsolver#0|) (>= BwdInv_2_n (/ 3.0 32.0)) (not spacer_proxy!11)))
(assert (or BwdInv_4_0
    BwdInv_5_0
    (not BwdInv__tr0)
    (not (= BwdInv_0_0 0.0))
    (not (= BwdInv_1_0 (/ 3.0 32.0)))
    (not |vsolver#0|)
    (not spacer_proxy!12)
    (not (>= BwdInv_2_0 (/ 3.0 32.0)))))
(assert (or BwdInv_4_0
    BwdInv_5_0
    (not BwdInv__tr0)
    (not (= BwdInv_0_0 0.0))
    (not |vsolver#0|)
    (not (>= BwdInv_2_0 (/ 3.0 32.0)))
    (not spacer_proxy!13)))
(assert (or (not |vsolver#0|) (<= BwdInv_1_n (/ 3.0 32.0)) (not spacer_proxy!14)))
(assert (or BwdInv_4_0
    BwdInv_5_0
    (not BwdInv__tr0)
    (not (= BwdInv_0_0 0.0))
    (not |vsolver#0|)
    (not (>= BwdInv_2_0 (/ 3.0 32.0)))
    (not spacer_proxy!15)
    (not (<= BwdInv_1_0 (/ 3.0 32.0)))))
(assert (or BwdInv_4_0
    BwdInv_5_0
    (not BwdInv__tr0)
    (not |vsolver#0|)
    (not (>= BwdInv_2_0 (/ 3.0 32.0)))
    (not (<= BwdInv_1_0 (/ 3.0 32.0)))
    (not spacer_proxy!16)))
;; extra clause
(assert (or BwdInv_ext0_n BwdInv__tr0 BwdInv__tr1 ))
(check-sat |vsolver#0|
 spacer_proxy!16
 (not BwdInv_ext0_n)
 |BwdInv#level_0!9|
 (not |BwdInv#level_1!13|)
 (not |BwdInv#level_2!14|)
 (not |BwdInv#level_3!15|)
 (not |BwdInv#level_4!17|)
 spacer_proxy!14
 (not BwdInv_4_n)
 (not BwdInv_5_n)
 spacer_proxy!11
)
(exit)
(:added-eqs          131
 :arith-add-rows     89
 :arith-assert-diseq 45
 :arith-assert-lower 113
 :arith-assert-upper 95
 :arith-bound-prop   21
 :arith-conflicts    3
 :arith-eq-adapter   28
 :arith-fixed-eqs    9
 :arith-offset-eqs   2
 :arith-pivots       25
 :conflicts          14
 :decisions          153
 :del-clause         66
 :final-checks       7
 :mk-bool-var        186
 :mk-clause          196
 :num-checks         15
 :propagations       461
 :time               0.01)
(params arith.solver 2 random_seed 0 dump_benchmarks true dump_threshold 0.00 mbqi true arith.ignore_int true array.weak true)