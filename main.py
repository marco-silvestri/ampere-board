import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.peg_oled_Display import (
    Oled,
    OledDisplayMode,
    OledReactionType,
    OledData,
)
from kmk.scanners.keypad import KeysScanner
from kmk.modules.encoder import EncoderHandler
from kmk.modules.layers import Layers
from kmk.modules.capsword import CapsWord
from kmk.extensions.RGB import RGB
from kmk.extensions.rgb import AnimationModes
from kmk.modules.split import Split, SplitType, SplitSide
from kmk.scanners.keypad import MatrixScanner
from kmk.scanners.encoder import RotaryioEncoder
from storage import getmount

caps_word = CapsWord()
sat = 255
val = 100
# brightness in range 0-255
side = SplitSide.RIGHT if str(getmount("/").label)[-1] == "R" else SplitSide.LEFT

if side == SplitSide.RIGHT:
    imgToDisplay = "hearts.bmp"
else:
    imgToDisplay = "stars.bmp"
split = Split(
    split_side=side,
    split_target_left=True,
    split_type=SplitType.UART,  # Defaults to UART
    uart_interval=20,  # Sets the uarts delay. Lower numbers draw more power
    data_pin=board.GP0,  # The primary data pin to talk to the secondary device with
    data_pin2=board.GP1,  # Second uart pin to allow 2 way communication
    uart_flip=True,  # Reverses the RX and TX pins if both are provided
    use_pio=True,  # Use RP2040 PIO implementation of UART. Required if you want to use other pins than RX/TX
)

layers = Layers()
encoder_handler = EncoderHandler()
rgb = RGB(
    pixel_pin=board.GP10,
    num_pixels=5,
    animation_mode=AnimationModes.BREATHING_RAINBOW,
    hue_default=170,
    sat_default=sat,
    val_default=val,
)


class CustomKMKKeyboard(KMKKeyboard):
    def __init__(
        self,
    ):
        # create and register the scanner(s)
        self.matrix = [
            MatrixScanner(
                # required arguments:
                column_pins=self.col_pins,
                row_pins=self.row_pins,
                # optional arguments with defaults:
                columns_to_anodes=self.diode_orientation,
                interval=0.02,  # Debounce time in floating point seconds
                max_events=64,
            ),
            RotaryioEncoder(
                pin_a=self.encoder_a,
                pin_b=self.encoder_b,
                divisor=2,
            ),
            KeysScanner(
                # require argument:
                pins=[board.GP28],
                # optional arguments with defaults:
                value_when_pressed=False,
                pull=True,
                interval=0.02,  # Debounce time in floating point seconds
                max_events=64,
            ),
        ]

    col_pins = (
        board.GP16,
        board.GP17,
        board.GP18,
        board.GP19,
        board.GP20,
        board.GP21,
        board.GP22,
    )
    row_pins = (
        board.GP15,
        board.GP14,
        board.GP13,
        board.GP12,
        board.GP11,
    )
    diode_orientation = DiodeOrientation.COL2ROW
    encoder_a = board.GP27
    encoder_b = board.GP26
    SCL = board.GP7
    SDA = board.GP6

    # fmt: off
    coord_mapping = [
     0,  1,  2,  3,  4,  5, 6,  44 ,43, 42, 41, 40, 39, 38,
     7,  8,  9, 10, 11, 12, 13, 51, 50, 49, 48, 47, 46, 45,
    14, 15, 16, 17, 18, 19, 20, 58, 57, 56, 55, 54, 53, 52,
    21, 22, 23, 24, 25, 26, 27, 65, 64, 63, 62, 61, 60, 59,
    28, 29, 30, 31, 32, 33, 34, 72, 71, 70, 69, 68, 67, 66,
            35, 36, 37,                 73, 74, 75
    ]

# fmt: off
keyboard = CustomKMKKeyboard()

keyboard.extensions.append(MediaKeys())
keyboard.extensions.append(rgb)
keyboard.modules.append(split)
keyboard.modules.append(layers)

# keyboard.modules.append(encoder_handler)
# encoder_handler.pins = ((board.GP27, board.GP26, board.GP28),)
# encoder_handler.map = [((KC.AUDIO_VOL_UP, KC.AUDIO_VOL_DOWN,KC.MPLY),(KC.AUDIO_VOL_UP, KC.AUDIO_VOL_DOWN,KC.MPLY)),]

oled = Oled(
    OledData(
        corner_one={0: OledReactionType.STATIC, 1: ["layer"]},
        corner_two={0: OledReactionType.LAYER, 1: ["1", "2", "3", "4"]},
        corner_three={
            0: OledReactionType.LAYER,
            1: ["base", "raise", "lower", "adjust"],
        },
        corner_four={
            0: OledReactionType.LAYER,
            1: ["colemak_dh", "f keys", "shifted", "leds"],
        },
    ),
    toDisplay=OledDisplayMode.TXT,
    flip=True,
    oHeight=64,
)

keyboard.modules.append(caps_word)
keyboard.extensions.append(oled)

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
        KC.AUDIO_VOL_UP,  # Left side clockwise
        KC.AUDIO_VOL_DOWN,  # Left side counterclockwise
        KC.AUDIO_MUTE,
        KC.MEDIA_NEXT_TRACK,  # Right side clockwise
        KC.MEDIA_PREV_TRACK,  # Right side counterclockwise
        KC.MEDIA_PLAY_PAUSE,
    ],
    [
        KC.GRAVE,
        KC.F1,
        KC.F2,
        KC.F3,
        KC.F4,
        KC.F5,
        KC.MO(0),
        KC.RGB_TOG(),
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
        KC.AUDIO_VOL_UP,  # Left side clockwise
        KC.AUDIO_VOL_DOWN,  # Left side counterclockwise
        KC.MEDIA_PLAY_PAUSE,
        KC.MEDIA_NEXT_TRACK,  # Right side clockwise
        KC.MEDIA_PREV_TRACK,  # Right side counterclockwise
        KC.AUDIO_MUTE,
    ],
]

keyboard.debug_enabled = True

if __name__ == "__main__":
    keyboard.go()
