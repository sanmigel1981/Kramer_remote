# commands.py
# Kramer VP-437N Controller - Command Dictionary

def build_command_bytes(control_type, function, param=None):
    """
    Build raw bytes command for Kramer protocol.
    Format: Y<space>CT<space>FUNC<space>[PARAM]<CR>
    Returns: bytearray like b'Y 3 0 1\r'
    """
    if param is not None:
        cmd_str = f"Y {control_type} {function} {param}\r"
    else:
        cmd_str = f"Y {control_type} {function}\r"
    return cmd_str.encode('ascii')

# Pre-built commands as bytearrays for performance
COMMANDS = {
    # === INPUT SOURCES ===
    'Input: CV': build_command_bytes(3, 0, 1),
    'Input: YC': build_command_bytes(3, 0, 2),
    'Input: COMP1': build_command_bytes(3, 0, 3),
    'Input: COMP2': build_command_bytes(3, 0, 4),
    'Input: VGA': build_command_bytes(3, 0, 5),
    'Input: HDMI1': build_command_bytes(3, 0, 6),
    'Input: HDMI2': build_command_bytes(3, 0, 7),
    
    # === OUTPUT RESOLUTIONS ===
    'Resolution: Native': build_command_bytes(3, 21, 0),
    'Resolution: VGA': build_command_bytes(3, 21, 1),
    'Resolution: SVGA': build_command_bytes(3, 21, 2),
    'Resolution: XGA': build_command_bytes(3, 21, 3),
    'Resolution: SXGA': build_command_bytes(3, 21, 4),
    'Resolution: UXGA': build_command_bytes(3, 21, 5),
    'Resolution: 480i': build_command_bytes(3, 21, 6),
    'Resolution: 480p': build_command_bytes(3, 21, 7),
    'Resolution: 720p60': build_command_bytes(3, 21, 8),
    'Resolution: 1080i60': build_command_bytes(3, 21, 9),
    'Resolution: 1080p60': build_command_bytes(3, 21, 10),
    'Resolution: 576i': build_command_bytes(3, 21, 11),
    'Resolution: 576p': build_command_bytes(3, 21, 12),
    'Resolution: 720p50': build_command_bytes(3, 21, 13),
    'Resolution: 1080i50': build_command_bytes(3, 21, 14),
    'Resolution: 1080p50': build_command_bytes(3, 21, 15),
    'Resolution: WXGA': build_command_bytes(3, 21, 16),
    'Resolution: WSXGA': build_command_bytes(3, 21, 17),
    'Resolution: WUXGA': build_command_bytes(3, 21, 18),
    'Resolution: 1280x800': build_command_bytes(3, 21, 19),
    'Resolution: 1440x900': build_command_bytes(3, 21, 20),
    'Resolution: 1400x1050': build_command_bytes(3, 21, 21),
    'Resolution: 1600x900': build_command_bytes(3, 21, 22),
    'Resolution: 480i59': build_command_bytes(3, 21, 23),
    'Resolution: 480p59': build_command_bytes(3, 21, 24),
    'Resolution: 720p59': build_command_bytes(3, 21, 25),
    'Resolution: 1080i59': build_command_bytes(3, 21, 26),
    'Resolution: 1080p59': build_command_bytes(3, 21, 27),
    
    # === SIZE MODES ===
    'Size: Full': build_command_bytes(3, 1, 0),
    'Size: Panscan': build_command_bytes(3, 1, 1),
    'Size: Overscan': build_command_bytes(3, 1, 2),
    'Size: Underscan': build_command_bytes(3, 1, 3),
    'Size: Letterbox': build_command_bytes(3, 1, 4),
    'Size: Underscan2': build_command_bytes(3, 1, 5),
    'Size: Best Fit': build_command_bytes(3, 1, 6),
    
    # === POWER ===
    'Power: ON': build_command_bytes(6, 0, 1),
    'Power: OFF': build_command_bytes(6, 0, 0),
    'Power: REBOOT': build_command_bytes(6, 0, 2),
    
    # === REMOTE BUTTONS ===
    'Remote: INFO': build_command_bytes(0, 14),
    'Remote: FREEZE': build_command_bytes(0, 2),
    'Remote: BLANK': build_command_bytes(0, 30),
    'Remote: MUTE': build_command_bytes(0, 31),
    'Remote: MENU': build_command_bytes(0, 20),
    'Remote: EXIT': build_command_bytes(0, 22),
    
    # === TOGGLE FUNCTIONS ===
    'Freeze: ON': build_command_bytes(6, 1, 1),
    'Freeze: OFF': build_command_bytes(6, 1, 0),
    'Blank: ON': build_command_bytes(6, 2, 1),
    'Blank: OFF': build_command_bytes(6, 2, 0),
    'Mute: ON': build_command_bytes(6, 3, 1),
    'Mute: OFF': build_command_bytes(6, 3, 0),
    
    # === ADVANCED ===
    'Drop Lines: ON': build_command_bytes(1, 95, 1),
    'Drop Lines: OFF': build_command_bytes(1, 95, 0),
    'HDCP Input: ON': build_command_bytes(1, 160, 1),
    'HDCP Input: OFF': build_command_bytes(1, 160, 0),
    'Auto Sync: ON': build_command_bytes(1, 84, 1),
    'Auto Sync: OFF': build_command_bytes(1, 84, 0),
    
    # === FACTORY RESET ===
    'Factory Reset': build_command_bytes(3, 23, 1),
    
    # === GET COMMANDS ===
    'Get: Info': build_command_bytes(0, 14),
    'Get: Input': build_command_bytes(4, 0),
    'Get: Resolution': build_command_bytes(4, 21),
    'Get: Input Resolution': build_command_bytes(4, 24),
    'Get: Size': build_command_bytes(4, 1),
}

# For debugging: convert bytes to hex string
def cmd_to_hex(cmd_bytes):
    return ' '.join(f'{b:02X}' for b in cmd_bytes)