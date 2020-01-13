(set-info :status sat)
(declare-fun |vsolver#1| () Bool)
(declare-fun BwdInv__tr1 () Bool)
(declare-fun BwdInv_7_n () Bool)
(declare-fun aux!12_n () Real)
(declare-fun BwdInv_6_n () Real)
(declare-fun aux!3_n () Real)
(declare-fun BwdInv_13_n () Bool)
(declare-fun BwdInv_5_n () Real)
(declare-fun aux!4_n () Real)
(declare-fun BwdInv_12_n () Bool)
(declare-fun BwdInv_4_n () Real)
(declare-fun aux!5_n () Real)
(declare-fun BwdInv_11_n () Bool)
(declare-fun BwdInv_3_n () Real)
(declare-fun aux!6_n () Real)
(declare-fun BwdInv_10_n () Bool)
(declare-fun BwdInv_2_n () Real)
(declare-fun aux!7_n () Real)
(declare-fun BwdInv_9_n () Bool)
(declare-fun BwdInv_1_n () Real)
(declare-fun aux!8_n () Real)
(declare-fun BwdInv_8_n () Bool)
(declare-fun BwdInv_0_n () Real)
(declare-fun aux!9_n () Real)
(declare-fun aux!15_n () Real)
(declare-fun BwdInv_2_0 () Real)
(declare-fun aux!17_n () Real)
(declare-fun BwdInv_0_0 () Real)
(declare-fun aux!16_n () Real)
(declare-fun BwdInv_1_0 () Real)
(declare-fun aux!14_n () Real)
(declare-fun BwdInv_3_0 () Real)
(declare-fun aux!13_n () Real)
(declare-fun BwdInv_4_0 () Real)
(declare-fun aux!10_n () Real)
(declare-fun BwdInv_6_0 () Real)
(declare-fun aux!11_n () Real)
(declare-fun BwdInv_5_0 () Real)
(declare-fun BwdInv_7_0 () Bool)
(declare-fun BwdInv_8_0 () Bool)
(declare-fun BwdInv_10_0 () Bool)
(declare-fun BwdInv_9_0 () Bool)
(declare-fun BwdInv_11_0 () Bool)
(declare-fun BwdInv_12_0 () Bool)
(declare-fun BwdInv_13_0 () Bool)
(declare-fun BwdInv__tr0 () Bool)
(declare-fun |BwdInv#level_0!18| () Bool)
(declare-fun |BwdInv#reach_tag_0_0| () Bool)
(declare-fun spacer_proxy!0 () Bool)
(declare-fun spacer_proxy!1 () Bool)
(declare-fun spacer_proxy!2 () Bool)
(declare-fun spacer_proxy!3 () Bool)
(declare-fun spacer_proxy!4 () Bool)
(declare-fun spacer_proxy!5 () Bool)
(declare-fun spacer_proxy!6 () Bool)
(declare-fun spacer_proxy!7 () Bool)
(declare-fun |BwdInv#level_1!21| () Bool)
(declare-fun spacer_proxy!8 () Bool)
(declare-fun spacer_proxy!9 () Bool)
(declare-fun spacer_proxy!10 () Bool)
(declare-fun spacer_proxy!11 () Bool)
(declare-fun BwdInv_ext0_n () Bool)
(declare-fun |BwdInv#level_2!22| () Bool)
(declare-fun |BwdInv#level_3!24| () Bool)
(declare-fun |BwdInv#level_4!26| () Bool)
(assert (or BwdInv_7_n (not BwdInv__tr1) (not |vsolver#1|)))
(assert (let ((a!1 (>= (+ (* (/ 9.0 16.0) aux!5_n)
                  (* (- (/ 11.0 32.0)) aux!8_n)
                  (* (/ 19.0 32.0) aux!3_n)
                  (* (/ 37.0 32.0) aux!4_n)
                  (* (- (/ 13.0 16.0)) aux!6_n)
                  (* (/ 7.0 32.0) aux!7_n)
                  (* (- (/ 3.0 4.0)) aux!9_n)
                  (* (/ 1.0 32.0) aux!12_n))
               (- (/ 1.0 32.0))))
      (a!2 (<= (+ (* (/ 3.0 4.0) aux!5_n)
                  (* (/ 5.0 32.0) aux!8_n)
                  (* (/ 21.0 32.0) aux!3_n)
                  (* (- (/ 19.0 32.0)) aux!4_n)
                  (* (- (/ 3.0 8.0)) aux!6_n)
                  (* (/ 1.0 32.0) aux!7_n)
                  (* (- (/ 7.0 8.0)) aux!9_n)
                  (* (- (/ 1.0 16.0)) aux!12_n))
               (- (/ 1.0 16.0))))
      (a!3 (>= (+ (* (/ 7.0 32.0) aux!5_n)
                  (* (/ 1.0 32.0) aux!8_n)
                  (* (- (/ 5.0 16.0)) aux!3_n)
                  (* (/ 3.0 8.0) aux!6_n)
                  (* (/ 1.0 2.0) aux!7_n)
                  (* (/ 7.0 16.0) aux!9_n)
                  (* (/ 1.0 16.0) aux!12_n))
               0.0))
      (a!4 (<= (+ (* (/ 19.0 32.0) aux!5_n)
                  (* (/ 5.0 16.0) aux!8_n)
                  (* (/ 1.0 32.0) aux!3_n)
                  (* (- (/ 1.0 4.0)) aux!4_n)
                  (* (- (/ 23.0 32.0)) aux!6_n)
                  (* (- (/ 13.0 16.0)) aux!7_n)
                  (* (- (/ 3.0 8.0)) aux!9_n))
               (/ 1.0 32.0)))
      (a!5 (<= (+ (* (/ 1.0 4.0) aux!5_n)
                  (* (- (/ 1.0 16.0)) aux!8_n)
                  (* (/ 1.0 32.0) aux!3_n)
                  (* (- (/ 3.0 32.0)) aux!4_n)
                  (* (- (/ 13.0 32.0)) aux!6_n)
                  (* (- (/ 3.0 8.0)) aux!7_n)
                  (* (- (/ 5.0 32.0)) aux!9_n)
                  (* (/ 1.0 8.0) aux!12_n))
               (- (/ 1.0 32.0))))
      (a!6 (>= (+ (* (/ 9.0 16.0) aux!5_n)
                  (* (- (/ 7.0 32.0)) aux!8_n)
                  (* (- (/ 9.0 16.0)) aux!3_n)
                  (* (- (/ 3.0 32.0)) aux!4_n)
                  (* (- (/ 11.0 32.0)) aux!6_n)
                  (* (/ 7.0 32.0) aux!7_n)
                  (* (/ 5.0 16.0) aux!9_n)
                  (* (- (/ 1.0 32.0)) aux!12_n))
               0.0))
      (a!7 (>= (+ (* (/ 3.0 16.0) aux!5_n)
                  (* (/ 15.0 16.0) aux!8_n)
                  (* (- (/ 3.0 32.0)) aux!3_n)
                  (* (- (/ 17.0 32.0)) aux!4_n)
                  (* (- (/ 11.0 16.0)) aux!6_n)
                  (* (/ 1.0 32.0) aux!7_n)
                  (* (/ 7.0 16.0) aux!9_n)
                  (* (/ 3.0 32.0) aux!12_n))
               0.0)))
(let ((a!8 (ite a!2
                (= (+ BwdInv_5_0
                      (* (/ 3.0 4.0) aux!5_n)
                      (* (/ 5.0 32.0) aux!8_n)
                      (* (/ 21.0 32.0) aux!3_n)
                      (* (- (/ 19.0 32.0)) aux!4_n)
                      (* (- (/ 3.0 8.0)) aux!6_n)
                      (* (/ 1.0 32.0) aux!7_n)
                      (* (- (/ 7.0 8.0)) aux!9_n)
                      (* (- (/ 1.0 16.0)) aux!12_n))
                   (- (/ 1.0 16.0)))
                (= BwdInv_5_0 aux!11_n)))
      (a!9 (ite a!1
                (= (+ BwdInv_6_0
                      (* (- (/ 9.0 16.0)) aux!5_n)
                      (* (/ 11.0 32.0) aux!8_n)
                      (* (- (/ 19.0 32.0)) aux!3_n)
                      (* (- (/ 37.0 32.0)) aux!4_n)
                      (* (/ 13.0 16.0) aux!6_n)
                      (* (- (/ 7.0 32.0)) aux!7_n)
                      (* (/ 3.0 4.0) aux!9_n)
                      (* (- (/ 1.0 32.0)) aux!12_n))
                   (/ 1.0 32.0))
                (= BwdInv_6_0 aux!10_n)))
      (a!10 (ite a!3
                 (= (+ BwdInv_4_0
                       (* (- (/ 7.0 32.0)) aux!5_n)
                       (* (- (/ 1.0 32.0)) aux!8_n)
                       (* (/ 5.0 16.0) aux!3_n)
                       (* (- (/ 3.0 8.0)) aux!6_n)
                       (* (- (/ 1.0 2.0)) aux!7_n)
                       (* (- (/ 7.0 16.0)) aux!9_n)
                       (* (- (/ 1.0 16.0)) aux!12_n))
                    0.0)
                 (= BwdInv_4_0 aux!13_n)))
      (a!11 (ite a!5
                 (= (+ BwdInv_3_0
                       (* (/ 1.0 4.0) aux!5_n)
                       (* (- (/ 1.0 16.0)) aux!8_n)
                       (* (/ 1.0 32.0) aux!3_n)
                       (* (- (/ 3.0 32.0)) aux!4_n)
                       (* (- (/ 13.0 32.0)) aux!6_n)
                       (* (- (/ 3.0 8.0)) aux!7_n)
                       (* (- (/ 5.0 32.0)) aux!9_n)
                       (* (/ 1.0 8.0) aux!12_n))
                    (- (/ 1.0 32.0)))
                 (= BwdInv_3_0 aux!14_n)))
      (a!12 (ite a!6
                 (= (+ BwdInv_1_0
                       (* (- (/ 9.0 16.0)) aux!5_n)
                       (* (/ 7.0 32.0) aux!8_n)
                       (* (/ 9.0 16.0) aux!3_n)
                       (* (/ 3.0 32.0) aux!4_n)
                       (* (/ 11.0 32.0) aux!6_n)
                       (* (- (/ 7.0 32.0)) aux!7_n)
                       (* (- (/ 5.0 16.0)) aux!9_n)
                       (* (/ 1.0 32.0) aux!12_n))
                    0.0)
                 (= BwdInv_1_0 aux!16_n)))
      (a!13 (ite a!7
                 (= (+ BwdInv_0_0
                       (* (- (/ 3.0 16.0)) aux!5_n)
                       (* (- (/ 15.0 16.0)) aux!8_n)
                       (* (/ 3.0 32.0) aux!3_n)
                       (* (/ 17.0 32.0) aux!4_n)
                       (* (/ 11.0 16.0) aux!6_n)
                       (* (- (/ 1.0 32.0)) aux!7_n)
                       (* (- (/ 7.0 16.0)) aux!9_n)
                       (* (- (/ 3.0 32.0)) aux!12_n))
                    0.0)
                 (= BwdInv_0_0 aux!17_n)))
      (a!14 (ite a!4
                 (= (+ BwdInv_2_0
                       (* (/ 19.0 32.0) aux!5_n)
                       (* (/ 5.0 16.0) aux!8_n)
                       (* (/ 1.0 32.0) aux!3_n)
                       (* (- (/ 1.0 4.0)) aux!4_n)
                       (* (- (/ 23.0 32.0)) aux!6_n)
                       (* (- (/ 13.0 16.0)) aux!7_n)
                       (* (- (/ 3.0 8.0)) aux!9_n))
                    (/ 1.0 32.0))
                 (= BwdInv_2_0 aux!15_n))))
(let ((a!15 (or (= BwdInv_13_0 a!1)
                (= BwdInv_12_0 a!2)
                (= BwdInv_11_0 a!3)
                (= BwdInv_9_0 a!4)
                (= BwdInv_10_0 a!5)
                (= BwdInv_8_0 a!6)
                (= BwdInv_7_0 a!7)
                (not a!8)
                (not a!9)
                (not a!10)
                (not a!11)
                (not a!12)
                (not a!13)
                (not a!14)
                (not (ite BwdInv_7_n (= aux!9_n 0.0) (= aux!9_n BwdInv_0_n)))
                (not (ite BwdInv_8_n (= aux!8_n 0.0) (= aux!8_n BwdInv_1_n)))
                (not (ite BwdInv_9_n (= aux!7_n 0.0) (= aux!7_n BwdInv_2_n)))
                (not (ite BwdInv_10_n (= aux!6_n 0.0) (= aux!6_n BwdInv_3_n)))
                (not (ite BwdInv_11_n (= aux!5_n 0.0) (= aux!5_n BwdInv_4_n)))
                (not (ite BwdInv_12_n (= aux!4_n 0.0) (= aux!4_n BwdInv_5_n)))
                (not (ite BwdInv_13_n (= aux!3_n 0.0) (= aux!3_n BwdInv_6_n)))
                (not (>= aux!12_n (/ 3.0 32.0)))
                (not (<= aux!12_n (/ 1.0 8.0))))))
  (or (not BwdInv__tr0) (not |vsolver#1|) (not a!15))))))
(assert (or (not BwdInv__tr0) |BwdInv#level_0!18| (not |vsolver#1|)))
(assert (or BwdInv_7_0 (not BwdInv__tr0) |BwdInv#reach_tag_0_0| (not |vsolver#1|)))
(assert (or (= BwdInv_3_n 0.0) (not spacer_proxy!0) (not |vsolver#1|)))
(assert (or (= BwdInv_6_n (- (/ 1.0 32.0))) (not spacer_proxy!1) (not |vsolver#1|)))
(assert (or (= BwdInv_4_n (/ 1.0 16.0)) (not spacer_proxy!2) (not |vsolver#1|)))
(assert (or (= BwdInv_2_n (/ 1.0 32.0)) (not spacer_proxy!3) (not |vsolver#1|)))
(assert (or (= BwdInv_1_n (/ 1.0 16.0)) (not spacer_proxy!4) (not |vsolver#1|)))
(assert (or (= BwdInv_0_n (/ 1.0 8.0)) (not spacer_proxy!5) (not |vsolver#1|)))
(assert (or (= BwdInv_5_n (- (/ 1.0 32.0))) (not spacer_proxy!6) (not |vsolver#1|)))
(assert (or BwdInv_7_0 (not BwdInv__tr0) (not |vsolver#1|) (not spacer_proxy!7)))
(assert (or BwdInv_7_n |BwdInv#level_0!18| (not |vsolver#1|)))
(assert (or BwdInv_7_0 (not BwdInv__tr0) |BwdInv#level_1!21| (not |vsolver#1|)))
(assert (or BwdInv_7_0
    BwdInv_8_0
    BwdInv_9_0
    BwdInv_11_0
    (not BwdInv__tr0)
    (not (= BwdInv_0_0 (/ 1.0 8.0)))
    (not (= BwdInv_1_0 (/ 1.0 16.0)))
    (not (= BwdInv_2_0 (/ 1.0 32.0)))
    (not (= BwdInv_4_0 (/ 1.0 16.0)))
    (not BwdInv_10_0)
    (not BwdInv_12_0)
    (not BwdInv_13_0)
    (not |vsolver#1|)
    (not spacer_proxy!8)))
(assert (or BwdInv_7_0
    BwdInv_8_0
    BwdInv_9_0
    BwdInv_11_0
    (not BwdInv__tr0)
    (not (= BwdInv_0_0 (/ 1.0 8.0)))
    (not (= BwdInv_1_0 (/ 1.0 16.0)))
    (not (= BwdInv_2_0 (/ 1.0 32.0)))
    (not (= BwdInv_4_0 (/ 1.0 16.0)))
    (not BwdInv_12_0)
    (not BwdInv_13_0)
    (not |vsolver#1|)
    (not spacer_proxy!9)))
(assert (or BwdInv_7_0
    BwdInv_8_0
    BwdInv_9_0
    BwdInv_11_0
    (not BwdInv__tr0)
    (not (= BwdInv_0_0 (/ 1.0 8.0)))
    (not (= BwdInv_1_0 (/ 1.0 16.0)))
    (not (= BwdInv_2_0 (/ 1.0 32.0)))
    (not (= BwdInv_4_0 (/ 1.0 16.0)))
    (not BwdInv_10_0)
    (not BwdInv_13_0)
    (not |vsolver#1|)
    (not spacer_proxy!10)))
(assert (or BwdInv_7_0
    BwdInv_8_0
    BwdInv_9_0
    BwdInv_11_0
    (not BwdInv__tr0)
    (not (= BwdInv_0_0 (/ 1.0 8.0)))
    (not (= BwdInv_1_0 (/ 1.0 16.0)))
    (not (= BwdInv_2_0 (/ 1.0 32.0)))
    (not (= BwdInv_4_0 (/ 1.0 16.0)))
    (not BwdInv_10_0)
    (not BwdInv_12_0)
    (not |vsolver#1|)
    (not spacer_proxy!11)))
;; extra clause
(assert (or BwdInv_ext0_n BwdInv__tr0 BwdInv__tr1 ))
(check-sat |vsolver#1|
 spacer_proxy!11
 (not BwdInv_ext0_n)
 |BwdInv#level_0!18|
 (not |BwdInv#level_1!21|)
 (not |BwdInv#level_2!22|)
 (not |BwdInv#level_3!24|)
 (not |BwdInv#level_4!26|)
 (not BwdInv_9_n)
 (not BwdInv_8_n)
 BwdInv_10_n
 spacer_proxy!5
 (not BwdInv_7_n)
 spacer_proxy!4
 spacer_proxy!2
 BwdInv_12_n
 (not BwdInv_11_n)
 spacer_proxy!3
)
(exit)
(:added-eqs          119
 :arith-add-rows     129
 :arith-assert-diseq 33
 :arith-assert-lower 106
 :arith-assert-upper 79
 :arith-bound-prop   31
 :arith-conflicts    1
 :arith-eq-adapter   34
 :arith-pivots       17
 :conflicts          6
 :decisions          119
 :del-clause         56
 :final-checks       4
 :mk-bool-var        208
 :mk-clause          297
 :num-checks         8
 :propagations       436
 :time               0.00)
(params arith.solver 2 random_seed 0 dump_benchmarks true dump_threshold 0.00 mbqi true arith.ignore_int true array.weak true)