# deep_researcher/agents/fact_extractor_agent.py

from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

from .baseclass import ResearchAgent
from ..llm_config import LLMConfig, model_supports_structured_output
from .utils.parse_output import create_type_parser


class ExtractedItem(BaseModel):
    title: str = Field(..., description="Name of information type (e.g., fact, preference, limitation, context)")
    description: str = Field(..., description="Description of what the user said")


class FlexibleExtractionOutput(BaseModel):
    extracted: List[ExtractedItem] = Field(..., description="List of extracted key information blocks")


INSTRUCTIONS = f"""
You are an intelligent agent for extracting durable facts and background data from user queries. Today's date: {datetime.now().strftime('%Y-%m-%d')}

Your task is to decide what should be remembered **long-term** from the user’s message for future reasoning.

You must:
- Extract **only persistent or factual context** (e.g., location, status, preferences, background);
- Ignore **temporary goals**, questions, or intentions ("the user wants to know", "the user is looking for...");
- Focus on what the user states about themselves — not what they are asking about.

Examples of what to extract:
- Residence, citizenship, employment, education, health, legal status, ownership, preferences, past experiences.

Examples of what **not** to extract:
- Questions or hypotheses;
- Intentions to learn something;
- Temporary research focus.

Output format: JSON with a single key `extracted`, which contains an array of objects.
Each object has:
- title: short label for the type of information (e.g., "residence", "employment status", "citizenship")
- description: exact user-claimed information, written in plain language

Example output:
{{
  "extracted": [
    {{
      "title": "residence",
      "description": "The user lives in Germany"
    }},
    {{
      "title": "citizenship",
      "description": "The user is a refugee from Ukraine"
    }}
  ]
}}

Important: output **only** valid JSON. No extra text, comments or markdown. JSON must follow the exact schema:
{FlexibleExtractionOutput.model_json_schema()}
"""

def init_fact_extractor_agent(config: LLMConfig) -> ResearchAgent:
    selected_model = config.fast_model
    return ResearchAgent(
        name="FactExtractorAgent",
        instructions=INSTRUCTIONS,
        model=selected_model,
        output_type=FlexibleExtractionOutput if model_supports_structured_output(selected_model) else None,
        output_parser=create_type_parser(FlexibleExtractionOutput) if not model_supports_structured_output(selected_model) else None
    )