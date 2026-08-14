from typing import Callable
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage

from src.graph.state import ReportState
from src.graph.prompts import (
    RESEARCHER_SYSTEM_PROMPT,
    WRITER_SYSTEM_PROMPT,
    CRITIC_SYSTEM_PROMPT,
    EvaluationSchema,
)

def make_research_node(llm: BaseChatModel) -> Callable[[ReportState], dict]:
    """Factory creating research node subroutine bound to injected LLM instance."""

    def research_node(state: ReportState) -> dict:
        """Gathers raw information on the topic based on current state & feedback."""
        prompt = RESEARCHER_SYSTEM_PROMPT.format(
            topic=state["topic"],
            critique=state.get("critique", "None")
        )
        
        response = llm.invoke(prompt)
        
        # Return dictionary patch: operator.add appends raw_researches
        return {
            "raw_researches": [response.content],
            "messages": [AIMessage(content=f"Gathered research for topic: {state['topic']}")]
        }
    
    return research_node


def make_writer_node(llm: BaseChatModel) -> Callable[[ReportState], dict]:
    """Factory creating writer node subroutine bound to injected LLM instance."""
    
    def writer_node(state: ReportState) -> dict:
        """Synthesizes raw research into a structured draft report."""
        prompt = WRITER_SYSTEM_PROMPT.format(
            topic=state["topic"],
            raw_researches="\n---\n".join(state.get("raw_researches", [])),
            critique=state.get("critique", "None")
        )
        
        response = llm.invoke(prompt)
        
        # Overwrites draft_report state key
        return {
            "draft_report": response.content,
            "messages": [AIMessage(content="Generated draft report.")]
        }
    
    return writer_node

def make_critic_node(llm: BaseChatModel) -> Callable[[ReportState], dict]:
    """Factory creating critic node subroutine bound to injected LLM instance."""
    structured_llm = llm.with_structured_output(EvaluationSchema)
    
    def critic_node(state: ReportState) -> dict:
        """Evaluates the draft report using structured output matching EvaluationSchema."""
        prompt = CRITIC_SYSTEM_PROMPT.format(
            topic=state["topic"],
            draft_report=state["draft_report"]
        )
        
        evaluation: EvaluationSchema = structured_llm.invoke(prompt)
        current_iterations = state.get("iteration_count", 0) + 1
        
        return {
            "is_approved": evaluation.is_approved,
            "critique": evaluation.critique,
            "iteration_count": current_iterations,
            "messages": [AIMessage(content=f"Critique complete. Approved: {evaluation.is_approved}")]
        }
        
    return critic_node