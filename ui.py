import tkinter as tk
import json
import subprocess
import sys

window = tk.Tk()
window.title("Codecast")
scene_label = tk.Label(window, text="Scene 1")
scene_label.grid(row=0, column=0, columnspan=2)

code_label = tk.Label(window, text="Code")
code_label.grid(row=1, column=0)
code_box = tk.Text(window, height=10, width=40)
code_box.grid(row=2, column=0)

output_label = tk.Label(window, text="Output:")
output_label.grid(row=3, column=0)
output_box = tk.Text(window, height=5, width=40)
output_box.grid(row=4, column=0)

narration_label = tk.Label(window, text="Narration")
narration_label.grid(row=1, column=1)
narration_box = tk.Text(window, height=10, width=40)
narration_box.grid(row=2, column=1)

def export_video():
    code = code_box.get("1.0", "end-1c")
    narration = narration_box.get("1.0", "end-1c")
    output = output_box.get("1.0", "end-1c")
    scene = {"code": code, "narration": narration, "output": output}
    scenes = [scene]

    with open("video.json", "w") as f:
        json.dump(scenes, f)
    subprocess.run([sys.executable, "make_video.py"])

    
export_button = tk.Button(window, text="Export Video", command=export_video)
export_button.grid(row=4, column=1)

window.mainloop()

