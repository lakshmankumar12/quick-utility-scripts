'''

On client do:

curl -F 'file=@path/to/file' http://server:port


'''
import http.server
import socketserver
import os
import cgi
from urllib.parse import parse_qs

class FileUploadHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve a simple HTML form for file uploads
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            html = '''
            <html>
            <body>
                <h2>Upload File</h2>
                <form enctype="multipart/form-data" method="post">
                    <input type="file" name="file" required>
                    <input type="submit" value="Upload">
                </form>
            </body>
            </html>
            '''
            self.wfile.write(html.encode())
        else:
            super().do_GET()

    def do_POST(self):
        # Handle file upload
        content_type = self.headers.get('Content-Type')

        if content_type and 'multipart/form-data' in content_type:
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': content_type
                }
            )

            if 'file' in form:
                file_item = form['file']
                if file_item.filename:
                    # Save the file to uploads directory
                    os.makedirs('uploads', exist_ok=True)
                    file_path = os.path.join('uploads', file_item.filename)

                    with open(file_path, 'wb') as f:
                        f.write(file_item.file.read())

                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(f"File '{file_item.filename}' uploaded successfully!".encode())
                    return

        self.send_response(400)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Error uploading file")

def run_server(port=8000):
    with socketserver.TCPServer(("", port), FileUploadHandler) as httpd:
        print(f"Serving at http://0.0.0.0:{port}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
