"""Build the Vesktop Frosted Glass theme from its parts.

Run:  python3 -I ~/Projects/vesktop-theme/build.py
Parts: fg-mapped.css (upstream Frosted Glass with Discord's Nov 2026 class names),
       layout-fixes.css (overlay and panel darkness fixes, from quickcss-v2.css),
       user-settings.css (your variables and hides), assets/background-2560.jpg.
Writes dist/FrostedGlass.theme.css and copies it into the Vesktop themes folder.
"""
import base64
import os
import shutil

P = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.expanduser('~/.config/vesktop/themes/FrostedGlass.theme.css')

HEAD = """/**
 * @name Frosted Glass
 * @author Gibbu#1211
 * @version 2.0.0
 * @description Display your picture of choice with adjustable blur and brightness. Dark theme is required.
 * @source https://github.com/DiscordStyles/FrostedGlass
 */

/* Font import */
@import url('https://fonts.googleapis.com/css2?family=Karla:ital,wght@0,200..800;1,200..800&display=swap');

/* BlackBox tags */
@import url('https://monstrousdev.github.io/themes/addons/user-tags.css');

/* The old Windows titlebar addon is OFF: it made the DM glyph unhoverable. */

"""

fg = open(P + '/fg-mapped.css').read()
user = open(P + '/user-settings.css').read()
layout = open(P + '/layout-fixes.css').read()
bg = base64.b64encode(open(P + '/assets/background-2560.jpg', 'rb').read()).decode()
user = user.replace('__BG__', bg)

css = (HEAD
       + '/* ==== FrostedGlass, class-mapped 2026-11-06 ==== */\n' + fg
       + '\n/* ==== layout fixes ==== */\n' + layout
       + '\n/* ==== user settings ==== */\n' + user)

os.makedirs(P + '/dist', exist_ok=True)
open(P + '/dist/FrostedGlass.theme.css', 'w').write(css)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
shutil.copy(P + '/dist/FrostedGlass.theme.css', OUT)
print('wrote', OUT, len(css), 'bytes')
