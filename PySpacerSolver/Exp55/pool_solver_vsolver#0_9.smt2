(set-info :status unsat)
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
(declare-fun spacer_proxy!29 () Bool)
(declare-fun spacer_proxy!30 () Bool)
(declare-fun spacer_proxy!31 () Bool)
(declare-fun spacer_proxy!32 () Bool)
(declare-fun spacer_proxy!33 () Bool)
(declare-fun spacer_proxy!34 () Bool)
(declare-fun spacer_proxy!35 () Bool)
(declare-fun spacer_proxy!36 () Bool)
(declare-fun spacer_proxy!37 () Bool)
(declare-fun spacer_proxy!38 () Bool)
(declare-fun spacer_proxy!39 () Bool)
(declare-fun spacer_proxy!40 () Bool)
(declare-fun spacer_proxy!41 () Bool)
(declare-fun spacer_proxy!42 () Bool)
(declare-fun spacer_proxy!43 () Bool)
(declare-fun spacer_proxy!44 () Bool)
(declare-fun spacer_proxy!45 () Bool)
(declare-fun spacer_proxy!46 () Bool)
(declare-fun spacer_proxy!47 () Bool)
(declare-fun spacer_proxy!48 () Bool)
(declare-fun spacer_proxy!49 () Bool)
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
(assert (let ((a!1 (not (<= (+ (* (/ 5.0 16.0) INV_0_0) (* (- (/ 57.0 64.0)) INV_2_0))
                    (/ 19.0 1024.0)))))
  (or INV_3_0 (not INV__tr1) (not |vsolver#0|) a!1 (not spacer_proxy!29))))
(assert (let ((a!1 (not (>= (+ (* (/ 57.0 64.0) INV_2_n) (* (- (/ 5.0 16.0)) INV_0_n))
                    (- (/ 19.0 1024.0))))))
  (or INV_3_n
      |INV#level_1!13|
      (not |vsolver#0|)
      (<= (+ (* (/ 7.0 64.0) INV_1_n)
             (* (- (/ 59.0 64.0)) INV_2_n)
             (* (/ 5.0 16.0) INV_0_n))
          (/ 11.0 512.0))
      a!1)))
(assert (let ((a!1 (not (<= (+ (* (/ 5.0 16.0) INV_0_0) (* (- (/ 57.0 64.0)) INV_2_0))
                    (/ 19.0 1024.0)))))
  (or INV_3_0
      (not INV__tr1)
      (not |vsolver#0|)
      |INV#level_2!14|
      (<= (+ (* (/ 5.0 16.0) INV_0_0)
             (* (/ 7.0 64.0) INV_1_0)
             (* (- (/ 59.0 64.0)) INV_2_0))
          (/ 11.0 512.0))
      a!1)))
(assert (or (not |vsolver#0|)
    (<= (+ (* (/ 7.0 64.0) INV_1_n) (* (- (/ 59.0 64.0)) INV_2_n))
        (/ 11.0 512.0))
    (not spacer_proxy!30)))
(assert (or (not |vsolver#0|) (>= INV_2_n (- (/ 121.0 2736.0))) (not spacer_proxy!31)))
(assert (let ((a!1 (not (>= (+ (* (/ 49.0 4096.0) INV_1_n)
                       (* (/ 1475.0 2048.0) INV_2_n))
                    (- (/ 2375.0 65536.0))))))
  (or (not |vsolver#0|) (not spacer_proxy!32) a!1)))
(assert (or (not |vsolver#0|)
    (not spacer_proxy!33)
    (<= (+ (* (/ 77.0 2048.0) INV_1_n) (* (/ 2863.0 4096.0) INV_2_n))
        (/ 3065.0 65536.0))))
(assert (or |INV#level_0!9|
    (not |vsolver#0|)
    (>= (+ (* (/ 49.0 4096.0) INV_1_n) (* (/ 1475.0 2048.0) INV_2_n))
        (- (/ 2375.0 65536.0)))))
(assert (or (not INV__tr1)
    |INV#level_1!13|
    (not |vsolver#0|)
    (>= (+ (* (/ 49.0 4096.0) INV_1_0) (* (/ 1475.0 2048.0) INV_2_0))
        (- (/ 2375.0 65536.0)))))
(assert (let ((a!1 (not (>= (+ (* (/ 147.0 15808.0) INV_1_n)
                       (* (- (/ 5229.0 15808.0)) INV_2_n))
                    (- (/ 1.0 104.0))))))
  (or (not |vsolver#0|) a!1 (not spacer_proxy!34))))
(assert (let ((a!1 (not (>= (+ (* (/ 1383.0 3952.0) INV_1_n)
                       (* (- (/ 12131.0 15808.0)) INV_2_n))
                    (- (/ 33.0 416.0))))))
  (or (not |vsolver#0|) (not spacer_proxy!35) a!1)))
(assert (or (not |vsolver#0|)
    (not spacer_proxy!36)
    (>= (+ (* (/ 49.0 494.0) INV_1_n) (* (/ 1475.0 247.0) INV_2_n))
        (- (/ 125.0 416.0)))))
(assert (or (not |vsolver#0|)
    (<= (+ (* (/ 1239.0 15808.0) INV_1_n) (* (- (/ 44073.0 15808.0)) INV_2_n))
        (/ 3.0 26.0))
    (not spacer_proxy!37)))
(assert (or (not |vsolver#0|)
    (not spacer_proxy!38)
    (<= (+ (* (/ 16527.0 1011712.0) INV_1_n)
           (* (- (/ 587889.0 1011712.0)) INV_2_n))
        (/ 185.0 1664.0))))
(assert (let ((a!1 (not (>= (+ (* (/ 49.0 494.0) INV_1_n) (* (/ 1475.0 247.0) INV_2_n))
                    (- (/ 237.0 832.0))))))
  (or (not |vsolver#0|) (not spacer_proxy!39) a!1)))
(assert (let ((a!1 (not (>= (+ (* (/ 147.0 15808.0) INV_1_n)
                       (* (- (/ 5229.0 15808.0)) INV_2_n))
                    (/ 7.0 624.0)))))
  (or (not |vsolver#0|) (not spacer_proxy!40) a!1)))
(assert (or |INV#level_0!9|
    (not |vsolver#0|)
    (>= (+ (* (/ 49.0 494.0) INV_1_n) (* (/ 1475.0 247.0) INV_2_n))
        (- (/ 237.0 832.0)))))
(assert (or (not INV__tr1)
    |INV#level_1!13|
    (not |vsolver#0|)
    (>= (+ (* (/ 49.0 494.0) INV_1_0) (* (/ 1475.0 247.0) INV_2_0))
        (- (/ 237.0 832.0)))))
(assert (let ((a!1 (not (<= (+ (* (/ 7.0 64.0) INV_1_n) (* (- (/ 59.0 64.0)) INV_2_n))
                    (/ 11.0 512.0)))))
  (or (not |vsolver#0|) a!1 (not spacer_proxy!41))))
(assert (or INV_4_0
    INV_5_0
    (not INV__tr1)
    (not |vsolver#0|)
    (<= (+ (* (/ 7.0 64.0) INV_1_0) (* (- (/ 59.0 64.0)) INV_2_0))
        (/ 11.0 512.0))
    (not spacer_proxy!42)))
(assert (or INV_5_0
    (not INV__tr1)
    (not |vsolver#0|)
    (<= (+ (* (/ 7.0 64.0) INV_1_0) (* (- (/ 59.0 64.0)) INV_2_0))
        (/ 11.0 512.0))
    (not spacer_proxy!43)))
(assert (or (not INV__tr1)
    (not |vsolver#0|)
    (<= (+ (* (/ 7.0 64.0) INV_1_0) (* (- (/ 59.0 64.0)) INV_2_0))
        (/ 11.0 512.0))
    (not spacer_proxy!44)))
(assert (or |INV#level_1!13|
    (not |vsolver#0|)
    (<= (+ (* (/ 7.0 64.0) INV_1_n) (* (- (/ 59.0 64.0)) INV_2_n))
        (/ 11.0 512.0))))
(assert (or (not INV__tr1)
    (not |vsolver#0|)
    |INV#level_2!14|
    (<= (+ (* (/ 7.0 64.0) INV_1_0) (* (- (/ 59.0 64.0)) INV_2_0))
        (/ 11.0 512.0))))
(assert (let ((a!1 (not (<= (+ (* (/ 7.0 64.0) INV_1_n)
                       (* (- (/ 59.0 64.0)) INV_2_n)
                       (* (/ 5.0 16.0) INV_0_n))
                    (/ 27.0 1024.0)))))
  (or (not |vsolver#0|) (not spacer_proxy!45) a!1)))
(assert (let ((a!1 (not (>= (+ (* (/ 57.0 64.0) INV_2_n) (* (- (/ 5.0 16.0)) INV_0_n))
                    (- (/ 35.0 2048.0))))))
  (or (not |vsolver#0|) (not spacer_proxy!46) a!1)))
(assert (or (not |vsolver#0|)
    (not spacer_proxy!47)
    (>= (+ (* (/ 11.0 32.0) INV_1_n)
           (* (- (/ 73.0 64.0)) INV_2_n)
           (* (/ 1.0 4.0) INV_0_n))
        (- (/ 63.0 1024.0)))))
(assert (let ((a!1 (not (<= (+ (* (/ 7.0 64.0) INV_1_n)
                       (* (- (/ 59.0 64.0)) INV_2_n)
                       (* (/ 5.0 16.0) INV_0_n))
                    (/ 27.0 1024.0)))))
  (or (not |vsolver#0|) a!1 (not spacer_proxy!48))))
(assert (or INV_3_0
    INV_4_0
    (not INV__tr1)
    (not |vsolver#0|)
    (<= (+ (* (/ 5.0 16.0) INV_0_0)
           (* (/ 7.0 64.0) INV_1_0)
           (* (- (/ 59.0 64.0)) INV_2_0))
        (/ 27.0 1024.0))
    (not spacer_proxy!49)))
;; extra clause
(assert (or INV_ext0_n INV__tr0 INV__tr1 ))
(check-sat |vsolver#0|
 spacer_proxy!49
 (not INV_ext0_n)
 |INV#level_0!9|
 (not |INV#level_1!13|)
 (not |INV#level_2!14|)
 (not |INV#level_3!15|)
 (not |INV#level_4!17|)
 (not |INV#level_5!19|)
 (not INV_3_n)
 (not INV_4_n)
 spacer_proxy!48
)
(exit)
(:added-eqs                      565
 :arith-eq-adapter               136
 :arith-bound-propagations-cheap 368
 :arith-bound-propagations-lp    181
 :arith-conflicts                18
 :arith-diseq                    522
 :arith-fixed-eqs                4
 :arith-lower                    538
 :arith-make-feasible            378
 :arith-max-columns              47
 :arith-max-rows                 33
 :arith-propagations             368
 :arith-rows                     1428
 :arith-upper                    882
 :conflicts                      72
 :decisions                      687
 :del-clause                     124
 :final-checks                   24
 :minimized-lits                 2
 :mk-bool-var                    611
 :mk-clause                      864
 :num-checks                     64
 :propagations                   3048)
(params arith.solver 6 random_seed 0 dump_benchmarks true dump_threshold 0 mbqi true arith.ignore_int true array.weak true)