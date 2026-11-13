# BasedCode 1.0 validation

Test baseline: Omarchy **4.5.0-3**, Linux/Hyprland Lua configuration, NVIDIA hardware
video decoding. Tested on a 2560×1440 landscape display and two rotated 1920×1080
displays, including 1.25× scaling. The centre display began at 1× and was independently
changed to 2× during testing; that setting was preserved. Build inputs are recorded in `qa/build-info.json`
in the source distribution.

## Automated results

- 51 palette, shell and editor contrast checks pass (`qa/validation.json`).
- 31 theme/generated files checked for unresolved placeholders; TOML, JSON and Foot INI parsed.
- Foot and Ghostty native configuration validation pass; generated Hyprland and Neovim Lua parse.
- Installed Aether loads the generated palette successfully. All 12 sampled highlight groups
  exceed 4.5:1: comments 6.87:1, selection 12.64:1, search 7.71:1, diagnostics at least 9.28:1.
- The weakest tested essential focus pair is Lumen on Core, 3.45:1; Lumen on Deep is 4.43:1.
- Primary white text on Carbon is 18.92:1. Muted text on Carbon is 6.87:1.
- A fresh isolated home with a Git-marked theme stages correctly: the native generator creates
  terminal/Neovim configurations and keeps the colour-only VS Code override.
- BasedCode → Vantablack → BasedCode succeeds in isolated native staging and remembers a
  previously selected still wallpaper.
- The same theme round trip passed on the live desktop with no Hyprland configuration errors.
- A native screen recording produced 368 H.264 frames at 1920×1080 over 6.03 seconds,
  without audio. A decoded frame was visually inspected, including a readable notification.
  The test harness initially timed out on inherited recorder output pipes; launch and stop
  now write to files. Recording artifacts remain private. See `qa/live-validation.json`.
- Video is H.264, yuv420p, 3840×2160, 30 fps, 12 seconds, and has no audio stream.
- Source endpoints differ by at most one channel value due to floating-point rounding.
  Encoded wraparound mean channel difference is 0.323/255; movement is measurable after two
  seconds (mean channel difference 2.989/255). See `qa/motion-validation.json`.

## Visual inspection

Reviewed the landscape wallpaper, portrait crop, six-frame motion contact sheet, and
schematic surface sheet. Inspected actual Foot ANSI/selection output, active and inactive
window borders, the native menu, the transparent bar, and the native non-locking lock preview.
The wallpaper preview and lock-preview capture included in the package contain no private
application content. Other workstation screenshots remain local and are not distributed.

The native lock screen blurs and crops its text-free wallpaper poster. This package preserves that native treatment instead of modifying
authentication UI code. The lock field has an opaque Carbon background and a Lumen border.

The native video renderer reported ready, `hwdec=nvdec`, three outputs, and no swap failures
at the initial check. Selecting the still reported `has_video=false` and `engine=shell`.

## Resource measurements

Each mode was sampled 60 times over approximately five minutes. Public results are in
`qa/performance-summary.json` in the source distribution.

| Observed mean | Still | 4K animation |
|---|---:|---:|
| Shell + wallpaper CPU (% of one core) | 1.14% | 4.46% |
| Shell + wallpaper RSS | 1054.0 MiB | 1537.4 MiB |
| Whole GPU utilisation | 6.80% | 6.22% |
| Whole decoder utilisation | 1.30% | 2.92% |
| Whole GPU memory | 2783.48 MiB | 4288.58 MiB |
| Whole GPU power | 55.77 W | 96.48 W |

CPU measurements cover the shell and wallpaper processes; GPU, decoder, memory and power
totals include other running apps. Animation is not free: use the matching still when
minimising resource use matters. No renderer swap failures were reported during inspection.
The centre monitor scale changed during the measurement period, so the samples are not
a controlled A/B comparison. They should not be interpreted as exact wallpaper-only GPU cost.

## Limits and manual follow-up

- VS Code-family editors, Kitty, Alacritty, Helix and btop are covered by generated-config
  checks where unavailable; this report does not claim live visual validation for them.
- Neovim was tested through the installed Aether runtime without loading the user's full
  plugin set. Existing user transparency rules are preserved and can change backgrounds.
- Native lock **preview** was tested. Password authentication and real suspend/resume are
  deliberately not exercised during an active work session; confirm these during normal use.
- Polkit is configuration/contrast-checked, not tested by triggering an unnecessary privileged action.
- Opaque-bar colours pass token checks; the live desktop retains its existing transparent bar.
- The animation has been inspected as decoded frames and native playback status. Subjective
  distraction and long-session comfort still depend on the user; the matching still is provided.

The theme implementation changed no stock Omarchy files, global templates, widget layouts,
shortcuts, monitor settings or font sizes. Shell, bindings and look-and-feel hashes remained
unchanged. The monitor file changed independently during the session and was not reverted.
Original appearance state is saved by the local installer.

Text-free revision: rebuilt both wallpapers without the wordmark, rechecked the motion seam,
and inspected live desktop and lock previews. Native playback remains ready with zero swap failures.
