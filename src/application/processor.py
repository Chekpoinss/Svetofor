import cv2
import numpy as np
from src.config import AppConfig
from src.domain.enums import LightColor, ActionSignal
from src.domain.models import FrameResult
from src.services.detectors import TrafficLightDetector, StopLineDetector
from src.services.analyzer import StateAnalyzer

class VideoProcessor:
    def __init__(self, config: AppConfig):
        self.config = config
        self.light_detector = TrafficLightDetector(config)
        self.line_detector = StopLineDetector(config)
        self.analyzer = StateAnalyzer(config)

    def _draw_annotations(self, frame: np.ndarray, result: FrameResult) -> None:
        height, width = frame.shape[:2]
        threshold_y = int(height * self.config.PROXIMITY_THRESHOLD_RATIO)
        
        cv2.line(frame, (0, threshold_y), (width, threshold_y), (255, 0, 0), 2)
        
        if result.light_data.bbox:
            b = result.light_data.bbox
            color = (0, 0, 255) if result.light_data.color == LightColor.RED else (0, 255, 0)
            cv2.rectangle(frame, (b.x, b.y), (b.x + b.w, b.y + b.h), color, 2)
            cv2.putText(frame, result.light_data.color.name, (b.x, b.y - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        if result.line_data.bbox:
            b = result.line_data.bbox
            cv2.rectangle(frame, (b.x, b.y), (b.x + b.w, b.y + b.h), (0, 255, 255), 2)

        if result.action != ActionSignal.NONE:
            text = "STOP" if result.action == ActionSignal.STOP else "GO!"
            text_color = (0, 0, 255) if result.action == ActionSignal.STOP else (0, 255, 0)
            cv2.putText(frame, text, (width // 2 - 100, height // 2), 
                        cv2.FONT_HERSHEY_SIMPLEX, 3.0, text_color, 5)

    def process_frame(self, frame: np.ndarray) -> FrameResult:
        height, width = frame.shape[:2]
        mid_y = height // 2
        
        top_roi = frame[0:mid_y, 0:width]
        bottom_roi = frame[mid_y:height, 0:width]
        
        light_data = self.light_detector.detect(top_roi)
        line_data = self.line_detector.detect(bottom_roi, offset_y=mid_y)
        
        smoothed_color = self.analyzer.get_smoothed_color(light_data.color)
        is_near = False
        if line_data.detected:
            is_near = self.analyzer.check_proximity(line_data.lowest_y, height)
            
        action = self.analyzer.determine_action(smoothed_color, is_near)
        
        result = FrameResult(
            frame=frame,
            light_data=light_data,
            line_data=line_data,
            smoothed_color=smoothed_color,
            action=action,
            is_near_line=is_near
        )
        
        self._draw_annotations(frame, result)
        return result

    def process_video(self, input_path: str, output_path: str) -> None:
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            raise IOError(f"Cannot open video {input_path}")

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            result_frame = self.process_frame(frame).frame
            out.write(result_frame)

        cap.release()
        out.release()