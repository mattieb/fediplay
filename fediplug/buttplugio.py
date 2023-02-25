'''Buttplug controller'''

import asyncio
import logging
import sys

from buttplug import Client, WebsocketConnector, ProtocolSpec

from fediplug.cli import options
import fediplug.env as env

async def connect_plug_client():
    '''create Client object and connect plug client to Intiface Central or similar'''
    # And now we're in the main function. First, we'll need to set up a client
    # object. This is our conduit to the server.
    # We create a Client object, passing it the name we want for the client.
    # Names are shown in things like Intiface Central. We also can specify the
    # protocol version we want to use, which will default to the latest version.
    plug_client = Client("fediplug", ProtocolSpec.v3)

    # Now we have a client called "Test Client", but it's not connected to
    # anything yet. We can fix that by creating a connector. Connectors
    # allow clients to talk to servers through different methods, including:
    # - Websockets
    # - IPC (Not currently available in Python)
    # - WebRTC (Not currently available in Python)
    # - TCP/UDP (Not currently available in Python)
    # For now, all we've implemented in python is a Websocket connector, so
    # we'll use that. This connector will connect to Intiface Central/Engine
    # on the local machine, using the 12345 port for insecure websockets.
    # We also pass the client logger so that it is used as the parent.
    connector = WebsocketConnector("ws://127.0.0.1:12345", logger=plug_client.logger)

    # Finally, we connect.
    # If this succeeds, we'll be connected. If not, we'll probably have some
    # sort of exception thrown of type ButtplugError.
    try:
        await plug_client.connect(connector)
    except Exception as e:
        logging.error(f"Could not connect to server, exiting: {e}")
        return
    print('plug client connected')
    return plug_client

async def scan_devices(plug_client):
    # Now we move on to looking for devices. We will tell the server to start
    # scanning for devices. It returns while it is scanning, so we will wait
    # for 10 seconds, and then we will tell the server to stop scanning.
    await plug_client.start_scanning()
    await asyncio.sleep(5)
    await plug_client.stop_scanning()

    # We can use the found devices as we see fit. The list of devices is
    # automatically kept up to date by the client:

    # First, we are going to list the found devices.
    plug_client.logger.info(f"Devices: {plug_client.devices}")

       # If we have any device we can print the list of devices 
       # and access it by its ID: ( this step is done is trigger_actuators() )
    if len(plug_client.devices) != 0:
        print(plug_client.devices)
        print(len(plug_client.devices), "devices found")
    return plug_client


async def trigger_actuators(plug_client, play_command):
    # If we have any device we can access it by its ID:
    device = plug_client.devices[0]
    # The most common case among devices is that they have some actuators
    # which accept a scalar value (0.0-1.0) as their command.
    play_command = (1, 1)
    if len(device.actuators) != 0:
        print(len(device.actuators), "actuators found")
        # cycle through all actuators in device
        print(device.actuators)
        for actuator in device.actuators:
            await actuator.command(play_command[0])
            print("generic actuator")
        await asyncio.sleep(play_command[1])
        #stops all actuators
        for actuator in device.actuators:
            await actuator.command(0)
'''
    # Some devices may have linear actuators which need a different command.
    # The first parameter is the time duration in ms and the second the
    # position for the linear axis (0.0-1.0).
    if len(device.linear_actuators) != 0:
        await device.linear_actuators[0].command(1000, 0.5)
        print("linear actuator")

    # Other devices may have rotatory actuators which another command.
    # The first parameter is the speed (0.0-1.0) and the second parameter
    # is a boolean, true for clockwise, false for anticlockwise.
    if len(device.rotatory_actuators) != 0:
        await device.rotatory_actuators[0].command(0.5, True)
        print("rotary actuator") 
'''

async def disconnect_plug_client(plug_client):
    # Disconnect the plug_client.
    await plug_client.disconnect()


# First things first. We set logging to the console and at INFO level.
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
