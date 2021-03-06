from os import path as Path
from os import listdir
import json
from cv2 import imread
from app.frame import Frame
from numpy import array
from numpy import sqrt
from numpy import zeros


def face_point_to_array(dct):
    return array([dct['X'], dct['Y'], dct['Z']]).reshape(1, 3) * array([[1], [-1], [1]])


def quaternion_to_angle_axis(quaternion):
    """
    Converts angle-axis to quaternion
    :param quaternion: dict {'X': , 'Y': , 'Z': , 'W': }
    :return: angle-axis rotation vector
    """
    t = sqrt(1 - quaternion['W'] * quaternion['W'])
    if t:
        x = quaternion['X'] / t
        y = quaternion['Y'] / t
        z = quaternion['Z'] / t
        return array([[x], [y], [z]])
    else:
        return zeros((3, 1))


class ExperimentParser:

    def __init__(self, cams_dict, data_dict):
        self.path_to_dataset = None
        self.cams_dict = cams_dict
        self.data_dict = data_dict
        self.snapshots = None

    def fit(self, path_to_dataset):
        self.path_to_dataset = path_to_dataset
        self.snapshots = sorted([
            Path.splitext(frame_index)[0]
            for frame_index in listdir(Path.join(self.path_to_dataset, list(self.cams_dict.values())[0]))
        ])

    def read_frame(self, cam, snapshot):
        frame_file = Path.join(self.path_to_dataset, self.cams_dict[cam], snapshot + '.png')
        if Path.isfile(frame_file):
            return Frame(cam, imread(frame_file))
        else:
            return None

    def read_frames(self, snapshot):
        return {cam.name: self.read_frame(cam, snapshot) for cam, cam_dir in self.cams_dict.items()}

    @staticmethod
    def load_json_data(file, data_key):
        if data_key is 'face_points':
            return [face_point_to_array(point) for point in json.load(file)]
        if data_key is 'face_poses':
            return [quaternion_to_angle_axis(face_pose['FaceRotationQuaternion']) for face_pose in json.load(file)]
        if data_key is 'gazes':
            gaze = json.load(file)
            assert int(gaze['REC']['FPOGV'])
            return tuple(map(float, (gaze['REC']['FPOGX'], gaze['REC']['FPOGY'])))
        else:
            raise Exception('Wrong data_key.')

    def read_data(self, snapshot):
        data = {}
        try:
            for data_key, data_dir in self.data_dict.items():
                with open(Path.join(self.path_to_dataset, data_dir, snapshot + '.txt'), 'r') as file:
                    data[data_key] = self.load_json_data(file, data_key)
            return data
        except FileNotFoundError:
            # TODO add logger
            print(f'WARNING: {data_key} {snapshot} in {data_dir} not found.')
            return None
        except AssertionError:
            # TODO add logger
            print(f'WARNING: {data_key} {snapshot} have non-valid gaze point.')
            return None

    def read_snapshot(self, snapshot):
        return self.read_frames(snapshot), self.read_data(snapshot)

    def snapshots_iterate(self, indices):
        """
        Dataset generator
        :param indices: indices of snapshots, according to BRS
        :return: yield tuple(frame, face_points, faces_rotations)
        """
        for snapshot in [self.snapshots[i] for i in indices]:
            snapshot_data = self.read_snapshot(snapshot)
            if all(snapshot_data):
                yield snapshot_data
            else:
                pass
