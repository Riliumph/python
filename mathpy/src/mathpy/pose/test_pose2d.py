import numpy as np
import pytest

from mathpy.pose.pose2d import Pose2d


@pytest.mark.parametrize(
    "pos, ori, affine, answer",
    [
        (  # affine
            np.array([1.0, 1.0, 1.0]),
            np.array([1.0, 1.0, 1.0, 1.0]),
            np.array([[1, 0, 2], [0, 1, 3], [0, 0, 1]]),
            np.array([3.0, 4.0, 0.0])
        )
    ]
)
def test_pose_apply_affine(pos, ori, affine, answer):
    p = Pose2d(pos, ori)
    p.apply_affine(affine3x3=affine)
    result = p.position
    np.testing.assert_allclose(result[:2], answer[:2], atol=1e-6)
