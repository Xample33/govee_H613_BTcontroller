import asyncio
import logging

from bleak import BleakClient
from bleak.exc import BleakDeviceNotFoundError

from .constants import Constants
from .utils import calculate_string, convert_color, is_valid_color, split_string, to_bytes


class GoveeController:
    def __init__(self, mac_address):
        if not isinstance(mac_address, str):
            raise TypeError("mac_address argument must be a string")

        self.mac_address = mac_address
        self.client = None
        self.name = None

    async def connect(self) -> "GoveeController":
        if not self.client:
            self.client = BleakClient(self.mac_address)
            try:
                await self.client.connect()
            except BleakDeviceNotFoundError:
                raise BleakDeviceNotFoundError(f'Could not connect to {self.mac_address}')

            raw_name = await self.client.read_gatt_char(Constants.GET_NAME_UUID)
            self.name = raw_name.decode("utf-8")

            return self

    async def disconnect(self):
        if self.client:
            await self.client.disconnect()
            self.client = None

    async def get_power(self):
        byte_array = bytearray(to_bytes(Constants.POWER_STATUS))
        await _get_status(self.device, byte_array)

    async def get_rgb(self):
        byte_array = bytearray(to_bytes(Constants.RGB_STATUS))
        await _get_status(self.device, byte_array)

    async def get_brightness(self):
        byte_array = bytearray(to_bytes(Constants.BRIGHTNESS_STATUS))
        await _get_status(self.device, byte_array)

    async def turn_on(self, smooth=False):
        if not isinstance(smooth, bool):
            raise TypeError("smooth argument must be a boolean")

        if smooth:
            for i in range(0, 255, 25):
                await self.set_brightness(i)
                await asyncio.sleep(0.15)

        command_bytes = to_bytes(Constants.TURN_ON_COMMAND)
        await _send_command(self.client, command_bytes)

    async def turn_off(self, smooth=False):
        if not isinstance(smooth, bool):
            raise TypeError("smooth argument must be a boolean")

        if smooth:
            for i in range(255, 0, -25):
                await self.set_brightness(i)
                await asyncio.sleep(0.15)

        command_bytes = to_bytes(Constants.TURN_OFF_COMMAND)
        await _send_command(self.client, command_bytes)

    async def set_brightness(self, brightness):
        if not isinstance(brightness, int):
            raise TypeError("Brightness must be an integer")

        if (brightness < Constants.BRIGHTNESS_MIN) or (brightness > Constants.BRIGHTNESS_MAX):
            raise ValueError("Brightness must be between 0 and 255")

        # Calculate the brightness hex value
        brightness_hex = hex(brightness)[2:].zfill(2)

        # Calculate checksum
        checksum = hex(brightness ^ 0x33 ^ 0x04)[2:].zfill(2)

        string = f'3304{brightness_hex}00000000000000000000000000000000{checksum}'.upper()

        # Send the command
        await _send_command(self.client, to_bytes(string))

    async def set_color(self, color):
        if isinstance(color, str):
            # Convert color name to RGB
            if is_valid_color(color_name=color) is False:
                raise ValueError(f"Invalid color name, valid values are: {Constants.COLORS_NAMES}")
            rgb = convert_color(color_name=color)
        elif isinstance(color, tuple):
            # Color is already in RGB format
            rgb = color
        else:
            raise ValueError("Invalid color format, color argument must be tuple or str.")

        # Calculate the command string
        command_string = calculate_string(rgb)

        # Split the command string into bytes
        command_bytes = split_string(command_string)

        # Send the command
        await _send_command(self.client, command_bytes)

async def _send_command(device, value):
    logging.debug(f'Sending: {value.hex()}')
    await device.write_gatt_char(Constants.WRITE_CHARACTERISTIC_UUID, bytearray(value), True)

def _notification_handler(raw, data: bytearray) -> None:
    logging.debug(f"Raw: {raw}")
    logging.debug(f"Received: {data.hex()}")

    if data.hex()[0:4] == 'aa01':
        power = int(data.hex()[4:6], 16)
        logging.debug(f'Power: {power}')

    elif data.hex()[0:4] == 'aa05':
        r = int(data.hex()[6:8], 16)
        g = int(data.hex()[8:10], 16)
        b = int(data.hex()[10:12], 16)

        rgb = (r, g, b)
        logging.debug(f'RGB: {rgb} ({convert_color(rgb)})')

    elif data.hex()[0:4] == 'aa04':
        brightness = int(data.hex()[4:6], 16)
        logging.debug(f'Brightness: {brightness}')

async def _get_status(device, byte_array):
    # Subscribe to notifications
    logging.debug(f'Subscribing to {Constants.READ_CHARACTERISTIC_UUID}')
    await device.start_notify(Constants.READ_CHARACTERISTIC_UUID, _notification_handler)

    # Read the state
    await device.write_gatt_char(Constants.WRITE_CHARACTERISTIC_UUID, byte_array)
    await asyncio.sleep(Constants.COMMAND_DELAY)

    # Unsubscribe from notifications
    await device.stop_notify(Constants.READ_CHARACTERISTIC_UUID)
