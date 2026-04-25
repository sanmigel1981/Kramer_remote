# config.py
# Kramer VP-437N Controller - Configuration Settings

DEFAULT_BAUDRATE = 9600
DEFAULT_TIMEOUT = 3

# Colors (for reference, not used in mobile version)
COLOR_SENT = '#006600'
COLOR_RECEIVED = '#0066CC'
COLOR_SYSTEM = '#666666'
COLOR_ERROR = '#CC0000'

# Input Sources (Control Type 3, Function 0)
INPUT_SOURCES = {
    1: ('CV', 'Composite Video'),
    2: ('YC', 'S-Video'),
    3: ('COMP1', 'Component 1'),
    4: ('COMP2', 'Component 2'),
    5: ('VGA', 'VGA/PC'),
    6: ('HDMI1', 'HDMI 1'),
    7: ('HDMI2', 'HDMI 2'),
}

# Output Resolutions (Control Type 3, Function 21)
OUTPUT_RESOLUTIONS = {
    0: ('Native', 'Native (from EDID)'),
    1: ('VGA', 'VGA (640x480)'),
    2: ('SVGA', 'SVGA (800x600)'),
    3: ('XGA', 'XGA (1024x768)'),
    4: ('SXGA', 'SXGA (1280x1024)'),
    5: ('UXGA', 'UXGA (1600x1200)'),
    6: ('480i', '480i'),
    7: ('480p', '480p'),
    8: ('720p60', '720p@60Hz'),
    9: ('1080i60', '1080i@60Hz'),
    10: ('1080p60', '1080p@60Hz'),
    11: ('576i', '576i'),
    12: ('576p', '576p'),
    13: ('720p50', '720p@50Hz'),
    14: ('1080i50', '1080i@50Hz'),
    15: ('1080p50', '1080p@50Hz'),
    16: ('WXGA', 'WXGA (1366x768)'),
    17: ('WSXGA', 'WSXGA (1680x1050)'),
    18: ('WUXGA', 'WUXGA (1920x1200)'),
    19: ('1280x800', '1280x800'),
    20: ('1440x900', 'WXGA+ (1440x900)'),
    21: ('1400x1050', 'SXGA+ (1400x1050)'),
    22: ('1600x900', '1600x900'),
    23: ('480i59', '480i@59.94Hz'),
    24: ('480p59', '480p@59.94Hz'),
    25: ('720p59', '720p@59.94Hz'),
    26: ('1080i59', '1080i@59.94Hz'),
    27: ('1080p59', '1080p@59.94Hz'),
}

# Size Modes (Control Type 3, Function 1)
SIZE_MODES = {
    0: 'Full',
    1: 'Panscan',
    2: 'Overscan',
    3: 'Underscan',
    4: 'Letterbox',
    5: 'Underscan2',
    6: 'Best Fit',
}

# Remote Control Buttons (Control Type 0)
REMOTE_BUTTONS = {
    0: 'SIZE', 1: 'POWER', 2: 'FREEZE', 3: '480p', 4: '576p',
    5: '720p', 6: '1080i', 7: '1080p', 8: 'VGA', 9: 'SVGA',
    10: 'XGA', 11: 'SXGA', 12: 'WXGA', 13: 'UXGA', 14: 'INFO',
    15: 'UP', 16: 'NATIVE', 17: 'LEFT', 18: 'OK', 19: 'RIGHT',
    20: 'MENU', 21: 'DOWN', 22: 'EXIT', 23: 'AV', 24: 'YC',
    25: 'COMP1', 26: 'HDMI1', 27: 'HDMI2', 28: 'COMP2', 29: 'VGA',
    30: 'BLANK', 31: 'MUTE', 33: 'AUTO_ADJUST',
}

# Audio Delay (Control Type 1, Function 51)
AUDIO_DELAY = {0: 'Off', 1: '40ms', 2: '110ms', 3: '150ms'}

# HDCP Options
HDCP_INPUT = {0: 'OFF', 1: 'ON'}
HDCP_OUTPUT = {0: 'Follow Input', 1: 'Follow Output'}

# Input Resolutions (Control Type 4, Function 24)
INPUT_RESOLUTIONS = {
    0: 'Unknown', 1: 'VGA (640x480)', 2: 'SVGA (800x600)', 3: 'XGA (1024x768)',
    4: 'SXGA (1280x1024)', 5: 'UXGA (1600x1200)', 6: '480i', 7: '480p',
    8: '720p60', 9: '1080i60', 10: '1080p60', 11: '576i', 12: '576p',
    13: '720p50', 14: '1080i50', 15: '1080p50', 16: 'WXGA (1366x768)',
    17: 'WSXGA (1680x1050)', 18: 'WUXGA (1920x1200)', 19: '1280x800',
    20: '1440x900', 21: '1400x1050', 22: '1600x900',
    23: '2048x1080@50Hz (2K)', 24: '2048x1080@60Hz (2K)',
}