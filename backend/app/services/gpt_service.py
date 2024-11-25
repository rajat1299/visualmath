from openai import OpenAI
from app.core.config import settings
import logging
import re
import ast

logger = logging.getLogger(__name__)

class GPTService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def clean_code(self, code: str) -> str:
        """Clean and validate the generated Python code."""
        try:
            # Remove markdown and explanatory text
            code = re.sub(r'```python\s*', '', code)
            code = re.sub(r'```\s*', '', code)
            code = re.sub(r'^Here\'s.*?\n', '', code, flags=re.MULTILINE)
            code = code.strip()
            
            # Ensure proper imports
            if "from manim import *" not in code:
                code = "from manim import *\n\n" + code
            
            # Basic syntax validation
            ast.parse(code)  # This will raise SyntaxError if code is invalid
            
            # Validate Manim-specific requirements
            self._validate_manim_code(code)
            
            return code

        except SyntaxError as e:
            logger.error(f"Syntax error in generated code: {str(e)}")
            raise ValueError(f"Generated code has syntax errors: {str(e)}")
        except Exception as e:
            logger.error(f"Code validation error: {str(e)}")
            raise ValueError(f"Code validation failed: {str(e)}")

    def _validate_manim_code(self, code: str) -> None:
        """Validate Manim-specific code requirements."""
        # Check for Scene class
        if not re.search(r'class\s+\w+\s*\(\s*(?:Scene|ThreeDScene)\s*\)', code):
            raise ValueError("No Scene class found in generated code")
        
        # Check for construct method
        if 'def construct(self):' not in code:
            raise ValueError("No construct method found in Scene class")
        
        # Check for prohibited imports
        prohibited_imports = ['manimlib', 'manim.mobject', 'os', 'sys', 'subprocess']
        for imp in prohibited_imports:
            if f'import {imp}' in code or f'from {imp}' in code:
                raise ValueError(f"Prohibited import found: {imp}")
        
        # Check for minimum required content
        if not re.search(r'self\.play\(', code):
            raise ValueError("No animation commands found in code")
        
        # Check for proper scene structure
        if not re.search(r'self\.wait\(\)', code):
            logger.warning("No wait() call found in animation")

    async def generate_manim_code(self, description: str, max_retries: int = 3) -> str:
        """Generate Manim code with retry logic."""
        last_error = None
        
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": """You are an expert Manim developer specializing in Manim Community version 0.17.3. Generate ONLY valid Python code for Manim Community v0.17.3.
DO NOT include any explanations or text - ONLY the Python code.

**Your Task:**
Generate ONLY valid Python code compatible with Manim Community v0.17.3, based on the user's description.

**Instructions:**

1. **Code Structure:**
   - **Import Statement:**
     - Begin with: `from manim import *`
     - Do NOT use any other import statements.
   - **Scene Class:**
     - Create a descriptive class that inherits from `Scene` or `ThreeDScene` as appropriate.
   - **Construct Method:**
     - Implement the `construct(self)` method containing the animation code.

2. **Syntax and Features:**
   - Use ONLY documented features from Manim Community v0.17.3.
   - Avoid deprecated, experimental, or future-version features.
   - Ensure all class names, method names, and parameter names are correct for v0.17.3.
   - Do NOT use parameters or methods that do not exist in this version.

3. **Restrictions:**
   - Do NOT use any additional imports, especially from `manimlib`, `manim.mobject`, or other submodules.
   - Do NOT include any comments, explanations, markdown formatting, or code fences.
   - Do NOT use code that requires internet access or external resources.

**Example (2D Animation):**
from manim import *

class BezierCurveExample(Scene):
    def construct(self):
        curve = CubicBezier(
            LEFT, UP, RIGHT, DOWN,
            color=BLUE
        )
        self.play(Create(curve))
        self.wait()

**Example (3D Animation):**
from manim import *

class MobiusStripExample(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        mobius = Surface(
            lambda u, v: np.array([
                (1 + 0.5 * v * np.cos(u / 2)) * np.cos(u),
                (1 + 0.5 * v * np.cos(u / 2)) * np.sin(u),
                0.5 * v * np.sin(u / 2)
            ]),
            u_range=[0, TAU],
            v_range=[-1, 1],
            resolution=(32, 16),
            fill_opacity=0.5,
            checkerboard_colors=[BLUE_D, BLUE_E]
        )
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.play(Create(axes), Create(mobius))
        self.wait()

Return ONLY the Python code without any additional text or formatting."""
                        },
                        {
                            "role": "user", 
                            "content": f"Generate Manim code for: {description}"
                        }
                    ],
                    temperature=0.2,
                )
                
                code = response.choices[0].message.content
                cleaned_code = self.clean_code(code)
                
                logger.info(f"Generated code (attempt {attempt + 1}):\n{cleaned_code}")
                return cleaned_code

            except ValueError as e:
                last_error = e
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                continue
            except Exception as e:
                logger.error(f"GPT service error: {str(e)}")
                raise

        raise ValueError(f"Failed to generate valid code after {max_retries} attempts. Last error: {str(last_error)}")

# Create singleton instance
gpt_service = GPTService()