# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "obrobot_navigation: 2 messages, 1 services")

set(MSG_I_FLAGS "-Iobrobot_navigation:/home/pi/autoslam_gm/src/obrobot_navigation/msg;-Istd_msgs:/opt/ros/kinetic/share/std_msgs/cmake/../msg;-Iobrobot_navigation:/home/pi/autoslam_gm/src/obrobot_navigation/msg;-Igeometry_msgs:/opt/ros/kinetic/share/geometry_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(obrobot_navigation_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/pi/autoslam_gm/src/obrobot_navigation/srv/PoseManage.srv" NAME_WE)
add_custom_target(_obrobot_navigation_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "obrobot_navigation" "/home/pi/autoslam_gm/src/obrobot_navigation/srv/PoseManage.srv" "obrobot_navigation/PoseOperation:geometry_msgs/Pose:geometry_msgs/Quaternion:geometry_msgs/Point:obrobot_navigation/PoseDefine"
)

get_filename_component(_filename "/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseDefine.msg" NAME_WE)
add_custom_target(_obrobot_navigation_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "obrobot_navigation" "/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseDefine.msg" "geometry_msgs/Quaternion:geometry_msgs/Pose:geometry_msgs/Point"
)

get_filename_component(_filename "/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseOperation.msg" NAME_WE)
add_custom_target(_obrobot_navigation_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "obrobot_navigation" "/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseOperation.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(obrobot_navigation
  "/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseDefine.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/obrobot_navigation
)
_generate_msg_cpp(obrobot_navigation
  "/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseOperation.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/obrobot_navigation
)

### Generating Services
_generate_srv_cpp(obrobot_navigation
  "/home/pi/autoslam_gm/src/obrobot_navigation/srv/PoseManage.srv"
  "${MSG_I_FLAGS}"
  "/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseOperation.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Point.msg;/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseDefine.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/obrobot_navigation
)

