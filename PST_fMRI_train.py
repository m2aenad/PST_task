#!/usr/bin/python

#fMRI PST training script.
#Last Updated: Sep 8, 2022
#Original Author: Dan Dillon
#Updated by: G Shearrer and Y Akmadjonova

import os
import math
import numpy as np
import pandas as pd
from psychopy import core, data, event, gui, misc, sound, visual

#Screen refresh duration.

refresh = 16.7

#Basic parameters.

num_disdaqs = 5 # not sure what this is yet

TR = 3 #Shouldn't need not scanning

stim_dur = 3
fdbk_dur = 1
disdaq_time = int(math.floor((num_disdaqs*3000)/refresh)) #15s (5TRs)
num_trials = 60 #Per block.
trial_dur = 8 #On average.
lastHRF = 15 #Time in sec, adjusted on-fly to account for timing errors.

end_time = (TR * num_disdaqs) + (num_trials * trial_dur) + lastHRF

#Define response keys.

left_key = '1'
right_key = '4'
quit_key = 'q'

#Define response keys for ratings.

b0 = '0'
b1 = '1'
b2 = '2'
b3 = '3'
b4 = '4'

##GUI to get subject number, date.

try:
    expInfo = misc.fromFile('PST_fMRI_lastParams.pickle')
except:
    expInfo = {'subject':'999'}
expInfo['dateStr'] = data.getDateStr()

dlg = gui.DlgFromDict(expInfo, title='PST_fMRI', fixed=['dateStr'])
if dlg.OK:
    misc.toFile('PST_fMRI_lastParams.pickle', expInfo) 
else:
    core.quit()

#Functions.

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

def show_resp(action,l_stim_num,r_stim_num,frames,measured_refresh,start_time):

    refresh = measured_refresh
    resp_onset = start_time
    
    if action == 'left':

        while frames < int(math.floor(3000/refresh)):
            left_stim.draw()
            right_stim.draw()
            fix.draw()
            left_choice.draw()
            win.flip()
            frames = frames + 1

        if l_stim_num < r_stim_num: 
            accuracy = 1
            
        else: 
            accuracy = 0

    if action == 'right':

        while frames < int(math.floor(3000/refresh)):
            left_stim.draw()
            right_stim.draw()
            fix.draw()
            right_choice.draw()
            win.flip()
            frames = frames + 1

        if l_stim_num > r_stim_num: 
            accuracy = 1
            
        else: 
            accuracy = 0

    return (accuracy, resp_onset)

def show_fdbk(accuracy,sched_out,action,start_time,measured_refresh):

    refresh = measured_refresh
    fdbk_clock = core.Clock()
    fdbk_clock.reset()
    fdbk_onset = start_time

    if accuracy == 1 and sched_out == 1:

        #corr_sound.play()
        for frames in range(int(math.floor(1000/refresh))):
            reward.draw()
            win.flip()
        
        fdbk_dur = fdbk_clock.getTime()

        return ('reward',fdbk_onset,fdbk_dur)

    elif accuracy == 1 and sched_out == 0:

        #incorr_sound.play()
        for frames in range(int(math.floor(1000/refresh))):
            zero.draw()
            win.flip()

        fdbk_dur = fdbk_clock.getTime()

        return ('zero',fdbk_onset,fdbk_dur)

    elif accuracy == 0 and sched_out == 1:

        #incorr_sound.play()
        for frames in range(int(math.floor(1000/refresh))):
            zero.draw()
            win.flip()

        fdbk_dur = fdbk_clock.getTime()

        return ('zero',fdbk_onset,fdbk_dur)

    elif accuracy == 0 and sched_out == 0:
        
        #corr_sound.play()
        for frames in range(int(math.floor(1000/refresh))):
            reward.draw()
            win.flip()

        fdbk_dur = fdbk_clock.getTime()

        return ('reward',fdbk_onset,fdbk_dur)

    elif accuracy == 999:

        for frames in range(int(math.floor(1000/refresh))):
            no_resp.draw()
            win.flip()

        fdbk_dur = fdbk_clock.getTime()

        return ('no_response',fdbk_onset,fdbk_dur)

def show_fix(duration,start_time,measured_refresh):

    refresh = measured_refresh
    fix_onset = start_time
    fix_clock = core.Clock()
    fix_clock.reset()
    
    for i in range(duration):
        fix.draw()
        win.flip()

    fix_dur = fix_clock.getTime()

    return (fix_onset,fix_dur)
