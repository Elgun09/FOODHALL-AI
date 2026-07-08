from openai_client import ask_gpt

class Brain:

    def think(self, task: str):
        return ask_gpt(task)

brain = Brain()
