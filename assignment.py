from __future__ import print_function
from cmath import cos

import time
import math
from sr.robot import *

R = Robot()
a_th = 2.0
d_th = 0.4
count=0
silver = True
def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_silver_token():
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:
            dist=token.dist
            rot_y=token.rot_y
    if dist==100:
       return -1, -1
    else:
       return dist, rot_y

def find_golden_token():

    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
            dist=token.dist
            rot_y=token.rot_y
    if dist==100:
        return -1, -1
    else:
        return dist, rot_y

while 1:
    if silver == True: # if silver is True, look for the silver token
        dist, rot_y = find_silver_token() #adquire the distance and rotation of the silver token detected
        if dist <d_th: # if we are close to the token, we try grab it.
           print("Found it!")
           if R.grab(): # if we grab the token, we move the robot forward and on the right, we release the token, and we go back to the initial position
                print("Gotcha!")
                turn(30,1)
                silver = not silver # modify the silver value, to do the next task: release the token
           else:
                print("Aww, I'm not close enough.")
        if -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
            print("Ah, that'll do.")
            drive(40, 0.5)
        elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
            print("Left a bit...")
            turn(-2, 0.5)
        elif rot_y > a_th:
            print("Right a bit...")
            turn(+2, 0.5)
    if silver == False: # if silver is False, look for the golden token to release
        dist, rot_y = find_golden_token()  #adquire the distance and rotation of the silver token detected
        print(dist)
        if dist <d_th*1.5: # the distance to release the token should be 1.5 greater than the distance to pick the token, to avoid push the tokens
           print("Found it!")
           if R.release(): # if the token is released, move away from the token to look for the next silver token
                print("release token")
                drive(-20,2)
                turn(-50, 1)
                count=count+1# A counter is required to do the task 6 times
                silver = not silver #To go back to search the silver token, the silver value change again to the True state
           else:
             print("Aww, I'm not close enough.")
        if -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
            print("Ah, that'll do.")
            drive(40, 0.5)
        elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
            print("Left a bit...")
            turn(-2, 0.5)
        elif rot_y > a_th:
            print("Right a bit...")
            turn(+2, 0.5)
        if count==6:#if the counter is equal to 6, it have to stop the simulation and exit the program
            exit()   