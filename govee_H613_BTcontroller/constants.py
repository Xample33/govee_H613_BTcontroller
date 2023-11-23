class Constants:
    # Bluetooth timeout
    BT_TIMEOUT = 15

    # Delay between commands
    COMMAND_DELAY = 0.3
    
    # BRIGHNESS VALUES
    BRIGHTNESS_MIN = 0
    BRIGHTNESS_MAX = 255
    
    # Device Service UUID
    GET_NAME_UUID = '00002a00-0000-1000-8000-00805f9b34fb'

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
        ("white", (255, 255, 255)),
        ("warm_white", (255, 166, 87)),
        ("cool_white", (255, 254, 250)),

        ("black", (0, 0, 0)),

        ("red", (255, 0, 0)),
        ("dark_red", (139, 0, 0)),
        ("light_red", (255, 69, 69)),

        ("green", (0, 255, 0)),
        ("dark_green", (0, 100, 0)),
        ("light_green", (144, 238, 144)),

        ("blue", (0, 0, 255)),
        ("dark_blue", (0, 0, 139)),
        ("light_blue", (173, 216, 230)),

        ("yellow", (255, 255, 0)),
        ("dark_yellow", (184, 134, 11)),
        ("light_yellow", (255, 255, 153)),

        ("orange", (255, 165, 0)),
        ("dark_orange", (255, 140, 0)),
        ("light_orange", (255, 179, 71)),

        ("purple", (128, 0, 128)),
        ("dark_purple", (75, 0, 130)),
        ("light_purple", (218, 112, 214)),

        ("pink", (255, 182, 193)),
        ("dark_pink", (255, 20, 147)),
        ("light_pink", (255, 182, 193)),

        ("brown", (165, 42, 42)),
        ("dark_brown", (139, 69, 19)),
        ("light_brown", (205, 133, 63)),
    ]

    COLORS_NAMES = [color[0] for color in COLORS]
