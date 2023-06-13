import os
from psychopy import core, data, event, gui, misc, sound, visual

monSize = [800, 600]

#Window.
wintype='pyglet'
#instruct = visual.TextStim(win, text='Text', alignHoriz = 'center', height = 0.12, wrapWidth = 350, color = 'white')
#win = visual.Window([600,400], fullscr=info, allowGUI = False, monitor = 'MacAir', color = 'black', winType=wintype) #check window here
#left_choice = visual.Circle(win, radius = 0.3, lineColor = 'ForestGreen', lineWidth = 2.0, pos = [-0.4,0])
#right_choice = visual.Circle(win, radius = 0.3, lineColor = 'ForestGreen', lineWidth = 2.0, pos = [0.4,0])
def set_visuals(size, full, monitor, color, wintype, text, align, ht, wWidth, textcolor, radius, stimpath):
    win = visual.Window([600,400], fullscr=full, allowGUI = False, monitor = monitor, color = color, winType=wintype) #check window here
    instruct = visual.TextStim(win, text=text, alignHoriz = align, height = ht, wrapWidth = wWidth, color = textcolor)
    fix = visual.TextStim(win, text = '+')
    left_choice = visual.Circle(win, radius = radius, lineColor = textcolor, lineWidth = 2.0, pos = [-0.4,0])
    right_choice = visual.Circle(win, radius = radius, lineColor = textcolor, lineWidth = 2.0, pos = [0.4,0])
    reward = visual.ImageStim(win, units = 'norm', size = [1,1], pos = [0,0], image = os.path.join(stimpath,'reward.png'))
    zero = visual.ImageStim(win, units = 'norm', size = [1,1], pos = [0,0], image = os.path.join(stimpath,'zero.png'))
    no_resp = visual.TextStim(win, text='No Response Detected!', height = 0.15, wrapWidth = 35, color = 'red')
    parameters = {'win':win, 'instruct':instruct, 'fix':fix, 'left_choice':left_choice, 'right_choice':right_choice, 'reward':reward, 'zero':zero, 'no_resp':no_resp}
    return(parameters)

#Object, response, fix, and instruction stims.
#instruct = visual.TextStim(win, text='Text', alignHoriz = 'center', height = 0.12, wrapWidth = 350, color = 'white')

# Control keys
LEFT_KEY = '1'
RIGHT_KEY = '4'
QUIT_KEY = 'q'
# Test Keys
SIMULATE_CORRECT = "c"
SIMULATE_INCORRECT = "v"
START_MOTOR = "b"
STOP_MOTOR = "n"
# Timestamp Variables
dispense_time = None
taken_time = None
# Creates the Datapath folder if it does not exist
