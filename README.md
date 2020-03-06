# Basic Network Simulation

## Description:

This code is a simulation of portable devices (like smartphones and tablets) that move in an out of a 2D rectangular environment. Each device has a max signal range it can send and receive signals directly. The simulation has a GUI display as seen below.

<img src="https://github.com/PopeyedLocket/basic-network-simulation/blob/master/images_and_videos/video1-devices_moving.gif">

You can pause the movement of the devices, click on a device, and see its signal range highlighted around it, the ping messages it sends on regular intervals in red and the echo messages it receives back in green.

<img src="https://github.com/PopeyedLocket/basic-network-simulation/blob/master/images_and_videos/video2-pings_and_echos.gif">

Each device uses the time between sending a ping to receiving an echo and known signal speed to estimate how far away neighboring devices are (as seen in terminal output on the left).

Devices can also send each other messages with arbitrary data, that is neither a ping or an echo, as seen in blue. These arbitrary messages can propegate through the network to devices the sender is not directly connected to, and are the primary means of communication.

<img src="https://github.com/PopeyedLocket/basic-network-simulation/blob/master/images_and_videos/video3-custome_message-moving_devices.gif">

<img src="https://github.com/PopeyedLocket/basic-network-simulation/blob/master/images_and_videos/video3-custome_message-stationary_devices.gif">

The reason this simulation was created is to provide the playground to create an application that a device (be it simulated, or real) can install and run. The goal of the app is to give a device the ability to communicate with other devices that also have the app and give all the devices the collective ability to store and process data on a single distributed data base, aka distributed cloud computing aka smart contracts.

To make this app, developers are provided with the Node class which can be imported and made the parent class of the various types of nodes in their network. The Node class allows its child classes to send messages, and automatically ping and echo each other. See Node.py for all the functions it provides.



## Usage:

python main.py



## Requirements:

pandas
numpy
hashlib
pygame



