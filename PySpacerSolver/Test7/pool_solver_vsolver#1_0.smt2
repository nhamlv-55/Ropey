(set-info :status unsat)
(declare-fun aux!2_n () Real)
(declare-fun aux!9_n () Real)
(declare-fun aux!8_n () Real)
(declare-fun aux!7_n () Real)
(declare-fun aux!6_n () Real)
(declare-fun aux!5_n () Real)
(declare-fun aux!4_n () Real)
(declare-fun aux!3_n () Real)
(declare-fun INV_6_n () Real)
(declare-fun INV_5_n () Real)
(declare-fun INV_4_n () Real)
(declare-fun INV_3_n () Real)
(declare-fun INV_2_n () Real)
(declare-fun INV_1_n () Real)
(declare-fun INV_0_n () Real)
(declare-fun INV_6_0 () Real)
(declare-fun INV_5_0 () Real)
(declare-fun INV_3_0 () Real)
(declare-fun INV_4_0 () Real)
(declare-fun INV_2_0 () Real)
(declare-fun INV_1_0 () Real)
(declare-fun INV_0_0 () Real)
(declare-fun |vsolver#1| () Bool)
(declare-fun INV__tr1 () Bool)
(declare-fun INV__tr0 () Bool)
(declare-fun |INV#level_0!10| () Bool)
(declare-fun |INV#reach_tag_0_0| () Bool)
(declare-fun spacer_proxy!0 () Bool)
(declare-fun spacer_proxy!1 () Bool)
(declare-fun spacer_proxy!2 () Bool)
(declare-fun INV_ext0_n () Bool)
(declare-fun |INV#level_1!13| () Bool)
(assert (let ((a!1 (not (= (+ INV_0_n
                      (* (- (/ 3.0 32.0)) aux!2_n)
                      (* (/ 3.0 32.0) aux!3_n)
                      (* (/ 17.0 32.0) aux!4_n)
                      (* (- (/ 3.0 16.0)) aux!5_n)
                      (* (/ 11.0 16.0) aux!6_n)
                      (* (- (/ 1.0 32.0)) aux!7_n)
                      (* (- (/ 15.0 16.0)) aux!8_n)
                      (* (- (/ 7.0 16.0)) aux!9_n))
                   0.0)))
      (a!2 (not (= (+ INV_1_n
                      (* (/ 1.0 32.0) aux!2_n)
                      (* (/ 9.0 16.0) aux!3_n)
                      (* (/ 3.0 32.0) aux!4_n)
                      (* (- (/ 9.0 16.0)) aux!5_n)
                      (* (/ 11.0 32.0) aux!6_n)
                      (* (- (/ 7.0 32.0)) aux!7_n)
                      (* (/ 7.0 32.0) aux!8_n)
                      (* (- (/ 5.0 16.0)) aux!9_n))
                   0.0)))
      (a!3 (not (= (+ INV_2_n
                      (* (/ 1.0 32.0) aux!3_n)
                      (* (- (/ 1.0 4.0)) aux!4_n)
                      (* (/ 19.0 32.0) aux!5_n)
                      (* (- (/ 23.0 32.0)) aux!6_n)
                      (* (- (/ 13.0 16.0)) aux!7_n)
                      (* (/ 5.0 16.0) aux!8_n)
                      (* (- (/ 3.0 8.0)) aux!9_n))
                   (/ 1.0 32.0))))
      (a!4 (not (= (+ INV_3_n
                      (* (/ 1.0 8.0) aux!2_n)
                      (* (/ 1.0 32.0) aux!3_n)
                      (* (- (/ 3.0 32.0)) aux!4_n)
                      (* (/ 1.0 4.0) aux!5_n)
                      (* (- (/ 13.0 32.0)) aux!6_n)
                      (* (- (/ 3.0 8.0)) aux!7_n)
                      (* (- (/ 1.0 16.0)) aux!8_n)
                      (* (- (/ 5.0 32.0)) aux!9_n))
                   (- (/ 1.0 32.0)))))
      (a!5 (not (= (+ INV_4_n
                      (* (- (/ 1.0 16.0)) aux!2_n)
                      (* (/ 5.0 16.0) aux!3_n)
                      (* (- (/ 7.0 32.0)) aux!5_n)
                      (* (- (/ 3.0 8.0)) aux!6_n)
                      (* (- (/ 1.0 2.0)) aux!7_n)
                      (* (- (/ 1.0 32.0)) aux!8_n)
                      (* (- (/ 7.0 16.0)) aux!9_n))
                   0.0)))
      (a!6 (not (= (+ INV_5_n
                      (* (- (/ 1.0 16.0)) aux!2_n)
                      (* (/ 21.0 32.0) aux!3_n)
                      (* (- (/ 19.0 32.0)) aux!4_n)
                      (* (/ 3.0 4.0) aux!5_n)
                      (* (- (/ 3.0 8.0)) aux!6_n)
                      (* (/ 1.0 32.0) aux!7_n)
                      (* (/ 5.0 32.0) aux!8_n)
                      (* (- (/ 7.0 8.0)) aux!9_n))
                   (- (/ 1.0 16.0)))))
      (a!7 (not (= (+ INV_6_n
                      (* (- (/ 1.0 32.0)) aux!2_n)
                      (* (- (/ 19.0 32.0)) aux!3_n)
                      (* (- (/ 37.0 32.0)) aux!4_n)
                      (* (- (/ 9.0 16.0)) aux!5_n)
                      (* (/ 13.0 16.0) aux!6_n)
                      (* (- (/ 7.0 32.0)) aux!7_n)
                      (* (/ 11.0 32.0) aux!8_n)
                      (* (/ 3.0 4.0) aux!9_n))
                   (/ 1.0 32.0)))))
(let ((a!8 (or (not (ite (>= INV_0_0 0.0) (= aux!9_n INV_0_0) (= aux!9_n 0.0)))
               (not (ite (>= INV_1_0 0.0) (= aux!8_n INV_1_0) (= aux!8_n 0.0)))
               (not (ite (>= INV_2_0 0.0) (= aux!7_n INV_2_0) (= aux!7_n 0.0)))
               (not (ite (>= INV_4_0 0.0) (= aux!5_n INV_4_0) (= aux!5_n 0.0)))
               (not (ite (>= INV_3_0 0.0) (= aux!6_n INV_3_0) (= aux!6_n 0.0)))
               (not (ite (>= INV_5_0 0.0) (= aux!4_n INV_5_0) (= aux!4_n 0.0)))
               (not (ite (>= INV_6_0 0.0) (= aux!3_n INV_6_0) (= aux!3_n 0.0)))
               a!1
               a!2
               a!3
               a!4
               a!5
               a!6
               a!7
               (not (>= aux!2_n (/ 3.0 32.0)))
               (not (<= aux!2_n (/ 1.0 8.0))))))
  (or (not INV__tr1) (not |vsolver#1|) (not a!8)))))
(assert (let ((a!1 (not (or (not (= INV_0_n (/ 1.0 8.0)))
                    (not (= INV_1_n (/ 1.0 16.0)))
                    (not (= INV_2_n (/ 1.0 32.0)))
                    (not (= INV_3_n 0.0))
                    (not (= INV_4_n (/ 1.0 16.0)))
                    (not (= INV_5_n (- (/ 1.0 32.0))))
                    (not (= INV_6_n (- (/ 1.0 32.0))))))))
  (or (not INV__tr0) (not |vsolver#1|) a!1)))
(assert (or (not INV__tr1) |INV#level_0!10| (not |vsolver#1|)))
(assert (let ((a!1 (not (or (not (= INV_0_0 (/ 1.0 8.0)))
                    (not (= INV_1_0 (/ 1.0 16.0)))
                    (not (= INV_2_0 (/ 1.0 32.0)))
                    (not (= INV_3_0 0.0))
                    (not (= INV_4_0 (/ 1.0 16.0)))
                    (not (= INV_5_0 (- (/ 1.0 32.0))))
                    (not (= INV_6_0 (- (/ 1.0 32.0))))))))
  (or (not INV__tr1) |INV#reach_tag_0_0| a!1 (not |vsolver#1|))))
(assert (or (not spacer_proxy!0) (not (>= INV_0_n 0.0)) (not |vsolver#1|)))
(assert (or (not |vsolver#1|) (not (>= INV_0_n (/ 1.0 8.0))) (not spacer_proxy!1)))
(assert (or (not INV__tr1)
    (not |vsolver#1|)
    (>= INV_0_0 (/ 1.0 8.0))
    (not spacer_proxy!2)))
;; extra clause
(assert (or INV_ext0_n INV__tr0 INV__tr1 ))
(check-sat |vsolver#1|
 spacer_proxy!2
 (not INV_ext0_n)
 (not |INV#level_0!10|)
 (not |INV#level_1!13|)
 spacer_proxy!1
)
(exit)
(:arith-assert-diseq 1
 :arith-assert-upper 3
 :arith-eq-adapter   21
 :conflicts          2
 :del-clause         1
 :mk-bool-var        109
 :mk-clause          167
 :num-checks         2
 :propagations       13
 :time               0.00)
(params arith.solver 2 random_seed 0 dump_benchmarks true dump_threshold 0.00 mbqi true arith.ignore_int true array.weak true)