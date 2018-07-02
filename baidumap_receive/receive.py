"""
MIT License

Copyright (c) 2018 Liu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import json
import urllib.request

import serial
import math


def baidu_geocode(address, region):
    search = urllib.parse.quote(address.encode('utf-8'))
    region = urllib.parse.quote(region.encode('utf-8'))
    url = "http://api.map.baidu.com/place/v2/search?query=%s&region=" \
          "%s&city_limit=true&output=json&ak=你的ak" % (search, region)

    req = urllib.request.urlopen(url)  # JSON格式的返回数据
    res = req.read().decode("utf-8")  # 将其他编码的字符串解码成unicode
    temp = json.loads(res)
    print(temp)
    address = temp['results'][0]['address']  # 地址
    location = temp['results'][0]['location']  # 经纬度坐标
    print(address, location)
    lat = str(location['lat'])  # 纬度坐标
    lng = str(location['lng'])  # 经度坐标
    print(lng)
    print(lat)


def baidu_direct(address_o, address_d, region='成都', mode='walking'):
    #baidu_geocode(address_o, region)
    #baidu_geocode(address_d, region)

    origin = urllib.parse.quote(address_o.encode('utf-8'))
    destination = urllib.parse.quote(address_d.encode('utf-8'))
    region = urllib.parse.quote(region.encode('utf-8'))
    mode = urllib.parse.quote(mode.encode('utf-8'))

    url = "http://api.map.baidu.com/direction/v1?mode=%s&origin=%s&" \
          "destination=%s&region=%s&output=json&ak=你的ak" % (mode, origin, destination, region)
    req = urllib.request.urlopen(url)  # JSON格式的返回数据
    res = req.read().decode("utf-8")  # 将其他编码的字符串解码成unicode
    temp = json.loads(res)
    return temp


def longitudeToBaiduFormat(longitude):
    longitude_temp = float(longitude) * 100000
    #print(longitude_temp)
    long_dd_int = math.floor(longitude_temp / 10000000)
    #print(long_dd_int)
    long_mm_int = longitude_temp % 10000000
    #print(long_mm_int)
    longitude_float = long_dd_int + float(long_mm_int/ 60 / 100000)

    #longitude_round_off = ("%.5f" % longitude_float)
    return longitude_float


def latitudeToBaiduFormat(latitude):
    latitude_temp = float(latitude) * 100000
    #print(longitude_temp)
    lati_dd_int = math.floor(latitude_temp / 10000000)
    #print(long_dd_int)
    lati_mm_int = latitude_temp % 10000000
    #print(long_mm_int)
    latitude_float = lati_dd_int + float(lati_mm_int/ 60 / 100000)

    #latitude_round_off = ("%.5f" % latitude_float)
    return latitude_float


def main():
    serial_port = '/dev/ttyACM0'
    baud_rate = 115200
    ser = serial.Serial(serial_port, baud_rate)
    word_list = []
    while True:
        result_json = baidu_direct('电子科技大学清水河校区', '龙湖时代天街')
        if result_json['status'] != 240:
            #with open("./route.json", 'w', encoding='utf-8') as json_file:
             #   json.dump(result_json, json_file, ensure_ascii=False)
            for i in range(len(result_json['result']['routes'][0]['steps'])):
                result = result_json['result']['routes'][0]['steps'][i]['instructions'].replace('<', ' ')
                result1 = result.replace('>', ' ')
                result2 = result1.replace('b', ' ')
                result3 = result2.replace('/', ' ')
                result_list = list(result3)
                for i in range(result_list.count(' ')):
                    result_list.remove(' ')
                result_str = ''.join(result_list)
                #print(result_json['result']['routes'][0]['steps'][i]['instructions'])
                print(result_str)
            break
        else:
            print('waiting for response...')


    # result = baidumap_obj.geocode(location='116.43213,38.76623')

    #print(result_direction)

    #while True:
    #    line = ser.readline()
    #    line_string = line.decode('utf-8')
    #    word_list = line_string.split(",")

    #    if (word_list[0] == '$GNRMC'):
    #        longitude_baidu = longitudeToBaiduFormat(word_list[5])
    #        latitude_baidu = latitudeToBaiduFormat(word_list[3])

    #        location = str(longitude_baidu) + ',' + str(latitude_baidu)
     #       result = baidumap_obj.geocode(location=location)
            # print(result)


if __name__ == '__main__':
  main()


