from moviepy.editor import ColorClip

# Generate a 3-second red video, 640x360, 24fps
clip = ColorClip(size=(640, 360), color=(255, 0, 0), duration=3)
clip.write_videofile("input.mp4", fps=24)
