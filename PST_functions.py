#!/usr/bin/python
# Requires Python 3.8.10
from math import floor
import os
from math import floor
import numpy as np
import pandas as pd
from psychopy import core, data, event, gui, misc, sound, visual
import serial
import pickle
import datetime

datefmt='%m-%d-%Y_%I-%M-%S'

def adillyofapickle(basepath, dic, name):
    # st = datetime.fromtimestamp(time()).strftime(datefmt)
    if os.path.exists(os.path.join(basepath,'%s'%name)):
        print('already have %s'%name)
    else:
        os.makedirs(os.path.join(basepath,'%s'%name))
    pickle.dump(dic, open(os.path.join(basepath,'%s'%name,'%s'%(name)), 'wb'), protocol=4)
'''
All about the pickles
Each pickle file should be all the data needed to recreate any of the runs including all answers
The data key is formated to import into pandas with each block as a dataframe
example_datat = pk[participant_ID]['data'][block]

df = pd.DataFrame.from_dict(example_data, orient='index',
                       columns=['trial_number', 'left_stim_name', 'left_stim_number', 'right_stim_name','right_stim_number','onset','response','trial_feedback','reward','RT'])
df['block']= block_num


pk = {
    info['particpant']:{ 
        'date': info['date'],
        'fullscr':info['fullscr'], 
        'test?':info['test'], 
        'experiment_parameters':{
            'num_blocks':num_blocks,
            'num_stims':num_stims,
            'trials_per_stim':trials_per_stim, 
            'win':win, 
            'left':left_choice,
            'right':right_choice,
            'small_blocks':small_blocks,
            'picture_map': stim_rand,
            'stim_mat':stim_matrix
            }, 
        'data':{
            block:{
                trial_num:[left_stim_name, 
                left_stim_number, 
                right_stim_name, 
                right_stim_number, 
                onset, 
                response, 
                trail_feedback, 
                reward, 
                RT]
                }
            }
        }
    }
}
'''

def check_quit(check_key, basepath, dic, name):
    if len(check_key)>0:
        if check_key[0] == 'q':
            adillyofapickle(basepath, dic, name)
            core.quit()

def present_stims(fix,left_stim, right_stim, win, left_key,right_key,quit_key, RT, task_clock, scheduled_outcome):
    # from psychopy import event
    left_stim.draw()
    right_stim.draw()
    win.flip()
    # wait for key press
    key_press = event.waitKeys(keyList = [left_key,right_key,quit_key], timeStamped=RT)
    return(key_press)

def response_update(key_pressed, win, left_stim, right_stim, left_choice, right_choice, task_clock):  
    resp_onset = task_clock.getTime()
    if key_pressed == '1':
        left_choice.draw()
        left_stim.draw()
        right_stim.draw()
        win.flip()
    elif key_pressed == '4':
        right_choice.draw()
        left_stim.draw()
        right_stim.draw()
        win.flip()
        

def drawing(left_stim, right_stim, fix, left_choice, right_choice, win):
    left_stim.draw()
    right_stim.draw()
    fix.draw()
    win.flip()

def accuracy(l_stim_num , r_stim_num, choice):
    # print(l_stim_num)
    # print(r_stim_num)
    if l_stim_num < r_stim_num: 
            accuracy = 1        
    else: 
        accuracy = 0
    if l_stim_num > r_stim_num: 
            accuracy = 1        
    else: 
        accuracy = 0
    return (accuracy)

def show_resp(key_pressed, left_choice, right_choice, task_clock):
    resp_onset = task_clock.getTime()
    if key_pressed == '1':
        left_choice.draw()
        # win.flip()
    if key_pressed == '4':
        right_choice.draw()
        # win.flip()
    return(resp_onset)
    

