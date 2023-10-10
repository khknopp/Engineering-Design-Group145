import asyncio
from bleak import BleakScanner, BleakClient

async def run():
    devices = await BleakScanner.discover()

    rp2040_address = None
    for device in devices:
        if device.name == "RP2040":
            rp2040_address = device.address
            print(rp2040_address)
            break

    if not rp2040_address:
        print("RP2040 device not found!")
        return

    client = BleakClient(rp2040_address, timeout=30)
    print("Connecting to device...")
    connected = await client.connect()

    print("Connected:", connected)

    services = client.services

    for service in services:
        if service.uuid == "0000180d-0000-1000-8000-00805f9b34fb":  # Match the service UUID we set in the Arduino code
            print("Service found!")
            for char in service.characteristics:
                if char.uuid == "00002a37-0000-1000-8000-00805f9b34fb":  # Match the characteristic UUID
                    print("Characteristic found!")
                    while True:
                        value = await client.read_gatt_char(char.uuid)
                        print("Random Value:", int.from_bytes(value, byteorder='little'))
                        await asyncio.sleep(1)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
