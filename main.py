from flask import Flask

# Create a minimal app for testing
app = Flask(__name__)

@app.route('/')
def hello():
    return {'message': 'Hello from EduTrack!'}

@app.route('/test')
def test():
    return {'status': 'success', 'message': 'App is running!'}

# Vercel handler
if __name__ != "__main__":
    # For Vercel deployment
    handler = app

# For local development
if __name__ == "__main__":
    app.run(debug=True)
