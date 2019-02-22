# commands for controlling various programs

from aenea import *

gitcommand_array = [
    'add',
    'branch',
    'checkout',
    'clone',
    'commit',
    'diff',
    'fetch',
    'init',
    'log',
    'merge',
    'pull',
    'push',
    'rebase',
    'reset',
    'show',
    'stash',
    'status',
    'tag',
]
gitcommand = {}
for command in gitcommand_array:
    gitcommand[command] = command

class ProgramsRule(MappingRule):
    mapping = {
        #"vim save": Key("escape, colon, w, enter"),
        #"vim quit": Key("escape, colon, q, enter"),
        #"vim really quit": Key("escape, colon, q, exclamation, enter"),
        #"vim save and quit": Key("escape, colon, w, q, enter"),
        #"vim split": Text(":sp "),
        #"vim vertical split": Text(":vs "),
        #"vim tab new": Text(":tabnew "),
        #"vim tab close": Text(":tabclose\n"),
        #
        #"vim open source": Text(":vs %<.c\n"),
        #"vim open source plus": Text(":vs %<.cpp\n"),
        #"vim open header": Text(":vs %<.h\n") + Key('c-w, c-w'),
        #"vim (switch|toggle|swap)": Key('c-w, c-w'),
        #"vim rotate": Key('c-w, r'),
        #"vim try that": Key('escape, colon, w, enter, a-tab/5, up, enter'),
        #
        #'screen': Key('c-a'),
        #'screen switch': Key('c-a, c-a'),
        #'screen scroll': Key('c-a, lbracket'),
        #
        #"just execute": Key("backspace, enter"),
        #"command (git|get)": Text("git "),
        #"command (git|get) <gitcommand>": Text("git %(gitcommand)s "),
        #"command vim": Text("vim "),
        #"command C D": Text("cd "),
        ##"command list": Text("ls "),
        #"command make": Text("make "),
        #"command make clean": Text("make clean "),
        ##"command cat": Text("cat "),
        #"command (grep|grip)": Text("grep "),
        ##"command background": Text("bg "),
        ##"command foreground": Text("fg "),


        # web browser
        'browser location':         Key('a-d'),
        'browser refresh':          Key('f5'),
        'browser really refresh':   Key('s-f5'),
        'browser back [<n>]':       Key('a-left:%(n)d'),
        'browser forward [<n>]':    Key('a-right:%(n)d'),
        'browser previous [<n>]':   Key('c-pgup:%(n)d'),
        'browser next [<n>]':       Key('c-pgdown:%(n)d'),
        #'browser new':             Key('c-t'),
        'browser close':            Key('c-w'),

        ## Xfce-like desktop environment commands
        #'(desk|desktop) left [<n>]': Key('ca-left:%(n)d'),
        #'(desk|desktop) right [<n>]': Key('ca-right:%(n)d'),
        #'(desk|desktop) up [<n>]': Key('ca-up:%(n)d'),
        #'(desk|desktop) down [<n>]': Key('ca-down:%(n)d'),
        #'(desk|desktop) (top|upper) [<n>]': Key('c-f1, ca-left, ca-right:%(n)d'),
        #'(desk|desktop) (bottom|lower) [<n>]': Key('c-f1, ca-down, ca-left, ca-right:%(n)d'),
        #'switch window [<n>]': Key('a-tab:%(n)d'),
        #'really close window': Key('a-f4'),
        #'maximize window': Key('a-f10'),
        #'minimize window': Key('a-f9'),

        # Some custom shortcuts to open my fav applications. Use Linux AutoKey to switch to these programs when needed.
        "change to Firefox":            Key("ctrl:down/3, win:down/3, alt:down/3, f") + Key("ctrl:up, win:up, alt:up"),
        "change to console":            Key("ctrl:down/3, win:down/3, alt:down/3, c") + Key("ctrl:up, win:up, alt:up"),
        "change to text":               Key("ctrl:down/3, win:down/3, alt:down/3, t") + Key("ctrl:up, win:up, alt:up"),
        "change to sublime":            Key("ctrl:down/3, win:down/3, alt:down/3, s") + Key("ctrl:up, win:up, alt:up"),
        "change to dolphin":            Key("ctrl:down/3, win:down/3, alt:down/3, d") + Key("ctrl:up, win:up, alt:up"),

        # Switching OSes, when Windows is in a VM on top of a Linux host:
        # (These functions have been moved to "_aenea.py")
        #"change to Linux":              Key("ctrl:down/3, win:down/3, alt:down/3, l") + Key("ctrl:up, win:up, alt:up"),
        #"change to Windows":            Key("ctrl:down/3, win:down/3, alt:down/3, w") + Key("ctrl:up, win:up, alt:up"),

        # For some universal operations whose shortcuts vary between applications, run a Linux AutoKey script that knows the correct keyboard shortcut.
        "find":                         Key("ctrl:down/3, win:down/3, alt:down/3, shift:down/3, f") + Key("ctrl:up, win:up, alt:up, shift:up"),
        "change to left tab [<n> times]":           Key("ctrl:down/3, win:down/3, alt:down/3, shift:down/3, l/90:%(n)d") + Key("ctrl:up/3, win:up/3, alt:up/3, shift:up/3"),
        "change to right tab [<n> times]":          Key("ctrl:down/3, win:down/3, alt:down/3, shift:down/3, r/90:%(n)d") + Key("ctrl:up/3, win:up/3, alt:up/3, shift:up/3"),
        "change to previous tab [<n> times]":       Key("ctrl:down/3, win:down/3, alt:down/3, shift:down/3, p/50:%(n)d/50") + Key("ctrl:up, win:up, alt:up, shift:up"),
        "change to next tab [<n> times]":           Key("ctrl:down/3, win:down/3, alt:down/3, shift:down/3, n/50:%(n)d/50") + Key("ctrl:up, win:up, alt:up, shift:up"),
        #"change to left <n> times":     Key("ctrl:down/3, win:down/3, alt:down/3, shift:down/3, l") + Key("ctrl:up, win:up, alt:up, shift:up"),
        #"change to right <n> times":    Key("ctrl:down/3, win:down/3, alt:down/3, shift:down/3, r") + Key("ctrl:up, win:up, alt:up, shift:up"),
        "close tab":                    Key("ctrl:down/3, win:down/3, alt:down/3, shift:down/3, c") + Key("ctrl:up, win:up, alt:up, shift:up"),

        # My current aenea proxy system isn't allowing to hold down shift or caps lock, so try using Linux AutoKey instead
        "press caps lock": Key("ctrl:down/3, win:down/3, alt:down/3, z") + Key("ctrl:up, win:up, alt:up"),

        # Moved to _aenea.py
        #"window list":      Key("win:down/999, tab") + Key("win:up"),

        # Konsole shortcuts
        #"search": Key("c-r"),   # Ctrl+R
        #"find": Key("ctrl:down/3, shift:down/3, f") + Key("ctrl:up, shift:up"),   # Ctrl+Shift+F

        "perforce": Text("p4"),
        "SSH remote": Text("ssh -XC $REMOTE"),
        "dollar sign remote": Text("$REMOTE"),
        "profile remote": Text("profile_remote whole"),
        "list files": Text("ls -oAFh --color=auto"),

    }
    extras = [
        Dictation("text"),
        IntegerRef("n", 1, 100),
        Choice('gitcommand', gitcommand),
    ]
    defaults = {
        "n": 1,
    }
