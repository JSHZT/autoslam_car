;; Auto-generated. Do not edit!


(when (boundp 'obrobot_navigation::PoseManage)
  (if (not (find-package "OBROBOT_NAVIGATION"))
    (make-package "OBROBOT_NAVIGATION"))
  (shadow 'PoseManage (find-package "OBROBOT_NAVIGATION")))
(unless (find-package "OBROBOT_NAVIGATION::POSEMANAGE")
  (make-package "OBROBOT_NAVIGATION::POSEMANAGE"))
(unless (find-package "OBROBOT_NAVIGATION::POSEMANAGEREQUEST")
  (make-package "OBROBOT_NAVIGATION::POSEMANAGEREQUEST"))
(unless (find-package "OBROBOT_NAVIGATION::POSEMANAGERESPONSE")
  (make-package "OBROBOT_NAVIGATION::POSEMANAGERESPONSE"))

(in-package "ROS")





(defclass obrobot_navigation::PoseManageRequest
  :super ros::object
  :slots (_poseoperation ))

(defmethod obrobot_navigation::PoseManageRequest
  (:init
   (&key
    ((:poseoperation __poseoperation) (instance obrobot_navigation::PoseOperation :init))
    )
   (send-super :init)
   (setq _poseoperation __poseoperation)
   self)
  (:poseoperation
   (&rest __poseoperation)
   (if (keywordp (car __poseoperation))
       (send* _poseoperation __poseoperation)
     (progn
       (if __poseoperation (setq _poseoperation (car __poseoperation)))
       _poseoperation)))
  (:serialization-length
   ()
   (+
    ;; obrobot_navigation/PoseOperation _poseoperation
    (send _poseoperation :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; obrobot_navigation/PoseOperation _poseoperation
       (send _poseoperation :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; obrobot_navigation/PoseOperation _poseoperation
     (send _poseoperation :deserialize buf ptr-) (incf ptr- (send _poseoperation :serialization-length))
   ;;
   self)
  )

(defclass obrobot_navigation::PoseManageResponse
  :super ros::object
  :slots (_status _posedefine ))

(defmethod obrobot_navigation::PoseManageResponse
  (:init
   (&key
    ((:status __status) "")
    ((:posedefine __posedefine) (instance obrobot_navigation::PoseDefine :init))
    )
   (send-super :init)
   (setq _status (string __status))
   (setq _posedefine __posedefine)
   self)
  (:status
   (&optional __status)
   (if __status (setq _status __status)) _status)
  (:posedefine
   (&rest __posedefine)
   (if (keywordp (car __posedefine))
       (send* _posedefine __posedefine)
     (progn
       (if __posedefine (setq _posedefine (car __posedefine)))
       _posedefine)))
  (:serialization-length
   ()
   (+
    ;; string _status
    4 (length _status)
    ;; obrobot_navigation/PoseDefine _posedefine
    (send _posedefine :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _status
       (write-long (length _status) s) (princ _status s)
     ;; obrobot_navigation/PoseDefine _posedefine
       (send _posedefine :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _status
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _status (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; obrobot_navigation/PoseDefine _posedefine
     (send _posedefine :deserialize buf ptr-) (incf ptr- (send _posedefine :serialization-length))
   ;;
   self)
  )

(defclass obrobot_navigation::PoseManage
  :super ros::object
  :slots ())

(setf (get obrobot_navigation::PoseManage :md5sum-) "ced5f2372deedb2a41f03ed0ae9a8337")
(setf (get obrobot_navigation::PoseManage :datatype-) "obrobot_navigation/PoseManage")
(setf (get obrobot_navigation::PoseManage :request) obrobot_navigation::PoseManageRequest)
(setf (get obrobot_navigation::PoseManage :response) obrobot_navigation::PoseManageResponse)

(defmethod obrobot_navigation::PoseManageRequest
  (:response () (instance obrobot_navigation::PoseManageResponse :init)))

(setf (get obrobot_navigation::PoseManageRequest :md5sum-) "ced5f2372deedb2a41f03ed0ae9a8337")
(setf (get obrobot_navigation::PoseManageRequest :datatype-) "obrobot_navigation/PoseManageRequest")
(setf (get obrobot_navigation::PoseManageRequest :definition-)
      "obrobot_navigation/PoseOperation poseoperation

================================================================================
MSG: obrobot_navigation/PoseOperation
string opt
uint32 id
string name
string type
uint32 floor
---
string status
obrobot_navigation/PoseDefine posedefine


================================================================================
MSG: obrobot_navigation/PoseDefine
uint32 id
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

(setf (get obrobot_navigation::PoseManageResponse :md5sum-) "ced5f2372deedb2a41f03ed0ae9a8337")
(setf (get obrobot_navigation::PoseManageResponse :datatype-) "obrobot_navigation/PoseManageResponse")
(setf (get obrobot_navigation::PoseManageResponse :definition-)
      "obrobot_navigation/PoseOperation poseoperation

================================================================================
MSG: obrobot_navigation/PoseOperation
string opt
uint32 id
string name
string type
uint32 floor
---
string status
obrobot_navigation/PoseDefine posedefine


================================================================================
MSG: obrobot_navigation/PoseDefine
uint32 id
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



(provide :obrobot_navigation/PoseManage "ced5f2372deedb2a41f03ed0ae9a8337")


