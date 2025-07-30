from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return {'message': 'Hello from EduTrack! Flask is working!'}

@app.route('/test')
def test():
    return {'status': 'success', 'message': 'App is running!'}

@app.route('/health')
def health():
    return {'status': 'healthy', 'message': 'Server is up and running!'}

# Vercel handler
if __name__ != "__main__":
    # For Vercel deployment
    handler = app

# For local development
if __name__ == "__main__":
    app.run(debug=True)
