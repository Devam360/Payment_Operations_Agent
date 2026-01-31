from typing import TypedDict, List, Annotated, Literal
import operator
from colorama import Fore, Style
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END

from simulator import env
import tools 

# --- 1. THE REASONING ENGINE (STRUCTURED OUTPUT) ---
class AgentReasoning(BaseModel):
    summary: str = Field(description="Brief summary of observed metrics")
    status_assessment: Literal["HEALTHY", "CRITICAL", "WARNING"] = Field(description="Assessment of system health")
    hypothesis: str = Field(description="What is causing the issue?")
    action_plan: Literal["reroute", "escalate", "wait"] = Field(description="The decision on what to do")
    target_gateway: str = Field(description="If rerouting, which gateway? (Stripe/Adyen)", default="None")
    reasoning_trace: str = Field(description="Step-by-step logic for the decision")

# --- 2. THE LANGGRAPH STATE ---
class AgentState(TypedDict):
    metrics: dict
    history: Annotated[List[str], operator.add]
    last_reasoning: AgentReasoning


# --- DEFINE NODES ---
def monitor_node(state):
    metrics = env.get_metrics() 
    return {"metrics": metrics}

def reason_node(state):
    metrics = state["metrics"]
    
    llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0)
    
    structured_llm = llm.with_structured_output(AgentReasoning)
    
    system_prompt = """
    You are a Senior Payment Operations AI. Your goal is to maintain >95% success rates.
    Stripe is Primary. Adyen is Secondary.
    
    Rules:
    1. If Success Rate < 90% and error is 504/Timeout, it is likely a gateway outage. Reroute immediately.
    2. If Success Rate is > 95%, do nothing.
    3. Always explain your reasoning clearly.
    """
    
    response = structured_llm.invoke(f"System Context: {system_prompt}\n\nCurrent Metrics: {metrics}")
    
    print(f"{Fore.MAGENTA}[BRAIN]{Style.RESET_ALL} Assessment: {response.status_assessment}")
    print(f"        Decision: {response.action_plan.upper()}")
    
    return {"last_reasoning": response}

def act_node(state):
    decision = state["last_reasoning"]
    
    if decision.action_plan == "reroute":
        result = tools.reroute_traffic(decision.target_gateway)
    elif decision.action_plan == "escalate":
        result = tools.escalate_to_human(decision.reasoning_trace)
    else:
        result = tools.no_action()
        
    return {"history": [result]}

# --- BUILD GRAPH ---
workflow = StateGraph(AgentState)

workflow.add_node("monitor", monitor_node)
workflow.add_node("reason", reason_node)
workflow.add_node("act", act_node)

workflow.set_entry_point("monitor")
workflow.add_edge("monitor", "reason")
workflow.add_edge("reason", "act")
workflow.add_edge("act", END)

app = workflow.compile()