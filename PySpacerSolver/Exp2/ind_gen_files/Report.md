# SUMMARY:
## no policy: 10.12s
## with policy: 7.08s
# POLICY
```
{"Exp2/ind_gen_files/pool_solver_vsolver#0_9.smt2.with_lemma.smt2" : [2, 3],
 "Exp2/ind_gen_files/pool_solver_vsolver#0_21.smt2.with_lemma.smt2" : [0, 1, 3],
 "Exp2/ind_gen_files/pool_solver_vsolver#0_11.smt2.with_lemma.smt2" : [2, 3],
 "Exp2/ind_gen_files/pool_solver_vsolver#0_13.smt2.with_lemma.smt2" : [0, 1],
 "Exp2/ind_gen_files/pool_solver_vsolver#0_14.smt2.with_lemma.smt2" : [2, 3],
 "Exp2/ind_gen_files/pool_solver_vsolver#0_3.smt2.with_lemma.smt2" : [1, 2],
 "Exp2/ind_gen_files/pool_solver_vsolver#0_23.smt2.with_lemma.smt2" : [0, 1, 2, 3],
 "Exp2/ind_gen_files/pool_solver_vsolver#0_6.smt2.with_lemma.smt2" : [3],
 "Exp2/ind_gen_files/pool_solver_vsolver#0_17.smt2.with_lemma.smt2" : [1, 2, 3],
 "Exp2/ind_gen_files/pool_solver_vsolver#0_24.smt2.with_lemma.smt2" : [1, 4],
 "Exp2/ind_gen_files/pool_solver_vsolver#0_2.smt2.with_lemma.smt2" : [0, 1],
 "Exp2/ind_gen_files/pool_solver_vsolver#0_20.smt2.with_lemma.smt2" : [0, 1, 5],
 "Exp2/ind_gen_files/pool_solver_vsolver#0_5.smt2.with_lemma.smt2" : [1],
 "Exp2/ind_gen_files/pool_solver_vsolver#0_0.smt2.with_lemma.smt2" : [2, 3],
 "Exp2/ind_gen_files/pool_solver_vsolver#0_22.smt2.with_lemma.smt2" : [0, 1, 4],
 "Exp2/ind_gen_files/pool_solver_vsolver#0_19.smt2.with_lemma.smt2" : [0, 1, 2, 3]
}
```
# Details