##Basics for the experiment.


#Window.
wintype='pyglet' 
win = visual.Window([600,400], fullscr = 'True', allowGUI = False, monitor = 'MacAir', color = 'black', winType=wintype) #check window here

#Object, response, fix, and instruction stims.
instruct = visual.TextStim(win, text='Text', alignHoriz = 'center', height = 0.12, wrapWidth = 350, color = 'white')
fix = visual.TextStim(win, text = '+')
left_choice = visual.Circle(win, radius = 0.3, lineColor = 'ForestGreen', lineWidth = 2.0, pos = [-0.4,0])
right_choice = visual.Circle(win, radius = 0.3, lineColor = 'ForestGreen', lineWidth = 2.0, pos = [0.4,0])

stimpath = '/Users/gracer/Desktop/PST_Py_Stims'

#Feedback stims.
reward = visual.ImageStim(win, units = 'norm', size = [1,1], pos = [0,0], image = os.path.join(stimpath,'reward.bmp'))
zero = visual.ImageStim(win, units = 'norm', size = [1,1], pos = [0,0], image = os.path.join(stimpath,'zero.bmp'))
no_resp = visual.TextStim(win, text='No Response Detected!', height = 0.15, wrapWidth = 35, color = 'red')

#Sounds.
#corr_sound = sound.SoundPygame(value=os.path.join(stimpath,'Stimuli/correct.ogg'))
#incorr_sound = sound.SoundPygame(value=os.path.join(stimpath,'Stimuli/incorrect.ogg'))
#advance_sound = sound.SoundPygame(value=os.path.join(stimpath,'Stimuli/click_quiet.ogg'))

#Rating stims.
feedback_image = visual.ImageStim(win, units = 'norm', size = [1,1], pos = [0,0], image = os.path.join(stimpath,'reward.bmp'))
rating_text = visual.TextStim(win, text = 'How Do You Feel Right Now?', pos = [0,0.5], height = 0.18, wrapWidth = 35, color = 'white')
valence_rate = visual.ImageStim(win, units = 'cm', size = [22.44,6.42], pos = [0,-7.0], image = os.path.join(stimpath,'valence2.bmp'))
arousal_rate = visual.ImageStim(win, units = 'cm', size = [22.44,6.42], pos = [0,-7.0], image = os.path.join(stimpath,'arousal2.bmp'))
b0_choice = visual.Rect(win, units = 'cm', width = 3.5, height = 6.2, lineColor = 'ForestGreen', lineWidth = 4.0, pos = [-9.4,-7.0])
b1_choice = visual.Rect(win, units = 'cm', width = 3.5, height = 6.2, lineColor = 'ForestGreen', lineWidth = 4.0, pos = [-4.8,-7.0])
b2_choice = visual.Rect(win, units = 'cm', width = 3.5, height = 6.2, lineColor = 'ForestGreen', lineWidth = 4.0, pos = [-0.2,-7.0])
b3_choice = visual.Rect(win, units = 'cm', width = 3.5, height = 6.2, lineColor = 'ForestGreen', lineWidth = 4.0, pos = [4.4,-7.0])
b4_choice = visual.Rect(win, units = 'cm', width = 3.5, height = 6.2, lineColor = 'ForestGreen', lineWidth = 4.0, pos = [8.9,-7.0])

#Durations (s) for ISI and ITI
#fix_list was generated by random selection from an exponential distribution.
#min = 0.5, max = 8.0, mean = 2.0, mode = 0.5

fix_list = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 3.0, 3.0, 4.0, 4.0, 4.0, 4.0, 5.0, 5.0, 5.0, 6.0, 6.0, 6.0, 7.0, 8.0]

#Create isi/iti lists w/durations in screen refreshs, and randomize them.

isi_list = []
iti_list = []

for dur in range(len(fix_list)):
    for list in [isi_list, iti_list]:
        list.append(int(round((fix_list[dur]*1000)/refresh)))

##Set-up the stim/response contingencies.

num_blocks = 4
num_stims = 6
trials_per_stim = 10 #Number times stim on left out of 20 trials.

#Make master list of stim lists.

list = [1 for x in range(num_stims)]
count = 1
for x in range(num_stims):
    list[x] = [count for y in range(trials_per_stim)]
    count+=1

