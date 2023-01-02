FROM python:3.8.10

# create the work dirs and copy
# only the required files from the repo
WORKDIR /usr/src/app
COPY requirements.txt .
ADD src/ ./src
ADD  pyproject.toml .

# install the package-SPLcli locally
RUN pip install .

# add sample data for easy experimentation
RUN mkdir ./sample_data
COPY sample_data/ /usr/src/app/sample_data
RUN gzip -d /usr/src/app/sample_data/access.log.gz

# the tool needs to run interactively
# provide bash as the entry pointS
CMD ["bash"]