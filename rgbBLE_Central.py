# -*- coding: utf-8 -*-
"""
/******************************************************************* 
  ProtoStax Arduino Nano 33 BLE Sense RGB LED Control Central Device

  This is a example sketch for controlling the RGB LED on an 
  Arduino Nano 33 BLE Sense with Bluetooth over Python  
   
  Items used:
  Arduino Nano 33 BLE Sense
  ProtoStax for BreadBoard/Custom Boards - 
      - to house and protect the Nano and allow for other circuitry 
      --> https://www.protostax.com/collections/all/products/protostax-for-breadboard
  
  The Nano publishes a Bluetooth LE Client profile with Characteristics for the Red, Green, 
  and Blue components of the onboard RGB LED. These can be read and written to
  control the LED colors.

  This program toggles the R,G,B LEDs based on user input. Run the python program from your computer
  (PC, Mac or Linux) that has Bluetooth support and the requisite python packages - 
  you can then read and set the on/off states of the 3 colors. 
  
  The Red, Green and Blue colors of the onboard RGB LED can only be turned on or off. 
  It is not possible to use PWM to mix colors, unfortunately, based on how the Arduino 
  Nano BLE Sense board is configured.
  
  We write a value of 1 to turn on a color and 0 to turn it off. The user inputs 
  a string that can contain r,g,b (or any combination) and those colors will be toggled. 

  The Arduino Nano 33 BLE Sense is chockful of other sensors - you can similarly expose 
  those sensors data as Characteristics
 
  Written by Sridhar Rajagopal for ProtoStax
  BSD license. All text above must be included in any redistribution
 */
"""


import logging
import asyncio
import platform
import ast

from bleak import BleakClient
from bleak import BleakScanner
from bleak import discover

# These values have been randomly generated - they must match between the Central and Peripheral devices
# Any changes you make here must be suitably made in the Arduino program as well

RED_LED_UUID = '13012F01-F8C3-4F4A-A8F4-15CD926DA146'
GREEN_LED_UUID = '13012F02-F8C3-4F4A-A8F4-15CD926DA146'
BLUE_LED_UUID = '13012F03-F8C3-4F4A-A8F4-15CD926DA146'

on_value = bytearray([0x01])
off_value = bytearray([0x00])

RED = False
GREEN = False
BLUE = False


def getValue(on):
    if on:
        return on_value
    else:
        return off_value

async def setColor(client):
    global RED, GREEN, BLUE
    val = input('Enter rgb to toggle red, green and blue LEDs :')
    print(val)

    if ('r' in val):
        RED = not RED
        await client.write_gatt_char(RED_LED_UUID, getValue(RED))
    if ('g'in val):
        GREEN = not GREEN
        await client.write_gatt_char(GREEN_LED_UUID, getValue(GREEN))
    if ('b' in val):
        BLUE = not BLUE
        await client.write_gatt_char(BLUE_LED_UUID, getValue(BLUE))
    

async def run():
    global RED, GREEN, BLUE

    print('ProtoStax Arduino Nano BLE LED Peripheral Central Service')
    print('Looking for Arduino Nano 33 BLE Sense Peripheral Device...')

    found = False
    devices = await discover()
    for d in devices:       
        if 'Arduino Nano 33 BLE Sense'in d.name:
            print('Found Arduino Nano 33 BLE Sense Peripheral')
            found = True
            async with BleakClient(d.address) as client:
                print(f'Connected to {d.address}')
                val = await client.read_gatt_char(RED_LED_UUID)
                if (val == on_value):
                    print ('RED ON')
                    RED = True
                else:
                    print ('RED OFF')
                    RED = False

                val = await client.read_gatt_char(GREEN_LED_UUID)
                if (val == on_value):
                    print ('GREEN ON')
                    GREEN = True
                else:
                    print ('GREEN OFF')
                    GREEN = False

                val = await client.read_gatt_char(BLUE_LED_UUID)
                if (val == on_value):
                    print ('BLUE ON')
                    BLUE = True
                else:
                    print ('BLUE OFF')
                    BLUE = False                    


                while True:
                    await setColor(client)

    if not found:
        print('Could not find Arduino Nano 33 BLE Sense Peripheral')

                    
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(run())
except KeyboardInterrupt:
    print('\nReceived Keyboard Interrupt')
finally:
    print('Program finished')
        
