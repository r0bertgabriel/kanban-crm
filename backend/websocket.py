from typing import Dict

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket
    
    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
    
    async def send_personal_message(self, message: dict, user_id: int):
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_json(message)
            except:
                pass
    
    async def broadcast(self, message: dict):
        """Envia mensagem para todos os conectados"""
        for connection in list(self.active_connections.values()):
            try:
                await connection.send_json(message)
            except:
                pass
    
    async def broadcast_to_vendedores(self, message: dict, vendedores_ids: list):
        """Envia mensagem apenas para vendedores específicos"""
        for vendedor_id in vendedores_ids:
            await self.send_personal_message(message, vendedor_id)

manager = ConnectionManager()
