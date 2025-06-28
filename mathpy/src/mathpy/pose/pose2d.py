import numpy as np
from scipy.spatial.transform import Rotation as R

from mathpy.pose.pose import Pose


class Pose2d(Pose):
    def __init__(self, position: np.ndarray, orientation: np.ndarray):
        pos3x1 = np.asarray(position, dtype=float)
        ori4x1 = np.asarray(orientation, dtype=float)
        if pos3x1.shape[0] < 2:
            p_shape = pos3x1.shape
            msg = f"position must have at least 2 elem, got {p_shape}"
            raise ValueError(msg)
        if ori4x1.shape != (4,):
            o_shape = ori4x1.shape
            msg = f"orientaion must be quaternion (4,), got {o_shape}"
            raise ValueError(msg)
        # クォータニオン正規化
        norm = np.linalg.norm(ori4x1)
        if norm == 0:
            msg = "orientation quaternion norm is zero, invalid rotation"
            raise ValueError(msg)
        ori4x1 = ori4x1 / norm
        # 値を格納
        self._pos = np.array([pos3x1[0], pos3x1[1], 0.0])
        self._ori = ori4x1

    @property
    def position(self) -> np.ndarray:
        return self._pos

    @property
    def orientation(self) -> np.ndarray:
        return self._ori

    def apply_affine(self, affine3x3: np.ndarray):
        if affine3x3.shape != (3, 3):
            raise ValueError("affine matrix must be (3,3)")
        # 座標変換
        homo3x1 = np.append(self._pos[:2], 1.0)
        pos3x1 = affine3x3 @ homo3x1
        self._pos[:2] = pos3x1[:2]
        # 角度変換
        rot2x2 = affine3x3[:2, :2]
        angle = np.arctan2(rot2x2[1, 0], rot2x2[0, 0])
        quat4x1 = R.from_euler('z', angle).as_quat()
        self._ori = quat4x1

    def __repr__(self):
        p = self._pos.tolist()
        o = self._ori.tolist()
        return f"Pose2d(p=[{p}], o=[{o}])"
