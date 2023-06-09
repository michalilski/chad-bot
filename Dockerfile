FROM python:3.9-slim
ENV PATH /usr/local/bin:$PATH

COPY . /chad-bot
WORKDIR /chad-bot
RUN pip install -r requirements.txt
CMD ["gradio", "app/main.py"]