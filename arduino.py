import asyncio
from bleak import BleakScanner, BleakClient

async def connect():
    devices = await BleakScanner.discover()

    rp2040_address = None
    for device in devices:
        if device.name == "RP2040":
            rp2040_address = device.address
            print(rp2040_address)
            break

    if not rp2040_address:
        print("RP2040 device not found!")
        return None, None

    client = BleakClient(rp2040_address, timeout=60)
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
                    # BleakClient.disconnect(client)
                    return char, client
    return 0, 0
    
async def read(char, client):
    value = await client.read_gatt_char(char.uuid)
    unparsed = int.from_bytes(value, byteorder='little')
    f1 = unparsed % 100
    f2 = unparsed // 100 % 100
    f3 = unparsed // 10000 % 100
    f4 = unparsed // 1000000 % 100
    p = unparsed // 100000000
    return f1,f2,f3,f4,p

#async def run(db, Sessions, Measurements):
async def run():
    char, client = await connect()
    value = await client.read_gatt_char(char.uuid)
    unparsed = int.from_bytes(value, byteorder='little')
    f1 = unparsed % 100
    f2 = unparsed // 100 % 100
    f3 = unparsed // 10000 % 100
    f4 = unparsed // 1000000 % 100
    p = unparsed // 100000000
    # session = Session(Average = (f1+f2+f3+f4+p)/5, Average_F1=f1, Average_F2=f2, Average_F3=f3, Average_F4=f4, Average_P=p)
    # db.session.add(session)
    # measurement = Measurement(Session_Id=session.Id, F1=f1, F2=f2, F3=f3, F4=f4, P=p)
    print("Created session!")
    while True:
        value = await client.read_gatt_char(char.uuid)
        print("Value:", int.from_bytes(value, byteorder='little'))
        await asyncio.sleep(0.1)
    # db.session.add(session)

# async def main():
#     await connect

# loop = asyncio.get_event_loop()
# loop.run_until_complete(run())