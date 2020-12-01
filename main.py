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

def page(b):
    a = b + 1
    return a



def build_url(query):
    return base_url + '?' + urllib.urlencode(query)


def vod_videos(num):
    
    url = 'https://tv.kakao.com/api/v1/ft/home/category/original'


    req = requests.get(url=url).json()
    respone = req["list"]
    
    VIDEOS = []
    VIDEO = dict()
    VIDEO["page"] = req["hasMore"]
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


def live_videos(numb):

    url1 = 'https://tv.kakao.com/api/v1/ft/home/livelinks'
    load1 = {
        'tab': 'all',
        'fields': 'ccuCount,isShowCcuCount,thumbnailUrl,channel,live',
        'sort': 'CcuCount',
        'size': '35',
        'page': numb
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
            'profile': 'BASE',
            'contentType': 'HLS'   
        }
        req2 = requests.get(url=urllive, params=load2).json()
        LIVE["play"] = req2["videoLocation"]["url"]
        li = xbmcgui.ListItem(LIVE["title"], iconImage=LIVE["thumb"])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=LIVE["play"], listitem=li, isFolder=False)
    
        LIVES.append(LIVE)
        
    return LIVES


mode = args.get('mode', None)

if mode is None:
    url = build_url({'mode': 'VOD', 'foldername': 'VOD'})
    li = xbmcgui.ListItem('VOD', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'LIVE', 'foldername': 'LIVE'})
    li = xbmcgui.ListItem('LIVE', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'NEXT_vod':
    foldername = args['foldername'][0]
    b = page(page(0))
    pa = vod_videos(b)
    for a in pa:    
        if a["page"] == True:
            url = build_url({'mode': 'NEXT_vod', 'foldername': 'NEXT'})
            li = xbmcgui.ListItem('NEXT', iconImage='DefaultFolder.png')
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
            xbmcplugin.endOfDirectory(addon_handle)
    
        elif a["page"] == False:
            xbmcplugin.endOfDirectory(addon_handle)



elif mode[0] == 'NEXT_live':
    foldername = args['foldername'][0]
    b = page(page(0))
    pa = live_videos(b)
    for a in pa:
        try:    
            if a["page"] == True:

                url = build_url({'mode': 'NEXT_live', 'foldername': 'NEXT'})
                li = xbmcgui.ListItem('NEXT', iconImage='DefaultFolder.png')
                xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
                xbmcplugin.endOfDirectory(addon_handle) 

            elif a["page"] == False:
                xbmcplugin.endOfDirectory(addon_handle)
        
        except:
            xbmcplugin.endOfDirectory(addon_handle)
    xbmcplugin.endOfDirectory(addon_handle)
    


elif mode[0] == 'VOD':
    foldername = args['foldername'][0]
    pa = vod_videos(page(1))
    for a in pa:    
        if a["page"] == True:
            url = build_url({'mode': 'NEXT_vod', 'foldername': 'NEXT'})
            li = xbmcgui.ListItem('NEXT', iconImage='DefaultFolder.png')
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
            xbmcplugin.endOfDirectory(addon_handle)

        elif a["page"] == False:
            xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'LIVE':
    foldername = args['foldername'][0]
    ba = live_videos(page(1))
    for b in ba:
        if b["page"] == True:
            url = build_url({'mode': 'NEXT_live', 'foldername': 'NEXT'})
            li = xbmcgui.ListItem('NEXT', iconImage='DefaultFolder.png')
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
            xbmcplugin.endOfDirectory(addon_handle)

        elif b["page"] == False:
            xbmcplugin.endOfDirectory(addon_handle)


