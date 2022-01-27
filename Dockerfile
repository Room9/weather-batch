FROM python:3.9
WORKDIR /usr/src/app 
COPY . .
RUN pip install -r requirements.txt
CMD ["weather.py"]

# 작업제출 할 때마다(docker container run할 때마다) 기본적으로 입력되는 명령어, 완전한 디폴트 명령어(CMD와 비교해서 이해하기)
ENTRYPOINT ["python"]