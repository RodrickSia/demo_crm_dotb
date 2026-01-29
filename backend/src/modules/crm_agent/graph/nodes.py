from typing import Literal
from .state import AgentState
from langgraph.graph import END
from langgraph.types import interrupt, Command
from langchain_google_genai import ChatGoogleGenerativeAI
from ..config.settings import GOOGLE_API_KEY
from ..config.prompts import LEAD_SCORE_CRITERIA, NEXT_FOLLOWUP_ACTIONS
from deepagents import create_deep_agent
from ....shared.utils.helpers import readMDFiles
from deepagents.backends.utils import create_file_data

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY
)
LEAD_SCORE_SKILL = ""
ACTIVITY_SUMMARY_SKILL = ""
NEXT_FOLLOWUP_ACTIONS = ""


# TODO Create node in which it is implmeneted by the deepagents with the skillsMD
"""
from pydantic import BaseModel, Field
from deepagents import create_deep_agent, CompiledSubAgent

class SkillOutput(BaseModel):
    summary: str = Field(description="Analysis summary")
    score: float = Field(ge=0, le=1)

deep_agent = create_deep_agent(
    response_format=SkillOutput,  # Structured!
    skills=["/skills/"]
)

subagent = CompiledSubAgent(
    name="structured-skill",
    description="Returns typed analysis.",
    runnable=deep_agent
)"""
# Structured output node to classify intent
def classifying_intent(state: AgentState) -> Command[Literal["generate_lead_score", "generate_followup_action", "generate_activity_summary"]]:
    """Route to appropriate node based on intent."""
    goto = None
    if state.intent == "score":
        goto = "generate_lead_score"
    elif state.intent == "stage":
        goto = "generate_followup_action"
    elif state.intent == "activity_summary":
        goto = "generate_activity_summary"
        
    assert goto is not None, "Invalid intent for classification."
    return Command(goto=goto)


# Read MD files
LeadScoreSkillStr = readMDFiles(LEAD_SCORE_SKILL)
leadScoreDeepAgent = create_deep_agent(
    context_schema=AgentState,
    skills=["./skills/"],
    model=llm, 
)
def generate_lead_score_deepagent(state: AgentState) -> Command:
    agentResponse = leadScoreDeepAgent.invoke(
        {   
            
            "messages": [
                {
                    "role": "user",
                    "content": f"""You are an expert leadScorer. You will need to analyze this student profile and provide for me a lead score
                    Here is the student data:
                    {state.user.model_dump_json(indent=2)}
                    You are also provided the weights for each criteria:
                    {state.weights.model_dump_json(indent=2)}
                    """,
                }
            ],
            "files": {"/leadscore.md": create_file_data(LeadScoreSkillStr)},
        },
            config={"configurable": {"thread_id": "123456"}},
        )
    # TODO make this return to evaluation Node
    # TODO fetch the agent Response and parse it onto the command
    return Command(
        goto=END)



def generate_lead_score(state: AgentState) -> Command:
    """Generate lead score based on user data and weighted attributes."""
    user_data = state.user
    weights = state.weights
    
    # Build weights description if provided
    weights_description = ""
    if weights:
        weights_description = f"""
APPLIED WEIGHTS (must sum to 100%):
• Demographics: {weights.demographics * 100:.0f}%
• Academic Background: {weights.acedemic_background * 100:.0f}%
• Activities History: {weights.activities_history * 100:.0f}%
• Payment History: {weights.payment_history * 100:.0f}%
• Learning History: {weights.learning_history * 100:.0f}%
"""
    else:
        weights_description = """
APPLIED WEIGHTS (default distribution):
• Demographics: 10%
• Academic Background: 20%
• Activities History: 20%
• Payment History: 30%
• Learning History: 20%
"""
    
    
    score_prompt = f"""You are an expert CRM analyst evaluating lead quality for an educational institution.

{LEAD_SCORE_CRITERIA}

{weights_description}

USER DATA:
{str(user_data)}

TASK: Analyze the user data against the five criteria above, apply the specified weights, and calculate a comprehensive lead score.

OUTPUT: Return ONLY a single integer between 0 and 100. No explanation, no text, just the number.
"""
    
    score_response = llm.invoke(score_prompt)
    score = score_response.content.strip()  # type: ignore
    assert score is not None, "LLM did not return a lead score."
    assert score.isdigit(), "Lead score is not a valid number."
    
    # Generate explanation
    explanation_prompt = f"""You are an expert CRM analyst. You've assigned a lead score of {score}/100 to this prospect.

{LEAD_SCORE_CRITERIA}

{weights_description}

USER DATA:
{str(user_data)}
SCORE: {score}
TASK: Provide a concise 2-3 sentence explanation for why this lead received a score of {score}/100.
Focus on the most impactful factors from the weighted criteria that influenced the score.
Mention specific strengths or concerns identified in the data.

OUTPUT: Write your explanation in clear, professional language and easy to understand.
"""
    
    explanation_response = llm.invoke(explanation_prompt)
    explanation = explanation_response.content.strip()  # type: ignore
    
    return Command(
        update={
            "lead_score": int(score),
            "lead_score_explanation": explanation
        },
        goto=END
    )

