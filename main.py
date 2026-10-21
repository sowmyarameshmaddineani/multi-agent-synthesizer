from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from agent_engine import AgentEngine

app = FastAPI(
    title="Live Multi-Agent Knowledge Synthesizer",
    description="Real-Time Autonomous Agent Event Stream with Vector RAG & Session Memory",
    version="1.0.0"
)

html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Live Multi-Agent Knowledge Synthesizer</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; font-family: 'Inter', sans-serif; margin: 0; padding: 0; }
        body { background-color: #0f172a; color: #f8fafc; min-height: 100vh; padding: 30px 20px; }
        .container { max-width: 900px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { font-size: 2rem; font-weight: 700; color: #38bdf8; margin-bottom: 8px; }
        .header p { color: #94a3b8; font-size: 0.95rem; }
        
        .search-box { display: flex; gap: 12px; margin-bottom: 25px; }
        input[type="text"] { flex: 1; padding: 14px 18px; border-radius: 8px; border: 1px solid #334155; background-color: #1e293b; color: #fff; font-size: 1rem; outline: none; }
        input[type="text"]:focus { border-color: #38bdf8; }
        button { padding: 14px 28px; background-color: #0284c7; color: white; border: none; border-radius: 8px; font-weight: 600; font-size: 1rem; cursor: pointer; transition: background 0.2s; }
        button:hover { background-color: #0369a1; }
        
        .card { background: #1e293b; border-radius: 12px; border: 1px solid #334155; padding: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.3); }
        .card-header { font-size: 0.9rem; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 15px; }
        
        #logs { max-height: 520px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }
        .log-entry { padding: 12px 16px; border-radius: 8px; background: #0f172a; border-left: 4px solid #38bdf8; font-size: 0.95rem; line-height: 1.5; color: #e2e8f0; }
        
        /* Agent Specific Colors */
        .badge { display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 700; margin-right: 8px; text-transform: uppercase; }
        .badge-Router { background: #475569; color: #fff; }
        .badge-Researcher { background: #0284c7; color: #fff; }
        .badge-Fact-Checker { background: #d97706; color: #fff; }
        .badge-Synthesizer { background: #16a34a; color: #fff; }
        .badge-System { background: #6366f1; color: #fff; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Live Multi-Agent Knowledge Synthesizer 🧠</h1>
            <p>Real-Time Vector RAG & Autonomous Agent Reasoning Telemetry</p>
        </div>
        
        <div class="search-box">
            <input type="text" id="queryInput" placeholder="Ask a question..." value="SOWMYA" />
            <button onclick="runAgents()">Run Agents</button>
        </div>

        <div class="card">
            <div class="card-header">Live Telemetry & Synthesis</div>
            <div id="logs">
                <div class="log-entry" style="border-left-color: #64748b; color: #94a3b8;">
                    Enter a prompt above and click <strong>Run Agents</strong> to observe real-time multi-agent reasoning.
                </div>
            </div>
        </div>
    </div>

    <script>
        let ws;
        function runAgents() {
            const query = document.getElementById('queryInput').value;
            const logsDiv = document.getElementById('logs');
            logsDiv.innerHTML = ''; 

            if (ws) { ws.close(); }

            ws = new WebSocket("ws://localhost:8000/ws/agent");

            ws.onopen = function() { ws.send(query); };

            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                const entry = document.createElement('div');
                entry.className = "log-entry";
                
                let borderColor = "#38bdf8";
                if (data.agent === "Router") borderColor = "#94a3b8";
                if (data.agent === "Researcher") borderColor = "#38bdf8";
                if (data.agent === "Fact-Checker") borderColor = "#f59e0b";
                if (data.agent === "Synthesizer") borderColor = "#22c55e";
                if (data.agent === "System") borderColor = "#818cf8";
                
                entry.style.borderLeftColor = borderColor;
                entry.innerHTML = `<span class="badge badge-${data.agent}">${data.agent}</span> ${data.status.replace(/\\n/g, '<br>')}`;
                
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
        print("Client disconnected cleanly.")