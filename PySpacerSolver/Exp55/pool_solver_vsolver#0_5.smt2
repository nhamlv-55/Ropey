(set-info :status sat)
(declare-fun aux!5_n () Real)
(declare-fun aux!2_n () Real)
(declare-fun INV_2_n () Real)
(declare-fun aux!8_n () Real)
(declare-fun aux!6_n () Real)
(declare-fun aux!3_n () Real)
(declare-fun INV_1_n () Real)
(declare-fun aux!7_n () Real)
(declare-fun aux!4_n () Real)
(declare-fun INV_0_n () Real)
(declare-fun INV_2_0 () Real)
(declare-fun INV_5_0 () Bool)
(declare-fun INV_1_0 () Real)
(declare-fun INV_4_0 () Bool)
(declare-fun INV_4_n () Bool)
(declare-fun INV_0_0 () Real)
(declare-fun INV_3_0 () Bool)
(declare-fun INV_3_n () Bool)
(declare-fun INV_5_n () Bool)
(declare-fun |vsolver#0| () Bool)
(declare-fun INV__tr1 () Bool)
(declare-fun INV__tr0 () Bool)
(declare-fun |INV#level_0!9| () Bool)
(declare-fun |INV#reach_tag_0_0| () Bool)
(declare-fun |INV#level_1!13| () Bool)
(declare-fun spacer_proxy!0 () Bool)
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
(declare-fun spacer_proxy!11 () Bool)
(declare-fun |INV#level_2!14| () Bool)
(declare-fun spacer_proxy!12 () Bool)
(declare-fun spacer_proxy!13 () Bool)
(declare-fun spacer_proxy!14 () Bool)
(declare-fun spacer_proxy!15 () Bool)
(declare-fun spacer_proxy!16 () Bool)
(declare-fun spacer_proxy!17 () Bool)
(declare-fun spacer_proxy!18 () Bool)
(declare-fun spacer_proxy!19 () Bool)
(declare-fun spacer_proxy!20 () Bool)
(declare-fun spacer_proxy!21 () Bool)
(declare-fun spacer_proxy!22 () Bool)
(declare-fun spacer_proxy!23 () Bool)
(declare-fun spacer_proxy!24 () Bool)
(declare-fun spacer_proxy!25 () Bool)
(declare-fun spacer_proxy!26 () Bool)
(declare-fun spacer_proxy!27 () Bool)
(declare-fun spacer_proxy!28 () Bool)
(declare-fun INV_ext0_n () Bool)
(declare-fun |INV#level_3!15| () Bool)
(declare-fun |INV#level_4!17| () Bool)
(declare-fun |INV#level_5!19| () Bool)
(assert (let ((a!1 (>= (+ (* (/ 3.0 32.0) aux!5_n)
                  (* (/ 57.0 64.0) aux!6_n)
                  (* (- (/ 5.0 16.0)) aux!8_n))
               (- (/ 1.0 64.0))))
      (a!2 (<= (+ (* (/ 1.0 16.0) aux!5_n)
                  (* (/ 73.0 64.0) aux!6_n)
                  (* (- (/ 11.0 32.0)) aux!7_n)
                  (* (- (/ 1.0 4.0)) aux!8_n))
               (/ 1.0 16.0)))
      (a!3 (<= (+ (* (/ 5.0 16.0) aux!5_n)
                  (* (- (/ 59.0 64.0)) aux!6_n)
                  (* (/ 7.0 64.0) aux!7_n)
                  (* (/ 5.0 16.0) aux!8_n))
               (/ 1.0 32.0))))
(let ((a!4 (ite a!2
                (= (+ INV_0_n
                      (* (/ 1.0 16.0) aux!5_n)
                      (* (/ 73.0 64.0) aux!6_n)
                      (* (- (/ 11.0 32.0)) aux!7_n)
                      (* (- (/ 1.0 4.0)) aux!8_n))
                   (/ 1.0 16.0))
                (= INV_0_n aux!4_n)))
      (a!5 (ite a!3
                (= (+ INV_1_n
                      (* (/ 5.0 16.0) aux!5_n)
                      (* (- (/ 59.0 64.0)) aux!6_n)
                      (* (/ 7.0 64.0) aux!7_n)
                      (* (/ 5.0 16.0) aux!8_n))
                   (/ 1.0 32.0))
                (= INV_1_n aux!3_n)))
      (a!6 (ite a!1
                (= (+ INV_2_n
                      (* (- (/ 3.0 32.0)) aux!5_n)
                      (* (- (/ 57.0 64.0)) aux!6_n)
                      (* (/ 5.0 16.0) aux!8_n))
                   (/ 1.0 64.0))
                (= INV_2_n aux!2_n))))
(let ((a!7 (or (= INV_5_n a!1)
               (= INV_3_n a!2)
               (not (ite INV_3_0 (= aux!8_n 0.0) (= aux!8_n INV_0_0)))
               (= INV_4_n a!3)
               (not (ite INV_4_0 (= aux!7_n 0.0) (= aux!7_n INV_1_0)))
               (not (ite INV_5_0 (= aux!6_n 0.0) (= aux!6_n INV_2_0)))
               (not a!4)
               (not a!5)
               (not a!6)
               (not (>= aux!5_n (/ 1.0 64.0)))
               (not (<= aux!5_n (/ 1.0 32.0))))))
  (or (not INV__tr1) (not |vsolver#0|) (not a!7))))))
(assert (let ((a!1 (not (or INV_5_n
                    INV_4_n
                    INV_3_n
                    (not (= INV_0_n 0.0))
                    (not (= INV_1_n (/ 3.0 32.0)))
                    (not (= INV_2_n (/ 3.0 32.0)))))))
  (or (not INV__tr0) (not |vsolver#0|) a!1)))
(assert (or (not INV__tr1) |INV#level_0!9| (not |vsolver#0|)))
(assert (let ((a!1 (not (or INV_3_0
                    INV_4_0
                    INV_5_0
                    (not (= INV_0_0 0.0))
                    (not (= INV_1_0 (/ 3.0 32.0)))
                    (not (= INV_2_0 (/ 3.0 32.0)))))))
  (or (not INV__tr1) |INV#reach_tag_0_0| a!1 (not |vsolver#0|))))
(assert (or (not INV_4_n) |INV#level_0!9| (not |vsolver#0|)))
(assert (or (not INV__tr1) (not INV_4_0) |INV#level_1!13| (not |vsolver#0|)))
(assert (let ((a!1 (not (>= (+ (* (/ 11.0 32.0) INV_1_n) (* (/ 1.0 4.0) INV_0_n))
                    (- (/ 31.0 512.0))))))
  (or (not |vsolver#0|) (not spacer_proxy!0) a!1)))
(assert (or (not |vsolver#0|) (= INV_2_n 0.0) (not spacer_proxy!1)))
(assert (let ((a!1 (not (<= (+ (* (/ 7.0 64.0) INV_1_n) (* (/ 5.0 16.0) INV_0_n))
                    (/ 11.0 512.0)))))
  (or (not |vsolver#0|) (not spacer_proxy!2) a!1)))
(assert (or (not |vsolver#0|) (not (<= INV_0_n (/ 19.0 320.0))) (not spacer_proxy!3)))
(assert (or |INV#level_0!9| (not |vsolver#0|) (<= INV_0_n 0.0)))
(assert (or (not INV__tr1) |INV#level_1!13| (not |vsolver#0|) (<= INV_0_0 0.0)))
(assert (or (not |vsolver#0|) (not spacer_proxy!4) (not (>= INV_2_n (- (/ 1.0 48.0))))))
(assert (let ((a!1 (not (<= (+ (* (/ 7.0 64.0) INV_1_n) (* (- (/ 59.0 64.0)) INV_2_n))
                    (/ 11.0 512.0)))))
  (or (not |vsolver#0|) (not spacer_proxy!5) a!1)))
(assert (let ((a!1 (not (>= (+ (* (/ 11.0 32.0) INV_1_n) (* (- (/ 73.0 64.0)) INV_2_n))
                    (- (/ 31.0 512.0))))))
  (or (not |vsolver#0|) a!1 (not spacer_proxy!6))))
(assert (or (= INV_0_n 0.0) (not |vsolver#0|) (not spacer_proxy!7)))
(assert (or |INV#level_0!9| (not |vsolver#0|) (>= INV_2_n 0.0)))
(assert (or (not INV__tr1) |INV#level_1!13| (not |vsolver#0|) (>= INV_2_0 0.0)))
(assert (or (not |vsolver#0|) (not (<= INV_1_n (/ 11.0 56.0))) (not spacer_proxy!8)))
(assert (or (not |vsolver#0|) (>= INV_1_n (- (/ 31.0 176.0))) (not spacer_proxy!9)))
(assert (or |INV#level_0!9| (not |vsolver#0|) (not (= INV_2_n 0.0))))
(assert (or (not INV__tr1) |INV#level_1!13| (not |vsolver#0|) (not (= INV_2_0 0.0))))
(assert (or (not INV_5_n) |INV#level_0!9| (not |vsolver#0|)))
(assert (or (not INV__tr1) (not INV_5_0) |INV#level_1!13| (not |vsolver#0|)))
(assert (or (not |vsolver#0|)
    (>= (+ (* (/ 11.0 32.0) INV_1_n) (* (- (/ 73.0 64.0)) INV_2_n))
        (- (/ 31.0 512.0)))
    (not spacer_proxy!10)))
(assert (or (not |vsolver#0|) (>= INV_2_n (- (/ 1.0 48.0))) (not spacer_proxy!11)))
(assert (or |INV#level_0!9|
    (not |vsolver#0|)
    (<= (+ (* (/ 7.0 64.0) INV_1_n) (* (- (/ 59.0 64.0)) INV_2_n))
        (/ 11.0 512.0))))
(assert (or (not INV__tr1)
    |INV#level_1!13|
    (not |vsolver#0|)
    (<= (+ (* (/ 7.0 64.0) INV_1_0) (* (- (/ 59.0 64.0)) INV_2_0))
        (/ 11.0 512.0))))
(assert (or (not INV_4_n) |INV#level_1!13| (not |vsolver#0|)))
(assert (or (not INV__tr1) (not INV_4_0) (not |vsolver#0|) |INV#level_2!14|))
(assert (or (not INV_5_n) |INV#level_1!13| (not |vsolver#0|)))
(assert (or (not INV__tr1) (not INV_5_0) (not |vsolver#0|) |INV#level_2!14|))
(assert (or (not |vsolver#0|) (not (<= INV_0_n 0.0)) (not spacer_proxy!12)))
(assert (or (not |vsolver#0|) (not (>= INV_2_n 0.0)) (not spacer_proxy!13)))
(assert (or |INV#level_1!13| (not |vsolver#0|) (>= INV_2_n 0.0)))
(assert (or (not INV__tr1) (not |vsolver#0|) |INV#level_2!14| (>= INV_2_0 0.0)))
(assert (or |INV#level_1!13| (not |vsolver#0|) (not (= INV_2_n 0.0))))
(assert (or (not INV__tr1) (not |vsolver#0|) |INV#level_2!14| (not (= INV_2_0 0.0))))
(assert (let ((a!1 (not (>= (+ (* (/ 57.0 64.0) INV_2_n) (* (- (/ 5.0 16.0)) INV_0_n))
                    (- (/ 19.0 1024.0))))))
  (or (not |vsolver#0|) (not spacer_proxy!14) a!1)))
(assert (let ((a!1 (not (>= (+ (* (/ 11.0 32.0) INV_1_n)
                       (* (- (/ 73.0 64.0)) INV_2_n)
                       (* (/ 1.0 4.0) INV_0_n))
                    (- (/ 31.0 512.0))))))
  (or (not |vsolver#0|) a!1 (not spacer_proxy!15))))
(assert (let ((a!1 (not (<= (+ (* (/ 7.0 64.0) INV_1_n)
                       (* (- (/ 59.0 64.0)) INV_2_n)
                       (* (/ 5.0 16.0) INV_0_n))
                    (/ 11.0 512.0)))))
  (or (not |vsolver#0|) (not spacer_proxy!16) a!1)))
(assert (let ((a!1 (not (>= (+ (* (/ 11.0 32.0) INV_1_n)
                       (* (- (/ 73.0 64.0)) INV_2_n)
                       (* (/ 1.0 4.0) INV_0_n))
                    (- (/ 31.0 512.0))))))
  (or (not |vsolver#0|) a!1 (not spacer_proxy!17))))
(assert (let ((a!1 (not (<= (+ (* (/ 7.0 64.0) INV_1_n)
                       (* (- (/ 59.0 64.0)) INV_2_n)
                       (* (/ 5.0 16.0) INV_0_n))
                    (/ 11.0 512.0)))))
  (or (not |vsolver#0|) a!1 (not spacer_proxy!18))))
(assert (or INV_3_0
    INV_4_0
    (not INV__tr1)
    (not |vsolver#0|)
    (>= (+ (* (/ 1.0 4.0) INV_0_0)
           (* (/ 11.0 32.0) INV_1_0)
           (* (- (/ 73.0 64.0)) INV_2_0))
        (- (/ 31.0 512.0)))
    (<= (+ (* (/ 5.0 16.0) INV_0_0)
           (* (/ 7.0 64.0) INV_1_0)
           (* (- (/ 59.0 64.0)) INV_2_0))
        (/ 11.0 512.0))
    (not spacer_proxy!19)))
(assert (or INV_3_0
    (not INV__tr1)
    (not |vsolver#0|)
    (>= (+ (* (/ 1.0 4.0) INV_0_0)
           (* (/ 11.0 32.0) INV_1_0)
           (* (- (/ 73.0 64.0)) INV_2_0))
        (- (/ 31.0 512.0)))
    (<= (+ (* (/ 5.0 16.0) INV_0_0)
           (* (/ 7.0 64.0) INV_1_0)
           (* (- (/ 59.0 64.0)) INV_2_0))
        (/ 11.0 512.0))
    (not spacer_proxy!20)))
(assert (or (not INV__tr1)
    (not |vsolver#0|)
    (>= (+ (* (/ 1.0 4.0) INV_0_0)
           (* (/ 11.0 32.0) INV_1_0)
           (* (- (/ 73.0 64.0)) INV_2_0))
        (- (/ 31.0 512.0)))
    (<= (+ (* (/ 5.0 16.0) INV_0_0)
           (* (/ 7.0 64.0) INV_1_0)
           (* (- (/ 59.0 64.0)) INV_2_0))
        (/ 11.0 512.0))
    (not spacer_proxy!21)))
(assert (or INV_3_0
    (not INV__tr1)
    (not |vsolver#0|)
    (not spacer_proxy!22)
    (>= (+ (* (/ 1.0 4.0) INV_0_0)
           (* (/ 11.0 32.0) INV_1_0)
           (* (- (/ 73.0 64.0)) INV_2_0))
        (- (/ 31.0 512.0)))))
(assert (or INV_3_0
    (not INV__tr1)
    (not |vsolver#0|)
    (<= (+ (* (/ 5.0 16.0) INV_0_0)
           (* (/ 7.0 64.0) INV_1_0)
           (* (- (/ 59.0 64.0)) INV_2_0))
        (/ 11.0 512.0))
    (not spacer_proxy!23)))
(assert (or INV_3_n
    |INV#level_1!13|
    (not |vsolver#0|)
    (>= (+ (* (/ 11.0 32.0) INV_1_n)
           (* (- (/ 73.0 64.0)) INV_2_n)
           (* (/ 1.0 4.0) INV_0_n))
        (- (/ 31.0 512.0)))
    (<= (+ (* (/ 7.0 64.0) INV_1_n)
           (* (- (/ 59.0 64.0)) INV_2_n)
           (* (/ 5.0 16.0) INV_0_n))
        (/ 11.0 512.0))))
(assert (or INV_3_0
    (not INV__tr1)
    (not |vsolver#0|)
    |INV#level_2!14|
    (>= (+ (* (/ 1.0 4.0) INV_0_0)
           (* (/ 11.0 32.0) INV_1_0)
           (* (- (/ 73.0 64.0)) INV_2_0))
        (- (/ 31.0 512.0)))
    (<= (+ (* (/ 5.0 16.0) INV_0_0)
           (* (/ 7.0 64.0) INV_1_0)
           (* (- (/ 59.0 64.0)) INV_2_0))
        (/ 11.0 512.0))))
(assert (or (not |vsolver#0|)
    (>= (+ (* (/ 57.0 64.0) INV_2_n) (* (- (/ 5.0 16.0)) INV_0_n))
        (- (/ 19.0 1024.0)))
    (not spacer_proxy!24)))
(assert (or (not |vsolver#0|)
    (>= (+ (* (/ 11.0 32.0) INV_1_n)
           (* (- (/ 73.0 64.0)) INV_2_n)
           (* (/ 1.0 4.0) INV_0_n))
        (- (/ 31.0 512.0)))
    (not spacer_proxy!25)))
(assert (let ((a!1 (not (<= (+ (* (/ 5.0 16.0) INV_0_0) (* (- (/ 57.0 64.0)) INV_2_0))
                    (/ 19.0 1024.0)))))
  (or INV_3_0
      INV_4_0
      (not INV__tr1)
      (not |vsolver#0|)
      (<= (+ (* (/ 5.0 16.0) INV_0_0)
             (* (/ 7.0 64.0) INV_1_0)
             (* (- (/ 59.0 64.0)) INV_2_0))
          (/ 11.0 512.0))
      a!1
      (not spacer_proxy!26))))
(assert (let ((a!1 (not (<= (+ (* (/ 5.0 16.0) INV_0_0) (* (- (/ 57.0 64.0)) INV_2_0))
                    (/ 19.0 1024.0)))))
  (or INV_3_0
      (not INV__tr1)
      (not |vsolver#0|)
      (<= (+ (* (/ 5.0 16.0) INV_0_0)
             (* (/ 7.0 64.0) INV_1_0)
             (* (- (/ 59.0 64.0)) INV_2_0))
          (/ 11.0 512.0))
      (not spacer_proxy!27)
      a!1)))
(assert (let ((a!1 (not (<= (+ (* (/ 5.0 16.0) INV_0_0) (* (- (/ 57.0 64.0)) INV_2_0))
                    (/ 19.0 1024.0)))))
  (or (not INV__tr1)
      (not |vsolver#0|)
      (<= (+ (* (/ 5.0 16.0) INV_0_0)
             (* (/ 7.0 64.0) INV_1_0)
             (* (- (/ 59.0 64.0)) INV_2_0))
          (/ 11.0 512.0))
      a!1
      (not spacer_proxy!28))))
;; extra clause
(assert (or INV_ext0_n INV__tr0 INV__tr1 ))
(check-sat |vsolver#0|
 spacer_proxy!28
 (not INV_ext0_n)
 |INV#level_0!9|
 (not |INV#level_1!13|)
 (not |INV#level_2!14|)
 (not |INV#level_3!15|)
 (not |INV#level_4!17|)
 (not |INV#level_5!19|)
 spacer_proxy!18
 spacer_proxy!24
)
(exit)
(:added-eqs                      400
 :arith-eq-adapter               96
 :arith-bound-propagations-cheap 242
 :arith-bound-propagations-lp    125
 :arith-conflicts                13
 :arith-diseq                    378
 :arith-fixed-eqs                4
 :arith-lower                    361
 :arith-make-feasible            278
 :arith-max-columns              38
 :arith-max-rows                 24
 :arith-propagations             242
 :arith-rows                     935
 :arith-upper                    566
 :conflicts                      49
 :decisions                      478
 :del-clause                     102
 :final-checks                   18
 :minimized-lits                 2
 :mk-bool-var                    450
 :mk-clause                      633
 :num-checks                     44
 :propagations                   1942
 :time                           0.00)
(params arith.solver 6 random_seed 0 dump_benchmarks true dump_threshold 0.00 mbqi true arith.ignore_int true array.weak true)