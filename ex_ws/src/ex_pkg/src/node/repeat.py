#! /usr/bin/python3

from math import atan2, pow, sqrt
from sys import stderr
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist, Vector3

pub = rospy.Publisher('/turtle/repeat', Twist, queue_size=10)
cur_data = Pose()

def calculate_angle(cur_data, data):
    return atan2(data.y - cur_data.y, data.x - cur_data.x) - cur_data.theta

def calculate_speed(cur_data, data):
    return sqrt(pow(data.x - cur_data.x, 2) + pow(data.y - cur_data.y, 2))

def key_callback(data):
    twist = Twist()
    twist.linear.x = calculate_speed(cur_data, data)
    twist.angular.z = 10*calculate_angle(cur_data, data)
    pub.publish(twist)

def sync_callback(data):
    global cur_data
    cur_data = data

if __name__ == '__main__':
    rospy.init_node('transmitter')
    rospy.Subscriber('/turtle_key/pose', Pose, key_callback)
    rospy.Subscriber('/turtle_sync/pose', Pose, sync_callback)
    rospy.spin()
