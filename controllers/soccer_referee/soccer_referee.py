"""Supervisor controller"""

from controller import Supervisor
from controller import Emitter
import struct

# Supervisor setup

supervisor = Supervisor()
TIMESTEP = int(supervisor.getBasicTimeStep())
COMMUNICATION_CHANNEL = -1
ball_radius = 0.113

# Supervisor interpret world
soccerball = supervisor.getFromDef("BALL")
trans_field = soccerball.getField("translation")
INITIAL_TRANS = [0, ball_radius, 0]

# Emitter setup

emitter = supervisor.getEmitter('emitter')
emitter.setChannel(COMMUNICATION_CHANNEL)
timeLastMessage = -1

while supervisor.step(TIMESTEP) != -1:

    values = trans_field.getSFVec3f()

    # Emit ball position
    if supervisor.getTime() > timeLastMessage + 1:
        message = struct.pack("ddd", values[0], values[1], values[2])
        emitter.send(message)
        timeLastMessage = int(supervisor.getTime())
    
    # determine out of bounds64
    if values[0] > 5:
        trans_field.setSFVec3f([5, ball_radius, values[2]])
        soccerball.resetPhysics()
    elif values[0] < -5:
        trans_field.setSFVec3f([-5, ball_radius, values[2]])
        soccerball.resetPhysics()
    elif values[2] > 3:
        trans_field.setSFVec3f([values[0], ball_radius, 3])
        soccerball.resetPhysics()
    elif values[2] < -3:
        trans_field.setSFVec3f([values[0], ball_radius, -3])
        soccerball.resetPhysics()
        
    if (values[2] > 0.75) or (values[2] < -0.75):
        if (values[0] > 4.5):
            trans_field.setSFVec3f([4.5, ball_radius, values[2]])
            soccerball.resetPhysics()
        elif (values[0] < -4.5):
            trans_field.setSFVec3f([-4.5, ball_radius, values[2]])
            soccerball.resetPhysics()
    # determine in goal
    if ((values[2] < 0.75) and (values[2] >-0.75)):
        if ((values[0] > 4.5) and (values[0] < 5)) or ((values[0] < -4.5) and (values[0] > -5)):
            trans_field.setSFVec3f(INITIAL_TRANS)
            soccerball.resetPhysics()



""" from controller import Supervisor
import struct
from controller import Emitter

supervisor = Supervisor()
TIME_STEP = int(supervisor.getBasicTimeStep())
COMMUNICATION_CHANNEL = 1

# do this once only
soccer_ball = supervisor.getFromDef("BALL")
trans_field = soccer_ball.getField("translation")
soccerball_radius = 0.113
INITIAL_TRANS = [0, soccerball_radius, 0]
#ball_radius = robot_node.getField("radius")


emitter = supervisor.getEmitter('emitter')
emitter.setChannel(COMMUNICATION_CHANNEL)
tInitial = supervisor.getTime()
timeLastMsg = -1

while supervisor.step(TIME_STEP) != -1:

    # this is done repeatedly
    values = trans_field.getSFVec3f()
    t = supervisor.getTime()

    # Emit ball position
    if(t-tInitial) >=1: #supervisor.getTime() > timeLastMsg + 1:
        message = struct.pack("ddd", values[0], values[1], values[2])
        emitter.send(message)
        time_difference = 1-(t-tInitial)
        #timeLastMsg = int(supervisor.getTime())
        print("BALL is at position: %g %g %g" % (values[0], values[1], values[2]))

    #check if ball is going in goal or ut of boundaries
    if ((values[0]>4.5 and values[2]>-0.75 and values[2]<0.75) or (values[0]<-4.5 and values[2]>-0.75 and values[2]<0.7)):
        INITIAL = [0, soccerball_radius, 0]
        trans_field.setSFVec3f(INITIAL)
        soccer_ball.resetPhysics()
    elif( values[0]>4.5):
        trans_field.setSFVec3f([4.5, soccerball_radius, values[2]])
        soccer_ball.resetPhysics()
    elif( values[0]<-4.5):
        trans_field.setSFVec3f([-4.5, soccerball_radius, values[2]])
        soccer_ball.resetPhysics()
    elif( values[2]>3):
        trans_field.setSFVec3f([values[0], soccerball_radius, 3])
        soccer_ball.resetPhysics()
    elif( values[2]<-3):
        trans_field.setSFVec3f([values[0], soccerball_radius, -3])
        soccer_ball.resetPhysics()



 """