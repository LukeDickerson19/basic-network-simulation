# Basic Network Simulation

## Description:

This code is a simulation of portable devices (like smartphones and tablets) that move in an out of a 2D rectangular environment. Each device has a max signal range it can send and receive signals directly. The simulation has a GUI display as seen below.

<img src="https://github.com/PopeyedLocket/basic-network-simulation/blob/master/images_and_videos/video1-devices_moving.gif">

You can pause the movement of the devices, click on a device, and see its signal range highlighted around it, the ping messages it sends on regular intervals in red and the echo messages it receives back in green.

<img src="https://github.com/PopeyedLocket/basic-network-simulation/blob/master/images_and_videos/video2-pings_and_echos.gif">

Each device uses the time between sending a ping to receiving an echo and known signal speed to estimate how far away neighboring devices are (as seen in terminal output on the left).

Devices can also send each other messages with arbitrary data, that is neither a ping or an echo, as seen in blue. These arbitrary messages can propegate through the network to devices the sender is not directly connected to, and are the primary means of communication.

<img src="https://github.com/PopeyedLocket/basic-network-simulation/blob/master/images_and_videos/video3-custome_message-moving_devices.gif">

Currently the nodes just relay any message they recieve to all their direct neighbors creating what is called a [broadcast storm](https://en.wikipedia.org/wiki/Broadcast_storm), so some protocal of how messages are coordinated would need to be made to keep that from happening. The end goal being to create an app that enables users to communicate via a mesh network. To make this app, developers are provided with the Node class which can be imported and made the parent class of the various types of nodes in their network. The Node class allows its child classes to send messages, and automatically ping and echo each other. See node.py for all the functions it provides.



### Setup
```
git clone git@github.com:PopeyedLocket/basic-network-simulation.git # download repository
cd basic-network-simulation # enter repository folder
python3 -m venv ./virt_env # create a virtual environment
source ./virt_env/bin/activate # activate virtual environment
pip install -r ./src/requirements.txt # install all the required libraries
```

### Usage
```
cd basic-network-simulation # enter repository folder
source ./virt_env/bin/activate # activate virtual environment
python ./src/main.py # run simulation
```

