# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.13

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/pi/autoslam_gm/src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/pi/autoslam_gm/build

# Include any dependencies generated for this target.
include sc_mini/CMakeFiles/sc_mini.dir/depend.make

# Include the progress variables for this target.
include sc_mini/CMakeFiles/sc_mini.dir/progress.make

# Include the compile flags for this target's objects.
include sc_mini/CMakeFiles/sc_mini.dir/flags.make

sc_mini/CMakeFiles/sc_mini.dir/src/sc_mini.cpp.o: sc_mini/CMakeFiles/sc_mini.dir/flags.make
sc_mini/CMakeFiles/sc_mini.dir/src/sc_mini.cpp.o: /home/pi/autoslam_gm/src/sc_mini/src/sc_mini.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/pi/autoslam_gm/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object sc_mini/CMakeFiles/sc_mini.dir/src/sc_mini.cpp.o"
	cd /home/pi/autoslam_gm/build/sc_mini && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/sc_mini.dir/src/sc_mini.cpp.o -c /home/pi/autoslam_gm/src/sc_mini/src/sc_mini.cpp

sc_mini/CMakeFiles/sc_mini.dir/src/sc_mini.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/sc_mini.dir/src/sc_mini.cpp.i"
	cd /home/pi/autoslam_gm/build/sc_mini && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/pi/autoslam_gm/src/sc_mini/src/sc_mini.cpp > CMakeFiles/sc_mini.dir/src/sc_mini.cpp.i

sc_mini/CMakeFiles/sc_mini.dir/src/sc_mini.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/sc_mini.dir/src/sc_mini.cpp.s"
	cd /home/pi/autoslam_gm/build/sc_mini && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/pi/autoslam_gm/src/sc_mini/src/sc_mini.cpp -o CMakeFiles/sc_mini.dir/src/sc_mini.cpp.s

# Object files for target sc_mini
sc_mini_OBJECTS = \
"CMakeFiles/sc_mini.dir/src/sc_mini.cpp.o"

# External object files for target sc_mini
sc_mini_EXTERNAL_OBJECTS =

/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: sc_mini/CMakeFiles/sc_mini.dir/src/sc_mini.cpp.o
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: sc_mini/CMakeFiles/sc_mini.dir/build.make
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /usr/lib/arm-linux-gnueabihf/libtinyxml2.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /opt/ros/kinetic/lib/libclass_loader.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /usr/lib/libPocoFoundation.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /usr/lib/arm-linux-gnueabihf/libdl.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /opt/ros/kinetic/lib/libroslib.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /opt/ros/kinetic/lib/librospack.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /usr/lib/arm-linux-gnueabihf/libpython2.7.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /usr/local/lib/libboost_program_options.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /usr/lib/arm-linux-gnueabihf/libtinyxml.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /opt/ros/kinetic/lib/libtf.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /opt/ros/kinetic/lib/libtf2_ros.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /opt/ros/kinetic/lib/libactionlib.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /opt/ros/kinetic/lib/libmessage_filters.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /opt/ros/kinetic/lib/libroscpp.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /usr/lib/arm-linux-gnueabihf/libpthread.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /usr/local/lib/libboost_filesystem.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /usr/local/lib/libboost_signals.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /opt/ros/kinetic/lib/libxmlrpcpp.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /opt/ros/kinetic/lib/libtf2.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /opt/ros/kinetic/lib/libroscpp_serialization.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /opt/ros/kinetic/lib/librosconsole.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /opt/ros/kinetic/lib/librosconsole_log4cxx.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /opt/ros/kinetic/lib/librosconsole_backend_interface.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /usr/lib/arm-linux-gnueabihf/liblog4cxx.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /usr/local/lib/libboost_regex.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /opt/ros/kinetic/lib/librostime.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /opt/ros/kinetic/lib/libcpp_common.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /usr/local/lib/libboost_system.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /usr/local/lib/libboost_thread.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /usr/local/lib/libboost_chrono.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /usr/local/lib/libboost_date_time.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /usr/local/lib/libboost_atomic.so
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: /usr/lib/arm-linux-gnueabihf/libconsole_bridge.so.0.4
/home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini: sc_mini/CMakeFiles/sc_mini.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/pi/autoslam_gm/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable /home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini"
	cd /home/pi/autoslam_gm/build/sc_mini && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/sc_mini.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
sc_mini/CMakeFiles/sc_mini.dir/build: /home/pi/autoslam_gm/devel/lib/sc_mini/sc_mini

.PHONY : sc_mini/CMakeFiles/sc_mini.dir/build

sc_mini/CMakeFiles/sc_mini.dir/clean:
	cd /home/pi/autoslam_gm/build/sc_mini && $(CMAKE_COMMAND) -P CMakeFiles/sc_mini.dir/cmake_clean.cmake
.PHONY : sc_mini/CMakeFiles/sc_mini.dir/clean

sc_mini/CMakeFiles/sc_mini.dir/depend:
	cd /home/pi/autoslam_gm/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/pi/autoslam_gm/src /home/pi/autoslam_gm/src/sc_mini /home/pi/autoslam_gm/build /home/pi/autoslam_gm/build/sc_mini /home/pi/autoslam_gm/build/sc_mini/CMakeFiles/sc_mini.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : sc_mini/CMakeFiles/sc_mini.dir/depend

