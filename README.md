# Basic Network Simulation

## Description:

This code is a simulation of portable devices (like smartphones and tablets) that move in an out of a 2D rectangular environment. Each device has a max signal range it can send and receive signals direclty. The simulation has a GUI display (using Pygame GUI library) as seen below.

![results](https://github.com/PopeyedLocket/sma-tsl-switch/blob/master/images/asset-BTC_x-1_w-100.png?raw=true "Results")

<img src="https://github.com/PopeyedLocket/basic-network-simulation/blob/master/images_and_videos/video1-devices_moving.gif" width="600" height="400">

You can pause the movement of the devices, click on a device, and see its signal range highlighted around it, the ping messages it sends on regular intervals in red and the echo messages it receives back in green (the devices' movement is paused, but not the signals the devices send each other).

<put a gif here>
![results](https://github.com/PopeyedLocket/sma-tsl-switch/blob/master/images/asset-BTC_x-1_w-100.png?raw=true "Results")

Each device uses the time delay of sending a ping and receiving an echo in a simple linear equation of the signal moving there and back with known signal speed to estimate how far away neighboring devices are.

Devices can also send each other messages with arbitrary data, that is neither a ping or an echo, as seen in blue. These arbitrary messages are the main way devices will interact with each other to accomplish their goal in the collective of all the devices.

<put a gif here>
![results](https://github.com/PopeyedLocket/sma-tsl-switch/blob/master/images/asset-BTC_x-1_w-100.png?raw=true "Results")

The reason this simulation was created is to provide the playground to create an application that a device (be it simulated, or real) can install and run. This app will give a device the ability to communicate with other devices that also have the app and give all the devices the collective ability to store and process data on a single shared distributed data base with different permissions for each user, aka distributed cloud computing aka smart contracts.

To make this app, developers are provided with the Node class which can be imported and made the parent class of the various types of nodes in their network. The Node class allows its child classes to send messages, and automatically ping and echo each other. See Node.py for ALL the functions it provides, and see Child_Node_1.py and Child_Node_2.py for examples of how to use Node.py as a parent class.



## Usage:

python main.py



## Requirements:

pandas
numpy
hashlib
pygame