## no policy
```
Run 1
nv3le@precious3:~/workspace/PySpacerSolver$ time PYTHONPATH=~/opt/z3/build/python/ python3 spacer_solver.py -input Exp2/ind_gen_files/
CRITICAL
50
Exp2/ind_gen_files/pool_solver_vsolver#0_9.smt2.with_lemma.smt2
CANNOT DROP: [2, 3]
Exp2/ind_gen_files/pool_solver_vsolver#0_21.smt2.with_lemma.smt2
CANNOT DROP: [0, 1, 3]
Exp2/ind_gen_files/pool_solver_vsolver#0_11.smt2.with_lemma.smt2
CANNOT DROP: [2, 3]
Exp2/ind_gen_files/pool_solver_vsolver#0_13.smt2.with_lemma.smt2
CANNOT DROP: [0, 1]
Exp2/ind_gen_files/pool_solver_vsolver#0_14.smt2.with_lemma.smt2
CANNOT DROP: [2, 3]
Exp2/ind_gen_files/pool_solver_vsolver#0_3.smt2.with_lemma.smt2
CANNOT DROP: [1, 2]
Exp2/ind_gen_files/pool_solver_vsolver#0_23.smt2.with_lemma.smt2
CANNOT DROP: [0, 1, 2, 3]
Exp2/ind_gen_files/pool_solver_vsolver#0_6.smt2.with_lemma.smt2
CANNOT DROP: [3]
Exp2/ind_gen_files/pool_solver_vsolver#0_17.smt2.with_lemma.smt2
CANNOT DROP: [1, 2, 3]
Exp2/ind_gen_files/pool_solver_vsolver#0_24.smt2.with_lemma.smt2
CANNOT DROP: [1, 4]
Exp2/ind_gen_files/pool_solver_vsolver#0_2.smt2.with_lemma.smt2
CANNOT DROP: [0, 1]
Exp2/ind_gen_files/pool_solver_vsolver#0_20.smt2.with_lemma.smt2
CANNOT DROP: [0, 1, 5]
Exp2/ind_gen_files/pool_solver_vsolver#0_5.smt2.with_lemma.smt2
CANNOT DROP: [1]
Exp2/ind_gen_files/pool_solver_vsolver#0_0.smt2.with_lemma.smt2
CANNOT DROP: [2, 3]
Exp2/ind_gen_files/pool_solver_vsolver#0_22.smt2.with_lemma.smt2
CANNOT DROP: [0, 1, 4]
Exp2/ind_gen_files/pool_solver_vsolver#0_19.smt2.with_lemma.smt2
CANNOT DROP: [0, 1, 2, 3]

real    0m9.995s
user    0m9.950s
sys     0m0.045s
```
```
Run 2
nv3le@precious3:~/workspace/PySpacerSolver$ time PYTHONPATH=~/opt/z3/build/python/ python3 spacer_solver.py -input Exp2/ind_gen_files/
CRITICAL
50
Exp2/ind_gen_files/pool_solver_vsolver#0_9.smt2.with_lemma.smt2
CANNOT DROP: [2, 3]
Exp2/ind_gen_files/pool_solver_vsolver#0_21.smt2.with_lemma.smt2
CANNOT DROP: [0, 1, 3]
Exp2/ind_gen_files/pool_solver_vsolver#0_11.smt2.with_lemma.smt2
CANNOT DROP: [2, 3]
Exp2/ind_gen_files/pool_solver_vsolver#0_13.smt2.with_lemma.smt2
CANNOT DROP: [0, 1]
Exp2/ind_gen_files/pool_solver_vsolver#0_14.smt2.with_lemma.smt2
CANNOT DROP: [2, 3]
Exp2/ind_gen_files/pool_solver_vsolver#0_3.smt2.with_lemma.smt2
CANNOT DROP: [1, 2]
Exp2/ind_gen_files/pool_solver_vsolver#0_23.smt2.with_lemma.smt2
CANNOT DROP: [0, 1, 2, 3]
Exp2/ind_gen_files/pool_solver_vsolver#0_6.smt2.with_lemma.smt2
CANNOT DROP: [3]
Exp2/ind_gen_files/pool_solver_vsolver#0_17.smt2.with_lemma.smt2
CANNOT DROP: [1, 2, 3]
Exp2/ind_gen_files/pool_solver_vsolver#0_24.smt2.with_lemma.smt2
CANNOT DROP: [1, 4]
Exp2/ind_gen_files/pool_solver_vsolver#0_2.smt2.with_lemma.smt2
CANNOT DROP: [0, 1]
Exp2/ind_gen_files/pool_solver_vsolver#0_20.smt2.with_lemma.smt2
CANNOT DROP: [0, 1, 5]
Exp2/ind_gen_files/pool_solver_vsolver#0_5.smt2.with_lemma.smt2
CANNOT DROP: [1]
Exp2/ind_gen_files/pool_solver_vsolver#0_0.smt2.with_lemma.smt2
CANNOT DROP: [2, 3]
Exp2/ind_gen_files/pool_solver_vsolver#0_22.smt2.with_lemma.smt2
CANNOT DROP: [0, 1, 4]
Exp2/ind_gen_files/pool_solver_vsolver#0_19.smt2.with_lemma.smt2
CANNOT DROP: [0, 1, 2, 3]

real    0m10.033s
user    0m9.984s
sys     0m0.048s
```
```
Run 3
nv3le@precious3:~/workspace/PySpacerSolver$ time PYTHONPATH=~/opt/z3/build/python/ python3 spacer_solver.py -input Exp2/ind_gen_files/
CRITICAL
50
Exp2/ind_gen_files/pool_solver_vsolver#0_9.smt2.with_lemma.smt2
CANNOT DROP: [2, 3]
Exp2/ind_gen_files/pool_solver_vsolver#0_21.smt2.with_lemma.smt2
CANNOT DROP: [0, 1, 3]
Exp2/ind_gen_files/pool_solver_vsolver#0_11.smt2.with_lemma.smt2
CANNOT DROP: [2, 3]
Exp2/ind_gen_files/pool_solver_vsolver#0_13.smt2.with_lemma.smt2
CANNOT DROP: [0, 1]
Exp2/ind_gen_files/pool_solver_vsolver#0_14.smt2.with_lemma.smt2
CANNOT DROP: [2, 3]
Exp2/ind_gen_files/pool_solver_vsolver#0_3.smt2.with_lemma.smt2
CANNOT DROP: [1, 2]
Exp2/ind_gen_files/pool_solver_vsolver#0_23.smt2.with_lemma.smt2
CANNOT DROP: [0, 1, 2, 3]
Exp2/ind_gen_files/pool_solver_vsolver#0_6.smt2.with_lemma.smt2
CANNOT DROP: [3]
Exp2/ind_gen_files/pool_solver_vsolver#0_17.smt2.with_lemma.smt2
CANNOT DROP: [1, 2, 3]
Exp2/ind_gen_files/pool_solver_vsolver#0_24.smt2.with_lemma.smt2
CANNOT DROP: [1, 4]
Exp2/ind_gen_files/pool_solver_vsolver#0_2.smt2.with_lemma.smt2
CANNOT DROP: [0, 1]
Exp2/ind_gen_files/pool_solver_vsolver#0_20.smt2.with_lemma.smt2
CANNOT DROP: [0, 1, 5]
Exp2/ind_gen_files/pool_solver_vsolver#0_5.smt2.with_lemma.smt2
CANNOT DROP: [1]
Exp2/ind_gen_files/pool_solver_vsolver#0_0.smt2.with_lemma.smt2
CANNOT DROP: [2, 3]
Exp2/ind_gen_files/pool_solver_vsolver#0_22.smt2.with_lemma.smt2
CANNOT DROP: [0, 1, 4]
Exp2/ind_gen_files/pool_solver_vsolver#0_19.smt2.with_lemma.smt2
CANNOT DROP: [0, 1, 2, 3]

real    0m10.346s
user    0m10.296s
sys     0m0.049s
```
--------------------------------------------------------------------
## with policy
```
Run 1
nv3le@precious3:~/workspace/PySpacerSolver$ time PYTHONPATH=~/opt/z3/build/python/ python3 spacer_solver.py -input Exp2/ind_gen_files/ -policy Exp2/ind_gen_files/policy.json 
CRITICAL
50
Exp2/ind_gen_files/pool_solver_vsolver#0_9.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_21.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_11.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_13.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_14.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_3.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_23.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_6.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_17.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_24.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_2.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_20.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_5.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_0.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_22.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_19.smt2.with_lemma.smt2
CANNOT DROP: []

real    0m6.951s
user    0m6.894s
sys     0m0.057s
```
```
Run 2
nv3le@precious3:~/workspace/PySpacerSolver$ time PYTHONPATH=~/opt/z3/build/python/ python3 spacer_solver.py -input Exp2/ind_gen_files/ -policy Exp2/ind_gen_files/policy.json 
CRITICAL
50
Exp2/ind_gen_files/pool_solver_vsolver#0_9.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_21.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_11.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_13.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_14.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_3.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_23.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_6.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_17.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_24.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_2.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_20.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_5.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_0.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_22.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_19.smt2.with_lemma.smt2
CANNOT DROP: []

real    0m7.161s
user    0m7.096s
sys     0m0.061s
```
```
Run 3
nv3le@precious3:~/workspace/PySpacerSolver$ time PYTHONPATH=~/opt/z3/build/python/ python3 spacer_solver.py -input Exp2/ind_gen_files/ -policy Exp2/ind_gen_files/policy.json 
CRITICAL
50
Exp2/ind_gen_files/pool_solver_vsolver#0_9.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_21.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_11.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_13.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_14.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_3.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_23.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_6.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_17.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_24.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_2.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_20.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_5.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_0.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_22.smt2.with_lemma.smt2
CANNOT DROP: []
Exp2/ind_gen_files/pool_solver_vsolver#0_19.smt2.with_lemma.smt2
CANNOT DROP: []

real    0m7.121s
user    0m7.064s
sys     0m0.057s
```
