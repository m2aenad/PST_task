#!/usr/bin/python

#PST training script.
#Last Updated: Jun 13, 2023
#Original Author: Dan Dillon
#Updated by: G Shearrer and Y Akmadjonova
#for the serial library, download pyserial (not serial)
#ports differ on different pc-s

import os
import math
import numpy as np
import pandas as pd
import serial
import sys
import socket
from psychopy import core, data, event, gui, misc, visual, prefs, monitors
from itertools import count, takewhile
from typing import Iterator
from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
# Set the audio preferences to use PTB first and then import psychopy.sound
prefs.hardware['audioLib'] = ['PTB','pyo','pygame','sounddevice']
from psychopy import sound
#import psychopy_sounddevice
import SerialHandler
import keyboard as keebee # need to do this to prevent overlap with psychopy keyboard
import serial
from PST_functions import *
from PST_setup import *


# don't forget to check the port in device manager (associated with cp210 driver)
# ser = serial.Serial('COM4', 9800)

wintype='pyglet' 
HOST_NAME = socket.gethostname()

# Timestamp Variables
dispense_time = None
taken_time = None


#Screen refresh duration. Not needed, but good fyi
refresh = 16.7

# Note
'''
Wait for candy to be dispensed
Beam break trigger + 5
'''

##GUI to get subject number, date.
info = settingsGUI()

# Dictionary for pickle file
pk = {}
pk.update({info['participant']:{
        'date': info['Date'],
        'fullscr':info['Fullscreen'], 
        'test?':info['test?']
}})
# Paths
stimpath = './Stims/'
datapath = os.path.join('.','Datapath')
adillyofapickle(datapath, pk, info['participant'])

# Global_variables
## Define response keys.
left_key = '1'
right_key = '4'
quit_key = 'q'
fdbk_dur = 5
baud = 9600

if info['Bluetooth'] == False:    
    SerialHandler.connect_serial(info['Com Port'],baud)
    ready = SerialHandler.command_to_send(SerialHandler.establishConnection)    

if ready == True:
    print('ready to start')
