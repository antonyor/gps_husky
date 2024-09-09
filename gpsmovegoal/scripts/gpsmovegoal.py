#!/usr/bin/env python3
import roslib
roslib.load_manifest('gpsmovegoal')
import rospy
from move_base_msgs.msg import MoveBaseActionGoal, MoveBaseAction
from move_base_msgs.msg import MoveBaseGoal
from sensor_msgs.msg import NavSatFix
import geonav_transform.geonav_conversions as gc
#reload(gc)
import alvinxy.alvinxy as axy
import subprocess
import actionlib

from geometry_msgs.msg import PoseStamped

#reload(axy)
def get_xy_based_on_lat_long(lat,lon):
    # Define a local orgin, latitude and longitude in decimal degrees
    # GPS Origin
    olat = 49.9
    olon = 8.9

    xg2, yg2 = gc.ll2xy(lat,lon,olat,olon)
    utmy, utmx, utmzone = gc.LLtoUTM(lat,lon)
    xa,ya = axy.ll2xy(lat,lon,olat,olon)
    
    return xg2, yg2


if __name__ == '__main__':
    #pub = rospy.Publisher('/move_base/goal', MoveBaseActionGoal, queue_size=10)
    rospy.init_node("gpsmovegoal",anonymous=True)
    msg = rospy.wait_for_message("/gps/fix", NavSatFix, timeout=None)
    print(msg.latitude,msg.longitude)

    #pub = rospy.Publisher('/move_base/goal', MoveBaseActionGoal, queue_size=1,latch=True)

    x,y=get_xy_based_on_lat_long(msg.latitude,msg.longitude)

    print(x,y)
    
    client=actionlib.SimpleActionClient("move_base",MoveBaseAction)
    client.wait_for_server()
    #print('client working')    
    #goal=MoveBaseGoal()
    #goal.target_pose.header.frame_id = "map"
    #goal.target_pose.header.stamp = rospy.Time.now()
    #goal.target_pose.pose.position.x=x
    #goal.target_pose.pose.position.y=y
    #print('msg working')

    #pubmsg=MoveBaseActionGoal()
    goal=MoveBaseGoal()
    #pubmsg.header.seq=0
    #pubmsg.header.stamp=0
    #pubmsg.header.frame_id=''
    #pubmsg.goal_id.stamp=0
    #pubmsg.goal_id.id=''

    #pubmsg.goal.target_pose.header.seq=0
    #pubmsg.goal.target_pose.header.stamp=0
    goal.target_pose.header.frame_id='map'
    goal.target_pose.header.stamp=rospy.Time.now()
    goal.target_pose.pose.position.x=x
    goal.target_pose.pose.position.y=y
    goal.target_pose.pose.position.z=0.0
    goal.target_pose.pose.orientation.x=0.0
    goal.target_pose.pose.orientation.y=0.0
    goal.target_pose.pose.orientation.z=0.0
    goal.target_pose.pose.orientation.w=1.0
    #pubmsg.goal.target_pose.pose.position.z=0
    #pubmsg.goal.target_pose.pose.orientation.x=0
    #pubmsg.goal.target_pose.pose.orientation.y=0
    #pubmsg.goal.target_pose.pose.orientation.z=0.75
    #pubmsg.goal.target_pose.pose.orientation.w=0.66
    client.send_goal(goal)
    client.wait_for_result()
    #if not wait:
    #    rospy.logerr("Action server not available!")
    #    rospy.signal_shutdown("Action server not available!")
    #else:
    #    print("success")
    
    #rate = rospy.Rate(0.5)
    #while not rospy.is_shutdown():
    #pub.publish(pubmsg)
        #rate.sleep()
    #rospy.spin()
    

