docker run --rm --name flask -it -v "C:\Users\francesco.roccabruna\flaskr:/app" -p 5000:5000  -w /app python:3.12 bash -c "pip install flask cryptography sqlalchemy pymysql && bash start.sh"
