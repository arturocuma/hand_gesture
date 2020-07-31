#!/usr/bin/env python3.5
# coding: utf-8

# Copyright 2020 SoftBank Robotics Europe

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Project     : CROWDBOT
# Author      : Arturo Cruz Maya
# Departement : Software


import os
import sys

CV2_ROS = '/opt/ros/kinetic/lib/python2.7/dist-packages'
if CV2_ROS in sys.path:
    sys.path.remove(CV2_ROS)
    sys.path.append(CV2_ROS)

import rospy
import argparse

import tf
import geometry_msgs.msg
import time

from geometry_msgs.msg import PoseStamped


class tfHandGesture:
    """
    Class for transforming the frames of the hand, head and target
    to a local reference (odom) in order to perform the hand gesture
    """
    def __init__(self):
        """
        Constructor
        """
        publisher_gesture = rospy.init_node(
            "tf_hand_gesture",
            anonymous=True,
            disable_signals=False,
            log_level=rospy.INFO)

        self.pub_target = rospy.Publisher(
            "hand_gesture/target_local_position",
            PoseStamped,
            queue_size=1)

        self.pub_hand = rospy.Publisher(
            "hand_gesture/hand_local_position",
            PoseStamped,
            queue_size=1)

        self.pub_head = rospy.Publisher(
            "hand_gesture/head_local_position",
            PoseStamped,
            queue_size=1)

        self.listener1 = tf.TransformListener()

    def start(self):
        """
        Transform frames to local reference (odom)
        publish PoseStamped msgs of the head, hand and target
        """

        # Transform the target frame to local reference
        try:
            (target, _) = self.listener1.lookupTransform(
                "odom",
                "target_position",
                rospy.Time())

            # Publish the target_local_position
            target_local_position = PoseStamped()
            # target_local_position.header.frame_id = 'target_position'
            target_local_position.header.stamp = rospy.Time.now()
            target_local_position.pose.position.x = target[0]
            target_local_position.pose.position.y = target[1]
            target_local_position.pose.position.z = target[2]
            self.pub_target.publish(target_local_position)

        except(tf.LookupException,
               tf.ConnectivityException,
               tf.ExtrapolationException):
            pass

        # Transform the hand frame to local reference
        try:
            (hand, _) = self.listener1.lookupTransform(
                "odom",
                "r_gripper",
                rospy.Time())

            # Publish the hand_local_position
            hand_local_position = PoseStamped()
            # hand_local_position.header.frame_id = 'hand_local_position'
            hand_local_position.header.stamp = rospy.Time.now()

            hand_local_position.pose.position.x = hand[0]
            hand_local_position.pose.position.y = hand[1]
            hand_local_position.pose.position.z = hand[2]
            self.pub_hand.publish(hand_local_position)

        except (tf.LookupException,
                tf.ConnectivityException,
                tf.ExtrapolationException):
            pass

        # Transform the head frame to local reference
        try:
            (head, head_rot) = self.listener1.lookupTransform(
                "odom",
                "RealSense_frame",
                rospy.Time())

            # Publish the head_local_position
            head_local_position = PoseStamped()
            # head_local_position.header.frame_id = 'hand_local_position'
            head_local_position.header.stamp = rospy.Time.now()

            head_local_position.pose.position.x = head[0]
            head_local_position.pose.position.y = head[1]
            head_local_position.pose.position.z = head[2]
            head_local_position.pose.orientation.x = head_rot[0]
            head_local_position.pose.orientation.y = head_rot[1]
            head_local_position.pose.orientation.z = head_rot[2]
            head_local_position.pose.orientation.w = head_rot[3]
            self.pub_head.publish(head_local_position)

        except (tf.LookupException,
                tf.ConnectivityException,
                tf.ExtrapolationException):
            pass


if __name__ == '__main__':
    tfHandGesture = tfHandGesture()
    try:
        rate = rospy.Rate(30.0)
        while not rospy.is_shutdown():
            tfHandGesture.start()
            rate.sleep()
    except KeyboardInterrupt:
        pass
