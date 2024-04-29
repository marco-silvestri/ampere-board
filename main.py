print("ciao")

import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.extensions.peg_oled_Display import Oled,OledDisplayMode,OledReactionType,OledData
from kmk.modules.encoder import EncoderHandler
from kmk.modules.layers import Layers
from kmk.extensions.RGB import RGB
from kmk.extensions.rgb import AnimationModes
from kmk.modules.split import Split, SplitType, SplitSide
from storage import getmount

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

keyboard.modules.append(layers)
keyboard.modules.append(encoder_handler)
keyboard.modules.append(split)

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
      KC.DOT,
      KC.DOT,
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
      KC.KP_ASTERISK,
      KC.LCTRL,
      KC.BSPACE,
      KC.DELETE,
      KC.ENTER,
      KC.SPACE,
      KC.LEFT,
      KC.DOWN,
      KC.UP,
      KC.RIGHT
    ]
]

Zoom_in = KC.LCTRL(KC.EQUAL)
Zoom_out = KC.LCTRL(KC.MINUS)

encoder_handler.map = [((KC.A, KC.B, KC.C),),]

oled_ext = Oled(OledData(image={0:OledReactionType.LAYER,1:[imgToDisplay]}),toDisplay=OledDisplayMode.IMG,flip=True)

keyboard.debug_enabled = True
rgb = RGB(pixel_pin=board.GP10, num_pixels=5, animation_mode=AnimationModes.KNIGHT,)
keyboard.extensions.append(rgb)
keyboard.extensions.append(oled_ext)
if __name__ == "__main__":
    keyboard.go()
