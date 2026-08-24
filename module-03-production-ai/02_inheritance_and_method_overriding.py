# Implementing Abstract Base Class

from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name):
        self.name = name

    def log(self, message):
        pass

    @abstractmethod
    def execute(self, task):
        pass


class SummaryAgent(BaseAgent):
    def execute(self, task):
        return f"Summary of: {task}"


class TranslationAgent(BaseAgent):
    def __init__(self, name, target_language):
        super().__init__(name)
        self.target_language = target_language

    def execute(self, task):
        return f"Translated '{task}' to {self.target_language}"


def run_all(task, *agents):
    for agent in agents:
        print(agent.execute(task))


summary = SummaryAgent(name= "Summarization")
translation = TranslationAgent("Translation", "Sanskrit")
agent = (summary, translation)
run_all("Summarize the news article", *agent)
