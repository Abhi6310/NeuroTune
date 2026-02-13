const WS_BASE = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000";

export class SessionWebSocket {
  private ws: WebSocket | null = null;
  private onMessage: ((data: Record<string, unknown>) => void) | null = null;

  connect(sessionId: number, onMessage: (data: Record<string, unknown>) => void): void {
    this.onMessage = onMessage;
    this.ws = new WebSocket(`${WS_BASE}/sessions/ws/${sessionId}`);

    this.ws.onopen = () => console.log("WS connected");
    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (this.onMessage) this.onMessage(data);
    };
    this.ws.onerror = (err) => console.error("WS error:", err);
    this.ws.onclose = () => console.log("WS closed");
  }

  send(data: Record<string, unknown>): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  disconnect(): void {
    this.ws?.close();
    this.ws = null;
  }
}
