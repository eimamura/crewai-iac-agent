"""CrewAI crew setup with agents and tasks."""

import os
from crewai import Agent, Crew, Process, Task

try:
    from langchain_openai import ChatOpenAI
except ImportError:
    ChatOpenAI = None

from .prompts import (
    AWS_ARCHITECT_ROLE,
    AWS_ARCHITECT_TASK,
    TERRAFORM_DESIGNER_ROLE,
    TERRAFORM_DESIGNER_TASK,
    REVIEWER_ROLE,
    REVIEWER_TASK,
    SYSTEM_PROMPT_TEMPLATE,
)


def create_crew(requirements: str, dry_run: bool = False) -> Crew:
    """
    Create and configure the CrewAI crew.
    
    Args:
        requirements: AWS requirements as string
        dry_run: If True, use a mock LLM (not implemented, will use actual LLM if key available)
    """
    # LLM configuration
    llm = None
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    
    if api_key and not dry_run:
        # Prefer OpenAI, fallback to Anthropic if available
        if os.getenv("OPENAI_API_KEY") and ChatOpenAI is not None:
            llm = ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0.1,
                api_key=api_key,
            )
        # Add Anthropic support if needed
        # elif os.getenv("ANTHROPIC_API_KEY"):
        #     from langchain_anthropic import ChatAnthropic
        #     llm = ChatAnthropic(model="claude-3-haiku-20240307", api_key=api_key)
    
    # If no LLM available, crew will need to handle gracefully
    # (dry_run mode should use templates instead)
    
    # Agents
    aws_architect = Agent(
        role="AWS Solutions Architect",
        goal="Analyze AWS requirements and propose minimal, cost-effective architecture",
        backstory="""You are an experienced AWS Solutions Architect who has designed 
        hundreds of production systems. You excel at balancing requirements with 
        cost and complexity, always preferring minimal viable solutions over 
        over-engineered architectures.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        system_message=AWS_ARCHITECT_ROLE,
    )
    
    terraform_designer = Agent(
        role="Terraform Infrastructure Designer",
        goal="Design minimal, maintainable Terraform repository structure and code",
        backstory="""You are a Terraform expert who has structured dozens of 
        infrastructure repositories. You understand the balance between 
        modularity and simplicity, always preferring clear, minimal code over 
        complex abstractions.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        system_message=TERRAFORM_DESIGNER_ROLE,
    )
    
    reviewer = Agent(
        role="Technical Reviewer",
        goal="Ensure proposal meets format requirements and quality standards",
        backstory="""You are a meticulous technical reviewer who catches 
        formatting errors, missing sections, and over-engineering. You ensure 
        all deliverables meet specifications exactly.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        system_message=REVIEWER_ROLE,
    )
    
    # Tasks
    analyze_task = Task(
        description=f"""Analyze the following AWS requirements and produce a summary, 
        assumptions, and minimal architecture proposal:

{requirements}

Remember to follow the output format requirements exactly.""",
        agent=aws_architect,
        expected_output="Summary, assumptions, and minimal AWS architecture proposal",
    )
    
    design_task = Task(
        description="""Based on the architecture proposal, design the Terraform 
        repository layout, modules, resources table, and skeleton code. Include 
        all required sections in the exact format specified.""",
        agent=terraform_designer,
        expected_output="Complete Terraform baseline proposal with all 15 required sections",
        context=[analyze_task],
    )
    
    review_task = Task(
        description="""Review the complete proposal and ensure:
        1. All 15 required headings are present in exact order
        2. All sections have meaningful content
        3. Format compliance is perfect
        4. Proposal is minimal and actionable
        
        Output the final proposal with all sections properly formatted.""",
        agent=reviewer,
        expected_output="Final proposal with all 15 sections in correct order and format",
        context=[analyze_task, design_task],
    )
    
    # Crew
    crew = Crew(
        agents=[aws_architect, terraform_designer, reviewer],
        tasks=[analyze_task, design_task, review_task],
        process=Process.sequential,
        verbose=True,
    )
    
    return crew

