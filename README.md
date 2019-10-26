# RaspberryPi Temperature and RH Monitor

Main goal of this script is to monitor temp/RH remotely. 

This is done by sending temp/RH values to [Dweet.io](http://dweet.io) every 30 seconds. You can read dweets from the last 24 hours by going to this [page](https://dweet.io/get/dweets/for/TempMonitor). 

The dweet values are then read by [Freeboard.io](http://freeboard.io) and displayed in real time on a guage/histogram. My Freeboard dashboard can be found [here](https://freeboard.io/board/OM6K4R). (Currently using the 30 day trial so this link may be broken in the future)

There is also a 16x2 LCD display wired up to the RaspberryPi which displays current temp/RH along with the min/max values. 

10/26/19 Update:
This script now sends temp and rh values to a google sheet every 10 minutes. I plan to use this sheet in the near future to create a custom dashboard and live graph. 
