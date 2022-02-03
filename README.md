# weather_batch
openAPI 이용한 전국 날씨 업데이트 배치

<!-- ABOUT THE PROJECT -->
## About The Project

![image](https://user-images.githubusercontent.com/79136484/152281209-15b88d64-5b8e-4172-9a37-0590f411d746.png)


기상청 open API 이용한 전국 날씨 현황 업데이트

- 전국 3500여개 행정동 기준 날씨 현황 호출
- Docker image 이용한 aws ecr 내 배포
- Cloud watch 내 cron tab 이용한 주기적인 trigger 설정
- python 비동기 적용한 속도 개선


### Built With

- python 3.9
- asyncio
- aurora mysql
- 기상청 open api(초단기예보)
