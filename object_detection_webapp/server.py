# Main server application.
from http.server import SimpleHTTPRequestHandler, HTTPServer


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="app", **kwargs)

def main():
    print("Starting web-server on port 8080.")
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, Handler)
    httpd.serve_forever()

if __name__ == "__main__":
    main()
