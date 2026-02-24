# rpi-lego-robot

Code to control my Raspberry Pi + BrickPi controlled LEGO robot.
This version also has a static webcam.

See also my more recent [non-LEGO rpi robot](https://github.com/jaredclaypoole/rpi-gpio-robot).

## Setup

All of the following needs to be done on a Raspberry Pi, except for the browser interaction.
I recommend SSHing in.

(Note that you may have to use `sudo python3` to get BrickPi control on the Raspberry Pi.)

### Webcam feed server

Clone my fork of the webcam feed server and install the dependencies:

```
git clone https://github.com/jaredclaypoole/LiveStream-WebRTC-Flask-OpenCV.git
cd LiveStream-WebRTC-Flask-OpenCV
python3 -m pip install -r requirements-versionless.txt
```

Test the installation by running the server:

```
cd src
python3 server.py
```

Navigate to `http://<rpi-ip-address>:5000/video_feed` to view the video feed.

### GUI dependencies

Clone this repo and `cd` into its root directory.

```
python3 -m pip install -r requirements.txt
```

## Running the robot control GUI

First, start the webcam feed server as described in the Setup section.

Next, `cd` into this repo's root directory and run:

```
flet run --web --port <your-chosen-port> --hidden main_gui.py
```

Finally, navigate to `http://<rpi-ip-address>:<your-chosen-port>` to access the web gui.

## GUI instructions

The buttons on the interface should be relatively self-explanatory.

Currently the robot will keep moving until told to stop or change direction.

As an alternative to the buttons in the GUI, you can use the WSAD keys to move the robot,
space to stop, and J and K to decrease/increase speed.
