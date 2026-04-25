# decoder.py
# Kramer VP-437N Controller - Response Decoder

from config import (
    INPUT_SOURCES, OUTPUT_RESOLUTIONS, SIZE_MODES, REMOTE_BUTTONS,
    AUDIO_DELAY, HDCP_INPUT, HDCP_OUTPUT, INPUT_RESOLUTIONS
)

def decode_response(response_str):
    """Decode HEX response to human-readable text"""
    if not response_str or not response_str.startswith('Z'):
        return response_str.strip()
    
    try:
        parts = response_str.strip().split()
        if len(parts) < 3:
            return response_str
        
        ct = int(parts[1])  # Control Type
        fn = int(parts[2])  # Function
        param = int(parts[3]) if len(parts) > 3 else None
        
        return _decode(ct, fn, param)
    except (ValueError, IndexError):
        return response_str

def _decode(ct, fn, param):
    """Internal decoder"""
    # Remote buttons (Type 0)
    if ct == 0:
        return f"Button: {REMOTE_BUTTONS.get(fn, f'Unknown({fn})')}"
    
    # Picture settings (Type 1/2)
    if ct in (1, 2):
        mode = "Set" if ct == 1 else "Get"
        settings = {
            4: ("Color Red", param), 5: ("Color Green", param), 6: ("Color Blue", param),
            16: ("Brightness", param), 17: ("Contrast", param), 25: ("Hue", param),
            26: ("Sharpness", param), 29: ("Saturation", param),
            33: ("Output Volume", param), 34: ("Input Volume", param),
            41: ("OSD H-Pos", param), 42: ("OSD V-Pos", param),
            43: ("OSD Timeout", f"{param}s"),
            50: ("Noise Reduction", AUDIO_DELAY.get(param, f"Unknown({param})")),
            51: ("Audio Delay", AUDIO_DELAY.get(param, f"Unknown({param})")),
            95: ("Drop Lines", "ON" if param else "OFF"),
            160: ("HDCP Input", HDCP_INPUT.get(param, f"Unknown({param})")),
            161: ("HDCP Output", HDCP_OUTPUT.get(param, f"Unknown({param})")),
        }
        name, val = settings.get(fn, (f"Func {fn}", param))
        return f"{mode}: {name} = {val}"
    
    # Parameters (Type 3/4)
    if ct in (3, 4):
        mode = "Set" if ct == 3 else "Get"
        if fn == 0:  # Input Source
            return f"{mode}: Input = {INPUT_SOURCES.get(param, (f'Unknown({param})',))[0]}"
        elif fn == 1:  # Size
            return f"{mode}: Size = {SIZE_MODES.get(param, f'Unknown({param}')}"
        elif fn == 21:  # Resolution
            return f"{mode}: Resolution = {OUTPUT_RESOLUTIONS.get(param, (f'Unknown({param})',))[0]}"
        elif fn == 23:
            return "Factory Reset Executed"
        elif fn == 24:
            return f"Input Resolution = {INPUT_RESOLUTIONS.get(param, f'Unknown({param}')}"
        return f"{mode}: Func {fn} = {param}"
    
    # Power/Functions (Type 6/7)
    if ct in (6, 7):
        mode = "Set" if ct == 6 else "Get"
        funcs = {
            0: ("Power", "OFF" if param == 0 else ("ON" if param == 1 else "REBOOT")),
            1: ("Freeze", "ON" if param else "OFF"),
            2: ("Blank", "ON" if param else "OFF"),
            3: ("Mute", "ON" if param else "OFF"),
            4: ("Key Lock", "ON" if param else "OFF"),
        }
        name, val = funcs.get(fn, (f"Func {fn}", param))
        return f"{mode}: {name} = {val}"
    
    return f"Response: Z {ct} {fn} {param}"