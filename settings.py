import datetime
MODEL_PATH='models'

def new_model_name(basename):
    x = datetime.datetime.now()
    return "%s-%s"%(basename, str(x))


