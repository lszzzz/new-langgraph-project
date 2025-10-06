import uuid

import httpx
import requests
from langgraph_sdk import get_client
import asyncio

client = get_client(url="http://localhost:2024")


async def main():
    # config = {"configurable": {"thread_id": "1"}}
    # thread_id = str(uuid.uuid4())
    thread_id = "fb3f026a-b0f2-4929-9235-e84e6416c43f"

    async for chunk in client.runs.stream(
        thread_id,  # Threadless run
        "agent", # Name of assistant. Defined in langgraph.json.
        input={
        "messages": [{
            "role": "user",
            "content": "我是李四",
            }],
        },
    ):
        print(f"Receiving new event of type: {chunk.event}...")
        print(chunk.data)
        print("\n\n")

    async for chunk in client.runs.stream(
        thread_id,  # Threadless run
        "agent", # Name of assistant. Defined in langgraph.json.
        input={
        "messages": [{
            "role": "user",
            "content": "我是谁",
            }],
        },
    ):
        print(f"Receiving new event of type: {chunk.event}...")
        print(chunk.data)
        print("\n\n")


def create_thread():
    response = requests.post("http://localhost:2024/threads",
                  headers={
                      "Content-Type": "application/json"
                  },
                  json={
                      "thread_id": "",
                      "metadata": {},
                      "if_exists": "raise",
                      "ttl": {
                          "strategy": "delete",
                          "ttl": 1
                      },
                      "supersteps": [
                          {
                              "updates": [
                                  {
                                      "values": [
                                          {}
                                      ],
                                      "command": {
                                          "update": None,
                                          "resume": None,
                                          "goto": {
                                              "node": "",
                                              "input": None
                                          }
                                      },
                                      "as_node": ""
                                  }
                              ]
                          }
                      ]
                  }
                  )
    print(response.text)


asyncio.run(main())
# create_thread()
