from os import getcwd
from app import config

class Camera():

    cameras = {}

    def __init__(self, name):
        self.cameras[name] = self
        self.dataset_path = getcwd()
        self.distortion = dict()
        self.id = str()
        self.matrix = dict()
        self.name = name
        self.rotation = config.ZEROS
        self.translation = config.ZEROS

    @classmethod
    def get(cls, name):
        return cls.cameras[name]

    @staticmethod
    def get_params(name):
        _params = CameraParams(name)
        return params if params else dict()

    @staticmethod
    def set_params(camera, params):
        _camera = CameraParams(camera.name)
        if isinstance(_camera, Camera):
            for key, value in params.items():
                setattr(_camera, key, value)
            return _camera

    def __repr__(self):
        return '<Camera({}), mtrx {}, dstrn {}>'.format(self.name,
                                                        self.matrix[:4],
                                                        self.distortion[:4])