def generate_followup_action(state: AgentState) -> Command:
    """Determine the next follow-up action based on user data."""
    user_data = state.user
    
    prompt = f"""You are an expert CRM analyst for an educational institution.

TASK: Recommend the most appropriate next follow-up action for this lead.

{NEXT_FOLLOWUP_ACTIONS}

USER DATA:
{str(user_data)}

Analyze:
- Current engagement level and responsiveness
- Recent activity and interaction history
- Stage in the customer journey
- Outstanding needs or gaps
- Momentum and timing considerations

OUTPUT: Return ONLY the exact action name from the list above (e.g., "Send Welcome Email", "Schedule Discovery Call"). No explanation, no additional text.
"""
    
    response = llm.invoke(prompt)
    action = response.content.strip()  # type: ignore
    assert action is not None, "LLM did not return a follow-up action."
    
    # Validate action
    valid_actions = [
        "Send Welcome Email",
        "Schedule Discovery Call",
        "Share Program Information",
        "Invite to Open House/Campus Tour",
        "Send Personalized Enrollment Proposal",
        "Follow Up on Pending Application",
        "Schedule Assessment/Placement Test",
        "Offer Trial Class/Demo Session",
        "Send Re-Engagement Campaign",
        "Request Referral/Testimonial"
    ]
    
    if action not in valid_actions:
        # Default to a safe action
        action = "Schedule Discovery Call"
    
    # Generate explanation
    explanation_prompt = f"""You are an expert CRM analyst. You've recommended the action "{action}" for this lead.

USER DATA:
{str(user_data)}

TASK: Provide a concise 2-3 sentence explanation for why "{action}" is the most appropriate next step.
Cite specific factors from the user data that informed this recommendation.

OUTPUT: Write your explanation in clear, professional language.
"""
    
    explanation_response = llm.invoke(explanation_prompt)
    explanation = explanation_response.content.strip()  # type: ignore
    
    return Command(
        update={
            "followup_action": action,
            "followup_action_explanation": explanation
        },
        goto=END
    )

def generate_activity_summary(state: AgentState) -> Command:
    """Generate activity summary and recommendations for a lead."""
    user_data = state.user
    
    # Generate summary
    summary_prompt = f"""You are an expert CRM analyst for an educational institution.

TASK: Create a concise activity summary for this lead.

USER DATA:
{str(user_data)}

Analyze and summarize:
- Overall engagement patterns and trends
- Communication frequency and responsiveness
- Key activities and interactions
- Notable behaviors or milestones

OUTPUT: Write a 3-4 sentence professional summary that captures the lead's activity profile.
"""
    
    summary_response = llm.invoke(summary_prompt)
    summary = summary_response.content.strip()  # type: ignore
    assert summary is not None, "LLM did not return an activity summary."
    
    # Generate insights and recommendations
    explanation_prompt = f"""You are an expert CRM analyst. You've summarized this lead's activities as follows:

"{summary}"

USER DATA:
{str(user_data)}

TASK: Based on the activity summary and data patterns, provide:
1. 2-3 key insights about this lead's behavior and potential
2. Specific recommendations for next steps to advance this lead

OUTPUT: Write clear, actionable insights and recommendations (2-3 sentences total).
"""
    
    explanation_response = llm.invoke(explanation_prompt)
    explanation = explanation_response.content.strip()  # type: ignore
    
    return Command(
        update={
            "activity_summary": summary,
            "activity_summary_explanation": explanation
        },
        goto=END
    )
