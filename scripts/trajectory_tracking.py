#!/usr/bin/env python2

import rosbag
import rospy
from nav_msgs.msg import Path
from geometry_msgs.msg import Pose, Twist, PoseWithCovariance, PointStamped, Point
from math import sqrt, pow

class Trajectory_tracking():

	def pose_callback(self, data):
		self.pose = data
		

	def __init__(self):
		self.inbag_filename = "2021-05-09-09-49-56.bag"
		self.list = []
		self.next_pose = []
		self.path = Path()
		self.goal_pose = Point()
		
		self.read_rosbag()

		rospy.Subscriber('/uav/pose_ref', Pose, self.pose_callback)
		self.pose = Pose()
		self.rate = rospy.Rate(2)
		

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
		

	def run(self):
		while not rospy.is_shutdown():
			for x in self.next_pose:
				self.goal_pose = x
				while self.check_distance() > 0.3:
					print(self.goal_pose)
					

if __name__ == '__main__':
	rospy.init_node('trajectory_tracking', anonymous = True)
	try:
		tt = Trajectory_tracking()
		tt.run()
		
	except rospy.ROSInterruptException:pass
