import argparse
import sys
from pathlib import Path
from src.config import AppConfig
from src.application.processor import VideoProcessor

def main() -> None:
    parser = argparse.ArgumentParser(description="Traffic Control Hackathon MVP")
    parser.add_argument("-i", "--input", required=True, help="Input .avi video file path")
    parser.add_argument("-o", "--output", default="output.mp4", help="Output .mp4 video file path")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file {input_path} does not exist.")
        sys.exit(1)

    config = AppConfig()
    processor = VideoProcessor(config)

    print(f"Processing {input_path} -> {args.output}")
    processor.process_video(str(input_path), args.output)
    print("Processing complete.")

if __name__ == "__main__":
    main()