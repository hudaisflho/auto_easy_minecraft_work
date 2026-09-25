# Minecraft Auto (mc.py)

A Python-based Minecraft automation script that simulates keyboard and mouse input to perform repetitive tasks such as mining forward, sprinting, boating, and tower-building.

> ⚠️ **Important:** The hotkey variables in `mc.py` (e.g. `mine_forward_key`, `rushing_key`) and the in-game key bindings (jump, sneak, sprint, etc.) **must be adjusted to match your own Minecraft settings**. The default values are just examples — if they don't match your game, the script won't work correctly.

## Features

- ⛏️ **Auto Mining** — holds `W` + left click to mine while moving forward
- 🏃 **Auto Sprint** — jumps, moves forward and sprints automatically
- 🚣 **Auto Boating** — holds forward + sprint to keep rowing
- 🧱 **Tower Building** — loops jump + place block to build upward
- 🛑 **One-key Stop** — press `0` to stop everything and release all keys
- 🔒 **Auto Admin Elevation** (Windows)
- ⌨️ Global hotkeys via `pynput`, works even when the game window is not focused

## Hotkeys

| Key | Action |
|-----|--------|
| `V` | Toggle auto mining |
| `C` | Toggle auto sprint |
| `X` | Toggle auto boating |
| `N` | Toggle tower building |
| `0` | Exit and release all keys |

> 🔧 These hotkeys are **user-configurable**. To change them, edit the trigger variables in `mc.py`:
>
> ```python
> mine_forward_key = 'v'
> rushing_key = 'c'
> boating_key = 'x'
> build_up_key = 'n'
> ```
>
> You can also remap the in-game action keys (jump, sprint, sneak, movement, attack, etc.) at the top of the file to match your own Minecraft key bindings.

## Requirements

- Python 3.7+
- Windows (uses `ctypes.windll` for admin elevation)
- Dependencies:

```bash
pip install pynput
