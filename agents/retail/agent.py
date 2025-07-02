from langchain_core.messages import AIMessage
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.types import Command

# Define state schema
class AgentState(MessagesState, total=False):
    """`total=False` is PEP589 specs.

    documentation: https://typing.readthedocs.io/en/latest/spec/typeddict.html#totality
    """

# Dummy agent that echoes back the last user message
def model(state: AgentState) -> AgentState:
    messages = state["messages"]
    last_message = messages[-1]
    
    # Create a dummy response message
    response = AIMessage(
        content = f"Echo: {last_message.content}"
    )

    # Append to message history
    return {
        "messages": messages + [response]
    }

# retail_agent = None

# Create the graph
graph = StateGraph(AgentState)

# Add a node for the dummy agent
graph.add_node("model", model)

# Set the start and end conditions
graph.set_entry_point("model")
graph.add_edge("model", END)

# Compile the graph
retail_agent = graph.compile()

