# Timi - Simple Command Line Timer

Timi is a lightweight command-line timer application that allows you to set and manage multiple concurrent timers.

## Features

- Set multiple concurrent timers
- Support for hours, minutes, seconds, and milliseconds
- Pause and resume timers
- List active timers and their remaining time
- Clear all timers at once
- Remove individual timers

## Installation

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