### Generating Module File
_generate_module_cpp(obrobot_navigation
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/obrobot_navigation
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(obrobot_navigation_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(obrobot_navigation_generate_messages obrobot_navigation_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/pi/autoslam_gm/src/obrobot_navigation/srv/PoseManage.srv" NAME_WE)
add_dependencies(obrobot_navigation_generate_messages_cpp _obrobot_navigation_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseDefine.msg" NAME_WE)
add_dependencies(obrobot_navigation_generate_messages_cpp _obrobot_navigation_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseOperation.msg" NAME_WE)
add_dependencies(obrobot_navigation_generate_messages_cpp _obrobot_navigation_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(obrobot_navigation_gencpp)
add_dependencies(obrobot_navigation_gencpp obrobot_navigation_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS obrobot_navigation_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(obrobot_navigation
  "/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseDefine.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/obrobot_navigation
)
_generate_msg_eus(obrobot_navigation
  "/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseOperation.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/obrobot_navigation
)

### Generating Services
_generate_srv_eus(obrobot_navigation
  "/home/pi/autoslam_gm/src/obrobot_navigation/srv/PoseManage.srv"
  "${MSG_I_FLAGS}"
  "/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseOperation.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Point.msg;/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseDefine.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/obrobot_navigation
)

### Generating Module File
_generate_module_eus(obrobot_navigation
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/obrobot_navigation
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(obrobot_navigation_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(obrobot_navigation_generate_messages obrobot_navigation_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/pi/autoslam_gm/src/obrobot_navigation/srv/PoseManage.srv" NAME_WE)
add_dependencies(obrobot_navigation_generate_messages_eus _obrobot_navigation_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseDefine.msg" NAME_WE)
add_dependencies(obrobot_navigation_generate_messages_eus _obrobot_navigation_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseOperation.msg" NAME_WE)
add_dependencies(obrobot_navigation_generate_messages_eus _obrobot_navigation_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(obrobot_navigation_geneus)
add_dependencies(obrobot_navigation_geneus obrobot_navigation_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS obrobot_navigation_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(obrobot_navigation
  "/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseDefine.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/obrobot_navigation
)
_generate_msg_lisp(obrobot_navigation
  "/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseOperation.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/obrobot_navigation
)

### Generating Services
_generate_srv_lisp(obrobot_navigation
  "/home/pi/autoslam_gm/src/obrobot_navigation/srv/PoseManage.srv"
  "${MSG_I_FLAGS}"
  "/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseOperation.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Point.msg;/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseDefine.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/obrobot_navigation
)

### Generating Module File
_generate_module_lisp(obrobot_navigation
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/obrobot_navigation
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(obrobot_navigation_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(obrobot_navigation_generate_messages obrobot_navigation_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/pi/autoslam_gm/src/obrobot_navigation/srv/PoseManage.srv" NAME_WE)
add_dependencies(obrobot_navigation_generate_messages_lisp _obrobot_navigation_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseDefine.msg" NAME_WE)
add_dependencies(obrobot_navigation_generate_messages_lisp _obrobot_navigation_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseOperation.msg" NAME_WE)
add_dependencies(obrobot_navigation_generate_messages_lisp _obrobot_navigation_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(obrobot_navigation_genlisp)
add_dependencies(obrobot_navigation_genlisp obrobot_navigation_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS obrobot_navigation_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(obrobot_navigation
  "/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseDefine.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/obrobot_navigation
)
_generate_msg_nodejs(obrobot_navigation
  "/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseOperation.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/obrobot_navigation
)

### Generating Services
_generate_srv_nodejs(obrobot_navigation
  "/home/pi/autoslam_gm/src/obrobot_navigation/srv/PoseManage.srv"
  "${MSG_I_FLAGS}"
  "/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseOperation.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Point.msg;/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseDefine.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/obrobot_navigation
)

### Generating Module File
_generate_module_nodejs(obrobot_navigation
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/obrobot_navigation
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(obrobot_navigation_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(obrobot_navigation_generate_messages obrobot_navigation_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/pi/autoslam_gm/src/obrobot_navigation/srv/PoseManage.srv" NAME_WE)
add_dependencies(obrobot_navigation_generate_messages_nodejs _obrobot_navigation_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseDefine.msg" NAME_WE)
add_dependencies(obrobot_navigation_generate_messages_nodejs _obrobot_navigation_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseOperation.msg" NAME_WE)
add_dependencies(obrobot_navigation_generate_messages_nodejs _obrobot_navigation_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(obrobot_navigation_gennodejs)
add_dependencies(obrobot_navigation_gennodejs obrobot_navigation_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS obrobot_navigation_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(obrobot_navigation
  "/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseDefine.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/obrobot_navigation
)
_generate_msg_py(obrobot_navigation
  "/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseOperation.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/obrobot_navigation
)

### Generating Services
_generate_srv_py(obrobot_navigation
  "/home/pi/autoslam_gm/src/obrobot_navigation/srv/PoseManage.srv"
  "${MSG_I_FLAGS}"
  "/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseOperation.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Point.msg;/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseDefine.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/obrobot_navigation
)

### Generating Module File
_generate_module_py(obrobot_navigation
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/obrobot_navigation
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(obrobot_navigation_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(obrobot_navigation_generate_messages obrobot_navigation_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/pi/autoslam_gm/src/obrobot_navigation/srv/PoseManage.srv" NAME_WE)
add_dependencies(obrobot_navigation_generate_messages_py _obrobot_navigation_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseDefine.msg" NAME_WE)
add_dependencies(obrobot_navigation_generate_messages_py _obrobot_navigation_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/src/obrobot_navigation/msg/PoseOperation.msg" NAME_WE)
add_dependencies(obrobot_navigation_generate_messages_py _obrobot_navigation_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(obrobot_navigation_genpy)
add_dependencies(obrobot_navigation_genpy obrobot_navigation_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS obrobot_navigation_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/obrobot_navigation)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/obrobot_navigation
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(obrobot_navigation_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()
if(TARGET obrobot_navigation_generate_messages_cpp)
  add_dependencies(obrobot_navigation_generate_messages_cpp obrobot_navigation_generate_messages_cpp)
endif()
if(TARGET geometry_msgs_generate_messages_cpp)
  add_dependencies(obrobot_navigation_generate_messages_cpp geometry_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/obrobot_navigation)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/obrobot_navigation
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(obrobot_navigation_generate_messages_eus std_msgs_generate_messages_eus)
endif()
if(TARGET obrobot_navigation_generate_messages_eus)
  add_dependencies(obrobot_navigation_generate_messages_eus obrobot_navigation_generate_messages_eus)
endif()
if(TARGET geometry_msgs_generate_messages_eus)
  add_dependencies(obrobot_navigation_generate_messages_eus geometry_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/obrobot_navigation)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/obrobot_navigation
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(obrobot_navigation_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()
if(TARGET obrobot_navigation_generate_messages_lisp)
  add_dependencies(obrobot_navigation_generate_messages_lisp obrobot_navigation_generate_messages_lisp)
endif()
if(TARGET geometry_msgs_generate_messages_lisp)
  add_dependencies(obrobot_navigation_generate_messages_lisp geometry_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/obrobot_navigation)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/obrobot_navigation
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(obrobot_navigation_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()
if(TARGET obrobot_navigation_generate_messages_nodejs)
  add_dependencies(obrobot_navigation_generate_messages_nodejs obrobot_navigation_generate_messages_nodejs)
endif()
if(TARGET geometry_msgs_generate_messages_nodejs)
  add_dependencies(obrobot_navigation_generate_messages_nodejs geometry_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/obrobot_navigation)
  install(CODE "execute_process(COMMAND \"/usr/bin/python\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/obrobot_navigation\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/obrobot_navigation
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(obrobot_navigation_generate_messages_py std_msgs_generate_messages_py)
endif()
if(TARGET obrobot_navigation_generate_messages_py)
  add_dependencies(obrobot_navigation_generate_messages_py obrobot_navigation_generate_messages_py)
endif()
if(TARGET geometry_msgs_generate_messages_py)
  add_dependencies(obrobot_navigation_generate_messages_py geometry_msgs_generate_messages_py)
endif()
