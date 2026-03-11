class LSystem:
    def __init__(self, axiom: str, rules: dict[str, str]) -> None:
        self.axiom = axiom
        self.rules = rules

    #Прилага правилата върху един низ
    def apply_rules(self, text: str) -> str:
        result = []

        for symbol in text:
            result.append(self.rules.get(symbol, symbol))

        return "".join(result)

    #Прилага правилата няколоко пъти
    def generate(self, iterations: int) -> str:
        current = self.axiom

        for _ in range(iterations):
            current = self.apply_rules(current)

        return current