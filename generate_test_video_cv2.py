import cv2
import numpy as np

# Create a 3-second blue video, 640x360, 24fps
width, height, fps, duration = 640, 360, 24, 3
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('input.mp4', fourcc, fps, (width, height))

frame = np.zeros((height, width, 3), dtype=np.uint8)
frame[:] = (255, 0, 0)  # Blue in BGR
for _ in range(fps * duration):
    out.write(frame)
out.release()
print('input.mp4 generated')
