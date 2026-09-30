"""Serve generated output only, on loopback beneath /od-guides/."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import socket

ROOT = Path(__file__).resolve().parent


class LoopbackServer(ThreadingHTTPServer):
    allow_reuse_address = False

    def server_bind(self):
        # Windows SO_REUSEADDR can otherwise bind a port owned by another preview.
        if hasattr(socket, 'SO_EXCLUSIVEADDRUSE'):
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        super().server_bind()


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if not self.path.startswith('/od-guides/'):
            self.send_error(404)
            return
        super().do_GET()

    def do_HEAD(self):
        if not self.path.startswith('/od-guides/'):
            self.send_error(404)
            return
        super().do_HEAD()

    def list_directory(self, path):
        self.send_error(404)
        return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8765, help='Preferred port; use a free one if occupied')
    args = parser.parse_args()
    www = ROOT / '.build' / 'www'
    if not (www / 'od-guides' / 'index.html').is_file():
        raise SystemExit('Build first: python build.py --build')
    handler = partial(Handler, directory=str(www))
    try:
        server = LoopbackServer(('127.0.0.1', args.port), handler)
    except OSError:
        server = LoopbackServer(('127.0.0.1', 0), handler)
    url = f'http://127.0.0.1:{server.server_port}/od-guides/'
    (ROOT / '.build' / 'server.json').write_text(json.dumps({'pid': os.getpid(), 'url': url, 'bind': '127.0.0.1'}, indent=2), encoding='utf-8')
    print(url, flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
