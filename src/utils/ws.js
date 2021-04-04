
class WebSocketConnection {
  constructor() {
    this.ws = null;
    this.connected = false;
    this.dispatch = {};
  }

  connect(path) {
    if (!this.connected) {
      let token = localStorage.getItem("token");
      //let url = ((window.location.protocol === "https:") ? "wss://" : "ws://") + window.location.host + path + "/?token=" + token;
      let url = ((window.location.protocol === "https:") ? "wss://" : "ws://") + 'localhost:8000/' + path + "?token=" + token;
      console.log(url)
      this.ws = new WebSocket(url);
      this.ws.onopen = () => {
        this.connected = true;
        console.log("OPEN");
      };
      this.ws.onmessage = (response) => {
        response = JSON.parse(response.data); 
        let method = this.dispatch['refresh_monitors'];
        method(response);
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

const ws = new WebSocketConnection()
export default ws;
