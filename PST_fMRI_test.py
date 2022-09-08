#!/usr/bin/python

#REWMEM.fMRI PST test script.
#Last Updated: January 12, 2013 
#Author: Dan Dillon

import numpy as np
import pandas as pd
from psychopy import core, data, event, gui, misc, sound, visual

##GUI for subject number, date.

try:
    expInfo = misc.fromFile('PST_fMRI_test_lastParams.pickle')
except:
    expInfo = {'subject':'999'}
expInfo['dateStr'] = data.getDateStr()

dlg = gui.DlgFromDict(expInfo, title='PST_fMRI_test', fixed=['dateStr'])
if dlg.OK:
    misc.toFile('PST_fMRI_test_lastParams.pickle', expInfo) 
else:
    core.quit()

#Define response keys.

left_key = '1'
right_key = '4'
quit_key = 'q'

#Read in stim/image assignment from training.

stim_rand = pd.read_csv(expInfo['subject']+'_PST_stim_rand.csv',names=['stim','image'])

stim_A = stim_rand['image'][0]
stim_B = stim_rand['image'][1]
stim_C = stim_rand['image'][2]
stim_D = stim_rand['image'][3]
stim_E = stim_rand['image'][4]
stim_F = stim_rand['image'][5]

##Basics for the experiment.

#Window.

wintype='pyglet' 
win = visual.Window([1280,800], fullscr = 'True', allowGUI = False, monitor = 'Dan Mac', color = 'black', winType=wintype)

#Object, response, fix, and instruction stims.

instruct = visual.TextStim(win, text='Text', alignHoriz = 'center', height = 0.12, wrapWidth = 350, color = 'white')
fix = visual.TextStim(win, text = '+')

left_stim = visual.ImageStim(win, units = 'norm', size = [0.5,0.5], pos = [-0.4,0])
right_stim = visual.ImageStim(win, units = 'norm', size = [0.5,0.5], pos = [0.4,0])
left_choice = visual.Circle(win, radius = 0.3, lineColor = 'ForestGreen', lineWidth = 2.0, pos = [-0.4,0])
right_choice = visual.Circle(win, radius = 0.3, lineColor = 'ForestGreen', lineWidth = 2.0, pos = [0.4,0])

#Feedback stims.
no_resp = visual.TextStim(win, text='No Response Detected!', height = 0.15, wrapWidth = 35, color = 'red')

#Sounds.
advance_sound = sound.SoundPygame(value='Stimuli/click_quiet.ogg')

#RT clock.

RT = core.Clock()

#File for test data. 

test_file = expInfo['subject'] + '_' + expInfo['dateStr']
testFile = open(test_file+'_PST_test.csv', 'w')
testFile.write('block_id,trial_id,left_stim_name,left_stim_number,right_stim_name,right_stim_number,response,trial_RT,trial_accuracy\n')

#Set-up test code, based on Jocham et al. (2011).

#Two blocks, 12 trials of 15 combinations:
#1. 3 original pairs (AB,CD,EF)
#2. 12 novel pairs (Choose A, Avoid B, and CD, CE, CF, DE, DF, and EF).

#Set number of:
#1. blocks
#2. stims
#3. combos
#4. test trials per combo
#5. times stim on left per combo, per block

num_test_blocks = 2
num_test_stims = 6
num_test_combos = 15
test_trials_per_combo = 12 
num_lstim_per_test_combo = 6

#Make a master list of stim lists.  

test_list = [1 for x in range(num_test_stims)]
test_count = 1
for x in range(num_test_stims):
    test_list[x] = [test_count for y in range(num_lstim_per_test_combo)]
    test_count+=1

#Assign the individual stim lists to stim names.

A = test_list[0]
C = test_list[1]
E = test_list[2]
F = test_list[3]
D = test_list[4]
B = test_list[5]

#Concatenate the stim lists.

AB = np.column_stack([A,B])
BA = np.column_stack([B,A])
AC = np.column_stack([A,C])
CA = np.column_stack([C,A])
AD = np.column_stack([A,D])
DA = np.column_stack([D,A])
AE = np.column_stack([A,E])
EA = np.column_stack([E,A])
AF = np.column_stack([A,F])
FA = np.column_stack([F,A])
BC = np.column_stack([B,C])
CB = np.column_stack([C,B])
BD = np.column_stack([B,D])
DB = np.column_stack([D,B])
BE = np.column_stack([B,E])
EB = np.column_stack([E,B])
BF = np.column_stack([B,F])
FB = np.column_stack([F,B])
CD = np.column_stack([C,D])
DC = np.column_stack([D,C])
CE = np.column_stack([C,E])
EC = np.column_stack([E,C])
CF = np.column_stack([C,F])
FC = np.column_stack([F,C])
DE = np.column_stack([D,E])
ED = np.column_stack([E,D])
DF = np.column_stack([D,F])
FD = np.column_stack([F,D])
EF = np.column_stack([E,F])
FE = np.column_stack([F,E])

