#!/usr/bin/python

#fMRI PST training script.
#Last Updated: Sep 8, 2022
#Last updated by Yana Oct 6
#Original Author: Dan Dillon
#Updated by: G Shearrer and Y Akmadjonova
#for the serial library, download pyserial (not serial)
#ports differ on different pc-s
#datapath may need updating on another pc

import os
from math import floor
import numpy as np
import pandas as pd
from psychopy import core, data, event, gui, misc, sound, visual
import serial
from PST_functions import *
from PST_setup import *

# don't forget to check the port in device manager (associated with cp210 driver)
# ser = serial.Serial('COM4', 9800)

wintype='pyglet' 

#Screen refresh duration. Not needed, but good fyi
refresh = 16.7

# Note
'''
Wait for candy to be dispensed
Beam break trigger + 5
'''


##GUI to get subject number, date.
info = {}

info['fullscr'] = False
info['test?'] = False
#info['port'] = '/dev/tty.usbserial'
info['participant'] = 'test'
info['Bluetooth'] = False
info['computer']= 'enter computer name here'
#info['Com_port']
info['dateStr'] = data.getDateStr()
#if info['Bluetooth'] == False:

dlg = gui.DlgFromDict(info)

if dlg.OK:
    misc.toFile('PST_fMRI_lastParams.pickle', info) 
else:
    core.quit()
#/Users/gracer/Library/CloudStorage/OneDrive-SharedLibraries-UniversityofWyoming/M2AENAD Lab - Documents/RESEARCH/GRRL/PST
pk = info

stimpath = './Stims/'
datapath = os.path.join('.','Datapath')
adillyofapickle(datapath, pk, info['participant'])

# Global_variables
#    ser = serial.Serial(info['Com_port'], 9600, write_timeout = 3)
## Define response keys.
left_key = '1'
right_key = '4'
quit_key = 'q'
fdbk_dur = 5

parameters = set_visuals([600,400], False, 'MacAir', 'black', wintype, 'Text', 'center', 0.12, 350, 'white', 0.3, stimpath)
win = parameters['win']
instruct = parameters['instruct']
left_choice = parameters['left_choice']
right_choice = parameters['right_choice']
reward = parameters['reward']
zero = parameters['zero']
no_resp = parameters['no_resp']
fix = parameters['fix']
num_blocks = 4
num_stims = 6
trials_per_stim = 10 # Number times stim on left out of 20 trials.
total_trials = trials_per_stim*num_stims

pic_list = [os.path.join(stimpath,'1.bmp'), os.path.join(stimpath,'2.bmp'), os.path.join(stimpath,'3.bmp'), os.path.join(stimpath,'4.bmp'), os.path.join(stimpath,'5.bmp'), os.path.join(stimpath,'6.bmp')]



#train_file = os.path.join(datapath, '%s_%s_PST_fMRI_train.csv'%(info['participant'], info['dateStr']))
#trainFile = open(train_file, 'w')
#trainFile.write('block,trial_num,left_stim,left_stim_number,right_stim,right_stim_number,object_onset,object_duration,response,response_onset,trial_RT,accuracy,isi_onset,isi_duration,scheduled_outcome,feedback,feedback_onset,feedback_duration,iti_onset,iti_duration\n')
#

#Make master list of stim lists.
stim_names = stimulating(num_stims, trials_per_stim)
AB_trialList, CD_trialList, EF_trialList = make_it(stim_names)
small_blocks = block_it(AB_trialList, CD_trialList, EF_trialList)

#Shuffle bitmaps so images used as stims A, B, C, etc. vary across subjects.
#stim_rand = {'stim_A':pic_list[0], 'stim_C':pic_list[1], 'stim_E':pic_list[2], 'stim_F':pic_list[3], 'stim_D':pic_list[4], 'stim_B':pic_list[5]}
stim_rand = stim_mapping(pic_list, datapath, info['participant'])

parameters.update({'num_blocks':num_blocks,'num_stims':num_stims, 'trials_per_stim':trials_per_stim, 'stim_names':stim_names, 'small_blocks':small_blocks, 'stim_rand':stim_rand})
pk.update({'experiment_parameters':parameters})

#Clocks.

RT = core.Clock()
task_clock = core.Clock()



##Start the study.

inst_text = [
'This is a new game, with\nchances to win more money.\n\nPress button 1 to advance.', 
'Two figures will appear\non the computer screen.\n\nOne figure will pay you more often\nthan the other, but at first you won\'t\nknow which figure is the good one.\n\nPress 1 to advance.', 
'Try to pick the figure that pays\nyou most often.\n\nWhen you see the REWARD screen,\nthat means you won bonus money!\n\nWhen you see the ZERO screen,\nyou did not win.\n\nPress 1 to advance.', 
'Keep in mind that no figure\npays you every time you pick it.\n\nJust try to pick the one\nthat pays most often.\n\nPress 1 to select the figure\non the left. Press 4 to select\nthe figure on the right.\n\nPress 1 to advance.', 
'At first you may be confused,\nbut don\'t worry.\n\nYou\'ll get plenty of chances.\n\nPress 1 to advance.', 
'There are 4 blocks of trials.\nEach one lasts about 8 minutes.\n\nMake sure to try all the figures\nso you can learn which ones\nare better and worse.\n\nPress button 1 to advance.']

allKeys = []

# Introduction    
intro(inst_text, instruct, win, allKeys, left_key, quit_key)

#Run experimental trials.
for block_num, block in enumerate(range(num_blocks)):    
    #Check-in 
    
    stim_matrix = starter(small_blocks, stim_rand, win)
    last_text = ['Ready to begin, press o when you are comfortable']

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
    fix.draw()
    win.flip()
    
    #Run through the trials.

    for i in range(total_trials):

        trial_num = i + 1

        #Clear buffers.

        event.clearEvents()
        allKeys=[]
        resp=[]
        trial_RT=[]

        #Prep the stims.

        left_stim = stim_matrix[trial_num-1][0]
        left_stim_name = stim_matrix[trial_num-1][1]
        left_stim_num = stim_matrix[trial_num-1][2]
        right_stim = stim_matrix[trial_num-1][3]
        right_stim_name = stim_matrix[trial_num-1][4]
        right_stim_num = stim_matrix[trial_num-1][5]
        scheduled_outcome = stim_matrix[trial_num-1][6]


        #Reset the RT clock. 
        check_key = event.getKeys(keyList=[quit_key],  timeStamped=task_clock)
        print(check_key)
        check_quit(check_key, datapath, pk, info['participant'])
        RT.reset()
        event.clearEvents(eventType='keyboard')
        key_press = present_stims(fix,left_stim, right_stim, win, left_key,right_key,quit_key, RT, task_clock, scheduled_outcome)
        acc = accuracy(left_stim_num, right_stim_num, key_press[0][0])
        response_update(key_press[0][0],win, left_stim, right_stim, left_choice, right_choice, task_clock)
        core.wait(2.0)
        show_fdbk(acc, scheduled_outcome, task_clock, zero, win, reward, info['test?'])
        core.wait(3.0)

        #Write out the data.


        #Fade out with lastHRF fixation cross after 60 trials.
        
        if trial_num == 60: 
            elapsed_time = task_clock.getTime()
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

   

#Now that we've looped over all the blocks, close the training file.

trainFile.close()



#Close the rating file.

PST_Rate_Data_File.close()