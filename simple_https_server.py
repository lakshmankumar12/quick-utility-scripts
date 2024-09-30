import http.server
import socketserver
import ssl
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", default="./", help="dir to serve")
    parser.add_argument("-c", "--cert", help="certfile", required=True)
    parser.add_argument("-k", "--key", help="keyfile", required=True)
    parser.add_argument("port", help="port", type=int, nargs="?", default=8443)
    cmd_options = parser.parse_args()
    return cmd_options

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, dirtoserve):
        self.dirtoserve = dirtoserve

    def __call__(self, *args, **kwargs):
        h = MyHandler(self.dirtoserve)
        http.server.SimpleHTTPRequestHandler.__init__(h, *args, directory=self.dirtoserve, **kwargs)

def serve_forever(opts):

    # Create an SSL context
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile=opts.cert, keyfile=opts.key)

    # Create the HTTPS server
    h = MyHandler(opts.dir)
    with socketserver.TCPServer(("0.0.0.0", opts.port), h) as httpd:
        httpd.dirtoserve = opts.dir
        httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)
        print(f"Serving directory at https://localhost:{opts.port}")
        httpd.serve_forever()


def main():
    opts = parse_args()
    serve_forever(opts)

if __name__ == "__main__":
    main()
