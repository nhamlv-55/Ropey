from datetime import datetime
import os
MODEL_PATH='models'
if not os.path.exists(MODEL_PATH):
    os.makedirs(MODEL_PATH)

def new_model_name(basename):
    now = datetime.now()
    current_time = now.strftime("%d%m%y_%H_%M_%S")
    return "%s-%s"%(basename, current_time)

def new_model_path(exp_path):
    basename = os.path.dirname(exp_path)
    new_model_path = os.path.join(MODEL_PATH, new_model_name(basename))
    return new_model_path
