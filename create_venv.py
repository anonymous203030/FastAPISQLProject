import logging
import os
import subprocess
import sys


def create_venv(env_name="venv"):
    # create venv
    subprocess.run([sys.executable, "-m", "venv", env_name], check=True)
    logging.info("Virtual environment created successfully!")

    # Windows/Linux specification
    if os.name == 'nt':  # For Windows
        activate_script = os.path.join(env_name, "Scripts", "activate.bat")
        print(f"To activate the virtual environment, run: {activate_script}")
    else:  # For macOS/Linux
        activate_script = os.path.join(env_name, "bin", "activate")
        print(f"To activate the virtual environment, run: source {activate_script}")

    requirements_file = "requirements.txt"
    if os.path.isfile(requirements_file):
        print(f"Installing dependencies from {requirements_file}...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_file])
        print("Dependencies installed successfully.")


# Run virtual env function
if __name__ == "__main__":
    create_venv()
