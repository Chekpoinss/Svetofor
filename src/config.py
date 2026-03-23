from dataclasses import dataclass, field
import numpy as np

@dataclass(frozen=True)
class AppConfig:
    RED_HSV_LOWER_1: np.ndarray = field(default_factory=lambda: np.array([0, 120, 70]))
    RED_HSV_UPPER_1: np.ndarray = field(default_factory=lambda: np.array([10, 255, 255]))
    RED_HSV_LOWER_2: np.ndarray = field(default_factory=lambda: np.array([160, 120, 70]))
    RED_HSV_UPPER_2: np.ndarray = field(default_factory=lambda: np.array([179, 255, 255]))
    
    GREEN_HSV_LOWER: np.ndarray = field(default_factory=lambda: np.array([40, 100, 70]))
    GREEN_HSV_UPPER: np.ndarray = field(default_factory=lambda: np.array([90, 255, 255]))
    
    YELLOW_HSV_LOWER: np.ndarray = field(default_factory=lambda: np.array([20, 100, 100]))
    YELLOW_HSV_UPPER: np.ndarray = field(default_factory=lambda: np.array([35, 255, 255]))
    
    MIN_AREA_LIGHT: int = 150
    MIN_AREA_LINE: int = 500
    
    PROXIMITY_THRESHOLD_RATIO: float = 0.66 
    SMOOTHING_WINDOW_SIZE: int = 5