import tempfile
import os
import asyncio
import logging
import shutil
from app.core.config import settings

logger = logging.getLogger(__name__)

class ManimExecutor:
    async def execute_manim_code(self, manim_code: str) -> str:
        """Execute Manim code and return path to generated video."""
        try:
            # Create temporary directory for Manim files
            with tempfile.TemporaryDirectory() as temp_dir:
                # Write Manim code to file
                script_path = os.path.join(temp_dir, "scene.py")
                with open(script_path, "w") as f:
                    f.write(manim_code)
                
                logger.info(f"Generated Manim code:\n{manim_code}")
                logger.info(f"Script path: {script_path}")
                
                # Get the Scene class name from the code
                scene_class = self._extract_scene_class_name(manim_code)
                
                # Execute Manim in Docker container
                cmd = [
                    "docker", "run", "--rm",
                    "-v", f"{os.path.abspath(temp_dir)}:/workspace",
                    "manim-env:latest",
                    "manim", "render", "scene.py", scene_class,
                    "-qm"
                ]
                
                logger.info(f"Running command: {' '.join(cmd)}")
                
                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=temp_dir
                )
                
                # Add timeout to process
                try:
                    stdout, stderr = await asyncio.wait_for(
                        process.communicate(),
                        timeout=60  # 60 seconds timeout
                    )
                except asyncio.TimeoutError:
                    process.kill()
                    raise Exception("Animation generation timed out after 60 seconds")
                
                logger.info(f"Manim stdout:\n{stdout.decode()}")
                logger.info(f"Manim stderr:\n{stderr.decode()}")
                
                if process.returncode != 0:
                    raise Exception(f"Manim execution failed: {stderr.decode()}")
                
                # Find generated video file
                media_dir = os.path.join(temp_dir, "media", "videos", "scene", "720p30")
                logger.info(f"Looking for video in: {media_dir}")
                
                if not os.path.exists(media_dir):
                    raise Exception(f"Media directory not found: {media_dir}")
                
                files = os.listdir(media_dir)
                logger.info(f"Files in media directory: {files}")
                
                # Look for any .mp4 file
                video_files = [f for f in files if f.endswith('.mp4')]
                if not video_files:
                    raise Exception("No video files found in output directory")
                
                source_video = os.path.join(media_dir, video_files[0])
                
                # Copy to storage directory
                storage_dir = os.path.join(settings.STORAGE_PATH, "temp")
                os.makedirs(storage_dir, exist_ok=True)
                target_video = os.path.join(storage_dir, f"{scene_class}.mp4")
                
                shutil.copy2(source_video, target_video)
                logger.info(f"Copied video to: {target_video}")
                
                return target_video

        except Exception as e:
            logger.error(f"Manim execution failed: {str(e)}")
            raise

    def _extract_scene_class_name(self, code: str) -> str:
        """Extract the Scene class name from the code."""
        try:
            # Simple extraction - find the first class that inherits from Scene
            lines = code.split('\n')
            for line in lines:
                if 'class' in line and '(Scene)' in line:
                    return line.split('class')[1].split('(')[0].strip()
            return "Scene"  # Default if not found
        except Exception as e:
            logger.error(f"Failed to extract scene class name: {str(e)}")
            return "Scene"