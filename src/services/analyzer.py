from collections import deque
from src.config import AppConfig
from src.domain.enums import LightColor, ActionSignal

class StateAnalyzer:
    def __init__(self, config: AppConfig):
        self.config = config
        self.color_history: deque[LightColor] = deque(maxlen=config.SMOOTHING_WINDOW_SIZE)

    def get_smoothed_color(self, current_color: LightColor) -> LightColor:
        self.color_history.append(current_color)
        
        counts = {
            LightColor.RED: 0,
            LightColor.GREEN: 0,
            LightColor.NONE: 0
        }
        for color in self.color_history:
            counts[color] += 1
            
        return max(counts, key=counts.get)

    def determine_action(self, smoothed_color: LightColor, is_near_line: bool) -> ActionSignal:
        if not is_near_line:
            return ActionSignal.NONE
            
        if smoothed_color == LightColor.RED:
            return ActionSignal.STOP
        if smoothed_color == LightColor.GREEN:
            return ActionSignal.GO
            
        return ActionSignal.NONE

    def check_proximity(self, line_lowest_y: int, frame_height: int) -> bool:
        threshold_y = int(frame_height * self.config.PROXIMITY_THRESHOLD_RATIO)
        return line_lowest_y > threshold_y