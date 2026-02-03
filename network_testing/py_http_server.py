from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import argparse

## to run a client to upload
##
## curl -k -X POST --data-binary @localfile.txt https://serverip:8000/remotename.txt

class UploadHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        filename = os.path.basename(self.path.strip('/')) or 'uploaded_file'
        with open(filename, 'wb') as f:
            remaining = length
            while remaining > 0:
                chunk_size = min(remaining, 1024 * 1024)
                f.write(self.rfile.read(chunk_size))
                remaining -= chunk_size
        self.send_response(200)
        self.end_headers()
        self.wfile.write(f'Saved: {filename}\n'.encode())

parser = argparse.ArgumentParser()
parser.add_argument('port', nargs='?', type=int, default=8000)
parser.add_argument('--ssl', metavar='cert,key', help='Enable HTTPS with cert.pem,key.pem')
args = parser.parse_args()

server = HTTPServer(('', args.port), UploadHandler)

if args.ssl:
    import ssl
    certfile, keyfile = args.ssl.split(',')
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile, keyfile)
    server.socket = context.wrap_socket(server.socket, server_side=True)
    proto = 'https'
else:
    proto = 'http'

print(f'Serving {proto} on port {args.port}...')
server.serve_forever()
