from typing import Literal
from .state import AgentState
from langgraph.graph import END
from langgraph.types import interrupt, Command
from langchain_google_genai import ChatGoogleGenerativeAI
from ..config.settings import GOOGLE_API_KEY
from ..config.prompts import LEAD_SCORE_CRITERIA, NEXT_FOLLOWUP_ACTIONS
from deepagents import create_deep_agent
from ....shared.utils.helpers import readMDFiles
import json

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.0 
)
LEAD_SCORE_SKILL = "src/modules/crm_agent/graph/skills/leadScore/SKILL.md"
ACTIVITY_SUMMARY_SKILL = "src/modules/crm_agent/graph/skills/activitySummary/SKILL.md"
NEXT_FOLLOWUP_ACTIONS = "src/modules/crm_agent/graph/skills/nextFollowupActions/SKILL.md"

# Structured output node to classify intent
def classifying_intent(state: AgentState) -> Command[Literal["generate_lead_score", "generate_followup_action", "generate_activity_summary"]]:
    """Route to appropriate node based on intent."""
    assert state.intent is not None, "Intent must be set in state."
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
# TODO: Implement this, this is an issue caused by file loading not supported on window https://github.com/langchain-ai/deepagents/issues/889
# leadScoreDeepAgent = create_deep_agent(
#     context_schema=AgentState,
#     skills=["./skills/leadScore/SKILL.md"],
#     model=llm, 
# )
# agentResponse = leadScoreDeepAgent.invoke(
#     {   
        
#         "messages": [
#             {
#                 "role": "user",
#                 "content": f""" Give me back the leadsocre skill aka the markdown file that you are being given
#                 """,
#             }
#         ],
#         "files": {"./skills/leadScore/SKILL.md": create_file_data(LeadScoreSkillStr)},
#     }
#
leadScoreDeepAgent = create_deep_agent(
    context_schema=AgentState,
    system_prompt=LeadScoreSkillStr,
    model=llm, 
)

def generate_lead_score_deepagent(state: AgentState) -> Command:
    # The response is a structred output enforce by the skill
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
        },
            config={"configurable": {"thread_id": "123456"}},
        )
    # TODO make this return to evaluation Node
    modelMesage = agentResponse["messages"][-1].content[0]['text'] # A str represent a dict with {score, explanation}
    modelMessage = json.loads(modelMesage)
    return Command(
        update={
            "lead_score": int(modelMessage["score"]),
            "lead_score_explanation": modelMessage["explanation"]
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
    # TODO: FIX THE RESPONSE PARSING
    summary = summary_response.content # type: ignore
    print(summary)
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
    # TODO: FIX THE RESPONSE PARSING
    explanation = explanation_response.content["input"][0]["text"]  # type: ignore
    print(explanation)
    return Command(
        update={
            "activity_summary": summary,
            "activity_summary_explanation": explanation
        },
        goto=END
    )
