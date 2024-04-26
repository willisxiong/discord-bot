FROM --platform=amd64 python:3.12.3-slim-bookworm AS build
RUN mkdir /app
WORKDIR /app
COPY . ./app
RUN pip3 install -r ./app/requirements.txt
EXPOSE 80
CMD ["python3", "./app/app.py"]