from langgraph.graph import END, StateGraph, START

class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        error : Binary flag for control flow to indicate whether test error was tripped
        messages : With user question, error messages, reasoning
        generation : Code solution
        iterations : Number of tries
    """

    error: str
    messages: List
    generation: str
    iterations: int

# Max tries
max_iterations = 3
# Reflect
flag = 'reflect'
#flag = "do not reflect"

### Nodes

chain_for_code_generation = code_gen_chain_oai


def generate(state: GraphState):
    """
    Generate a code solution

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation
    """

    print("---GENERATING CODE SOLUTION---")

    # State
    messages = state["messages"]
    iterations = state["iterations"]
    error = state["error"]

    # We have been routed back to generation with an error
    if error == "yes":
        messages += [
            (
                "user",
                "Now, try again. Invoke the code tool to structure the output with a prefix, imports, and code block:",
            )
        ]

    # Solution
    code_solution = chain_for_code_generation.invoke(
        {"context": "", "messages": messages}
    )
    messages += [
        (
            "assistant",
            f"{code_solution.prefix} \n Imports: {code_solution.imports} \n Code: {code_solution.code}",
        )
    ]

    # Increment
    iterations = iterations + 1
    return {"generation": code_solution, "messages": messages, "iterations": iterations}


def code_check(state: GraphState):
    """
    Check code

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, error
    """

    print("---CHECKING CODE---")

    # State
    messages = state["messages"]
    code_solution = state["generation"]
    iterations = state["iterations"]

    # Get solution components
    imports = code_solution.imports
    code = code_solution.code

    # Check imports
    try:
        exec(imports)
    except Exception as e:
        print("---CODE IMPORT CHECK: FAILED---")
        error_message = [("user", f"Your solution failed the import test: {e}")]
        messages += error_message
        return {
            "generation": code_solution,
            "messages": messages,
            "iterations": iterations,
            "error": "yes",
        }

    # Check execution
    error_logs = []
    stdout_logs, stderr_logs = exec_with_tests(imports + "\n" + code, error_logs)

    if stderr_logs == '':
      # No errors
      print("---NO CODE TEST FAILURES---")
      return {
          "generation": code_solution,
          "messages": messages,
          "iterations": iterations,
          "error": "no",
      }
    else:
      print("---CODE BLOCK CHECK: FAILED---")
      error_message = [("user", f"Your solution failed the code execution test: {stderr_logs}")]
      messages += error_message
      return {
          "generation": code_solution,
          "messages": messages,
          "iterations": iterations,
          "error": "yes",
      }


def reflect(state: GraphState):
    """
    Reflect on errors

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation
    """

    print("---GENERATING CODE SOLUTION---")

    # State
    messages = state["messages"]
    iterations = state["iterations"]
    code_solution = state["generation"]

    # Prompt reflection

    print("reflection messages")
    print(messages)
    print("reflection messages")

    # Add reflection
    reflections = reflection_chain.invoke(
        {"context": "", "messages": messages}
    )
    messages += [("assistant", f"Here are reflections on the error: {reflections}")]
    return {"generation": code_solution, "messages": messages, "iterations": iterations}


### Edges


def decide_to_finish(state: GraphState):
    """
    Determines whether to finish.

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """
    error = state["error"]
    iterations = state["iterations"]

    if error == "no":
        print("---DECISION: FINISH--- Code successfully compiled")
        return "end"
    elif iterations == max_iterations:
      print("max iterations reached, quitting")
      return "end"
    else:
        print("---DECISION: RE-TRY SOLUTION---")
        if flag == "reflect":
            return "reflect"
        else:
            return "generate"

workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("generate", generate)  # generation solution
workflow.add_node("check_code", code_check)  # check code
workflow.add_node("reflect", reflect)  # reflect

# Build graph
workflow.add_edge(START, "generate")
workflow.add_edge("generate", "check_code")
workflow.add_conditional_edges(
    "check_code",
    decide_to_finish,
    {
        "end": END,
        "reflect": "reflect",
        "generate": "generate",
    },
)
workflow.add_edge("reflect", "generate")
app = workflow.compile()

##Testing the app : 
#question = "use sin function to model microsoft stock to trade." + "Make sure to output the class that contains the lumibot trading strategy. This will be deployed so make sure quantity traded works"
#solution = app.invoke({"messages": [("user", question)], "iterations": 4, "error": ""})