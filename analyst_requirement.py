from crewai import Crew, Process
from crewai.task import TaskOutput
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic


from textwrap import dedent
from agents.ba_agents import BAAgents
from tasks.ba_tasks import BATasks
from dotenv import load_dotenv

import os

load_dotenv()

def task_callback(output: TaskOutput, aspect: str, task_responses: dict):
    if task_responses is not None:
        task_responses[aspect] = output.raw_output

def create_task_callback(aspect: str, task_responses: dict = None):
    def callback(output: TaskOutput):
        task_callback(output, aspect, task_responses)
    return callback

class AnalystBusinessCrew:
    def __init__(self,
                 file_path,
                 cloud_provider,
                 model_choice,
                 openai_api_key=None,
                 anthropic_api_key=None,
                 serper_api_key=None,
                 task_responses=None):
        self.file_path = file_path;
        self.task_responses = task_responses
        self.provider = cloud_provider
        self.model_choice = model_choice
        self.serper_api_key = serper_api_key
        self.openai_api_key = openai_api_key
        self.anthropic_api_key = anthropic_api_key

        if (cloud_provider == "AWS"):
            self.agents = BAAgents(self.serper_api_key)
            self.tasks = BATasks()

        self.OpenAI35GPT = ChatOpenAI(
            model_name=os.getenv("OPENAI_MODEL_NAME"),
            openai_api_key=self.openai_api_key,
            temperature=0.7)
        self.Anthropic = ChatAnthropic(
            temperature=0.7,
            anthropic_api_key=self.anthropic_api_key,
            model_name=os.getenv("ANTHROPIC_MODEL_NAME"))

        if (model_choice == "OpenAI"):
            self.selectedllm = self.OpenAI35GPT
        else:
            self.selectedllm = self.Anthropic

    def run(self):
        ba_agent = self.agents.solution_agent(llm=self.selectedllm)

        ba_task = self.tasks.summary_requirement_task(
            agent=ba_agent,
            file_path=self.file_path,
            callback=create_task_callback("solution", self.task_responses)
        )

        crew = Crew(
            agents=[
                ba_agent,
            ],
            tasks=[
                ba_task,
            ],
            verbose=1,
            process=Process.sequential
        )
        result = crew.kickoff()
        print(f"START-----usage metrics----")
        print(crew.usage_metrics)
        print(f"-----usage metrics----END")
        return result
