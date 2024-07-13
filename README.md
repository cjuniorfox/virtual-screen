# Virtual Screen

This script, `hyprland-virtual-screen.py`, creates a virtual second screen using `hyprctl` and optionally starts a VNC server using `wayvnc`. It is useful for setting up a headless display environment.

## Prerequisites

- `hyprctl` must be installed on your system.
- `wayvnc` must be installed if you want to start the VNC server.

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Ensure `hyprctl` and `wayvnc` are installed on your system. You can install them using your package manager. For example, on Debian-based systems:
```bash
sudo apt-get install hyprctl wayvnc
```

## Configuration

You can create a configuration file at `~/.config/virtual-screen/config.ini` to specify the resolution, position, and scale of the virtual screen. If the configuration file is not found, default values will be used.

Example configuration file:
```ini
[Settings]
resolution = 1920x1080
position = auto
scale = 1
```

## Usage

Run the script with the following command:
```bash
python hyprland-virtual-screen.py
```

### Options

- `--no-vnc`, `-n`: Do not start the VNC server.

Example:
```bash
python hyprland-virtual-screen.py --no-vnc
```

## Logging

The script logs important information, such as whether the VNC server was started and the IP address of the machine.

## Signal Handling

The script handles the `SIGINT` signal (Ctrl-C) to clean up and remove the headless output before exiting.

## Example Script

The complete script is available on [GitHub](<hyprland-start-2nd-screen.py>).

## License

This project is licensed under the MIT License.