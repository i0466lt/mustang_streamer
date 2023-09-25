# Mustang Streamer control

![Mustang Streamer logo](https://www.oluo.it/public/mustang1_1480x320.jpg)

Touch display and led pushbutton for Volumio 3


Descrizione da fare....


![Mustang Streamer](https://www.oluo.it/public/mustang1.jpg)



## Hardware
- [Waveshare POE IO Board for Raspberry CM4](https://www.waveshare.com/product/compute-module-4-poe-board-b.htm)
- Raspberry CM4 8Gb emmc
- [Waveshare 11.9 inch touch display](https://www.waveshare.com/11.9inch-hdmi-lcd.htm)
- Pushbutton with RGB led
- 3x 120Ohm 1/4W resistors
- 1x 1k 1/4W resistor
- 1x 10k 1/4W resistor
- Raspberry compatible soundcard (in this project is DIGI2 Pro by HiFiBerry)
- Adapter cables (based on your enclosure)
- Some spare GPIO Jumper cables
- RCA Panel connector
- 1x RCA Jack
- Shielded audio cable
- Passthrough Ethernet connector
- Cat 5 Ethernet cable (short)
- Termorestringente?!?!?!



![Internal view](https://www.oluo.it/public/mustang3-int.jpg)

## Scheme

![GPIO](https://www.oluo.it/public/mustang_gpio.jpg)

Used pins
| |  |
|--|--|
| Switch | GPIO17 |
| Led Red | GPIO23 |
| Led Green | GPIO24 |
| Led Blue | GPIO25 |

Please note, the RGB led in the switch is ***common anode*** without internal resistor.


## Volumio plugin
Install ***Now playing*** and ***Touch display*** plugin from Volumio3 plugin menu

## Volumio3 configuration

- Under installed plugins, set ***Screensaver timeout*** to 0 in Touch Display Configuration

- Make your favourite layout by editing parameters in Now Playing Configuration

- If you want, you can set Mustang Streamer background for idle screen by selecting `mustang1_1480x320.jpg` under Now Playing Configuration -> Idle Screen

![Idle backgroung](https://www.oluo.it/public/mustang1_1480x320.jpg)



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


## mustang_control.py
The main script


# HOW-TO: Use other GPIO Pin
You can change the PIN Number in mustang_control.py
Make sure the GPIO Pin are unused. You can check by running `gpio readall` from terminal


## Note for Raspberry CM4 users

Make sure you are running gpio version ***>= 2.70*** otherwise the CM4 GPIO is not recognized

***gpio -v***

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

# TO-DO

- Metti qui...

### Version 0.2
- Added background new image for idle screen

### Version 0.1
Initial version. 