AB_test_list = np.vstack([AB,BA])
AC_test_list = np.vstack([AC,CA])
AD_test_list = np.vstack([AD,DA])
AE_test_list = np.vstack([AE,EA])
AF_test_list = np.vstack([AF,FA])
BC_test_list = np.vstack([BC,CB])
BD_test_list = np.vstack([BD,DB])
BE_test_list = np.vstack([BE,EB])
BF_test_list = np.vstack([BF,FB])
CD_test_list = np.vstack([CD,DC])
CE_test_list = np.vstack([CE,EC])
CF_test_list = np.vstack([CF,FC])
DE_test_list = np.vstack([DE,ED])
DF_test_list = np.vstack([DF,FD])
EF_test_list = np.vstack([EF,FE])

#Randomize the contents of those arrays.

np.random.shuffle(AB_test_list)
np.random.shuffle(AC_test_list)
np.random.shuffle(AD_test_list)
np.random.shuffle(AE_test_list)
np.random.shuffle(AF_test_list)
np.random.shuffle(BC_test_list)
np.random.shuffle(BD_test_list)
np.random.shuffle(BE_test_list)
np.random.shuffle(BF_test_list)
np.random.shuffle(CD_test_list)
np.random.shuffle(CE_test_list)
np.random.shuffle(CF_test_list)
np.random.shuffle(DE_test_list)
np.random.shuffle(DF_test_list)
np.random.shuffle(EF_test_list)

#Create small_test_blocks, which will hold 12 lists of 1 each of all 15 combos.
#We'll run through 6 of these 12 lists in each block, for 90 trials per block.

small_test_blocks = [[i] for i in range(test_trials_per_combo)]

for i in range(test_trials_per_combo):
    small_test_blocks[i] = np.vstack([AB_test_list[i],AC_test_list[i],AD_test_list[i],AE_test_list[i],AF_test_list[i],BC_test_list[i],BD_test_list[i],BE_test_list[i],BF_test_list[i],CD_test_list[i],CE_test_list[i],CF_test_list[i],DE_test_list[i],DF_test_list[i],EF_test_list[i]])

#Shuffle combos in each list, and order of the lists, in small_test_blocks.
#Randomizes the stim order in each block.

for i in range(test_trials_per_combo):
    np.random.shuffle(small_test_blocks[i])

np.random.shuffle(small_test_blocks)

#Make All_Test_Trials array out of small_test_blocks (easier to work with).

All_Test_Trials = np.asarray(small_test_blocks)
left_Test_Stims = []
right_Test_Stims = []

for x in range(test_trials_per_combo):
    for y in range(num_test_combos):
        left_Test_Stims.append(All_Test_Trials[x,y,0])
        right_Test_Stims.append(All_Test_Trials[x,y,1])

#Insert bitmaps for stim numbers. Obviously, no change in which bitmap goes with stim A, B, C, etc.
    
left_test_stim_numbers = left_Test_Stims
left_Test_Stims = [stim_A if x==1 else stim_C if x==2 else stim_E if x==3 else stim_F if x==4 else stim_D if x==5 else stim_B if x==6 else x for x in left_Test_Stims]
right_test_stim_numbers = right_Test_Stims
right_Test_Stims = [stim_A if x==1 else stim_C if x==2 else stim_E if x==3 else stim_F if x==4 else stim_D if x==5 else stim_B if x==6 else x for x in right_Test_Stims]

#Present instructions.

test_instructs = ['Now we will test what you\n\nhave learned in this game.\n\nPress 1 to advance.','During this set of trials\n\nyou will NOT get any\n\nmore REWARDs or ZEROs.\n\nPress 1 to advance.', 'However, your job is to pick\n\nthe figure that you think gave\n\nyou REWARDs more often.\n\nPress 1 to advance.', 'You will see old and new\n\ncombinations of figures.\n\nChoose the figure that\n\ngave REWARDs more often.\n\nIf you are not sure what to pick,\n\njust go with your gut.\n\nPress 1 to advance.', 'As usual, press 1 to\n\nselect the figure on the left.\n\nPress 4 to select\n\nthe figure on the right.\n\nPress 1 to start.']

allKeys = []

