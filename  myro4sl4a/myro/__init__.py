"""
Tercer intento de adaptacion de la libreria myro 
a sl4a usando python 2.6
"""

import android, atexit,time,random,pickle,threading,os,types,copy
import StringIO, traceback, urllib, glob
import scribbler

def initialize():
	print "probando inicializacion"
init = initialize


def beep(duration=.5, frequency1=None, frequency2=None):
    if type(duration) in [tuple, list]:
        frequency2 = frequency1
        frequency1 = duration
        duration =.5
    if frequency1 == None:
        frequency1 = random.randrange(200, 10000)
    if type(frequency1) in [tuple, list]:
        if frequency2 == None:
            frequency2 = [None for i in range(len(frequency1))]
        for (f1, f2) in zip(frequency1, frequency2):
            if myro.globvars.robot:
                scribbler.Scribbler().beep(duration, f1, f2)
            # else:
                # computer.beep(duration, f1, f2)
    else:
        if scribbler.Scribbler():
            scribbler.Scribbler().beep(duration, frequency1, frequency2)
        # else:
            # computer.beep(duration, frequency1, frequency2)

def motors(left,right):
	return scribbler.Scribbler().motors(left,right)
	
def move(translate,rotate):
	return scribbler.Scribbler().move(translate,rotate)

def setLED(position, value):
	return scribbler.Scribbler().set("led", position, value)

def setLEDFront(value):
	return scribbler.Scribbler().setLEDFront(value)

def setLEDBack(value):
	return scribbler.Scribbler().setLEDBack(value)

def getBattery():
	return scribbler.Scribbler().getBattery()
	
def test():
	print "Funciona la importacion"
	#return scribbler.Scribbler()
	return scribbler.Scribbler().env()