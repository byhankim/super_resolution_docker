FROM tensorflow/tensorflow:latest-gpu

RUN mkdir /workspace

WORKDIR /workspace
COPY . /workspace

RUN apt-get update
RUN apt-get install -y libgl1-mesa-dev
RUN pip3 PIL install flask PIL matplotlib keras numpy

# COPY . .


EXPOSE 80
# ENTRYPOINT ["python"]
# CMD ["server.py"]

CMD python3 server.py