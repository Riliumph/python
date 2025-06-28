import numpy as np

from mathpy.pose import pose2d as p2d
from mathpy.pose import pose3d as p3d

p = np.array([40.0, 159.104004, 0.0])
o = np.array([1.0, 1.0, 1.0, 1.0])
affine = np.array([[4, 0, 0, 2], [0, -4, 0, 3], [0, 0, 1, 0], [0, 0, 0, 1]])
answer = np.array([3.0, 4.0, 0.0])

p = p3d.Pose3d(position=p, orientation=o)
p.apply_affine(affine4x4=affine)

print(p)
