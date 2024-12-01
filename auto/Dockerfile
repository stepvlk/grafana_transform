FROM docker.nexign.com/ubi8/python-311

USER 0
RUN mkdir -p /data && chmod 777 /data
COPY ./templates/alerts.html /data/alerts.html
RUN chmod 777 /data/alerts.html
WORKDIR /app
COPY . /app
RUN chmod -R 777 /app
#RUN chown -R 1001:0 /app
RUN python3 --version
COPY ./pip.conf /etc/pip.conf
COPY ./req.txt /app/requirements.txt

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
USER 1001
#COPY --chown=1001:root . /app

EXPOSE 5000
CMD python3 alerting.py
LABEL org.opencontainers.image.authors="Andrey.Stepankin"

#sudo docker image build -f auto/Dockerfile -t alerting:1.0.0 . --network=host