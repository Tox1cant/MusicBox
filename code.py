#############################################################################################################
#libraries
import os
import board
import audiomp3
import audiopwmio
from adafruit_debouncer import Debouncer
import digitalio
import time
import busio
import sdcardio
import storage
import adafruit_sdcard
import array
import supervisor
#############################################################################################################
#SD card implementation and defenitions Raspberry Pi Pico Gen 1 
spi = busio.SPI(clock=board.GP10, MOSI=board.GP11, MISO=board.GP12) #define SPI comms on the controller
cs = digitalio.DigitalInOut(board.GP13) #define Chip Select
sdcard = adafruit_sdcard.SDCard(spi, cs) #define SD Card using SPI and SC
vfs = storage.VfsFat(sdcard) #MicroPython implements a Unix-like Virtual File System (VFS) layer
storage.mount(vfs, '/sd') #Mounting the VFS
directory = os.listdir('/sd') #lists all files in directory /sd
extension = '*.mp3'
#############################################################################################################
#audio variables and defenitions
audio = audiopwmio.PWMAudioOut(board.GP15) #Audio out + pin (PWM)  
#############################################################################################################
#switch for music switching and definitions
pin = digitalio.DigitalInOut(board.GP0) #Switch PIN (pull up high) open circuit = 1(true or high)
pin.direction = digitalio.Direction.INPUT
pin.pull = digitalio.Pull.UP #pulling up the current
switch = Debouncer(pin) #debouncing the switch
#############################################################################################################
#LED controls for debuging
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT #Turns on led if boar is working!!
#/sd/songs.txt
#with open("/sd/songs.txt", "r") as inputfile:        
#        for line in inputfile:
#            print(line)
#############################################################################################################
SongArray = []
#print (directory)#debugging code for cheking
#print (SongArray)#debugging code for cheking
for filename in directory:
    if "mp3" in filename:
        SongArray.append(filename)
        #print(SongArray) #debugging code for cheking
SongArray.sort()
#print(SongArray)#debugging code for cheking

while True:
    led.value = True  
    #switch.update()
    #if switch.rose:
    #if pin.value == True: 
    increment = 0
    while not pin.value == True: time.sleep(0.2)

        #count += 1 #debug code for switch cheking
    for i in SongArray:
        increment+=1
        #print(increment)#debugging code for cheking
        SongNumber = len(SongArray)
        #print(SongNumber)#debugging code for cheking
        #print ("first", pin.value)
        if pin.value == True: 
            #print("{}".format(count, line)) # debug code for the switch cheking
            #song_playing = line
            mp3 = open("/sd/" + i, "rb") 
            decoder = audiomp3.MP3Decoder(mp3)
            time.sleep(0.5) 
            audio.play(decoder)
            while audio.playing: #while music is playing its cheking if the switch is updated
                switch.update()
                if switch.fell and increment == SongNumber:
                    supervisor.reload()
                    break
                if switch.fell and increment < SongNumber: #if switch does fall it checks the pin state before skipping
                    #print ("switch fell", pin.value)#debugging code for cheking
                    
                    audio.stop() #stops music
                    while not pin.value == True: time.sleep(0.2)#indefinet sleep unless you open the switch again
                    #print ("switch rise", pin.value)#debugging code for cheking
                    
                    break
       
    #print ("we left loop 1 enpty array index")#debugging code for cheking
    while pin.value == True:
        #print("you fell asleep listening to music")#debugging code for cheking
        
        switch.update()
        if switch.fell:
            #print("switch fell")#debugging code for cheking
            while not pin.value == True: time.sleep(0.2)
            time.sleep(1)
            break
        time.sleep(0.5)
                
    #print("Start from the Top of List Again BB!")#debugging code for cheking  
        
