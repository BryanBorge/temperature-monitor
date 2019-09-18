# RaspberryPi Temperature and RH Monitor

Main goal of this script is to monitor temp/RH remotely. 

This is done by sending temp/RH values to [Dweet.io](http://dweet.io). You can read dweets from the last 24 hours by going to this [page](https://dweet.io/get/dweets/for/TempMonitor). 

The dweet values are then read by [Freeboard.io](http://freeboard.io) and displayed in real time on a guage/histogram. There is also a 16x2 LCD display wired up to the RaspberryPi which displays current temp/RH along with the min/max values. 
