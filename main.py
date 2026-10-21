from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from agent_engine import AgentEngine

app = FastAPI(title="Live Multi-Agent Knowledge Synthesizer")

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Live Agent Synthesizer</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f8f9fa; }
            h1 { color: #333; }
            #logs { margin-top: 20px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); max-height: 500px; overflow-y: auto; }
            input[type="text"] { width: 300px; padding: 10px; border: 1px solid #ccc; border-radius: 4px; }
            button { padding: 10px 20px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
            button:hover { background-color: #0056b3; }
        </style>
    </head>
    <body>
        <h1>Live Multi-Agent Knowledge Synthesizer 🤖</h1>
        <input type="text" id="queryInput" placeholder="Enter query..." value="SOWMYA" />
        <button onclick="runAgents()">Run Agents</button>
        <div id="logs"></div>

        <script>
            let ws;
            function runAgents() {
                const query = document.getElementById('queryInput').value;
                const logsDiv = document.getElementById('logs');
                logsDiv.innerHTML = ''; 

                if (ws) {
                    ws.close();
                }

                ws = new WebSocket("ws://localhost:8000/ws/agent");

                ws.onopen = function() {
                    ws.send(query);
                };

                ws.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    const entry = document.createElement('div');
                    entry.style.margin = "8px 0";
                    entry.style.padding = "10px";
                    entry.style.borderRadius = "6px";
                    entry.style.border = "1px solid #ddd";
                    entry.style.backgroundColor = "#fafafa";
                    
                    // Color code agents
                    let badgeColor = "#007bff";
                    if (data.agent === "Router") badgeColor = "#6c757d";
                    if (data.agent === "Researcher") badgeColor = "#17a2b8";
                    if (data.agent === "Fact-Checker") badgeColor = "#ffc107";
                    if (data.agent === "Synthesizer") badgeColor = "#28a745";
                    if (data.agent === "System") badgeColor = "#343a40";

                    entry.innerHTML = `<span style="background:${badgeColor}; color:white; padding:3px 8px; border-radius:4px; font-weight:bold; font-size:12px; margin-right:8px;">[${data.agent}]</span> ${data.status}`;
                    logsDiv.appendChild(entry);
                    logsDiv.scrollTop = logsDiv.scrollHeight;
                };
            }
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws/agent")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        query = await websocket.receive_text()
        engine = AgentEngine(query)
        await engine.run_workflow(websocket)
    except WebSocketDisconnect:
        print("Client disconnected.")