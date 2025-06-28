import numpy as np

from mathpy.pose import pose2d as p2d

p = np.array([1.0, 1.0, 1.0])
o = np.array([1.0, 1.0, 1.0, 1.0])
affine = np.array([[1, 0, 2], [0, 1, 3], [0, 0, 1]])
answer = np.array([3.0, 4.0, 0.0])

p = p2d.Pose2d(position=p, orientation=o)
p.apply_affine(affine3x3=affine)

print(p)
