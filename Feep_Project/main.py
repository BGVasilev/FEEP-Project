import random
import os
from datetime import datetime

from examples import koch_curve, sierpinski_triangle, fractal_plant
from lsystem import LSystem
from renderer import LSystemRenderer


def save_result(name: str, instructions: str, iterations: int, angle: float, step: float):
    folder = "Results"

    os.makedirs(folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name.replace(' ', '_')}_{timestamp}.txt"
    path = os.path.join(folder, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write("L-System Result\n")
        f.write("====================\n\n")
        f.write(f"Example: {name}\n")
        f.write(f"Iterations: {iterations}\n")
        f.write(f"Angle: {angle}\n")
        f.write(f"Step: {step}\n")
        f.write(f"Instruction length: {len(instructions)}\n\n")
        f.write("Instructions:\n")
        f.write(instructions)

    print(f"\nРезултатът е записан в: {path}")


def get_positive_int(prompt: str, default: int, min_value: int = 0, max_value: int = 10) -> int:
    value = input(f"{prompt} (по подразбиране {default}): ").strip()

    if value == "":
        return default

    try:
        number = int(value)
        if min_value <= number <= max_value:
            return number
    except ValueError:
        pass

    print(f"Невалидна стойност. Използва се {default}.")
    return default


def get_positive_float(prompt: str, default: float, min_value: float = 0.1, max_value: float = 360.0) -> float:
    value = input(f"{prompt} (по подразбиране {default}): ").strip()

    if value == "":
        return default

    try:
        number = float(value)
        if min_value <= number <= max_value:
            return number
    except ValueError:
        pass

    print(f"Невалидна стойност. Използва се {default}.")
    return default


def choose_example():
    print("\nИзбери готов пример:")
    print("1 - Koch Curve")
    print("2 - Sierpinski Triangle")
    print("3 - Fractal Plant")

    choice = input("Въведи номер: ").strip()

    if choice == "1":
        return koch_curve(), "Koch Curve", 0
    elif choice == "2":
        return sierpinski_triangle(), "Sierpinski Triangle", 0
    elif choice == "3":
        return fractal_plant(), "Fractal Plant", 90
    else:
        print("Невалиден избор.")
        return None


def create_custom_lsystem():
    print("\nСъздаване на потребителска L-система")

    axiom = input("Въведи аксиома: ").strip()
    if not axiom:
        axiom = "F"

    rules = {}
    rule_count = get_positive_int("Брой правила", 1, 1, 10)

    for i in range(rule_count):
        print(f"\nПравило {i + 1}")
        left = input("Символ отляво: ").strip()
        right = input("Замяна отдясно: ").strip()

        if len(left) != 1:
            print("Лявата страна трябва да е точно 1 символ. Правилото се пропуска.")
            continue

        rules[left] = right

    angle = get_positive_float("Ъгъл", 60.0, 1.0, 360.0)
    step = get_positive_float("Дължина на стъпка", 5.0, 1.0, 50.0)
    iterations = get_positive_int("Брой итерации", 4, 0, 8)

    system = LSystem(axiom, rules)
    return (system, angle, iterations, step), "Custom L-System", 90


def random_example():
    examples = [
        {
            "name": "Koch Curve",
            "data": koch_curve(),
            "start_heading": 0,
            "iterations_range": (2, 5),
            "step_range": (3, 8),
            "angle_options": [60.0]
        },
        {
            "name": "Sierpinski Triangle",
            "data": sierpinski_triangle(),
            "start_heading": 0,
            "iterations_range": (3, 6),
            "step_range": (3, 7),
            "angle_options": [120.0]
        },
        {
            "name": "Fractal Plant",
            "data": fractal_plant(),
            "start_heading": 90,
            "iterations_range": (3, 5),
            "step_range": (3, 6),
            "angle_options": [20.0, 22.5, 25.0, 30.0]
        }
    ]

    chosen = random.choice(examples)
    system, _, _, _ = chosen["data"]

    iterations = random.randint(*chosen["iterations_range"])
    step = round(random.uniform(*chosen["step_range"]), 1)
    angle = random.choice(chosen["angle_options"])

    return (
        (system, angle, iterations, step),
        chosen["name"] + " (Random Mode)",
        chosen["start_heading"]
    )


def main():
    print("Избери режим:")
    print("1 - Готов пример")
    print("2 - Готов пример с ръчни итерации")
    print("3 - Потребителска L-система")
    print("4 - Случаен пример")

    mode = input("Въведи номер: ").strip()

    if mode == "1":
        selected = choose_example()
        if selected is None:
            return

    elif mode == "2":
        selected = choose_example()
        if selected is None:
            return

        (system, angle, iterations, step), name, start_heading = selected
        iterations = get_positive_int("Въведи брой итерации", iterations, 0, 10)
        angle = get_positive_float("Въведи ъгъл", angle, 1.0, 360.0)
        step = get_positive_float("Въведи дължина на стъпка", step, 1.0, 50.0)

        selected = (system, angle, iterations, step), name, start_heading

    elif mode == "3":
        selected = create_custom_lsystem()

    elif mode == "4":
        selected = random_example()

    else:
        print("Невалиден режим.")
        return

    (system, angle, iterations, step), name, start_heading = selected

    instructions = system.generate(iterations)

    print(f"\nИзбран пример: {name}")
    print(f"Брой итерации: {iterations}")
    print(f"Ъгъл: {angle}")
    print(f"Стъпка: {step}")
    print(f"Дължина на генерирания низ: {len(instructions)}")

    if len(instructions) > 200000:
        print("Генерираният низ е прекалено голям за рисуване.")
        return

    print("\nИзбери режим на чертане:")
    print("1 - Бавно")
    print("2 - Бързо")

    draw_mode = input("Въведи номер: ").strip()

    if draw_mode == "1":
        animate = True
    elif draw_mode == "2":
        animate = False
    else:
        print("Невалиден избор. Използва се бавно чертане.")
        animate = True

    renderer = LSystemRenderer(angle, step)
    renderer.draw(instructions, start_heading=start_heading, animate=animate)

    save_result(name, instructions, iterations, angle, step)
    print("Програмата приключи.")


if __name__ == "__main__":
    main()