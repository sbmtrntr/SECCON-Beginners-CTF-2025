FROM python:3.13-alpine

RUN apk --no-cache add file socat
RUN adduser -D ctf

ADD main.py /home/ctf/url-checker/main.py
RUN chmod 500 /home/ctf/url-checker/main.py
RUN chown ctf:root /home/ctf -R

USER ctf
WORKDIR /home/ctf/url-checker/
CMD socat TCP-L:33457,fork,reuseaddr EXEC:"python3 -u main.py",stderr