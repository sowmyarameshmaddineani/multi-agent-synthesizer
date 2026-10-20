import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI(title="Live Multi-Agent Knowledge Synthesizer")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
    <head>
        <title>Agent Stream Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f4f4f9; }
            h1 { color: #333; }
            button { padding: 10px 20px; font-size: 16px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #0056b3; }
            ul { margin-top: 20px; padding: 0; list-style: none; }
            li { background: white; padding: 10px 15px; margin-bottom: 8px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        </style>
    </head>
    <body>
        <h1>Live Agent Activity Stream 🤖</h1>
        <button onclick="startStream()">Trigger Agent Query</button>
        <ul id="messages"></ul>

        <script>
            function startStream() {
                const messages = document.getElementById('messages');
                messages.innerHTML = '';
                
                const ws = new WebSocket("ws://localhost:8000/ws/agent-stream");
                
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
        mock_steps = [
            {"agent": "Router", "status": "Analyzing user query intent..."},
            {"agent": "Researcher", "status": "Querying local vector database for context..."},
            {"agent": "Fact-Checker", "status": "Cross-referencing retrieved chunks for accuracy..."},
            {"agent": "Synthesizer", "status": "Drafting final comprehensive knowledge summary..."}
        ]

        for step in mock_steps:
            await asyncio.sleep(1.2)
            await websocket.send_text(json.dumps(step))
            
        await websocket.send_text(json.dumps({"agent": "System", "status": "Workflow completed successfully! 🎉"}))

    except WebSocketDisconnect:
        print("Client disconnected from agent stream.")