#!/usr/bin/env python 
# Based on http://wiki.ros.org/tf2/Tutorials/Adding%20a%20frame%20%28Python%29
import rospy
import tf2_msgs.msg
import geometry_msgs.msg
from object_detector.msg import Detected_object
from object_detector_node import DetectedObject


class TFBroadcaster:
    def __init__(self):
        self.pub_tf = rospy.Publisher("/tf", tf2_msgs.msg.TFMessage, queue_size=1)
        self.sub_det_obj = rospy.Subscriber("/object_found", Detected_object, self.object_callback)
        self.detected_objects = []
        self.counter_of_detected_objects = 0
      
    def object_callback(self, msg):
        self.counter_of_detected_objects += 1
        self.detected_objects.append(DetectedObject(msg.name_id, 0, 0, 0, msg.x, msg.y, msg.z, msg.width, msg.height))
        print("Objects on the map: " + str(len(self.detected_objects)))

    def publish_tfs(self, event):
        for obj in self.detected_objects:
            t = geometry_msgs.msg.TransformStamped()
            t.header.frame_id = "map"
            t.header.stamp = rospy.Time.now()
            t.child_frame_id = "Object" + str(obj.name_id)
            t.transform.translation.x = obj.x
            t.transform.translation.y = obj.y
            t.transform.translation.z = obj.z

            t.transform.rotation.x = 0.0
            t.transform.rotation.y = 0.0
            t.transform.rotation.z = 0.0
            t.transform.rotation.w = 1.0

            tfm = tf2_msgs.msg.TFMessage([t])
            self.pub_tf.publish(tfm)


if __name__ == '__main__':
    rospy.init_node('tf2_broadcaster')
    tfb = TFBroadcaster()

    rospy.Timer(rospy.Duration(1), tfb.publish_tfs)
    rospy.loginfo("tf2_broadcaster node is up!")

    rospy.spin()
