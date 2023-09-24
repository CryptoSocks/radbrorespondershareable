FROM python:3.11

ADD constants.py .
ADD radbroresponderv2.py .
ADD tweeter.py .
ADD /pics /pics

RUN pip install requests tweepy regex

CMD ["stdbuf", "-oL", "python", "./radbroresponderv2.py" ]