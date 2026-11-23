#!/usr/bin/env python3
"""Small instrumented service fixture for infrastructure labs."""
import collections
import json
import os
import signal
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

COUNTS = collections.Counter()
LOCK = threading.Lock()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        route = self.path if self.path in ('/healthz','/readyz','/version','/metrics') else 'unmatched'
        status = 200 if route != 'unmatched' else 404
        with LOCK:
            COUNTS[(route,status)] += 1
        if route == '/metrics':
            with LOCK:
                rows = sorted(COUNTS.items())
            text = '# HELP demo_http_requests_total Requests handled by the lab service.\n# TYPE demo_http_requests_total counter\n'
            text += ''.join('demo_http_requests_total{route="%s",status="%s"} %s\n' % (path,code,count) for (path,code),count in rows)
            body = text.encode()
            content_type = 'text/plain; version=0.0.4; charset=utf-8'
        else:
            payload = ({'status':'ok'} if route in ('/healthz','/readyz') else
                       {'version':os.getenv('APP_VERSION','development')} if route=='/version' else
                       {'error':'not found'})
            body = json.dumps(payload).encode()
            content_type = 'application/json'
        self.send_response(status)
        self.send_header('Content-Type',content_type)
        self.send_header('Content-Length',str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    server = ThreadingHTTPServer((os.getenv('HOST','127.0.0.1'),int(os.getenv('PORT','8080'))),Handler)
    def shutdown(_signum,_frame):
        threading.Thread(target=server.shutdown,daemon=True).start()
    signal.signal(signal.SIGTERM,shutdown)
    signal.signal(signal.SIGINT,shutdown)
    try:
        server.serve_forever()
    finally:
        server.server_close()

if __name__=='__main__':
    main()
