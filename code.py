import time
from adafruit_macropad import MacroPad

# https://learn.adafruit.com/adafruit-macropad-rp2040/troubleshooting
# https://github.com/dxinteractive/macropad-midilooper
# https://docs.circuitpython.org/projects/macropad/en/latest/api.html

# https://www.rebeltech.org/patch-library/patch/mosfez_midilooper
# https://www.openwarelab.org/Faust/
# https://github.com/RebelTechnology/OpenWare/blob/master/Source/OpenWareMidiControl.h#L149-L180

macropad = MacroPad(rotation=90)
# macropad.display.auto_refresh = False
# macropad.pixels.auto_write = False

macropad.pixels.brightness = 0.5
macropad.pixels.fill((0, 255, 0))

while True:
    macropad.midi.send(macropad.ControlChange(75, 127))
    print("-")
    time.sleep(0.25)
    macropad.midi.send(macropad.ControlChange(75, 0))
    print(" ")
    key_event = macropad.keys.events.get()
    # if key_event and key_event.pressed:
    #  print("Key pressed: {}".format(key_event.key_number))
    # print("Encoder: {}".format(macropad.encoder))
    # print("Encoder switch: {}".format(macropad.encoder_switch))
    time.sleep(1.0)
