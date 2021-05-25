#!/usr/bin/env python2

from geometry_msgs.msg import Pose, Twist, PoseWithCovariance, PointStamped
import rospy


class Republisher():

	def twist_callback(self, data):
		self.twist = data

	def pose_callback(self, data):
		self.current_pose = data


	def __init__(self):
		
		self.twist = Twist()
		self.cmd_pose = Pose()
		self.current_pose = PointStamped()
		
		rospy.Subscriber('/cmd_vel', Twist, self.twist_callback)
		rospy.Subscriber('/uav/position', PointStamped, self.pose_callback)
		
		self.pub = rospy.Publisher('/uav/pose_ref', Pose, queue_size = 1)
		
		self.hz = 2
		self.rate = rospy.Rate(self.hz)


	def republish(self):
		while not rospy.is_shutdown():

			self.lin_x = self.twist.linear.x
			self.lin_y = self.twist.linear.y
			self.lin_z = self.twist.linear.z

			self.x_inc = self.lin_x / self.hz
			self.y_inc = self.lin_y / self.hz
			self.z_inc = self.lin_z / self.hz

			self.cmd_pose.position.x = self.current_pose.point.x + self.x_inc
			self.cmd_pose.position.y = self.current_pose.point.y + self.y_inc
			self.cmd_pose.position.z = self.current_pose.point.z + self.z_inc
			#self.cmd_pose.position.z = 1

			#print("//////////")
			#print(self.current_pose)
			#print(self.cmd_pose)
			self.pub.publish(self.cmd_pose)

		
		
				
if __name__ == '__main__':
	rospy.init_node('joy_pose_republisher', anonymous = True)
	try:
		rp = Republisher()
		rp.republish()
	except rospy.ROSInterruptException:pass
	
