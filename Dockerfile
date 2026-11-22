FROM python:3.12-alpine
WORKDIR /app
COPY app.py .
USER 10001:10001
ENV HOST=0.0.0.0 PORT=8080 PYTHONDONTWRITEBYTECODE=1
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/healthz', timeout=2).read()"]
CMD ["python", "app.py"]
