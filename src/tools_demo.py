from langchain_tavily import TavilySearch

tool = TavilySearch(max_results=2)
tools = [tool]
result = tool.invoke("What's a 'node' in LangGraph?")

print(result)
