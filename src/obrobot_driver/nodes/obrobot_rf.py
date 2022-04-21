#!/usr/bin/env python
#encoding=utf-8

import rospy
from geometry_msgs.msg import Twist
import os, time
import thread

import math
from math import pi as PI, degrees, radians, sin, cos
import os
import time
import sys, traceback
from serial.serialutil import SerialException
from serial import Serial
import serial.tools.list_ports
import roslib

from geometry_msgs.msg import Quaternion, Twist, Pose ,Point
from nav_msgs.msg import Odometry
from std_msgs.msg import Bool, Int16, Int32, UInt16, Float32, String
from tf.broadcaster import TransformBroadcaster
from sensor_msgs.msg import Range, Imu, LaserScan
import sensor_msgs.point_cloud2 as pc2
from sensor_msgs.msg import PointCloud2, PointField 

import struct
import binascii
 
ODOM_POSE_COVARIANCE = [1e-3, 0, 0, 0, 0, 0, 
                        0, 1e-3, 0, 0, 0, 0,
                        0, 0, 1e6, 0, 0, 0,
                        0, 0, 0, 1e6, 0, 0,
                        0, 0, 0, 0, 1e6, 0,
                        0, 0, 0, 0, 0, 1e3]
ODOM_POSE_COVARIANCE2 = [1e-9, 0, 0, 0, 0, 0, 
                         0, 1e-3, 1e-9, 0, 0, 0,
                         0, 0, 1e6, 0, 0, 0,
                         0, 0, 0, 1e6, 0, 0,
                         0, 0, 0, 0, 1e6, 0,
                         0, 0, 0, 0, 0, 1e-9]

ODOM_TWIST_COVARIANCE = [1e-3, 0, 0, 0, 0, 0, 
                         0, 1e-3, 0, 0, 0, 0,
                         0, 0, 1e6, 0, 0, 0,
                         0, 0, 0, 1e6, 0, 0,
                         0, 0, 0, 0, 1e6, 0,
                         0, 0, 0, 0, 0, 1e3]
ODOM_TWIST_COVARIANCE2 = [1e-9, 0, 0, 0, 0, 0, 
                          0, 1e-3, 1e-9, 0, 0, 0,
                          0, 0, 1e6, 0, 0, 0,
                          0, 0, 0, 1e6, 0, 0,
                          0, 0, 0, 0, 1e6, 0,
                          0, 0, 0, 0, 0, 1e-9]


SERVO_MAX = 180
SERVO_MIN = 0



