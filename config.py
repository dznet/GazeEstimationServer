from numpy import zeros
#### Main config

class Config(object):
    HOST = '127.0.0.1'
    PORT = 5055
    ORIGIN_CAM = 'infrared'
    DATA_PATH = {'face_poses':  'cam_6',
                 'face_points': 'cam_7',
                 'gazes':       'cam_9'}
    ZEROS = zeros((3,), dtype='float')

class Development(Config):
    DEBUG = True
    SECRET_KEY = 'BMREJsCLAlv0tucfnkjOFp2bgzVIG3wKmiQTP1o6dWDXHa9ySZ'

class Testing(Config):
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'UzAEiR5yMpWTnOxdFlYgCBDKm6HwehutoQar9Xv0sISNLjGVq4'

class Production(Config):
    DEBUG = False
    SECRET_KEY = 'Qc87SZgNDwGojIAUtkKaYbpLq1snPJEfRe9T2uHx6lhMvz43yF'

config = {
    'development': Development,
    'testing': Testing,
    'production': Production,
    'default': Development
}

###############################################################################

class ScreenParams():

    def __init__(self, resolution, size):
        self.resolution = resolution
        self.size = inches_to_meters(size)

    def inches_to_meters(self, inches):
        return inches * 0.0254

class DatasetHandler():

    def __init__(self):
        self.images = ['basler', 'kinect', 'direct']
        self.metadata = ['basler', 'kinect', 'direct']
        self.dataset_path = r'C:\Users\Valik\Documents\GitHub\dataroot\RETNNA\BAS'

    def handle_path(self):
        return '\\1525974053\DataSource'

    def get_from(self):
        pass

class Utils():

    def __init__(self):
        pass

    def get_ml_models(self):
        PATH_TO_ESTIMATOR       = os.path.join(os.getcwd(), '/estimator.h5')
        PATH_TO_FACE_LANDMARKS  = os.path.join(os.getcwd(), '/face_landmarks.dat')
        PATH_TO_FACE_POINTS     = os.path.join(os.getcwd(), '/face_points_tutorial.mat')
        PATH_TO_HAARCASCADE     = os.path.join(os.getcwd(), '/haarcascade_frontalface_default.xml')

class CameraParams():

    def __init__(self, name):
        self.name = name
        if self.name == 'direct':
            self.id = 'cam_0'
            self.distortion = [0.1014, -0.2622, 0.0017, -0.0019]
            self.matrix = [[363.6643, 0., 257.1285],
                            [0., 363.7357, 208.6171],
                            [0., 0., 1.]]
        elif self.name == 'color':
            self.id = 'cam_1'
            self.distortion = [-0.0026, 0.1780, 0.0011, 0.0003]
            self.matrix = [[1051.7, 0., 957.6],
                            [0., 1051.7, 537.6],
                            [0.,  0., 1. ]]
        elif self.name == 'infrared':
            self.id = 'cam_2'
            self.distortion = [0.1014, -0.2622, 0.0017, -0.0019]
            self.matrix =  [[363.6643, 0., 257.1285],
                            [0., 363.7357, 208.6171],
                            [0., 0., 1.]]
        elif self.name == 'basler':
            self.id = 'cam_8'
            self.distortion = [-0.6819, 0.3729, -0.0021, -0.0005]
            self.matrix =  [[1896.6, 0., 654.8],
                            [0., 1897.9, 461.5],
                            [0., 0., 1. ]]
        else:
            self.id = 'unknown'
            self.distortion = dict()
            self.matrix =  dict()
