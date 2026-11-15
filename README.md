# Basedcode Dark for Omarchy

A quiet dark theme for building things: dark subtly plum-tinted working surfaces with lilac accents,
white text, clear focus indicators, and a solid photo-matched #1F241F wallpaper.

![Basedcode Dark desktop preview: Neovim, btop, terminal and Files](preview.png)

Built against **Omarchy 4.5.0-3** and [BasedCode Brand Bible v2.4](https://brand.basedcode.dev/).
The theme preserves the user's layout, shortcuts, font sizes, monitor settings, and opacity preferences.

## Install from GitHub

```sh
omarchy theme install https://github.com/BasedCodeDev/omarchy-basedcode-dark-theme
```

Omarchy installs and activates the theme as `basedcode-dark`. Its installer replaces an existing
theme with that name, so back up any local changes first. To use the bundled backup-aware
installer instead, clone this repository and follow the source installation below.

## Install from this source project

Run as your ordinary desktop user, not root:

```sh
python scripts/install.py --apply
```

This copies `theme/` into `~/.config/omarchy/themes/basedcode-dark`, records the previous theme,
saves the selected wallpaper, and activates Basedcode Dark. If Basedcode Dark already exists, it is
moved into the timestamped backup first. Backups live in
`~/.local/state/omarchy/basedcode-dark-backups/`; the installer prints the exact location.
The installer suppresses theme mirroring to other machines for this invocation.

Dependencies for using the theme: Omarchy's shell and native theme generator, video-wallpaper
support for animation, **Yaru-purple** icons, and **JetBrainsMono Nerd Font** (recommended).
Fonts and icons are not bundled or installed automatically. Omarchy selects its regular
Adwaita dark application mode; this is not a replacement GTK widget theme.

## Motion controls

The default wallpaper is the solid #1F241F still. The earlier silent 12-second, 30 fps animation is an optional alternative.
Choose either in Omarchy's background picker, or use:

```sh
# Stop wallpaper motion by selecting the still:
omarchy theme bg set ~/.config/omarchy/themes/basedcode-dark/backgrounds/02-basedcode-dark-still.png

# Restore the animation:
omarchy theme bg set ~/.config/omarchy/themes/basedcode-dark/backgrounds/03-basedcode-dark-motion.mp4
```

This is a still-image choice, not a frozen frame from a paused decoder. There is no custom
wallpaper service or shell animation plugin. Omarchy's lock screen uses its own video poster
and blur treatment. Both wallpapers are text-free.

## Switch back

Use the normal theme picker or `omarchy theme set vantablack`. To restore the exact saved
wallpaper and previous desktop appearance settings as well:

```sh
python scripts/rollback.py ~/.local/state/omarchy/basedcode-dark-backups/TIMESTAMP
```

Replace `TIMESTAMP` with the installer's printed backup directory. This restores the prior
active theme and wallpaper; it leaves the newly installed Basedcode Dark package available.
A pre-existing Basedcode Dark directory is preserved as `previous-basedcode-dark` in the backup.
If that was the previously active theme, rollback restores that package before selecting it.

## Design and application coverage

- Official colours: Carbon `#121014`, Plum `#1D0A25`, Deep `#2D1540`, Core `#472458`,
  Violet `#83478F`, Lumen `#B568C2`, and white.
- Secondary text comes from the guide's `#D7C9DD` and `#A995B2` tokens.
- Terminal errors, warnings, successes, syntax and diffs use restrained functional colours.
  These additions are documented exceptions, not new BasedCode brand colours.
- Working surfaces use `#19181B`, panels `#201E23` and selections `#472458`.
- Solid lilac `#D7A4E2` borders identify keyboard focus. White selected text avoids low-contrast purple-on-purple labels.
- The user's transparent bar remains transparent; an opaque bar uses the working-surface colour.
- Omarchy generates Foot, Ghostty, Kitty, Alacritty, Aether/Neovim, Helix, btop and other
  integrations from the palette. Only supported, installed applications are actually refreshed.
- The colour-only `vscode-theme.json` corrects low-contrast secondary buttons and focus indicators
  in the stock template. It retains native syntax mappings and does not request an extension download.
- User application customisations take precedence. For example, existing Neovim transparency
  customisations can remove backgrounds independently of this theme.

See [validation](docs/VALIDATION.md) for the distinction between live, parser, and generated-config tests.

## Rebuild

Use Python 3.11+ with pinned dependencies, FFmpeg with libx264, Fontconfig, an installed
JetBrains Mono font, and the tested Omarchy templates:

```sh
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/build_shell.py
.venv/bin/python scripts/build_editor.py
.venv/bin/python scripts/render.py --video
.venv/bin/python scripts/review.py
.venv/bin/python scripts/validate.py
.venv/bin/python scripts/check_motion.py
.venv/bin/python scripts/check_apps.py
.venv/bin/python scripts/check_staging.py
.venv/bin/python scripts/package.py
```

The normal render is 3840×2160. A lower-cost animation can be generated with
`scripts/render.py --video --width 2560 --height 1440`; the still remains 4K.
The wallpaper renderer is deterministic for the same dependencies and encoder. Different
FFmpeg versions may change compressed bytes; `qa/build-info.json` records the build inputs.

`src/design.json` defines the brand references and motion geometry; `theme/colors.toml` defines
application tokens. Shell and editor overrides are rebuilt from scripts. The wallpaper has
no external photographs or generated raster dependencies. Font files are not redistributed.

## Distribution

`scripts/package.py` produces a runtime archive and a separate source archive in `dist/`,
plus SHA-256 checksums. The runtime archive has `basedcode-dark/colors.toml` at its root folder,
so it can be extracted into `~/.config/omarchy/themes/` on another compatible installation.
Do not overwrite an existing theme directory without backing it up.

The repository root is directly installable with `omarchy theme install`. The `theme/`
directory is the editable source of the runtime files; `scripts/package.py` also synchronises
those files to the repository root. After editing or rebuilding assets, run that script and
commit both copies. Git stores identical file contents only once. Build caches, archives,
private screenshots and local rollback records are ignored.

The runtime package contains no executable Lua or terminal configuration overrides. It is
compatible with Omarchy's Git-installed theme staging rules. Personal screenshots, rollback
records, and raw workstation measurements under `qa/local/` are excluded from both archives.

## Rights and attribution

Original implementation code and unbranded procedural artwork are MIT-licensed; see `LICENSE`.
Basedcode Dark names and wordmarks remain the rights of their owner. The code licence grants no
trademark rights or implied endorsement. See `BRAND-RIGHTS.md` and `THIRD-PARTY-NOTICES.md`.

The current exact-match wallpaper is `backgrounds/02-basedcode-dark-still.png`. Select this
PNG for exact RGB; the earlier animation remains an optional alternative.

## Desktop preview

The preview is a real 2560×1440 capture with Neovim and its file tree, btop, a
terminal directory listing, and GNOME Files. Both variants use the same layout
and sample files. btop shows loopback networking instead of a private network
address, with the process list hidden. Fonts and monitor scaling are unchanged.
Files uses the native dark GTK appearance with Yaru-purple icons.

## Theme naming migration

The purple variant previously called **BasedCode Light** is now **Basedcode**
(`basedcode`, `BasedCodeDev/omarchy-basedcode-theme`). The grey variant previously
called **BasedCode** is now **Basedcode Dark** (`basedcode-dark`,
`BasedCodeDev/omarchy-basedcode-dark-theme`). Appearance and screenshots are unchanged.

The old unsuffixed GitHub URL now identifies the purple variant. Existing dark-theme
users must update their remote to `https://github.com/BasedCodeDev/omarchy-basedcode-dark-theme.git`.
Install the renamed dark variant before installing the purple variant to avoid replacing
an existing `basedcode` installation. Back up local changes and custom wallpapers first.
Use the new URLs explicitly: redirects do not change the theme slug derived from an old URL.

Historical rollback records remain untouched. The updated rollback script maps pre-rename
`basedcode` records to `basedcode-dark` and `basedcode-light` records to `basedcode`.
New records include versioned identity metadata and use the current names.

## Herdr integration

Herdr can use a dedicated Basedcode palette whenever this Omarchy theme is selected.
After installing the theme, run this explicit, optional integration step from the source
checkout (Python 3.11+, Herdr and Omarchy required):

```sh
python scripts/build_herdr.py
python scripts/herdr_integration.py install
```

Run it from each theme checkout when installing both siblings. Both installers maintain
one shared, versioned user hook. The installer backs up existing files, installs the
colour-only `herdr.toml` into the corresponding installed theme, and applies the active
palette immediately. A normal Git theme installation includes the palette but does not
install executable hooks automatically. The source archive includes the installer.

Selecting `basedcode` or `basedcode-dark` applies that theme's custom Herdr colours.
Selecting any other theme restores the appearance settings saved when entering the
Basedcode themes, including terminal-following behaviour. The transparent tab bar,
shortcuts, layouts, session state and unrelated configuration are preserved. Functional
status colours follow the Omarchy palette; these are usability exceptions to the brand's
purple-and-white decorative palette. Terminal font and transparency remain user-controlled.

The hook validates candidate configurations before replacing them and reloads a running
server without terminating sessions. It does not start a stopped server or contact remote
machines. Install this integration separately on each machine where it is wanted.
If you edit managed theme settings while it is active, it stops with a diagnostic rather
than overwriting those edits. The saved and last-applied settings are recorded in
`~/.local/state/omarchy/basedcode-herdr/active.json`; restore the last-applied settings
before retrying, or manually reconcile the saved settings before removing that record.

Remove the integration and restore the saved appearance with:

```sh
python ~/.local/share/basedcode-herdr/integration.py uninstall
```

Timestamped backups remain under `~/.local/state/omarchy/basedcode-herdr/`.
Uninstallation leaves colour-only theme data installed. Full config backups are available
for manual recovery, but restoring a whole backup would also revert subsequent unrelated edits.

Validate the palettes and switching behaviour without changing the live desktop:

```sh
python scripts/build_herdr.py
python scripts/check_herdr.py
python scripts/package.py
```
