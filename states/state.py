from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

# Define the state object for the agent graph
class AgentGraphState(TypedDict):
    question: str
    schema: str
    planner_response: Annotated[list, add_messages]
    # table_selector_response: Annotated[list, add_messages]
    query_generator_response: Annotated[list, add_messages]
    query_checker_response: Annotated[list, add_messages]
    router_response: Annotated[list, add_messages]
    end_chain: Annotated[list, add_messages]

# Define the nodes in the agent graph
def get_agent_graph_state(state:AgentGraphState, state_key:str):
    if state_key == "planner_all":
        return state["planner_response"]
    elif state_key == "planner_latest":
        if state["planner_response"]:
            return state["planner_response"][-1]
        else:
            return state["planner_response"]
    

    # elif state_key == "table_selector_all":
        # return state["table_selector_response"]
    # elif state_key == "table_selector_latest":
        # if state["table_selector_response"]:
            # return state["table_selector_response"][-1]
        # else: 
            # return state["table_selector_response"]
        
    elif state_key == "query_generator_all":
        return state["query_generator_response"]
    elif state_key == "query_generator_latest":
        if state["query_generator_response"]:
            return state["query_generator_response"][-1]
        else: 
            return state["query_generator_response"]
        
    elif state_key == "query_checker_all":
        return state["query_checker_response"]
    elif state_key == "query_checker_latest":
        if state["query_checker_response"]:
            return state["query_checker_response"][-1]
        else: 
            return state["query_checker_response"]

    else:
        return None
    
state = {
    "question":"",
    "schema": "",
    "planner_response": [],
    # "table_selector_response": [],
    "query_generator_response": [],
    "query_checker_response": [],
    "router_response": [],
    "end_chain": []
}