class Stm32:
    ''' Configuration Parameters
    '''    
    N_ANALOG_PORTS = 6
    N_DIGITAL_PORTS = 12


    
    def __init__(self, port="/dev/ttyUSB1", baudrate=115200, timeout=0.5):
        
        self.PID_RATE = 30 # Do not change this! 
        self.PID_INTERVAL = 1000 / 30

        
        self.port = rospy.get_param("~port", "/dev/ttyUSB1") #port
        self.baudrate = baudrate
        self.timeout = timeout
        self.encoder_count = 0
        self.writeTimeout = timeout
        self.interCharTimeout = timeout / 30.

        self.WAITING_FF = 0
        self.WAITING_AA = 1
        self.RECEIVE_LEN = 2
        self.RECEIVE_PACKAGE = 3
        self.RECEIVE_CHECK = 4
        self.HEADER0 = 0xff
        self.HEADER1 = 0xaa
        
        self.SUCCESS = 0
        self.FAIL = -1

        self.receive_state_ = self.WAITING_FF
        self.receive_check_sum_ = 0
        self.payload_command = ''
        self.payload_ack = ''
        self.payload_args = ''
        self.payload_len = 0
        self.byte_count_ = 0
        self.receive_message_length_ = 0

        self.sendcmdad = 0 #zark
    
        # Keep things thread safe
        self.mutex = thread.allocate_lock()
            
        # An array to cache analog sensor readings
        self.analog_sensor_cache = [None] * self.N_ANALOG_PORTS
        
        # An array to cache digital sensor readings
        self.digital_sensor_cache = [None] * self.N_DIGITAL_PORTS
    
    def clearsendcmdad(self):
        self.sendcmdad = 0

    def setsendcmdad(self):
        self.sendcmdad = 1

    def getsendcmdad(self):
        return self.sendcmdad
    
    def connect(self):

        port_list = list(serial.tools.list_ports.comports())
        count_port = len(port_list)
        #print "port list length",count_port
        if count_port<=0:
	    print "the serial port can not find!"
            os._exit(1)
        else:

            while count_port>0:
                port_info = list(port_list[count_port-1])
                self.port = port_info[0]
                #print self.port
                self.port = Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout, writeTimeout=self.writeTimeout)
                print "check which port was connected to mcu>",self.port.name
                time.sleep(1)
                #self.receive_state_ = self.WAITING_FF
                #self.receive_check_sum_ = 0
                #self.payload_command = ''
                #self.payload_ack = ''
                #self.payload_args = ''
                #self.payload_len = 0
                #self.byte_count_ = 0
                #state_, val = self.get_baud()
                #if (state_ == self.SUCCESS):
		   #break
		state_,val0, val1,val2,val3 = self.get_firmware_version()
                #print state_,val0, val1,val2,val3
	        if (state_ == self.SUCCESS) and (val0==0x01):
		    print "Device Type:",val0, "firmware version:",val1,".",val2,val3
                    print "Connected at ", self.port.name," and baudrate is ",self.baudrate
                    print "MCU is ready."
                    break
                self.port.close()
                count_port = count_port - 1
            if count_port==0:
                print "Cannot connect to mcu!"
                os._exit(1)

    def open(self): 
        ''' Open the serial port.
        '''
        self.port.open()

    def close(self): 
        ''' Close the serial port.
        '''
        self.port.close() 
    
    def send(self, cmd):
        ''' This command should not be used on its own: it is called by the execute commands
            below in a thread safe manner.
        '''
        self.port.write(cmd)


    def receiveFiniteStates(self, rx_data):
        if self.receive_state_ == self.WAITING_FF:
            #print str(binascii.b2a_hex(rx_data))
            if rx_data == '\xff':
                self.receive_state_ = self.WAITING_AA
                self.receive_check_sum_ =0
                self.receive_message_length_ = 0
                self.byte_count_=0
                self.payload_ack = ''
                self.payload_args = ''
                self.payload_len = 0


        elif self.receive_state_ == self.WAITING_AA :
             if rx_data == '\xaa':
                 self.receive_state_ = self.RECEIVE_LEN
                 self.receive_check_sum_ = 0
             else:
                 self.receive_state_ = self.WAITING_FF

        elif self.receive_state_ == self.RECEIVE_LEN:
             self.receive_message_length_, = struct.unpack("B",rx_data)
             self.receive_state_ = self.RECEIVE_PACKAGE
             self.receive_check_sum_ = self.receive_message_length_
        elif self.receive_state_ == self.RECEIVE_PACKAGE:
             if self.byte_count_==0:
                 self.payload_ack = rx_data
             else:
                 self.payload_args += rx_data
             uc_tmp_, = struct.unpack("B",rx_data)
             self.receive_check_sum_ = self.receive_check_sum_ + uc_tmp_
             self.byte_count_ +=1
             #print "byte:"+str(byte_count_) +","+ "rece_len:"+str(receive_message_length_)
             if self.byte_count_ >= self.receive_message_length_:
                 self.receive_state_ = self.RECEIVE_CHECK

        elif self.receive_state_ == self.RECEIVE_CHECK:
            #print "checksun:" + str(rx_data) + " " + str(self.receive_check_sum_%255)
            #uc_tmp_, = struct.unpack("B",rx_data)
            #print "checksum:" + str(uc_tmp_) +" " + str((self.receive_check_sum_)%255)
            #if uc_tmp_ == (self.receive_check_sum_)%255:
            if 1:
                self.receive_state_ = self.WAITING_FF
                #print str(binascii.b2a_hex(value))
                #left, right, = struct.unpack('hh', value)
                #print "left:"+str(left)+", right:"+str(right)
                return 1 
            else:
                self.receive_state_ = self.WAITING_FF
        else:
            self.receive_state_ = self.WAITING_FF;
        return 0
    def car_changeposition1(self, motor_id, time, motor_angular): # jin_liang 3.7
        data1 = struct.pack("h", motor_id)
        d1, d2 = struct.unpack("BB", data1)

        data2 = struct.pack("h", time)
        c1, c2 = struct.unpack("BB", data2)
        
        data3 = struct.pack("h", motor_angular)
        b1, b2 = struct.unpack("BB", data2)

        self.check_list = [0x07,0x22, d1, d2, c1, c2, b1, b2]
        self.check_num = self.get_check_sum(self.check_list)
        cmd_str=struct.pack("4B", self.HEADER0, self.HEADER1, 0x07, 0x22) + struct.pack("hhh", motor_id, time, motor_angular) + struct.pack("B", self.check_num)
        #print("left drive at", left, "right drive at",right) #
        if (self.execute(cmd_str))==1 and self.payload_ack == '\x00':
           return  self.SUCCESS
        else:
           return self.FAIL
    def recv(self, timeout=0.5):
        timeout = min(timeout, self.timeout)
        ''' This command should not be used on its own: it is called by the execute commands   
            below in a thread safe manner.  Note: we use read() instead of readline() since
            readline() tends to return garbage characters from the Stm32
        '''
        c = ''
        value = ''
        attempts = 0
        c = self.port.read(1)
        #print str(binascii.b2a_hex(c))
        while self.receiveFiniteStates(c) != 1:
            c = self.port.read(1)
            #print str(binascii.b2a_hex(c))
            attempts += 1
            if attempts * self.interCharTimeout > timeout:
                return 0
        return 1
            
    def recv_ack(self):
        ''' This command should not be used on its own: it is called by the execute commands
            below in a thread safe manner.
        '''
        ack = self.recv(self.timeout)
        return ack == 'OK'

    def execute(self, cmd):
        ''' Thread safe execution of "cmd" on the Stm32 returning a single integer value.
        '''
        self.mutex.acquire()
        
        try:
            self.port.flushInput()
        except:
            pass
        
        ntries = 1
        attempts = 0

        try:
            self.port.write(cmd)
            res = self.recv(self.timeout)
            while attempts < ntries and res !=1 :
                try:
                    self.port.flushInput()
                    self.port.write(cmd)
                    self.receive_state_ = self.WAITING_FF
                    self.receive_check_sum_ = 0
                    self.payload_command = ''
                    self.payload_ack = ''
                    self.payload_args = ''
                    self.payload_len = 0
                    self.byte_count_ = 0
                    res = self.recv(self.timeout)
                    #print "response : " + str(binascii.b2a_hex(res))
                except:
                    print "Exception executing command: " + str(binascii.b2a_hex(cmd))
                attempts += 1
        except:
            self.mutex.release()
            print "Exception executing command: " + str(binascii.b2a_hex(cmd))
            return 0
        
        self.mutex.release()
        return 1
                                 

    def get_baud(self):
        ''' Get the current baud rate on the serial port.
        '''
        cmd_str=struct.pack("4B", self.HEADER0, self.HEADER1, 0x01, 0x00) + struct.pack("B", 0x01)
        if (self.execute(cmd_str))==1 and self.payload_ack == '\x00':
           val, = struct.unpack('I', self.payload_args) #
           return  self.SUCCESS, val 
        else:
           return self.FAIL, 0

    def get_encoder_counts(self):
        cmd_str=struct.pack("4B", self.HEADER0, self.HEADER1, 0x01, 0x02) + struct.pack("B", 0x03)
        if (self.execute(cmd_str))==1 and self.payload_ack == '\x00':
            enc_left_stm32, enc_right_stm32, yawangle_stm32, whetherreach_stm32, voltage_stm32, recharge_ir_data_stm32 = struct.unpack('6H', self.payload_args) #zark
            if yawangle_stm32 > 32768:
                yawangle_stm32 -=65536
            yawangle_stm32 = yawangle_stm32 / 10.0
            # print("voltage", voltage_stm32)
            #print("getencoder:", enc_left_stm32, enc_right_stm32, yawangle_stm32, whetherreach_stm32, voltage_stm32, recharge_ir_data_stm32)
            return  self.SUCCESS, enc_left_stm32, enc_right_stm32, yawangle_stm32, whetherreach_stm32, voltage_stm32, recharge_ir_data_stm32
        else:
            print("getencoder  error!!!")
            return self.FAIL, 0, 0, 0, 0, 0, 0


    def get_emergency_button(self):
        cmd_str=struct.pack("4B", self.HEADER0, self.HEADER1, 0x01, 0x15) + struct.pack("B", 0x16)
        if (self.execute(cmd_str))==1 and self.payload_ack == '\x00':
           emergency_state, _, = struct.unpack('2H', self.payload_args)
           return  self.SUCCESS, emergency_state
        else:
           return self.FAIL, 0

    def reset_encoders(self):
        cmd_str=struct.pack("4B", self.HEADER0, self.HEADER1, 0x01, 0x03) + struct.pack("B", 0x04)
        if (self.execute(cmd_str))==1 and self.payload_ack == '\x00':
           return  self.SUCCESS
        else:
           return self.FAIL

    def get_check_sum(self,list):
        list_len = len(list)
        cs = 0
        for i in range(list_len):
            #print i, list[i]
            cs += list[i]
        cs=cs%255
        return cs

    def drive(self, left, right):
        data1 = struct.pack("h", left)
        d1, d2 = struct.unpack("BB", data1)

        data2 = struct.pack("h", right)
        c1, c2 = struct.unpack("BB", data2)

        self.check_list = [0x05,0x04, d1, d2, c1, c2]
        self.check_num = self.get_check_sum(self.check_list)
        cmd_str=struct.pack("4B", self.HEADER0, self.HEADER1, 0x05, 0x04) + struct.pack("hh", left, right) + struct.pack("B", self.check_num)
        #print("left drive at", left, "right drive at",right) #

        if (self.execute(cmd_str))==1 and self.payload_ack == '\x00':
           return  self.SUCCESS
        else:
           return self.FAIL



    def lidar(self, laser_front, laser_left, laser_back, laser_right):

        data1 = struct.pack("h", laser_front)
        d1, d2 = struct.unpack("BB", data1)
        data2 = struct.pack("h", laser_left)
        c1, c2 = struct.unpack("BB", data2)

        data3 = struct.pack("h", laser_back)
        da1, da2 = struct.unpack("BB", data3)
        data4 = struct.pack("h", laser_right)
        ca1, ca2 = struct.unpack("BB", data4)

        #self.check_list = [0x05,0x04, d1, d2, c1, c2]
        self.check_list = [0x09,0x24, d1, d2, c1, c2, da1, da2, ca1, ca2]

        self.check_num = self.get_check_sum(self.check_list)
        #cmd_str=struct.pack("4B", self.HEADER0, self.HEADER1, 0x05, 0x04) + struct.pack("hh", left, right) + struct.pack("B", self.check_num)
        cmd_str=struct.pack("4B", self.HEADER0, self.HEADER1, 0x09, 0x24) + struct.pack("hhhh", laser_front, laser_left, laser_back, laser_right) + struct.pack("B", self.check_num)
        #print("left drive at", left, "right drive at",right) #
        if (self.execute(cmd_str))==1 and self.payload_ack == '\x00':
           return  self.SUCCESS
        else:
           return self.FAIL





    def drive_angle_distance(self, angle, distance):
        ''' zark set angle and distance
        '''
        data1 = struct.pack("h", angle)
        d1, d2 = struct.unpack("BB", data1)

        data2 = struct.pack("h", distance)
        c1, c2 = struct.unpack("BB", data2)

        self.check_list = [0x05,0x16, d1, d2, c1, c2]
        self.check_num = self.get_check_sum(self.check_list)
        cmd_str=struct.pack("4B", self.HEADER0, self.HEADER1, 0x05, 0x16) + struct.pack("hh", angle, distance) + struct.pack("B", self.check_num)
        print("angle at", angle, "distance at",distance) # zark
        # print("sendcmdad1:", self.getsendcmdad())
        self.clearsendcmdad()
        # print("sendcmdad2:", self.getsendcmdad())
        if (self.execute(cmd_str))==1 and self.payload_ack == '\x00':
            # rospy.loginfo("send success")
            # rospy.loginfo(cmd_str)
            #self.clearsendcmdad()
            return  self.SUCCESS
        else:
            return self.FAIL
        
    def stop(self):
        ''' Stop both motors.
        '''
        self.drive(0, 0)

    def get_firmware_version(self):
        ''' Get the current version of the firmware.
        '''
        cmd_str=struct.pack("4B", self.HEADER0, self.HEADER1, 0x01, 0x01) + struct.pack("B", 0x02)
        if (self.execute(cmd_str))==1 and self.payload_ack == '\x00':
           val0,val1,val2,val3 = struct.unpack('BBBB', self.payload_args)
           return  self.SUCCESS, val0, val1,val2,val3
        else:
           return self.FAIL, -1, -1,-1,-1

    def get_hardware_version(self):
        ''' Get the current version of the hardware.
        '''
        cmd_str=struct.pack("4B", self.HEADER0, self.HEADER1, 0x01, 0x13) + struct.pack("B", 0x14)
        if (self.execute(cmd_str))==1 and self.payload_ack == '\x00':
           #val0,val1,val2,val3 = struct.unpack('BBBB', self.payload_args) #
           val0=0
           val1=1
           val2=0
           val3=1
           return  self.SUCCESS, val0, val1,val2,val3
        else:
           return self.FAIL, -1, -1, -1, -1


    def get_voltage(self):
        ''' Get the current voltage the battery.
        '''
        cmd_str=struct.pack("4B", self.HEADER0, self.HEADER1, 0x01, 0x12) + struct.pack("B", 0x13)
        if (self.execute(cmd_str))==1 and self.payload_ack == '\x00':
           #vol1, vol2, vol3, vol4, vol5, vol6 = struct.unpack('6H', self.payload_args) #
           vol1=1
           vol2=1
           vol3=1
           vol4=1
           vol5=1
           vol6=1
           return  self.SUCCESS, vol1, vol2, vol3, vol4, vol5, vol6
        else:
           return self.FAIL, -1, -1, -1, -1, -1, -1


    def start_automatic_recharge(self):
        ''' start for automatic recharge.
        '''
        cmd_str=struct.pack("6B", self.HEADER0, self.HEADER1, 0x03, 0x10, 0x01, 0x00) + struct.pack("B", 0x14)
        if (self.execute(cmd_str))==1 and self.payload_ack == '\x00':
           print "start recharge"
           return  self.SUCCESS
        else:
           return self.FAIL

    def stop_automatic_recharge(self):
        ''' stop for automatic recharge.
        '''
        cmd_str=struct.pack("6B", self.HEADER0, self.HEADER1, 0x03, 0x10, 0x00, 0x00) + struct.pack("B", 0x13)
        if (self.execute(cmd_str))==1 and self.payload_ack == '\x00':
           print "stop recharge"
           return  self.SUCCESS
        else:
           return self.FAIL

    def get_automatic_recharge_status(self):
        ''' Get the status of automatic recharge.
        '''
        cmd_str=struct.pack("4B", self.HEADER0, self.HEADER1, 0x01, 0x11) + struct.pack("B", 0x12)
        if (self.execute(cmd_str))==1 and self.payload_ack == '\x00':
           val, = struct.unpack('H', self.payload_args)
        #    print("I get recharge status:", val)
           if val == 6:
               self.is_recharge = False
               rospy.loginfo("exit recharge!!")
           return self.SUCCESS, val 
        else:
           return self.FAIL, -1


    def reset_system(self):
        ''' reset system.
        '''
        cmd_str=struct.pack("4B", self.HEADER0, self.HEADER1, 0x01, 0x40) + struct.pack("B", 0x41)
        if (self.execute(cmd_str))==1 and self.payload_ack == '\x00':
           return  self.SUCCESS
        else:
           return self.FAIL




