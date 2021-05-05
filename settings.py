from datetime import datetime
import os
MODEL_PATH='models'
if not os.path.exists(MODEL_PATH):
    os.makedirs(MODEL_PATH)

def new_model_path(basename="M", epoch = -1):
    now = datetime.now()
    current_time = now.strftime("%d%m_%H_%M_%S")
    current_time+="Epoch{}".format(epoch)
    return os.path.join(MODEL_PATH, "%s-%s.pt"%(basename, current_time))

