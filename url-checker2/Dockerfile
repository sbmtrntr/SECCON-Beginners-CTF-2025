FROM python:3.13-alpine

RUN apk --no-cache add file socat
RUN adduser -D ctf

ADD main.py /home/ctf/url-checker2/main.py
RUN chmod 500 /home/ctf/url-checker2/main.py
RUN chown ctf:root /home/ctf -R

USER ctf
WORKDIR /home/ctf/url-checker2/
CMD socat TCP-L:33458,fork,reuseaddr EXEC:"python3 -u main.py",stderr