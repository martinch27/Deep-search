# deep_researcher/agents/critic_agent.py

"""
CriticAgent: оценивает текущие результаты (findings) и предлагает уточняющий follow-up вопрос, если нужно.
"""

from pydantic import BaseModel, Field
from typing import Optional
from .baseclass import ResearchAgent
from ..llm_config import LLMConfig, model_supports_structured_output
from .utils.parse_output import create_type_parser
from datetime import datetime

class CritiqueOutput(BaseModel):
    critique_summary: str = Field(..., description="Обзор того, насколько полно текущие findings отвечают на исходный запрос.")
    follow_up_question: Optional[str] = Field(None, description="Уточняющий follow-up вопрос, если в текущих findings есть пробелы")

INSTRUCTIONS = f"""
You are a critical research reviewer. Your job is to assess whether the current findings are complete and suggest further questions if needed.
Today's date is {datetime.now().strftime("%Y-%m-%d")}.

You will receive:
1. The original research query
2. Findings from the current iteration
3. All findings collected so far

Then:
- Summarize how well the findings meet the user's query and how deep and detailed the information is collected
- If something is missing or unclear, suggest a precise follow-up question to deepen the analysis.

Return a CritiqueOutput object with your assessment and optional question.

Only output JSON and follow the JSON schema below. Do not output anything else. I will be parsing this with Pydantic so output valid JSON only:
{CritiqueOutput.model_json_schema()}
"""

def init_critic_agent(config: LLMConfig) -> ResearchAgent:
    selected_model = config.fast_model  # или config.slow_model, если хочешь более качественный анализ

    return ResearchAgent(
        name="CriticAgent",
        instructions=INSTRUCTIONS,
        model=selected_model,
        output_type=CritiqueOutput if model_supports_structured_output(selected_model) else None,
        output_parser=create_type_parser(CritiqueOutput) if not model_supports_structured_output(selected_model) else None
    )