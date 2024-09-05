import asyncio
from pathlib import Path

from fastapi import FastAPI, WebSocket, websockets
from fastapi.responses import HTMLResponse

from model.body import HumanBody

app = FastAPI()

@app.get("/")
async def get():
    html_content = Path("app.html").read_text()
    return HTMLResponse(html_content)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    model = HumanBody()

    async def send_updates():
        while True:
            try:
                dt = model.step()
                metrics = model.get_metrics()
                await websocket.send_json(metrics)
                await asyncio.sleep(dt)
            except asyncio.CancelledError:
                break
            except websockets.WebSocketDisconnect:
                break

    update_task = asyncio.create_task(send_updates())
    try:
        while True:
            data = await websocket.receive_json()
            if data['action'] == 'start_exercise':
                model.start_exercise()
            elif data['action'] == 'stop_exercise':
                model.stop_exercise()
            elif data['action'] == 'drink':
                model.drink(data['amount'])
            elif data['action'] == 'eat':
                model.eat(data['amount'])
            elif data['action'] == 'pee':
                model.pee()
    finally:
        update_task.cancel()
        await asyncio.wait_for(update_task, timeout=1.0)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
