(set-info :status sat)
(declare-fun INV_2_n () Real)
(declare-fun INV_1_n () Real)
(declare-fun INV_0_n () Real)
(declare-fun INV_3_n () Bool)
(declare-fun INV_4_n () Bool)
(declare-fun INV_5_n () Bool)
(declare-fun |vsolver#0| () Bool)
(declare-fun INV__tr1 () Bool)
(declare-fun aux!5_n () Real)
(declare-fun aux!2_n () Real)
(declare-fun aux!8_n () Real)
(declare-fun aux!6_n () Real)
(declare-fun aux!3_n () Real)
(declare-fun aux!7_n () Real)
(declare-fun aux!4_n () Real)
(declare-fun INV_2_0 () Real)
(declare-fun INV_5_0 () Bool)
(declare-fun INV_1_0 () Real)
(declare-fun INV_4_0 () Bool)
(declare-fun INV_0_0 () Real)
(declare-fun INV_3_0 () Bool)
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
(declare-fun |INV#level_2!14| () Bool)
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
(declare-fun |INV#level_3!15| () Bool)
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
(declare-fun spacer_proxy!72 () Bool)
(declare-fun |INV#level_4!17| () Bool)
(declare-fun spacer_proxy!73 () Bool)
(declare-fun spacer_proxy!74 () Bool)
(declare-fun spacer_proxy!75 () Bool)
(declare-fun spacer_proxy!76 () Bool)
(declare-fun spacer_proxy!77 () Bool)
(declare-fun spacer_proxy!78 () Bool)
(declare-fun spacer_proxy!79 () Bool)
(declare-fun spacer_proxy!80 () Bool)
(declare-fun spacer_proxy!81 () Bool)
(declare-fun |INV#level_5!19| () Bool)
(declare-fun spacer_proxy!82 () Bool)
(declare-fun spacer_proxy!83 () Bool)
(declare-fun INV_ext0_n () Bool)
(declare-fun |INV#level_6!21| () Bool)
(declare-fun |INV#level_7!23| () Bool)
(assert (let ((a!1 (not (or INV_5_n
                    INV_4_n
                    INV_3_n
                    (not (= INV_0_n (/ 1.0 128.0)))
                    (not (= INV_1_n (/ 13.0 128.0)))
                    (not (= INV_2_n (/ 13.0 128.0)))))))
  (or (not INV__tr1) (not |vsolver#0|) a!1)))
(assert (let ((a!1 (>= (+ (* (/ 3.0 32.0) aux!5_n)
                  (* (/ 57.0 64.0) aux!6_n)
                  (* (- (/ 41.0 128.0)) aux!8_n))
               (- (/ 3.0 128.0))))
      (a!2 (<= (+ (* (/ 41.0 128.0) aux!5_n)
                  (* (- (/ 119.0 128.0)) aux!6_n)
                  (* (/ 15.0 128.0) aux!7_n)
                  (* (/ 5.0 16.0) aux!8_n))
               (/ 5.0 128.0)))
      (a!3 (<= (+ (* (/ 9.0 128.0) aux!5_n)
                  (* (/ 73.0 64.0) aux!6_n)
                  (* (- (/ 11.0 32.0)) aux!7_n)
                  (* (- (/ 1.0 4.0)) aux!8_n))
               (/ 9.0 128.0))))
(let ((a!4 (ite a!3
                (= (+ INV_0_n
                      (* (/ 9.0 128.0) aux!5_n)
                      (* (/ 73.0 64.0) aux!6_n)
                      (* (- (/ 11.0 32.0)) aux!7_n)
                      (* (- (/ 1.0 4.0)) aux!8_n))
                   (/ 9.0 128.0))
                (= INV_0_n aux!4_n)))
      (a!5 (ite a!2
                (= (+ INV_1_n
                      (* (/ 41.0 128.0) aux!5_n)
                      (* (- (/ 119.0 128.0)) aux!6_n)
                      (* (/ 15.0 128.0) aux!7_n)
                      (* (/ 5.0 16.0) aux!8_n))
                   (/ 5.0 128.0))
                (= INV_1_n aux!3_n)))
      (a!6 (ite a!1
                (= (+ INV_2_n
                      (* (- (/ 3.0 32.0)) aux!5_n)
                      (* (- (/ 57.0 64.0)) aux!6_n)
                      (* (/ 41.0 128.0) aux!8_n))
                   (/ 3.0 128.0))
                (= INV_2_n aux!2_n))))
(let ((a!7 (or (= INV_5_n a!1)
               (= INV_4_n a!2)
               (= INV_3_n a!3)
               (not (ite INV_3_0 (= aux!8_n 0.0) (= aux!8_n INV_0_0)))
               (not (ite INV_4_0 (= aux!7_n 0.0) (= aux!7_n INV_1_0)))
               (not (ite INV_5_0 (= aux!6_n 0.0) (= aux!6_n INV_2_0)))
               (not a!4)
               (not a!5)
               (not a!6)
               (not (>= aux!5_n 0.0))
               (not (<= aux!5_n 0.0)))))
  (or (not INV__tr0) (not |vsolver#0|) (not a!7))))))
(assert (or (not INV__tr0) |INV#level_0!9| (not |vsolver#0|)))
(assert (let ((a!1 (not (or INV_3_0
                    INV_4_0
                    INV_5_0
                    (not (= INV_0_0 (/ 1.0 128.0)))
                    (not (= INV_1_0 (/ 13.0 128.0)))
                    (not (= INV_2_0 (/ 13.0 128.0)))))))
  (or (not INV__tr0) |INV#reach_tag_0_0| a!1 (not |vsolver#0|))))
(assert (or (not INV_4_n) |INV#level_0!9| (not |vsolver#0|)))
(assert (or (not INV__tr0) (not INV_4_0) |INV#level_1!13| (not |vsolver#0|)))
(assert (let ((a!1 (not (<= (+ (* (/ 15.0 128.0) INV_1_n)
                       (* (- (/ 119.0 128.0)) INV_2_n)
                       (* (/ 5.0 16.0) INV_0_n))
                    (/ 5.0 128.0)))))
  (or (not |vsolver#0|) (not spacer_proxy!0) a!1)))
(assert (let ((a!1 (not (>= (+ (* (/ 57.0 64.0) INV_2_n) (* (- (/ 41.0 128.0)) INV_0_n))
                    (- (/ 3.0 128.0))))))
  (or (not |vsolver#0|) a!1 (not spacer_proxy!1))))
(assert (let ((a!1 (not (>= (+ (* (/ 11.0 32.0) INV_1_n)
                       (* (- (/ 73.0 64.0)) INV_2_n)
                       (* (/ 1.0 4.0) INV_0_n))
                    (- (/ 9.0 128.0))))))
  (or (not |vsolver#0|) (not spacer_proxy!2) a!1)))
(assert (or |INV#level_0!9|
    (not |vsolver#0|)
    (>= (+ INV_1_n (* (- (/ 1016.0 1523.0)) INV_0_n)) (/ 18783.0 194944.0))))
(assert (or (not INV__tr0)
    |INV#level_1!13|
    (not |vsolver#0|)
    (<= (+ (* (/ 1016.0 1523.0) INV_0_0) (* (- 1.0) INV_1_0))
        (- (/ 18783.0 194944.0)))))
(assert (or (not |vsolver#0|)
    (>= (+ (* (/ 11.0 32.0) INV_1_n)
           (* (- (/ 73.0 64.0)) INV_2_n)
           (* (/ 1.0 4.0) INV_0_n))
        (- (/ 9.0 128.0)))
    (not spacer_proxy!3)))
(assert (or |INV#level_0!9|
    (not |vsolver#0|)
    (<= (+ INV_1_n (* (- (/ 119.0 15.0)) INV_2_n) (* (/ 8.0 3.0) INV_0_n))
        (- (/ 41.0 60.0)))))
(assert (or (not INV__tr0)
    |INV#level_1!13|
    (not |vsolver#0|)
    (<= (+ (* (/ 8.0 3.0) INV_0_0) INV_1_0 (* (- (/ 119.0 15.0)) INV_2_0))
        (- (/ 41.0 60.0)))))
(assert (let ((a!1 (not (<= (+ (* (/ 15.0 128.0) INV_1_n)
                       (* (- (/ 119.0 128.0)) INV_2_n))
                    (/ 5.0 128.0)))))
  (or (not |vsolver#0|) a!1 (not spacer_proxy!4))))
(assert (let ((a!1 (not (>= (+ (* (/ 11.0 32.0) INV_1_n) (* (- (/ 73.0 64.0)) INV_2_n))
                    (- (/ 9.0 128.0))))))
  (or (not |vsolver#0|) (not spacer_proxy!5) a!1)))
(assert (or (not |vsolver#0|) (not spacer_proxy!6) (not (>= INV_2_n (- (/ 1.0 38.0))))))
(assert (or (not INV_3_n) |INV#level_0!9| (not |vsolver#0|)))
(assert (or (not INV__tr0) (not INV_3_0) |INV#level_1!13| (not |vsolver#0|)))
(assert (or (not |vsolver#0|) (= INV_0_n 0.0) (not spacer_proxy!7)))
(assert (or (not |vsolver#0|) (not (<= INV_1_n (/ 1.0 3.0))) (not spacer_proxy!8)))
(assert (or (not |vsolver#0|) (>= INV_1_n (- (/ 9.0 44.0))) (not spacer_proxy!9)))
(assert (or (not INV_5_n) |INV#level_0!9| (not |vsolver#0|)))
(assert (or (not INV__tr0) (not INV_5_0) |INV#level_1!13| (not |vsolver#0|)))
(assert (or (not INV_4_n) |INV#level_1!13| (not |vsolver#0|)))
(assert (or (not INV__tr0) (not INV_4_0) (not |vsolver#0|) |INV#level_2!14|))
(assert (let ((a!1 (not (>= (+ INV_1_n (* (- (/ 1016.0 1523.0)) INV_0_n))
                    (/ 18783.0 194944.0)))))
  (or (not |vsolver#0|) (not spacer_proxy!10) a!1)))
(assert (let ((a!1 (not (<= (+ INV_1_n
                       (* (- (/ 119.0 15.0)) INV_2_n)
                       (* (/ 8.0 3.0) INV_0_n))
                    (- (/ 41.0 60.0))))))
  (or (not |vsolver#0|) a!1 (not spacer_proxy!11))))
(assert (or (not |vsolver#0|)
    (not spacer_proxy!12)
    (<= (+ (* (/ 19.0 2.0) INV_2_n) (* (- (/ 41.0 12.0)) INV_0_n))
        (- (/ 1.0 4.0)))))
(assert (let ((a!1 (not (<= (+ (* (/ 451.0 4096.0) INV_1_n)
                       (* (- (/ 4961.0 32768.0)) INV_2_n)
                       (* (/ 205.0 65536.0) INV_0_n))
                    (- (/ 309.0 65536.0))))))
  (or (not |vsolver#0|) (not spacer_proxy!13) a!1)))
(assert (or (not |vsolver#0|)
    (not spacer_proxy!14)
    (<= (+ (* (/ 15.0 128.0) INV_1_n)
           (* (- (/ 1017.0 256.0)) INV_2_n)
           (* (/ 2161.0 1536.0) INV_0_n))
        (/ 61.0 512.0))))
(assert (let ((a!1 (not (<= (+ (* (/ 1535.0 16384.0) INV_1_n)
                       (* (/ 10415.0 32768.0) INV_2_n)
                       (* (- (/ 10605.0 65536.0)) INV_0_n))
                    (- (/ 155.0 65536.0))))))
  (or (not |vsolver#0|) a!1 (not spacer_proxy!15))))
(assert (or (not |vsolver#0|)
    (not spacer_proxy!16)
    (>= (+ (* (/ 11.0 32.0) INV_1_n)
           (* (- (/ 121.0 256.0)) INV_2_n)
           (* (/ 5.0 512.0) INV_0_n))
        (- (/ 45.0 512.0)))))
(assert (or (not |vsolver#0|)
    (not spacer_proxy!17)
    (>= (+ (* (/ 19.0 2.0) INV_2_n) (* (- (/ 41.0 12.0)) INV_0_n))
        (- (/ 1.0 4.0)))))
(assert (or (not |vsolver#0|)
    (not spacer_proxy!18)
    (>= (+ (* (/ 187.0 4096.0) INV_1_n)
           (* (/ 10219.0 8192.0) INV_2_n)
           (* (- (/ 23651.0 49152.0)) INV_0_n))
        (- (/ 2183.0 16384.0)))))
(assert (or |INV#level_0!9|
    (not |vsolver#0|)
    (<= (+ (* (/ 188805.0 168272.0) INV_1_n)
           (* (- (/ 1666125.0 168272.0)) INV_2_n)
           (* (/ 62935.0 21034.0) INV_0_n))
        (- (/ 9468729.0 12788672.0)))))
(assert (or (not INV__tr0)
    |INV#level_1!13|
    (not |vsolver#0|)
    (<= (+ (* (/ 62935.0 21034.0) INV_0_0)
           (* (/ 188805.0 168272.0) INV_1_0)
           (* (- (/ 1666125.0 168272.0)) INV_2_0))
        (- (/ 9468729.0 12788672.0)))))
(assert (let ((a!1 (not (<= (+ (* (/ 1845.0 4397.0) INV_1_n)
                       (* (- (/ 14637.0 4397.0)) INV_2_n)
                       (* (/ 4920.0 4397.0) INV_0_n))
                    (- (/ 7737069.0 42774016.0))))))
  (or (not |vsolver#0|) a!1 (not spacer_proxy!19))))
(assert (let ((a!1 (not (<= (+ INV_1_n
                       (* (- (/ 119.0 15.0)) INV_2_n)
                       (* (/ 8.0 3.0) INV_0_n))
                    (- (/ 41.0 60.0))))))
  (or (not |vsolver#0|) a!1 (not spacer_proxy!20))))
(assert (or INV_3_0
    INV_4_0
    (not INV__tr0)
    (not |vsolver#0|)
    (<= (+ (* (/ 8.0 3.0) INV_0_0) INV_1_0 (* (- (/ 119.0 15.0)) INV_2_0))
        (- (/ 41.0 60.0)))
    (<= (+ (* (/ 4920.0 4397.0) INV_0_0)
           (* (/ 1845.0 4397.0) INV_1_0)
           (* (- (/ 14637.0 4397.0)) INV_2_0))
        (- (/ 7737069.0 42774016.0)))
    (not spacer_proxy!21)))
(assert (or INV_4_0
    (not INV__tr0)
    (not |vsolver#0|)
    (<= (+ (* (/ 8.0 3.0) INV_0_0) INV_1_0 (* (- (/ 119.0 15.0)) INV_2_0))
        (- (/ 41.0 60.0)))
    (<= (+ (* (/ 4920.0 4397.0) INV_0_0)
           (* (/ 1845.0 4397.0) INV_1_0)
           (* (- (/ 14637.0 4397.0)) INV_2_0))
        (- (/ 7737069.0 42774016.0)))
    (not spacer_proxy!22)))
(assert (or INV_3_0
    (not INV__tr0)
    (not |vsolver#0|)
    (<= (+ (* (/ 8.0 3.0) INV_0_0) INV_1_0 (* (- (/ 119.0 15.0)) INV_2_0))
        (- (/ 41.0 60.0)))
    (<= (+ (* (/ 4920.0 4397.0) INV_0_0)
           (* (/ 1845.0 4397.0) INV_1_0)
           (* (- (/ 14637.0 4397.0)) INV_2_0))
        (- (/ 7737069.0 42774016.0)))
    (not spacer_proxy!23)))
(assert (or INV_3_0
    (not INV__tr0)
    (not |vsolver#0|)
    (<= (+ (* (/ 4920.0 4397.0) INV_0_0)
           (* (/ 1845.0 4397.0) INV_1_0)
           (* (- (/ 14637.0 4397.0)) INV_2_0))
        (- (/ 7737069.0 42774016.0)))
    (not spacer_proxy!24)))
(assert (or INV_3_0 (not INV__tr0) (not |vsolver#0|) (not spacer_proxy!25)))
(assert (or INV_3_n
    |INV#level_1!13|
    (not |vsolver#0|)
    (<= (+ (* (/ 1845.0 4397.0) INV_1_n)
           (* (- (/ 14637.0 4397.0)) INV_2_n)
           (* (/ 4920.0 4397.0) INV_0_n))
        (- (/ 7737069.0 42774016.0)))))
(assert (or INV_3_0
    (not INV__tr0)
    (not |vsolver#0|)
    |INV#level_2!14|
    (<= (+ (* (/ 4920.0 4397.0) INV_0_0)
           (* (/ 1845.0 4397.0) INV_1_0)
           (* (- (/ 14637.0 4397.0)) INV_2_0))
        (- (/ 7737069.0 42774016.0)))))
(assert (or (not |vsolver#0|)
    (>= (+ (* (/ 11.0 32.0) INV_1_n) (* (- (/ 73.0 64.0)) INV_2_n))
        (- (/ 9.0 128.0)))
    (not spacer_proxy!26)))
(assert (let ((a!1 (not (<= (+ (* (/ 15.0 128.0) INV_1_n)
                       (* (- (/ 119.0 128.0)) INV_2_n))
                    (- (/ 41.0 512.0))))))
  (or (not |vsolver#0|) a!1 (not spacer_proxy!27))))
(assert (or (not |vsolver#0|) (not spacer_proxy!28) (not (>= INV_2_n 0.0))))
(assert (or (not INV__tr0)
    (not |vsolver#0|)
    (<= (+ (* (/ 15.0 128.0) INV_1_0) (* (- (/ 119.0 128.0)) INV_2_0))
        (- (/ 41.0 512.0)))
    (not (= INV_0_0 0.0))
    (>= INV_2_0 0.0)
    (not spacer_proxy!29)))
(assert (or INV_5_0
    (not INV__tr0)
    (not |vsolver#0|)
    (<= (+ (* (/ 15.0 128.0) INV_1_0) (* (- (/ 119.0 128.0)) INV_2_0))
        (- (/ 41.0 512.0)))
    (not spacer_proxy!30)
    (not (= INV_0_0 0.0))))
(assert (or INV_5_0
    (not INV__tr0)
    (not |vsolver#0|)
    (<= (+ (* (/ 15.0 128.0) INV_1_0) (* (- (/ 119.0 128.0)) INV_2_0))
        (- (/ 41.0 512.0)))
    (>= INV_2_0 0.0)
    (not spacer_proxy!31)))
(assert (or INV_5_n (not |vsolver#0|) (>= INV_2_n 0.0)))
(assert (or INV_5_0 (not INV__tr0) (not |vsolver#0|) (>= INV_2_0 0.0)))
(assert (or (not |vsolver#0|) (not spacer_proxy!32) (not (<= INV_0_n (/ 3.0 41.0)))))
(assert (let ((a!1 (not (>= (+ (* (/ 11.0 32.0) INV_1_n) (* (/ 1.0 4.0) INV_0_n))
                    (- (/ 9.0 128.0))))))
  (or (not |vsolver#0|) a!1 (not spacer_proxy!33))))
(assert (let ((a!1 (not (<= (+ (* (/ 15.0 128.0) INV_1_n) (* (/ 5.0 16.0) INV_0_n))
                    (/ 5.0 128.0)))))
  (or (not |vsolver#0|) (not spacer_proxy!34) a!1)))
(assert (or (not |vsolver#0|) (not (>= INV_1_n (- (/ 9.0 44.0)))) (not spacer_proxy!35)))
(assert (or INV_4_0
    (not INV__tr0)
    (not |vsolver#0|)
    (>= INV_1_0 (- (/ 9.0 44.0)))
    (not spacer_proxy!36)))
(assert (or (not INV__tr0)
    (not |vsolver#0|)
    (>= INV_1_0 (- (/ 9.0 44.0)))
    (not spacer_proxy!37)))
(assert (or INV_4_0 (not INV__tr0) (not |vsolver#0|) (not spacer_proxy!38)))
(assert (or INV_4_n (not |vsolver#0|) (>= INV_1_n (- (/ 9.0 44.0)))))
(assert (or INV_4_0 (not INV__tr0) (not |vsolver#0|) (>= INV_1_0 (- (/ 9.0 44.0)))))
(assert (or (not |vsolver#0|) (not spacer_proxy!39) (not (<= INV_0_n (/ 1.0 8.0)))))
(assert (or (not |vsolver#0|) (not spacer_proxy!40) (>= INV_0_n (- (/ 9.0 32.0)))))
(assert (or (not |vsolver#0|) (= INV_1_n 0.0) (not spacer_proxy!41)))
(assert (or (not INV__tr0) (not INV_5_0) (not |vsolver#0|) (not spacer_proxy!42)))
(assert (or (not INV_5_n) |INV#level_1!13| (not |vsolver#0|)))
(assert (or (not INV__tr0) (not INV_5_0) (not |vsolver#0|) |INV#level_2!14|))
(assert (or (not |vsolver#0|) (>= INV_2_n (- (/ 1.0 38.0))) (not spacer_proxy!43)))
(assert (let ((a!1 (not (<= (+ (* (/ 1228800.0 1251523.0) INV_1_n)
                       (* (- (/ 81920.0 10517.0)) INV_2_n))
                    (- (/ 103983001.0 160194944.0))))))
  (or (not |vsolver#0|) (not spacer_proxy!44) a!1)))
(assert (or INV_4_0
    INV_5_0
    (not INV__tr0)
    (not |vsolver#0|)
    (<= (+ (* (/ 1228800.0 1251523.0) INV_1_0)
           (* (- (/ 81920.0 10517.0)) INV_2_0))
        (- (/ 103983001.0 160194944.0)))
    (not spacer_proxy!45)))
(assert (or INV_5_0
    (not INV__tr0)
    (not |vsolver#0|)
    (<= (+ (* (/ 1228800.0 1251523.0) INV_1_0)
           (* (- (/ 81920.0 10517.0)) INV_2_0))
        (- (/ 103983001.0 160194944.0)))
    (not spacer_proxy!46)))
(assert (or (not INV__tr0)
    (not |vsolver#0|)
    (not spacer_proxy!47)
    (<= (+ (* (/ 1228800.0 1251523.0) INV_1_0)
           (* (- (/ 81920.0 10517.0)) INV_2_0))
        (- (/ 103983001.0 160194944.0)))))
(assert (or |INV#level_1!13|
    (not |vsolver#0|)
    (<= (+ (* (/ 1228800.0 1251523.0) INV_1_n)
           (* (- (/ 81920.0 10517.0)) INV_2_n))
        (- (/ 103983001.0 160194944.0)))))
(assert (or (not INV__tr0)
    (not |vsolver#0|)
    |INV#level_2!14|
    (<= (+ (* (/ 1228800.0 1251523.0) INV_1_0)
           (* (- (/ 81920.0 10517.0)) INV_2_0))
        (- (/ 103983001.0 160194944.0)))))
(assert (or (not INV_4_n) (not |vsolver#0|) |INV#level_2!14|))
(assert (or (not INV__tr0) (not INV_4_0) (not |vsolver#0|) |INV#level_3!15|))
(assert (let ((a!1 (not (<= (+ (* (/ 188805.0 168272.0) INV_1_n)
                       (* (- (/ 1666125.0 168272.0)) INV_2_n)
                       (* (/ 62935.0 21034.0) INV_0_n))
                    (- (/ 9468729.0 12788672.0))))))
  (or (not |vsolver#0|) (not spacer_proxy!48) a!1)))
(assert (let ((a!1 (not (<= (+ (* (/ 1845.0 4397.0) INV_1_n)
                       (* (- (/ 14637.0 4397.0)) INV_2_n)
                       (* (/ 4920.0 4397.0) INV_0_n))
                    (- (/ 7737069.0 42774016.0))))))
  (or (not |vsolver#0|) (not spacer_proxy!49) a!1)))
(assert (or INV_3_n
    (not |vsolver#0|)
    |INV#level_2!14|
    (<= (+ (* (/ 1845.0 4397.0) INV_1_n)
           (* (- (/ 14637.0 4397.0)) INV_2_n)
           (* (/ 4920.0 4397.0) INV_0_n))
        (- (/ 7737069.0 42774016.0)))))
(assert (or INV_3_0
    (not INV__tr0)
    (not |vsolver#0|)
    |INV#level_3!15|
    (<= (+ (* (/ 4920.0 4397.0) INV_0_0)
           (* (/ 1845.0 4397.0) INV_1_0)
           (* (- (/ 14637.0 4397.0)) INV_2_0))
        (- (/ 7737069.0 42774016.0)))))
(assert (let ((a!1 (not (<= (+ (* (/ 1228800.0 1251523.0) INV_1_n)
                       (* (- (/ 81920.0 10517.0)) INV_2_n))
                    (- (/ 103983001.0 160194944.0))))))
  (or (not |vsolver#0|) a!1 (not spacer_proxy!50))))
(assert (or (not |vsolver#0|)
    (<= (+ (* (/ 15.0 128.0) INV_1_n)
           (* (- (/ 119.0 128.0)) INV_2_n)
           (* (/ 5.0 16.0) INV_0_n))
        (/ 343.0 1408.0))
    (not spacer_proxy!51)))
(assert (let ((a!1 (not (>= (+ (* (/ 15.0 128.0) INV_1_n)
                       (* (- (/ 119.0 128.0)) INV_2_n)
                       (* (/ 5.0 16.0) INV_0_n))
                    (- (/ 113.0 384.0))))))
  (or (not |vsolver#0|) a!1 (not spacer_proxy!52))))
(assert (or (not |vsolver#0|)
    (<= (+ (* (/ 15.0 128.0) INV_1_n)
           (* (- (/ 119.0 128.0)) INV_2_n)
           (* (/ 5.0 16.0) INV_0_n))
        (/ 5.0 128.0))
    (not spacer_proxy!53)))
(assert (let ((a!1 (not (>= (+ (* (/ 1737360.0 485837.0) INV_1_n)
                       (* (- (/ 1016.0 1523.0)) INV_0_n))
                    (- (/ 294529077.0 684058496.0))))))
  (or (not |vsolver#0|) (not spacer_proxy!54) a!1)))
(assert (or (not |vsolver#0|)
    (<= (+ (* (/ 16924800.0 3354923.0) INV_1_n)
           (* (/ 81920.0 10517.0) INV_2_n)
           (* (- (/ 39360.0 10517.0)) INV_0_n))
        (- (/ 279497623.0 73808306.0)))
    (not spacer_proxy!55)))
(assert (let ((a!1 (not (>= (+ (* (/ 39360.0 10517.0) INV_0_0)
                       (* (- (/ 16924800.0 3354923.0)) INV_1_0)
                       (* (- (/ 81920.0 10517.0)) INV_2_0))
                    (/ 279497623.0 73808306.0)))))
  (or INV_3_0
      INV_5_0
      (not INV__tr0)
      (not |vsolver#0|)
      a!1
      (<= (+ (* (/ 1016.0 1523.0) INV_0_0)
             (* (- (/ 1737360.0 485837.0)) INV_1_0))
          (/ 294529077.0 684058496.0))
      (not spacer_proxy!56))))
(assert (let ((a!1 (not (>= (+ (* (/ 39360.0 10517.0) INV_0_0)
                       (* (- (/ 16924800.0 3354923.0)) INV_1_0)
                       (* (- (/ 81920.0 10517.0)) INV_2_0))
                    (/ 279497623.0 73808306.0)))))
  (or INV_5_0
      (not INV__tr0)
      (not |vsolver#0|)
      a!1
      (<= (+ (* (/ 1016.0 1523.0) INV_0_0)
             (* (- (/ 1737360.0 485837.0)) INV_1_0))
          (/ 294529077.0 684058496.0))
      (not spacer_proxy!57))))
(assert (let ((a!1 (not (>= (+ (* (/ 39360.0 10517.0) INV_0_0)
                       (* (- (/ 16924800.0 3354923.0)) INV_1_0)
                       (* (- (/ 81920.0 10517.0)) INV_2_0))
                    (/ 279497623.0 73808306.0)))))
  (or INV_3_0
      (not INV__tr0)
      (not |vsolver#0|)
      a!1
      (<= (+ (* (/ 1016.0 1523.0) INV_0_0)
             (* (- (/ 1737360.0 485837.0)) INV_1_0))
          (/ 294529077.0 684058496.0))
      (not spacer_proxy!58))))
(assert (let ((a!1 (not (>= (+ (* (/ 39360.0 10517.0) INV_0_0)
                       (* (- (/ 16924800.0 3354923.0)) INV_1_0)
                       (* (- (/ 81920.0 10517.0)) INV_2_0))
                    (/ 279497623.0 73808306.0)))))
  (or INV_3_0 (not INV__tr0) (not |vsolver#0|) a!1 (not spacer_proxy!59))))
(assert (let ((a!1 (not (<= (+ (* (/ 16924800.0 3354923.0) INV_1_n)
                       (* (/ 81920.0 10517.0) INV_2_n)
                       (* (- (/ 39360.0 10517.0)) INV_0_n))
                    (- (/ 279497623.0 73808306.0))))))
  (or INV_3_n (not |vsolver#0|) |INV#level_2!14| a!1)))
(assert (let ((a!1 (not (>= (+ (* (/ 39360.0 10517.0) INV_0_0)
                       (* (- (/ 16924800.0 3354923.0)) INV_1_0)
                       (* (- (/ 81920.0 10517.0)) INV_2_0))
                    (/ 279497623.0 73808306.0)))))
  (or INV_3_0 (not INV__tr0) (not |vsolver#0|) |INV#level_3!15| a!1)))
(assert (or (not |vsolver#0|) (>= INV_1_n (/ 13.0 128.0)) (not spacer_proxy!60)))
(assert (or (not INV__tr0)
    (not INV_3_0)
    (not INV_5_0)
    (not |vsolver#0|)
    (not (>= INV_1_0 (/ 13.0 128.0)))
    (not spacer_proxy!61)))
(assert (or (not INV__tr0)
    (not INV_3_0)
    (not |vsolver#0|)
    (not (>= INV_1_0 (/ 13.0 128.0)))
    (not spacer_proxy!62)))
(assert (or (not INV__tr0)
    (not INV_5_0)
    (not |vsolver#0|)
    (not (>= INV_1_0 (/ 13.0 128.0)))
    (not spacer_proxy!63)))
(assert (or (not INV__tr0) (not INV_5_0) (not |vsolver#0|) (not spacer_proxy!64)))
(assert (or (not INV_5_n)
    (not |vsolver#0|)
    |INV#level_2!14|
    (not (>= INV_1_n (/ 13.0 128.0)))))
(assert (or (not INV__tr0)
    (not INV_5_0)
    (not |vsolver#0|)
    |INV#level_3!15|
    (not (>= INV_1_0 (/ 13.0 128.0)))))
(assert (or (not |vsolver#0|)
    (>= (+ (* (/ 11.0 32.0) INV_1_n) (* (/ 1.0 4.0) INV_0_n)) (- (/ 9.0 128.0)))
    (not spacer_proxy!65)))
(assert (or INV_3_n (not INV_5_n) (not |vsolver#0|) |INV#level_2!14|))
(assert (or INV_3_0 (not INV__tr0) (not INV_5_0) (not |vsolver#0|) |INV#level_3!15|))
(assert (let ((a!1 (not (<= (+ (* (/ 15.0 128.0) INV_1_n)
                       (* (- (/ 119.0 128.0)) INV_2_n))
                    (- (/ 105420354009.0 1889785610240.0))))))
  (or (not |vsolver#0|) a!1 (not spacer_proxy!66))))
(assert (or (not |vsolver#0|)
    (not spacer_proxy!67)
    (>= (+ (* (/ 144424960.0 3354923.0) INV_1_n)
           (* (- (/ 180101120.0 3354923.0)) INV_2_n))
        (/ 310748183.0 73808306.0))))
(assert (let ((a!1 (not (>= (+ (* (/ 144424960.0 3354923.0) INV_1_0)
                       (* (- (/ 180101120.0 3354923.0)) INV_2_0))
                    (/ 310748183.0 73808306.0)))))
  (or INV_4_0
      INV_5_0
      (not INV__tr0)
      (not |vsolver#0|)
      (<= (+ (* (/ 15.0 128.0) INV_1_0) (* (- (/ 119.0 128.0)) INV_2_0))
          (- (/ 105420354009.0 1889785610240.0)))
      a!1
      (not spacer_proxy!68))))
(assert (let ((a!1 (not (>= (+ (* (/ 144424960.0 3354923.0) INV_1_0)
                       (* (- (/ 180101120.0 3354923.0)) INV_2_0))
                    (/ 310748183.0 73808306.0)))))
  (or INV_5_0
      (not INV__tr0)
      (not |vsolver#0|)
      (<= (+ (* (/ 15.0 128.0) INV_1_0) (* (- (/ 119.0 128.0)) INV_2_0))
          (- (/ 105420354009.0 1889785610240.0)))
      a!1
      (not spacer_proxy!69))))
(assert (let ((a!1 (not (>= (+ (* (/ 144424960.0 3354923.0) INV_1_0)
                       (* (- (/ 180101120.0 3354923.0)) INV_2_0))
                    (/ 310748183.0 73808306.0)))))
  (or (not INV__tr0)
      (not |vsolver#0|)
      (<= (+ (* (/ 15.0 128.0) INV_1_0) (* (- (/ 119.0 128.0)) INV_2_0))
          (- (/ 105420354009.0 1889785610240.0)))
      a!1
      (not spacer_proxy!70))))
(assert (or INV_5_0
    (not INV__tr0)
    (not |vsolver#0|)
    (<= (+ (* (/ 15.0 128.0) INV_1_0) (* (- (/ 119.0 128.0)) INV_2_0))
        (- (/ 105420354009.0 1889785610240.0)))
    (not spacer_proxy!71)))
(assert (let ((a!1 (not (>= (+ (* (/ 144424960.0 3354923.0) INV_1_0)
                       (* (- (/ 180101120.0 3354923.0)) INV_2_0))
                    (/ 310748183.0 73808306.0)))))
  (or INV_5_0 (not INV__tr0) (not |vsolver#0|) a!1 (not spacer_proxy!72))))
(assert (let ((a!1 (not (>= (+ (* (/ 144424960.0 3354923.0) INV_1_n)
                       (* (- (/ 180101120.0 3354923.0)) INV_2_n))
                    (/ 310748183.0 73808306.0)))))
  (or INV_5_n (not |vsolver#0|) |INV#level_2!14| a!1)))
(assert (let ((a!1 (not (>= (+ (* (/ 144424960.0 3354923.0) INV_1_0)
                       (* (- (/ 180101120.0 3354923.0)) INV_2_0))
                    (/ 310748183.0 73808306.0)))))
  (or INV_5_0 (not INV__tr0) (not |vsolver#0|) |INV#level_3!15| a!1)))
(assert (or (not INV_4_n) (not |vsolver#0|) |INV#level_3!15|))
(assert (or (not INV__tr0) (not INV_4_0) (not |vsolver#0|) |INV#level_4!17|))
(assert (or (not |vsolver#0|)
    (<= (+ (* (/ 16924800.0 3354923.0) INV_1_n)
           (* (/ 81920.0 10517.0) INV_2_n)
           (* (- (/ 39360.0 10517.0)) INV_0_n))
        (- (/ 279497623.0 73808306.0)))
    (not spacer_proxy!73)))
(assert (let ((a!1 (not (<= (+ (* (/ 16924800.0 3354923.0) INV_1_n)
                       (* (/ 81920.0 10517.0) INV_2_n)
                       (* (- (/ 39360.0 10517.0)) INV_0_n))
                    (- (/ 279497623.0 73808306.0))))))
  (or INV_3_n (not |vsolver#0|) |INV#level_3!15| a!1)))
(assert (let ((a!1 (not (>= (+ (* (/ 39360.0 10517.0) INV_0_0)
                       (* (- (/ 16924800.0 3354923.0)) INV_1_0)
                       (* (- (/ 81920.0 10517.0)) INV_2_0))
                    (/ 279497623.0 73808306.0)))))
  (or INV_3_0 (not INV__tr0) (not |vsolver#0|) |INV#level_4!17| a!1)))
(assert (or (not INV_5_n)
    (not |vsolver#0|)
    |INV#level_3!15|
    (not (>= INV_1_n (/ 13.0 128.0)))))
(assert (or (not INV__tr0)
    (not INV_5_0)
    (not |vsolver#0|)
    |INV#level_4!17|
    (not (>= INV_1_0 (/ 13.0 128.0)))))
(assert (or INV_3_n (not INV_5_n) (not |vsolver#0|) |INV#level_3!15|))
(assert (or INV_3_0 (not INV__tr0) (not INV_5_0) (not |vsolver#0|) |INV#level_4!17|))
(assert (or (not |vsolver#0|)
    (>= (+ (* (/ 144424960.0 3354923.0) INV_1_n)
           (* (- (/ 180101120.0 3354923.0)) INV_2_n))
        (/ 310748183.0 73808306.0))
    (not spacer_proxy!74)))
(assert (let ((a!1 (not (>= (+ (* (/ 144424960.0 3354923.0) INV_1_n)
                       (* (- (/ 180101120.0 3354923.0)) INV_2_n))
                    (/ 310748183.0 73808306.0)))))
  (or INV_5_n (not |vsolver#0|) |INV#level_3!15| a!1)))
(assert (let ((a!1 (not (>= (+ (* (/ 144424960.0 3354923.0) INV_1_0)
                       (* (- (/ 180101120.0 3354923.0)) INV_2_0))
                    (/ 310748183.0 73808306.0)))))
  (or INV_5_0 (not INV__tr0) (not |vsolver#0|) |INV#level_4!17| a!1)))
(assert (or (not |vsolver#0|)
    (>= (+ (* (/ 57.0 64.0) INV_2_n) (* (- (/ 41.0 128.0)) INV_0_n))
        (- (/ 3.0 128.0)))
    (not spacer_proxy!75)))
(assert (let ((a!1 (not (<= (+ (* (/ 12294373.0 99888960.0) INV_1_n)
                       (* (- (/ 1335659.0 12486120.0)) INV_2_n)
                       (* (/ 3354923.0 199777920.0) INV_0_n))
                    (/ 2954046511.0 562574622720.0)))))
  (or (not |vsolver#0|) a!1 (not spacer_proxy!76))))
(assert (or INV_3_0
    INV_5_0
    (not INV__tr0)
    (not |vsolver#0|)
    (<= (+ (* (/ 8.0 3.0) INV_0_0) INV_1_0 (* (- (/ 119.0 15.0)) INV_2_0))
        (- (/ 41.0 60.0)))
    (<= (+ (* (/ 3354923.0 199777920.0) INV_0_0)
           (* (/ 12294373.0 99888960.0) INV_1_0)
           (* (- (/ 1335659.0 12486120.0)) INV_2_0))
        (/ 2954046511.0 562574622720.0))
    (not spacer_proxy!77)))
(assert (or INV_5_0
    (not INV__tr0)
    (not |vsolver#0|)
    (<= (+ (* (/ 8.0 3.0) INV_0_0) INV_1_0 (* (- (/ 119.0 15.0)) INV_2_0))
        (- (/ 41.0 60.0)))
    (<= (+ (* (/ 3354923.0 199777920.0) INV_0_0)
           (* (/ 12294373.0 99888960.0) INV_1_0)
           (* (- (/ 1335659.0 12486120.0)) INV_2_0))
        (/ 2954046511.0 562574622720.0))
    (not spacer_proxy!78)))
(assert (or INV_3_0
    (not INV__tr0)
    (not |vsolver#0|)
    (<= (+ (* (/ 8.0 3.0) INV_0_0) INV_1_0 (* (- (/ 119.0 15.0)) INV_2_0))
        (- (/ 41.0 60.0)))
    (<= (+ (* (/ 3354923.0 199777920.0) INV_0_0)
           (* (/ 12294373.0 99888960.0) INV_1_0)
           (* (- (/ 1335659.0 12486120.0)) INV_2_0))
        (/ 2954046511.0 562574622720.0))
    (not spacer_proxy!79)))
(assert (or INV_3_0
    INV_5_0
    (not INV__tr0)
    (not |vsolver#0|)
    (<= (+ (* (/ 3354923.0 199777920.0) INV_0_0)
           (* (/ 12294373.0 99888960.0) INV_1_0)
           (* (- (/ 1335659.0 12486120.0)) INV_2_0))
        (/ 2954046511.0 562574622720.0))
    (not spacer_proxy!80)))
(assert (or INV_3_0 INV_5_0 (not INV__tr0) (not |vsolver#0|) (not spacer_proxy!81)))
(assert (or INV_5_n
    INV_3_n
    (not |vsolver#0|)
    |INV#level_4!17|
    (<= (+ (* (/ 12294373.0 99888960.0) INV_1_n)
           (* (- (/ 1335659.0 12486120.0)) INV_2_n)
           (* (/ 3354923.0 199777920.0) INV_0_n))
        (/ 2954046511.0 562574622720.0))))
(assert (or INV_3_0
    INV_5_0
    (not INV__tr0)
    (not |vsolver#0|)
    |INV#level_5!19|
    (<= (+ (* (/ 3354923.0 199777920.0) INV_0_0)
           (* (/ 12294373.0 99888960.0) INV_1_0)
           (* (- (/ 1335659.0 12486120.0)) INV_2_0))
        (/ 2954046511.0 562574622720.0))))
(assert (let ((a!1 (not (>= (+ (* (/ 939560.0 1335659.0) INV_1_n)
                       (* (/ 81920.0 10517.0) INV_2_n)
                       (* (- (/ 39360.0 10517.0)) INV_0_n))
                    (- (/ 19196875.0 29384498.0))))))
  (or (not |vsolver#0|) (not spacer_proxy!82) a!1)))
(assert (or INV_3_0
    INV_5_0
    (not INV__tr0)
    (not |vsolver#0|)
    (<= (+ (* (/ 8.0 3.0) INV_0_0) INV_1_0 (* (- (/ 119.0 15.0)) INV_2_0))
        (- (/ 41.0 60.0)))
    (not spacer_proxy!83)
    (<= (+ (* (/ 39360.0 10517.0) INV_0_0)
           (* (- (/ 939560.0 1335659.0)) INV_1_0)
           (* (- (/ 81920.0 10517.0)) INV_2_0))
        (/ 19196875.0 29384498.0))))
;; extra clause
(assert (or INV_ext0_n INV__tr0 INV__tr1 ))
(check-sat |vsolver#0|
 spacer_proxy!83
 (not INV_ext0_n)
 |INV#level_0!9|
 |INV#level_1!13|
 |INV#level_2!14|
 |INV#level_3!15|
 |INV#level_4!17|
 |INV#level_5!19|
 |INV#level_6!21|
 |INV#level_7!23|
 spacer_proxy!20
 (not INV_5_n)
 spacer_proxy!82
 (not INV_3_n)
)
(exit)
(:added-eqs          1123
 :arith-add-rows     9813
 :arith-assert-diseq 352
 :arith-assert-lower 2074
 :arith-assert-upper 1365
 :arith-bound-prop   419
 :arith-conflicts    70
 :arith-eq-adapter   190
 :arith-fixed-eqs    262
 :arith-offset-eqs   28
 :arith-pivots       539
 :conflicts          190
 :decisions          2967
 :del-clause         244
 :final-checks       52
 :minimized-lits     82
 :mk-bool-var        888
 :mk-clause          941
 :num-checks         124
 :propagations       8819
 :time               0.03)
(params arith.solver 2 random_seed 0 dump_benchmarks true dump_threshold 0.00 mbqi true arith.ignore_int true array.weak true)(act-lvl 4294967295)
(ind-gen (let ((a!1 (not (<= (+ (* (/ 39360.0 10517.0) INV_0_n)
                       (* (- (/ 939560.0 1335659.0)) INV_1_n)
                       (* (- (/ 81920.0 10517.0)) INV_2_n))
                    (/ 19196875.0 29384498.0))))
      (a!2 (not (<= (+ (* (/ 8.0 3.0) INV_0_n)
                       (* (- (/ 119.0 15.0)) INV_2_n)
                       INV_1_n)
                    (- (/ 41.0 60.0))))))
  (and (not INV_4_n) (not INV_3_n) (not INV_5_n) a!1 a!2))
)
