# Training time details
We have specifically considered realistic applications where training time is not a bottleneck -- 
train once on one instance and apply to many similar instances (offline), 
or train during a very long run and apply to the rest of the run (online). 
We did not optimize training code, nor have we run training in an isolated environment where time measurements are meaningful.
Nonetheless, we are happy to share some statistics of training time

### All models
mean 18759.219733669208

std 38231.536908230875

min 16.67198920249939

max 165811.38317894936

median 1027.116681098938

__percentage of models that are trained in less than X hours__

less than 2 0.6602564102564102

less than 3 0.6858974358974359

less than 4 0.6923076923076923

less than 5 0.7564102564102564

less than 6 0.8076923076923077

less than 7 0.8397435897435898

### Offline models
mean 24637.847560567014

std 43689.16580019082

min 27.239623546600342

max 165811.38317894936

median 892.3176974058151

__percentage of models that are trained in less than X hours__

less than 2 0.6470588235294118

less than 3 0.6764705882352942

less than 4 0.6764705882352942

less than 5 0.6764705882352942

less than 6 0.7058823529411765

less than 7 0.7058823529411765

### Online models
mean 17120.913617976377

std 36396.91943578297

min 16.67198920249939

max 161942.81482434273

median 1102.2910166978836

__percentage of models that are trained in less than X hours__

less than 2 0.6639344262295082

less than 3 0.6885245901639344

less than 4 0.6967213114754098

less than 5 0.7786885245901639

less than 6 0.8360655737704918

less than 7 0.8770491803278688