#Assign the individual stim lists to stim names.

A = list[0]
C = list[1]
E = list[2]
F = list[3]
D = list[4]
B = list[5]

#Make the reward probability vectors.

n80 = [1,1,1,1,1,1,1,1,0,0]
n70 = [1,1,1,1,1,1,1,0,0,0]
n60 = [1,1,1,1,1,1,0,0,0,0]

#Concatenate stim lists and reward probability vectors.

AB = np.column_stack([A,B,n80])
BA = np.column_stack([B,A,n80])
CD = np.column_stack([C,D,n70])
DC = np.column_stack([D,C,n70])
EF = np.column_stack([E,F,n60])
FE = np.column_stack([F,E,n60])

AB_trialList = np.vstack([AB,BA])
CD_trialList = np.vstack([CD,DC])
EF_trialList = np.vstack([EF,FE])

#Shuffle trial lists to space out rewards.

np.random.shuffle(AB_trialList)
np.random.shuffle(CD_trialList)
np.random.shuffle(EF_trialList)

#Make 20 "small blocks" with one trial each from the AB, CD, and EF lists.

small_blocks = [[i] for i in range(20)]

for i in range(20):
    small_blocks[i] = np.vstack([AB_trialList[i],CD_trialList[i],EF_trialList[i]])

#Shuffle bitmaps so images used as stims A, B, C, etc. vary across subjects.

pic_list = [os.path.join(stimpath,'1.bmp'), os.path.join(stimpath,'2.bmp'), os.path.join(stimpath,'3.bmp'), os.path.join(stimpath,'4.bmp'), os.path.join(stimpath,'5.bmp'), os.path.join(stimpath,'6.bmp')]
np.random.shuffle(pic_list) 

stim_A = pic_list[0]
stim_C = pic_list[1]
stim_E = pic_list[2]
stim_F = pic_list[3]
stim_D = pic_list[4]
stim_B = pic_list[5]

#Write out stim randomization for use in test.

stim_rand = {'stim_A':pic_list[0], 'stim_C':pic_list[1], 'stim_E':pic_list[2], 'stim_F':pic_list[3], 'stim_D':pic_list[4], 'stim_B':pic_list[5]}

df = pd.DataFrame(stim_rand.items())
df.to_csv(expInfo['subject']+'_PST_stim_rand.csv', header=False, index=False)

#Clocks.

RT = core.Clock()
fMRI_clock = core.Clock()

#File to collect training data. 

train_file = expInfo['subject'] + '_' + expInfo['dateStr']
trainFile = open(train_file+'_PST_fMRI_train.csv', 'w')
trainFile.write('block,trial_num,left_stim,left_stim_number,right_stim,right_stim_number,object_onset,object_duration,response,response_onset,trial_RT,accuracy,isi_onset,isi_duration,scheduled_outcome,feedback,feedback_onset,feedback_duration,iti_onset,iti_duration\n')

##Start the study.
#Instructions.

inst_text = ['This is a new game, with\nchances to win more money.\n\nPress button 1 to advance.', 
'Two figures will appear\non the computer screen.\n\nOne figure will pay you more often\nthan the other, but at first you won\'t\nknow which figure is the good one.\n\nPress 1 to advance.', 'Try to pick the figure that pays\nyou most often.\n\nWhen you see the REWARD screen,\nthat means you won bonus money!\n\nWhen you see the ZERO screen,\nyou did not win.\n\nPress 1 to advance.', 'Keep in mind that no figure\npays you every time you pick it.\n\nJust try to pick the one\nthat pays most often.\n\nPress 1 to select the figure\non the left. Press 4 to select\nthe figure on the right.\n\nPress 1 to advance.', 'At first you may be confused,\nbut don\'t worry.\n\nYou\'ll get plenty of chances.\n\nPress 1 to advance.', 'There are 4 blocks of trials.\nEach one lasts about 8 minutes.\n\nMake sure to try all the figures\nso you can learn which ones\nare better and worse.\n\nPress button 1 to advance.']

allKeys = []

for i in range(len(inst_text)):
    advance = 'false'

    while advance == 'false':
        instruct.setText(text = inst_text[i]) 
        instruct.draw()
        win.flip()
        allKeys = event.waitKeys(keyList = [left_key, quit_key])
        resp = allKeys[0][0]

        if resp == left_key:
            #advance_sound.play()
            advance = 'true'
            allKeys = []

        elif resp == quit_key:
            #advance_sound.play()
            core.quit()