""" Class to receive Twist commands and publish Odometry data """
class BaseController:
    def __init__(self, Stm32, base_frame):
        self.Stm32 = Stm32
        self.base_frame = base_frame
        # self.rate = float(rospy.get_param("~base_controller_rate", 10))
        self.rate = float(rospy.get_param("~rate", 10))
        self.timeout = rospy.get_param("~base_controller_timeout", 1.0)
        self.stopped = False
        self.useImu = rospy.get_param("~useImu", False)
        # self.useSonar = rospy.get_param("~useSonar", False)

        self.wheel_diameter = rospy.get_param("~wheel_diameter", 0.1518)
        self.wheel_track = rospy.get_param("~wheel_track", 0.375)
        self.encoder_resolution = rospy.get_param("~encoder_resolution", 42760)
        self.gear_reduction = rospy.get_param("~gear_reduction", 1.0)
        
        self.accel_limit = rospy.get_param('~accel_limit', 0.1)
        self.motors_reversed = rospy.get_param("~motors_reversed", False)
       
        self.start_rotation_limit_w = rospy.get_param("~start_rotation_limit_w", 0.4) #0.4
        self.start_rotation_limit_w_x0 = rospy.get_param("~start_rotation_limit_w_x0", 0.2) #0.15
        
            
        # How many encoder ticks are there per meter?
        self.ticks_per_meter = self.encoder_resolution * self.gear_reduction  / (self.wheel_diameter * PI)
        
        # What is the maximum acceleration we will tolerate when changing wheel speeds?
        self.max_accel = self.accel_limit * self.ticks_per_meter / self.rate
                
        # Track how often we get a bad encoder count (if any)
        self.bad_encoder_count = 0

        self.encoder_min = rospy.get_param('encoder_min', 0)
        self.encoder_max = rospy.get_param('encoder_max', 65535)
        self.encoder_low_wrap = rospy.get_param('wheel_low_wrap', (self.encoder_max - self.encoder_min) * 0.3 + self.encoder_min )
        self.encoder_high_wrap = rospy.get_param('wheel_high_wrap', (self.encoder_max - self.encoder_min) * 0.7 + self.encoder_min )
        self.l_wheel_mult = 0
        self.r_wheel_mult = 0
                        
        now = rospy.Time.now()    
        self.then = now # time for determining dx/dy
        self.t_delta = rospy.Duration(1.0 / self.rate)
        self.t_next = now + self.t_delta

        # Internal data        
        self.enc_left = None            # encoder readings
        self.enc_right = None
        self.enc_left_last = None            # encoder readings
        self.enc_right_last = None        
        self.x = 0                      # position in xy plane
        self.y = 0
        self.th = 0                     # rotation in radians
        self.v_left = 0
        self.v_right = 0
        self.v_des_left = 0             # cmd_vel setpoint
        self.v_des_right = 0

        self.des_angle = 0    #zark         
        self.des_distance = 0
        #self.sendcmdad = 0
        self.yawangle = 0
        self.yawanglelast = 0
        self.whetherreach = 0
        self.resetencoderflag = False
        self.distancefront = -1
        self.distancefrontPub = rospy.Publisher('distancefront', Int16, queue_size=5)

        self.voltage = 0
        self.vxylast = 0
        self.vthlast = 0

        self.x_last = 0
        self.th_last = 0

        self.last_cmd_vel = now

        # Subscriptions
        rospy.Subscriber("cmd_vel", Twist, self.cmdVelCallback)
        #rospy.Subscriber("smoother_cmd_vel", Twist, self.cmdVelCallback)
        self.robot_cmd_vel_pub = rospy.Publisher('robot_cmd_vel', Twist, queue_size=5)

        rospy.Subscriber("cmd_angle_dis", Twist, self.cmdADCallback) #zark
        # rospy.Subscriber("scan", LaserScan, self.laserCallback) #zark
 
        self.start_ok_pub = rospy.Publisher('car_driver_ok', Int16, queue_size = 5)

        
        # Clear any old odometry info
        self.Stm32.reset_encoders()

        # Set up the odometry broadcaster
        self.odomPub = rospy.Publisher('odom', Odometry, queue_size=5)
        self.odomBroadcaster = TransformBroadcaster()
        
        rospy.loginfo("Started base controller for a base of " + str(self.wheel_track) + "m wide with " + str(self.encoder_resolution) + " ticks per rev")
        rospy.loginfo("Publishing odometry data at: " + str(self.rate) + " Hz using " + str(self.base_frame) + " as base frame")

        self.lEncoderPub = rospy.Publisher('Lencoder', UInt16, queue_size=5)
        self.rEncoderPub = rospy.Publisher('Rencoder', UInt16, queue_size=5)
        self.lVelPub = rospy.Publisher('Lvel', Int16, queue_size=5)
        self.rVelPub = rospy.Publisher('Rvel', Int16, queue_size=5)
        self.yawAnglePub = rospy.Publisher('yaw_angle', Float32, queue_size=5)
        self.whetherreachPub = rospy.Publisher('reach_goal', Int16, queue_size=5)
        #self.Stm32.BEEP_SOUND()

        self.SUCCESS = 0
        self.FAIL = -1

        self.voltage_val = 0
        self.voltage_pub = rospy.Publisher('voltage_value', Int32, queue_size=5)
        self.voltage_percentage_pub = rospy.Publisher('voltage_percentage', Int32, queue_size=5)
        self.voltage_str = ""
        self.voltage_str_pub = rospy.Publisher('voltage_str', String, queue_size=5)
   
        self.emergencybt_val = 0
        self.emergencybt_pub = rospy.Publisher('emergencybt_status', Int16, queue_size=5)
        # self.recharge_ir_pub = rospy.Publisher('recharge_ir_status', Int16, queue_size=5)

        rospy.Subscriber("recharge_handle", Int16, self.handleRechargeCallback)
        self.is_recharge = False
        self.recharge_status = 0
        #0: matching status
        #2: get the handshake signal
        #3: charging
        #4: charging and error 
        #5: battery is full and charge finish 
        self.recharge_Index_control = 0
        self.rechargestatusperiod = 0.1 * self.rate #period is 0.1s self.rate=30
        # print("self.rechargestatusperiod", self.rechargestatusperiod)
        self.rechargestatuscnt = 0
        self.recharge_ir_data = 0
        self.recharge_v_left = 0
        self.recharge_v_right = 0

        self.recharge_status_pub = rospy.Publisher('recharge_status', Int16, queue_size=5)
        self.ir_data_pub = rospy.Publisher('ir_data', Int16, queue_size=5)

        rospy.Subscriber("ware_version_req", Int16, self.reqVersionCallback)
        self.version_pub = rospy.Publisher('ware_version', String, queue_size=5)

        rospy.Subscriber("encoder_reset", Int16, self.resetEncoderCallback)
        rospy.Subscriber("system_reset", Int16, self.resetSystemCallback)

        self.lwheel_ele = 0
        self.rwheel_ele = 0
        self.lwheel_ele_pub = rospy.Publisher('lwheel_ele', Int32, queue_size=5)
        self.rwheel_ele_pub = rospy.Publisher('rwheel_ele', Int32, queue_size=5)


        rospy.Subscriber("driver_enable", Int16, self.enabledriverCallback) #zark
        self.enable_driver_flag = True


        rospy.Subscriber("scan", LaserScan, self.laser_cb) #zark
        self.laser_front = 0
        self.laser_back = 0
        self.laser_left = 0
        self.laser_right = 0


        self.stm32_version=0
        self.slam_project_version = rospy.get_param("~slam_project_version",0)
        rospy.loginfo ("*************************************************")
        rospy.loginfo ("on-bright slam version is "+str(self.slam_project_version))
        rospy.loginfo ("*************************************************")
     

     
        self.start_ok_pub.publish(11) 
        
        
    # def laserCallback(self,data):
    #     cnt = 0
    #     sum = 0
    #     for tempi in range(357, 363):
    #         if(data.ranges[tempi] != 0):
    #             sum += data.ranges[tempi]
    #             cnt += 1
    #     if(cnt != 0):
    #         self.distancefront = float(sum) / cnt * 100
    #         if self.distancefront >= 200:
    #             self.distancefront = -1
    #     else:
    #         self.distancefront = -1
    #     self.distancefrontPub.publish(self.distancefront)
        # print("self.distancefront", self.distancefront)



    def laser_cb(self, data):

        if(data.ranges[0]!=0.0):
            self.laser_front = 100.0 * data.ranges[0]
            #print("self.laser_front", self.laser_front)
        if(data.ranges[1]!=0.0):
            self.laser_front = 100.0 * data.ranges[1]

        if(data.ranges[200]!=0.0):
            self.laser_left = 100.0 * data.ranges[200]
            #print("self.laser_left", self.laser_left)
        if(data.ranges[201]!=0.0):
            self.laser_left = 100.0 * data.ranges[201]
           
        if(data.ranges[400]!=0.0):
            self.laser_back = 100.0 * data.ranges[400]
            #print("self.laser_back", self.laser_back)
        if(data.ranges[401]!=0.0):
            self.laser_back = 100.0 * data.ranges[401]
            
        if(data.ranges[600]!=0.0):
            self.laser_right = 100.0 * data.ranges[600]
            #print("self.laser_right", self.laser_right)
        if(data.ranges[601]!=0.0):
            self.laser_right = 100.0 * data.ranges[601]
            
        print("self.laser_front", self.laser_front)
        print("self.laser_left", self.laser_left)
        print("self.laser_back", self.laser_back)
        print("self.laser_right", self.laser_right)


    def enabledriverCallback(self, data):
        if data.data == 0:
            self.enable_driver_flag = False
        else:
            self.enable_driver_flag = True

    # def car_changeposition(self, req): #obrobot_arm
    #     e=0
    #     a = req.x #ID
    #     b = req.y #angle
    #     c = req.z #distance
    #     rospy.loginfo(".............car change position...............")
    #     rospy.loginfo("cunt= %f",a)  
    #     rospy.loginfo("angle= %f",b)
    #     rospy.loginfo("distance= %f",c)
    #     #if (e<10):
    #     self.Stm32.car_changeposition1(a, b, c)
        #   e+=1

    
    def handleRechargeCallback(self, req):
        ''' send recharge command to the robot
        '''
        if req.data==1:
            rospy.loginfo("robot start searching recharger")
            try:
                if self.is_recharge is False:
                    # res = self.Stm32.start_automatic_recharge()
                    # if res == self.SUCCESS:
                    self.is_recharge = True
                        # self.recharge_Index_control = 1 
            except:
		        rospy.logerr("start automatic recharge exception ")
        else:
            try:
                if self.is_recharge is True:               
                    # res = self.Stm32.stop_automatic_recharge()
                    # if res == self.SUCCESS:
                    self.is_recharge = False
                        # self.recharge_Index_control = 7 
            except:
                rospy.logerr("stop automatic recharge exception ")

    def resetEncoderCallback(self, req):
        if req.data==1:
            try:
                res = self.Stm32.reset_encoders()
                if res==self.FAIL:
                    rospy.logerr("reset encoder failed ")
                else:
                    # zark        
                    self.resetencoderflag = True

            except:
                rospy.logerr("request to reset encoder exception ")

    def resetSystemCallback(self, req):
        if req.data==1:
            try:
                res = self.Stm32.reset_system()
                if res==self.FAIL:
                    rospy.logerr("reset system failed ")
            except:
                    rospy.logerr("request to reset system exception ")
    


    def resetImuCallback(self, req):
        if req.data==1:
            try:
                res = self.Stm32.reset_imu()
                if res==self.FAIL:
                    rospy.logerr("reset imu failed ")
            except:
                rospy.logerr("request to reset imu exception ")

    def reqVersionCallback(self, req):
        if req.data==1:
            try:
                res,ver0,ver1,ver2,ver3 = self.Stm32.get_hardware_version()
                self.version_pub.publish(str(ver0)+"."+str(ver1)+"-"+str(ver2)+"."+str(ver3))
                if res==self.FAIL:
                    rospy.logerr("request the version of hardware failed ")
            except:
                self.version_pub.publish("")
                rospy.logerr("request the version of hardware exception ")
        if req.data==2:
            try:
	        res,ver0,ver1,ver2,ver3 = self.Stm32.get_firmware_version()
		self.version_pub.publish(str(ver0)+"."+str(ver1)+"-"+str(ver2)+"."+str(ver3))
                if res==self.FAIL:
                    rospy.logerr("request the version of firmware failed ")
            except:
		self.version_pub.publish("")
                rospy.logerr("request the version of firmware exception ")

        
    def volTransPerentage(self, vo):
         if(vo == -1):
             return -1;
         if(vo>4.2*7*1000):
             COUNT = 10*1000
         else:
             COUNT = 7*1000

         if(vo >= 4.0*COUNT):
             return 100
         elif(vo >= 3.965*COUNT):
             return 95
         elif(vo >= 3.93*COUNT):
             return 90
         elif(vo >= 3.895*COUNT):
             return 85
         elif(vo >= 3.86*COUNT):
             return 80
         elif(vo >= 3.825*COUNT):
             return 75
         elif(vo >= 3.79*COUNT):
             return 70
         elif(vo >= 3.755*COUNT):
             return 65
         elif (vo >= 3.72*COUNT):
             return 60
         elif (vo >= 3.685*COUNT):
             return 55
         elif (vo >= 3.65*COUNT):
             return 50
         elif (vo >= 3.615*COUNT):
             return 45
         elif (vo >= 3.58*COUNT):
             return 40
         elif (vo >= 3.545*COUNT):
             return 35
         elif (vo >= 3.51*COUNT):
             return 30
         elif (vo >= 3.475*COUNT):
             return 25
         elif (vo >= 3.44*COUNT):
             return 20
         elif (vo >= 3.405*COUNT):
             return 15
         elif (vo >= 3.37*COUNT):
             return 10
         elif (vo >= 3.335*COUNT):
             return 5
         else:
             return 0
        

    def poll(self):
        now = rospy.Time.now()
        # if now > self.t_next:
        if True:
            # try:
            if True:
                stat_,temp1,temp2,temp3,temp4,temp5,temp6 = self.Stm32.get_encoder_counts()
                if stat_ == self.FAIL:
                    return 0
                else:
                    self.enc_left = temp1
                    self.enc_right = temp2
                    self.yawangle = temp3
                    self.whetherreach = temp4
                    self.voltage = temp5
                    self.recharge_ir_data = temp6

                self.lEncoderPub.publish(self.enc_left)
                self.rEncoderPub.publish(self.enc_right)
                self.yawAnglePub.publish(self.yawangle)
                self.whetherreachPub.publish(self.whetherreach)
                self.voltage_pub.publish(self.voltage)
                self.ir_data_pub.publish(self.recharge_ir_data)

                if self.voltage < 106:
                    #print(self.voltage)
                    print("now voltage:", self.voltage/10.0)
                    rospy.logwarn("low voltage!!!")

                if self.is_recharge is True:
                    # print("in recharging!!")
                    self.rechargestatuscnt += 1
                    # print(self.rechargestatuscnt, self.rechargestatusperiod)
                    if self.rechargestatuscnt >= self.rechargestatusperiod:
                        # print("in recharging!!")
                        self.rechargestatuscnt = 0
                        stat_, rechargestatus=self.Stm32.get_automatic_recharge_status()
                        self.recharge_status = rechargestatus
                        self.recharge_status_pub.publish(rechargestatus)
                        # self.recharge_control()

                # else:
                #     if self.voltage < 282:
                #         rospy.logwarn("low voltage!!")

            # except:
            #     self.bad_encoder_count += 1
            #     rospy.logerr("Encoder exception count: " + str(self.bad_encoder_count))
            #     return
         
            dt = now - self.then
            self.then = now
            dt = dt.to_sec()
            
            # Calculate odometry
            if self.enc_left_last == None:
                dright = 0
                dleft = 0
            else:
                if (self.enc_left < self.encoder_low_wrap and self.enc_left_last > self.encoder_high_wrap) :
                    self.l_wheel_mult = + 1     
                elif (self.enc_left > self.encoder_high_wrap and self.enc_left_last < self.encoder_low_wrap) :
                    self.l_wheel_mult = - 1
                else:
                     self.l_wheel_mult = 0
                if (self.enc_right < self.encoder_low_wrap and self.enc_right_last > self.encoder_high_wrap) :
                    self.r_wheel_mult = + 1     
                elif (self.enc_right > self.encoder_high_wrap and self.enc_right_last < self.encoder_low_wrap) :
                    self.r_wheel_mult = - 1
                else:
                     self.r_wheel_mult = 0
                dleft = 1.0 * (self.enc_left + self.l_wheel_mult * (self.encoder_max - self.encoder_min)-self.enc_left_last) / self.ticks_per_meter 
                dright = 1.0 * (self.enc_right + self.r_wheel_mult * (self.encoder_max - self.encoder_min)-self.enc_right_last) / self.ticks_per_meter 

            self.enc_right_last = self.enc_right
            self.enc_left_last = self.enc_left
            
            dxy_ave = (dright + dleft) / 2.0
            vxy = (dxy_ave / dt) * 0.5 + self.vxylast * 0.5
            self.vxylast = vxy
            # dth = (dright - dleft) / self.wheel_track
            # vth = dth / dt
            # zark
            tempvth = (self.yawangle - self.yawanglelast) / 180.0 * math.pi 
            if(tempvth > math.pi):
                tempvth -= 2 * math.pi
            elif(tempvth < -math.pi):
                tempvth += 2 * math.pi

            vth = tempvth / dt
            # vth = (tempvth / dt) * 0.5 + self.vthlast * 0.5
            # self.vthlast = vth

            dth = tempvth
                
            if (dxy_ave != 0):
                dx = cos(dth) * dxy_ave
                dy = -sin(dth) * dxy_ave
                self.x += (cos(self.th) * dx - sin(self.th) * dy)
                self.y += (sin(self.th) * dx + cos(self.th) * dy)
    
            # if (dth != 0):
            #     self.th += dth 
            self.th = self.yawangle / 180.0 * math.pi 
            self.yawanglelast = self.yawangle
    
            quaternion = Quaternion()
            quaternion.x = 0.0 
            quaternion.y = 0.0
            quaternion.z = sin(self.th / 2.0)
            quaternion.w = cos(self.th / 2.0)
            
    
            # Create the odometry transform frame broadcaster.
            if (self.useImu == False) :
                self.odomBroadcaster.sendTransform(
                  (self.x, self.y, 0), 
                  (quaternion.x, quaternion.y, quaternion.z, quaternion.w),
                  rospy.Time.now(),
                  self.base_frame,
                  "odom"
                )

            # print(self.x, self.y, self.yawangle, self.th/3.1415926*180)
    
            odom = Odometry()
            odom.header.frame_id = "odom"
            odom.child_frame_id = self.base_frame
            odom.header.stamp = now
            odom.pose.pose.position.x = self.x
            odom.pose.pose.position.y = self.y
            odom.pose.pose.position.z = 0
            odom.pose.pose.orientation = quaternion
            odom.twist.twist.linear.x = vxy 
            odom.twist.twist.linear.y = 0
            odom.twist.twist.angular.z = vth

            odom.pose.covariance = ODOM_POSE_COVARIANCE
            odom.twist.covariance = ODOM_TWIST_COVARIANCE


            self.odomPub.publish(odom)
            
            if now > (self.last_cmd_vel + rospy.Duration(self.timeout)):
                self.v_des_left = 0
                self.v_des_right = 0
                
            #temp=0.3#目前底层驱动的响应太慢，刹车太慢导致需要减速到零才能在高速情况下转过大弯
            temp=0.4 #0.3#目前底层驱动的响应太慢，刹车太慢导致需要减速到零才能在高速情况下转过大弯
            self.v_left += (self.v_des_left - self.v_left) * temp
            if abs(self.v_des_left - self.v_left) < 1:#cm/s
                self.v_left = self.v_des_left


            temp=0.4 #0.3
            self.v_right += (self.v_des_right - self.v_right) * temp
            if abs(self.v_des_right - self.v_right) < 1:
                self.v_right = self.v_des_right
            

            self.lVelPub.publish(self.v_left)
            self.rVelPub.publish(self.v_right)     
            #rospy.loginfo("polling zark")       

            # zark
            if self.resetencoderflag is True:
                self.resetencoderflag = False
                self.enc_left = None            # encoder readings
                self.enc_right = None
                self.enc_left_last = None            # encoder readings
                self.enc_right_last = None                 
                self.x = 0                      # position in xy plane
                self.y = 0
                self.th = 0                     # rotation in radians
                self.v_left = 0
                self.v_right = 0
                self.v_des_left = 0             # cmd_vel setpoint
                self.v_des_right = 0
                self.l_wheel_mult = 0
                self.r_wheel_mult = 0
                rospy.loginfo("reset encoder success ")

            # Set motor speeds in encoder ticks per PID loop
            # if not self.stopped:
            '''if (not self.stopped):  #3.7 jinliang 
                # zark
                #rospy.loginfo("not stop zark")
                if self.Stm32.getsendcmdad() == 1:
                    self.Stm32.drive_angle_distance(self.des_angle, self.des_distance)
                else:
                    if (self.enable_driver_flag is True):
                        self.Stm32.drive(int(self.v_left), int(self.v_right))'''
                

            # Set motor speeds in encoder ticks per PID loop
            # if not self.stopped:
            '''if ((not self.stopped) and (not self.is_recharge)):  #3.7 jinliang 
                self.Stm32.drive(int(self.v_left), int(self.v_right))'''


            if ((not self.stopped) and (not self.is_recharge)):  #3.7 jinliang 
                self.Stm32.lidar(int(self.laser_front), int(self.laser_left), int(self.laser_back), int(self.laser_right))



            self.t_next = now + self.t_delta
            
    def stop(self):
        self.stopped = True
        self.Stm32.drive(0, 0)

    def isPassedCallback(self, msg): 
        if(msg.data>2):
            self.isPassed = False
        else:
            self.isPassed = True

    def isPassedCallback_2(self, msg):
        if(msg.data>2):
            self.isPassed_2 = False
        else:
            self.isPassed_2 = True
            
    def cmdVelCallback(self, req):
        # Handle velocity-based movement requests
        self.last_cmd_vel = rospy.Time.now()
        
        robot_cmd_vel = Twist()
        x = req.linear.x         # m/s
        th = req.angular.z       # rad/s

        if th > 0 and th < 0.4:
            th = 0.4
        if th < 0 and th > -0.4:
            th = -0.4


        if self.emergencybt_val==1:
            robot_cmd_vel.linear.x = 0
            robot_cmd_vel.linear.y = 0
            robot_cmd_vel.angular.z = 0
        else:
            robot_cmd_vel.linear.x = x
            robot_cmd_vel.linear.y = 0
            robot_cmd_vel.angular.z = th
        self.robot_cmd_vel_pub.publish(robot_cmd_vel)


        left = x - th * self.wheel_track  * self.gear_reduction / 2.0
        right = x + th * self.wheel_track  * self.gear_reduction / 2.0


        self.v_des_left = 100 * left; #cm/s
        self.v_des_right = 100 * right; 

    
    
    def cmdADCallback(self, req):
       # zark
        rospy.loginfo("callback zark")
        x = req.linear.x         # cm
        th = req.angular.z       # 0.1deg

        self.des_distance = x
        self.des_angle = th

        if self.Stm32.getsendcmdad() == 0:
            # rospy.loginfo("set sendcmdad")
            self.Stm32.setsendcmdad()
        



