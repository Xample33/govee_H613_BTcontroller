import asyncio
from bleak import BleakClient
import math

# Govee LED MAC Address
govee_mac_address = 'A4:C1:38:35:97:24'
govee_mac_address2 = '60:74:F4:0D:DC:AD'

class Constants:
    # Delay between commands
    COMMAND_DELAY = 2
    
    # Control Service and Characteristic UUIDs
    WRITE_CHARACTERISTIC_UUID = '00010203-0405-0607-0809-0a0b0c0d2b11'
    READ_CHARACTERISTIC_UUID = '00010203-0405-0607-0809-0a0b0c0d2b10'
    
    # LED Command Strings
    TURN_ON_COMMAND = '3301010000000000000000000000000000000033'
    TURN_OFF_COMMAND = '3301000000000000000000000000000000000032'
    
    POWER_STATUS = 'aa010000000000000000000000000000000000ab'
    RGB_STATUS = 'aa050100000000000000000000000000000000ae'
    BRIGHTNESS_STATUS = 'aa040000000000000000000000000000000000ae'
    
    COLORS = [
    ("black", (0, 0, 0)),
    ("silver", (192, 192, 192)),
    ("gray", (128, 128, 128)),
    ("white", (255, 255, 255)),
    ("maroon", (128, 0, 0)),
    ("red", (255, 0, 0)),
    ("dark_red", (139, 0, 0)),
    ("light_red", (255, 99, 71)),
    ("purple", (128, 0, 128)),
    ("fuchsia", (255, 0, 255)),
    ("dark_fuchsia", (128, 0, 128)),
    ("light_fuchsia", (255, 182, 193)),
    ("green", (0, 128, 0)),
    ("lime", (0, 255, 0)),
    ("dark_green", (0, 100, 0)),
    ("light_green", (144, 238, 144)),
    ("olive", (128, 128, 0)),
    ("yellow", (255, 255, 0)),
    ("dark_yellow", (184, 134, 11)),
    ("light_yellow", (255, 255, 224)),
    ("navy", (0, 0, 128)),
    ("blue", (0, 0, 255)),
    ("dark_blue", (0, 0, 139)),
    ("light_blue", (173, 216, 230)),
    ("teal", (0, 128, 128)),
    ("aqua", (0, 255, 255)),
    ("dark_aqua", (0, 139, 139)),
    ("light_aqua", (224, 255, 255)),
]
    
def convert_color(rgb_tuple = None, color_name = None):
    def distance(a, b):
        dx = a[0] - b[0]
        dy = a[1] - b[1]
        dz = a[2] - b[2]
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    def rgb_to_color_name(rgb):
        mn = float('inf')
        color = None
        for name, color_rgb in Constants.COLORS:
            d = distance(rgb, color_rgb)
            if d < mn:
                mn = d
                color = name
        return color

    def color_name_to_rgb(color_name):
        for name, rgb in Constants.COLORS:
            if name == color_name:
                return rgb
        return None

    if rgb_tuple is None and color_name is None:
        return None
    
    if rgb_tuple is not None:
        return rgb_to_color_name(rgb_tuple)
    
    if color_name is not None:
        return color_name_to_rgb(color_name)
    
def calculate_string(rgb):
    r,g,b = rgb
    
    hex_r = hex(r)[2:].zfill(2)
    hex_g = hex(g)[2:].zfill(2)
    hex_b = hex(b)[2:].zfill(2)
    
    checksum = hex(r ^ g ^ b ^ 0x31)[2:].zfill(2)
    
    return f'330502{hex_r}{hex_g}{hex_b}00FFAE54000000000000000000{checksum}'.upper()

def split_string(string):
    # Split the string into groups of two characters
    pairs = [string[i:i+2] for i in range(0, len(string), 2)]

    # Convert each pair to a byte and create a bytes object
    result_bytes = bytes([int(pair, 16) for pair in pairs])

    return result_bytes

