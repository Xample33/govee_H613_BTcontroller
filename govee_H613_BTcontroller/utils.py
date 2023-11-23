import math

from .constants import Constants


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
    r, g, b = rgb

    hex_r = hex(r)[2:].zfill(2)
    hex_g = hex(g)[2:].zfill(2)
    hex_b = hex(b)[2:].zfill(2)

    checksum = hex(r ^ g ^ b ^ 0x31)[2:].zfill(2)

    return f'330502{hex_r}{hex_g}{hex_b}00FFAE54000000000000000000{checksum}'.upper()

def split_string(string):
    # Split the string into groups of two characters
    pairs = [string[i:i + 2] for i in range(0, len(string), 2)]

    # Convert each pair to a byte and create a bytes object
    result_bytes = bytes([int(pair, 16) for pair in pairs])

    return result_bytes

def to_bytes(raw_string):
    # Convert a raw string of hex characters to bytes
    return bytes.fromhex(raw_string)

def is_valid_color(color_name):
    for name, _ in Constants.COLORS:
        if color_name.lower() == name.lower():
            return True
    return False

def make_string(rgb):
    r, g, b = rgb

    hex_r = hex(r)[2:].zfill(2)
    hex_g = hex(g)[2:].zfill(2)
    hex_b = hex(b)[2:].zfill(2)
    
    string_rgb = f'330502{hex_r}{hex_g}{hex_b}00FFAE54000000000000000000'
    
    checksum = calculate_xor(string_rgb)
    
    string = string_rgb + checksum
    
    return string.upper()

def calculate_xor(string):
    # Split the string into groups of two characters
    pairs = [string[i:i + 2] for i in range(0, len(string), 2)]

    # Convert each pair to an integer and calculate the XOR
    xor_result = int(pairs[0], 16)
    for pair in pairs[1:]:
        xor_result ^= int(pair, 16)

    return hex(xor_result)[2:].zfill(2)