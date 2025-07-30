from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Debug: log the request path
        print(f"Request path: {self.path}")
        
        if self.path == '/' or self.path == '/index.html':
            response = {"message": "EduTrack is running!", "status": "success", "endpoint": "root"}
        elif self.path == '/health':
            response = {"status": "healthy", "message": "EduTrack is running!", "endpoint": "health"}
        elif self.path == '/test':
            response = {"status": "success", "message": "Test endpoint working!", "endpoint": "test"}
        elif self.path.startswith('/api/'):
            response = {"status": "success", "message": "API endpoint reached", "path": self.path, "endpoint": "api"}
        else:
            response = {"status": "error", "message": "Route not found", "path": self.path, "endpoint": "unknown"}
        
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        self.do_GET()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
