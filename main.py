from app import app

# Vercel handler
if __name__ != "__main__":
    # For Vercel deployment
    handler = app

# For local development
if __name__ == "__main__":
    app.run(debug=True)
