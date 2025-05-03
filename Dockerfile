FROM python:3.9-slim
WORKDIR /app

# 先复制依赖文件
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 再复制整个app目录
COPY app/ .

CMD ["python", "app.py"]