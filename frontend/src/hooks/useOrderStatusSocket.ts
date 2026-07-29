import { useEffect, useRef, useState } from "react";
import { useAuthStore } from "../store/authStore";

export function useOrderStatusSocket(onUpdate: (data: { order_number: string; status: string }) => void) {
  const accessToken = useAuthStore((s) => s.accessToken);
  const socketRef = useRef<WebSocket | null>(null);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    if (!accessToken) return;

    const wsUrl = `${import.meta.env.VITE_WS_BASE_URL}/orders/?token=${accessToken}`;
    const socket = new WebSocket(wsUrl);
    socketRef.current = socket;

    socket.onopen = () => setConnected(true);
    socket.onclose = () => setConnected(false);
    socket.onmessage = (event) => onUpdate(JSON.parse(event.data));

    // Basic reconnect — one of the gaps flagged back in Phase 14's kickoff.
    socket.onerror = () => socket.close();

    return () => socket.close();
  }, [accessToken]);

  return { connected };
}