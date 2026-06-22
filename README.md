# Codecast

This project turns code and text into a synced narrated video

## Features

- Types out your code with an animation
- Generates narration automatically with text to speech
- Syncs the typing to the length of the narration   
- Pulls content from a JSON file so you can swap in new code and a script easily

## Why did I build this project?

Making coding videos is hard, you need to come up with a curriculum to teach, type everything out, record a voice over, and make sure both elements are aligned.  Codecast does all of this automatically from a single file so you can focus more on teaching

## Requirements
- **Python 3** - make sure it is installed
- **FFmpeg** - this is a seperate program (not a python package) so install it on your device
  - **Windows:** `winget install Gyan.FFmpeg`
  - **Mac:** `brew install ffmpeg`
  - **Linux:** `sudo apt install ffmpeg`

## How to run it
1. **Clone the repo**
```
 git clone https://github.com/ompanem/Codecast.git
 cd Codecast
```
2. **Install the python packages**
```
pip install -r requirements.txt
```
3. **Run it**
```
python make_video.py
```
This reads `video.json`, generates the narration, creates the frames, and outputs it into output.mp4