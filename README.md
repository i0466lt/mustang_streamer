# Mustang Streamer control (v.0.4)

![Mustang Streamer logo](https://www.oluo.it/public/mustang1_1480x320.jpg)

Mustang Streamer is a personal project that runs Volumio3 installed on a Raspberry CM4 with HiFiBerry sound card, 11.9" touch display, led pushbutton (changing color based on audio sample rate) and POE powered. Only two cables: Ethernet and Optical output.

This software works on Raspberry CM4, Raspberry Pi 3, Raspberry Pi 4. Feel free to test on other platforms and please report the issues.

## Main features
- Turn off display after desired idle time
- Wake up display automatically when player resume
- Led changing color with different sample-rates
- Wake up with button
- Play/pause with button short press
- Power off or reboot CM4 with button long press

![Mustang Streamer](https://www.oluo.it/public/mustang_main.jpg)


## RGB Led configuration

### PCM Formats (FLAC, MP3, Tidal, Spotify...)

| Sample rate | 16bit | 24bit |
|--------|--------|--------|
| <44kHz | Red    | -      |
| 44kHz  | Green  | Yellow |
| 48kHz  | Yellow | Blue   |
| 88kHz  | Blue   | Purple |
| 96kHz  | Purple | Cyan   |
| 192kHz | Cyan   | White  |

### DSD/DSF Formats

| Format  | 1bit   |
|---------|--------|
| DSD64   | Yellow |
| DSD128  | Blue   |
| DSD256  | Purple |
| DSD512  | Cyan   |
| DSD1024 | White  |


___

# Hardware
- [Waveshare POE IO Board for Raspberry CM4](https://www.waveshare.com/product/compute-module-4-poe-board-b.htm)
- Raspberry CM4 8Gb emmc
- [Waveshare 11.9 inch touch display](https://www.waveshare.com/11.9inch-hdmi-lcd.htm)
- [Pushbutton with RGB led](https://it.rs-online.com/web/p/interruttori-a-pulsante/1759645)
- 3x 120Ohm 1/4W resistors
- 1x 1k 1/4W resistor
- 1x 10k 1/4W resistor
- Raspberry compatible soundcard (in this project is [DIGI2 Pro by HiFiBerry](https://www.hifiberry.com/shop/boards/hifiberry-digi2-pro/))
- Adapter cables (based on your enclosure)
- Some spare GPIO Jumper cables
- RCA Panel connector
- 1x RCA Jack
- Shielded audio cable
- Passthrough Ethernet connector
- Cat 5 Ethernet cable (short)
- Shrinking hose
- Hey, obiouvsly, a box! 



![Internal view](https://www.oluo.it/public/mustang3-int.jpg)


Waveshare wide touch display is very ***very*** nice! 

..but making the square hole in the front panel is a nightmare, this display have about 2mm border and a flatcable on one side.. my suggestion: rasps and files (and be patient, self control, yoga, some cigarettes, no swear)!

## Schematics

![GPIO](https://www.oluo.it/public/mustang_gpio.jpg)

Used pins:

| HW        | PIN BCM |
|-----------|---------|
| Switch    | GPIO17  |
| Led Red   | GPIO23  |
| Led Green | GPIO24  |
| Led Blue  | GPIO25  |

Please note, the RGB led in the switch is ***common anode*** without internal resistor.


# Installation
Make sure you have enabled SSH access to your volumio installation. 

From a terminal, log into your device with `ssh volumio@YOURVOLUMIOIP` and:

```
git clone https://github.com/i0466lt/mustang_streamer.git
cd mustang_streamer
./setup.sh
```
Reboot your device with `sudo reboot`

# Basic configuration

## Volumio plugin
Install ***Now playing*** and ***Touch display*** plugin from Volumio3 plugin menu

## Volumio3 configuration

- Under installed plugins, set ***Screensaver timeout*** to 0 in Touch Display Configuration

- Make your favourite layout by editing parameters in Now Playing Configuration

- If you want, you can set Mustang Streamer background for idle screen by selecting `mustang1_1480x320.jpg` under Now Playing Configuration -> Idle Screen

![Mustang streamer idle background](https://www.oluo.it/public/mustang1_1480x320.jpg)



## OS tweaks

### /boot/userconfig.txt
Add these lines to your /boot/userconfig.txt to set your Waveshare display. (Also enables USB for touchscreen)
```
# Enable USB on Waveshare POE IO Board
dtoverlay=dwc2,dr_mode=host


#### Config for waveshare 11.9" HDMI touch display
hdmi_force_hotplug=1
max_framebuffer_height=1480
hdmi_group=2
hdmi_mode=87
hdmi_timings=320 0 80 16 32 1480 0 16 4 12 0 0 0 60 0 42000000 3
## Display rotation
display_rotate=3 #1: 90; 2: 180; 3: 270
```

## Main configuration file (config.ini)

This file contains the pin number assignments and display timeout (in seconds).

Change settings based on your needs.

| Parameter | default | options |
|-----------|---------|---------|
| ledRed | 23 | Control red part of RGB led |
| ledGreen | 24 | Control green part of RGB led |
| ledBlue | 25 | Control blue part of RGB led |
| button | 17 | Button pin |
| timeout_display | 1200 | Seconds before turn off display |
| long_press | reboot | Choose between poweroff or reboot |



# Update

Login into Volumio device via SSH, enter the `mustang_control` directory and issue `./update.sh`



# HOW-TO: Use other GPIO Pin

You can change the PIN Number in `config.ini` file.

Make sure the desired GPIO Pins are unused. You can check by running `gpio readall` from terminal.


If you don't have the `gpio` command install ***WiringPi unofficial fork*** at [https://github.com/WiringPi/WiringPi](https://github.com/WiringPi/WiringPi). I suggest to install the unofficial fork because WiringPi development ceased some years ago. The unofficial fork works and grant support to new hardware like CM4.


## Note for Raspberry CM4 users

If you are running a Raspberry CM4, make sure you are running `gpio` version ***>=2.70*** otherwise the CM4 GPIO is not recognized by `gpio readall` command. You can check your version by type `gpio -v` in the volumio device terminal.

Example fom my device:

```
gpio version: 2.70
Copyright (c) 2012-2018 Gordon Henderson
This is free software with ABSOLUTELY NO WARRANTY.
For details type: gpio -warranty

Raspberry Pi Details:
  Type: CM4, Revision: 00, Memory: 2048MB, Maker: Sony 
  * Device tree is enabled.
  *--> Raspberry Pi Compute Module 4 Rev 1.0
  * This Raspberry Pi supports user-level GPIO access.
```

# Mustang Streamer logo

Yes, I love Deftones! The horse on the logo comes from the album ***white pony***. I've used as part of this useless/non-commercial/diy/free project. (Chino, if you disagree please drop me a mail!)

If you want to make more background images with this logo, you'll find the SVG vector file under the `logo` folder.


## Background image

Background image is based on artwork by [freepik.com](https://it.freepik.com/foto-gratuito/composizione-astratta-della-luce-ultravioletta-uv_21794910.htm#query=background%20neon&position=9&from_view=search&track=ais)


# TO-DO

- Much to do!!

Feel free to open issues, comment and contribute!

