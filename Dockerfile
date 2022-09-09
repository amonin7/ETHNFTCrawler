FROM python:3.9
ADD . .

ARG API_KEY
ENV apikey=$API_KEY
ARG START_BLOCK
ENV start_block=$START_BLOCK

RUN pip install requests -r requirements.txt
CMD ["python", "./main.py"]
