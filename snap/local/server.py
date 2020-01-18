#!/usr/bin/python3

import http.server
import socketserver
import os
import html
import http.client
import io
import sys
import urllib.parse
import re

from http import HTTPStatus

base_folder = os.getenv('SNAP_USER_COMMON') if os.getenv("SNAP") else \
    os.path.join(os.path.dirname(__file__), "..", "..")
web_dir = os.path.join(base_folder, 'archive')
os.chdir(web_dir)
PORT = 8076


def LoopTemplate(s, ctx):
    """Minute templating language: use like str.format,
       so LoopTemplate("{one}", dict(one="1")) => "1",
       but also supports {loop people}{name}{endloop} which
       loops over an iterable in the context and processes the
       inside as a subtemplate with the next item in the iterable
       as its context."""
    def loophandler(m):
        print("loophandler", m)
        md = m.groupdict()
        return "".join([LoopTemplate(md["content"], val)
                        for val in ctx[md["var"]]])
    return re.sub(r"\{loop (?P<var>[^}]+)\}(?P<content>.*?)\{endloop\}",
                  loophandler, s, flags=re.DOTALL).format(**ctx)


SITES = """<!doctype html>
<html><head><meta charset="{enc}">
<title>Websites in your Personal Wayback Machine</title>
</head><body>
<h1>Websites in your Personal Wayback Machine</h1>
<ul>
{loop items}
    <li><a href="{link}">{display}</a></li>
{endloop}
</ul>
</body>
</html>"""

PAGES = """<!doctype html>
<html><head><meta charset="{enc}">
<title>Pages in your Personal Wayback Machine from site {site}</title>
</head><body>
<h1>Pages in your Personal Wayback Machine from site {site}</h1>
<ul>
{loop items}
    <li><a href="{link}">{display}</a></li>
{endloop}
</ul>
</body>
</html>"""

DATES = """<!doctype html>
<html><head><meta charset="{enc}">
<title>Pages in your Personal Wayback Machine from site {site} path {path}</title>
</head><body>
<h1>Pages in your Personal Wayback Machine from site {site} path {path}</h1>
<ul>
{loop items}
    <li><a href="{link}">{display}</a></li>
{endloop}
</ul>
</body>
</html>"""


class PWBMHandler(http.server.SimpleHTTPRequestHandler):
    def list_directory(self, path):
        """Helper to produce a directory listing (absent index.html).

        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().

        """
        try:
            items = os.listdir(path)
        except OSError:
            self.send_error(
                HTTPStatus.NOT_FOUND,
                "No permission to list directory")
            return None
        items.sort(key=lambda a: a.lower())
        nitems = []
        for name in items:
            fullname = os.path.join(path, name)
            if os.path.isdir(fullname):
                name = "{}/".format(name)
            nitems.append({
                "link": urllib.parse.quote(name, errors="surrogatepass"),
                "display": html.escape(name, quote=False)
            })

        try:
            displaypath = urllib.parse.unquote(self.path,
                                               errors='surrogatepass')
        except UnicodeDecodeError:
            displaypath = urllib.parse.unquote(path)
        displayparts = [html.escape(x, quote=False) for x in displaypath.split("/")]

        enc = sys.getfilesystemencoding()
        context = {"items": nitems, "enc": enc}
        if self.path == "/":
            r = LoopTemplate(SITES, {**context})
        elif self.path.count("/") == 2:
            r = LoopTemplate(PAGES, {"site": displayparts[1], **context})
        else:
            for item in context["items"]:
                item["display"] = "-".join(item["display"].split("-")[:3])
            r = LoopTemplate(DATES, {"site": displayparts[1],
                                     "path": displayparts[2].replace("__", "/"),
                                     **context})

        encoded = r.encode(enc, 'surrogateescape')
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return f

if __name__ == "__main__":
    Handler = PWBMHandler
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("", PORT), Handler)
    print("serving at port", PORT)
    httpd.serve_forever()
