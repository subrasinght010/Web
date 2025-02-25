#!/bin/bash

# Create main project folder
mkdir -p flask-task-manager/{routes,templates,static,logs,migrations}

# Create empty Python files
touch flask-task-manager/{app.py,config.py,models.py,utils.py,requirements.txt,Dockerfile}
touch flask-task-manager/routes/{auth.py,tasks.py}
touch flask-task-manager/templates/index.html
touch flask-task-manager/static/styles.css
touch flask-task-manager/logs/app.log

# Make setup script executable
chmod +x flask-task-manager/*.sh

echo "✅ Project structure created successfully!"
