from datetime import datetime
from tempfile import TemporaryDirectory

from websockets.sync.client import connect as ws_connect

import autogen
from autogen.io.websockets import IOWebsockets

from configs import llama_3_1_config
import asyncio
from contextlib import asynccontextmanager  # noqa: E402
from pathlib import Path  # noqa: E402

from fastapi import FastAPI  # noqa: E402
from fastapi.responses import HTMLResponse  # noqa: E402
import uvicorn  # noqa: E402

from groupchat import groupchat_yzhu_cust

PORT = 8000

def on_connect(iostream: IOWebsockets) -> None:
    print(f" - on_connect(): Connected to client using IOWebsockets {iostream}", flush=True)

    print(" - on_connect(): Receiving message from client.", flush=True)

    # 1. Receive Initial Message
    # initial_msg = iostream.input()
    initial_msg = None

    # 2. Instantiate ConversableAgent
    agent = autogen.ConversableAgent(
        name="chatbot",
        system_message="Complete a task given to you and reply TERMINATE when the task is done. If asked about the weather, use tool 'weather_forecast(city)' to get the weather forecast for a city.",
        llm_config=llama_3_1_config
    )

    # 3. Define UserProxyAgent
    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        system_message="A proxy for the user.",
        is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
        code_execution_config=False,
    )

    # 4. Define Agent-specific Functions
    def weather_forecast(city: str) -> str:
        return f"The weather forecast for {city} at {datetime.now()} is sunny."

    autogen.register_function(
        weather_forecast, caller=agent, executor=user_proxy, description="Weather forecast for a city"
    )

    # 5. Initiate conversation
    print(
        f" - on_connect(): Initiating chat with agent {agent} using message '{initial_msg}'",
        flush=True,
    )
    groupchat_yzhu_cust()

if False:
    with IOWebsockets.run_server_in_thread(on_connect=on_connect, port=8765) as uri:
        print(f" - test_setup() with websocket server running on {uri}.", flush=True)

        with ws_connect(uri) as websocket:
            print(f" - Connected to server on {uri}", flush=True)

            print(" - Sending message to server.", flush=True)
            # websocket.send("2+2=?")
            websocket.send("Check out the weather in Paris and write a poem about it.")

            while True:
                message = websocket.recv()
                message = message.decode("utf-8") if isinstance(message, bytes) else message

                print(message, end="", flush=True)

                if "TERMINATE" in message:
                    print()
                    print(" - Received TERMINATE message. Exiting.", flush=True)
                    break

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Autogen websocket test</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8080/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

@asynccontextmanager
async def run_websocket_server(app):
    with IOWebsockets.run_server_in_thread(on_connect=on_connect, port=8080) as uri:
        print(f"Websocket server started at {uri}.", flush=True)

        yield

app = FastAPI(lifespan=run_websocket_server)

@app.get("/")
async def get():
    return HTMLResponse(html)

async def main():
    config = uvicorn.Config(app)
    server = uvicorn.Server(config)
    await server.serve()  # noqa: F704


if __name__ == "__main__":
    asyncio.run(main())