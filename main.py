import sys
import xbmcgui
import xbmcplugin
import requests
import json
import urlparse
import urllib

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'videos')


def build_url(query):
    return base_url + '?' + urllib.urlencode(query)


def vod_videos():
    
    url = 'https://tv.kakao.com/api/v1/ft/home/category/original'

    req = requests.get(url=url).json()
    respone = req["list"]
    
    VIDEOS = []
    VIDEO = dict()
    for i in respone:
                
        VIDEO["id"] = i["id"]
        VIDEO["title"] = i["displayTitle"]
        VIDEO["thumb"] = i["clip"]["thumbnailUrl"]

        url3 = 'https://tv.kakao.com/katz/v1/ft/cliplink/{}/readyNplay'.format(i["id"])
        load3 = {
            'player': 'monet_html5',
            'uuid': 'edb32a231df16d59a986069f343c015f',
            'profile': 'HIGH4'
            }

        req1 = requests.get(url=url3, params=load3).json()
        VIDEO["play"] = req1["videoLocation"]["url"]

        li = xbmcgui.ListItem(VIDEO["title"], iconImage=VIDEO["thumb"])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=VIDEO["play"], listitem=li, isFolder=False)
        VIDEOS.append(VIDEO)
    
    return VIDEOS


def live_videos():

    url1 = 'https://tv.kakao.com/api/v1/ft/home/livelinks'
    load1 = {
        'tab': 'all',
        'fields': 'ccuCount,isShowCcuCount,thumbnailUrl,channel,live',
        'sort': 'CcuCount',
        'size': '30'
        }

    req1 = requests.get(url=url1, params=load1).json()
    respone = req1["list"]
    
    LIVES = []
    LIVE = dict()
    LIVE["page"] = req1["hasMore"]
    for i in respone:
        
        LIVE["id"] = i["id"]
        LIVE["title"] = i["displayTitle"]
        LIVE["thumb"] = i["live"]["thumbnailUrl"]

        urllive = 'https://tv.kakao.com/katz/v1/ft/livelink/{}/readyNplay'.format(i["id"])
        load2 = {
            'player':'moment_html5',
            'profile': 'BASE',
            'contentType': 'HLS'   
        }
        req2 = requests.get(url=urllive, params=load2).json()
        LIVE["play"] = req2['videoLocation']['url']
        li = xbmcgui.ListItem(LIVE["title"], iconImage=LIVE["thumb"])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=LIVE["play"], listitem=li, isFolder=False)
    
        LIVES.append(LIVE)
        
    return LIVES

def folderlist(mode, foldername, name):
    url = build_url({'mode': mode, 'foldername': foldername})
    li = xbmcgui.ListItem(name, iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)


mode = args.get('mode', None)

if mode is None:
    folderlist('VOD', 'VOD', 'VOD')
    folderlist('LIVE', 'LIVE', 'LIVE')
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'VOD':
    foldername = args['foldername'][0]
    vod_videos()
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'LIVE':
    foldername = args['foldername'][0]
    live_videos()
    xbmcplugin.endOfDirectory(addon_handle)
