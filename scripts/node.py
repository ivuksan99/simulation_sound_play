#!/usr/bin/env python2

import sys
import rospy
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
		self.zastavica = int(sys.argv[1])
		self.pub = rospy.Publisher('/uav/pose_ref', Pose, queue_size = 1)
		self.pub_sound = rospy.Publisher('/robotsound', SoundRequest, queue_size = 1)
		self.rate = rospy.Rate(1)
		self.point = Pose()
		self.sound = SoundRequest()
		self.bool = 1
		self.bool2 = 0

	def run(self):
		while not rospy.is_shutdown():
			if(self.zastavica == 1):
				if self.pose.position.x == 0:
					while self.pose.position.x < 10:
						self.point.position.z = 1
						self.point.position.x = self.pose.position.x + 0.5

						self.sound.sound = -3
						self.sound.command = 2
						self.sound.volume = 1.0 
						self.sound.arg = 'going right'
						self.sound.arg2 = 'voice_kal_diphone'
					
						self.pub_sound.publish(self.sound)
						self.pub.publish(self.point)
						self.rate.sleep()
				if self.pose.position.x == 10:	
					while self.pose.position.x > 0:
						self.point.position.z = 1
						self.point.position.x = self.pose.position.x - 0.5 
					
						self.sound.sound = -3
						self.sound.command = 2
						self.sound.volume = 1.0 
						self.sound.arg = 'going left'
						self.sound.arg2 = 'voice_kal_diphone'
					
						self.pub_sound.publish(self.sound)
						self.pub.publish(self.point)
						self.rate.sleep()
			else:
				while self.zastavica == -1:
					if(self.pose.position.x >= 0 and self.bool):
						self.point.position.z = 1
						self.point.position.x = self.pose.position.x + 0.5
						if(self.point.position.x == 10):
							self.bool = 0
							self.bool2 = 1
					elif(self.pose.position.x <= 10 and self.bool2):
						self.point.position.z = 1
						self.point.position.x = self.pose.position.x - 0.5
						if(self.point.position.x == 0):
							self.bool = 1
							self.bool2 = 0
						
					if(self.vel.twist.twist.linear.x > 0 and self.vel.twist.twist.linear.x <= 1 ):
						self.sound.sound = -3
						self.sound.command = 2
						self.sound.volume = 1.0 
						self.sound.arg = 'right'
						self.sound.arg2 = 'voice_kal_diphone'
						self.pub_sound.publish(self.sound)
					else:
						self.sound.sound = -3
						self.sound.command = 2
						self.sound.volume = 1.0 
						self.sound.arg = 'left'
						self.sound.arg2 = 'voice_kal_diphone'
						self.pub_sound.publish(self.sound)
					
					#self.pub_sound.publish(self.sound)
					self.pub.publish(self.point)
					self.rate.sleep()

				
				
if __name__ == '__main__':
	rospy.init_node('Node', anonymous = True)
	#s = 'going right'
	#voice = 'voice_kal_diphone'
    	#volume = 1.0
	try:
		mv = Move()
		mv.run()
		#soundhandle = SoundClient()
		#soundhandle.say(s, voice, volume)
	except rospy.ROSInterruptException:pass
	