#Run experimental trials.

block_num = 1

for block in range(num_blocks):

    #Shuffle ISI/ITI durations.

    np.random.shuffle(isi_list)
    np.random.shuffle(iti_list)

    #Randomize each small block (scramble AB,CD,EF trios).

    for i in range(20):
        np.random.shuffle(small_blocks[i])

    #Make AllTrials array of small blocks.

    AllTrials = np.asarray(small_blocks)

    #Check no more than 6 consecutive rewards scheduled, otherwise shuffle.

    while not check_rand(AllTrials,20,3):
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

    leftStims = [stim_A if x==1 else stim_C if x==2 else stim_E if x==3 else stim_F if x==4 else stim_D if x==5 else stim_B if x==6 else x for x in leftStims]

    rightStims = [stim_A if x==1 else stim_C if x==2 else stim_E if x==3 else stim_F if x==4 else stim_D if x==5 else stim_B if x==6 else x for x in rightStims]

    #Load the stims in a matrix to improve timing/efficiency.
    stim_matrix = {}

    for i in range(len(leftStims)): 
        instruct.setText(text = 'Please relax and hold still\n\nas we set up the computer.\n\nThis will only take a few seconds.')
        instruct.draw()
        win.flip()

        left_stim = visual.ImageStim(win, units = 'norm', size = [0.5,0.5], pos = [-0.4,0], image=leftStims[i])
        left_stim_name = leftStims[i]
        left_stim_number = left_stim_numbers[i]
        right_stim = visual.ImageStim(win, units = 'norm', size = [0.5,0.5], pos = [0.4,0], image=rightStims[i])
        right_stim_name = rightStims[i]
        right_stim_number = right_stim_numbers[i]
        scheduled_outcome = sch_outcome[i] 
        stim_matrix[i] = (left_stim,left_stim_name,left_stim_number,right_stim,right_stim_name,right_stim_number,scheduled_outcome)
    
    #Check-in before starting scan.

    last_text = ['We will check in with you now\n\nto ask if you are ready to begin.']

    advance = 'false'
    k = ['']

    while advance == 'false':
        instruct.setText(text=last_text[0])
        instruct.draw()
        win.flip()
        k = event.waitKeys()

        if k[0] == 'o':
            advance = 'true'

        elif k[0] == 'q':
            core.quit()

    #Disdaqs, start fMRI clock.
    fMRI_clock.reset() #fMRI_clock begins at start of disdaqs.

    for frame in range(disdaq_time):
        fix.draw()
        win.flip()

    #Run through the trials.

    for i in range(len(leftStims)):

        trial_num = i + 1

        #Clear buffers.

        event.clearEvents()
        allKeys=[]
        resp=[]
        trial_RT=[]
        stim_frameN = 0

        #Prep the stims.

        left_stim = stim_matrix[trial_num-1][0]
        left_stim_name = stim_matrix[trial_num-1][1]
        left_stim_number = stim_matrix[trial_num-1][2]
        right_stim = stim_matrix[trial_num-1][3]
        right_stim_name = stim_matrix[trial_num-1][4]
        right_stim_number = stim_matrix[trial_num-1][5]
        scheduled_outcome = stim_matrix[trial_num-1][6]

        #Set ISI/ITI durs.

        isi_dur = isi_list[i]
        iti_dur = iti_list[i]

        #Reset the RT clock. 

        RT.reset()

        #Set-up desired trial dur (excluding ITI).

        targ_trial_dur = stim_dur + (isi_dur * refresh)/1000 + fdbk_dur

        #Draw the stims and handle keyboard input.
        
        object_onset = fMRI_clock.getTime()
        while stim_frameN < int(math.floor(3000/refresh)):
            response = 'false'
            left_stim.draw()
            right_stim.draw()
            fix.draw()
            win.flip()
            allKeys=event.getKeys(keyList = [left_key,right_key,quit_key], timeStamped=RT)

            if allKeys:
                resp = allKeys[0][0]
                trial_RT=allKeys[0][1]
                #advance_sound.play()

                if resp == quit_key:
                    core.quit()

                elif resp == left_key:
                    response = 'left'
                    trial_response = show_resp(response,left_stim_number,right_stim_number,stim_frameN,refresh,fMRI_clock.getTime())
                    isi = show_fix(isi_dur,fMRI_clock.getTime(),refresh)
                    object_dur = isi[0] - object_onset
                    feedback = show_fdbk(trial_response[0],scheduled_outcome,response,fMRI_clock.getTime(),refresh)
                    act_trial_dur = object_dur + isi[1] + feedback[2]
                    iti_dur = iti_dur + int(round(((targ_trial_dur - act_trial_dur)*1000)/refresh))
                    iti = show_fix(iti_dur,fMRI_clock.getTime(),refresh)
                    stim_frameN = int(math.floor(3000/refresh))

                elif resp == right_key:
                    response = 'right'
                    trial_response = show_resp(response,left_stim_number,right_stim_number,stim_frameN,refresh,fMRI_clock.getTime())
                    isi = show_fix(isi_dur,fMRI_clock.getTime(),refresh)
                    object_dur = isi[0] - object_onset
                    feedback = show_fdbk(trial_response[0],scheduled_outcome,response,fMRI_clock.getTime(),refresh)
                    act_trial_dur = object_dur + isi[1] + feedback[2]
                    iti_dur = iti_dur + int(round(((targ_trial_dur - act_trial_dur)*1000)/refresh))
                    iti = show_fix(iti_dur,fMRI_clock.getTime(),refresh)
                    stim_frameN = int(math.floor(3000/refresh))
            
            stim_frameN = stim_frameN + 1

        #Catch trials with no response.

        if stim_frameN == int(math.floor(3000/refresh)) and response == 'false':
            response = 'No_response'
            trial_RT = 999
            accuracy = 999
            isi = show_fix(isi_dur,fMRI_clock.getTime(),refresh)
            object_dur = isi[0] - object_onset
            trial_response = (999,999.0)
            feedback = show_fdbk(accuracy,scheduled_outcome,response,fMRI_clock.getTime(),refresh)
            act_trial_dur = object_dur + isi[1] + feedback[2]
            iti_dur = iti_dur + int(round(((targ_trial_dur - act_trial_dur)*1000)/refresh))
            iti = show_fix(iti_dur,fMRI_clock.getTime(),refresh)

        #Write out the data.

        trainFile.write('%i,%i,%s,%i,%s,%i,%0.3f,%0.3f,%s,%0.3f,%0.3f,%i,%0.3f,%0.3f,%i,%s,%0.3f,%0.3f,%0.3f,%0.3f\n' %(block_num, trial_num, left_stim_name, left_stim_number, right_stim_name, right_stim_number, object_onset, object_dur, response, trial_response[1], trial_RT, trial_response[0], isi[0], isi[1], scheduled_outcome, feedback[0], feedback[1], feedback[2], iti[0], iti[1]))

        #Fade out with lastHRF fixation cross after 60 trials.
        
        if trial_num == 60: 
            elapsed_time = fMRI_clock.getTime()
            time_left = end_time - elapsed_time

            for i in range(int(round((time_left*1000)/refresh))):
                fix.draw()
                win.flip()

    #Present a screen between blocks.

    if block_num < num_blocks:

        pause_text = ['Great job!\n\nYou are done with that block.\n\nTake a few seconds to relax.\n\nWhen you are ready to continue,\npress button 1.']
        
        allKeys = []

        for i in range(len(pause_text)):
            advance = 'false'
            instruct.setText(text = pause_text[i]) 
            
            while advance == 'false':
                instruct.draw()
                win.flip()
                allKeys = event.waitKeys(keyList = [left_key,quit_key])
                resp = allKeys[0][0]

                if resp == left_key:
                    advance = 'true'
                    #advance_sound.play()
                    allKeys = []

                elif resp == quit_key:
                    core.quit()

    #Update the block count.

    block_num+=1

