from app.estimation import Estimation
from config import config

def gaze_estimation(config_name):

    app = Estimation(__name__)
    app.config = config[config_name]

    return app
