# About
Working Example for Raspberry Pi 3.

# Procedure

## Install Pd-extended
http://support.tetrastyle.net/rpi/puredata/

## Check your I/O with pd-rpi-workshop
https://github.com/sebpiq/pd-rpi-workshop

I used Rocksmith Real tone Cable for Input and standard for output.

## Make Electric Works
http://barubora3.net/?p=279

Circuit diagram is perfect, but scripts at this site are old and doesn't works.

## Run sctipt

* Clone this Project to /home/pi/rpieffectbox
* Run

```shell
sudo python main.py
```

# Changed I Mede

* Edited path
* Changed Serial to /dev/serial0
* Made Function to be called once on GPIO.RISING
* Changed 2nd button to trigger Knob enabled/disabled
* Add I/O option when calling server.pd
* Added 'loadbang' then ';pd dsp 1' to All patches(Necessary to enable DSP on load)
