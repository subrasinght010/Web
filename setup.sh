#!/bin/bash

# Create main project folder
mkdir -p Web/{routes,templates,static,logs,migrations}

# Create empty Python files
touch Web/{app.py,config.py,models.py,utils.py,requirements.txt,Dockerfile}
touch Web/routes/{auth.py,tasks.py}
touch Web/templates/index.html
touch Web/static/styles.css
touch Web/logs/app.log

# Make setup script executable
chmod +x Web/*.sh

echo "✅ Project structure created successfully!"
