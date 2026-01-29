from typing import Literal
from .state import AgentState
from langgraph.graph import END
from langgraph.types import interrupt, Command
from langchain_google_genai import ChatGoogleGenerativeAI
from ..config.settings import GOOGLE_API_KEY
from deepagents import create_deep_agent
from ....shared.utils.helpers import readMDFiles
import json

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemma-3-27b-it",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.0 
)
LEAD_SCORE_SKILL_PATH = "src/modules/crm_agent/graph/skills/leadScore/SKILL.md"
ACTIVITY_SUMMARY_SKILL_PATH = "src/modules/crm_agent/graph/skills/activitySummary/SKILL.md"
NEXT_FOLLOWUP_ACTIONS_SKILL_PATH = "src/modules/crm_agent/graph/skills/nextFollowupActions/SKILL.md"

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
LeadScoreSkillStr = readMDFiles(LEAD_SCORE_SKILL_PATH)
ActivitySummarySkillStr = readMDFiles(ACTIVITY_SUMMARY_SKILL_PATH)
NextFollowupActionSkillStr = readMDFiles(NEXT_FOLLOWUP_ACTIONS_SKILL_PATH)

leadScoreDeepAgent = create_deep_agent(
    context_schema=AgentState,
    system_prompt=LeadScoreSkillStr,
    model=llm, 
)

activitySummaryDeepAgent = create_deep_agent(
    context_schema=AgentState,
    system_prompt=ActivitySummarySkillStr,
    model=llm,
)

nextFollowupActionDeepAgent = create_deep_agent(
    context_schema=AgentState,
    system_prompt=NextFollowupActionSkillStr,
    model=llm,
)

def generate_lead_score(state: AgentState) -> Command:
    # The response is a structured output enforce by the skill
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
    modelMessageContent = agentResponse["messages"][-1].content
    if isinstance(modelMessageContent, list):
        modelMessageStr = modelMessageContent[0]['text']
    else:
        modelMessageStr = modelMessageContent
        
    modelMessage = json.loads(modelMessageStr)
    return Command(
        update={
            "lead_score": int(modelMessage["score"]),
            "lead_score_explanation": modelMessage["explanation"]
        },
        goto=END
    )

def generate_followup_action(state: AgentState) -> Command:
    agentResponse = nextFollowupActionDeepAgent.invoke(
        {   
            "messages": [
                {
                    "role": "user",
                    "content": f"""You are an expert CRM analyst. Analyze this student profile and recommend the best next follow-up action.
                    Here is the student data:
                    {state.user.model_dump_json(indent=2)}
                    """,
                }
            ],
        },
        config={"configurable": {"thread_id": "followup_123"}},
    )
    
    modelMessageContent = agentResponse["messages"][-1].content
    if isinstance(modelMessageContent, list):
        modelMessageStr = modelMessageContent[0]['text']
    else:
        modelMessageStr = modelMessageContent
        
    modelMessage = json.loads(modelMessageStr)
    
    return Command(
        update={
            "followup_action": modelMessage["followup_action"],
            "followup_action_explanation": modelMessage["followup_action_explanation"]
        },
        goto=END
    )

def generate_activity_summary(state: AgentState) -> Command:
    agentResponse = activitySummaryDeepAgent.invoke(
        {   
            "messages": [
                {
                    "role": "user",
                    "content": f"""You are an expert CRM analyst. Analyze this student profile and provide an activity summary and recommendations.
                    Here is the student data:
                    {state.user.model_dump_json(indent=2)}
                    """,
                }
            ],
        },
        config={"configurable": {"thread_id": "summary_123"}},
    )
    
    modelMessageContent = agentResponse["messages"][-1].content
    if isinstance(modelMessageContent, list):
        modelMessageStr = modelMessageContent[0]['text']
    else:
        modelMessageStr = modelMessageContent
        
    modelMessage = json.loads(modelMessageStr)
    
    return Command(
        update={
            "activity_summary": modelMessage["activity_summary"],
            "activity_summary_explanation": modelMessage["activity_summary_explanation"]
        },
        goto=END
    )
