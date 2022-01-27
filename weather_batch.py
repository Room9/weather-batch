import json
import time
import pymysql
import datetime
import asyncio
from urllib.request import urlopen

class weather_batch():
    def get_db_connection(self):
        host = ''
        port = 3306
        db_name = 'mealgen'
        self.conn = pymysql.connect(host=host, port=int(port), user='mealgen', password='', db='mealgen', charset='utf8')
        self.curs = self.conn.cursor()
    
    async def proc(self):
        data = self.get_coordinate()
        weathers = [asyncio.ensure_future(self.get_weather(d)) for d in data]
        r = await asyncio.gather(*weathers)
        return r

    def get_coordinate(self):
        q = "SELECT NX, NY FROM WEATHER_INFO GROUP BY NX, NY"
        self.curs.execute(q)
        result = self.curs.fetchall()
        return result

    async def get_weather(self, cdn):
        now = datetime.datetime.now()
        hour = now.hour

        if now.minute < 42:
            hour -= 1

        base_time = str(hour) + '30'
        base_time = base_time.zfill(4)

        base_date = now.strftime("%Y%m%d")

        # API key
        service_key = ''

        dataType = 'json'

        nx = cdn[0]
        ny = cdn[1]
        
        api_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst?serviceKey={}' \
              '&numOfRows=31&pageNo=1&base_date={}&base_time={}&nx={}&ny={}&dataType={}'.format(
        service_key, base_date, base_time, nx, ny, dataType)

        response = await loop.run_in_executor(None, urlopen, api_url)
        data = response.read().decode('utf8')

        json_data = json.loads(data)
        
        tag_li = ['TM6001','TM6002','TM6003','TM6004','TM6009','TM6013']
        PTY = json_data['response']['body']['items']['item'][6]['fcstValue']
        SKY = json_data['response']['body']['items']['item'][18]['fcstValue']
        HUMIDITY = int(json_data['response']['body']['items']['item'][30]['fcstValue'])
        TEMP = int(json_data['response']['body']['items']['item'][24]['fcstValue'])
        
        if PTY in ['1','2','4','5','6']:
            tag_code = tag_li[0]

        elif PTY in ['3','7'] :
            tag_code = tag_li[3]
        
        elif PTY=='0'and SKY =='4':
            tag_code = tag_li[5]
            
        elif PTY =='0' :
            if HUMIDITY > 70 and TEMP > 30 :
                tag_code = tag_li[4]
            elif TEMP>30 :
                tag_code = tag_li[1]
            elif TEMP<30 :
                tag_code = tag_li[2]
            else :
                tag_code = tag_li[0]
            
        tag_tuple=(tag_code,nx,ny)

        return tag_tuple
    
    def update_tag(self, data):
        q_update = "UPDATE WEATHER_INFO SET TAG_CODE=%s WHERE NX=%s AND NY=%s"
        self.curs.executemany(q_update, data)
        self.conn.commit()
                
if __name__ == "__main__":
    start = time.time()
    
    t = weather_batch()
    t.get_db_connection()
    
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    
    r = loop.run_until_complete(t.proc())
    loop.close()
    t.update_tag(r)
    
    print(time.time()-start)
