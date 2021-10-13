


class WebSocketConnection {
  ws: WebSocket | null = null
  connected: boolean
  dispatch: any

  constructor() {
    this.ws = null;
    this.connected = false;
    this.dispatch = {};
  }

  connect(path: string) {
    let token = localStorage.getItem("token");
    if (!this.connected && token) {
      let host = process.env.REACT_APP_HOST
      let url = `${window.location.protocol === "https:" ? "wss://" : "ws://"}${host}/${path}`
      this.ws = new WebSocket(url, [`token=${token}`]);
      this.ws.onopen = () => {
        this.connected = true;
        console.log("OPEN");
      };
      this.ws.onmessage = (response) => {
        response = JSON.parse(response.data);
        let method = this.dispatch[response.type];
        if (method){
          method(response);
        }
      };
      this.ws.onclose = () => {
        console.log("Close!");
        this.connected = false;
      };
    }
  }

  close() {
    if (this.ws) {
      this.ws.close();
    }
  }
}


export default WebSocketConnection


