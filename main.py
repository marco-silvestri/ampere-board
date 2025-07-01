import board
import busio
from kmk.extensions.display import Display, TextEntry, ImageEntry
from kmk.extensions.display.ssd1306 import SSD1306
from jiggler import MouseJitter
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.extensions.media_keys import MediaKeys
from kmk.scanners.keypad import KeysScanner
from kmk.modules.layers import Layers
from kmk.modules.capsword import CapsWord
from kmk.extensions.RGB import RGB
from kmk.extensions.rgb import AnimationModes
from kmk.modules.split import Split, SplitType, SplitSide
from kmk.scanners.keypad import MatrixScanner
from kmk.scanners.encoder import RotaryioEncoder
from kmk.modules.holdtap import HoldTap
from storage import getmount

side = SplitSide.RIGHT if str(getmount("/").label)[-1] == "R" else SplitSide.LEFT

split = Split(
    split_side=side,
    split_target_left=True,
    split_type=SplitType.UART,
    uart_interval=30,
    data_pin=board.GP0,
    data_pin2=board.GP1,
    uart_flip=True,
    use_pio=True,
)

rgb = RGB(
    pixel_pin=board.GP10,
    num_pixels=3,
    animation_mode=AnimationModes.KNIGHT,
    hue_default=170,
    sat_default=255,
    val_default=0,
)

jitter = MouseJitter()
caps_word = CapsWord()
layers = Layers()
holdtap = HoldTap()

