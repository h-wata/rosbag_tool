#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import numpy as np
import rosbag
import os
import sys
import matplotlib.pyplot as plt

args = sys.argv
print(args)
filename = os.path.normpath(os.path.join(os.getcwd(), args[1]))
print(filename)
# init

# rosbag open
bag = rosbag.Bag(filename)

dataset = None
np_pose_twist = np.array([[0.0, 0.0, 0.0, 0.0]])
# rosbagから/robot_pose, /odom/twist/linear/xを取る
for topic, msg, t in bag.read_messages():
    if topic == "/cuboid/diff_drive_controller/odom":
        np_pose_twist[0, 2] = msg.twist.twist.linear.x
        np_pose_twist[0, 3] = msg.twist.twist.angular.z
    if topic == "/amcl_pose":
        np_pose_twist[0, 0] = msg.pose.pose.position.x
        np_pose_twist[0, 1] = msg.pose.pose.position.y
    # robot_poseの方が寄さそうだけど、取り忘れた
    # if topic == "/robot_pose":
    #     np_pose_twist[0, 0] = msg.pose.position.x
    #     np_pose_twist[0, 1] = msg.pose.position.y
        # poseが更新されたら、heatmapにpose,twistを格納
        if dataset is None:
            dataset = np_pose_twist
        else:
            dataset = np.append(dataset, np_pose_twist, axis=0)

# csv形式で保存
np.savetxt('./text.csv', dataset, delimiter=',', fmt='%.5f')
# 散布図の描画
plt.figure()
plt.scatter(dataset[:, 0], dataset[:, 1], s=5, c=dataset[:, 3], cmap='jet')
plt.colorbar()
plt.show()
plt.savefig('./' + args[2] + '.png')
