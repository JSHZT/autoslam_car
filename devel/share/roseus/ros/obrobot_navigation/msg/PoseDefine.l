;; Auto-generated. Do not edit!


(when (boundp 'obrobot_navigation::PoseDefine)
  (if (not (find-package "OBROBOT_NAVIGATION"))
    (make-package "OBROBOT_NAVIGATION"))
  (shadow 'PoseDefine (find-package "OBROBOT_NAVIGATION")))
(unless (find-package "OBROBOT_NAVIGATION::POSEDEFINE")
  (make-package "OBROBOT_NAVIGATION::POSEDEFINE"))

(in-package "ROS")
;;//! \htmlinclude PoseDefine.msg.html
(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))


(defclass obrobot_navigation::PoseDefine
  :super ros::object
  :slots (_id _name _type _floor _pose ))

(defmethod obrobot_navigation::PoseDefine
  (:init
   (&key
    ((:id __id) 0)
    ((:name __name) "")
    ((:type __type) "")
    ((:floor __floor) 0)
    ((:pose __pose) (instance geometry_msgs::Pose :init))
    )
   (send-super :init)
   (setq _id (round __id))
   (setq _name (string __name))
   (setq _type (string __type))
   (setq _floor (round __floor))
   (setq _pose __pose)
   self)
  (:id
   (&optional __id)
   (if __id (setq _id __id)) _id)
  (:name
   (&optional __name)
   (if __name (setq _name __name)) _name)
  (:type
   (&optional __type)
   (if __type (setq _type __type)) _type)
  (:floor
   (&optional __floor)
   (if __floor (setq _floor __floor)) _floor)
  (:pose
   (&rest __pose)
   (if (keywordp (car __pose))
       (send* _pose __pose)
     (progn
       (if __pose (setq _pose (car __pose)))
       _pose)))
  (:serialization-length
   ()
   (+
    ;; uint32 _id
    4
    ;; string _name
    4 (length _name)
    ;; string _type
    4 (length _type)
    ;; uint32 _floor
    4
    ;; geometry_msgs/Pose _pose
    (send _pose :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint32 _id
       (write-long _id s)
     ;; string _name
       (write-long (length _name) s) (princ _name s)
     ;; string _type
       (write-long (length _type) s) (princ _type s)
     ;; uint32 _floor
       (write-long _floor s)
     ;; geometry_msgs/Pose _pose
       (send _pose :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint32 _id
     (setq _id (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; string _name
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _name (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; string _type
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _type (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; uint32 _floor
     (setq _floor (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; geometry_msgs/Pose _pose
     (send _pose :deserialize buf ptr-) (incf ptr- (send _pose :serialization-length))
   ;;
   self)
  )

(setf (get obrobot_navigation::PoseDefine :md5sum-) "4961e9ce48eeb076d10e966f73b4f21b")
(setf (get obrobot_navigation::PoseDefine :datatype-) "obrobot_navigation/PoseDefine")
(setf (get obrobot_navigation::PoseDefine :definition-)
      "uint32 id
string name
string type
uint32 floor
geometry_msgs/Pose pose

================================================================================
MSG: geometry_msgs/Pose
# A representation of pose in free space, composed of position and orientation. 
Point position
Quaternion orientation

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.

float64 x
float64 y
float64 z
float64 w

")



(provide :obrobot_navigation/PoseDefine "4961e9ce48eeb076d10e966f73b4f21b")