class AmpereBoard(KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.col_pins = (
            board.GP16,
            board.GP17,
            board.GP18,
            board.GP19,
            board.GP20,
            board.GP21,
            board.GP22,
        )
        self.row_pins = (
            board.GP15,
            board.GP14,
            board.GP13,
            board.GP12,
            board.GP11,
        )
        self.diode_orientation = DiodeOrientation.COL2ROW
        self.encoder_a = board.GP27
        self.encoder_b = board.GP26
        self.SCL = board.GP7
        self.SDA = board.GP6

        self.matrix = [
            MatrixScanner(
                column_pins=self.col_pins,
                row_pins=self.row_pins,
                columns_to_anodes=self.diode_orientation,
                interval=0.02,
                max_events=64,
            ),
            RotaryioEncoder(
                pin_a=self.encoder_a,
                pin_b=self.encoder_b,
                divisor=2,
            ),
            KeysScanner(
                pins=[board.GP28, board.GP29],
                value_when_pressed=False,
                pull=True,
                interval=0.02,
                max_events=64,
            ),
        ]

        # fmt: off
        self.coord_mapping = [
        0,  1,  2,  3,  4,  5, 6,  45, 44, 43, 42, 41, 40, 39,
        7,  8,  9, 10, 11, 12, 13, 52, 51, 50, 49, 48, 47, 46,
        14, 15, 16, 17, 18, 19, 20, 59, 58, 57, 56, 55, 54, 53,
        21, 22, 23, 24, 25, 26, 27, 66, 65, 64, 63, 62, 61, 60,
        28, 29, 30, 31, 32, 33, 34, 73, 72, 71, 70, 69, 68, 67,
            35, 36, 37, 38,         74, 75, 76, 77,
        ]
        # fmt: on


keyboard = AmpereBoard()

keyboard.extensions.append(MediaKeys())
keyboard.extensions.append(rgb)
keyboard.modules.append(split)
keyboard.modules.append(layers)
keyboard.modules.append(jitter)
keyboard.modules.append(caps_word)
keyboard.modules.append(holdtap)

i2c_bus = busio.I2C(keyboard.SCL, keyboard.SDA)
driver = SSD1306(
    i2c=i2c_bus,
    device_address=0x3C,
)

display = Display(
    display=driver,
    entries=[
        TextEntry(text="Ampere Board", x=0, y=0, y_anchor="A"),
        TextEntry(text="Layer: ", x=0, y=42, y_anchor="B"),
        TextEntry(text="BASE", x=40, y=42, y_anchor="B", layer=0),
        TextEntry(text="FN", x=40, y=42, y_anchor="B", layer=1),
        TextEntry(text="0 1", x=0, y=14),
        TextEntry(text="0", x=0, y=14, inverted=True, layer=0),
        TextEntry(text="1", x=12, y=14, inverted=True, layer=1),
    ],
    width=128,
    height=64,
    dim_time=10,
    dim_target=0.2,
    off_time=300,
    brightness=1,
    flip_left=True,
    flip_right=True,
)

keyboard.extensions.append(display)

keyboard.keymap = [
    [
        KC.GRAVE,
        KC.N1,
        KC.N2,
        KC.N3,
        KC.N4,
        KC.N5,
        KC.HT(KC.CW, KC.MO(1)),
        KC.PS_TOG,
        KC.N6,
        KC.N7,
        KC.N8,
        KC.N9,
        KC.N0,
        KC.MINUS,
        #row2
        KC.TAB,
        KC.Q,
        KC.W,
        KC.F,
        KC.P,
        KC.B,
        KC.PGDOWN,
        KC.BSLASH,
        KC.J,
        KC.L,
        KC.U,
        KC.Y,
        KC.SCOLON,
        KC.EQUAL,
        #row3
        KC.ESCAPE,
        KC.A,
        KC.R,
        KC.S,
        KC.T,
        KC.G,
        KC.PGUP,
        KC.PGDOWN,
        KC.M,
        KC.N,
        KC.E,
        KC.I,
        KC.O,
        KC.QUOTE,
        #row4
        KC.LSHIFT,
        KC.Z,
        KC.X,
        KC.C,
        KC.D,
        KC.V,
        KC.LBRC,
        KC.RBRC,
        KC.K,
        KC.H,
        KC.COMMA,
        KC.DOT,
        KC.SLSH,
        KC.RSHIFT,
        #row5
        KC.LGUI,
        KC.KP_PLUS,
        KC.KP_MINUS,
        KC.HT(KC.KP_ASTERISK, KC.LALT),
        KC.HT(KC.BSLASH, KC.LCTRL),
        KC.BSPACE,
        KC.DELETE,
        KC.ENTER,
        KC.SPACE,
        KC.RALT,
        KC.LEFT,
        KC.DOWN,
        KC.UP,
        KC.RIGHT,
        # Encoder 1 mappings
        KC.MEDIA_NEXT_TRACK,  # Encoder 1 clockwise
        KC.MEDIA_PREV_TRACK,  # Encoder 1 counterclockwise
        KC.MEDIA_PLAY_PAUSE,  # Encoder 1 press
        #Key Scanner
        KC.A,
        # Encoder 1 mappings
        KC.AUDIO_VOL_UP,  # Encoder 2 clockwise
        KC.AUDIO_VOL_DOWN,  # Encoder 2 counterclockwise
        KC.AUDIO_MUTE,  # Encoder 2 press
        #Key Scanner
        KC.D,
    ],
    [
        KC.TG_JITTER,
        KC.F1,
        KC.F2,
        KC.F3,
        KC.F4,
        KC.F5,
        KC.MO(0),
        KC.RGB_TOG,
        KC.F6,
        KC.F7,
        KC.F8,
        KC.F9,
        KC.F10,
        KC.MINUS,
        KC.TAB,
        KC.RGB_MODE_PLAIN,
        KC.RGB_MODE_BREATHE,
        KC.RGB_MODE_RAINBOW,
        KC.RGB_MODE_BREATHE_RAINBOW,
        KC.RGB_MODE_KNIGHT,
        KC.RGB_MODE_SWIRL,
        KC.RBRC,
        KC.J,
        KC.L,
        KC.U,
        KC.Y,
        KC.SCOLON,
        KC.EQUAL,
        KC.ESCAPE,
        KC.RGB_HUI,
        KC.RGB_HUD,
        KC.RGB_SAI,
        KC.RGB_SAD,
        KC.G,
        KC.PGUP,
        KC.PGDOWN,
        KC.M,
        KC.N,
        KC.E,
        KC.I,
        KC.O,
        KC.QUOTE,
        KC.LSHIFT,
        KC.RGB_VAI,
        KC.RGB_VAD,
        KC.RGB_ANI,
        KC.RGB_AND,
        KC.V,
        KC.PGDOWN,
        KC.BSLASH,
        KC.K,
        KC.H,
        KC.COMMA,
        KC.DOT,
        KC.SLSH,
        KC.RSHIFT,
        KC.LGUI,
        KC.KP_PLUS,
        KC.KP_MINUS,
        KC.HT(KC.KP_ASTERISK, KC.LALT),
        KC.HT(KC.BSLASH, KC.LCTRL),
        KC.BSPACE,
        KC.DELETE,
        KC.ENTER,
        KC.SPACE,
        KC.RALT,
        KC.LEFT,
        KC.DOWN,
        KC.UP,
        KC.RIGHT,
        # Encoder mappings for layer 2
        KC.RGB_HUI,  # Encoder 1 clockwise - Hue increase
        KC.RGB_HUD,  # Encoder 1 counterclockwise - Hue decrease
        KC.RGB_TOG,  # Encoder 1 press - RGB toggle
        KC.RGB_VAI,  # Encoder 2 clockwise - Brightness increase
        KC.RGB_VAD,  # Encoder 2 counterclockwise - Brightness decrease
        KC.RGB_MODE_PLAIN,  # Encoder 2 press - Change to plain mode
    ],
]

if __name__ == "__main__":
    keyboard.go()
