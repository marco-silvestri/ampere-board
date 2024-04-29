print("ciao")

import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.extensions.peg_oled_Display import Oled,OledDisplayMode,OledReactionType,OledData
from kmk.modules.encoder import EncoderHandler
from kmk.modules.layers import Layers
from kmk.modules.layers import Layers as _Layers
from kmk.extensions.RGB import RGB
from kmk.extensions.rgb import AnimationModes
from kmk.modules.split import Split, SplitType, SplitSide
from storage import getmount

sat = 255
val = 100; # brightness in range 0-255
side = SplitSide.RIGHT if str(getmount('/').label)[-1] == 'R' else SplitSide.LEFT

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

keyboard = KMKKeyboard()
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

keyboard.extensions.append(rgb)

keyboard.modules.append(encoder_handler)
keyboard.modules.append(split)

keyboard.modules.append(layers)

encoder_handler.pins = ((board.GP27, board.GP26, board.GP28),)

keyboard.SCL=board.GP7
keyboard.SDA=board.GP6
keyboard.col_pins = (
    board.GP16,
    board.GP17,
    board.GP18,
    board.GP19,
    board.GP20,
    board.GP21,
    board.GP22,
)
keyboard.row_pins = (
    board.GP15,
    board.GP14,
    board.GP13,
    board.GP12,
    board.GP11,
)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

keyboard.keymap = [[
      KC.GRAVE,
      KC.N1,
      KC.N2,
      KC.N3,
      KC.N4,
      KC.N5,
      KC.MO(1),
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
      KC.LBRC,
      KC.RBRC,
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
      KC.HT(KC.BSLASH,KC.LCTRL),
      KC.BSPACE,
      KC.DELETE,
      KC.ENTER,
      KC.SPACE,
      KC.RALT,
      KC.LEFT,
      KC.DOWN,
      KC.UP,
      KC.RIGHT
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
      KC.HT(KC.BSLASH,KC.LCTRL),
      KC.BSPACE,
      KC.DELETE,
      KC.ENTER,
      KC.SPACE,
      KC.RALT,
      KC.LEFT,
      KC.DOWN,
      KC.UP,
      KC.RIGHT
    ]
]

Zoom_in = KC.LCTRL(KC.EQUAL)
Zoom_out = KC.LCTRL(KC.MINUS)

encoder_handler.map = [((Zoom_in, Zoom_out, KC.C),),]

#oled_ext = Oled(OledData(image={0:OledReactionType.LAYER,1:[imgToDisplay]}),toDisplay=OledDisplayMode.IMG,flip=True)
oled = Oled(
    OledData(
        corner_one={0:OledReactionType.STATIC,1:["layer"]},
        corner_two={0:OledReactionType.LAYER,1:["1","2","3","4"]},
        corner_three={0:OledReactionType.LAYER,1:["base","raise","lower","adjust"]},
        corner_four={0:OledReactionType.LAYER,1:["colemak_dh","f keys","shifted","leds"]}
        ),
        toDisplay=OledDisplayMode.TXT,flip=True,oHeight=64)
keyboard.debug_enabled = False

keyboard.extensions.append(oled)

if __name__ == "__main__":
    keyboard.go()
