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

clientID = vrep.simxStart('127.0.0.1', 19998, True, True, 5000, 5)  # Connect to V-REP

if clientID != -1:
    print('Connected to remote API server')

else:
    sys.exit('Failed connecting to remote API server')

# handles
errorCode, car = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx',
                                                          vrep.simx_opmode_blocking)
print("Car", car, errorCode)
errorCode, left_motor_handle = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_leftMotor',
                                                          vrep.simx_opmode_blocking)
print("Car leftJoint", left_motor_handle, errorCode)
errorCode, right_motor_handle = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_rightMotor',
                                                           vrep.simx_opmode_blocking)
print("Car rightJoint", right_motor_handle, errorCode)

# init sensors
sensors_dist = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
for i in range(16):
    errorCode, sensors_dist[i] = vrep.simxGetFloatSignal(clientID, 'Sensor_{}'.format(i), vrep.simx_opmode_streaming)

# sample codes
braitenbergL = [-0.2, -0.4, -0.6, -0.8, -1, -1.2, -1.4, -1.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
braitenbergR = [-1.6, -1.4, -1.2, -1, -0.8, -0.6, -0.4, -0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

while 1:
    for i in range(16):
        errorCode, sensors_dist[i] = vrep.simxGetFloatSignal(clientID, 'Sensor_{}'.format(i), vrep.simx_opmode_buffer)
    print(sensors_dist[1], sensors_dist[6], sensors_dist[3], sensors_dist[4])

    if sensors_dist[1] == 0 and (sensors_dist[3] == 0 or sensors_dist[4] == 0):
        vLeft = 0.5
        vRight = 1
    elif sensors_dist[3] > 0 or sensors_dist[4] > 0:
        if sensors_dist[6] == 0 and sensors_dist[1] > 0:
            vLeft = 1
            vRight = 0
        elif sensors_dist[1] > 0 and sensors_dist[6] > 0:
            vLeft = 1
            vRight = -1
    else:
        vLeft = 1.5 - sensors_dist[6]
        vRight = 1.5 - sensors_dist[1]

    errorCode = vrep.simxSetJointTargetVelocity(clientID, left_motor_handle, vLeft, vrep.simx_opmode_oneshot)
    errorCode = vrep.simxSetJointTargetVelocity(clientID, right_motor_handle, vRight, vrep.simx_opmode_oneshot)
    time.sleep(0.1)
