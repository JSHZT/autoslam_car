// Auto-generated. Do not edit!

// (in-package obrobot_navigation.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let PoseOperation = require('../msg/PoseOperation.js');

//-----------------------------------------------------------

let PoseDefine = require('../msg/PoseDefine.js');

//-----------------------------------------------------------

class PoseManageRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.poseoperation = null;
    }
    else {
      if (initObj.hasOwnProperty('poseoperation')) {
        this.poseoperation = initObj.poseoperation
      }
      else {
        this.poseoperation = new PoseOperation();
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type PoseManageRequest
    // Serialize message field [poseoperation]
    bufferOffset = PoseOperation.serialize(obj.poseoperation, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type PoseManageRequest
    let len;
    let data = new PoseManageRequest(null);
    // Deserialize message field [poseoperation]
    data.poseoperation = PoseOperation.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += PoseOperation.getMessageSize(object.poseoperation);
    return length;
  }

  static datatype() {
    // Returns string type for a service object
    return 'obrobot_navigation/PoseManageRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '1c9db663067220fe547812392b537bd8';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    obrobot_navigation/PoseOperation poseoperation
    
    ================================================================================
    MSG: obrobot_navigation/PoseOperation
    string opt
    uint32 id
    string name
    string type
    uint32 floor
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new PoseManageRequest(null);
    if (msg.poseoperation !== undefined) {
      resolved.poseoperation = PoseOperation.Resolve(msg.poseoperation)
    }
    else {
      resolved.poseoperation = new PoseOperation()
    }

    return resolved;
    }
};

class PoseManageResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.status = null;
      this.posedefine = null;
    }
    else {
      if (initObj.hasOwnProperty('status')) {
        this.status = initObj.status
      }
      else {
        this.status = '';
      }
      if (initObj.hasOwnProperty('posedefine')) {
        this.posedefine = initObj.posedefine
      }
      else {
        this.posedefine = new PoseDefine();
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type PoseManageResponse
    // Serialize message field [status]
    bufferOffset = _serializer.string(obj.status, buffer, bufferOffset);
    // Serialize message field [posedefine]
    bufferOffset = PoseDefine.serialize(obj.posedefine, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type PoseManageResponse
    let len;
    let data = new PoseManageResponse(null);
    // Deserialize message field [status]
    data.status = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [posedefine]
    data.posedefine = PoseDefine.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += object.status.length;
    length += PoseDefine.getMessageSize(object.posedefine);
    return length + 4;
  }

  static datatype() {
    // Returns string type for a service object
    return 'obrobot_navigation/PoseManageResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '3ee0d3f1402669f95ae05bb612a861fa';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string status
    obrobot_navigation/PoseDefine posedefine
    
    
    ================================================================================
    MSG: obrobot_navigation/PoseDefine
    uint32 id
    string name
    string type
    uint32 floor
    geometry_msgs/Pose pose
    
    ================================================================================
    MSG: geometry_msgs/Pose
    # A representation of pose in free space, composed of position and orientation. 
    Point position
    Quaternion orientation
    
    ================================================================================
    MSG: geometry_msgs/Point
    # This contains the position of a point in free space
    float64 x
    float64 y
    float64 z
    
    ================================================================================
    MSG: geometry_msgs/Quaternion
    # This represents an orientation in free space in quaternion form.
    
    float64 x
    float64 y
    float64 z
    float64 w
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new PoseManageResponse(null);
    if (msg.status !== undefined) {
      resolved.status = msg.status;
    }
    else {
      resolved.status = ''
    }

    if (msg.posedefine !== undefined) {
      resolved.posedefine = PoseDefine.Resolve(msg.posedefine)
    }
    else {
      resolved.posedefine = new PoseDefine()
    }

    return resolved;
    }
};

module.exports = {
  Request: PoseManageRequest,
  Response: PoseManageResponse,
  md5sum() { return 'ced5f2372deedb2a41f03ed0ae9a8337'; },
  datatype() { return 'obrobot_navigation/PoseManage'; }
};
