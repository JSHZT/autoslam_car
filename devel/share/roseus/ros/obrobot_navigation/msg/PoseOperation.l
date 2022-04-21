;; Auto-generated. Do not edit!


(when (boundp 'obrobot_navigation::PoseOperation)
  (if (not (find-package "OBROBOT_NAVIGATION"))
    (make-package "OBROBOT_NAVIGATION"))
  (shadow 'PoseOperation (find-package "OBROBOT_NAVIGATION")))
(unless (find-package "OBROBOT_NAVIGATION::POSEOPERATION")
  (make-package "OBROBOT_NAVIGATION::POSEOPERATION"))

(in-package "ROS")
;;//! \htmlinclude PoseOperation.msg.html


(defclass obrobot_navigation::PoseOperation
  :super ros::object
  :slots (_opt _id _name _type _floor ))

(defmethod obrobot_navigation::PoseOperation
  (:init
   (&key
    ((:opt __opt) "")
    ((:id __id) 0)
    ((:name __name) "")
    ((:type __type) "")
    ((:floor __floor) 0)
    )
   (send-super :init)
   (setq _opt (string __opt))
   (setq _id (round __id))
   (setq _name (string __name))
   (setq _type (string __type))
   (setq _floor (round __floor))
   self)
  (:opt
   (&optional __opt)
   (if __opt (setq _opt __opt)) _opt)
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
  (:serialization-length
   ()
   (+
    ;; string _opt
    4 (length _opt)
    ;; uint32 _id
    4
    ;; string _name
    4 (length _name)
    ;; string _type
    4 (length _type)
    ;; uint32 _floor
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _opt
       (write-long (length _opt) s) (princ _opt s)
     ;; uint32 _id
       (write-long _id s)
     ;; string _name
       (write-long (length _name) s) (princ _name s)
     ;; string _type
       (write-long (length _type) s) (princ _type s)
     ;; uint32 _floor
       (write-long _floor s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _opt
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _opt (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; uint32 _id
     (setq _id (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; string _name
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _name (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; string _type
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _type (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; uint32 _floor
     (setq _floor (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get obrobot_navigation::PoseOperation :md5sum-) "a3c8f0bce74dfc0445629cc8fb5aa8a9")
(setf (get obrobot_navigation::PoseOperation :datatype-) "obrobot_navigation/PoseOperation")
(setf (get obrobot_navigation::PoseOperation :definition-)
      "string opt
uint32 id
string name
string type
uint32 floor

")



(provide :obrobot_navigation/PoseOperation "a3c8f0bce74dfc0445629cc8fb5aa8a9")


