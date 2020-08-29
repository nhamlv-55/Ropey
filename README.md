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
`PYTHONPATH=~/workspace/ python3 X_train.py --json_config_file exp_config_1.json --threshold 0.99`
(Basically, you need to add the project to your PYTHONPATH)

#### Eval command
``
`PYTHONPATH=~/workspace/ python3 X_eval.py --test_folder grpc_test_runs/chc0002/ind_gen_files -Th 0.5 --model_path <some model.pt>`