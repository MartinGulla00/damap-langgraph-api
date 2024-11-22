from agent_graph.graph import create_graph, compile_workflow

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

    limit = {"recursion_limit": iterations}

    for event in workflow.stream(
        dict_inputs, limit
        ):
        if verbose:
            print("\nState Dictionary:", event)
        else:
            print("\n")
