"""
Scribler para android

"""

import time,string,threading
import sys,os.path
import android

def isTrue(value):
	if type(value) == str:
		return (value.lower() == "on")
	elif value: return True
	return False

droid=android.Android()
	
class Scribbler:

	SOFT_RESET=33
	GET_ALL=65 
	GET_ALL_BINARY=66  
	GET_LIGHT_LEFT=67  
	GET_LIGHT_CENTER=68  
	GET_LIGHT_RIGHT=69  
	GET_LIGHT_ALL=70  
	GET_IR_LEFT=71  
	GET_IR_RIGHT=72  
	GET_IR_ALL=73  
	GET_LINE_LEFT=74  
	GET_LINE_RIGHT=75  
	GET_LINE_ALL=76  
	GET_STATE=77  
	GET_NAME1=78
	GET_NAME2=64
	GET_STALL=79  
	GET_INFO=80  
	GET_DATA=81  

	GET_PASS1=50
	GET_PASS2=51

	GET_RLE=82  # a segmented and run-length encoded image
	GET_IMAGE=83  # the entire 256 x 192 image in YUYV format
	GET_WINDOW=84  # the windowed image (followed by which window)
	GET_DONGLE_L_IR=85  # number of returned pulses when left emitter is turned on
	GET_DONGLE_C_IR=86  # number of returned pulses when center emitter is turned on
	GET_DONGLE_R_IR=87  # number of returned pulses when right emitter is turned on
	GET_WINDOW_LIGHT=88    # average intensity in the user defined region
	GET_BATTERY=89  # battery voltage
	GET_SERIAL_MEM=90  # with the address returns the value in serial memory
	GET_SCRIB_PROGRAM=91  # with offset, returns the scribbler program buffer
	GET_CAM_PARAM=92 # with address, returns the camera parameter at that address

	GET_BLOB=95

	SET_PASS1=55
	SET_PASS2=56
	SET_SINGLE_DATA=96
	SET_DATA=97
	SET_ECHO_MODE=98
	SET_LED_LEFT_ON=99 
	SET_LED_LEFT_OFF=100
	SET_LED_CENTER_ON=101
	SET_LED_CENTER_OFF=102
	SET_LED_RIGHT_ON=103
	SET_LED_RIGHT_OFF=104
	SET_LED_ALL_ON=105
	SET_LED_ALL_OFF=106
	SET_LED_ALL=107 
	SET_MOTORS_OFF=108
	SET_MOTORS=109 
	SET_NAME1=110 
	SET_NAME2=119           # set name2 byte
	SET_LOUD=111
	SET_QUIET=112
	SET_SPEAKER=113
	SET_SPEAKER_2=114

	SET_DONGLE_LED_ON=116   # turn binary dongle led on
	SET_DONGLE_LED_OFF=117  # turn binary dongle led off
	SET_RLE=118             # set rle parameters 
	SET_DONGLE_IR=120       # set dongle IR power
	SET_SERIAL_MEM=121      # set serial memory byte
	SET_SCRIB_PROGRAM=122   # set scribbler program memory byte
	SET_START_PROGRAM=123   # initiate scribbler programming process
	SET_RESET_SCRIBBLER=124 # hard reset scribbler
	SET_SERIAL_ERASE=125    # erase serial memory
	SET_DIMMER_LED=126      # set dimmer led
	SET_WINDOW=127          # set user defined window
	SET_FORWARDNESS=128     # set direction of scribbler
	SET_WHITE_BALANCE=129   # turn on white balance on camera 
	SET_NO_WHITE_BALANCE=130 # diable white balance on camera (default)
	SET_CAM_PARAM=131       # with address and value, sets the camera parameter at that address

	GET_JPEG_GRAY_HEADER=135
	GET_JPEG_GRAY_SCAN=136
	GET_JPEG_COLOR_HEADER=137
	GET_JPEG_COLOR_SCAN=138

	SET_PASS_N_BYTES=139
	GET_PASS_N_BYTES=140
	GET_PASS_BYTES_UNTIL=141

	GET_VERSION=142

	GET_IR_MESSAGE = 150
	SEND_IR_MESSAGE = 151
	SET_IR_EMITTERS = 152

	SET_START_PROGRAM2=153   # initiate scribbler2 programming process
	SET_RESET_SCRIBBLER2=154 # hard reset scribbler2
	SET_SCRIB_BATCH=155      # upload scribbler2 firmware
	GET_ROBOT_ID=156

	PACKET_LENGTH     =  9

	droid=android.Android()
	
	def __init__(self):
		self.startbluetooth()
		self.lock=threading.Lock()
		##Variables a inicializarse
		self._lastTranslate = 0
		self._lastRotate    = 0
		self.requestStop = 0
		self.debug=0
		self.dongle=None
	def move(self, translate, rotate):
		self._lastTranslate = translate
		self._lastRotate = rotate
		self._adjustSpeed()
	# def set(self, item, position, value = None):
		# item = item.lower()
		# if item == "led":
			# if type(position) in [int, float]:
				# if position == 0:
					# if isTrue(value): return self._set(Scribbler.SET_LED_LEFT_ON)
					# else:             return self._set(Scribbler.SET_LED_LEFT_OFF)
				# elif position == 1:
					# if isTrue(value): return self._set(Scribbler.SET_LED_CENTER_ON)
					# else:             return self._set(Scribbler.SET_LED_CENTER_OFF)
				# elif position == 2:
					# if isTrue(value): return self._set(Scribbler.SET_LED_RIGHT_ON)
					# else:             return self._set(Scribbler.SET_LED_RIGHT_OFF)
				# else:
					# raise AttributeError("no such LED: '%s'" % position)
			# else:
				# position = position.lower()
				# if position == "center":
					# if isTrue(value): return self._set(Scribbler.SET_LED_CENTER_ON)
					# else:             return self._set(Scribbler.SET_LED_CENTER_OFF)
				# elif position == "left":
					# if isTrue(value): return self._set(Scribbler.SET_LED_LEFT_ON)
					# else:             return self._set(Scribbler.SET_LED_LEFT_OFF)
				# elif position == "right":
					# if isTrue(value): return self._set(Scribbler.SET_LED_RIGHT_ON)
					# else:             return self._set(Scribbler.SET_LED_RIGHT_OFF)
				# elif position == "front":
					# return self.setLEDFront(value)
				# elif position == "back":
					# return self.setLEDBack(value)
				# elif position == "all":
					# if isTrue(value): return self._set(Scribbler.SET_LED_ALL_ON)
					# else:             return self._set(Scribbler.SET_LED_ALL_OFF)
				# else:
					# raise AttributeError("no such LED: '%s'" % position)
	def setLEDBack(self, value):
		if value > 1:
			value = 1
		elif value <= 0:
			value = 0
		else:
			value = int(float(value) * (255 - 170) + 170) # scale
		try:
			self.lock.acquire()
			self.droid.bluetoothWrite(unichr(Scribbler.SET_DIMMER_LED))
			print value
			print chr(value)
			# val2=unicode(value,"utf-8")
			# print val2
			# t=val2.enconde()
			self.droid.bluetoothWrite(unichr(value))
		finally:
			self.lock.release()
					
	def setLEDFront(self, value):
		value = int(min(max(value, 0), 1))
		try:
			self.lock.acquire()
			if isTrue(value):
				self.droid.bluetoothWrite(unichr(Scribbler.SET_DONGLE_LED_ON))
			else:
				self.droid.bluetoothWrite(unichr(Scribbler.SET_DONGLE_LED_OFF))
		finally:
			self.lock.release()
		
	def _adjustSpeed(self):
		left  = min(max(self._lastTranslate - self._lastRotate, -1), 1)
		right  = min(max(self._lastTranslate + self._lastRotate, -1), 1)
		leftPower = (left + 1.0) * 100.0
		rightPower = (right + 1.0) * 100.0
		self._set(Scribbler.SET_MOTORS, rightPower, leftPower)
	
	def _write(self, rawdata):
		print rawdata
		t = map(lambda x: unichr(int(round(x))).encode('utf8'), rawdata)
		# tp = map(lambda x: unichr(int(round(x))), rawdata)
		t2=''
		print t
		for k in t:
			t2=t2+k
		# data2 = string.join(tp, '') + (chr(0) * (Scribbler.PACKET_LENGTH - len(t)))[:9]
		self.droid.makeToast(t2)
		
		# data=t2+(unichr(0) * (Scribbler.PACKET_LENGTH - len(t)))[:9]
		data=t2+(unichr(0).encode('utf8') * (Scribbler.PACKET_LENGTH - len(t)))
		data=data[:9]
		print data
		# print data2
		# print string.join(t, '')
		print "La longitud del paquete es: "+str(len(t))
		print "El char de cero es "+chr(0)
		print chr(0)*(Scribbler.PACKET_LENGTH - len(t))
		print (chr(0) * (Scribbler.PACKET_LENGTH - len(t)))[:9]
		
		# print data
		self.droid.makeToast(data)
		if self.debug:
			print "_write:", data, len(data),
			print "data:",
			print map(lambda x:"0x%x" % ord(x), data)
		if self.dongle == None:
			time.sleep(0.01) # HACK! THIS SEEMS TO NEED TO BE HERE!
		# self.ser.write(data)      # write packets
		# print data
		self.droid.bluetoothWrite(data) 
	
	def _set(self, *values):
		try:
			self.lock.acquire() #print "locked acquired"
			print values
			self._write(values)
			# test = self._read(Scribbler.PACKET_LENGTH) # read echo
			# self._lastSensors = self._read(11) # single bit sensors
            #self.ser.flushInput()
			
			# if self.requestStop:
				# self.requestStop = 0
				# self.stop()
				# self.lock.release()
				# raise KeyboardInterrupt
		finally:
			self.lock.release()
	
	def startbluetooth(self):
		#droid = android.Android()
		uuid = '00001101-0000-1000-8000-00805F9B34FB'
		self.droid.dialogCreateAlert( "Elija una operacion" )
		self.droid.dialogSetPositiveButtonText( "Conectarse como cliente" )
		self.droid.dialogSetNegativeButtonText( "Cancelar" )
		self.droid.dialogShow()
		ret = self.droid.dialogGetResponse().result[ "which" ]
		if ret == "positive":
			ret = self.droid.bluetoothConnect( uuid ).result
			if not ret:
				self.droid.makeToast( "bluetooth not connected" )
				sys.exit( 0 )
			return True
		print "skip bt setup"
		return False
	
	
	def motors(self, left, right):
		trans = (right + left) / 2.0
		rotate = (right - left) / 2.0
		print trans
		print rotate
		return self.move(trans, rotate)
	
	def stop(self):
		self._lastTranslate=0
		self._lastRotate=0
		return self._set(Scribbler.SET_MOTORS_OFF)
	
	
	def getBattery(self):
		# try:
			# self.lock.acquire()
		self.droid.bluetoothWrite(unichr(self.GET_LIGHT_LEFT))
		# while True:
		if self.droid.bluetoothReadReady():
			print "LOL!"
			while True:
				# print self.droid.bluetoothRead()
				a=self.droid.bluetoothReadLine().result
				b=self.droid.bluetoothRead().result
				droid.makeToast(a)
				droid.makeToast(b)
					# print chr(a)
					# print b
		else:
			print "NO PASO NADA"
			# retval=self.read_2byte()/20.9813
			# self.droid.makeToast(str(retval))
		# finally:
			# self.lock.release()
		# return retval
	
	# def read_2byte():
    # hbyte = ord(self.droid.bluetoothRead())
    # lbyte = ord(self.droid.bluetoothRead())
    # lbyte = (hbyte << 8) | lbyte
    # return lbyte
	
	def env(self):
		self.droid.bluetoothWrite(chr(self.SET_LED_ALL_ON))