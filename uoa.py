from win32con import WM_USER
import win32gui

# this is a part of Razor's window title
WINDOW_TITLE = "- Razor v"

_skills = {
    0: "Alchemy",
    1: "Anatomy",
    2: "Animal Lore",
    3: "Item Identification",
    4: "Arms Lore",
    5: "Parrying",
    6: "Begging",
    7: "Blacksmithy",
    8: "Bowcraft and Fletching",
    9: "Peacemaking",
    10: "Camping",
    11: "Carpentry",
    12: "Cartography",
    13: "Cooking",
    14: "Detecting Hidden",
    15: "Discordance",
    16: "Evaluating Intelligence",
    17: "Healing",
    18: "Fishing",
    19: "Forensics",
    20: "Herding",
    21: "Hiding",
    22: "Provocation",
    23: "Inscription",
    24: "Lock Picking",
    25: "Magery",
    26: "Resisting Spells",
    27: "Tactics",
    28: "Snooping",
    29: "Musicianship",
    30: "Poisoning",
    31: "Archery",
    32: "Spirit Speak",
    33: "Stealing",
    34: "Tailoring",
    35: "Animal Taming",
    36: "Taste Identification",
    37: "Tinkering",
    38: "Tracking",
    39: "Veterinary",
    40: "Swordsmanship",
    41: "Mace Fighting",
    42: "Fencing",
    43: "Wrestling",
    44: "Lumberjacking",
    45: "Mining",
    46: "Meditation",
    47: "Stealth",
    48: "Disarming",
    49: "Necromancy",
    50: "Focus",
    51: "Chivalry",
    52: "Bushido",
    53: "Ninjitsu",
    54: "Spellweaving",
    55: ""
}

_skills_by_name = {}
for k in _skills.keys():
    _skills_by_name[_skills[k]] = k

class UOA:
    def __init__(self):
        self.razor = None
        win32gui.EnumWindows(self.get_razor_window, None)

    def get_coords(self):
        r = win32gui.SendMessage(self.razor, WM_USER+202)
        ns = r >> 16
        ew = r - (ns << 16)
        return { "ns": ns, "ew": ew }

    def get_razor_window(self, hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if WINDOW_TITLE in title:
                self.razor = hwnd
    
    def get_skill_by_id(self, skill:int) -> dict:
        r_disp = int(win32gui.SendMessage(self.razor, WM_USER+203, skill, 0))
        r_base = int(win32gui.SendMessage(self.razor, WM_USER+203, skill, 1))
        r_lock = int(win32gui.SendMessage(self.razor, WM_USER+203, skill, 2))
        #r_name = win32gui.SendMessage(self.razor, WM_USER+203, skill, 3)
        if r_lock == 0:
            r_lock_str = "U"
        elif r_lock == 1:
            r_lock_str = "D"
        elif r_lock == 2:
            r_lock_str = "L"
        else:
            r_lock_str = "?"
        return {
            "display": r_disp / 10,
            "base": r_base / 10,
            "lock": r_lock_str,
        #    "name_id": r_name,
            "name": _skills[skill]
        }
        
    def get_skill_id_from_name(self, name:str) -> int:
        try:
            return _skills_by_name[name.title()]
        except:
            return None

    def get_skill(self, name:str) -> dict:
        _id = self.get_skill_id_from_name(name)
        return self.get_skill_by_id(_id)
        
    def get_stat(self, STAT:str):
        """Get current value for STAT.  Can be one of STR, INT, DEX, WEIGHT, or MAXHP."""
        stat = STAT.lower()
        if stat == "str":
            _stat = 0
        elif stat == "int":
            _stat = 1
        elif stat == "dex":
            _stat = 2
        elif stat == "weight":
            _stat = 3
        elif stat == "maxhp":
            _stat = 4
        else:
            raise(RuntimeError(f"Invalid STAT ({STAT})"))
        r = int(win32gui.SendMessage(self.razor, WM_USER+204, _stat))
        hi = r >> 16
        lo = r - (hi << 16)
        return lo

    def is_poisoned(self) -> bool:
        r = int(win32gui.SendMessage(self.razor, WM_USER+214))
        return r == 1

    def request_data(self) -> bool:
        r = win32gui.SendMessage(self.razor, WM_USER+200)
        return r == 1
    
if __name__ == "__main__":
    # tests
    uoa = UOA()
    coords = uoa.get_coords()
    print(f"Coords: {coords['ew']}, {coords['ns']}")
    skills = ["anatomy", "tactics", "animal Lore", "carpentry", "mace FIGHTING"]
    for skill in skills:
        s = uoa.get_skill(skill)
        print(f"{s['name']} skill (disp, base): {s['display']}, {s['base']}")
    stats = ["str", "int", "dex", "weight", "maxhp"]
    for stat in stats:
        print(f"Stat {stat}: {uoa.get_stat(stat)}")
    print(f"Is poisoned: {uoa.is_poisoned()}")
