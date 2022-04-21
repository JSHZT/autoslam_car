# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "obrobot_tools: 7 messages, 0 services")

set(MSG_I_FLAGS "-Iobrobot_tools:/home/pi/autoslam_gm/devel/share/obrobot_tools/msg;-Iactionlib_msgs:/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg;-Istd_msgs:/opt/ros/kinetic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(obrobot_tools_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgResult.msg" NAME_WE)
add_custom_target(_obrobot_tools_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "obrobot_tools" "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgResult.msg" ""
)

get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionResult.msg" NAME_WE)
add_custom_target(_obrobot_tools_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "obrobot_tools" "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionResult.msg" "actionlib_msgs/GoalID:obrobot_tools/check_msgResult:std_msgs/Header:actionlib_msgs/GoalStatus"
)

get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionGoal.msg" NAME_WE)
add_custom_target(_obrobot_tools_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "obrobot_tools" "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionGoal.msg" "actionlib_msgs/GoalID:std_msgs/Header:obrobot_tools/check_msgGoal"
)

get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgAction.msg" NAME_WE)
add_custom_target(_obrobot_tools_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "obrobot_tools" "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgAction.msg" "actionlib_msgs/GoalStatus:obrobot_tools/check_msgActionFeedback:obrobot_tools/check_msgResult:obrobot_tools/check_msgGoal:std_msgs/Header:obrobot_tools/check_msgFeedback:actionlib_msgs/GoalID:obrobot_tools/check_msgActionResult:obrobot_tools/check_msgActionGoal"
)

get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionFeedback.msg" NAME_WE)
add_custom_target(_obrobot_tools_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "obrobot_tools" "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionFeedback.msg" "obrobot_tools/check_msgFeedback:actionlib_msgs/GoalID:std_msgs/Header:actionlib_msgs/GoalStatus"
)

get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgGoal.msg" NAME_WE)
add_custom_target(_obrobot_tools_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "obrobot_tools" "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgGoal.msg" ""
)

get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgFeedback.msg" NAME_WE)
add_custom_target(_obrobot_tools_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "obrobot_tools" "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgFeedback.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/obrobot_tools
)
_generate_msg_cpp(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgResult.msg;/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/obrobot_tools
)
_generate_msg_cpp(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgGoal.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/obrobot_tools
)
_generate_msg_cpp(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionFeedback.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgResult.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgGoal.msg;/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgFeedback.msg;/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionResult.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionGoal.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/obrobot_tools
)
_generate_msg_cpp(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgFeedback.msg;/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/obrobot_tools
)
_generate_msg_cpp(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgGoal.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/obrobot_tools
)
_generate_msg_cpp(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgFeedback.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/obrobot_tools
)

### Generating Services