for i in range(len(test_instructs)):
    advance = 'false'
    
    while advance == 'false':
        instruct.setText(text=test_instructs[i])
        instruct.draw()
        win.flip()
        allKeys = event.waitKeys(keyList=[left_key,quit_key])
        resp = allKeys[0][0]

        if resp == left_key:     
            advance = 'true'
            advance_sound.play()
            allKeys = []

        elif resp == quit_key:
            advance_sound.play()
            core.quit()

#Run the test trials.

for i in range(120):
    fix.draw()
    win.flip()

trial_id = 0
block_id = 1
    
for i in range(len(left_Test_Stims)):

    #Clear keystrokes and reset accuracy and RT before presenting stimuli.

    event.clearEvents()
    allKeys=[]
    resp=[]
    trial_RT=[]
    trial_accuracy=[]

    #Clear the frame counters.

    iti_frameN = 0
    fdbk_frameN = 0
    stim_frameN = 0

    #Prep the stims.

    left_stim.setImage(left_Test_Stims[i])
    left_stim_name = left_Test_Stims[i]
    left_test_stim_number = left_test_stim_numbers[i]

    right_stim.setImage(right_Test_Stims[i])
    right_stim_name = right_Test_Stims[i]
    right_test_stim_number = right_test_stim_numbers[i]

    #Reset RT clock.

    RT.reset()

    #Draw stims and handle keyboard input.

    while stim_frameN <= 240: #Test stims stay onscreen for 4s.
        no_response = 'false'
        left_stim.draw()
        right_stim.draw()
        fix.draw()
        win.flip()
        allKeys=event.getKeys(keyList = [left_key,right_key,quit_key], timeStamped=RT)

        if allKeys:
            resp = allKeys[0][0]
            trial_RT = allKeys[0][1]

            if resp == quit_key:
                advance_sound.play()
                core.quit()

            if resp == left_key:
                advance_sound.play()
                response = 'left'
                while stim_frameN <= 240:
                    left_stim.draw()
                    right_stim.draw()
                    fix.draw()
                    left_choice.draw()
                    win.flip()
                    stim_frameN = stim_frameN + 1

                if left_test_stim_number < right_test_stim_number:
                    trial_accuracy = 1
                else:
                    trial_accuracy = 0

            elif resp == right_key:
                advance_sound.play()
                response = 'right'
                while stim_frameN <= 240:
                    left_stim.draw()
                    right_stim.draw()
                    fix.draw()
                    right_choice.draw()
                    win.flip()
                    stim_frameN = stim_frameN + 1

                if left_test_stim_number < right_test_stim_number:
                    trial_accuracy = 0
                else:
                    trial_accuracy = 1
        
        stim_frameN = stim_frameN + 1

    #Catch trials with no response and present "No Response Detected!" screen.

    if stim_frameN == 241 and not allKeys:
        no_response = 'true'
        response = 'No_response'
        trial_RT = 999
        trial_accuracy = 999
        while fdbk_frameN <= 120:
            no_resp.draw()
            win.flip()
            fdbk_frameN = fdbk_frameN + 1
            
    #Standard 2 s ITI.

    for i in range(120):
        fix.draw()
        win.flip()

    #Update the trial count.

    trial_id+=1

    #Write the data to disk.

    testFile.write('%i,%i,%s,%i,%s,%i,%s,%0.3f,%i\n' %(block_id, trial_id, left_stim_name, left_test_stim_number, right_stim_name, right_test_stim_number, response, trial_RT, trial_accuracy))

#Present a screen b/w the two test blocks.

    if trial_id == 90:

        test_pause = ['Great job!\nYou are half-way through the test.\nTake a moment to rest.\n\nWhen you are ready,\npress button 1 to continue.']
        
        allKeys = []

        for i in range(len(test_pause)):
            advance = 'false'
            
            while advance == 'false':
                instruct.setText(text=test_pause[i])
                instruct.draw()
                win.flip()
                allKeys = event.waitKeys(keyList=[left_key,quit_key])
                resp = allKeys[0][0]
            
                if resp == left_key:
                    advance = 'true'
                    advance_sound.play()
                    allKeys = []

                elif resp == quit_key:
                    advance_sound.play()
                    core.quit()

        #Update the block count.

        block_id+=1

        #Present 2s fixation before resuming trials.

        for i in range(120):
            fix.draw()
            win.flip()

#Now that we've looped through both blocks, close the file.

testFile.close()

#Present end screen.

end_screen = ['Great job!\n\n\nPlease wait for the experimenter.']

instruct.setText(text=end_screen[0])
allKeys = []
advance = 'false'

while advance == 'false':
    instruct.draw()
    win.flip()
    allKeys=event.waitKeys(keyList=[quit_key])

    if allKeys:
        core.quit()
