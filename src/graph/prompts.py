from pydantic import BaseModel, Field

# ------------------
# Structured Output
# ------------------

class EvaluationSchema(BaseModel):
    """Structured response for the critic node to enforce deterministic routing."""
    is_approved: bool = Field(
        description="True if the report meets quality standards and addresses the topic, False otherwise."
    )
    critique: str = Field(
        description="Detailed feedback highlighting missing facts, poor structure, or actionable fixes."
    )


# ------------------
# Prompts
# ------------------

# --- RESEARCHER PROMPT ---
RESEARCHER_SYSTEM_PROMPT = ("""You are an expert web researcher.
Your task is to analyze the given topic and previous critique (if any), 
then formulate precise search queries or directly summarize key findings.

Topic: {topic}
Critique to address: {critique}
"""
)

# --- WRITER PROMPT ---
WRITER_SYSTEM_PROMPT = """You are a professional technical writer.
Synthesize the raw research findings into a well-structured, clear, and comprehensive report.

Topic: {topic}
Raw Research Data:
{raw_researches}

Previous Critique (if revising):
{critique}
"""

# --- CRITIC PROMPT ---
CRITIC_SYSTEM_PROMPT = """You are a rigorous report reviewer and quality controller.
Evaluate the draft report against the given topic. Determine if it is complete, accurate, and ready for delivery.

Topic: {topic}
Draft Report:
{draft_report}
"""