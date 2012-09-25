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