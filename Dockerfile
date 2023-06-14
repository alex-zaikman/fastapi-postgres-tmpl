FROM python:3.10
WORKDIR /
ENV PORT=8000
EXPOSE ${PORT}
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./src ./
CMD ["sh", "-c",  "uvicorn api:app --host 0.0.0.0 --port ${PORT}  --log-config logger.json --reload --log-level info"]