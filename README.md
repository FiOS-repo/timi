# Timi - Simple Command Line Timer

Timi is a lightweight command-line timer application that allows you to set and manage multiple concurrent timers.

## Features

- Set multiple concurrent timers
- Support for hours, minutes, seconds, and milliseconds
- Pause and resume timers
- List active timers and their remaining time
- Clear all timers at once
- Remove individual timers

## Installation (Other distros)
If you are using arch linux use the guide below for other distros follow these instructions
### Installing Dependencies
- Debian/Ubuntu:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-notify2 git
pip3 install --user colorama
```

- Fedora/RHEL:
```bash
sudo dnf install python3 python3-pip python3-notify2 git
pip3 install --user colorama
```

- OpenSUSE/SUSE:
```bash
sudo zypper install python3 python3-pip python3-notify2 git
pip3 install --user colorama
```

### Installing Timi
1. Clone the repository
```bash
git clone https://github.com/FiOS-repo/timi.git
cd timi
```

2. Set Up Directories
```bash
sudo mkdir -p /usr/bin
sudo mkdir -p /var/timi/timers 
sudo chmod 777 /var/timi/timers
```

3. Install Python Files
```bash
SITE_PACKAGES=$(python3 -c "import site; print(site.getsitepackages()[0])")
sudo mkdir -p "$SITE_PACKAGES/timi"
sudo install -Dm644 main.py "$SITE_PACKAGES/timi/"
sudo install -Dm644 timedeamon.py "$SITE_PACKAGES/timi/"
```

4. Create an Executable Wrapper
```bash
sudo tee /usr/bin/timi << 'EOF'
#!/bin/sh
python3 "$(python3 -c 'import site; print(site.getsitepackages()[0])')/timi/main.py" "$@"
EOF
sudo chmod 755 /usr/bin/timi
```

5. Verify Installation
```bash
timi help
```
## Installation (Arch Linux only)

I'm planing to publish it the AUR soon.

1. Clone the repository
2. Make sure that a `PKGBUILD` file exsits
3. Run `makepkg -si`

## Usage

### Setting Timers
```bash
timi 10s     # Set a timer for 10 seconds
timi 5m      # Set a timer for 5 minutes
timi 1h      # Set a timer for 1 hour
timi 100ms   # Set a timer for 100 milliseconds
timi 1h30m   # Set a timer for 1 hour and 30 minutes
```

### Managing Timers
```bash
timi get     # List all active timers
timi clear   # Clear all timers
timi remove timer1    # Remove a specific timer
timi toggle timer1    # Pause/resume a specific timer
```

### Help
```bash
timi help    # Show help message
```

## File Structure

- `main.py` - Main application logic
- `timedeamon.py` - Background timer daemon

## License

MIT
