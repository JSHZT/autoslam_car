; Auto-generated. Do not edit!


(cl:in-package obrobot_navigation-msg)


;//! \htmlinclude PoseOperation.msg.html

(cl:defclass <PoseOperation> (roslisp-msg-protocol:ros-message)
  ((opt
    :reader opt
    :initarg :opt
    :type cl:string
    :initform "")
   (id
    :reader id
    :initarg :id
    :type cl:integer
    :initform 0)
   (name
    :reader name
    :initarg :name
    :type cl:string
    :initform "")
   (type
    :reader type
    :initarg :type
    :type cl:string
    :initform "")
   (floor
    :reader floor
    :initarg :floor
    :type cl:integer
    :initform 0))
)

(cl:defclass PoseOperation (<PoseOperation>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <PoseOperation>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'PoseOperation)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name obrobot_navigation-msg:<PoseOperation> is deprecated: use obrobot_navigation-msg:PoseOperation instead.")))

(cl:ensure-generic-function 'opt-val :lambda-list '(m))
(cl:defmethod opt-val ((m <PoseOperation>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader obrobot_navigation-msg:opt-val is deprecated.  Use obrobot_navigation-msg:opt instead.")
  (opt m))

(cl:ensure-generic-function 'id-val :lambda-list '(m))
(cl:defmethod id-val ((m <PoseOperation>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader obrobot_navigation-msg:id-val is deprecated.  Use obrobot_navigation-msg:id instead.")
  (id m))

(cl:ensure-generic-function 'name-val :lambda-list '(m))
(cl:defmethod name-val ((m <PoseOperation>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader obrobot_navigation-msg:name-val is deprecated.  Use obrobot_navigation-msg:name instead.")
  (name m))

(cl:ensure-generic-function 'type-val :lambda-list '(m))
(cl:defmethod type-val ((m <PoseOperation>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader obrobot_navigation-msg:type-val is deprecated.  Use obrobot_navigation-msg:type instead.")
  (type m))

(cl:ensure-generic-function 'floor-val :lambda-list '(m))
(cl:defmethod floor-val ((m <PoseOperation>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader obrobot_navigation-msg:floor-val is deprecated.  Use obrobot_navigation-msg:floor instead.")
  (floor m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <PoseOperation>) ostream)
  "Serializes a message object of type '<PoseOperation>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'opt))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'opt))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'id)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'id)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'id)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'id)) ostream)
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'name))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'name))
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'type))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'type))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'floor)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'floor)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'floor)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'floor)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <PoseOperation>) istream)
  "Deserializes a message object of type '<PoseOperation>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'opt) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'opt) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'id)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'id)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'id)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'id)) (cl:read-byte istream))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'name) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'name) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'type) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'type) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'floor)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'floor)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'floor)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'floor)) (cl:read-byte istream))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<PoseOperation>)))
  "Returns string type for a message object of type '<PoseOperation>"
  "obrobot_navigation/PoseOperation")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'PoseOperation)))
  "Returns string type for a message object of type 'PoseOperation"
  "obrobot_navigation/PoseOperation")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<PoseOperation>)))
  "Returns md5sum for a message object of type '<PoseOperation>"
  "a3c8f0bce74dfc0445629cc8fb5aa8a9")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'PoseOperation)))
  "Returns md5sum for a message object of type 'PoseOperation"
  "a3c8f0bce74dfc0445629cc8fb5aa8a9")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<PoseOperation>)))
  "Returns full string definition for message of type '<PoseOperation>"
  (cl:format cl:nil "string opt~%uint32 id~%string name~%string type~%uint32 floor~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'PoseOperation)))
  "Returns full string definition for message of type 'PoseOperation"
  (cl:format cl:nil "string opt~%uint32 id~%string name~%string type~%uint32 floor~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <PoseOperation>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'opt))
     4
     4 (cl:length (cl:slot-value msg 'name))
     4 (cl:length (cl:slot-value msg 'type))
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <PoseOperation>))
  "Converts a ROS message object to a list"
  (cl:list 'PoseOperation
    (cl:cons ':opt (opt msg))
    (cl:cons ':id (id msg))
    (cl:cons ':name (name msg))
    (cl:cons ':type (type msg))
    (cl:cons ':floor (floor msg))
))
