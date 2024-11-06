from models.openai_models import get_open_ai, get_open_ai_json
from prompts.prompts import (
    planner_prompt_template,
    table_selector_prompt_template,
    query_checker_prompt_template
)
from utils.helper_functions import get_current_utc_datetime, check_for_content
from states.state import AgentGraphState

class Agent:
    def __init__(self, state: AgentGraphState, model=None, server=None, temperature=0, model_endpoint=None, stop=None, guided_json=None):
        self.state = state
        self.model = model
        self.server = server
        self.temperature = temperature
        self.model_endpoint = model_endpoint
        self.stop = stop
        self.guided_json = guided_json

    def get_llm(self, json_model=True):
        return get_open_ai_json(model=self.model, temperature=self.temperature) if json_model else get_open_ai(model=self.model, temperature=self.temperature)
    def update_state(self, key, value):
        self.state = {**self.state, key: value}

class PlannerAgent(Agent):
    def invoke(self, natural_language_question, prompt=planner_prompt_template, feedback=None):
        feedback_value = feedback() if callable(feedback) else feedback
        feedback_value = check_for_content(feedback_value)

        planner_prompt = prompt.format(
            feedback=feedback_value,
            datetime=get_current_utc_datetime()
        )

        messages = [
            {"role": "system", "content": planner_prompt},
            {"role": "user", "content": f"question: {natural_language_question}"}
        ]

        llm = self.get_llm()
        ai_msg = llm.invoke(messages)
        response = ai_msg.content

        print(f"planner: {response}")
        self.update_state("planner_response", response)

        return self.state

class TableSelectorAgent(Agent):
    def invoke(self, question, prompt=table_selector_prompt_template, feedback=None, previous_selections=None, schema=None):
        feedback_value = feedback() if callable(feedback) else feedback
        previous_selections_value = previous_selections() if callable(previous_selections) else previous_selections

        feedback_value = check_for_content(feedback_value)
        previous_selections_value = check_for_content(previous_selections_value)

        selector_prompt = prompt.format(
            feedback=feedback_value,
            previous_selections=previous_selections_value,
            schema=schema,
            datetime=get_current_utc_datetime()
        )

        messages = [
            {"role": "system", "content": selector_prompt},
            {"role": "user", "content": f"research question: {question}"}
        ]

        llm = self.get_llm()
        ai_msg = llm.invoke(messages)
        response = ai_msg.content

        print(f"table selector: {response}")
        self.update_state("selector_response", response)

        return self.state

class QueryCheckerAgent(Agent):
    def invoke(self, question, prompt=query_checker_prompt_template, feedback=None, generator=None):
        feedback_value = feedback() if callable(feedback) else feedback
        generator_value = generator() if callable(generator) else generator

        reporter_value = check_for_content(reporter_value)
        feedback_value = check_for_content(feedback_value)
        
        query_checker_prompt = prompt.format(
            generator=generator_value,
            state=self.state,
            feedback=feedback_value,
            datetime=get_current_utc_datetime(),
        )

        messages = [
            {"role": "system", "content": query_checker_prompt},
            {"role": "user", "content": f"research question: {question}"}
        ]

        llm = self.get_llm()
        ai_msg = llm.invoke(messages)
        response = ai_msg.content

        print(f"query_checker: {response}")
        self.update_state("query_checker_response", response)

        return self.state
# TODO: LLEGUE HASTA AQUI
class RouterAgent(Agent):
    def invoke(self, feedback=None, research_question=None, prompt=router_prompt_template):
        feedback_value = feedback() if callable(feedback) else feedback
        feedback_value = check_for_content(feedback_value)

        router_prompt = prompt.format(feedback=feedback_value)

        messages = [
            {"role": "system", "content": router_prompt},
            {"role": "user", "content": f"research question: {research_question}"}
        ]

        llm = self.get_llm()
        ai_msg = llm.invoke(messages)
        response = ai_msg.content

        print(colored(f"Router 🧭: {response}", 'blue'))
        self.update_state("router_response", response)
        return self.state

class FinalReportAgent(Agent):
    def invoke(self, final_response=None):
        final_response_value = final_response() if callable(final_response) else final_response
        response = final_response_value.content

        print(colored(f"Final Report 📝: {response}", 'blue'))
        self.update_state("final_reports", response)
        return self.state

class EndNodeAgent(Agent):
    def invoke(self):
        self.update_state("end_chain", "end_chain")
        return self.state