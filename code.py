import time
import math
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_macropad import MacroPad

#
# links
#

# https://learn.adafruit.com/adafruit-macropad-rp2040/troubleshooting
# https://github.com/dxinteractive/macropad-midilooper
# https://docs.circuitpython.org/projects/macropad/en/latest/api.html

# https://www.rebeltech.org/patch-library/patch/mosfez_midilooper
# https://www.openwarelab.org/Faust/
# https://github.com/RebelTechnology/OpenWare/blob/master/Source/OpenWareMidiControl.h#L149-L180

#
# consts
#

INPUT_UPDATE_FREQ = 0.01;

# 0,1,2,3
# 4,5,6,7
# 8,9,10,11
PIXEL_SUBDIVIDE = 4
PIXEL_SUBDIVIDE_AMOUNT = 4
PIXEL_SUBDIVIDE_COLOR = (150, 0, 0)
PIXEL_LOOPMODE = 8
PIXEL_LOOPMODE_COLOR = (0, 150, 0)
PIXEL_FILTER = 9
PIXEL_FILTER_COLOR = (255, 60, 0)
PIXEL_MUTE = 10
PIXEL_MUTE_COLOR = (0, 0, 255)
PIXEL_REC = 11
PIXEL_REC_COLOR = (255, 0, 0)

#
# initial config
#

macropad = MacroPad(rotation=90)
macropad.display.auto_refresh = False
macropad.pixels.auto_write = False
macropad.pixels.brightness = 0.3
macropad.pixels.fill((0, 0, 0))
macropad.pixels[PIXEL_SUBDIVIDE + PIXEL_SUBDIVIDE_AMOUNT - 1] = PIXEL_SUBDIVIDE_COLOR
macropad.pixels[PIXEL_LOOPMODE] = PIXEL_LOOPMODE_COLOR
macropad.pixels[PIXEL_FILTER] = PIXEL_FILTER_COLOR
macropad.pixels[PIXEL_MUTE] = PIXEL_MUTE_COLOR
macropad.pixels[PIXEL_REC] = PIXEL_REC_COLOR
macropad.pixels.show()

#
# state
#

# input
last_encoder = 0
last_encoder_switch = False

# time
time_start = time.monotonic()
time_elapsed = time_start
last_input_update_time = 0
last_beat_time = 0
current_beat = 0

# ui state
bpm = 110
bpb = 4
edit_bpm = True

#
# render
#

main_group = displayio.Group()
bpm_number_label = label.Label(font=terminalio.FONT, text="", scale=2)
bpm_number_label.anchor_point = (0, 0)
bpm_number_label.anchored_position = (0, 0)

bpm_label = label.Label(font=terminalio.FONT, text="bpm", scale=1)
bpm_label.anchor_point = (0, 0)
bpm_label.anchored_position = (0, 21)

bpb_number_label = label.Label(font=terminalio.FONT, text="", scale=2)
bpb_number_label.anchor_point = (0, 0)
bpb_number_label.anchored_position = (0, 41)

bpb_label = label.Label(font=terminalio.FONT, text="bpb", scale=1)
bpb_label.anchor_point = (0, 0)
bpb_label.anchored_position = (0, 62)

beats_label = label.Label(font=terminalio.FONT, text="", scale=1)
beats_label.anchor_point = (0, 0)
beats_label.anchored_position = (0, 118)

def render():
    bpm_number_label.text = "{}".format(bpm)
    bpb_number_label.text = "{}".format(bpb)

    if edit_bpm:
        bpm_number_label.text += "_"
    else:
        bpb_number_label.text += "_"

    beats_label.text = "/";
    for x in range(0, current_beat):
        beats_label.text += "/";

    macropad.display.refresh()

main_group.append(bpm_number_label)
main_group.append(bpm_label)
main_group.append(bpb_number_label)
main_group.append(bpb_label)
main_group.append(beats_label)
macropad.display.root_group = main_group
render()

#
# input
#

def input():
    global last_encoder
    global last_encoder_switch
    global bpm
    global bpb
    global edit_bpm

    if macropad.encoder != last_encoder:
        encoder_delta = macropad.encoder - last_encoder
        if edit_bpm:
            bpm += encoder_delta * 2
            bpm = max(min(bpm, 200), 0)
        else:
            bpb += encoder_delta
            bpb = max(min(bpb, 8), 1)
        last_encoder = macropad.encoder
        render()

    if macropad.encoder_switch != last_encoder_switch:
        last_encoder_switch = macropad.encoder_switch
        if macropad.encoder_switch:
            edit_bpm = not edit_bpm
            render()

    key_event = macropad.keys.events.get()
    if key_event and key_event.pressed:
        print("Key pressed: {}".format(key_event.key_number))


#
# loop
#

while True:
    time_elapsed = time.monotonic() - time_start

    beat_duration = 60 / bpm
    if time_elapsed > last_beat_time + beat_duration:
        # macropad.midi.send(macropad.ControlChange(75, 0))
        current_beat = (current_beat + 1) % bpb
        render()
        last_beat_time = time_elapsed

    if time_elapsed > (last_input_update_time + INPUT_UPDATE_FREQ):
        input()
        last_input_update_time = time_elapsed

    time.sleep(0.001)

