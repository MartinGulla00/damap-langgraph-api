import json
import ast
from langgraph.graph import StateGraph
from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage
from agents.agents import (
    PlannerAgent,
    TableSelectorAgent,
    EndNodeAgent,
    QueryGeneratorAgent,
    QueryCheckerAgent,
    RouterAgent,
)
from prompts.prompts import (
    planner_prompt_template,
    planner_guided_json,
    table_selector_prompt_template,
    table_selector_guided_json,
    query_generator_prompt_template,
    query_generator_guided_json,
    query_checker_prompt_template,
    query_checker_guided_json,
    router_prompt_template,
    router_guided_json,
)
from states.state import AgentGraphState, get_agent_graph_state, state
from utils.helper_functions import print_sql_query

def create_graph(server=None, model=None, stop=None, model_endpoint=None, temperature=0):
    graph = StateGraph(AgentGraphState)

    graph.add_node(
        "planner", 
        lambda state: PlannerAgent(
            state=state,
            model=model,
            server=server,
            guided_json=planner_guided_json,
            stop=stop,
            model_endpoint=model_endpoint,
            temperature=temperature
        ).invoke(
            natural_language_question=state["question"],
            prompt=planner_prompt_template,
            feedback=lambda: get_agent_graph_state(state=state, state_key="planner_latest"),
        )
    )

    graph.add_node(
        "selector",
        lambda state: TableSelectorAgent(
            state=state,
            model=model,
            server=server,
            guided_json=table_selector_guided_json,
            stop=stop,
            model_endpoint=model_endpoint,
            temperature=temperature
        ).invoke(
            question=state["question"],
            feedback=lambda: get_agent_graph_state(state=state, state_key="query_checker_latest"),
            previous_selections=lambda: get_agent_graph_state(state=state, state_key="table_selector_all"),
            prompt=table_selector_prompt_template,
            schema=state["schema"]
        )
    )

    graph.add_node(
        "generator", 
        lambda state: QueryGeneratorAgent(
            state=state,
            model=model,
            server=server,
            guided_json=query_generator_guided_json,
            stop=stop,
            model_endpoint=model_endpoint,
            temperature=temperature
        ).invoke(
            question=state["question"],
            feedback=lambda: get_agent_graph_state(state=state, state_key="query_checker_latest"),
            previous_queries=lambda: get_agent_graph_state(state=state, state_key="query_generator_all"),
            prompt=query_generator_prompt_template,
            schema=state["schema"],
            selector=lambda: get_agent_graph_state(state=state, state_key="selector_latest")
        )
    )

    graph.add_node(
        "checker", 
        lambda state: QueryCheckerAgent(
            state=state,
            model=model,
            server=server,
            guided_json=query_checker_guided_json,
            stop=stop,
            model_endpoint=model_endpoint,
            temperature=temperature
        ).invoke(
            question=state["question"],
            feedback=lambda: get_agent_graph_state(state=state, state_key="query_checker_latest"),
            generator=lambda: get_agent_graph_state(state=state, state_key="query_generator_latest"),
            prompt=query_checker_prompt_template,
            schema=state["schema"]
        )
    )

    graph.add_node(
        "router", 
        lambda state: RouterAgent(
            state=state,
            model=model,
            server=server,
            guided_json=router_guided_json,
            stop=stop,
            model_endpoint=model_endpoint,
            temperature=temperature
        ).invoke(
            question=state["question"],
            feedback=lambda: get_agent_graph_state(state=state, state_key="query_checker_latest"),
            prompt=router_prompt_template
        )
    )

    graph.add_node("end", lambda state: EndNodeAgent(state).invoke())

    # Define the edges in the agent graph
    def pass_review(state: AgentGraphState):
        review_list = state["router_response"]
        if review_list:
            review = review_list[-1]
        else:
            review = "No review"
        print("Review: ", review)
        if review != "No review":
            if isinstance(review, HumanMessage):
                review_content = review.content
            else:
                review_content = review
            
            review_data = json.loads(review_content)
            next_agent = review_data["next_agent"]
        else:
            next_agent = "end"
        if next_agent == "end":
            print_sql_query(lambda: get_agent_graph_state(state=state, state_key="query_generator_latest"))
        return next_agent

    # Add edges to the graph
    graph.set_entry_point("planner")
    graph.set_finish_point("end")
    graph.add_edge("planner", "selector")
    graph.add_edge("selector", "generator")
    graph.add_edge("generator", "checker")
    graph.add_edge("checker", "router")

    graph.add_conditional_edges(
        "router",
        lambda state: pass_review(state=state),
    )

    return graph

def compile_workflow(graph):
    workflow = graph.compile()
    return workflow
