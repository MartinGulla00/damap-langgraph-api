import json
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent_graph.graph import create_graph, compile_workflow
from states.state import state

server = 'openai'
model = 'gpt-4o'
model_endpoint = None
iterations = 20

print("Creating graph and compiling workflow...")
graph = create_graph(server=server, model=model, model_endpoint=model_endpoint)
workflow = compile_workflow(graph)
print("Graph and workflow created.")

app = FastAPI()

class WorkflowRequest(BaseModel):
    question: str
    schema: str  
    thread_id: str = None

@app.post("/execute-workflow")
async def execute_workflow(request: WorkflowRequest):
    try:
        initial_state = state.copy()
        initial_state.update({
            "question": request.question,
            "schema": request.schema,  
        })

        thread_id = request.thread_id or str(uuid.uuid4())
        limit = {
            "recursion_limit": iterations,
            "configurable": {"thread_id": thread_id}
        }

        response = []

        for event in workflow.stream(initial_state, limit):
            response.append(event)

        sql_query = extract_sql_query(response)

        return {
            "thread_id": thread_id,
            "sql_query": sql_query or "No SQL query generated.",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def extract_sql_query(response):
    """
    Extrae la consulta SQL desde la respuesta del workflow.
    """
    try:
        for event in response:
            if "generator" in event:
                generator_response = event["generator"].get("query_generator_response", None)

                if generator_response:
                    # Manejar diferentes formatos de datos
                    if isinstance(generator_response, str):
                        generator_data = json.loads(generator_response)
                    elif isinstance(generator_response, list) and generator_response:
                        generator_data = json.loads(generator_response[-1]["content"])
                    else:
                        generator_data = generator_response

                    return generator_data.get("sql_query", None)

    except Exception as e:
        print(f"Error extracting SQL query: {e}")
    return None
