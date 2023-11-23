import asyncio
import logging

from bleak import BleakClient
from bleak.exc import BleakDeviceNotFoundError, BleakError

from .constants import Constants
from .utils import convert_color, is_valid_color, to_bytes, make_string


_LOGGER = logging.getLogger(__name__)

class GoveeController:
    def __init__(self, mac_address):
        if not isinstance(mac_address, str):
            raise TypeError("mac_address argument must be a string")

        self.mac_address = mac_address
        self.client = None
        self.name = None
        
        self.rgb = None
        self.color_name = None
        self.brightness = None        
        self.power = None

    async def connect(self) -> "GoveeController":
        if not self.client:
            self.client = BleakClient(self.mac_address)
            try:
                await self.client.connect()
            except BleakDeviceNotFoundError:
                raise BleakDeviceNotFoundError(f'Could not connect to {self.mac_address}')

            raw_name = await self.client.read_gatt_char(Constants.GET_NAME_UUID)
            self.name = raw_name.decode("utf-8")
            
            _LOGGER.debug(f'Connected to {self.name} ({self.mac_address})')
            return self
        
    async def disconnect(self):
        if self.client:
            await self.client.disconnect()
            self.client = None

    async def get_power(self):
        byte_array = bytearray(to_bytes(Constants.POWER_STATUS))
        await self._get_status(byte_array)
        return self.power

    async def get_rgb(self):
        byte_array = bytearray(to_bytes(Constants.RGB_STATUS))
        await self._get_status(byte_array)
        return self.rgb

    async def get_brightness(self):
        byte_array = bytearray(to_bytes(Constants.BRIGHTNESS_STATUS))
        await self._get_status(byte_array)
        return self.brightness

    async def turn_on(self, smooth=False):
        _LOGGER.debug('Turning on')
        if not isinstance(smooth, bool):
            raise TypeError("smooth argument must be a boolean")

        if smooth:
            for i in range(0, 255, 50):
                await self.set_brightness(i)
                await asyncio.sleep(0.15)

        command_bytes = to_bytes(Constants.TURN_ON_COMMAND)
        
        await self._send_command(command_bytes)

    async def turn_off(self, smooth=False):
        _LOGGER.debug('Turning off')
        if not isinstance(smooth, bool):
            raise TypeError("smooth argument must be a boolean")

        if smooth:
            for i in range(255, 0, -50):
                await self.set_brightness(i)
                await asyncio.sleep(0.15)

        command_bytes = to_bytes(Constants.TURN_OFF_COMMAND)
        
        await self._send_command(command_bytes)

    async def set_brightness(self, brightness):
        _LOGGER.debug('Setting brightness')
        if not isinstance(brightness, int):
            raise TypeError("Brightness must be an integer")

        if (brightness < Constants.BRIGHTNESS_MIN) or (brightness > Constants.BRIGHTNESS_MAX):
            raise ValueError("Brightness must be between 0 and 255")

        # Calculate the brightness hex value
        brightness_hex = hex(brightness)[2:].zfill(2)

        # Calculate checksum
        checksum = hex(brightness ^ 0x33 ^ 0x04)[2:].zfill(2)

        string = f'3304{brightness_hex}00000000000000000000000000000000{checksum}'

        # Send the command
        await self._send_command(to_bytes(string))

    async def set_color(self, color):
        _LOGGER.debug('Setting color')
        
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

        # Split the command string into bytes
        command_bytes = make_string(rgb)
        
        # Send the command
        await self._send_command(to_bytes(command_bytes))

    async def _send_command(self, value):
        _LOGGER.debug(f'Sending: {bytearray(value).hex()}')
        try:
            await self.client.write_gatt_char(Constants.WRITE_CHARACTERISTIC_UUID, bytearray(value))
            await asyncio.sleep(Constants.COMMAND_DELAY)
        except BleakError as e:
            raise e
        
    async def _notification_handler(self, raw, data: bytearray) -> None:
        _LOGGER.debug(f"Received: {data.hex()}")
        
        if data.hex()[0:4] == 'aa01':
            self.power = int(data.hex()[4:6], 16)
            
            _LOGGER.debug(f'Power: {self.power}')

        elif data.hex()[0:4] == 'aa05':
            r = int(data.hex()[6:8], 16)
            g = int(data.hex()[8:10], 16)
            b = int(data.hex()[10:12], 16)

            self.rgb = (r, g, b)
            self.color_name = convert_color(rgb_tuple=self.rgb)
            
            _LOGGER.debug(f'RGB: {self.rgb} ({self.color_name})')

        elif data.hex()[0:4] == 'aa04':
            self.brightness = int(data.hex()[4:6], 16)
            
            _LOGGER.debug(f'Brightness: {self.brightness}')
            
        else:
            _LOGGER.debug(f'Unknown command: {data.hex()}')

    async def _get_status(self, byte_array):
        # Subscribe to notifications
        _LOGGER.debug(f'Subscribing to {Constants.READ_CHARACTERISTIC_UUID}')
        await self.client.start_notify(Constants.READ_CHARACTERISTIC_UUID, self._notification_handler)
        await asyncio.sleep(Constants.COMMAND_DELAY)
        
        # Read the state
        _LOGGER.debug(f'Sending: {byte_array.hex()}')
        await self.client.write_gatt_char(Constants.WRITE_CHARACTERISTIC_UUID, byte_array)
        await asyncio.sleep(Constants.COMMAND_DELAY)

        # Unsubscribe from notifications
        _LOGGER.debug(f'Unsubscribing from {Constants.READ_CHARACTERISTIC_UUID}')
        try:
            await self.client.stop_notify(Constants.READ_CHARACTERISTIC_UUID)
        except BleakError("Not connected"):
            raise BleakError("Not connected")