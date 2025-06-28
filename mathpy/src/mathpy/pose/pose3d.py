import numpy as np
from scipy.spatial.transform import Rotation as R

from mathpy.pose.pose import Pose


class Pose3d(Pose):
    def __init__(self, position: np.ndarray, orientation: np.ndarray):
        pos3x1 = np.asarray(position, dtype=float)
        ori4x1 = np.asarray(orientation, dtype=float)
        if pos3x1.shape != (3,):
            # x,y,z
            p_shape = pos3x1.shape
            raise ValueError(f"position must be shape (3,), but got {p_shape}")
        if ori4x1.shape != (4,):
            # x,y,z,w
            o_shape = ori4x1.shape
            raise ValueError(
                f"orientation must be shape(4,), but got {o_shape}")
        norm = np.linalg.norm(ori4x1)
        if norm == 0:
            msg = "orientation quaternion norm is zero, invalid rotation"
            raise ValueError(msg)
        ori4x1 = ori4x1 / norm
        # 値を格納
        self._pos = pos3x1
        self._ori = ori4x1

    @property
    def position(self) -> np.ndarray:
        return self._pos

    @property
    def orientation(self) -> np.ndarray:
        return self._ori

    def apply_affine(self, affine4x4: np.ndarray):
        if affine4x4.shape != (3, 3):
            raise ValueError("affine matrix must be (4,4)")
        # 座標変換
        homo4x1 = np.append(self._pos, 1.0)
        pos4x1 = affine4x4 @ homo4x1
        self._pos = pos4x1[:3]
        # 角度変換
        rot3x3 = affine4x4[:3, :3]
        affine_rot = R.from_matrix(rot3x3)
        current_rot = R.from_quat(self._ori)
        new_rot = affine_rot * current_rot
        self._ori = new_rot.as_quat()

    def __repr__(self):
        p = self.position.tolist()
        o = self.orientation.tolist()
        return f"Pose2d(p=[{p}], o=[{o}])"