### Generating Module File
_generate_module_cpp(obrobot_tools
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/obrobot_tools
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(obrobot_tools_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(obrobot_tools_generate_messages obrobot_tools_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgResult.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_cpp _obrobot_tools_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionResult.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_cpp _obrobot_tools_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionGoal.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_cpp _obrobot_tools_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgAction.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_cpp _obrobot_tools_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionFeedback.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_cpp _obrobot_tools_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgGoal.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_cpp _obrobot_tools_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgFeedback.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_cpp _obrobot_tools_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(obrobot_tools_gencpp)
add_dependencies(obrobot_tools_gencpp obrobot_tools_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS obrobot_tools_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/obrobot_tools
)
_generate_msg_eus(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgResult.msg;/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/obrobot_tools
)
_generate_msg_eus(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgGoal.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/obrobot_tools
)
_generate_msg_eus(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionFeedback.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgResult.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgGoal.msg;/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgFeedback.msg;/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionResult.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionGoal.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/obrobot_tools
)
_generate_msg_eus(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgFeedback.msg;/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/obrobot_tools
)
_generate_msg_eus(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgGoal.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/obrobot_tools
)
_generate_msg_eus(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgFeedback.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/obrobot_tools
)

### Generating Services

### Generating Module File
_generate_module_eus(obrobot_tools
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/obrobot_tools
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(obrobot_tools_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(obrobot_tools_generate_messages obrobot_tools_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgResult.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_eus _obrobot_tools_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionResult.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_eus _obrobot_tools_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionGoal.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_eus _obrobot_tools_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgAction.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_eus _obrobot_tools_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionFeedback.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_eus _obrobot_tools_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgGoal.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_eus _obrobot_tools_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgFeedback.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_eus _obrobot_tools_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(obrobot_tools_geneus)
add_dependencies(obrobot_tools_geneus obrobot_tools_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS obrobot_tools_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/obrobot_tools
)
_generate_msg_lisp(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgResult.msg;/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/obrobot_tools
)
_generate_msg_lisp(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgGoal.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/obrobot_tools
)
_generate_msg_lisp(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionFeedback.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgResult.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgGoal.msg;/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgFeedback.msg;/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionResult.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionGoal.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/obrobot_tools
)
_generate_msg_lisp(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgFeedback.msg;/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/obrobot_tools
)
_generate_msg_lisp(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgGoal.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/obrobot_tools
)
_generate_msg_lisp(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgFeedback.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/obrobot_tools
)

### Generating Services

### Generating Module File
_generate_module_lisp(obrobot_tools
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/obrobot_tools
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(obrobot_tools_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(obrobot_tools_generate_messages obrobot_tools_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgResult.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_lisp _obrobot_tools_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionResult.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_lisp _obrobot_tools_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionGoal.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_lisp _obrobot_tools_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgAction.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_lisp _obrobot_tools_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionFeedback.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_lisp _obrobot_tools_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgGoal.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_lisp _obrobot_tools_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgFeedback.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_lisp _obrobot_tools_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(obrobot_tools_genlisp)
add_dependencies(obrobot_tools_genlisp obrobot_tools_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS obrobot_tools_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/obrobot_tools
)
_generate_msg_nodejs(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgResult.msg;/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/obrobot_tools
)
_generate_msg_nodejs(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgGoal.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/obrobot_tools
)
_generate_msg_nodejs(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionFeedback.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgResult.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgGoal.msg;/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgFeedback.msg;/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionResult.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionGoal.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/obrobot_tools
)
_generate_msg_nodejs(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgFeedback.msg;/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/obrobot_tools
)
_generate_msg_nodejs(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgGoal.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/obrobot_tools
)
_generate_msg_nodejs(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgFeedback.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/obrobot_tools
)

### Generating Services

### Generating Module File
_generate_module_nodejs(obrobot_tools
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/obrobot_tools
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(obrobot_tools_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(obrobot_tools_generate_messages obrobot_tools_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgResult.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_nodejs _obrobot_tools_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionResult.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_nodejs _obrobot_tools_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionGoal.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_nodejs _obrobot_tools_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgAction.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_nodejs _obrobot_tools_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionFeedback.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_nodejs _obrobot_tools_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgGoal.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_nodejs _obrobot_tools_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgFeedback.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_nodejs _obrobot_tools_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(obrobot_tools_gennodejs)
add_dependencies(obrobot_tools_gennodejs obrobot_tools_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS obrobot_tools_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/obrobot_tools
)
_generate_msg_py(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgResult.msg;/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/obrobot_tools
)
_generate_msg_py(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgGoal.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/obrobot_tools
)
_generate_msg_py(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionFeedback.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgResult.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgGoal.msg;/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgFeedback.msg;/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionResult.msg;/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionGoal.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/obrobot_tools
)
_generate_msg_py(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgFeedback.msg;/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/obrobot_tools
)
_generate_msg_py(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgGoal.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/obrobot_tools
)
_generate_msg_py(obrobot_tools
  "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgFeedback.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/obrobot_tools
)

### Generating Services

### Generating Module File
_generate_module_py(obrobot_tools
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/obrobot_tools
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(obrobot_tools_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(obrobot_tools_generate_messages obrobot_tools_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgResult.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_py _obrobot_tools_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionResult.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_py _obrobot_tools_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionGoal.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_py _obrobot_tools_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgAction.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_py _obrobot_tools_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgActionFeedback.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_py _obrobot_tools_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgGoal.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_py _obrobot_tools_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/pi/autoslam_gm/devel/share/obrobot_tools/msg/check_msgFeedback.msg" NAME_WE)
add_dependencies(obrobot_tools_generate_messages_py _obrobot_tools_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(obrobot_tools_genpy)
add_dependencies(obrobot_tools_genpy obrobot_tools_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS obrobot_tools_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/obrobot_tools)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/obrobot_tools
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET actionlib_msgs_generate_messages_cpp)
  add_dependencies(obrobot_tools_generate_messages_cpp actionlib_msgs_generate_messages_cpp)
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(obrobot_tools_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/obrobot_tools)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/obrobot_tools
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET actionlib_msgs_generate_messages_eus)
  add_dependencies(obrobot_tools_generate_messages_eus actionlib_msgs_generate_messages_eus)
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(obrobot_tools_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/obrobot_tools)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/obrobot_tools
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET actionlib_msgs_generate_messages_lisp)
  add_dependencies(obrobot_tools_generate_messages_lisp actionlib_msgs_generate_messages_lisp)
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(obrobot_tools_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/obrobot_tools)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/obrobot_tools
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET actionlib_msgs_generate_messages_nodejs)
  add_dependencies(obrobot_tools_generate_messages_nodejs actionlib_msgs_generate_messages_nodejs)
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(obrobot_tools_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/obrobot_tools)
  install(CODE "execute_process(COMMAND \"/usr/bin/python\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/obrobot_tools\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/obrobot_tools
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET actionlib_msgs_generate_messages_py)
  add_dependencies(obrobot_tools_generate_messages_py actionlib_msgs_generate_messages_py)
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(obrobot_tools_generate_messages_py std_msgs_generate_messages_py)
endif()
