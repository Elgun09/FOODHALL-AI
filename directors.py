from brain import brain

class Director:

    def __init__(self, name, role):
        self.name = name
        self.role = role

    def answer(self, question):
        prompt = f"""
Ты {self.name}.
Твоя должность: {self.role}.

Ответь на вопрос как специалист.

Вопрос:
{question}
"""
        return brain.think(prompt)

DIRECTORS = [
    Director("Александр", "Генеральный директор"),
    Director("Дмитрий", "Коммерческий директор"),
    Director("Максим", "Финансовый директор"),
    Director("Анна", "Директор по маркетингу"),
    Director("Илья", "Директор по автоматизации"),
    Director("Елена", "Представитель гостя"),
]
