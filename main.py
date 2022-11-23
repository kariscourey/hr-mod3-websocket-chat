from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse


app = FastAPI()


@app.get("/")
def homepage():
    with open("index.html") as f:
        return HTMLResponse(f.read())

connections = []
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for connection in connections:
                await connection.send_text(data)
    except WebSocketDisconnect:
        connections.remove(websocket)
