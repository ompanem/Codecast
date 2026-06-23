import tkinter as tk
import json
import subprocess
import sys
from tkinter import filedialog
from make_video import make_full_video


scenes = [] #All the scenes in the video
current_scene = 0 #The scene the user is currently editing  
window = tk.Tk()
window.resizable(False, False)
window.title("Codecast")
scene_label = tk.Label(window, text="Scene 1", font=("Arial", 20, "bold")) #Big title to show the current scene number
scene_label.grid(row=0, column=0, columnspan=2, pady=10) #place it at the top and make it 2 columns wide

code_label = tk.Label(window, text="Code", font=("Arial", 14))
code_label.grid(row=1, column=0, padx=10, pady=5)
code_box = tk.Text(window, height=10, width=40)
code_box.grid(row=2, column=0, padx=10, pady=5)

output_label = tk.Label(window, text="Output:", font=("Arial", 14))
output_label.grid(row=3, column=0, padx=10, pady=5)
output_box = tk.Text(window, height=5, width=40)
output_box.grid(row=4, column=0, padx=10, pady=5)

narration_label = tk.Label(window, text="Narration", font=("Arial", 14))
narration_label.grid(row=1, column=1, padx=10, pady=5)
narration_box = tk.Text(window, height=10, width=40)
narration_box.grid(row=2, column=1, padx=10, pady=5)

def export_video():
    save_path = filedialog.asksaveasfilename(
        defaultextension=".mp4",
        filetypes=[("MP4 video", "*.mp4")]
    )

    if not save_path:
        return
    code = code_box.get("1.0", "end-1c")
    narration = narration_box.get("1.0", "end-1c")
    output = output_box.get("1.0", "end-1c")
    scene = {"code": code, "narration": narration, "output": output}
    if current_scene < len(scenes):
        scenes[current_scene] = scene
    else:
        scenes.append(scene)

    with open("video.json", "w") as f:
        json.dump(scenes, f)
    make_full_video(scenes, save_path)

def load_scene(index):
    code_box.delete("1.0", "end")
    narration_box.delete("1.0", "end")
    output_box.delete("1.0", "end")

    scene = scenes[index]
    code_box.insert("1.0", scene["code"])
    narration_box.insert("1.0", scene["narration"])
    output_box.insert("1.0", scene["output"])
    scene_label.config(text=f"Scene {index + 1}")

def back_scene():
    global current_scene
    if current_scene==0:
        return
    code = code_box.get("1.0", "end-1c")
    narration = narration_box.get("1.0", "end-1c")
    output = output_box.get("1.0", "end-1c")

    scene = {"code": code, "narration": narration, "output": output}

    if current_scene<len(scenes):
        scenes[current_scene] = scene
    else:
        scenes.append(scene)
    current_scene-=1
    load_scene(current_scene)
def next_scene(): 
    global current_scene
    
    code = code_box.get("1.0", "end-1c")
    narration = narration_box.get("1.0", "end-1c")
    output = output_box.get("1.0", "end-1c")
    scene = {"code": code, "narration": narration, "output": output}
    if current_scene<len(scenes):
        scenes[current_scene] = scene
    else:
        scenes.append(scene)
    current_scene+=1

    if current_scene< len(scenes):
        load_scene(current_scene)
    else:
        code_box.delete("1.0", "end")
        narration_box.delete("1.0", "end")
        output_box.delete("1.0", "end")
        scene_label.config(text=f"Scene {current_scene+1}")

back_button = tk.Button(window, text="Previous Scene", command=back_scene, font=("Arial", 12))
back_button.grid(row=5, column=1, padx=10, pady=5)
next_button = tk.Button(window, text="Next Scene", command=next_scene, font=("Arial", 12))
next_button.grid(row=3, column=1, padx=10, pady=5)
export_button = tk.Button(window, text="Export Video", command=export_video, font=("Arial", 12))
export_button.grid(row=4, column=1, padx=10, pady=5)

window.mainloop()

