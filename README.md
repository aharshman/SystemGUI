# Command HUD – System Monitor (Python GUI)

Command HUD is a lightweight desktop system monitor built with Python. It provides a real-time view of system performance through a clean, minimal interface using customtkinter and psutil.

The goal of this project is to create a simple but functional monitoring tool that is easy to run, visually clear, and useful for everyday system tracking.

---

## Features

### System Information
- Live CPU usage display
- Live RAM usage display
- System uptime tracking
- Operating system detection (Windows 10 and 11 support)
- Local IP address display

### Network Monitoring
- Real-time download and upload speeds
- Session-based network usage tracking

### Storage Metrics
- Disk usage percentage
- Available storage space in gigabytes

### Power Status
- Battery percentage (if available)
- Charging or plugged-in status

### Process Monitoring
- Top 5 processes by CPU usage
- CPU usage normalized across cores

### Interface
- Minimal dark-themed UI
- Always-on-top window
- Draggable custom header
- Updates automatically every second

---

## Preview

Add a screenshot here after running the application. This significantly improves how the project looks on GitHub.

---

## Requirements

- Python 3.8 or newer

Install dependencies:

pip install customtkinter psutil

---

## How to Run

Clone the repository:

git clone https://github.com/yourusername/command-hud.git
cd command-hud

Run the application:

python command_hud.py

---

## Project Structure

command-hud/
│── command_hud.py
│── README.md

---

## Notes

- This project is designed primarily for Windows systems
- Some features, such as battery status, may not be available on all devices
- Certain process information may be limited without elevated permissions

---

## Future Improvements

- GPU usage monitoring
- Temperature sensors
- Log export functionality
- Custom themes and layout options
- System alerts for high usage or low resources
- Packaged executable for easier distribution

---

## Purpose

This project was built to explore Python GUI development and system monitoring tools. It is intended to be both a practical utility and a portfolio project.

---

## License

This project is licensed under the MIT License.

---

## Author

Alexander Harshman

---

## Contributing

Contributions are welcome. Feel free to open issues or submit pull requests if you have ideas for improvements.
