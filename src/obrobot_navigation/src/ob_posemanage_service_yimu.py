#!/usr/bin/env python
import rospy
import os,sys
import json
import getpass

from obrobot_navigation.srv import *
from geometry_msgs.msg import Pose
from obrobot_navigation.msg import PoseDefine
import tf

    
# print(load_dict['floor'][0]['destination'][0]['pose']['position']['x'])

#select function
def select_posemanage(dict_source,dict_pose):

    flag_floor_exit = False #detect the right floor

    for i in xrange(len(dict_source['floor'])):
        list_floor=dict_source['floor'][i]

        if list_floor['floor_id'] == dict_pose['floor_id']:
            
            flag_floor_exit = True
            flag_pos_exit = False

            for j in xrange(len(list_floor['destination'])):
                list_destination=dict_source['floor'][i]['destination'][j]

                if list_destination['id'] == dict_pose['id']:
                    flag_pos_exit = True # pos id is exit
                    dict_pose=list_destination
                    dict_pose['floor_id']=list_floor['floor_id']
                    flag_status = "SUCCESS: floor aleady existed,select pose"
                    break#

            if flag_pos_exit == False:
                flag_status = "FAIL: floor existed, pose does not exist"
                break
    if flag_floor_exit == False:
        flag_status = "FAIL: floor does not existed"

    return flag_status,dict_source,dict_pose

#delete function
def delete_posemanage(dict_source,dict_pose):

    flag_floor_exit = False #detect the right floor

    for i in xrange(len(dict_source['floor'])):
        list_floor=dict_source['floor'][i]

        if list_floor['floor_id'] == dict_pose['floor_id']:
            
            flag_floor_exit = True
            flag_pos_exit = False

            for j in xrange(len(list_floor['destination'])):
                list_destination=dict_source['floor'][i]['destination'][j]

                if list_destination['id'] == dict_pose['id']:
                    flag_pos_exit = True # pos id is exit
                    list_floor['destination'].pop(j)
                    flag_status = "SUCCESS: floor aleady existed,delete pose"
                    break#

            if flag_pos_exit == False:
                flag_status = "FAIL: floor aleady existed, pose does not exit"
                break
    if flag_floor_exit == False:
        flag_status = "FAIL: floor does not existed"

    return flag_status,dict_source,dict_pose

#update function
def update_posemanage(dict_source,dict_pose):

    flag_floor_exit = False #detect the right floor

    for i in xrange(len(dict_source['floor'])):
        list_floor=dict_source['floor'][i]

        if list_floor['floor_id'] == dict_pose['floor_id']:
            
            flag_floor_exit = True
            flag_pos_exit = False

            for j in xrange(len(list_floor['destination'])):
                list_destination=dict_source['floor'][i]['destination'][j]

                if list_destination['id'] == dict_pose['id']:
                    flag_pos_exit = True # pos id is exit
                    dict_pose_insert=dict_pose.copy()
                    dict_pose_insert.pop('floor_id')
                    list_floor['destination'].insert(j,dict_pose_insert)
                    list_floor['destination'].pop(j+1)
                    flag_status = "SUCCESS: floor aleady existed,update pose"
                    break#

            if flag_pos_exit == False:
                # dict_pose_insert=dict_pose.copy()
                # dict_pose_insert.pop('floor_id')
                # list_floor['destination'].append(dict_pose_insert)
                flag_status = "FAIL: floor aleady existed, pose does not exit"
                break
    if flag_floor_exit == False:

        # dict_pose_insert=dict_pose.copy()
        # dict_pose_insert.pop('floor_id')
        # dict_floor={
        #     'map_md5': "map_md5", 
        #     'floor_id': dict_pose['floor_id'], 
        #     'destination': [dict_pose_insert]
        # }
        # dict_source['floor'].append(dict_floor)
        flag_status = "FAIL: floor does not existed"

    return flag_status,dict_source,dict_pose

#insert function
def insert_posemanage(dict_source,dict_pose):

    flag_floor_exit = False #detect the right floor

    for i in xrange(len(dict_source['floor'])):
        list_floor=dict_source['floor'][i]

        if list_floor['floor_id'] == dict_pose['floor_id']:
            
            flag_floor_exit = True
            flag_pos_exit = False

            for j in xrange(len(list_floor['destination'])):
                list_destination=dict_source['floor'][i]['destination'][j]

                if list_destination['id'] == dict_pose['id']:
                    flag_pos_exit = True # pos id is exit
                    break
            if flag_pos_exit == False:
                dict_pose_insert=dict_pose.copy()
                dict_pose_insert.pop('floor_id')
                list_floor['destination'].append(dict_pose_insert)
                flag_status = "SUCCESS: floor aleady existed,insert new pose"
            else:
                flag_status = "FAIL: pos aleady existed"
                break
    if flag_floor_exit == False:

        dict_pose_insert=dict_pose.copy()
        dict_pose_insert.pop('floor_id')
        dict_floor={
            'map_md5': "map_md5", 
            'floor_id': dict_pose['floor_id'], 
            'destination': [dict_pose_insert]
        }
        dict_source['floor'].append(dict_floor)
        flag_status = "SUCCESS: floor does not existed,insert new floor and pose"

    return flag_status,dict_source,dict_pose

