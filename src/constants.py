# 抢早八 · Campus Rush — Game Constants

# ── Window ───────────────────────────────────────────────────
WIDTH = 960
HEIGHT = 540
FPS = 60
TITLE = "赶早八 · Campus Rush"

# ── Layout ───────────────────────────────────────────────────
GROUND_Y = 450
GROUND_H = 90

# ── Physics ──────────────────────────────────────────────────
GRAVITY = 0.58
JUMP_VEL = -14.5
DB_JUMP_VEL = -13.0

# ── Speed ────────────────────────────────────────────────────
BASE_SPEED = 5.5
SPEED_CAP = 16.0
SPEED_RAMP = 400

# ── Player ───────────────────────────────────────────────────
PLAYER_W = 38
PLAYER_H = 62
PLAYER_SLIDE_H = 30
PLAYER_SLIDE_DURATION = 38
PLAYER_X = 110
PLAYER_MAX_JUMPS = 2

# ── Spawn ────────────────────────────────────────────────────
BASE_SPAWN_GAP = 95
MIN_SPAWN_GAP = 52
SPAWN_GAP_DECAY = 350
SCORE_RATE = 0.048

# ── Game States ──────────────────────────────────────────────
START = "start"
PLAYING = "playing"
DEAD = "dead"

# ── High Score ───────────────────────────────────────────────
HIGHSCORE_FILE = "highscore.txt"

# ── Color Palette ────────────────────────────────────────────
OUTLINE = (40, 40, 40)
SKY_TOP = (135, 206, 235)
SKY_BOTTOM = (224, 240, 255)
CLOUD = (255, 255, 255)

BUILDING_PALETTE = [
    (255, 204, 153),  # peach
    (178, 223, 219),  # mint
    (197, 176, 213),  # lavender
    (255, 245, 157),  # butter
    (179, 208, 255),  # sky blue
    (255, 182, 182),  # salmon
]

GROUND_LIGHT = (200, 190, 175)
GROUND_DARK = (170, 160, 145)
ROAD_LINE = (255, 255, 255, 80)

PLAYER_BODY = (220, 60, 60)
PLAYER_SKIN = (255, 220, 180)
PLAYER_JEANS = (50, 80, 160)
PLAYER_BAG = (30, 40, 80)
PLAYER_HAIR = (30, 25, 20)
PLAYER_SHOE = (50, 50, 50)

TRASH_CAN = (100, 130, 150)
TRASH_LID = (70, 90, 110)
SIGN_POLE = (140, 140, 150)
SIGN_BOARD = (80, 160, 120)
CONE_ORANGE = (255, 140, 30)
CONE_WHITE = (240, 240, 240)
TAPE_YELLOW = (255, 210, 0)
CART_RED = (200, 50, 50)
CART_SILVER = (180, 190, 200)
BUMP_YELLOW = (255, 220, 50)
BUMP_BLACK = (40, 40, 40)
BIKE_GREEN = (60, 180, 100)
BIKE_TIRE = (50, 50, 50)
BIKE_RIDER = (240, 180, 60)

HUD_BG = (0, 0, 0, 140)
TEXT_LIGHT = (240, 240, 240)
TEXT_ACCENT = (255, 200, 50)
TEXT_RED = (255, 60, 60)
