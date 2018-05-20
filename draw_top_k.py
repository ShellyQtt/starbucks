from find import findTopK ,findRange,findTopKWithKeyWord
import os
import pickle
import pandas as pd
from random import randint
import plotly.offline as py
from plotly.graph_objs import *
from PyQt5.QtCore import QUrl

mapbox_access_token = 'pk.eyJ1IjoibHNoaXl1ZSIsImEiOiJjamYyZW5raWYwbWF5MnpxN3Fva3Jxc2xmIn0.RdUrTcrSiCMA84-suzPgJg'

def drawTopkMap(file, lon, lat, topk, keyWord, data, fileName = "topk1.html", title = 'Top-k'):
    if keyWord == "":
        topKInfo = findTopK(file, lon, lat, topk)
    else:
        topKInfo = findTopKWithKeyWord(file, lon, lat, topk, keyWord, data)

    topKInfo = topKInfo.fillna('Not set')  # 将空值设为Not set
    topKInfo['info'] = "Store Number: " + topKInfo["Store Number"] + "</br></br>" \
                       + "Store Name: " + topKInfo["Store Name"] + "</br>" \
                       + "Street Address: " + topKInfo["Street Address"] + "</br>" \
                       + "Postcode: " + topKInfo["Postcode"] + "</br>" \
                       + "Phone Number: " + topKInfo["Phone Number"] + "</br>"


    data = []
    data.append(Scattermapbox(
        lat=topKInfo['Latitude'],
        lon=topKInfo['Longitude'],
        mode='markers',
        marker=Marker(size=10, color='green'),
        text=topKInfo['info'],
        textposition='top left',
        hoverinfo='text',
        name="topK点",
    ))

    data.append(Scattermapbox(
        lat=[lat],
        lon=[lon],
        mode='markers',
        marker=Marker(size=10, color='red'),
        text=["标记点</br></br>经度:%f  纬度: %f" % (lon, lat)],
        textposition='top left',
        hoverinfo='text',
        name="标记点",
    ))

    layout = Layout(
        title=title,
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            pitch=0, zoom=1),
    )

    fig = dict(data=data, layout=layout)
    py.plot(fig, filename=fileName, auto_open=False)

def drawRangeMap(file, lon, lat, range, fileName="rangeMap.html", title='Range'):
    rangeInfo = findRange(file, lon, lat, range)

    rangeInfo = rangeInfo.fillna('Not set')

    # 将数值强转成str,后续用于字符串拼接
    rangeInfo["Distance"] = [str(key) + "km" for key in rangeInfo["Distance"]]

    rangeInfo['info'] = "Store Number: " + rangeInfo["Store Number"] + "</br></br>" \
                        + "Store Name: " + rangeInfo["Store Name"] + "</br>" \
                        + "Street Address: " + rangeInfo["Street Address"] + "</br>" \
                        + "Postcode: " + rangeInfo["Postcode"] + "</br>" \
                        + "Phone Number: " + rangeInfo["Phone Number"] + "</br>" \
                        + "Distance: " + rangeInfo["Distance"] + "</br>"
    data = []
    data.append(Scattermapbox(
        lat=rangeInfo['Latitude'],
        lon=rangeInfo['Longitude'],
        mode='markers',
        marker=Marker(size=10, color='green'),
        text=rangeInfo['info'],
        textposition='top left',
        hoverinfo='text',
        name="距离标记点 < range的点",
    ))

    data.append(Scattermapbox(
        lat=[lat],
        lon=[lon],
        mode='markers',
        marker=Marker(size=10, color='red'),
        text=["标记点</br></br>经度:%f  纬度: %f 半径: %f" % (lon, lat, range)],
        textposition='top left',
        hoverinfo='text',
        name="标记点",
    ))

    layout = Layout(
        title=title,
        showlegend=True,
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            pitch=0, zoom=1),
    )

    fig = dict(data=data, layout=layout)
    py.plot(fig, filename=fileName, auto_open=False)