from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        if self.path == '/':
            response = {"message": "EduTrack is running!", "status": "success"}
        elif self.path == '/health':
            response = {"status": "healthy", "message": "EduTrack is running!"}
        elif self.path == '/test':
            response = {"status": "success", "message": "Test endpoint working!"}
        else:
            response = {"status": "error", "message": "Route not found", "path": self.path}
        
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        self.do_GET()