def show_fdbk(accuracy,sched_out,task_clock, zero, win, reward, X):

    fdbk_onset = task_clock.getTime()

    if accuracy == 1 and sched_out == 1:
        reward.draw()
        if X == False:
            ser.write(52)
            cc=str(ser.readline())
        else:
            print('dispensing candy')
            win.flip()
        return ('correct_reward', fdbk_onset)

    elif accuracy == 1 and sched_out == 0:
        zero.draw()
        win.flip()
        return ('zero')
    elif accuracy == 0 and sched_out == 1:
        zero.draw()
        win.flip()
        return ('zero',fdbk_onset)
    elif accuracy == 0 and sched_out == 0:
        reward.draw()
        win.flip()
        return ('prob_reward', fdbk_onset)



def starter(small_blocks, stim_rand, win):
    from psychopy import visual
    for i in range(len(small_blocks)): #Randomize each small block (scramble AB,CD,EF trios).
        np.random.shuffle(small_blocks[i])
    AllTrials = np.asarray(small_blocks) #Make AllTrials array of small blocks.
    while not check_rand(AllTrials,20,3): #Check no more than 6 consecutive rewards scheduled, otherwise shuffle.
        np.random.shuffle(AllTrials)
    #Generate lists for leftStims, rightStims, and sch_outcome.
    #sch_outcome different from reward/zero fdbk, which depends on accuracy. 
    leftStims = []
    left_stim_numbers = []
    rightStims = []
    right_stim_numbers = []
    sch_outcome = []
    for x in range(20):
        for y in range(3):
            leftStims.append(AllTrials[x,y,0])
            rightStims.append(AllTrials[x,y,1])
            sch_outcome.append(AllTrials[x,y,2])
    left_stim_numbers = leftStims
    right_stim_numbers = rightStims
    
    leftStims2 = [stim_rand['stim_A'] if x==1 else stim_rand['stim_C'] if x==2 else stim_rand['stim_E'] if x==3 else stim_rand['stim_F'] if x==4 else stim_rand['stim_D'] if x==5 else stim_rand['stim_B'] if x==6 else x for x in leftStims]
    rightStims2 = [stim_rand['stim_A'] if x==1 else stim_rand['stim_C'] if x==2 else stim_rand['stim_E'] if x==3 else stim_rand['stim_F'] if x==4 else stim_rand['stim_D'] if x==5 else stim_rand['stim_B']if x==6 else x for x in rightStims]
    
    #Load the stims in a matrix to improve timing/efficiency.
    stim_matrix = {}
    for i in range(len(leftStims2)): 
        left_stim = visual.ImageStim(win, units = 'norm', size = [0.5,0.5], pos = [-0.4,0], image=leftStims2[i])
        left_stim_name = leftStims2[i]
        left_stim_number = left_stim_numbers[i]
        right_stim = visual.ImageStim(win, units = 'norm', size = [0.5,0.5], pos = [0.4,0], image=rightStims2[i])
        right_stim_name = rightStims2[i]
        right_stim_number = right_stim_numbers[i]
        scheduled_outcome = sch_outcome[i] 
        stim_matrix[i] = (left_stim,left_stim_name,left_stim_number,right_stim,right_stim_name,right_stim_number,scheduled_outcome)
    return(stim_matrix)


def intro(inst_text, instruct, win, allKeys, left_key, quit_key):
    for i in range(len(inst_text)):
        advance = 'false'

        while advance == 'false':
            instruct.setText(text = inst_text[i]) 
            instruct.draw()
            win.flip()
            allKeys = event.waitKeys(keyList = [left_key, quit_key])#wait for left key or quit key
            resp = allKeys[0][0]

            if resp == left_key:
                advance = 'true'
                allKeys = []

            elif resp == quit_key:
                core.quit()



def stim_mapping(pic_list, datapath, participantID):
    '''
    this will map the images to the stimuli
    random person
    writes a csv file
    '''
    np.random.shuffle(pic_list)
    stim_rand = {'stim_A':pic_list[0], 'stim_C':pic_list[1], 'stim_E':pic_list[2], 'stim_F':pic_list[3], 'stim_D':pic_list[4], 'stim_B':pic_list[5]}
#    df = pd.DataFrame(stim_rand.items())
#    df.to_csv(os.path.join(datapath,'%s_PST_stim_rand.csv'%(participantID)), header=False, index=False)
    return(stim_rand)


