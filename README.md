# Bluefruit UART Utilities

This repo contains some utilities for using my Raspberry Pi to talk to a Bluefruit UART module. I'm using it for some quick debugging - I'm trying to send signals to the Bluefruit with a microcontroller, and it's useful to be able to do some debugging with another device.

Note that there is some preliminary setup. It's necessary to first enable serial communication on your pi by running:
`sudo raspi-config`

In the menu, go to interfacing, serial. Set "login prompt through serial" to "No", and "enable uart hardware" to "Yes.
## BLE Keyboard Interface

I enable the GATT over HID keyboard support with:

AT+BLEHIDEN=1

ATZ

### Send keys

AT+BLEKEYBOARD=something I send
