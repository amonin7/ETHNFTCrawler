FROM python:3.9
ADD . .
RUN pip install requests -r requirements.txt
CMD ["python", "./main.py"]
