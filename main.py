import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from agent_engine import AgentEngine

app = FastAPI(title="Live Multi-Agent Knowledge Synthesizer")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
    <head>
        <title>Live Agent Synthesizer</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f4f4f9; }
            h1 { color: #333; }
            .input-container { margin-bottom: 20px; }
            input { padding: 10px; width: 300px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px; }
            button { padding: 10px 20px; font-size: 16px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #0056b3; }
            ul { margin-top: 20px; padding: 0; list-style: none; }
            li { background: white; padding: 10px 15px; margin-bottom: 8px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        </style>
    </head>
    <body>
        <h1>Live Multi-Agent Knowledge Synthesizer 🤖</h1>
        <div class="input-container">
            <input type="text" id="queryInput" placeholder="Ask a complex question..." value="Explain quantum computing basics">
            <button onclick="startStream()">Run Agents</button>
        </div>
        <ul id="messages"></ul>

        <script>
            let ws = null;

            function startStream() {
                const query = document.getElementById('queryInput').value;
                const messages = document.getElementById('messages');
                messages.innerHTML = ''; // Clear previous messages
                
                ws = new WebSocket("ws://localhost:8000/ws/agent-stream");
                
                ws.onopen = function() {
                    // Send user query to the backend once connected
                    ws.send(JSON.stringify({ query: query }));
                };

                ws.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    const message = document.createElement('li');
                    message.innerHTML = `<strong>[${data.agent}]</strong> ${data.status}`;
                    messages.appendChild(message);
                };
            }
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(HTML_TEMPLATE)

@app.websocket("/ws/agent-stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        # Wait for the client to send the initial query packet
        data = await websocket.receive_text()
        payload = json.loads(data)
        user_query = payload.get("query", "General Knowledge Inquiry")

        # Instantiate our Agent Engine with the dynamic query
        engine = AgentEngine(query=user_query)
        await engine.run_workflow(websocket)

    except WebSocketDisconnect:
        print("Client disconnected from agent stream.")