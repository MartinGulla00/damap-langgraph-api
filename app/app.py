from agent_graph.graph import create_graph, compile_workflow
import uuid

server = 'openai'
model = 'gpt-4o'
model_endpoint = None

iterations = 40

print ("Creating graph and compiling workflow...")
graph = create_graph(server=server, model=model, model_endpoint=model_endpoint)
workflow = compile_workflow(graph)
print ("Graph and workflow created.")


if __name__ == "__main__":

    verbose = False

    query = input("Please enter your question: ")
    with open("schemas/damap.sql", "r") as file:
        schema = file.read()

    dict_inputs = {"question": query, "schema": schema}

    user_thread_id = input("Please enter your thread id: ")
    if user_thread_id:
        thread_id = user_thread_id
    else:
        thread_id = str(uuid.uuid4())
    limit = {"recursion_limit": iterations, "configurable": { "thread_id": thread_id }}

    for event in workflow.stream(
        dict_inputs, limit
        ):
        if verbose:
            print("\nState Dictionary:", event)
        else:
            print("\n")
