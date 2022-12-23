FROM python:3.8-slim


RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean \
&& apt-get install -y build-essential

RUN apt-get install -y \
    libx11-6 \
    libgl1 \
    libxext6 \
    libxrender1 \
    libsm6 \
    libglib2.0-0


RUN pip install --no-cache-dir -U 'ray[default]'

RUN mkdir /app
WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

RUN python -m pip install --trusted-host dl.fbaipublicfiles.com detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu102/torch1.9/index.html

ENV PYTHONUNBUFFERED 1
EXPOSE 8000
CMD ["bash","run.sh"]
