# Doping
Need https://github.com/nhamlv-55/PySpacerSolver clone in to the same folder. The folder should look like this
```
.
├── eval.py
├── eval_vis_server.py
├── generate_data.py
├── model.py
├── PySpacerSolver
├── pytorchtreelstm
├── README.md
├── requirements.txt
├── settings.py
├── templates
├── tests
├── train.py
├── utils
├── X_model.py
└── X_train.py

```
## Test
#### Train command
`python3 RNN_train.py -JI exp_config_getting_started.json`
The models are saved to a `model` folder where the code is run.

#### Eval command
Before running, please make sure the `PROJECT_ROOT` variable in `RNN_eval_runningtime.py` is set correctly
`
python RNN_eval_runningtime.py --test_folder _6counters.smt2.folder/ind_gen_files --gs_model_path _6counters.smt2.folder/models/getting_started.pt --getting_started
`