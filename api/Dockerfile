FROM python:3.8.10

WORKDIR /app

RUN apt update && apt install -y ffmpeg
RUN pip install yt-dlp

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8888
CMD ["make", "dev"]
