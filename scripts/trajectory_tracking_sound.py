#!/usr/bin/env python2

import time
import rosbag
import rospy
from nav_msgs.msg import Path
from geometry_msgs.msg import Pose, Twist, PoseWithCovariance, PointStamped, Point
from math import sqrt, pow
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient
import math

class Trajectory_tracking():

	def pose_callback(self, data):
		self.pose = data
		

	def __init__(self):
		self.inbag_filename = "2021-05-23-19-47-32.bag"
		self.next_pose = []
		self.path = Path()
		self.goal_pose = Point()
		
		self.read_rosbag()

		#print(self.next_pose)
		rospy.Subscriber('/uav/pose_ref', Pose, self.pose_callback)
		self.pub_sound = rospy.Publisher('/robotsound', SoundRequest, queue_size = 1)
		self.pose = Pose()
		self.sound = SoundRequest()
		self.rate = rospy.Rate(0.5)
		

	def read_rosbag(self):
		for (topic, msg, t) in rosbag.Bag(self.inbag_filename, 'r').read_messages():
			if(topic == '/path'):
				self.count = 0
				for x in msg.poses:
					if(self.count % 6 == 0):
						self.next_pose.append(x.pose.position)
					elif(self.count == len(msg.poses) - 1):
						self.next_pose.append(x.pose.position)
					self.count = self.count + 1
		
	
	def check_distance(self):
		self.distance = sqrt(pow(self.pose.position.x - self.goal_pose.x, 2) + pow(self.pose.position.y - self.goal_pose.y, 2) + pow(self.pose.position.z - self.goal_pose.z, 2))
		#print(self.distance)
		return self.distance

	def check_dir(self):
		self.diff_x = self.goal_pose.x - self.pose.position.x
		self.diff_y = self.goal_pose.y - self.pose.position.y
		self.diff_z = self.goal_pose.z - self.pose.position.z

		self.abs_x = abs(self.diff_x)
		self.abs_y = abs(self.diff_y)
		self.abs_z = abs(self.diff_z)

		#print("x:" + str(self.abs_x))
		#print("y:" + str(self.abs_y))
		#print("z:" + str(self.abs_z))

		if (self.abs_x > self.abs_y and self.abs_x > self.abs_z):
			self.bool_x = True
			self.bool_y = False
			self.bool_z = False
		elif (self.abs_y > self.abs_x and self.abs_y > self.abs_z):
			self.bool_x = False
			self.bool_y = True
			self.bool_z = False
		elif (self.abs_z > self.abs_y and self.abs_z > self.abs_x):
			self.bool_x = False
			self.bool_y = False
			self.bool_z = True
		else:
			self.bool_x = False
			self.bool_y = False
			self.bool_z = False
		

	def play_sound(self):
		self.sound.sound = -3
		self.sound.command = 2
		self.sound.volume = 1.0 
		self.sound.arg2 = 'voice_kal_diphone'
		
		self.check_dir()

		if(self.bool_x == True):
			if(self.diff_x > 0):
				self.sound.arg = 'go right'
			else:
				self.sound.arg = 'go left'
		elif(self.bool_y == True):
			if(self.diff_y > 0):
				self.sound.arg = 'go forward'
			else:
				self.sound.arg = 'go backwards'
		elif(self.bool_z == True):
			if(self.diff_z > 0):
				self.sound.arg = 'go up'
			else:
				self.sound.arg = 'go down'
		else:
			self.sound.arg = 'beep'

		rospy.loginfo("Sound feedback: {}".format(str(self.sound.arg).upper()))
		
		self.pub_sound.publish(self.sound)
		

	def run(self):
		while not rospy.is_shutdown():
			for x in self.next_pose:
				self.goal_pose = x
				print(x)
				while self.check_distance() > 2:
					#print(self.goal_pose)
					self.play_sound()
					self.rate.sleep()
					

if __name__ == '__main__':
	rospy.init_node('trajectory_tracking_sound', anonymous = True)
	time.sleep(5)
	try:
		tt = Trajectory_tracking()
		tt.run()
		
	except rospy.ROSInterruptException:pass
