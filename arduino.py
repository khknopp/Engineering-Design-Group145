import asyncio
from bleak import BleakScanner, BleakClient

async def run():
    devices = await BleakScanner.discover()
    rp2040_device = None

    for device in devices:
        if device.name == "RP2040":
            rp2040_device = device
            break

    if not rp2040_device:
        print("RP2040 device not found!")
        return

    async with BleakClient(rp2040_device) as client:
        services = await client.get_services()
        for service in services:
            if service.uuid == "0000180d-0000-1000-8000-00805f9b34fb":  # Match the service UUID we set in the Arduino code
                for char in service.characteristics:
                    if char.uuid == "00002a37-0000-1000-8000-00805f9b34fb":  # Match the characteristic UUID
                        while True:
                            value = await client.read_gatt_char(char)
                            print("Random Value:", int.from_bytes(value, byteorder='little'))
                            await asyncio.sleep(1)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
