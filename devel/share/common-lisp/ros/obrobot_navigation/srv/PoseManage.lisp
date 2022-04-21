; Auto-generated. Do not edit!


(cl:in-package obrobot_navigation-srv)


;//! \htmlinclude PoseManage-request.msg.html

(cl:defclass <PoseManage-request> (roslisp-msg-protocol:ros-message)
  ((poseoperation
    :reader poseoperation
    :initarg :poseoperation
    :type obrobot_navigation-msg:PoseOperation
    :initform (cl:make-instance 'obrobot_navigation-msg:PoseOperation)))
)

(cl:defclass PoseManage-request (<PoseManage-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <PoseManage-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'PoseManage-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name obrobot_navigation-srv:<PoseManage-request> is deprecated: use obrobot_navigation-srv:PoseManage-request instead.")))

(cl:ensure-generic-function 'poseoperation-val :lambda-list '(m))
(cl:defmethod poseoperation-val ((m <PoseManage-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader obrobot_navigation-srv:poseoperation-val is deprecated.  Use obrobot_navigation-srv:poseoperation instead.")
  (poseoperation m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <PoseManage-request>) ostream)
  "Serializes a message object of type '<PoseManage-request>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'poseoperation) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <PoseManage-request>) istream)
  "Deserializes a message object of type '<PoseManage-request>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'poseoperation) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<PoseManage-request>)))
  "Returns string type for a service object of type '<PoseManage-request>"
  "obrobot_navigation/PoseManageRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'PoseManage-request)))
  "Returns string type for a service object of type 'PoseManage-request"
  "obrobot_navigation/PoseManageRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<PoseManage-request>)))
  "Returns md5sum for a message object of type '<PoseManage-request>"
  "ced5f2372deedb2a41f03ed0ae9a8337")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'PoseManage-request)))
  "Returns md5sum for a message object of type 'PoseManage-request"
  "ced5f2372deedb2a41f03ed0ae9a8337")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<PoseManage-request>)))
  "Returns full string definition for message of type '<PoseManage-request>"
  (cl:format cl:nil "obrobot_navigation/PoseOperation poseoperation~%~%================================================================================~%MSG: obrobot_navigation/PoseOperation~%string opt~%uint32 id~%string name~%string type~%uint32 floor~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'PoseManage-request)))
  "Returns full string definition for message of type 'PoseManage-request"
  (cl:format cl:nil "obrobot_navigation/PoseOperation poseoperation~%~%================================================================================~%MSG: obrobot_navigation/PoseOperation~%string opt~%uint32 id~%string name~%string type~%uint32 floor~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <PoseManage-request>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'poseoperation))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <PoseManage-request>))
  "Converts a ROS message object to a list"
  (cl:list 'PoseManage-request
    (cl:cons ':poseoperation (poseoperation msg))
))
;//! \htmlinclude PoseManage-response.msg.html

(cl:defclass <PoseManage-response> (roslisp-msg-protocol:ros-message)
  ((status
    :reader status
    :initarg :status
    :type cl:string
    :initform "")
   (posedefine
    :reader posedefine
    :initarg :posedefine
    :type obrobot_navigation-msg:PoseDefine
    :initform (cl:make-instance 'obrobot_navigation-msg:PoseDefine)))
)

(cl:defclass PoseManage-response (<PoseManage-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <PoseManage-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'PoseManage-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name obrobot_navigation-srv:<PoseManage-response> is deprecated: use obrobot_navigation-srv:PoseManage-response instead.")))

(cl:ensure-generic-function 'status-val :lambda-list '(m))
(cl:defmethod status-val ((m <PoseManage-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader obrobot_navigation-srv:status-val is deprecated.  Use obrobot_navigation-srv:status instead.")
  (status m))

(cl:ensure-generic-function 'posedefine-val :lambda-list '(m))
(cl:defmethod posedefine-val ((m <PoseManage-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader obrobot_navigation-srv:posedefine-val is deprecated.  Use obrobot_navigation-srv:posedefine instead.")
  (posedefine m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <PoseManage-response>) ostream)
  "Serializes a message object of type '<PoseManage-response>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'status))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'status))
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'posedefine) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <PoseManage-response>) istream)
  "Deserializes a message object of type '<PoseManage-response>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'status) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'status) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'posedefine) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<PoseManage-response>)))
  "Returns string type for a service object of type '<PoseManage-response>"
  "obrobot_navigation/PoseManageResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'PoseManage-response)))
  "Returns string type for a service object of type 'PoseManage-response"
  "obrobot_navigation/PoseManageResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<PoseManage-response>)))
  "Returns md5sum for a message object of type '<PoseManage-response>"
  "ced5f2372deedb2a41f03ed0ae9a8337")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'PoseManage-response)))
  "Returns md5sum for a message object of type 'PoseManage-response"
  "ced5f2372deedb2a41f03ed0ae9a8337")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<PoseManage-response>)))
  "Returns full string definition for message of type '<PoseManage-response>"
  (cl:format cl:nil "string status~%obrobot_navigation/PoseDefine posedefine~%~%~%================================================================================~%MSG: obrobot_navigation/PoseDefine~%uint32 id~%string name~%string type~%uint32 floor~%geometry_msgs/Pose pose~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'PoseManage-response)))
  "Returns full string definition for message of type 'PoseManage-response"
  (cl:format cl:nil "string status~%obrobot_navigation/PoseDefine posedefine~%~%~%================================================================================~%MSG: obrobot_navigation/PoseDefine~%uint32 id~%string name~%string type~%uint32 floor~%geometry_msgs/Pose pose~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <PoseManage-response>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'status))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'posedefine))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <PoseManage-response>))
  "Converts a ROS message object to a list"
  (cl:list 'PoseManage-response
    (cl:cons ':status (status msg))
    (cl:cons ':posedefine (posedefine msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'PoseManage)))
  'PoseManage-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'PoseManage)))
  'PoseManage-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'PoseManage)))
  "Returns string type for a service object of type '<PoseManage>"
  "obrobot_navigation/PoseManage")