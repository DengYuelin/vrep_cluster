# Make sure to have the server side running in V-REP:
# in a child script of a V-REP scene, add following command
# to be executed just once, at simulation start:
#
# simRemoteApi.start(19999)
#
# then start simulation, and run this program.

import vrep
import sys
import numpy as np

print('Program started')
vrep.simxFinish(-1)  # just in case, close all opened connections

clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)  # Connect to V-REP

if clientID != -1:
    print('Connected to remote API server')

else:
    sys.exit('Failed connecting to remote API server')

errorCode, left_motor_handle = vrep.simxGetObjectHandle(clientID, 'dr12_leftJoint_', vrep.simx_opmode_blocking)
print("dr12_leftJoint_", errorCode, left_motor_handle)
errorCode, right_motor_handle = vrep.simxGetObjectHandle(clientID, 'dr12_rightJoint_', vrep.simx_opmode_blocking)
print("dr12_rightJoint_", errorCode, right_motor_handle)
errorCode, force_sensor_handle = vrep.simxGetObjectHandle(clientID, 'Force_sensor', vrep.simx_opmode_blocking)
print("Force_sensor", errorCode, force_sensor_handle)

errorCode, forceState, forceVector, torqueVector = vrep.simxReadForceSensor(clientID, force_sensor_handle,
                                                                            vrep.simx_opmode_streaming)
print("init force sensor", errorCode, forceState, forceVector, torqueVector)
timer = 0
while 1:
    errorCode, forceState, forceVector, torqueVector = vrep.simxReadForceSensor(clientID, force_sensor_handle,
                                                                                vrep.simx_opmode_buffer)
    if forceState > 0:
        if (np.abs(forceVector[1]) > 1) or (np.abs(forceVector[2]) > 1):
            print("force sensor data", errorCode, forceState, forceVector, torqueVector)
            timer = 1000

    if timer > 0:
        vrep.simxSetJointTargetVelocity(clientID, left_motor_handle, -50 * np.pi / 180, vrep.simx_opmode_streaming)
        vrep.simxSetJointTargetVelocity(clientID, right_motor_handle, -25 * np.pi / 180, vrep.simx_opmode_streaming)
        timer -= 1
    else:
        vrep.simxSetJointTargetVelocity(clientID, left_motor_handle, 50 * np.pi / 180, vrep.simx_opmode_streaming)
        vrep.simxSetJointTargetVelocity(clientID, right_motor_handle, 50 * np.pi / 180, vrep.simx_opmode_streaming)
