import datetime
import os
MODEL_PATH='models'

def new_model_name(basename):
    x = datetime.datetime.now()
    return "%s-%s"%(basename, str(x))

def new_model_path(exp_path):
    basename = os.path.basename(exp_path)
    new_model_name = new_model_name(basename)
    new_model_path(os.path.join(MODEL_PATH), basename)
