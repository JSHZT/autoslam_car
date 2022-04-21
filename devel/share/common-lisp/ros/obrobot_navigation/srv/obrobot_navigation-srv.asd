
(cl:in-package :asdf)

(defsystem "obrobot_navigation-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :obrobot_navigation-msg
)
  :components ((:file "_package")
    (:file "PoseManage" :depends-on ("_package_PoseManage"))
    (:file "_package_PoseManage" :depends-on ("_package"))
  ))