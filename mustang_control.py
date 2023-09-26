#!/usr/bin/env python3

###############################
# Mustang streamer controller #
###############################

import requests
import os
import time
import RPi.GPIO as GPIO
import json
import subprocess
import configparser



#### External config file
basedir = '/home/volumio/mustang_streamer/'
fileConfig = basedir + 'config.ini'
cfg_file = configparser.ConfigParser()
cfg_file.read(fileConfig)

# RGB Led pins (BCM)
pinR = int(cfg_file['mustang streamer config']['ledRed']) # default:23
pinG = int(cfg_file['mustang streamer config']['ledGreen']) # default:24
pinB = int(cfg_file['mustang streamer config']['ledBlue']) # default:25

# 3.3v -> switch ---> 10k -> GND
#                |_ 1k -> gpio_pin (pinRESET)	
pinRESET = int(cfg_file['mustang streamer config']['button']) # default:17
LONG_PRESS_TIME = 3.0  # in seconds

# Display poweroff timer
time_off = int(cfg_file['mustang streamer config']['timeout_display']) # Timeout display (in seconds) default:1200sec


### SETUP
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Button functions
def button(channel):

	print("Button pressed")

	start_time = time.time()
	while GPIO.input(channel) == GPIO.HIGH:
		# Check if is a long press or normal button press
		if time.time() - start_time > LONG_PRESS_TIME:
			print("- Long press! (more than "+str(LONG_PRESS_TIME)+" seconds)")
			os.system("volumio stop")
			led_rainbow()
			os.system("sudo systemctl reboot")
			return
		else:
			display_poweron()

		time.sleep(0.1)



# GPIO: Setup button
GPIO.setup(pinRESET, GPIO.IN, GPIO.PUD_DOWN)
GPIO.add_event_detect(pinRESET, GPIO.RISING, callback=button, bouncetime=500)


# GPIO: Setup RGB led pins
GPIO.setup(pinR,GPIO.OUT)
GPIO.setup(pinG,GPIO.OUT)
GPIO.setup(pinB,GPIO.OUT)

### General config
quality_txt = "-"		# Placeholder
rainbow_timer = 0.35	# Startup led rainbow wait time


##### FUNCTIONS #####
# Funzione per stato volumio
def status_volumio():
	# Volumio status
	response = requests.get("http://localhost:3000/api/v1/getState")
	volumio = response.json()

	if "samplerate" in volumio:
		raw_samplerate = volumio["samplerate"].split()
		raw_bit = volumio["bitdepth"].split()
		audio_samplerate = float(raw_samplerate[0])
		audio_bitrate = int(raw_bit[0])
	else:
		audio_samplerate = 0
		audio_bitrate = 0

	if "status" in volumio:	

		status = volumio["status"]

		if status == "play":
			print("In riproduzione")
			# Resetto il timer sleep display
			display_poweron()
			reset_timer_display()

			### AUDIO QUALITY ###
			# Audio DSD/DSF
			if audio_bitrate == 1: 

				if audio_samplerate < 5.6:
					quality_txt = "DSD64"
					led_Yellow()

				elif audio_samplerate < 11.2:
					quality_txt = "DSD128"
					led_Blue()

				elif audio_samplerate < 22.5:
					quality_txt = "DSD256"
					led_Purple()

				elif audio_samplerate < 45.1:
					quality_txt = "DSD512"
					led_Cyan()

				elif audio_samplerate >= 45.1:
					quality_txt = "DSD1024"
					led_White()

				else:
					quality_txt = "DSD format: unknown!"
					led_Red()

			# Audio 16bit
			elif audio_bitrate == 16:
				# Standard bitrate

				if audio_samplerate < 44:
					# Low quality
					quality_txt = "LOW"
					led_Red()

				elif 44 < audio_samplerate < 48:
					# 16bit - 44kHz
					quality_txt = "CD"
					led_Green()

				elif 48 <= audio_samplerate < 88:
					# 16bit - 48kHz
					quality_txt = "SACD"
					led_Yellow()

				elif 88 <= audio_samplerate < 96:
					# 16bit - 88kHz
					quality_txt = ""
					led_Blue()

				elif 96 <= audio_samplerate < 192:
					# 16bit - 96kHz
					quality_txt = ""
					led_Purple()

				elif audio_samplerate == 192:
					# 16bit - 192kHz
					quality_txt = ""
					led_Cyan()

				else: 
					# Unknown sample rate
					quality_txt = "Sample rate error"
					print("### Non definito: "+volumio["samplerate"]+" "+volumio["bitdepth"])


			# Audio 24bit
			elif audio_bitrate == 24:
				# High bitrate

				if 44 < audio_samplerate < 48:
					# 24bit - 44kHz
					quality_txt = ""
					led_Yellow()

				elif 48 <= audio_samplerate < 88:
					# 24bit - 48kHz
					quality_txt = ""
					led_Blue()

				elif 88 <= audio_samplerate < 96:
					# 24bit - 88kHz
					quality_txt = ""
					led_Purple()

				elif 96 <= audio_samplerate < 192:
					# 24bit - 96kHz
					quality_txt = ""
					led_Cyan()

				elif audio_samplerate == 192:
					# 24bit - 192kHz
					quality_txt = ""
					led_White()

				else: 
					# Unknown sample rate
					quality_txt = "Sample rate error"
					print("### Non definito: "+volumio["samplerate"]+" "+volumio["bitdepth"])
					led_Off()


			elif audio_bitrate == 0:
				# Transaction between local and streaming service
				quality_txt = "Changing music service..."
				led_Off()


			# Unknown format
			else:
				quality_txt = "Unknown format"
				led_Off()



				
			# Print audio quality on terminal
			print("Audio quality: "+quality_txt+" "+volumio["bitdepth"]+" "+volumio["samplerate"])


		elif status == "pause":
			print("In pausa")
			led_Off()
			set_timer_display()
		else:
			print("Fermo")
			led_Off()
			set_timer_display()

	else:
		# Stato non definito
		print("### Status non trovato! ###")
		led_Off()


