from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_json()
            # Handle received data
            # You can process the data here and send a response if needed
            await websocket.send_json({"message": str(data["message"])})
            
    except WebSocketDisconnect:
        print("WebSocket connection closed")