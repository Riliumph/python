import abc


class Pose(abc.ABC):
    def apply_affine(self):
        raise NotImplementedError
