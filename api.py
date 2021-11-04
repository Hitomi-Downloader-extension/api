# coding: utf8
# title: API
# comment: Expose some APIs locally for extended functions
# author: SaidBySolo

import threading
import http.server
import json
from http.server import BaseHTTPRequestHandler
from typing import Any, Callable, Dict, List, Optional, Set

from requests.cookies import RequestsCookieJar
import cooker  # type: ignore

__version__ = "0.1.0"

# Type annotations


class MainWindow:
    def close(self):
        ...


class ListWidget:
    def item(self, index: int) -> Any:
        ...

    def count(self) -> int:
        ...


class UI:
    listWidget: ListWidget


isValidURL: Callable[[str], Set[str]]
downButton: Callable[[str], Any]
mainWindow: MainWindow
ui: UI


class App:
    def __init__(self) -> None:
        self.handlers: List[Dict[str, Any]] = []

    # Register handlers
    def register(self, path: str, method: str):
        """
        Register handler for path and method
        """

        def wrapper(handler: Callable[["RequestHandler", Dict[str, Any]], Any]):
            self.handlers.append({"path": path, "handler": handler, "method": method})
            return handler

        return wrapper

    def get(self, path: str):
        """
        Register handler for GET method
        """

        def wrapper(handler: Callable[["RequestHandler"], Any]):
            self.handlers.append({"path": path, "handler": handler, "method": "GET"})
            return handler

        return wrapper

    def post(self, path: str):
        """
        Register handler for POST method
        """

        def wrapper(handler: Callable[["RequestHandler", Dict[str, Any]], Any]):
            self.handlers.append({"path": path, "handler": handler, "method": "POST"})
            return handler

        return wrapper

    def handle(self, req_handler: "RequestHandler", method: str) -> Any:
        """
        Handle request
        """
        for handler in self.handlers:
            if handler["path"] == req_handler.path and handler["method"] == method:
                if method == "POST":
                    content_length = int(req_handler.headers["Content-Length"])
                    raw_data = req_handler.rfile.read(content_length)

                    # When can't parse json, return 400
                    try:
                        data = json.loads(raw_data)
                    except json.JSONDecodeError:
                        return req_handler.bad_request()

                    return handler["handler"](req_handler, data)

                return handler["handler"](req_handler)

        else:
            return req_handler.not_found()


# Handler
app = App()


@app.get("/ping")
def ping(req_handler: "RequestHandler") -> Any:
    """
    This endpoint is used to check if the server is running.
    """
    return req_handler.ok()


@app.get("/list")
def download_list(req_handler: "RequestHandler") -> Any:
    items_all = [ui.listWidget.item(i) for i in range(ui.listWidget.count())]
    datas: List[Any] = []
    for item in items_all[::-1]:
        cw = item
        if not cw._lazy:
            cw.updateLazy()
        if not cw.alive or getattr(cw, "pc", None) is not None:
            continue
        # TODO: Need handle isGroup
        data = item.serialize(dumps=False, compat=True)
        data.pop("str_pixmap")
        datas.append(data)

    return req_handler.ok({"list": datas})


@app.post("/valid_url")
def valied_url(req: "RequestHandler", data: Dict[str, Any]):
    """
    This endpoint checks if the url is valid for Hitomi Downloader and returns the type if it is valid.
    """
    gal_num = data.get("gal_num")
    if not gal_num:
        return req.bad_request()

    valied = isValidURL(str(gal_num))

    if not valied:
        return req.bad_request({"error": "not_valied"})

    return req.ok({"type": list(valied)})


@app.post("/download")
def download(req: "RequestHandler", data: Dict[str, Any]):
    """
    This endpoint requests a download from Hitomi Downloader.
    """
    gal_num = data.get("gal_num")
    if not gal_num:
        return req.bad_request()

    downButton(str(gal_num))

    return req.ok()


@app.post("/cookie")
def get_cookie(req: "RequestHandler", data: Dict[str, Any]) -> Any:
    """
    This endpoint loads the received cookie value into Hitomi Downloader.

    {
        "cookies": [
            {
                "name": "value",
                "value": "value",
                "domain": "value",
                "expires": 0
            }
        ]
    }
    """

    cookie_infos: Optional[List[Dict[str, Any]]] = data.get("cookies")
    if not cookie_infos:
        return req.bad_request()

    cookie_jar = RequestsCookieJar()
    for cookie in cookie_infos:
        if (
            not cookie.get("domain")
            or not cookie.get("name")
            or not cookie.get("value")
        ):
            return req.bad_request(
                {"error": "['domain', 'name', 'value'] is required arguments"}
            )
        cookie_jar.set(**cookie)  # type: ignore

    cooker.load(cookie_jar)  # type: ignore
    return req.ok()


class RequestHandler(BaseHTTPRequestHandler):
    def _to_bytes(self, data: Dict[str, Any]) -> bytes:
        return json.dumps(data).encode("utf-8")

    def set_response(self, data: Dict[str, Any]):
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(self._to_bytes(data))

    def ok(self, data: Dict[str, Any] = {"status": "ok"}):
        """
        Send 200 OK
        """
        self.send_response(200, "OK")
        self.set_response(data)

    def not_found(self, data: Dict[str, Any] = {"error": "not_found"}):
        """
        Send 404 Not Found
        """
        self.send_response(404, "Not Found")
        self.set_response(data)

    def bad_request(self, data: Dict[str, Any] = {"error": "bad_request"}):
        """
        Send 400 Bad Request
        """
        self.send_response(400, "Bad Request")
        self.set_response(data)

    def do_GET(self):
        """
        Handle GET request
        """
        try:
            return app.handle(self, "GET")
        except Exception:
            self.send_response(500, "Internal Server Error")
            self.set_response({"error": "internal_server_error"})

    def do_POST(self):
        """
        Handle POST request
        """
        try:
            return app.handle(self, "POST")
        except Exception:
            self.send_response(500, "Internal Server Error")
            self.set_response({"error": "internal_server_error"})


def entrypoint():
    """
    Entrypoint

    This function is called when the program is started.
    """
    origin_close = mainWindow.close

    def patched_close():
        server.shutdown()
        server.server_close()
        origin_close()

    mainWindow.close = patched_close
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 6009), RequestHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()


entrypoint()
