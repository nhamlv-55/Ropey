from datetime import datetime
import os
MODEL_PATH='models'
if not os.path.exists(MODEL_PATH):
    os.makedirs(MODEL_PATH)

def new_model_path(basename="M"):
    now = datetime.now()
    current_time = now.strftime("%d%m%y_%H_%M_%S")
    return os.path.join(MODEL_PATH, "%s-%s.pt"%(basename, current_time))