else:
    pk.update({'error':'could not establish connection})
    clean_quit(datapath, pk, info['participant'], task_clock)
# set visual parameters
parameters = set_visuals([600,400], False, 'MacAir', 'black', wintype, 'Text', 'center', 0.12, 350, 'white', 0.3, stimpath)
pk.update({'experiment_parameters':{}})


win = parameters['win']
instruct = parameters['instruct']
left_choice = parameters['left_choice']
right_choice = parameters['right_choice']
reward = parameters['reward']
zero = parameters['zero']
no_resp = parameters['no_resp']
fix = parameters['fix']

#set number of blocks, stimuli, and trials
num_blocks = 4
num_stims = 6
trials_per_stim = 10 # Number times stim on left out of 20 trials.
total_trials = trials_per_stim*num_stims

pk['experiment_parameters'].update({'settings': ['600','400','False','MacAir','black','pyglet','Text','center','0.12','350','white','0.3']})
pk['experiment_parameters'].update({'num_blocks': num_blocks})
pk['experiment_parameters'].update({'num_stims': num_stims})
pk['experiment_parameters'].update({'trials_per_stim': trials_per_stim})

# List of paths to images
pic_list = [os.path.join(stimpath,'1.bmp'), os.path.join(stimpath,'2.bmp'), os.path.join(stimpath,'3.bmp'), os.path.join(stimpath,'4.bmp'), os.path.join(stimpath,'5.bmp'), os.path.join(stimpath,'6.bmp')]

#Make master list of stim lists.
stim_names = stimulating(num_stims, trials_per_stim)
AB_trialList, CD_trialList, EF_trialList = make_it(stim_names)
small_blocks = block_it(AB_trialList, CD_trialList, EF_trialList)

#Shuffle bitmaps so images used as stims A, B, C, etc. vary across subjects.
stim_rand = stim_mapping(pic_list, datapath, info['participant'])

# Text
inst_text = [
'This is a new game, with\nchances to win more money.\n\nPress button 1 to advance.', 
'Two figures will appear\non the computer screen.\n\nOne figure will pay you more often\nthan the other, but at first you won\'t\nknow which figure is the good one.\n\nPress 1 to advance.', 
'Try to pick the figure that pays\nyou most often.\n\nWhen you see the REWARD screen,\nthat means you won bonus money!\n\nWhen you see the ZERO screen,\nyou did not win.\n\nPress 1 to advance.', 
'Keep in mind that no figure\npays you every time you pick it.\n\nJust try to pick the one\nthat pays most often.\n\nPress 1 to select the figure\non the left. Press 4 to select\nthe figure on the right.\n\nPress 1 to advance.', 
'At first you may be confused,\nbut don\'t worry.\n\nYou\'ll get plenty of chances.\n\nPress 1 to advance.', 
'There are 4 blocks of trials.\nEach one lasts about 8 minutes.\n\nMake sure to try all the figures\nso you can learn which ones\nare better and worse.\n\nPress button 1 to advance.']

allKeys = []
adillyofapickle(datapath, pk, info['participant'])

# Introduction    
intro(inst_text, instruct, win, allKeys, left_key, quit_key)
stim_matrix = starter(small_blocks, stim_rand, win)
last_text = ['Ready to begin, press o when you are comfortable']
advance = 'false'
k = ['']

#Run experimental trials.
for block_num, block in enumerate(range(num_blocks)):    
    while advance == 'false':
        pk.update({'data':{'%i'%block_num:{}}})
        instruct.setText(text=last_text[0])
        instruct.draw()
        win.flip()
        k = event.waitKeys()

        if k[0] == 'o':
            RT = core.Clock() # begin the reaction time clock
            task_clock = core.Clock() #begin the task clock
            advance = 'true'

        elif k[0] == 'q':
            core.quit()
    fix.draw()
    win.flip()
    
    
    #Run through the trials.

    for i in range(total_trials):

        trial_num = i + 1
        pk['data']['%i'%block_num].update({'%i'%trial_num:[]})

        #Prep the stims.

        left_stim = stim_matrix[trial_num-1][0]
        left_stim_name = stim_matrix[trial_num-1][1]
        left_stim_num = stim_matrix[trial_num-1][2]
        right_stim = stim_matrix[trial_num-1][3]
        right_stim_name = stim_matrix[trial_num-1][4]
        right_stim_num = stim_matrix[trial_num-1][5]
        scheduled_outcome = stim_matrix[trial_num-1][6]
        for x in [left_stim_name, left_stim_num, right_stim_name, right_stim_num, scheduled_outcome]:
            pk['data']['%i'%block_num]['%i'%trial_num].append(x)
        
        #Reset the RT clock and clear events
        RT.reset()
        event.clearEvents(eventType='keyboard')
        # present the stimuli and wait for key press
        key_press, stim_onset = present_stims(fix,left_stim, right_stim, win, left_key,right_key,quit_key, RT, task_clock, scheduled_outcome)
        ## log events in dict for pickle
        pk['data']['%i'%block_num]['%i'%trial_num].append(stim_onset) # stimulus onset
        pk['data']['%i'%block_num]['%i'%trial_num].append(key_press[0][0]) # keypress
        pk['data']['%i'%block_num]['%i'%trial_num].append(key_press[0][1]) # RT
        # Check accuracy
        acc = accuracy(left_stim_num, right_stim_num, key_press[0][0])
        pk['data']['%i'%block_num]['%i'%trial_num].append(acc) # accuracy
        # show response for 2 seconds
        response_update(key_press[0][0],win, left_stim, right_stim, left_choice, right_choice, task_clock, datapath, pk, info['participant'])
        core.wait(2.0)
        # show feedback and dispense candy here, right now it is waiting 3 sec 
        R, fdbk_onset = show_fdbk(acc, scheduled_outcome, task_clock, zero, win, reward, info['test?'])
        output = SerialHandler.read_from_port() #not sure what the output of this looks like, once I know then I can add it to the core wait time
        
        pk['data']['%i'%block_num]['%i'%trial_num].append(R) # reward or not
        pk['data']['%i'%block_num]['%i'%trial_num].append(fdbk_onset) # feedback onset
        # wait 3 seconds, update with dispense time when we have it
        core.wait(3.0)
        # pickle dump
        adillyofapickle(datapath, pk, info['participant'])
        
        # check what trial it is
        if trial_num == total_trials:
            adillyofapickle(datapath, pk, info['participant'])

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
                    allKeys = []

                elif resp == quit_key:
                    clean_quit(datapath, pk, info['participant'], task_clock)

# create a dataframe and save   
df = make_df(pk)
savepath = os.path.join(datapath,'%s'%info['participant'],'%s.csv'%info['participant'])
df.to_csv(savepath, index=False)