FROM python:3.8.10
WORKDIR /usr/src/app
COPY requirements.txt .
ADD src/ ./src
ADD  pyproject.toml .
RUN pip install .
CMD ['SPLcli']