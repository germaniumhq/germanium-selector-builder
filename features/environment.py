from socketserver import ThreadingTCPServer
from threading import Thread

from germanium.static import *

from features.PostHTTPRequestHandler import PostHttpRequestHandler


def before_all(context):
    ThreadingTCPServer.allow_reuse_address = True
    Handler = PostHttpRequestHandler
    context._httpServer = ThreadingTCPServer(("0.0.0.0", 8000), Handler)

    print("started server on 0.0.0.0:8000")

    t = Thread(target=context._httpServer.serve_forever)
    t.start()

    open_browser("chrome")


def after_all(context):
    close_browser()

    print("Shutting down HTTP server")
    context._httpServer.shutdown()

    print("Done shutting down HTTP server")
