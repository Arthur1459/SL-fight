# --- General --- #
nb_frames = 0
inputs = {"RIGHT":False, "LEFT":False, "UP":False, "DOWN":False, "SPACE":False, "CLICK":False, "ESPCAPE":False, "O":False, "I":False, "U":False, "F":False, "H":False, "Z": False, "Q": False, "S": False, "D": False, "G": False, "L": False}
ButtonsClicked = {"Start": False, "Settings": False, "Rules": False, "Menu": False}
cursor = [0, 0]

time = 0

solid_num = 0
solids = {}  # all hitbox
event_num = 0
events = {}
events_del_keys = []

players = {}

