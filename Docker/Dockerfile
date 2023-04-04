FROM python:3.11.2
RUN mkdir /app
RUN git clone https://github.com/barnap/group-rec-music.git /app/group-rec-music
WORKDIR /app/group-rec-music
RUN pip install --no-cache-dir -r requirements.txt
CMD python -m webapp.main
EXPOSE 5000