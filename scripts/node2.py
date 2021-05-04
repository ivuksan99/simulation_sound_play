#!/usr/bin/env python2

import time
import sys
import rospy
import numpy as np
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient
from nav_msgs.msg import Odometry



class Move():
	def pose_callback(self, data):
		"""
		TODO: Add docstring 
		"""
		
		self.pose = data
		
	def twist_callback(self, data):
		"""
		TODO: Add docstring
		"""
		self.vel = Odometry()
		self.vel_x = 
		self.vel = data
	

	def __init__(self):
		"""
		TIDI; Group messages and subscribers, rest of the variables 
		"""
		self.pose = Pose()
		rospy.Subscriber('/uav/pose_ref', Pose, self.pose_callback)
		rospy.Subscriber('/uav/odometry', Odometry, self.twist_callback)
		self.vel = Odometry()
		self.control_mode = -1
		self.pub = rospy.Publisher('/uav/pose_ref', Pose, queue_size = 1)
		self.pub_sound = rospy.Publisher('/robotsound', SoundRequest, queue_size = 1)
		self.rate = rospy.Rate(1)
		self.point = Pose()
		self.sound = SoundRequest()
		self.point.position.z = 1
		self.pose_now = Pose()
		self.pose_prev = Pose()		


	def play_sound(self):
		"""
		TODO: add docstring 
		What this method does? 
		Plays sound depending on current UAV direction, also, calls check_direction method
		pyCharm has good docstrings e.g., https://www.jetbrains.com/help/pycharm/using-docstrings-to-specify-types.html#param-type-specification
		"""
		self.sound.sound = -3
		self.sound.command = 2
		self.sound.volume = 1.0 
		self.sound.arg2 = 'voice_kal_diphone'

		# flags for getting differnce in position coordinates and setting up current velocity
		self.diff_x, self.vel_x = 0, 0
		self.diff_y, self.vel_y = 0, 0 
		self.diff_z, self.vel_z = 0, 0
		
		# Check current UAV direction based on current(t) odometry reading and (t-1) odometry reading
		self.check_dir()
		
		# bool_x, bool_y, bool_z = find some descriptive names
		# Decoupled direction control (Controlling only one axes) 
		if(self.bool_x == True):
			# self.vel_x is not clear enough, do you read that value, or do you set it as reference? 
			# if we use vel_x as odom callback, than you should
			if(self.diff_x > 0 or self.vel_x >= 0.1):
				self.vel_x = self.vel_x - 0.1
				self.sound.arg = 'going right'
			else:
				self.sound.arg = 'going left'
		elif(self.bool_y == True):
			if(self.diff_y > 0 or self.vel_y >= 0.1):
				self.vel_y = self.vel_y - 0.1
				self.sound.arg = 'going forward'
			else:
				self.sound.arg = 'going backwards'
		elif(self.bool_z == True):
			if(self.diff_z > 0 or self.vel_z >= 0.1):
				self.vel_z = self.vel_z - 0.1
				self.sound.arg = 'going up'
			else:
				self.sound.arg = 'going down'
		else:
			self.sound.arg = 'beep'		

		self.pub_sound.publish(self.sound)
		

	def generate_reference(self, dir_x, dir_y, dir_z):
		""" TODO: Add docstring."""
		if(dir_x == 1):
			if self.pose.position.x == 0:
				while self.pose.position.x < 10:
					self.pose_prev.position.x = self.point.position.x
					self.point.position.x = self.pose.position.x + 0.5
					self.pose_now.position.x = self.point.position.x
					self.play_sound()
					self.pub.publish(self.point)
					self.rate.sleep()
			if self.pose.position.x == 10:
				while self.pose.position.x > 0:
					self.pose_prev.position.x = self.point.position.x
					self.point.position.x = self.pose.position.x - 0.5
					self.pose_now.position.x = self.point.position.x
					self.play_sound()
					self.pub.publish(self.point)
					self.rate.sleep()
		elif(dir_y == 1):
			if self.pose.position.y == 0:
				while self.pose.position.y < 10:
					self.pose_prev.position.y = self.point.position.y
					self.point.position.y = self.pose.position.y + 0.5
					self.pose_now.position.y = self.point.position.y
					self.play_sound()
					self.pub.publish(self.point)
					self.rate.sleep()
			if self.pose.position.y == 10:
				while self.pose.position.y > 0:
					self.pose_prev.position.y = self.point.position.y
					self.point.position.y = self.pose.position.y - 0.5
					self.pose_now.position.y = self.point.position.y 
					self.play_sound()
					self.pub.publish(self.point)
					self.rate.sleep()
		elif(dir_z == 1):
			if self.pose.position.z == 0:
				while self.pose.position.z < 10:
					self.pose_prev.position.z = self.point.position.z
					self.point.position.z = self.pose.position.z + 0.25
					self.pose_now.position.z = self.point.position.z
					self.play_sound()
					self.pub.publish(self.point)
					self.rate.sleep()
			if self.pose.position.z == 10:
				while self.pose.position.z > 0:
					self.pose_prev.position.z = self.point.position.z
					self.point.position.z = self.pose.position.z - 0.25 
					self.pose_now.position.z = self.point.position.z
					self.play_sound()
					self.pub.publish(self.point)
					self.rate.sleep()



	def check_dir(self):
		"""TODO: Add docstring
		"""
		# self.control_mode ? position_control 1, velocity control --> -1, maybe set different flags, self.position_control = true 
		# self.velocity control = false or describe somewhere which are available
		if(self.control_mode == 1):
			# Bear in mind that you should always check absolute differences, to maintain consistency between coordinates
			# Y_change = -0.6, X_change = 0.4 --> 0.4 > -0.6 -->̣ X_change > Y_change != correct ==> abs(Y_change) > abs(X_change) == correct 
			# -0.5 - 0.1 = -0.6 0.5 - 0.1 = 0.4 
			self.diff_x = abs(self.pose_now.position.x - self.pose_prev.position.x) 
			self.diff_y = abs(self.pose_now.position.y - self.pose_prev.position.y) 
			self.diff_z = abs(self.pose_now.position.z - self.pose_prev.position.z)  
		
			# Abs condition solves or comparisons as we can compare relative changes 
			if (self.diff_x > self.diff_y and self.diff_x > self.diff_z): # or (self.diff_x < self.diff_y and self.diff_x < self.diff_z):
				self.bool_x = True
				self.bool_y = False
				self.bool_z = False
			elif (self.diff_y > self.diff_x and self.diff_y > self.diff_z): # or (self.diff_y < self.diff_x and self.diff_y < self.diff_z):
				self.bool_x = False
				self.bool_y = True
				self.bool_z = False
			elif (self.diff_z > self.diff_y and self.diff_z > self.diff_x): # or (self.diff_z < self.diff_y and self.diff_z < self.diff_x):
				self.bool_x = False
				self.bool_y = False
				self.bool_z = True
		
		# Velocity control 
		elif(self.control_mode == -1):			
			
			# current speeds 
			self.vel_x = round(self.vel.twist.twist.linear.x)
			self.vel_y = round(self.vel.twist.twist.linear.y)
			self.vel_z = round(self.vel.twist.twist.linear.z)
			# Not getting this part, if velocity positive and in range [0-2> (moving right) or if velocity negative and in range [-2, 0> 
			if ((self.vel_x >= 0 and self.vel_x < 2) or (self.vel_x <= 0 and self.vel_x > -2)):
				# Bool x = True, and increase velocity 
				# Think about it a little more, whichever speed we have, we will increase in following conditions 
				# You're editing current speed, not recommended, you can create self.vel_x_ref = self.vel_x + 0.1  
				self.vel_x = self.vel_x + 0.1
				self.bool_x = True
				self.bool_y = False
				self.bool_z = False
			elif ((self.vel_y >= 0 and self.vel_z < 2) or (self.vel_y <= 0 and self.vel_y > -2)):
				self.vel_y = self.vel_y + 0.1
				self.bool_x = False
				self.bool_y = True
				self.bool_z = False
			elif ((self.vel_z >= 0 and self.vel_z < 1) or (self.vel_z <= 0 and self.vel_z > -1)):
				self.vel_z = self.vel_z + 0.1
				self.bool_x = False
				self.bool_y = False
				self.bool_z = True
			else:
				self.bool_x = False
				self.bool_y = False
				self.bool_z = False

					
		

	def run(self):
		while not rospy.is_shutdown():
			if(self.control_mode == 1):
				self.generate_reference(0, 1, 0)
			elif(self.control_mode == -1):
				self.generate_reference(0 ,1, 0)
					
						
						
			
				
		

				
				
if __name__ == '__main__':
	rospy.init_node('node2', anonymous = True)
	time.sleep(5)
	try:
		mv = Move()
		mv.run()
	except rospy.ROSInterruptException:pass
	
