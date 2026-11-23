from python:3.12-slim
workdir /app
copy  requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
copy app.py .
expose 5000
CMD ["python","app.py"]

