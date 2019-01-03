# Low-level keyboard input module
#
# Based on the work done by the creators of the Dictation Toolbox
# https://github.com/dictation-toolbox/dragonfly-scripts
#
# and _multiedit-en.py found at:
# http://dragonfly-modules.googlecode.com/svn/trunk/command-modules/documentation/mod-_multiedit.html
#
# Modifications by: Tony Grosinger
#
# Licensed under LGPL

from natlink import setMicState
from aenea import (
    Grammar,
    MappingRule,
    Text,
    Key,
    Mimic,
    Function,
    Dictation,
    Choice,
    Window,
    Config,
    Section,
    Item,
    IntegerRef,
    Alternative,
    RuleRef,
    Repetition,
    CompoundRule,
    AppContext,
)

from dragonfly.actions.keyboard import keyboard
from dragonfly.actions.typeables import typeables
if 'semicolon' not in typeables:
    typeables["semicolon"] = keyboard.get_typeable(char=';')


#  Note that this doesn't include the less common keys such as the "window" key.
release = Key("shift:up, ctrl:up, alt:up")


def cancel_and_sleep(text=None, text2=None):
    """Used to cancel an ongoing dictation and puts microphone to sleep.

    This method notifies the user that the dictation was in fact canceled,
     a message in the Natlink feedback window.
    Then the the microphone is put to sleep.
    Example:
    "'random mumbling go to sleep'" => Microphone sleep.

    """
    print("* Dictation canceled. Going to sleep. *")
    setMicState("sleeping")


# For repeating of characters.
specialCharMap = {
    "pipe": "|",
    "minus": "-",
    "dot": ".",
    "comma": ",",
    "backslash": "\\",
    "underscore": "_",
    "(asterisk|Asterix)": "*",
    "colon": ":",
    "(semicolon|semi-colon)": ";",
    "at symbol": "@",
    #"[double] quote": '"',
    "quotes": '"',
    "single quote": "'",
    "apostrophe": "'",
    "hash": "#",
    "dollar sign": "$",
    "percentage": "%",
    "ampersand": "&",
    "slash": "/",
    "equals": "=",
    "plus": "+",
    "space": " ",
    "exclamation mark": "!",		# "bang" sounds like "aim" that I might use for "a"
	#"bang": "!",
    "question mark": "?",
    "caret": "^",
	"tilde": "~",
	"back tick": "`",
	
    # some other symbols I haven't imported yet, lazy sorry
    # 'ampersand': Key('ampersand'),
    # 'apostrophe': Key('apostrophe'),
    # 'asterisk': Key('asterisk'),
    # 'at': Key('at'),
    # 'backslash': Key('backslash'),
    # 'backtick': Key('backtick'),
    # 'bar': Key('bar'),
    # 'caret': Key('caret'),
    # 'colon': Key('colon'),
    # 'comma': Key('comma'),
    # 'dollar': Key('dollar'),
    # #'(dot|period)': Key('dot'),
    # 'double quote': Key('dquote'),
    # 'equal': Key('equal'),
    # 'bang': Key('exclamation'),
    # 'hash': Key('hash'),
    # 'hyphen': Key('hyphen'),
    # 'minus': Key('minus'),
    # 'percent': Key('percent'),
    # 'plus': Key('plus'),
    # 'question': Key('question'),
    # # Getting Invalid key name: 'semicolon'
    # #'semicolon': Key('semicolon'),
    # 'slash': Key('slash'),
    # '[single] quote': Key('squote'),
    # 'tilde': Key('tilde'),
    # 'underscore | score': Key('underscore'),
}

## Modifiers for the press-command.
#modifierMap = {
#    "alt": "a",
#    "control": "c",
#    "shift": "s",
#    "super": "w",
#}
#
## Modifiers for the press-command, if only the modifier is pressed.
#singleModifierMap = {
#    "alt": "alt",
#    "control": "ctrl",
#    "shift": "shift",
#    "super": "win",
#}

