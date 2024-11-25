from manim import *

class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        self.play(Create(square))
        self.play(Transform(square, circle))
        self.wait()

if __name__ == "__main__":
    scene = SquareToCircle()
    scene.render() 