import subprocess
import sys
import configparser
import os
import signal
import logging
import argparse

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

output_name = None
DEFAULT_RESOLUTION = "1024x768"
DEFAULT_POSITION = "auto"
DEFAULT_SCALE = "1"

def check_command(command):
    """Check if a command is available on the system."""
    result = subprocess.run(['which', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        logging.error(f"{command} could not be found, please install it.")
        sys.exit(1)

def create_headless_output():
    """Create a headless output using hyprctl."""
    result = subprocess.run(['hyprctl', 'output', 'create', 'headless'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        logging.error("Failed to create headless output.")
        sys.exit(1)

def get_output_name():
    """Get the name of the newly created headless output."""
    result = subprocess.run(['hyprctl', 'monitors'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        logging.error("Failed to get monitors.")
        sys.exit(1)
    output = result.stdout.decode('utf-8')
    for line in output.split('\n'):
        if 'HEADLESS' in line:
            return line.split()[1]
    logging.error("Failed to find headless output.")
    sys.exit(1)

def configure_output(output_name, resolution, position, scale):
    """Configure the output resolution."""
    result = subprocess.run(['hyprctl', 'keyword', f'monitor {output_name},{resolution},{position},{scale}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        logging.error("Failed to configure output resolution.")
        sys.exit(1)

def start_wayvnc(output_name):
    """Start the wayvnc server."""
    result = subprocess.Popen(['wayvnc', '-gdo', output_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode is not None and result.returncode != 0:
        logging.error("Failed to start wayvnc server.")
        sys.exit(1)

def get_ip_address():
    """Get the IP address of the machine."""
    result = subprocess.run(['hostname', '-I'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        logging.error("Failed to get IP address.")
        sys.exit(1)
    return result.stdout.decode('utf-8').split()[0]

def read_config():
    """Read the configuration file for resolution."""
    config_path = os.path.expanduser('~/.config/virtual-screen/config.ini')
    config = configparser.ConfigParser()
    if os.path.exists(config_path):
        config.read(config_path)
        resolution = config['Settings']['resolution'] if ('Settings' in config and 'resolution' in config['Settings']) else DEFAULT_RESOLUTION
        position = config['Settings']['position'] if ('Settings' in config and 'position' in config['Settings']) else DEFAULT_POSITION
        scale = config['Settings']['scale'] if ('Settings' in config and 'scale' in config['Settings']) else DEFAULT_SCALE
    else:
        logging.warning("Config file not found or values not set. Using default values.")
        resolution = DEFAULT_RESOLUTION
        position = DEFAULT_POSITION
        scale = DEFAULT_SCALE
    return resolution, position, scale

def remove_headless_output():
    """Remove the headless output using hyprctl."""
    global output_name
    if output_name:
        subprocess.run(['hyprctl', 'output', 'remove', output_name])
        logging.info(f"Removed headless output ({output_name}).")

def signal_handler(sig, frame):
    """Handle the SIGINT signal (Ctrl-C)."""
    logging.info("Exiting script...")
    remove_headless_output()
    sys.exit(0)

def main():
    global output_name

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Create a virtual second screen and optionally start a VNC server.")
    parser.add_argument('--no-vnc', '-n', action='store_true', help="Do not start the wayvnc server.")
    args = parser.parse_args()

    # Ensure hyprctl and wayvnc are installed
    check_command('hyprctl')
    if not args.no_vnc:
        check_command('wayvnc')

    # Read the resolution from the config file or use default
    resolution, position, scale = read_config()

    # Create a headless output
    create_headless_output()

    # Get the name of the newly created headless output
    output_name = get_output_name()

    # Configure the output resolution
    configure_output(output_name, resolution, position, scale)

    if not args.no_vnc:
        # Start the wayvnc server
        start_wayvnc(output_name)
        logging.info(f"VNC server started on the headless output ({output_name}).")

        # Optionally, display the IP address
        ip_address = get_ip_address()
        logging.info(f"Your IP address is: {ip_address}")
    else:
        logging.info(f"Headless output ({output_name}) created without VNC server.")

    # Wait for a signal (e.g., Ctrl-C)
    signal.pause()

if __name__ == "__main__":
    # Register the signal handler for SIGINT
    signal.signal(signal.SIGINT, signal_handler)
    main()