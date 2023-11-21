class Constants:
    # Bluetooth timeout
    BT_TIMEOUT = 15
    
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