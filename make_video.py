from PIL import Image, ImageDraw, ImageFont
import os
import subprocess
import edge_tts
import asyncio
import json
import shutil
import sys

def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "bin", filename)

FFMPEG = resource_path("ffmpeg.exe")
FFPROBE = resource_path("ffprobe.exe")
#There are multiple paths so it's compatible with MAC, Linux, and Windows
def load_fonts(possible_paths, size):
    for path in possible_paths:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()

#Done so the coding can sync with the audio length
def get_audio_length(filename):
    result = subprocess.run(
        [
            FFPROBE, "-v", "error",
            "-show_entries", "format=duration", #show only the duration entries
            "-of", "default=noprint_wrappers=1:nokey=1", #print just the number, nothing else
            filename
        ],
        capture_output=True, #get what ffprobe outputs to use for code
        text=True #get the output as a string instead of bytes
    )
    return float(result.stdout)

async def make_voice(text, fileName):
    tts = edge_tts.Communicate(text, "en-US-GuyNeural")
    await tts.save(fileName)



#======SETUP======
FORMAT = "landscape"  #can either be landscape or shorts
BACKGROUND_COLOR = (18,20,26)
CODE_PANEL_COLOR = (28,31,40)
OUTPUT_PANEL_COLOR = (12,14,18)
DOT_RED = (237, 106, 94)
DOT_YELLOW = (244,191, 79)
DOT_GREEN = (98,197, 84)
DOT_COLORS = [DOT_RED, DOT_YELLOW, DOT_GREEN]  
PANEL_RADIUS = 24

if FORMAT == "shorts":
    WIDTH, HEIGHT = 1080, 1920
else:
    WIDTH, HEIGHT = 1920, 1080

VIDEO_DIMENSIONS = (WIDTH, HEIGHT)


MONO_FONT_PATHS = [
    "C:/Windows/Fonts/consola.ttf",
    "/System/Library/Fonts/Menlo.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
]

code_font = load_fonts(MONO_FONT_PATHS, int(HEIGHT*.03))
CODE_TEXT_COLOR = (235,238,245)

def draw_frame(code_displayed, output_text):
    img = Image.new("RGB", VIDEO_DIMENSIONS, BACKGROUND_COLOR)
    #Just the spacing, tinkered around with the values until it looked goodd
    panel_margin_x = int(WIDTH*.04)
    text_padding_x = int(WIDTH*.03)
    dot_padding_x = text_padding_x

    #code panel edges (top section of video editor)
    code_left = panel_margin_x
    code_top = int(HEIGHT*.06)
    code_right = WIDTH-panel_margin_x
    code_bottom = int(HEIGHT*.62)

    #output panel edges (bottom section of video editor)
    output_left = panel_margin_x
    output_top = int(HEIGHT*.66) #slight gap between code bottom and top of output
    output_right = WIDTH-panel_margin_x
    output_bottom = int(HEIGHT*.92)


    #Make a drawing canvas to draw stuff like lines and shapes on the image
    drawing_tool = ImageDraw.Draw(img)

    #Draw code panel
    drawing_tool.rounded_rectangle(
        [code_left, code_top, code_right, code_bottom],
        radius=PANEL_RADIUS,
        fill=CODE_PANEL_COLOR       
    )

    #Draw output panel
    drawing_tool.rounded_rectangle(
        [output_left, output_top, output_right, output_bottom],
        radius=PANEL_RADIUS,
        fill=OUTPUT_PANEL_COLOR
    )

    #for the circles on top of the window
    DOT_RADIUS = int(HEIGHT*.01)
    DOT_SPACING = int(HEIGHT*.025)
    dot_padding_y = int(HEIGHT*.02)
    dot_y = code_top + dot_padding_y
    dot_x = code_left + dot_padding_x

    for index, color in enumerate(DOT_COLORS):
        #xpos = edge_pos + padding + distance pushed right
        dot_x = code_left + dot_padding_x + index*DOT_SPACING
        
        drawing_tool.ellipse(
            [dot_x, dot_y, dot_x + DOT_RADIUS*2, dot_y + DOT_RADIUS*2],
            fill=color
        )
    #split the code at a newline so we can draw each line one by one
    code_lines = code_displayed.split("\n")
    line_height = int(HEIGHT*.05)
    text_x = code_left + text_padding_x
    text_y = code_top + int(HEIGHT*.10)

    #draw each line with the typing animation and move down so the next line is underneath
    for line in code_lines:
        drawing_tool.text((text_x, text_y), line, font=code_font, fill=CODE_TEXT_COLOR)
        text_y+=line_height
    output_x = output_left + text_padding_x
    output_y = output_top + int(HEIGHT*.05)
    for line in output_text.split("\n"):
        drawing_tool.text((output_x, output_y), line, font=code_font, fill=CODE_TEXT_COLOR)
        output_y+=line_height
    return img

def make_scene(scene, scene_number):
    code = scene["code"]
    narration = scene["narration"]
    output = scene["output"]
    asyncio.run(make_voice(narration, f"voice_{scene_number}.mp3"))
    FPS = 5
    audio_length = get_audio_length(f"voice_{scene_number}.mp3")
    total_frames = int(audio_length*FPS)
    #So typing doesn't immediately start slight delay
    start_hold_frames = total_frames//6
    #Same with the end so the video doesn't end abruptly
    end_hold_frames = total_frames//3 - start_hold_frames
    typing_frames = total_frames-end_hold_frames-start_hold_frames


    frame_number = 0
    scene_folder = f"frames_{scene_number}"
    os.makedirs(scene_folder, exist_ok=True)
    #draw the empty editor for a few frames so there's a short pause before typing starts
    for s in range(start_hold_frames):
        frame = draw_frame("", "")
        frame.save(f"{scene_folder}/frame_{frame_number:04d}.png")
        frame_number+=1

    for n in range(typing_frames):
        #the n+1 is so there isn't an extra blank frame in the typing animation since we already have a start buffer
        typing_progress = (n+1)/typing_frames #how far we are through typing as a percent (0 to 1)
        chars_to_show = int(typing_progress* len(code))  #multiply the progress by the length to get the number of characters to type
        frame = draw_frame(code[:chars_to_show], "")  #draw only that many characters 
        frame.save(f"{scene_folder}/frame_{frame_number:04d}.png")
        frame_number+=1

    #same as start_hold_frames loop, so there's a buffer before the video ends
    for h in range(end_hold_frames):
        frame = draw_frame(code, output)
        frame.save(f"{scene_folder}/frame_{frame_number:04d}.png")
        frame_number+=1

    subprocess.run([
        FFMPEG, #program running 
        "-y",     #yes to file override
        "-framerate", str(FPS), #play the video at 5 fps
        "-i", f"{scene_folder}/frame_%04d.png",
        "-i", f"voice_{scene_number}.mp3",
        "-c:a", "aac",
        "-pix_fmt", "yuv420p",
        "-shortest",
        f"scene_{scene_number}.mp4"
    ])
    
def make_full_video(scenes, output_path):
    for scene_number, scene in enumerate(scenes):
        make_scene(scene, scene_number)

    with open("scenes.txt", "w") as f:
        for i in range(len(scenes)):
            f.write(f"file 'scene_{i}.mp4'\n")

    subprocess.run([
        FFMPEG,
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", "scenes.txt",
        "-c", "copy",
        output_path
    ])

    for i in range(len(scenes)):
        os.remove(f"voice_{i}.mp3")
        os.remove(f"scene_{i}.mp4")
        shutil.rmtree(f"frames_{i}")
    os.remove("scenes.txt")