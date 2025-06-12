#!/bin/bash

# Add all changes
git add .

# Commit with descriptive message
git commit -m "Update: Implement modern PyQt6-based GUI
- Replace tkinter with PyQt6
- Add user authentication UI
- Add video processing features
- Add dark theme and modern styling
- Add batch processing support
- Add progress tracking
- Add file dialogs and error handling"

# Update version tag
git tag -f v1.1.0

# Push changes and tag
git push origin main
git push -f origin v1.1.0