# Funzione per play/pausa via pulsante
def volumio_playpausa():
	checkplay = requests.get("http://localhost:3000/api/v1/getState")
	playstatus = checkplay.json()

	if "status" in playstatus:
		stato = playstatus["status"]

		# Se e' in play: mette in pause
		if stato == "play":
			os.system('volumio pause')
			set_timer_display()
		# Se e' in pausa o stop: play!
		elif (stato == "pause" or stato == "stop"):
			display_poweron()
			os.system('volumio play')
			reset_timer_display()
		else:
			print("Stato player sconosciuto!")

	else:
		print("Nessuno stato! Errore connessione?")


# Funzione per spegnere il display
def display_poweroff():
	output = subprocess.getoutput("vcgencmd display_power")
	rawOut = output.split('=')
	verifica = int(rawOut[1])
	if verifica > 0:
		print('Spegnimento display!')
		os.system('vcgencmd display_power 0')
		reset_timer_display()


# Funzione per accendere il display
def display_poweron():
	output = subprocess.getoutput("vcgencmd display_power")
	rawOut = output.split('=')
	verifica = int(rawOut[1])
	if verifica == 0:
		print('WAKEUP display!')
		os.system('vcgencmd display_power 1')


# Funzione per mandare in sleep il monitor
def sleep_display():
	#print('check sleep')
	rawTimer = open("/tmp/timer_display.dat", "r")
	for line in rawTimer.readlines():
		last_timer = int(line)
	rawTimer.close()

	if last_timer > 0:
		tsNow = int( time.time() )
		# E' stato impostato un timestamp
		ts_limite = last_timer + time_off
		test = ts_limite - tsNow
		#print('DEBUG - tsNow:'+str(tsNow)+' Limite:'+str(last_timer)+' Rimanenti:'+str(test) )
		if tsNow > ts_limite:
			display_poweroff()


# Reset timer spegnimento display
def reset_timer_display():
	rawTimer = open("/tmp/timer_display.dat", "r")
	for line in rawTimer.readlines():
		last_timer = int(line)
	rawTimer.close()
	if last_timer > 0:
		timerfile = open("/tmp/timer_display.dat", "w")
		timerfile.write("0")
		timerfile.close()


# Imposta timer per spegnimento display
def set_timer_display():
	rawTimer = open("/tmp/timer_display.dat", "r")
	for line in rawTimer.readlines():
		last_timer = int(line)
	rawTimer.close()
	if last_timer == 0:
		print('- Imposto timestamp per spegnimento display')
		tsNow = str ( int( time.time() ) )
		timerfile = open("/tmp/timer_display.dat", "w")
		timerfile.write(tsNow)
		timerfile.close()




## Funzioni Led RGB
# Led spento
def led_Off():
	GPIO.output(pinR,GPIO.HIGH)
	GPIO.output(pinG,GPIO.HIGH)
	GPIO.output(pinB,GPIO.HIGH)

def led_Green():
    GPIO.output(pinR,GPIO.HIGH)
    GPIO.output(pinG,GPIO.LOW)
    GPIO.output(pinB,GPIO.HIGH)

def led_Red():
    GPIO.output(pinR,GPIO.LOW)
    GPIO.output(pinG,GPIO.HIGH)
    GPIO.output(pinB,GPIO.HIGH)

def led_Blue():
    GPIO.output(pinR,GPIO.HIGH)
    GPIO.output(pinG,GPIO.HIGH)
    GPIO.output(pinB,GPIO.LOW)

def led_White():
    GPIO.output(pinR,GPIO.LOW)
    GPIO.output(pinG,GPIO.LOW)
    GPIO.output(pinB,GPIO.LOW)

def led_Yellow():
    GPIO.output(pinR,GPIO.LOW)
    GPIO.output(pinG,GPIO.LOW)
    GPIO.output(pinB,GPIO.HIGH)

def led_Purple():
    GPIO.output(pinR,GPIO.LOW)
    GPIO.output(pinG,GPIO.HIGH)
    GPIO.output(pinB,GPIO.LOW)

def led_Cyan():
    GPIO.output(pinR,GPIO.HIGH)
    GPIO.output(pinG,GPIO.LOW)
    GPIO.output(pinB,GPIO.LOW)

# Sequenza arcobaleno avvio
def led_rainbow(quanti):
	for i in range(quanti):	
		print("Rainbow!")
		led_White()
		time.sleep(rainbow_timer)
		led_Purple()
		time.sleep(rainbow_timer)
		led_Blue()
		time.sleep(rainbow_timer)
		led_Cyan()
		time.sleep(rainbow_timer)
		led_Green()
		time.sleep(rainbow_timer)
		led_Yellow()
		time.sleep(rainbow_timer)
		led_Red()
		time.sleep(rainbow_timer)
	led_Off()

###### FINE FUNZIONI #######



### INIT ###
led_Off()
print("##### Mustang Streamer starting.. #####\n")
led_rainbow(1)

# imposta la variabile per il controllo sleep display
timerfile = open("/tmp/timer_display.dat", "w")
timerfile.write("0")
timerfile.close()



###### Main loop
try:
	while True:

		status_volumio()

		sleep_display()

		time.sleep(0.3)

except KeyboardInterrupt:
	print("\nUser interrupt..")
	GPIO.cleanup()

## Chiusura
GPIO.cleanup()