async def set_brightness(ble_device, brightness):
    # Calculate the brightness hex value
    brightness_hex = hex(brightness)[2:].zfill(2)
    
    # Calculate checksum
    checksum = hex(brightness ^ 0x33 ^ 0x04)[2:].zfill(2)
    
    string = f'3304{brightness_hex}00000000000000000000000000000000{checksum}'.upper()
    
    # Send the command
    await send_command(ble_device, to_bytes(string))

async def set_color(ble_device, color):
    if isinstance(color, str):
        # Convert color name to RGB
        rgb = convert_color(color_name=color)
    elif isinstance(color, tuple):
        # Color is already in RGB format
        rgb = color
    else:
        raise ValueError("Invalid color format. Provide either RGB tuple or color name.")

    # Calculate the command string
    command_string = calculate_string(rgb)

    # Split the command string into bytes
    command_bytes = split_string(command_string)

    # Send the command
    await send_command(ble_device, command_bytes)

async def send_command(ble_device, value):
    print(f'Sending: {value.hex()}')
    await ble_device.write_gatt_char(Constants.WRITE_CHARACTERISTIC_UUID, bytearray(value), True)
    
async def turn_on(ble_device):
    command_bytes = to_bytes('3301010000000000000000000000000000000033')
    await send_command(ble_device, command_bytes)

async def turn_off(ble_device):
    command_bytes = to_bytes('3301000000000000000000000000000000000032')
    await send_command(ble_device, command_bytes)

def to_bytes(raw_string):
    # Convert a raw string of hex characters to bytes
    return bytes.fromhex(raw_string)
    
def notification_handler(raw, data: bytearray) -> None:
    print(f"Raw: {raw}")
    print(f"Received: {data.hex()}")
    
    if data.hex()[0:4] == 'aa01':
        power = int(data.hex()[4:6], 16)
        print(f'Power: {power}')
    
    elif data.hex()[0:4] == 'aa05':
        r = int(data.hex()[6:8], 16)
        g = int(data.hex()[8:10], 16)
        b = int(data.hex()[10:12], 16)
        
        rgb = (r, g, b)
        print(f'RGB: {rgb} ({convert_color(rgb)})')
        
    elif data.hex()[0:4] == 'aa04':
        brightness = int(data.hex()[4:6], 16)
        print(f'Brightness: {brightness}')
    
async def get_status(device, byte_array):
    # Subscribe to notifications
    await device.start_notify(Constants.READ_CHARACTERISTIC_UUID, notification_handler)
    
    # Read the state
    await device.write_gatt_char(Constants.WRITE_CHARACTERISTIC_UUID, byte_array)
    await asyncio.sleep(Constants.COMMAND_DELAY)
    
    # Unsubscribe from notifications
    await device.stop_notify(Constants.READ_CHARACTERISTIC_UUID)

async def get_power(device):
    byte_array = bytearray(to_bytes(Constants.POWER_STATUS))
    await get_status(device, byte_array)
    
async def get_rgb(device):
    byte_array = bytearray(to_bytes(Constants.RGB_STATUS))
    await get_status(device, byte_array)
    
async def get_brightness(device):
    byte_array = bytearray(to_bytes(Constants.BRIGHTNESS_STATUS))
    await get_status(device, byte_array)
    
async def main():
    try:
        # Connect to Govee LED
        async with BleakClient(govee_mac_address) as govee_device:
            device_name = await govee_device.read_gatt_char("00002a00-0000-1000-8000-00805f9b34fb")
            print(f'Connected to {govee_device.address} ({device_name.decode("utf-8")})')
            await asyncio.sleep(0.3) 
            
            print("Getting LED power")
            power = await get_power(govee_device)
            
            if power == 0:
                print("Turning on LED")
                await turn_on(govee_device)
            
            print("changing color")
            await set_color(govee_device, 'lime')
            #await send_command(govee_device, to_bytes('33050200FF4000FFAE540000000000000000008E'))
            
            print("Getting LED color")
            await get_rgb(govee_device)
            
            print("Getting LED brightness")
            await get_brightness(govee_device)
            
            
            await govee_device.disconnect()
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Keyboard interrupt')