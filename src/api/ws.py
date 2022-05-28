from src.apps.news_feed.web_socket import WsManager

ws_manager = WsManager()


async def start_ws_consume():
    await ws_manager.setup()
