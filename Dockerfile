# InfraGuardian Production Container Image
# Updated: 01/11/26
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install --no-cache-dir .

ENTRYPOINT ["infraguardian"]
CMD ["--help"]