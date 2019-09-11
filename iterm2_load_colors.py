#!/usr/bin/env python3


import argparse
import plistlib
import iterm2


parser = argparse.ArgumentParser(description = 'iTerm2 color profile loader')
parser.add_argument('-q', '--quiet', help = 'be quiet', action = 'store_true')
parser.add_argument('file', help = '.itermcolors file to load')
args = parser.parse_args()


root = plistlib.load(open(args.file, 'rb'))


async def main(connection):

    app = await iterm2.async_get_app(connection)

    session = app.current_terminal_window.current_tab.current_session

    profile = iterm2.LocalWriteOnlyProfile()

    set_color = {
            'Foreground Color'    : profile.set_foreground_color,
            'Background Color'    : profile.set_background_color,
            'Bold Color'          : profile.set_bold_color,
            'Link Color'          : profile.set_link_color,
            'Selection Color'     : profile.set_selection_color,
            'Selected Text Color' : profile.set_selected_text_color,
            'Cursor Color'        : profile.set_cursor_color,
            'Cursor Text Color'   : profile.set_cursor_text_color,
            'Cursor Guide Color'  : profile.set_cursor_guide_color,
            'Badge Color'         : profile.set_badge_color,
            'Tab Color'           : profile.set_tab_color,
            'Underline Color'     : profile.set_underline_color,
            'Ansi 0 Color'        : profile.set_ansi_0_color,
            'Ansi 1 Color'        : profile.set_ansi_1_color,
            'Ansi 2 Color'        : profile.set_ansi_2_color,
            'Ansi 3 Color'        : profile.set_ansi_3_color,
            'Ansi 4 Color'        : profile.set_ansi_4_color,
            'Ansi 5 Color'        : profile.set_ansi_5_color,
            'Ansi 6 Color'        : profile.set_ansi_6_color,
            'Ansi 7 Color'        : profile.set_ansi_7_color,
            'Ansi 8 Color'        : profile.set_ansi_8_color,
            'Ansi 9 Color'        : profile.set_ansi_9_color,
            'Ansi 10 Color'       : profile.set_ansi_10_color,
            'Ansi 11 Color'       : profile.set_ansi_11_color,
            'Ansi 12 Color'       : profile.set_ansi_12_color,
            'Ansi 13 Color'       : profile.set_ansi_13_color,
            'Ansi 14 Color'       : profile.set_ansi_14_color,
            'Ansi 15 Color'       : profile.set_ansi_15_color,
    }

    def interp(x):
        return int(round(x * 255))

    for key in root.keys():
        red   = interp(root[key]['Red Component'])
        green = interp(root[key]['Green Component'])
        blue  = interp(root[key]['Blue Component'])
        try:
            alpha = interp(root[key]['Alpha Component'])
        except KeyError:
            alpha = 255
        set_color[key](iterm2.Color(red, green, blue, alpha))

    if not args.quiet:
        for key in set(set_color.keys()) - set(root.keys()):
            print(f'Warning: Missing key \'{key}\' in {args.file}')

    await session.async_set_profile_properties(profile)


iterm2.run_until_complete(main)
