import math
import turtle


class LSystemRenderer:
    def __init__(self, angle: float, step: float) -> None:
        self.angle = angle
        self.step = step
        self.screen_width = 1000
        self.screen_height = 800
        self.padding = 40

    def calculate_bounds(
        self,
        instructions: str,
        start_heading: float = 90,
        step: float | None = None
    ) -> tuple[float, float, float, float]:
        if step is None:
            step = self.step

        x = 0.0
        y = 0.0
        heading = start_heading

        stack = []
        points = [(x, y)]

        for symbol in instructions:
            if symbol in ("F", "G"):
                radians = math.radians(heading)
                x += step * math.cos(radians)
                y += step * math.sin(radians)
                points.append((x, y))

            elif symbol == "+":
                heading -= self.angle

            elif symbol == "-":
                heading += self.angle

            elif symbol == "[":
                stack.append((x, y, heading))

            elif symbol == "]":
                if stack:
                    x, y, heading = stack.pop()
                    points.append((x, y))

        x_values = [point[0] for point in points]
        y_values = [point[1] for point in points]

        return min(x_values), max(x_values), min(y_values), max(y_values)

    def calculate_scaled_step(self, instructions: str, start_heading: float = 90) -> float:
        min_x, max_x, min_y, max_y = self.calculate_bounds(instructions, start_heading, self.step)

        drawing_width = max_x - min_x
        drawing_height = max_y - min_y

        available_width = self.screen_width - 2 * self.padding
        available_height = self.screen_height - 2 * self.padding

        if drawing_width == 0:
            width_scale = 1.0
        else:
            width_scale = available_width / drawing_width

        if drawing_height == 0:
            height_scale = 1.0
        else:
            height_scale = available_height / drawing_height

        scale_factor = min(width_scale, height_scale, 1.0)

        return self.step * scale_factor

    def draw(self, instructions: str, start_heading: float = 90, animate: bool = True) -> None:
        screen = turtle.Screen()
        screen.setup(width=self.screen_width, height=self.screen_height)
        screen.title("L-System Fractal Visualizer")
        screen.bgcolor("white")

        actual_step = self.calculate_scaled_step(instructions, start_heading)

        min_x, max_x, min_y, max_y = self.calculate_bounds(
            instructions,
            start_heading,
            actual_step
        )

        drawing_width = max_x - min_x
        drawing_height = max_y - min_y

        offset_x = -(min_x + drawing_width / 2)
        offset_y = -(min_y + drawing_height / 2)

        t = turtle.Turtle()
        t.pensize(1)
        t.color("black")

        if animate:
            screen.tracer(1, 5)
            t.showturtle()
            t.speed(3)
        else:
            screen.tracer(0, 0)
            t.hideturtle()
            t.speed(0)

        x = offset_x
        y = offset_y
        heading = start_heading

        t.penup()
        t.goto(x, y)
        t.setheading(heading)
        t.pendown()

        stack = []

        for symbol in instructions:
            if symbol in ("F", "G"):
                radians = math.radians(heading)
                x += actual_step * math.cos(radians)
                y += actual_step * math.sin(radians)
                t.goto(x, y)

            elif symbol == "+":
                heading -= self.angle
                t.setheading(heading)

            elif symbol == "-":
                heading += self.angle
                t.setheading(heading)

            elif symbol == "[":
                stack.append((x, y, heading))

            elif symbol == "]":
                if stack:
                    x, y, heading = stack.pop()
                    t.penup()
                    t.goto(x, y)
                    t.setheading(heading)
                    t.pendown()

        if not animate:
            screen.update()

        turtle.done()