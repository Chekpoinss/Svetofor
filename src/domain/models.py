from dataclasses import dataclass

@dataclass(frozen=True)
class BoundingBox:
    x: int
    y: int
    w: int
    h: int

@dataclass(frozen=True)
class TrafficLightData:
    color: 'LightColor'
    bbox: BoundingBox | None

@dataclass(frozen=True)
class LineData:
    detected: bool
    lowest_y: int
    bbox: BoundingBox | None

@dataclass(frozen=True)
class FrameResult:
    frame: object
    light_data: TrafficLightData
    line_data: LineData
    smoothed_color: 'LightColor'
    action: 'ActionSignal'
    is_near_line: bool