def block_it(AB_trialList, CD_trialList, EF_trialList):
    '''
    This concatonates all the of trialLists into a large list
    '''
    small_blocks = [[i] for i in range(20)]
    for i in range(20):
        small_blocks[i] = np.vstack([AB_trialList[i],CD_trialList[i],EF_trialList[i]])
    return(small_blocks)


def stimulating(num_stims, trials_per_stim):
    '''
    this creates a dictionary with the letters mapped to numbers
    the each letter is a key with a corresponding list of length number of trials per stim
    ex. {'A' : [1,1,1,1]}
    '''
    letters = ['A','C','E','F','D','B']
    stim_list = [1 for x in range(num_stims)]
    for count,x in enumerate(range(num_stims)):
        count = count+1
        stim_list[x] = [count for y in range(trials_per_stim)]
    # print(stim_list)
    stim_names = {}
    for i,x in enumerate(stim_list):
        stim_names[letters[i]] = x
    return(stim_names)

def make_it(stim_names):
    '''
    This makes the 3 trialLists (AB, CD, EF)
    Each trialList is a list length of 3
    The first value is the stim name for the left, the second is the stim name for the right, and the final is if it is rewarded or not
    Ex. [6,1,1] => the left is stimulus B the right is stimulus A if the person chooses B it is rewarded
    '''
    #Make the reward probability vectors.
    n80 = [1,1,1,1,1,1,1,1,0,0]
    n70 = [1,1,1,1,1,1,1,0,0,0]
    n60 = [1,1,1,1,1,1,0,0,0,0]
    #Concatenate stim lists and reward probability vectors.
    AB = np.column_stack([stim_names['A'],stim_names['B'],n80])
    BA = np.column_stack([stim_names['B'],stim_names['A'],n80])
    CD = np.column_stack([stim_names['C'],stim_names['D'],n70])
    DC = np.column_stack([stim_names['D'],stim_names['C'],n70])
    EF = np.column_stack([stim_names['E'],stim_names['F'],n60])
    FE = np.column_stack([stim_names['F'],stim_names['E'],n60])
    AB_trialList = np.vstack([AB,BA])
    CD_trialList = np.vstack([CD,DC])
    EF_trialList = np.vstack([EF,FE])
    trialList = [AB_trialList, CD_trialList, EF_trialList]
    for item in trialList:
        np.random.shuffle(item)
    return(trialList)


def set_visuals(size, monitor, color, wintype,text, align, ht, wWidth, textcolor, radius):
    from psychopy import visual
    win = visual.Window([600,400], fullscr= False, allowGUI = False, monitor = monitor, color = color, winType=wintype) #check window here
    instruct = visual.TextStim(win, text=text, alignHoriz = align, height = ht, wrapWidth = wWidth, color = textcolor)
    fix = visual.TextStim(win, text = '+')
    left_choice = visual.Circle(win, radius = radius, lineColor = textcolor, lineWidth = 2.0, pos = [-0.4,0])
    right_choice = visual.Circle(win, radius = radius, lineColor = textcolor, lineWidth = 2.0, pos = [0.4,0])
    parameters = {'win':win, 'instruct':instruct, 'fix':fix, 'left_choice':left_choice, 'right_choice':right_choice}
    return(parameters)


def stupid_math(refresh):
    return(int(floor(1000/refresh)))

def check_rand (in_array,num_array,num_row): #Cannot have more than 6 consecutive reward outcomes scheduled.
    counter = 0
    for x in range(num_array):
        for y in range(num_row):
            if in_array[x,y,2] == 1:
                counter += 1
                if counter == 6:
                    return False
            else:
                counter = 0
    return True

   


def show_fix(duration,start_time,measured_refresh, fix, win):

    refresh = measured_refresh
    fix_onset = start_time
    fix_clock = core.Clock()
    fix_clock.reset()
    
    for i in range(duration):
        fix.draw()
        win.flip()

    fix_dur = fix_clock.getTime()

    return (fix_onset,fix_dur)