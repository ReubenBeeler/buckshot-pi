## Setup Instructions

If you build this project, be prepared to face many issues. Some useful scripts are attached to help you along your journey.

## TODOs

- TODO mention ssh config and `uv` installation (and any other required packages) in the setup instructions
- Separate ssh and other pi scripts into a github template for reusability for future pi projects
- Update env variables to read from .env and get loaded automatically
- Update README.md with project structure and description
- Update README.md with installation scripts/instructions (and include 'include-system-site-packages = true' in py .venv)
- automate crontab creation using /etc/cron.d/ instead of `crontab -e`
- make py_util a python package instead of a git submodule
- make AWS Lambda garbage collect so it works on warm starts

## Technical Difficulties:

- needed to compile wheels on separate device (which didn't work due to architecture mismatch): ml_dtypes==0.4.1, numpy==1.26.4, reverse-geocoder==1.5.1
- VS Code remote ssh server isn't stable on raspi zero 2 w, so I have to development via cli or locally and then sync with the pi

## Common Problems & Solutions

1. ### Missing `picamera2` or other system packages

   If you see something like this,

   ```bash
   reuben@pi-zero-2-W-buckshot:~/Code $ ./cronjob.sh
   Traceback (most recent call last):
   File "/home/reuben/Code/main.py", line 11, in <module>
   	from lib import *
   File "/home/reuben/Code/lib/__init__.py", line 1, in <module>
   	from .capture import *
   File "/home/reuben/Code/lib/capture.py", line 7, in <module>
   	from picamera2 import Picamera2 # pyright: ignore[reportMissingImports]
   	^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   ModuleNotFoundError: No module named 'picamera2'
   reuben@pi-zero-2-W-buckshot:~/Code $
   ```

   it means that `uv` failed to find you `picamera2` module, probably because:
   - Your venv is not using your system python packages. <br />
     You can check with

   ```bash
   grep -E "include-system-site-packages\s*=\s*true" .venv/pyvenv.cfg 1>/dev/null 2>/dev/null && echo '✅ uv is using system site packages' || echo '❌ uv is NOT using system site packages'
   ```

   You can fix it with

   ```bash
   uv venv --system-site-packages --clear
   ```

   - `picamera2` is not installed. <br/>
     You can check with

   ```bash
   /usr/bin/python -c 'import picamera2' 2>/dev/null && echo '✅ picamera2 is installed' || echo '❌ picamera2 is missing'
   ```

   You can fix it with

   ```bash
   sudo apt update
   sudo apt install -y python3-picamera2
   ```