#Now that we've looped over all the blocks, close the training file.

trainFile.close()

#Move on to outcome ratings.

rate_text = ['Great job!\n\nNow we\'d like you to rate your emotional\nresponse to the REWARD and ZERO\noutcomes again.\n\nPress 1 to continue.']

allKeys = []

for i in range(len(rate_text)):

    advance = 'false'
    
    while advance == 'false':
        instruct.setText(text=rate_text[i])
        instruct.draw()
        win.flip()
        allKeys = event.waitKeys(keyList=[b1,quit_key])

        if allKeys:
            resp = allKeys[0][0]

            if resp == b1:
                advance = 'true'
                #advance_sound.play()
                allKeys = []

            else:
                #advance_sound.play()
                core.quit()

#Valence instructions.

valence_rate_inst = ['You will again use all 5 buttons to tell us\nhow PLEASANT or UNPLEASANT you\nfind the reward and zero outcomes.\n\n\nPress 1 to continue.', 'Here\'s how to use the scale:\n\nPress 0 if you feel unhappy,\nunsatisfied, or bored.\n\nPress 2 if you feel neutral,\nnot pleased or displeased.\n\nPress 4 if you feel happy,\nsatisfied, or contented.\n\nUse 1 and 3 for intermediate ratings.\n\nPress 1 to start making your ratings.']