# Careful of any word that sounds similar to up, 8, 1, 2, and Dragon keywords "spell", "click", "select", "correct that", "read that", "close window", "exit dragon"!

letterMap = {
    "(acid) ": "a",         # alpha is a bit like up. axis is like backspace. "(aim|and) ": "a",		# careful of 8, @, lace, lack. My "aim" sometimes gets picked up as "and".
    "(brain) ": "b",        #  "brown" is like down. "black" is like "ebike", "best" sometimes gets picked up as "this" or "guess". "B|the" sometimes gets picked up as "enter"
    "(char) ": "c",
    "(dozen) ": "d",		# "does" is like "geez", "drax" is like "right". "dam" is like down. "dim" is like "ding". "dug" is like dot. "des" is like "this". "desk" is like "verse", "dose", "this".
    "(ebike) ": "e",		# "ebike" is like "end black", "evo" isn't getting picked up! careful of x, see, end, as, up
    "(foxy) ": "f",		# My "fox" is like "false" # careful of F1, F2 ...
    "(golf) ": "g",             # My "gang" is like "can"
    "(hotel) ": "h",		# careful of 8 and quote
    "(itchy) ": "i",        # itchy is like teach
    "(julia) ": "j",
    "(krife) ": "k",		#kidding? krog? # krux is like plus. careful of equal, colon, capital queen, geez.  My "kaput" is like "up". My "kilo" sometimes gets picked up as "killer"
    "(lazy) ": "l",	  # lucy? My "lima" is like "clean" and "end". My L sometimes gets picked up as "help". "L" is like Dragon keyword "spell" :-(
    "(miley) ": "m",       # Mosfet is somehow like "plus" and "space"! # Mix is a bit like minus?  # My "mike" is similar to "my"
    "(nasal) ": "n",   # newish sometimes isn't heard or is like unix. noosh is maybe like mosfet. niche is like unix. # nose?  "Nippy" is like "up"
    "(omez) ": "o",     # orange is like end. oryx is like "echo".  My "osh" is like "as". My "omar" is like "home up"
    "(premier) ": "p",     # please is like lazy and xray, pingu is like undo. "pom" is like "upon" and "up home"
    "(queen) ": "q",    # "queen" is like "clean"
    "(remo) ": "r",       # rezone? rolex is like home. "rod" is like "right"
    "(salty) ": "s",     # "sook" is like "up", "size" is like "keys". careful of snake, space,
    "(trish) ": "t",        # tricky is like keys # teach is like itchy
    "(unix) ": "u",          # "urge"? # careful of yang
    "(video) ": "v",            # My "vix" is like "mix". My "vax" is like "backspace". My "van" is a bit like "then"
    "(wages) ": "w",      # wintel is like hotel, end and enter. week is like queen. "wes" is like "worse"
    "(x-ray) ": "x",
    "(yeelax) ": "y",     # yeeshim is like shift, yiddish is like trish, yazzam is like home or down, yeast is like left. yellow is like "end left", yoke is like black. # "yang" is like "end". Careful of letter "u", home. "why" is like "white" that is like "why tay"
    "(zimeesi) ": "z",     # zoobkoi is a bit like "close window" and "quotes"! zirconium? zircumference? zosepi? zidacious is like shift, zultani is like up home, zood is like undo and rude, zooki? zyxel is like click, zooch & zener are like insert! zulu, zoolex, zolex, zook and zeakbajived often aren't getting picked up! "zed" is like "said" and "set"
}


# generate uppercase versions of every letter
upperLetterMap = {}
for letter in letterMap:
    #upperLetterMap["bam " + letter] = letterMap[letter].upper()         #
    #upperLetterMap["bam " + letter] = letterMap[letter].upper()         #
    upperLetterMap["biz " + letter] = letterMap[letter].upper()         # My "fig char" fails
    #upperLetterMap["buzz " + letter] = letterMap[letter].upper()         # My "buzz" is like "plus"
    #upperLetterMap["fig " + letter] = letterMap[letter].upper()         # My "fig char" fails
    #upperLetterMap["gross " + letter] = letterMap[letter].upper()         # My "gross" is like "quotes"
    #upperLetterMap["bam " + letter] = letterMap[letter].upper()         # My "bam" is like "end"
    #upperLetterMap["big " + letter] = letterMap[letter].upper()         # My "big" is pretty good, but usually fails "big yeelax"
    #upperLetterMap["case " + letter] = letterMap[letter].upper()         # My "case" is too much like "plus"
    #upperLetterMap["capital " + letter] = letterMap[letter].upper()     # My "cap" is too much like "up"
    #upperLetterMap["sky " + letter] = letterMap[letter].upper()         # My "sky" is too much like "score" :-(
