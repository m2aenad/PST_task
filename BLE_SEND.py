import asyncio
import logging
import sys
import time
from bleak import BleakClient

# This code is supposed to work with PST_task trial.py
# The input is a string of length 1 (either T or F)
# Takes the input and makes it a byte 
# Sends the byte to the arduino sketch 'T' or 'F'
# T = start motor
# F = stop motor

# these are the bluetooth unique ids
UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E" #transmitted data
UART_RX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E" #received data

# this function requires an address (see the main block below)
logger = logging.getLogger(__name__)

async def run_ble_client(address, debug=False):
    
    logger.info("starting scan...")

#     def handle_rx(_: int, data: bytearray): # I think we need to change this
#         byte_val = data
#         int_val = int.from_bytes(byte_val, "big") 
#         print("MI ETO PEREVELUI:"+str(int_val))
#         print("received:", data)
#         sys.exit(0)
    async def callback_handler(_, data):
        await queue.put((time.time(), data))

    async with BleakClient(address) as client: # this function is receiving the data
        logger.info("connected")
#         paired = await client.pair()
        await client.start_notify(UART_RX_CHAR_UUID.lower(), callback_handler)
        await asyncio.sleep(10.0) # this is 10 right now may need to change
        await client.stop_notify(args.characteristic)
        # Send an "exit command to the consumer"
        await queue.put((time.time(), None))
        logger.info("disconnected")
        
#         await client.start_notify(UART_RX_CHAR_UUID.lower(), handle_rx) # this is the characteristic (first) and the bytearray containing the data

#         text = 'T'
#         await client.write_gatt_char(UART_TX_CHAR_UUID.lower(), bytes(text, encoding = 'ascii')) # sending data back to the arduino 
#         await asyncio.sleep(1.0)
async def run_queue_consumer(queue: asyncio.Queue):
    logger.info("Starting queue consumer")

    while True:
        # Use await asyncio.wait_for(queue.get(), timeout=1.0) if you want a timeout for getting data.
        epoch, data = await queue.get()
        if data is None:
            logger.info(
                "Got message from client about disconnection. Exiting consumer loop..."
            )
            break
        else:
            logger.info("Received callback data via async queue at %s: %r", epoch, data)


        
        
if __name__ == "__main__":
    address = "C4:B9:DA:5F:83:50"
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(run(address, True))
    
