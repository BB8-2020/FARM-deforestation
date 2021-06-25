FROM python:3.8

RUN useradd -ms /bin/bash user
USER user

WORKDIR /home/user

COPY . .

RUN pip install .

CMD ["bash"]