allKeys = []

for i in range(len(valence_rate_inst)):

    advance = 'false'

    while advance == 'false':
        instruct.setText(text=valence_rate_inst[i])
        instruct.draw()
        win.flip()
        allKeys=event.waitKeys(keyList=[b1,quit_key])

        if allKeys:
            resp = allKeys[0][0]
            
            if resp == b1:
                advance = 'true'
                #advance_sound.play()
                allKeys = []

            else:
                #advance_sound.play()
                core.quit()

#Set-up file to collect ratings data.

ratefile = expInfo['subject'] + '_' + expInfo['dateStr']
PST_Rate_Data_File = open(ratefile+'_PST_fMRI_ratings.csv', 'w')
PST_Rate_Data_File.write('stimulus,prompt,rating\n')

#Valence ratings.

prompt = 'valence'

iti_frameN = 0
while iti_frameN <= 120:
    fix.draw()
    win.flip()
    iti_frameN = iti_frameN + 1

outcome_list = ['reward.bmp','zero.bmp']

for i in range(len(outcome_list)):

    allKeys = []
    fdbk_frameN = 0
    rate_frameN = 0
    advance = 'false'

    feedback_image.setImage(value=os.path.join(stimpath, outcome_list[i]))

    if outcome_list[i] == 'reward.bmp':
        outcome = 'reward'
        #corr_sound.play()
        while fdbk_frameN <= 120:
            feedback_image.draw()
            win.flip()
            fdbk_frameN = fdbk_frameN + 1

        rating_text.draw()
        valence_rate.draw()
        win.flip()

    else:
        outcome = 'zero'
        #incorr_sound.play()
        while fdbk_frameN <= 120:
            feedback_image.draw()
            win.flip()
            fdbk_frameN = fdbk_frameN + 1

        rating_text.draw()
        valence_rate.draw()
        win.flip()

    while advance == 'false':
        allKeys=event.waitKeys(keyList=[b0,b1,b2,b3,b4])
        rating_text.draw()
        valence_rate.draw()
        win.flip()
        
        if allKeys:
            resp = allKeys[0][0]
            if resp == b0:
                advance = 'true'
                #advance_sound.play()
                rating = 0
                while rate_frameN <= 60:
                    rating_text.draw()
                    valence_rate.draw()
                    b0_choice.draw()
                    win.flip()
                    rate_frameN = rate_frameN + 1

            if resp == b1:
                advance = 'true'
                #advance_sound.play()
                rating = 1
                while rate_frameN <= 60:
                    rating_text.draw()
                    valence_rate.draw()
                    b1_choice.draw()
                    win.flip()
                    rate_frameN = rate_frameN + 1

            if resp == b2:
                advance = 'true'
                #advance_sound.play()
                rating = 2
                while rate_frameN <= 60:
                    rating_text.draw()
                    valence_rate.draw()
                    b2_choice.draw()
                    win.flip()
                    rate_frameN = rate_frameN + 1

            if resp == b3:
                advance = 'true'
                #advance_sound.play()
                rating = 3
                while rate_frameN <= 60:
                    rating_text.draw()
                    valence_rate.draw()
                    b3_choice.draw()
                    win.flip()
                    rate_frameN = rate_frameN + 1

            if resp == b4:
                advance = 'true'
                #advance_sound.play()
                rating = 4
                while rate_frameN <= 60:
                    rating_text.draw()
                    valence_rate.draw()
                    b4_choice.draw()
                    win.flip()
                    rate_frameN = rate_frameN + 1

        #Record the valence ratings.

        PST_Rate_Data_File.write('%s,%s,%i\n' %(outcome, prompt, rating))
        
        #Present fixation.

        iti_frameN = 0
        while iti_frameN <= 60:
            fix.draw()
            win.flip()
            iti_frameN = iti_frameN + 1


