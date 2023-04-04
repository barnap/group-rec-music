FROM python:3.11.2
RUN mkdir /app
RUN git clone https://github.com/barnap/group-rec-music.git /app/group-rec-music
WORKDIR /app/group-rec-music
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /app
CMD python -m group_rec_music.webapp.main
EXPOSE 5000