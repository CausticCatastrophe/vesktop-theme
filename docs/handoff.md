# Handoff: Vesktop Frosted Glass theme (2026-11-06)

Resume by reading this file, then `~/claude-os/runbooks/2026-11-06-vesktop-frosted-glass-theme.md`.

## State
- Theme file rebuilt and installed at `~/.config/vesktop/themes/FrostedGlass.theme.css`. NOT yet enabled or viewed. Enabled-themes list was wiped by a Vesktop reset at 11:16.
- QuickCSS (`~/.config/vesktop/settings/quickCss.css`) is empty on purpose.
- Windows titlebar addon is OFF (it killed hover on the DM glyph). user-tags addon is ON, untested.

## Project layout
- `fg-mapped.css` upstream Frosted Glass with new Discord class names
- `user-settings.css` variables and hide rules (template, `__BG__` is the image)
- `assets/background-2560.jpg` and `background-orig.jpg` (imgur kYW2H5C)
- `build.py` builds `dist/` and installs into the Vesktop themes folder
- `quickcss-v2.css` last good QuickCSS patches, NOT applied
- `tools/remap.py` class mapper, `tools/bisect.py` theme bisect helper (paths point at an old scratch folder, edit before use)

## Next steps, in order
1. In Vesktop: Settings, Vencord, Themes, enable Frosted Glass, Ctrl+R. Check background, DM glyph hover, panel darkness.
2. Re-apply layout fixes inside the theme, not QuickCSS: take `quickcss-v2.css` (clear `container_H5ozaj`, rail at middle brightness with 10px top padding, title bar, one overlay per panel). Add it to `build.py` as a section after the mapped CSS.
3. Map the unresolved classes by hand: context menu, typing line, chat name line looked too dark from stacked overlays.
4. Make resets harmless: `git init` this project and commit; add a backup of `~/.config/vesktop/themes` and `settings` (systemd user timer, see scheduling agent); ask for snapper on `@home` (needs sudo, give commands to the user).
5. Find why Vesktop reset at 11:16 (journal around that time, vesktop-bin 1.6.8-2, electron44). Nothing this session wrote to sessionData.
6. Re-enter Vesktop and Vencord plugin settings; re-add the hide rules lost past `#message-tts`.

## Open checks
- Is user-tags addon safe for hover? Does the DM glyph still respond with the rebuilt theme?
- Does Discord rename classes again? Re-run `tools/remap.py` against fresh bundles.

## Gotchas
- Never regex across the theme file: the embedded image makes `[^{}]*` hang. Use find/rfind.
- Terminal-pasted console snippets wrap. Short lines, `;` before `[`.
- Do not store the only copy of anything in `~/.config/vesktop`.
- User wants the original theme look. Avoid stacking overlays on nested panels.
- Nothing is committed. Everything here is uncommitted.
