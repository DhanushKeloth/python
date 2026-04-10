let ws =new WebSocket("ws://localhost:8000/ws");
ws.onmessage = (event) => {
    let data = JSON.parse(event.data);
    console.log(event)
    console.log(data);
};
