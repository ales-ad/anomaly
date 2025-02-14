FROM public.ecr.aws/docker/library/python:3.12

WORKDIR /app

COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt

COPY ./ /app
RUN cd /app


CMD ["aerich", "upgrade"]
