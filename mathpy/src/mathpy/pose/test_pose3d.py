import numpy as np
import pytest

from mathpy.pose.pose3d import Pose3d


@pytest.mark.parametrize(
    "pos, ori, affine, answer",
    [
        (  # affine
            np.array([1.0, 1.0, 1.0]),
            np.array([1.0, 1.0, 1.0, 1.0]),
            np.array([[1, 0, 0, 2], [0, 1, 0, 3], [0, 0, 1, 0], [0, 0, 0, 1]]),
            np.array([3.0, 4.0, 0.0])
        )
    ]
)
def test_pose_apply_affine(pos, ori, affine, answer):
    p = Pose3d(pos, ori)
    p.apply_affine(affine4x4=affine)
    result = p.position
    np.testing.assert_allclose(result[:2], answer[:2], atol=1e-6)
