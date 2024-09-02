FROM python:3.10

COPY ./requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./src ./src
WORKDIR /src
EXPOSE 8000
CMD ["fastapi", "run", "main.py", "--port", "8000"]