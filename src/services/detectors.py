import cv2
import numpy as np
from src.config import AppConfig
from src.domain.enums import LightColor
from src.domain.models import BoundingBox, TrafficLightData, LineData

class HSVDetector:
    def __init__(self, config: AppConfig):
        self.config = config
        self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

    def _process_mask(self, mask: np.ndarray) -> np.ndarray:
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self.kernel)
        return mask

    def _find_largest_contour(self, mask: np.ndarray, min_area: int) -> tuple[bool, BoundingBox | None]:
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return False, None

        largest_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest_contour) < min_area:
            return False, None

        x, y, w, h = cv2.boundingRect(largest_contour)
        return True, BoundingBox(x, y, w, h)


class TrafficLightDetector(HSVDetector):
    def detect(self, top_roi: np.ndarray) -> TrafficLightData:
        hsv = cv2.cvtColor(top_roi, cv2.COLOR_BGR2HSV)
        
        mask_red_1 = cv2.inRange(hsv, self.config.RED_HSV_LOWER_1, self.config.RED_HSV_UPPER_1)
        mask_red_2 = cv2.inRange(hsv, self.config.RED_HSV_LOWER_2, self.config.RED_HSV_UPPER_2)
        mask_red = cv2.bitwise_or(mask_red_1, mask_red_2)
        mask_red = self._process_mask(mask_red)
        
        mask_green = cv2.inRange(hsv, self.config.GREEN_HSV_LOWER, self.config.GREEN_HSV_UPPER)
        mask_green = self._process_mask(mask_green)
        
        found_red, bbox_red = self._find_largest_contour(mask_red, self.config.MIN_AREA_LIGHT)
        found_green, bbox_green = self._find_largest_contour(mask_green, self.config.MIN_AREA_LIGHT)
        
        if found_red:
            return TrafficLightData(LightColor.RED, bbox_red)
        if found_green:
            return TrafficLightData(LightColor.GREEN, bbox_green)
            
        return TrafficLightData(LightColor.NONE, None)


class StopLineDetector(HSVDetector):
    def detect(self, bottom_roi: np.ndarray, offset_y: int) -> LineData:
        hsv = cv2.cvtColor(bottom_roi, cv2.COLOR_BGR2HSV)
        mask_yellow = cv2.inRange(hsv, self.config.YELLOW_HSV_LOWER, self.config.YELLOW_HSV_UPPER)
        mask_yellow = self._process_mask(mask_yellow)
        
        found, bbox = self._find_largest_contour(mask_yellow, self.config.MIN_AREA_LINE)
        
        if not found or not bbox:
            return LineData(False, 0, None)
            
        global_bbox = BoundingBox(bbox.x, bbox.y + offset_y, bbox.w, bbox.h)
        lowest_y = global_bbox.y + global_bbox.h
        
        return LineData(True, lowest_y, global_bbox)