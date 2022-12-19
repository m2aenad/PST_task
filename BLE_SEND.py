import asyncio
import logging
import sys

from bleak import BleakClient


# these are the bluetooth unique ids
UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E" #transmitted data
UART_RX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E" #received data

# this function requires an address (see the main block below)
async def run(address, debug=False):
    log = logging.getLogger(__name__)


    def handle_rx(_: int, data: bytearray): # I think we need to change this
        byte_val = data
        int_val = int.from_bytes(byte_val, "big") 
        print("MI ETO PEREVELUI:"+str(int_val))
        print("received:", data)
        sys.exit(0)


    async with BleakClient(address) as client:
        paired = await client.pair()
        await client.start_notify(UART_RX_CHAR_UUID.lower(), handle_rx) # this is the characteristic (first) and the bytearray containing the data

        text = 'T'
        await client.write_gatt_char(UART_TX_CHAR_UUID.lower(), bytes(text, encoding = 'ascii')) # sending data back to the arduino 
        await asyncio.sleep(1.0)

        
        
if __name__ == "__main__":
    address = "C4:B9:DA:5F:83:50"
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(run(address, True))
    
