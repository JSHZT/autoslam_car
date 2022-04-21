
(cl:in-package :asdf)

(defsystem "obrobot_navigation-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :geometry_msgs-msg
)
  :components ((:file "_package")
    (:file "PoseDefine" :depends-on ("_package_PoseDefine"))
    (:file "_package_PoseDefine" :depends-on ("_package"))
    (:file "PoseDefine" :depends-on ("_package_PoseDefine"))
    (:file "_package_PoseDefine" :depends-on ("_package"))
    (:file "PoseOperation" :depends-on ("_package_PoseOperation"))
    (:file "_package_PoseOperation" :depends-on ("_package"))
    (:file "PoseOperation" :depends-on ("_package_PoseOperation"))
    (:file "_package_PoseOperation" :depends-on ("_package"))
  ))