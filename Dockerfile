FROM python:3.8.10
WORKDIR /usr/src/app
COPY requirements.txt .
ADD src/ ./src
ADD  pyproject.toml .
RUN pip install .
RUN mkdir ./sample_data
COPY sample_data/ /usr/src/app/sample_data
RUN gzip -d /usr/src/app/sample_data/access.log.gz
CMD ["bash"]