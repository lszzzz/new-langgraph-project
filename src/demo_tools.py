import json
import logging
from typing import Annotated

from langchain.chat_models import init_chat_model
from langchain_core.messages import ToolMessage
from langchain_deepseek import ChatDeepSeek
from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from IPython.display import Image, display


class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)


tool = TavilySearch(max_results=2)
tools = [tool]

llm = ChatDeepSeek(model="deepseek-chat")
llm_with_tools = llm.bind_tools(tools)


def chatbot(state: State):
    print("chatbot state:{}".format(state))
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


tool_node = ToolNode(tools=[tool])
graph_builder.add_node("tools", tool_node)


graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition
)

graph_builder.add_edge("tools", "chatbot")
# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph = graph_builder.compile()

# try:
#     # display(Image(graph.get_graph().draw_mermaid_png()))
#     graph.get_graph().draw_mermaid_png(output_file_path="graph.png")
# except Exception:
#     # This requires some extra dependencies and is optional
#     pass


def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input)
    except:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break
