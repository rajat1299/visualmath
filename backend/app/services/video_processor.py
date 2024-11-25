import os
import subprocess
import logging
from app.core.config import settings
import tempfile

logger = logging.getLogger(__name__)

class VideoProcessor:
    def __init__(self):
        self.ffmpeg_path = "ffmpeg"  # Assuming ffmpeg is in PATH
        self.default_quality = "medium"  # low, medium, high
        self.quality_presets = {
            "low": {
                "resolution": "480p",
                "bitrate": "500k",
                "fps": "24",
            },
            "medium": {
                "resolution": "720p",
                "bitrate": "1500k",
                "fps": "30",
            },
            "high": {
                "resolution": "1080p",
                "bitrate": "3000k",
                "fps": "60",
            }
        }

    async def optimize_video(self, input_path: str, quality: str = None) -> str:
        """Optimize video for web delivery."""
        try:
            quality_settings = self.quality_presets[quality or self.default_quality]
            
            # Create temp file for output
            with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp_file:
                output_path = tmp_file.name

            # Prepare ffmpeg command
            cmd = [
                self.ffmpeg_path,
                "-i", input_path,
                "-c:v", "libx264",  # Video codec
                "-preset", "medium",  # Encoding speed preset
                "-crf", "23",  # Quality (lower = better, 18-28 is good)
                "-c:a", "aac",  # Audio codec
                "-b:a", "128k",  # Audio bitrate
                "-movflags", "+faststart",  # Enable fast start for web playback
                "-y",  # Overwrite output file
                output_path
            ]

            # Add quality-specific settings
            if "resolution" in quality_settings:
                height = quality_settings["resolution"].replace("p", "")
                cmd.extend(["-vf", f"scale=-2:{height}"])
            
            if "fps" in quality_settings:
                cmd.extend(["-r", quality_settings["fps"]])
            
            if "bitrate" in quality_settings:
                cmd.extend(["-b:v", quality_settings["bitrate"]])

            # Run ffmpeg
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                logger.error(f"FFmpeg error: {stderr.decode()}")
                raise Exception("Video optimization failed")

            logger.info(f"Video optimized: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Video optimization error: {str(e)}")
            raise

    async def get_video_info(self, video_path: str) -> dict:
        """Get video metadata."""
        try:
            cmd = [
                self.ffmpeg_path,
                "-i", video_path
            ]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()

            # Parse ffmpeg output
            info = {}
            for line in stderr.decode().split('\n'):
                if 'Duration' in line:
                    info['duration'] = line.split('Duration: ')[1].split(',')[0]
                elif 'Stream' in line and 'Video' in line:
                    parts = line.split(', ')
                    for part in parts:
                        if 'x' in part and any(c.isdigit() for c in part):
                            info['resolution'] = part.strip()
                        elif 'fps' in part.lower():
                            info['fps'] = part.strip()
                        elif 'kb/s' in part:
                            info['bitrate'] = part.strip()

            return info

        except Exception as e:
            logger.error(f"Failed to get video info: {str(e)}")
            return {}

video_processor = VideoProcessor() 