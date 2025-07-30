#!/bin/bash
echo "Starting EduTrack with gunicorn..."
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120 