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
(declare-fun spacer_proxy!17 () Bool)
(declare-fun spacer_proxy!18 () Bool)
(declare-fun spacer_proxy!19 () Bool)
(declare-fun |BwdInv#level_2!14| () Bool)
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
(declare-fun |BwdInv#level_3!15| () Bool)
(declare-fun spacer_proxy!47 () Bool)
(declare-fun spacer_proxy!48 () Bool)
(declare-fun spacer_proxy!49 () Bool)
(declare-fun spacer_proxy!50 () Bool)
(declare-fun spacer_proxy!51 () Bool)
(declare-fun spacer_proxy!52 () Bool)
(declare-fun spacer_proxy!53 () Bool)
(declare-fun spacer_proxy!54 () Bool)
(declare-fun spacer_proxy!55 () Bool)
(declare-fun spacer_proxy!56 () Bool)
(declare-fun spacer_proxy!57 () Bool)
(declare-fun spacer_proxy!58 () Bool)
(declare-fun spacer_proxy!59 () Bool)
(declare-fun spacer_proxy!60 () Bool)
(declare-fun spacer_proxy!61 () Bool)
(declare-fun spacer_proxy!62 () Bool)
(declare-fun spacer_proxy!63 () Bool)
(declare-fun spacer_proxy!64 () Bool)
(declare-fun spacer_proxy!65 () Bool)
(declare-fun spacer_proxy!66 () Bool)
(declare-fun spacer_proxy!67 () Bool)
(declare-fun spacer_proxy!68 () Bool)
(declare-fun spacer_proxy!69 () Bool)
(declare-fun spacer_proxy!70 () Bool)
(declare-fun spacer_proxy!71 () Bool)
(declare-fun BwdInv_ext0_n () Bool)
(declare-fun |BwdInv#level_4!17| () Bool)
(declare-fun |BwdInv#level_5!19| () Bool)
(declare-fun |BwdInv#level_6!21| () Bool)
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
(assert (or (not |vsolver#0|) (<= BwdInv_0_n 0.0) (not spacer_proxy!17)))
(assert (or BwdInv_4_0
    BwdInv_5_0
    (not BwdInv__tr0)
    (not |vsolver#0|)
    (not (>= BwdInv_2_0 (/ 3.0 32.0)))
    (not (<= BwdInv_1_0 (/ 3.0 32.0)))
    (not spacer_proxy!18)
    (not (<= BwdInv_0_0 0.0))))
(assert (or BwdInv_4_0
    BwdInv_5_0
    (not BwdInv__tr0)
    (not |vsolver#0|)
    (not (>= BwdInv_2_0 (/ 3.0 32.0)))
    (not (<= BwdInv_1_0 (/ 3.0 32.0)))
    (not (<= BwdInv_0_0 0.0))
    (not spacer_proxy!19)))
(assert (or BwdInv_4_n
    BwdInv_5_n
    |BwdInv#level_1!13|
    (not |vsolver#0|)
    (not (>= BwdInv_2_n (/ 3.0 32.0)))
    (not (<= BwdInv_1_n (/ 3.0 32.0)))
    (not (<= BwdInv_0_n 0.0))))
(assert (or BwdInv_4_0
    BwdInv_5_0
    (not BwdInv__tr0)
    (not |vsolver#0|)
    |BwdInv#level_2!14|
    (not (>= BwdInv_2_0 (/ 3.0 32.0)))
    (not (<= BwdInv_1_0 (/ 3.0 32.0)))
    (not (<= BwdInv_0_0 0.0))))
(assert (or (not |vsolver#0|) (not spacer_proxy!20) (>= BwdInv_1_n (/ 35.0 512.0))))
(assert (or (not |vsolver#0|) (not spacer_proxy!21) (<= BwdInv_1_n (/ 195.0 512.0))))
(assert (or (not |vsolver#0|) (>= BwdInv_1_n 0.0) (not spacer_proxy!22)))
(assert (or (not |vsolver#0|)
    (not spacer_proxy!23)
    (not (>= BwdInv_1_n (/ 165.0 1024.0)))))
(assert (or (not |vsolver#0|)
    (= (+ (* (/ 3.0 10.0) BwdInv_1_n) BwdInv_2_n) (/ 117.0 1024.0))
    (not spacer_proxy!24)))
(assert (or (not |vsolver#0|) (<= BwdInv_1_n (/ 5.0 64.0)) (not spacer_proxy!25)))
(assert (or (not |vsolver#0|) (>= BwdInv_2_n (/ 713.0 19968.0)) (not spacer_proxy!26)))
(assert (or (not |vsolver#0|)
    (= (+ (* (/ 3.0 10.0) BwdInv_1_n) BwdInv_2_n) (/ 117.0 1024.0))
    (not spacer_proxy!27)))
(assert (or (not |vsolver#0|) (not spacer_proxy!28) (<= BwdInv_1_n (/ 15685.0 59904.0))))
(assert (let ((a!1 (not (= (+ (* (/ 3.0 10.0) BwdInv_1_0) BwdInv_2_0) (/ 117.0 1024.0)))))
  (or BwdInv_4_0
      BwdInv_5_0
      (not BwdInv__tr0)
      (not BwdInv_3_0)
      (not |vsolver#0|)
      (not spacer_proxy!29)
      (not (>= BwdInv_2_0 (/ 713.0 19968.0)))
      a!1
      (not (<= BwdInv_1_0 (/ 15685.0 59904.0))))))
(assert (let ((a!1 (not (= (+ (* (/ 3.0 10.0) BwdInv_1_0) BwdInv_2_0) (/ 117.0 1024.0)))))
  (or BwdInv_4_0
      BwdInv_5_0
      (not BwdInv__tr0)
      (not |vsolver#0|)
      (not (>= BwdInv_2_0 (/ 713.0 19968.0)))
      a!1
      (not spacer_proxy!30))))
(assert (let ((a!1 (not (= (+ (* (/ 3.0 10.0) BwdInv_1_0) BwdInv_2_0) (/ 117.0 1024.0)))))
  (or BwdInv_5_0
      (not BwdInv__tr0)
      (not BwdInv_3_0)
      (not |vsolver#0|)
      (not (>= BwdInv_2_0 (/ 713.0 19968.0)))
      a!1
      (not spacer_proxy!31))))
(assert (let ((a!1 (not (= (+ (* (/ 3.0 10.0) BwdInv_1_0) BwdInv_2_0) (/ 117.0 1024.0)))))
  (or BwdInv_4_0
      (not BwdInv__tr0)
      (not BwdInv_3_0)
      (not |vsolver#0|)
      (not spacer_proxy!32)
      (not (>= BwdInv_2_0 (/ 713.0 19968.0)))
      a!1)))
(assert (let ((a!1 (not (= (+ (* (/ 3.0 10.0) BwdInv_1_0) BwdInv_2_0) (/ 117.0 1024.0)))))
  (or BwdInv_4_0
      BwdInv_5_0
      (not BwdInv__tr0)
      (not BwdInv_3_0)
      (not |vsolver#0|)
      a!1
      (not spacer_proxy!33))))
(assert (or BwdInv_4_0
    BwdInv_5_0
    (not BwdInv__tr0)
    (not BwdInv_3_0)
    (not |vsolver#0|)
    (not (>= BwdInv_2_0 (/ 713.0 19968.0)))
    (not spacer_proxy!34)))
(assert (or (not |vsolver#0|)
    (<= (+ (* (/ 3.0 10.0) BwdInv_1_n) BwdInv_2_n) (/ 117.0 1024.0))
    (not spacer_proxy!35)))
(assert (let ((a!1 (not (<= (+ (* (/ 3.0 10.0) BwdInv_1_0) BwdInv_2_0) (/ 117.0 1024.0)))))
  (or BwdInv_4_0
      BwdInv_5_0
      (not BwdInv__tr0)
      (not BwdInv_3_0)
      (not |vsolver#0|)
      (not (>= BwdInv_2_0 (/ 713.0 19968.0)))
      (not spacer_proxy!36)
      a!1)))
(assert (let ((a!1 (not (<= (+ (* (/ 3.0 10.0) BwdInv_1_n) BwdInv_2_n) (/ 117.0 1024.0)))))
  (or BwdInv_4_n
      BwdInv_5_n
      (not BwdInv_3_n)
      |BwdInv#level_1!13|
      (not |vsolver#0|)
      (not (>= BwdInv_2_n (/ 713.0 19968.0)))
      a!1)))
(assert (let ((a!1 (not (<= (+ (* (/ 3.0 10.0) BwdInv_1_0) BwdInv_2_0) (/ 117.0 1024.0)))))
  (or BwdInv_4_0
      BwdInv_5_0
      (not BwdInv__tr0)
      (not BwdInv_3_0)
      (not |vsolver#0|)
      |BwdInv#level_2!14|
      (not (>= BwdInv_2_0 (/ 713.0 19968.0)))
      a!1)))
(assert (or BwdInv_4_0
    BwdInv_5_0
    BwdInv_3_0
    (not BwdInv__tr0)
    (not (= BwdInv_0_0 0.0))
    (not (= BwdInv_1_0 (/ 3.0 32.0)))
    (not (= BwdInv_2_0 (/ 3.0 32.0)))
    (not |vsolver#0|)
    (not spacer_proxy!37)))
(assert (or BwdInv_4_0
    BwdInv_5_0
    (not BwdInv__tr0)
    (not (= BwdInv_0_0 0.0))
    (not (= BwdInv_2_0 (/ 3.0 32.0)))
    (not |vsolver#0|)
    (not spacer_proxy!38)))
(assert (or BwdInv_4_0
    BwdInv_5_0
    (not BwdInv__tr0)
    (not (= BwdInv_0_0 0.0))
    (not (= BwdInv_2_0 (/ 3.0 32.0)))
    (not |vsolver#0|)
    (not (<= BwdInv_1_0 (/ 3.0 32.0)))
    (not spacer_proxy!39)))
(assert (or (not |vsolver#0|) (>= BwdInv_1_n (/ 3.0 32.0)) (not spacer_proxy!40)))
(assert (or BwdInv_4_0
    BwdInv_5_0
    (not BwdInv__tr0)
    (not (= BwdInv_0_0 0.0))
    (not (= BwdInv_2_0 (/ 3.0 32.0)))
    (not |vsolver#0|)
    (not spacer_proxy!41)
    (not (>= BwdInv_1_0 (/ 3.0 32.0)))))
(assert (or BwdInv_4_0
    BwdInv_5_0
    (not BwdInv__tr0)
    (not (= BwdInv_1_0 (/ 3.0 32.0)))
    (not (= BwdInv_2_0 (/ 3.0 32.0)))
    (not |vsolver#0|)
    (not spacer_proxy!42)))
(assert (or BwdInv_4_0
    BwdInv_5_0
    (not BwdInv__tr0)
    (not (= BwdInv_1_0 (/ 3.0 32.0)))
    (not (= BwdInv_2_0 (/ 3.0 32.0)))
    (not |vsolver#0|)
    (not (<= BwdInv_0_0 0.0))
    (not spacer_proxy!43)))
(assert (or (not |vsolver#0|) (>= BwdInv_0_n 0.0) (not spacer_proxy!44)))
(assert (or BwdInv_4_0
    BwdInv_5_0
    (not BwdInv__tr0)
    (not (= BwdInv_1_0 (/ 3.0 32.0)))
    (not (= BwdInv_2_0 (/ 3.0 32.0)))
    (not |vsolver#0|)
    (not spacer_proxy!45)
    (not (>= BwdInv_0_0 0.0))))
(assert (or BwdInv_4_0
    BwdInv_5_0
    (not BwdInv__tr0)
    (not (= BwdInv_0_0 0.0))
    (not (= BwdInv_1_0 (/ 3.0 32.0)))
    (not (= BwdInv_2_0 (/ 3.0 32.0)))
    (not |vsolver#0|)
    (not spacer_proxy!46)))
(assert (or BwdInv_4_n
    BwdInv_5_n
    (not |vsolver#0|)
    |BwdInv#level_2!14|
    (not (= BwdInv_2_n (/ 3.0 32.0)))
    (not (= BwdInv_1_n (/ 3.0 32.0)))
    (not (= BwdInv_0_n 0.0))))
(assert (or BwdInv_4_0
    BwdInv_5_0
    (not BwdInv__tr0)
    (not (= BwdInv_0_0 0.0))
    (not (= BwdInv_1_0 (/ 3.0 32.0)))
    (not (= BwdInv_2_0 (/ 3.0 32.0)))
    (not |vsolver#0|)
    |BwdInv#level_3!15|))
(assert (or (not |vsolver#0|)
    (<= (+ (* (/ 3.0 10.0) BwdInv_1_n) BwdInv_2_n) (/ 117.0 1024.0))
    (not spacer_proxy!47)))
(assert (let ((a!1 (not (<= (+ (* (/ 243.0 1600.0) BwdInv_1_n)
                       (* (/ 1207.0 1600.0) BwdInv_2_n))
                    (/ 3738801.0 52428800.0)))))
  (or (not |vsolver#0|) (not spacer_proxy!48) a!1)))
(assert (or (not |vsolver#0|)
    (<= (+ (* (/ 3.0 10.0) BwdInv_1_n) BwdInv_2_n) (/ 18837.0 163840.0))
    (not spacer_proxy!49)))
(assert (or (not |vsolver#0|)
    (>= (+ (* (/ 3.0 10.0) BwdInv_1_n) BwdInv_2_n) (/ 36483.0 327680.0))
    (not spacer_proxy!50)))
(assert (or (not |vsolver#0|)
    (>= (+ (* (/ 21.0 25.0) BwdInv_1_n) (* (- (/ 117.0 100.0)) BwdInv_2_n))
        (- (/ 20589.0 409600.0)))
    (not spacer_proxy!51)))
(assert (or (not |vsolver#0|)
    (not spacer_proxy!52)
    (<= (+ (* (/ 3.0 10.0) BwdInv_1_n) BwdInv_2_n) (/ 46011.0 327680.0))))
(assert (or (not |vsolver#0|)
    (not spacer_proxy!53)
    (<= (+ (* (/ 21.0 25.0) BwdInv_1_n) (* (- (/ 117.0 100.0)) BwdInv_2_n))
        (- (/ 633.0 16384.0)))))
(assert (or (not |vsolver#0|) (not spacer_proxy!54) (>= BwdInv_2_n 0.0)))
(assert (let ((a!1 (not (<= (+ (* (/ 3.0 10.0) BwdInv_1_n) BwdInv_2_n)
                    (/ 52719.0 655360.0)))))
  (or (not |vsolver#0|) (not spacer_proxy!55) a!1)))
(assert (or (not |vsolver#0|)
    (not spacer_proxy!56)
    (>= (+ (* (/ 3.0 10.0) BwdInv_1_n) BwdInv_2_n) (- (/ 219.0 163840.0)))))
(assert (let ((a!1 (not (>= (+ BwdInv_1_n (* (- (/ 39.0 28.0)) BwdInv_2_n))
                    (/ 219.0 7168.0)))))
  (or (not |vsolver#0|) (not spacer_proxy!57) a!1)))
(assert (or BwdInv_4_0
    BwdInv_5_0
    (not BwdInv__tr0)
    (not BwdInv_3_0)
    (not |vsolver#0|)
    (not (<= BwdInv_2_0 (/ 3.0 32.0)))
    (>= BwdInv_1_0 (/ 165.0 1024.0))
    (not (>= BwdInv_2_0 (/ 713.0 19968.0)))
    (>= (+ BwdInv_1_0 (* (- (/ 39.0 28.0)) BwdInv_2_0)) (/ 219.0 7168.0))
    (not spacer_proxy!58)))
(assert (or BwdInv_4_0
    BwdInv_5_0
    (not BwdInv__tr0)
    (not |vsolver#0|)
    (>= BwdInv_1_0 (/ 165.0 1024.0))
    (not (>= BwdInv_2_0 (/ 713.0 19968.0)))
    (not spacer_proxy!59)))
(assert (or BwdInv_5_0
    (not BwdInv__tr0)
    (not BwdInv_3_0)
    (not |vsolver#0|)
    (>= BwdInv_1_0 (/ 165.0 1024.0))
    (not (>= BwdInv_2_0 (/ 713.0 19968.0)))
    (not spacer_proxy!60)))
(assert (or BwdInv_4_0
    (not BwdInv__tr0)
    (not BwdInv_3_0)
    (not |vsolver#0|)
    (>= BwdInv_1_0 (/ 165.0 1024.0))
    (not (>= BwdInv_2_0 (/ 713.0 19968.0)))
    (not spacer_proxy!61)))
(assert (or BwdInv_4_0
    BwdInv_5_0
    (not BwdInv__tr0)
    (not BwdInv_3_0)
    (not |vsolver#0|)
    (not (>= BwdInv_2_0 (/ 713.0 19968.0)))
    (not spacer_proxy!62)))
(assert (or BwdInv_4_0
    BwdInv_5_0
    (not BwdInv__tr0)
    (not BwdInv_3_0)
    (not |vsolver#0|)
    (>= BwdInv_1_0 (/ 165.0 1024.0))
    (not spacer_proxy!63)))
(assert (or BwdInv_4_n
    BwdInv_5_n
    (not BwdInv_3_n)
    |BwdInv#level_1!13|
    (not |vsolver#0|)
    (not (<= BwdInv_2_n (/ 3.0 32.0)))
    (>= BwdInv_1_n (/ 165.0 1024.0))
    (not (>= BwdInv_2_n (/ 713.0 19968.0)))
    (>= (+ BwdInv_1_n (* (- (/ 39.0 28.0)) BwdInv_2_n)) (/ 219.0 7168.0))))
(assert (or BwdInv_4_0
    BwdInv_5_0
    (not BwdInv__tr0)
    (not BwdInv_3_0)
    (not |vsolver#0|)
    |BwdInv#level_2!14|
    (not (<= BwdInv_2_0 (/ 3.0 32.0)))
    (>= BwdInv_1_0 (/ 165.0 1024.0))
    (not (>= BwdInv_2_0 (/ 713.0 19968.0)))
    (>= (+ BwdInv_1_0 (* (- (/ 39.0 28.0)) BwdInv_2_0)) (/ 219.0 7168.0))))
(assert (or (not |vsolver#0|) (>= BwdInv_2_n (/ 441.0 5120.0)) (not spacer_proxy!64)))
(assert (let ((a!1 (not (= (+ (* (/ 3.0 10.0) BwdInv_1_0) BwdInv_2_0) (/ 117.0 1024.0)))))
  (or BwdInv_4_0
      BwdInv_5_0
      (not BwdInv__tr0)
      (not BwdInv_3_0)
      (not |vsolver#0|)
      (not (<= BwdInv_2_0 (/ 3.0 32.0)))
      (not (<= BwdInv_1_0 (/ 3.0 32.0)))
      a!1
      (not (>= BwdInv_1_0 (/ 35.0 512.0)))
      (not (>= BwdInv_2_0 (/ 441.0 5120.0)))
      (not spacer_proxy!65))))
(assert (let ((a!1 (not (= (+ (* (/ 3.0 10.0) BwdInv_1_0) BwdInv_2_0) (/ 117.0 1024.0)))))
  (or BwdInv_4_0
      BwdInv_5_0
      (not BwdInv__tr0)
      (not |vsolver#0|)
      (not (<= BwdInv_2_0 (/ 3.0 32.0)))
      (not (<= BwdInv_1_0 (/ 3.0 32.0)))
      a!1
      (not spacer_proxy!66)
      (not (>= BwdInv_1_0 (/ 35.0 512.0)))
      (not (>= BwdInv_2_0 (/ 441.0 5120.0))))))
(assert (let ((a!1 (not (= (+ (* (/ 3.0 10.0) BwdInv_1_0) BwdInv_2_0) (/ 117.0 1024.0)))))
  (or BwdInv_5_0
      (not BwdInv__tr0)
      (not BwdInv_3_0)
      (not |vsolver#0|)
      (not (<= BwdInv_2_0 (/ 3.0 32.0)))
      (not (<= BwdInv_1_0 (/ 3.0 32.0)))
      a!1
      (not (>= BwdInv_1_0 (/ 35.0 512.0)))
      (not (>= BwdInv_2_0 (/ 441.0 5120.0)))
      (not spacer_proxy!67))))
(assert (let ((a!1 (not (= (+ (* (/ 3.0 10.0) BwdInv_1_0) BwdInv_2_0) (/ 117.0 1024.0)))))
  (or BwdInv_4_0
      (not BwdInv__tr0)
      (not BwdInv_3_0)
      (not |vsolver#0|)
      (not (<= BwdInv_2_0 (/ 3.0 32.0)))
      (not (<= BwdInv_1_0 (/ 3.0 32.0)))
      a!1
      (not spacer_proxy!68)
      (not (>= BwdInv_1_0 (/ 35.0 512.0)))
      (not (>= BwdInv_2_0 (/ 441.0 5120.0))))))
(assert (let ((a!1 (not (= (+ (* (/ 3.0 10.0) BwdInv_1_0) BwdInv_2_0) (/ 117.0 1024.0)))))
  (or BwdInv_4_0
      BwdInv_5_0
      (not BwdInv__tr0)
      (not BwdInv_3_0)
      (not |vsolver#0|)
      (not (<= BwdInv_1_0 (/ 3.0 32.0)))
      a!1
      (not (>= BwdInv_1_0 (/ 35.0 512.0)))
      (not (>= BwdInv_2_0 (/ 441.0 5120.0)))
      (not spacer_proxy!69))))
(assert (let ((a!1 (not (= (+ (* (/ 3.0 10.0) BwdInv_1_0) BwdInv_2_0) (/ 117.0 1024.0)))))
  (or BwdInv_4_0
      BwdInv_5_0
      (not BwdInv__tr0)
      (not BwdInv_3_0)
      (not |vsolver#0|)
      a!1
      (not (>= BwdInv_1_0 (/ 35.0 512.0)))
      (not (>= BwdInv_2_0 (/ 441.0 5120.0)))
      (not spacer_proxy!70))))
(assert (let ((a!1 (not (= (+ (* (/ 3.0 10.0) BwdInv_1_0) BwdInv_2_0) (/ 117.0 1024.0)))))
  (or BwdInv_4_0
      BwdInv_5_0
      (not BwdInv__tr0)
      (not BwdInv_3_0)
      (not |vsolver#0|)
      a!1
      (not (>= BwdInv_2_0 (/ 441.0 5120.0)))
      (not spacer_proxy!71))))
;; extra clause
(assert (or BwdInv_ext0_n BwdInv__tr0 BwdInv__tr1 ))
(check-sat |vsolver#0|
 spacer_proxy!71
 (not BwdInv_ext0_n)
 |BwdInv#level_0!9|
 |BwdInv#level_1!13|
 (not |BwdInv#level_2!14|)
 (not |BwdInv#level_3!15|)
 (not |BwdInv#level_4!17|)
 (not |BwdInv#level_5!19|)
 (not |BwdInv#level_6!21|)
 spacer_proxy!64
 (not BwdInv_5_n)
 (not BwdInv_4_n)
 spacer_proxy!27
 BwdInv_3_n
)
(exit)
(:added-eqs          662
 :arith-add-rows     912
 :arith-assert-diseq 249
 :arith-assert-lower 921
 :arith-assert-upper 844
 :arith-bound-prop   108
 :arith-conflicts    14
 :arith-eq-adapter   190
 :arith-fixed-eqs    96
 :arith-offset-eqs   24
 :arith-pivots       173
 :conflicts          54
 :decisions          1706
 :del-clause         143
 :final-checks       38
 :minimized-lits     25
 :mk-bool-var        595
 :mk-clause          443
 :num-checks         68
 :propagations       3541
 :time               0.01)
(params arith.solver 2 random_seed 0 dump_benchmarks true dump_threshold 0.00 mbqi true arith.ignore_int true array.weak true)