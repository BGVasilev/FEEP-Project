from lsystem import LSystem


def koch_curve():
    axiom = "F"

    rules = {
        "F": "F+F--F+F"
    }

    angle = 60
    iterations = 4
    step = 5

    system = LSystem(axiom, rules)

    return system, angle, iterations, step


def sierpinski_triangle():
    axiom = "F-G-G"

    rules = {
        "F": "F-G+F+G-F",
        "G": "GG"
    }

    angle = 120
    iterations = 5
    step = 5

    system = LSystem(axiom, rules)

    return system, angle, iterations, step


def fractal_plant():
    axiom = "X"

    rules = {
        "X": "F+[[X]-X]-F[-FX]+X",
        "F": "FF"
    }

    angle = 25
    iterations = 5
    step = 5

    system = LSystem(axiom, rules)

    return system, angle, iterations, step