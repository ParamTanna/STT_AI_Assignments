FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p ./models
COPY app.py .
COPY models/ ./models/
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]