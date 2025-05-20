from crewai import Agent
from tools.file_reader_tools import FileReadTool

class BAAgents():
  def __init__(self, serper_api_key):
    self.tool = FileReadTool.read_pdf
    print('tool ::', self.tool)

  def solution_agent(self, llm):
    return Agent(
        role="Business Analyst",
        goal="Extract and summarize business requirements from uploaded documents",
        backstory="An experienced business analyst skilled in translating documents into technical requirements for solution architects.",
        tools=[self.tool],
        verbose=True,
        llm=llm
    )