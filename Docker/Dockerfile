FROM python:3.11.2
RUN mkdir /app
WORKDIR /app
# RUN mkdir /app/group-rec-music
RUN git clone https://github.com/barnap/group-rec-music.git
WORKDIR /app/group-rec-music
RUN pip install --no-cache-dir -r requirements.txt
CMD python -m dao.db_initialization
CMD python -m webapp.main
EXPOSE 5000