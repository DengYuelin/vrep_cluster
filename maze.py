# Make sure to have the server side running in V-REP:
# in a child script of a V-REP scene, add following command
# to be executed just once, at simulation start:
#
# simRemoteApi.start(19999)
#
# then start simulation, and run this program.

import vrep
import sys
import time

print('Program started')
vrep.simxFinish(-1)  # just in case, close all opened connections

clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)  # Connect to V-REP

if clientID != -1:
    print('Connected to remote API server')

else:
    sys.exit('Failed connecting to remote API server')

# handles
errorCode, car = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx#0',
                                                          vrep.simx_opmode_blocking)
print("Car", car, errorCode)
errorCode, left_motor_handle = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_leftMotor#0',
                                                          vrep.simx_opmode_blocking)
print("Car leftJoint", left_motor_handle, errorCode)
errorCode, right_motor_handle = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_rightMotor#0',
                                                           vrep.simx_opmode_blocking)
print("Car rightJoint", right_motor_handle, errorCode)

# init sensors
sensors_dist = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
for i in range(16):
    errorCode, sensors_dist[i] = vrep.simxGetFloatSignal(clientID, 'Sensor_{}'.format(i), vrep.simx_opmode_streaming)

# sample codes
v0 = 2
braitenbergL = [-0.2, -0.4, -0.6, -0.8, -1, -1.2, -1.4, -1.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
braitenbergR = [-1.6, -1.4, -1.2, -1, -0.8, -0.6, -0.4, -0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

while 1:
    for i in range(16):
        errorCode, sensors_0_dist[i] = vrep.simxGetFloatSignal(clientID, 'Sensor_0_{}'.format(i), vrep.simx_opmode_buffer) #读传感器信息
    # print(sensors_0_dist)
    errorCode, car0_pos = vrep.simxGetObjectPosition(clientID, -1, vrep.simx_opmode_buffer)
    errorCode, car0_dir = vrep.simxGetObjectOrientation(clientID, -1, vrep.simx_opmode_buffer)
    # print("Car 0 position:", errorCode, car0_pos)
    print("Car 0 orientation:", errorCode, car0_dir)
    vLeft_0 = v0
    vRight_0 = v0

    for i in range(16):
        vLeft_0 = vLeft_0 + braitenbergL[i] * sensors_dist[i]
        vRight_0 = vRight_0 + braitenbergR[i] * sensors_dist[i]

    errorCode = vrep.simxSetJointTargetVelocity(clientID, left_motor_handle, vLeft_0, vrep.simx_opmode_oneshot) #电机速度
    errorCode = vrep.simxSetJointTargetVelocity(clientID, right_motor_handle, vRight_0, vrep.simx_opmode_oneshot)
    time.sleep(0.5)