def handle_posemanage(req):

    #test code
    posdefine = PoseDefine()

    if req.poseoperation.opt !="insert" and req.poseoperation.opt !="delete" and req.poseoperation.opt !="select" and req.poseoperation.opt !="update":
        return PoseManageResponse("Status: FAIL: Unkown Command, please use 'insert, delete, select or update'",posdefine)

    # zark
    if (req.poseoperation.opt =="insert") and (req.poseoperation.type != "charge" and req.poseoperation.type != "normal" and req.poseoperation.type != "origin" and req.poseoperation.type != ""):
        return PoseManageResponse("Status: FAIL: Unkown Type, please use 'charge, origin or normal'",posdefine)
    
    if (req.poseoperation.opt =="update") and (req.poseoperation.type != "charge" and req.poseoperation.type != "normal" and req.poseoperation.type != "origin" and req.poseoperation.type != ""):
        return PoseManageResponse("Status: FAIL: Unkown Type, please use 'charge, origin or normal'",posdefine)

    if (req.poseoperation.opt =="insert") and (req.poseoperation.type == ""):
        req.poseoperation.type = "normal"

    if (req.poseoperation.opt =="insert") and (req.poseoperation.name == ""):
        req.poseoperation.name = "pos" + str(req.poseoperation.id)

    if (req.poseoperation.id == 1304):
        req.poseoperation.type = "charge"
        req.poseoperation.name = "chargepose"

    if (req.poseoperation.id == 1302):
        req.poseoperation.type = "origin"
        req.poseoperation.name = "originpose"

    posdefine.id = req.poseoperation.id
    posdefine.name=req.poseoperation.name
    posdefine.type=req.poseoperation.type
    posdefine.floor=req.poseoperation.floor
    
    rospy.loginfo("waitForTransform")
    tflistener = tf.TransformListener()
    tflistener.waitForTransform("/map", "/base_footprint", rospy.Time(), rospy.Duration(60))
    (_trans, _rot) = tflistener.lookupTransform("/map", "/base_footprint", rospy.Time(0))
    posdefine.pose.position.x = _trans[0]
    posdefine.pose.position.y = _trans[1]
    posdefine.pose.position.z = 0    
    posdefine.pose.orientation.x = _rot[0]
    posdefine.pose.orientation.y = _rot[1]
    posdefine.pose.orientation.z = _rot[2]
    posdefine.pose.orientation.w = _rot[3]
    
    # # #test code
    # posdefine.pose.position.x = 1
    # posdefine.pose.position.y = 2
    # posdefine.pose.position.z = 0    
    # posdefine.pose.orientation.x = 3
    # posdefine.pose.orientation.y = 4
    # posdefine.pose.orientation.z = 5
    # posdefine.pose.orientation.w = 6

    dict_pos_={
               'floor_id' : posdefine.floor,
               'id' : posdefine.id,
               'id_type' : posdefine.type,
               'name' : posdefine.name,
               'pose' : {
                  'orientation' : {
                     'w' : posdefine.pose.orientation.w,
                     'x' : posdefine.pose.orientation.x,
                     'y' : posdefine.pose.orientation.y,
                     'z' : posdefine.pose.orientation.z
                  },
                  'position' : {
                     'x' : posdefine.pose.position.x,
                     'y' : posdefine.pose.position.y,
                     'z' : posdefine.pose.position.z
                  }
               }
            }

    with open("/home/" + getpass.getuser() + "/.ob/pos/test.json",'r') as f:
        load_dict = json.load(f)
        f.close()

    if req.poseoperation.opt =="insert":
        
        flag_status,load_dict,dict_pos_=insert_posemanage(load_dict,dict_pos_)
        if "SUCCESS" in flag_status:
            with open("/home/" + getpass.getuser() + "/.ob/pos/test.json","w") as f:
                json.dump(load_dict,f,indent=4)
                f.close()
    elif req.poseoperation.opt =="delete":

        flag_status,load_dict,dict_pos_=delete_posemanage(load_dict,dict_pos_)
        if "SUCCESS" in flag_status:
            with open("/home/" + getpass.getuser() + "/.ob/pos/test.json","w") as f:
                json.dump(load_dict,f,indent=4)
                f.close()

    elif req.poseoperation.opt =="select":
        
        flag_status,load_dict,dict_pos_=select_posemanage(load_dict,dict_pos_)

    elif req.poseoperation.opt =="update":   
        
        # zark
        flag_status,load_dict,dict_pos_1=select_posemanage(load_dict,dict_pos_)
        if req.poseoperation.name == '':
            dict_pos_['name']=dict_pos_1['name']

        if req.poseoperation.type == '':
            dict_pos_['id_type']=dict_pos_1['id_type']
            
        flag_status,load_dict,dict_pos_=update_posemanage(load_dict,dict_pos_)
        if "SUCCESS" in flag_status:
            with open("/home/" + getpass.getuser() + "/.ob/pos/test.json","w") as f:
                json.dump(load_dict,f,indent=4)
                f.close()

    # print("flag_status" +flag_status)
    # print(json.dumps(dict_pos_))


    posdefine.id = dict_pos_['id']
    posdefine.name=dict_pos_['name']
    posdefine.type=dict_pos_['id_type']
    posdefine.floor=dict_pos_['floor_id']
    posdefine.pose.position.x = dict_pos_['pose']['position']['x']
    posdefine.pose.position.y = dict_pos_['pose']['position']['y']
    posdefine.pose.position.z = dict_pos_['pose']['position']['z']    
    posdefine.pose.orientation.x = dict_pos_['pose']['orientation']['x']
    posdefine.pose.orientation.y = dict_pos_['pose']['orientation']['y']
    posdefine.pose.orientation.z = dict_pos_['pose']['orientation']['z']
    posdefine.pose.orientation.w = dict_pos_['pose']['orientation']['w']
    return PoseManageResponse("Status: "+flag_status,posdefine)
    
def posemanage_server():
    rospy.init_node("posemanage_server",anonymous=True)
    s = rospy.Service("posemanage_server",PoseManage,handle_posemanage)
    print"Ready to posemanage_server."
    rospy.spin()

if __name__=='__main__':
    posemanage_server()   
