from http.server import SimpleHTTPRequestHandler, HTTPServer

BLOCK_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Blocked</title>
    <style>
        body { text-align: center; font-family: Arial, sans-serif; margin-top: 100px; }
        h1 { color: red; }
    </style>
</head>
<body>
    <h1>This site is blocked!</h1>
    <p>Access to this site has been blocked by the network administrator.</p>
    
</body>
</html>
"""

class BlockPageHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(BLOCK_PAGE.encode())

def run_server():
    server_address = ("", 80)  # Run on localhost port 80
    httpd = HTTPServer(server_address, BlockPageHandler)
    print("Block page server running on http://127.0.0.1:80")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