class Stm32ROS():
    def __init__(self):
        rospy.init_node('ob_car_node', log_level=rospy.DEBUG)
                
        # Cleanup when termniating the node
        rospy.on_shutdown(self.shutdown)
        
        self.port = rospy.get_param("~port", "/dev/ttyUSB1")
        self.baud = int(rospy.get_param("~baud", 115200))
        self.timeout = rospy.get_param("~timeout", 0.5)
        self.base_frame = rospy.get_param("~base_frame", 'base_link')

        # Overall loop rate: should be faster than fastest sensor rate
        self.rate = int(rospy.get_param("~rate", 50))
        r = rospy.Rate(self.rate)

        # Rate at which summary SensorState message is published. Individual sensors publish
        # at their own rates.        
        self.sensorstate_rate = int(rospy.get_param("~sensorstate_rate", 10))
        
        self.use_base_controller = rospy.get_param("~use_base_controller", True)
        
        
        # Set up the time for publishing the next SensorState message
        now = rospy.Time.now()
        self.t_delta_sensors = rospy.Duration(1.0 / self.sensorstate_rate)
        self.t_next_sensors = now + self.t_delta_sensors
        
        # Initialize a Twist message
        self.cmd_vel = Twist()
  
        # A cmd_vel publisher so we can stop the robot when shutting down
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=5)
        
        # Initialize the controlller
        self.controller = Stm32(self.port, self.baud, self.timeout)
        
        # Make the connection
        self.controller.connect()
        
        rospy.loginfo("Connected to mcu on port " + self.port + " at " + str(self.baud) + " baud")
     
        # Reserve a thread lock
        mutex = thread.allocate_lock()
              
        # Initialize the base controller if used
        if self.use_base_controller:
            self.myBaseController = BaseController(self.controller, self.base_frame)
    
        # Start polling the sensors and base controller
        while not rospy.is_shutdown():
                    
            if self.use_base_controller:
                mutex.acquire()
                self.myBaseController.poll()
                #rospy.loginfo("poll test")
                mutex.release()
            r.sleep()
    
    def shutdown(self):
        # Stop the robot
        try:
            rospy.loginfo("Stopping the robot...")
            self.cmd_vel_pub.Publish(Twist())
            rospy.sleep(2)
        except:
            pass
        rospy.loginfo("Shutting down ob_car_node Node...")
        
if __name__ == '__main__':
    myStm32 = Stm32ROS()