#Arousal instructions.

arousal_rate_inst = ['Now you will (again) use a different 5-point\nscale to tell us how AROUSING you find\nthe reward and zero outcomes.\n\nPress 1 to continue.', 'Here\'s how to use the 5-point scale:\n\nPress 0 if you feel relaxed,\nsluggish, or sleepy.\n\nPress 2 if you feel moderate arousal:\nnot very calm, but not very excited.\n\nPress 4 if you feel excited,\njittery, or wide awake.\n\nUse 1 and 3 for intermediate ratings.\n\nPress 1 to start making your ratings.']

#Arousal ratings.

allKeys = []

for i in range(len(arousal_rate_inst)):

    advance = 'false'

    while advance == 'false':
        instruct.setText(text=arousal_rate_inst[i])
        instruct.draw()
        win.flip()
        allKeys=event.waitKeys(keyList=[b1,quit_key])

        if allKeys:
            resp = allKeys[0][0]
            
            if resp == b1:
                #advance_sound.play()
                advance = 'true'

            else:
                core.quit()

#Arousal ratings.

prompt = 'arousal'

iti_frameN = 0
while iti_frameN <= 120:
    fix.draw()
    win.flip()
    iti_frameN = iti_frameN + 1

outcome_list = ['reward.bmp','zero.bmp']

for i in range(len(outcome_list)):

    allKeys = []
    fdbk_frameN = 0
    rate_frameN = 0
    advance = 'false'

    feedback_image.setImage(value=outcome_list[i])

    if outcome_list[i] == 'reward.bmp':
        outcome = 'reward'
        #corr_sound.play()
        while fdbk_frameN <= 120:
            feedback_image.draw()
            win.flip()
            fdbk_frameN = fdbk_frameN + 1

        rating_text.draw()
        arousal_rate.draw()
        win.flip()

    else:
        outcome = 'zero'
        #incorr_sound.play()
        while fdbk_frameN <= 120:
            feedback_image.draw()
            win.flip()
            fdbk_frameN = fdbk_frameN + 1

        rating_text.draw()
        arousal_rate.draw()
        win.flip()

    while advance == 'false':
        allKeys=event.waitKeys(keyList=[b0,b1,b2,b3,b4])
        rating_text.draw()
        arousal_rate.draw()
        win.flip()
        
        if allKeys:
            resp = allKeys[0][0]
            if resp == b0:
                advance = 'true'
                #advance_sound.play()
                rating = 0
                while rate_frameN <= 60:
                    rating_text.draw()
                    arousal_rate.draw()
                    b0_choice.draw()
                    win.flip()
                    rate_frameN = rate_frameN + 1

            if resp == b1:
                advance = 'true'
                #advance_sound.play()
                rating = 1
                while rate_frameN <= 60:
                    rating_text.draw()
                    arousal_rate.draw()
                    b1_choice.draw()
                    win.flip()
                    rate_frameN = rate_frameN + 1

            if resp == b2:
                advance = 'true'
                #advance_sound.play()
                rating = 2
                while rate_frameN <= 60:
                    rating_text.draw()
                    arousal_rate.draw()
                    b2_choice.draw()
                    win.flip()
                    rate_frameN = rate_frameN + 1

            if resp == b3:
                advance = 'true'
                #advance_sound.play()
                rating = 3
                while rate_frameN <= 60:
                    rating_text.draw()
                    arousal_rate.draw()
                    b3_choice.draw()
                    win.flip()
                    rate_frameN = rate_frameN + 1

            if resp == b4:
                advance = 'true'
                #advance_sound.play()
                rating = 4
                while rate_frameN <= 60:
                    rating_text.draw()
                    arousal_rate.draw()
                    b4_choice.draw()
                    win.flip()
                    rate_frameN = rate_frameN + 1

        #Record the arousal ratings.

        PST_Rate_Data_File.write('%s,%s,%i\n' %(outcome, prompt, rating))

        #Present fixation.

        iti_frameN = 0
        while iti_frameN <= 60:
            fix.draw()
            win.flip()
            iti_frameN = iti_frameN + 1

#Close the rating file.

PST_Rate_Data_File.close()
