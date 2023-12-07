FROM python:3.11.2
RUN mkdir /app
WORKDIR /app
RUN git clone https://github.com/barnap/group-rec-music.git
WORKDIR /app/group-rec-music
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000