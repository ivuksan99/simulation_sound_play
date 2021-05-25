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
		self.pose = data
		
	def twist_callback(self, data):
		self.vel = data

	def __init__(self):
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
		self.count = 0

		


	def play_sound(self):
		self.sound.sound = -3
		self.sound.command = 2
		self.sound.volume = 1.0 
		self.sound.arg2 = 'voice_kal_diphone'

		
		self.diff_x, self.vel_x = 0, 0
		self.diff_y, self.vel_y = 0, 0 
		self.diff_z, self.vel_z = 0, 0

		self.check_dir()
		
		
		if(self.bool_x == True):
			if(self.diff_x > 0):
				self.sound.arg = 'going right'
			else:
				self.sound.arg = 'going left'
		elif(self.bool_y == True):
			if(self.diff_y > 0):
				self.sound.arg = 'going forward'
			else:
				self.sound.arg = 'going backwards'
		elif(self.bool_z == True):
			if(self.diff_z > 0):
				self.sound.arg = 'going up'
			else:
				self.sound.arg = 'going down'
		else:
			self.sound.arg = 'beep'

		

		if(self.bool_x == True):
			if(self.vel_x > 0):
				self.sound.arg = 'going right'
			else:
				self.sound.arg = 'going left'
		elif(self.bool_y == True):
			if(self.vel_y > 0):
				self.sound.arg = 'going forward'
			else:
				self.sound.arg = 'going backwards'
		elif(self.bool_z == True):
			if(self.vel_z > 0):
				self.sound.arg = 'going up'
			else:
				self.sound.arg = 'going down'
		else:
			self.sound.arg = 'beep'
		
		

		
				
			

		self.pub_sound.publish(self.sound)
		

	def generate_reference(self, dir_x, dir_y, dir_z):
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
		if(self.control_mode == 1):
			self.diff_x = self.pose_now.position.x - self.pose_prev.position.x 
			self.diff_y = self.pose_now.position.y - self.pose_prev.position.y 
			self.diff_z = self.pose_now.position.z - self.pose_prev.position.z 
			
			self.abs_x = abs(self.diff_x)
			self.abs_y = abs(self.diff_y)
			self.abs_z = abs(self.diff_z)
			
		
			if (self.abs_x > self.abs_y and self.abs_x > self.abs_z):
				self.bool_x = True
				self.bool_y = False
				self.bool_z = False
			elif (self.abs_y > self.diff_x and self.abs_y > self.abs_z):
				self.bool_x = False
				self.bool_y = True
				self.bool_z = False
			elif (self.abs_z > self.abs_y and self.abs_z > self.abs_x):
				self.bool_x = False
				self.bool_y = False
				self.bool_z = True

		elif(self.control_mode == -1):
			if self.pose.position.x % 0.125 == 0 or self.pose.position.y % 0.125 == 0 or self.pose.position.z % 0.125 == 0:
				
				if self.count % 4 == 0:

					self.vel_x = self.vel.twist.twist.linear.x
					self.vel_y = self.vel.twist.twist.linear.y
					self.vel_z = self.vel.twist.twist.linear.z
		
					self.vel_abs_x = abs(self.vel_x)
					self.vel_abs_y = abs(self.vel_y)
					self.vel_abs_z = abs(self.vel_z) - 0.2

					print("x:" + str(self.vel_x))
					print("y:" + str(self.vel_y))
					print("z:" + str(self.vel_z))

					if (self.vel_abs_x > self.vel_abs_y and self.vel_abs_x > self.vel_abs_z):
						self.bool_x = True
						self.bool_y = False
						self.bool_z = False
					elif (self.vel_abs_y > self.vel_abs_x and self.vel_abs_y > self.vel_abs_z):
						self.bool_x = False
						self.bool_y = True
						self.bool_z = False
					elif (self.vel_abs_z > self.vel_abs_y and self.vel_abs_z > self.vel_abs_x):
						self.bool_x = False
						self.bool_y = False
						self.bool_z = True
					else:
						self.bool_x = False
						self.bool_y = False
						self.bool_z = False
				self.count = self.count + 1
				
					
		

	def run(self):
		while not rospy.is_shutdown():
			if(self.control_mode == 1):
				self.generate_reference(0, 0, 1)
			
			elif(self.control_mode == -1):
				self.generate_reference(1 ,0, 0)
				
					
						
						
			
				
		

				
				
if __name__ == '__main__':
	rospy.init_node('generate_ref_sound', anonymous = True)
	time.sleep(5)
	try:
		mv = Move()
		mv.run()
	except rospy.ROSInterruptException:pass
	
