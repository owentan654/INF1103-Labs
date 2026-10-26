FROM python:3.11-slim
WORKDIR /app
COPY ["OOP_auditor.py", "."]
CMD ["python", "OOP_auditor.py"]