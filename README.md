# Buckshot-Pi

`buckshot-pi` is used for developing and deploying `buckshot`'s data ingestion on a Raspberry Pi. <br />
`buckshot-pi` captures images using a Raspberry Pi Camera Module 2, screens the images for wildlife using SpeciesNet hosted on AWS Lambda, and uploads all wildlife pictures to a gallery on AWS S3, all of which happens autonomously with `cron`. To view the wildlife gallery, go to [this link does not exist yet](https://buckshot.reubenbeeler.me/gallery).

## Design Choices

- `buckshot-pi` is a 'development tool' because lightweight Raspberry Pis (like my Pi Zero 2 W) cannot serve a stable SSH server for VS Code. This repository allows you to develop in an IDE locally while interacting with the raspi using convenient scripts that automatically handle file syncing, memory management, and more.
- This project is designed to take photos on a regular interval (15 minutes) rather than taking photos in response to motion detection. I opted for interval-based photography due to ease-of-use and budget constraints, although I might implement motion detection via a long-range outdoor PIR sensor in the future.

## Requirements

- You should be running Linux (MacOS probably works too)
- You should have SSH access to a Raspberry Pi SBC with an attached Raspberry Pi Camera Module 2. My raspi was flashed with 64-bit Raspberry Pi OS Lite (similar operating systems should work too).
- You should have a place to put the raspi where it will see wildlife, like your backyard! Notes:
  - The Camera Module 2 has dynamic exposure but is quite bad for taking photos in the dark because its maximum exposure setting is still too low to see anything.
  - Be careful to weather-proof your pi. If it's outside, consider an enclosure like [TODO link `buckshot-pi-zero-2-enclosure`] to prevent corrosion from water/humidity.

If you want to build this project, you're in the right place! However, be prepared for some debugging. To make the process easier for you than it was for me, I've included some useful scripts and setup instructions to help you along the way.

## Setup Instructions

Run `./setup.sh` for some guided help. If you're having trouble with any of the scripts, make sure that all your environment variables are set in `.env` using `.env.example` as a template. Many of the python files can be tested independently by invoking them directly.

For `buckshot-pi` to run autonomously, it uses `cron`. The `./setup.sh` file should automatically set up the cron job at `/etc/cron.d/buckshot`, which executes `cronjob.sh` every 15 minutes during daylight. Edit `/etc/cron.d/buckshot` to change the hours/frequency that it runs. The cron job's log file is `/var/log/buckshot.log`.

## Common Problems & Solutions

1. ### Missing `picamera2` or other system packages

   If you see an error message like `ModuleNotFoundError: No module named 'picamera2'`, it means that `uv` failed to find the `picamera2` module, probably for one of the following reasons:
   - Your venv is not using your system python packages. <br />
     You can check with

   ```bash
   grep -E "include-system-site-packages\s*=\s*true" .venv/pyvenv.cfg 1>/dev/null 2>/dev/null && echo '✅ uv is using system site packages' || echo '❌ uv is NOT using system site packages'
   ```

   You can fix it with

   ```bash
   uv venv --system-site-packages --clear
   uv sync
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

## TODOs

- Update env variables to read from .env and get loaded automatically
- TODO in Description, make a link to Buckshot repo, SpeciesNet pypi package, and buckshot website
- TODO create `buckshot-pi-zero-2-enclosure` repo and link it in Requirements
- TODO mention ssh config and `uv` installation (and any other required packages) in the setup instructions
- Separate ssh and other pi scripts into a github template for reusability for future pi projects
- Update README.md with project structure and description
- Update README.md with installation scripts/instructions (and include 'include-system-site-packages = true' in py .venv)
- automate crontab creation using /etc/cron.d/ instead of `crontab -e`
- make py_util a python package instead of a git submodule
- make AWS Lambda garbage collect so it works on warm starts
- Write the Technical Difficulties section and move it to the `buckshot` parent repo README.

## Technical Difficulties:

- needed to compile wheels on separate device (which didn't work due to architecture mismatch): ml_dtypes==0.4.1, numpy==1.26.4, reverse-geocoder==1.5.1
- VS Code remote ssh server isn't stable on raspi zero 2 w, so I have to development via cli or locally and then sync with the pi
