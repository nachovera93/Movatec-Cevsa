FROM rasa/rasa:2.8.12
WORKDIR  '/app'
COPY . /app
USER root

COPY ./data /app/data
RUN rasa train
VOLUME /app
VOLUME /app/data
VOLUME /app/models
CMD ["run","-m","/app/models","--enable-api","--cors","*","--debug" ,"--endpoints", "endpoints.yml", "--log-file", "out.log"]
