"""Networking helper for Sword Adventure.

LAN on desktop -> normal TCP.
Online -> WebSocket (desktop or pygbag/browser).
"""

import asyncio
import sys


class _BrowserReader:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.closed = False

    async def readline(self):
        while True:
            if not self.queue.empty():
                item = self.queue.get_nowait()
                if item is None:
                    return b""
                return (item + "\n").encode("utf-8")
            if self.closed:
                return b""
            await asyncio.sleep(0)

    def feed(self, text):
        self.queue.put_nowait(str(text))

    def close(self):
        if not self.closed:
            self.closed = True
            self.queue.put_nowait(None)


class _BrowserWriter:
    def __init__(self, websocket, reader, callbacks):
        self.websocket = websocket
        self.reader = reader
        self.callbacks = callbacks
        self.closed = False

    def write(self, data):
        if self.closed:
            return
        text = data.decode("utf-8", errors="ignore") if isinstance(data, bytes) else str(data)
        text = text.rstrip("\r\n")
        if text:
            self.websocket.send(text)

    async def drain(self):
        await asyncio.sleep(0)

    def close(self):
        if self.closed:
            return
        self.closed = True
        try:
            self.websocket.close()
        except Exception:
            pass
        self.reader.close()

    async def wait_closed(self):
        while not self.closed and not self.reader.closed:
            await asyncio.sleep(0)


class _DesktopWSReader:
    def __init__(self, websocket):
        self.websocket = websocket

    async def readline(self):
        try:
            msg = await self.websocket.recv()
        except Exception:
            return b""
        if msg is None:
            return b""
        return (str(msg) + "\n").encode("utf-8")


class _DesktopWSWriter:
    def __init__(self, websocket):
        self.websocket = websocket
        self.pending = []
        self.closed = False

    def write(self, data):
        if self.closed:
            return
        text = data.decode("utf-8", errors="ignore") if isinstance(data, bytes) else str(data)
        text = text.rstrip("\r\n")
        if text:
            self.pending.append(text)

    async def drain(self):
        while self.pending:
            await self.websocket.send(self.pending.pop(0))

    def close(self):
        self.closed = True

    async def wait_closed(self):
        try:
            await self.websocket.close()
        except Exception:
            pass


async def _browser_websocket_connection(url):
    import platform

    ws = platform.window.WebSocket.new(url)
    reader = _BrowserReader()
    state = {"opened": False, "failed": False}

    def on_open(event):
        state["opened"] = True

    def on_message(event):
        reader.feed(str(event.data))

    def on_error(event):
        state["failed"] = True

    def on_close(event):
        reader.close()

    ws.onopen = on_open
    ws.onmessage = on_message
    ws.onerror = on_error
    ws.onclose = on_close

    callbacks = (on_open, on_message, on_error, on_close)

    frames = 0
    while not state["opened"]:
        if state["failed"] or reader.closed:
            raise ConnectionError("Could not connect to online server")
        frames += 1
        if frames > 600:
            try:
                ws.close()
            except Exception:
                pass
            raise TimeoutError("Online server connection timed out")
        await asyncio.sleep(0)

    return reader, _BrowserWriter(ws, reader, callbacks)


async def open_game_connection(host, port=5050):
    host = str(host).strip()
    is_websocket = host.startswith(("ws://", "wss://"))

    if sys.platform == "emscripten":
        if not is_websocket:
            raise ConnectionError(
                "LAN TCP is not available from the browser build. Use Online Multiplayer instead."
            )
        return await _browser_websocket_connection(host)

    if is_websocket:
        import websockets
        ws = await websockets.connect(host, ping_interval=20, ping_timeout=20)
        return _DesktopWSReader(ws), _DesktopWSWriter(ws)

    return await asyncio.open_connection(host, port)