letterMap.update(upperLetterMap)


def handle_word(text):
    #words = map(list, text)
    #print text
    words = str(text).split()
    print 'word (', words, ')'
    if len(words) > 0:
        Text(words[0]).execute()
        if len(words) > 1:
            Mimic(' '.join(words[1:])).execute()


grammarCfg = Config("multi edit")
grammarCfg.cmd = Section("Language section")
grammarCfg.cmd.map = Item(
    {
        # Navigation keys.
        "up [<n> times]": Key("up:%(n)d"),
        "down [<n> times]": Key("down:%(n)d"),
        "left [<n> times]": Key("left:%(n)d"),
        "right [<n> times]": Key("right:%(n)d"),
        "page up [<n> times]": Key("pgup:%(n)d"),
        "page down [<n> times]": Key("pgdown:%(n)d"),
        "jump [<n> times]": Key("pgup:%(n)d"),
        "drop [<n> times]": Key("pgdown:%(n)d"),
        #"up <n> (page|pages)": Key("pgup:%(n)d"),
        #"down <n> (page|pages)": Key("pgdown:%(n)d"),
        #"left <n> (word|words)": Key("c-left/3:%(n)d/10"),
        #"right <n> (word|words)": Key("c-right/3:%(n)d/10"),
        "home": Key("home"),
        "end": Key("end"),
		"insert": Key("insert"),

		# Other special keys that could be nice to have, but might not be supported so far:
			#Caps_Lock
			#Alt_R
			#KP_Insert
			#Redo
			#XF86AudioPlay
			#XF86AudioNext
			#XF86AudioForward
			#XF86AudioPause
			#XF86AudioRaiseVolume
			#XF86AudioLowerVolume
			#XF86Back
			#KP_Next
			#Scroll_Lock
			#XF86MonBrightnessUp
			#XF86MonBrightnessDown
			#XF86ScrollUp
			#XF86ScrollDown
			#Insert
			#Next
			#XF86Next
			#XF86AudioMute
			#f1 ... f24
			#Print
			#Pause
        #"doc home": Key("c-home/3"),
        #"doc end": Key("c-end/3"),
        # Functional keys.
        #"space": release + Key("space"),
        "space [<n> times]": release + Key("space:%(n)d"),
        "(enter) [<n> times]": release + Key("enter:%(n)d"),
        "tab [<n> times]": Key("tab:%(n)d"),
        #"delete this line": Key("home, s-end, del"),  # @IgnorePep8
        "backspace [<n> times]": release + Key("backspace:%(n)d"),
        #"application key": release + Key("apps/3"),
        #"paste [that]": Function(paste_command),
        #"copy [that]": Function(copy_command),
        #"cut [that]": release + Key("c-x/3"),
        #"select all": release + Key("c-a/3"),
        #"[(hold|press)] met": Key("alt:down/3"),

        # Function keys. For some reason the functionKeyMap above isn't working for me.
        'F one': Key('f1'),
        'F two': Key('f2'),
        'F three': Key('f3'),
        'F four': Key('f4'),
        'F five': Key('f5'),
        'F six': Key('f6'),
        'F seven': Key('f7'),
        'F eight': Key('f8'),
        'F nine': Key('f9'),
        'F ten': Key('f10'),
        'F eleven': Key('f11'),
        'F twelve': Key('f12'),

        #"win key": release + Key("win/3"),
        #"window <char>": Key("win:down/3") + Text("%(char)s") + Key("win:up"),
        #"window run": Key("win:down/3") + Text("r") + Key("win:up"),
        #"release window": Key("win:up"),
        #"window [<num>]": Key("win:down/3") + Text("%(num)d") + Key("win:up"),    # Allow to say "window 2" to switch to the 2nd window
        "window 1": Key("win:down/3") + Text("1") + Key("win:up"),    # Allow to say "window 2" to switch to the 2nd window
        "window 2": Key("win:down/3") + Text("2") + Key("win:up"),    # Allow to say "window 2" to switch to the 2nd window
        "window 3": Key("win:down/3") + Text("3") + Key("win:up"),    # Allow to say "window 2" to switch to the 2nd window
        "window 4": Key("win:down/3") + Text("4") + Key("win:up"),    # Allow to say "window 2" to switch to the 2nd window
        "window 5": Key("win:down/3") + Text("5") + Key("win:up"),    # Allow to say "window 2" to switch to the 2nd window
        #"meta [<num>]": Key("alt:down/3") + Text("%(num)d") + release,      # Allow to say "meta 2" to hit Alt+2 to switch to the 2nd tab of Firefox, etc
		"meta": Key("alt:down/3"),    # Or do I prefer "alter"?
		"meta 1": Key("alt:down/3") + Text("1") + release,      # Allow to say "meta 2" to hit Alt+2 to switch to the 2nd tab of Firefox, etc
		"meta 2": Key("alt:down/3") + Text("2") + release,      # Allow to say "meta 2" to hit Alt+2 to switch to the 2nd tab of Firefox, etc
		"meta 3": Key("alt:down/3") + Text("3") + release,      # Allow to say "meta 2" to hit Alt+2 to switch to the 2nd tab of Firefox, etc
		"meta 4": Key("alt:down/3") + Text("4") + release,      # Allow to say "meta 2" to hit Alt+2 to switch to the 2nd tab of Firefox, etc
		"meta 5": Key("alt:down/3") + Text("5") + release,      # Allow to say "meta 2" to hit Alt+2 to switch to the 2nd tab of Firefox, etc
		#"meta 5": Key("alt:down/3") + Text("5") + release,      # Allow to say "meta 2" to hit Alt+2 to switch to the 2nd tab of Firefox, etc
		#"meta 6": Key("alt:down/3") + Text("6") + release,      # Allow to say "meta 2" to hit Alt+2 to switch to the 2nd tab of Firefox, etc
		#"meta 7": Key("alt:down/3") + Text("7") + release,      # Allow to say "meta 2" to hit Alt+2 to switch to the 2nd tab of Firefox, etc
		#"meta 8": Key("alt:down/3") + Text("8") + release,      # Allow to say "meta 2" to hit Alt+2 to switch to the 2nd tab of Firefox, etc
		"meta 9": Key("alt:down/3") + Text("9") + release,      # Allow to say "meta 2" to hit Alt+2 to switch to the 2nd tab of Firefox, etc
        #"hold met": Key("alt:down/3"),
        #"release met": Key("alt:up"),

        # My current aenea proxy system isn't allowing to hold down shift or caps lock, so I'm using Linux AutoKey instead. See "programs.py"
        "shift": Key("shift:down/3"),
        #"hold shift": Key("shift:down"),
        #"release shift": Key("shift:up"),
        "control": Key("ctrl:down/3"),
        #"hold control": Key("ctrl:down"),
        #"release control": Key("ctrl:up"),
        "release all": Key("shift:up, ctrl:up, alt:up, win:up"),
        #"press key <pressKey>": Key("%(pressKey)s"),

        # Closures.
        #"angle brackets": Key("langle, rangle, left/3"),
        #"[square] brackets": Key("lbracket, rbracket, left/3"),
        #"[curly] braces": Key("lbrace, rbrace, left/3"),
        #"(parens|parentheses)": Key("lparen, rparen, left/3"),
        #"quotes": Key("dquote/3, dquote/3, left/3"),
        #"backticks": Key("backtick:2, left"),
        #"single quotes": Key("squote, squote, left/3"),
        # Shorthand multiple characters.
        #"double <char>": Text("%(char)s%(char)s"),
        #"triple <char>": Text("%(char)s%(char)s%(char)s"),
        #"double escape": Key("escape, escape"),  # Exiting menus.
        # Punctuation and separation characters, for quick editing.
        "colon": Key("colon"),
        "semi-colon": Key("semicolon"),
        "comma": Key("comma"),
        "dot": Key("dot"),  # cannot be followed by a repeat count
        "full stop": Key("dot"),  # cannot be followed by a repeat count
        "point <n> [<num>]": Key("dot") + Text("%(n)d") + Text("%(num)d"),  # allow to say "number 1.23"
        "(dash|minus)": Key("hyphen"),
        "underscore": Key("underscore"),

        # These are needed by this grammar, otherwise many of these rules won't work!
        "<letters>": Text("%(letters)s"),
        "<char>": Text("%(char)s"),

        'less than': Key('langle'),     # angle bracket
		#'langle': Key('langle:%(n)d'),
        'curly brace':   Key('lbrace'),       # curly brace
        'square brace':   Key('lbracket'),      # square bracket
        'round bracket':    Key('lparen'),        # round parenthesis
        'greater than': Key('rangle'),
		#'rangle': Key('rangle'),
        'close curly brace':   Key('rbrace'),
        'close square brace':   Key('rbracket'),
        'close round bracket':   Key('rparen'),

        "escape": Key("escape"),
        "escape 2": Key("escape") + Key("escape"),

        'delete [<n> times]':       Key('del:%(n)d'),
		#'chuck [<n>]':       Key('del:%(n)d'),
        #'scratch [<n>]':     Key('backspace:%(n)d'),
		
        #"visual": Key("v"),
        #"visual line": Key("s-v"),
        #"visual block": Key("c-v"),
        #"doc save": Key("c-s"),
        #"(arrow|pointer)": Text("->"),

        #'fly [<n>]':  Key('pgup:%(n)d'),
        #'drop [<n>]':  Key('pgdown:%(n)d'),

        #'lope [<n>]':  Key('c-left:%(n)d'),
        #'(yope|rope) [<n>]':  Key('c-right:%(n)d'),
        #'(hill scratch|hatch) [<n>]': Key('c-backspace:%(n)d'),

        #'hexadecimal': Text("0x"),
        #'suspend': Key('c-z'),
		#'undo': Key('c-z'),  # Sounds too much like "end"
		'geez': Key('c-z'),

        #'word <text>': Function(handle_word),
        'number <num>': Text("%(num)d"),
        #'change <text> to <text2>': Key("home, slash") + Text("%(text)s") + Key("enter, c, e") + Text("%(text2)s") + Key("escape"),

        # Text corrections.
        #"again": Key("ctrl:down/3, shift:down/3, left") + Key("ctrl:up, shift:up"), # Type over a word
        #"fix missing space": Key("c-left/3, space, c-right/3"),
        #"remove extra space": Key("c-left/3, backspace, c-right/3"),  # @IgnorePep8
        #"remove extra character": Key("c-left/3, del, c-right/3"),  # @IgnorePep8
        # Microphone sleep/cancel started dictation.
        #"[<text>] (go to sleep|cancel and sleep) [<text2>]": Function(cancel_and_sleep),  # @IgnorePep8
    },
    namespace={
        "Key": Key,
        "Text": Text,
    }
)


class KeystrokeRule(MappingRule):
    exported = False
    mapping = grammarCfg.cmd.map
    extras = [
        IntegerRef("n", 1, 100),
        IntegerRef("num", 0, 100),
        Dictation("text"),
        #Dictation("text2"),
        Choice("char", specialCharMap),
        Choice("letters", letterMap),
        #Choice("modifier1", modifierMap),
        #Choice("modifier2", modifierMap),
        #Choice("modifierSingle", singleModifierMap),
    ]
    defaults = {
        "n": 1,
    }
