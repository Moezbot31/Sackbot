import cv2
import numpy as np
import os

class VideoEngine:
    def __init__(self):
        pass

    def export_video(self, input_path, output_path, resolution='1080p', fmt='mp4', bitrate='auto', progress_callback=None, live_preview=False, effect=None, brightness=1.0):
        try:
            # Resolution handling
            res_map = {'4k': (3840, 2160), '2160p': (3840, 2160), '1440p': (2560, 1440), '1080p': (1920, 1080), '720p': (1280, 720), '480p': (854, 480)}
            if resolution.lower() in res_map:
                w, h = res_map[resolution.lower()]
            else:
                w, h = (1920, 1080)
            # Format handling
            ext = fmt.lower()
            if not output_path.lower().endswith(f'.{ext}'):
                output_path += f'.{ext}'
            # Open input video
            cap = cv2.VideoCapture(input_path)
            if not cap.isOpened():
                print(f"[VideoEngine] Failed to open input video: {input_path}")
                return False
            fourcc = cv2.VideoWriter_fourcc(*('XVID' if ext == 'avi' else 'mp4v'))
            fps = cap.get(cv2.CAP_PROP_FPS) or 24
            out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            frame_idx = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frame_resized = cv2.resize(frame, (w, h))
                # --- Video Effects ---
                if effect == 'grayscale':
                    frame_resized = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
                    frame_resized = cv2.cvtColor(frame_resized, cv2.COLOR_GRAY2BGR)
                elif effect == 'invert':
                    frame_resized = cv2.bitwise_not(frame_resized)
                if brightness != 1.0:
                    frame_resized = cv2.convertScaleAbs(frame_resized, alpha=brightness, beta=0)
                # --- End Effects ---
                out.write(frame_resized)
                frame_idx += 1
                # Terminal progress bar for user POV
                percent = (frame_idx / total_frames) * 100 if total_frames else 0
                bar = ('#' * int(percent // 2)).ljust(50)
                print(f"\rExporting: [{bar}] {percent:.1f}% ({frame_idx}/{total_frames})", end='')
                if percent == 100 or frame_idx == total_frames:
                    print("\nExport complete! Output saved to:", output_path)
                if progress_callback:
                    progress_callback(frame_idx, total_frames)
            print()  # Newline after progress bar
            cap.release()
            out.release()
            if live_preview:
                cv2.destroyAllWindows()
            return True
        except Exception as e:
            print(f"[VideoEngine] Export failed: {e}")
            if live_preview:
                cv2.destroyAllWindows()
            return False

    def batch_export(self, jobs, progress_callback=None):
        results = []
        for job in jobs:
            result = self.export_video(progress_callback=progress_callback, **job)
            results.append(result)
        return results

    def batch_export_from_json(self, json_path):
        import json
        with open(json_path, 'r') as f:
            jobs = json.load(f)
        results = []
        for job in jobs:
            print(f"\nBatch exporting: {job.get('input_path')} -> {job.get('output_path')}")
            result = self.export_video(**job)
            results.append(result)
        return results

    def save_export_preset(self, preset_path, settings):
        import json
        with open(preset_path, 'w') as f:
            json.dump(settings, f, indent=2)
        print(f"Export preset saved to {preset_path}")

    def load_export_preset(self, preset_path):
        import json
        with open(preset_path, 'r') as f:
            settings = json.load(f)
        print(f"Loaded export preset from {preset_path}")
        return settings

if __name__ == "__main__":
    video = VideoEngine()
    # Example: Export with effect and brightness
    video.export_video('input.mp4', 'output_gray', effect='grayscale')
    video.export_video('input.mp4', 'output_invert', effect='invert')
    video.export_video('input.mp4', 'output_bright', brightness=1.5)
    # Example: Batch export from JSON
    # video.batch_export_from_json('batch_jobs.json')
    # Example: Save/load export preset
    preset = {'resolution': '720p', 'fmt': 'avi', 'effect': 'grayscale'}
    video.save_export_preset('export_preset.json', preset)
    loaded = video.load_export_preset('export_preset.json')
    print('Loaded preset:', loaded)
