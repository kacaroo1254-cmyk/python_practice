# -*- coding: utf-8 -*-
"""Create timestamped annotated video results (D31·D32 공용)."""
from datetime import datetime
from pathlib import Path
import cv2


def make_video_path(script_name):
    folder = Path(__file__).resolve().parent
    results = folder / "results"
    results.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return results / f"{script_name}_{stamp}.mp4"


def get_video_fps(video_path):
    capture = cv2.VideoCapture(str(video_path))
    fps = capture.get(cv2.CAP_PROP_FPS)
    capture.release()
    return fps if fps > 0 else 24.0


def save_video_frame(writer, output_path, frame, fps, zone=None):
    if zone is not None:
        x1, y1, x2, y2 = zone
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 3)
    if writer is None:
        height, width = frame.shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
        if not writer.isOpened():
            raise RuntimeError("결과 동영상을 만들 수 없습니다: " + str(output_path))
    writer.write(frame)
    return writer
