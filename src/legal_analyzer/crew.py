from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from .tools.rag_tool import rag_tool
from .tools.mcp_tool import mcp_tool
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class LegalAnalyzer():
    """Legal analyzer who  analyzes contracts and writes reports based on user queries"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def contract_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['contract_analyst'], 
            verbose=True,
            tools=[rag_tool, mcp_tool]
        )


    @agent
    def report_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['report_writer'], 
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['analysis_task'], # type: ignore[index]
            output_file='analysis.json',
             
        )

    @task
    def report_task(self) -> Task:
        return Task(
            config=self.tasks_config['report_task'], 
            output_file='report.md',
             
        )

    @crew
    def crew(self) -> Crew:
        """Creates the LegalAnalyzer crew"""
        

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
