#-*- coding: utf-8 -*-
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

def vod_first(num, id):

    url = 'https://tv.kakao.com/api/v1/ft/home/category/original'
    load = {
        'fields': 'channel,-user,-clipChapterThumbnailList,-tagList,-service',
        'size': '20',
        'page': num,
        'after': id
    }
    req = requests.get(url=url, params=load).json()
    id1 = req['list'][19]['id']

    return id1

def vod_play(id):

    url = 'https://tv.kakao.com/katz/v1/ft/cliplink/{}/readyNplay'.format(id)
    load = {
        'player': 'monet_html5',
        'uuid': 'edb32a231df16d59a986069f343c015f',
        'profile': 'HIGH4'
    }
    req = requests.get(url=url, params=load).json()
    play = req['videoLocation']['url']

    return play

def vod_play1(id):

    url = 'https://tv.kakao.com/katz/v1/ft/cliplink/{}/readyNplay'.format(id)
    load = {
        'player': 'monet_html5',
        'profile': 'HIGH',
        'service': 'kakao_tv',
        'dteType': 'PC'
    }
    req = requests.get(url=url, params=load).json()
    play = req['videoLocation']['url']

    return play

def vod_videos(num, id1, mod, mod1):

    url = 'https://tv.kakao.com/api/v1/ft/home/category/original'
    load = {
        'fields': 'channel,-user,-clipChapterThumbnailList,-tagList,-service',
        'size': '20',
        'page': num,
        'after': id1
    }

    req = requests.get(url=url, params=load).json()
    respone = req["list"]

    videos = []
    page = req['hasMore']
    for i in respone:

        video = dict()
        video['id'] = i['id']
        video['title'] = i['displayTitle']
        video['thumb'] = i['clip']['thumbnailUrl']
        video['play'] = vod_play(i['id'])

        videos.append(video)

    if page == True:
        folderlist(mod, mod1, 'NEXT', True, 'DefaultFolder.png')

    else:
        pass

    return videos

def vod_list(num, id1, mod, mod1, isfolder):
    a = vod_videos(num, id1, mod, mod1)
    for b in a:
        listset(b['title'], b['thumb'], b['play'], isfolder)

def search():
    try:
        kb = xbmc.Keyboard('default', 'heading', True)
        kb.setDefault('')  # optional
        kb.setHeading('Search')  # optional
        kb.setHiddenInput(False)  # optional
        kb.doModal()
        if kb.isConfirmed():
            Search = kb.getText()
    except:
        pass

    return Search

def search_vod(num, mod, mod1, Search):
    url = 'https://tv.kakao.com/api/v1/ft/search/cliplinks'
    load = {
        'sort': 'Score',
        'q': Search,
        'fulllevels': 'list',
        'fields': '-user, -clipChapterThumbnailList, -tagList',
        'size': '30',
        'page': num
        }
    req = requests.get(url=url, params=load).json()
    respone = req['list']
    page = req['hasMore']

    for i in respone:

        title = i['displayTitle']
        thumb = i['clip']['thumbnailUrl']

        try:
            play = vod_play(i['id'])
            listset(title, thumb, play, False)
        except:
            play = vod_play1(i['id'])
            listset(title, thumb, play, False)

    if page == True:
        folderlist(mod, mod1, 'NEXT', True, 'DefaultFolder.png')

    else:
        pass


def live_videos(num, mod, mod1):

    url = 'https://tv.kakao.com/api/v1/ft/home/livelinks'
    load = {
        'tab': 'all',
        'fields': 'ccuCount,isShowCcuCount,thumbnailUrl,channel,live',
        'sort': 'CcuCount',
        'size': '20',
        'page': num
        }

    req1 = requests.get(url=url, params=load).json()
    respone = req1["list"]

    page = req1["hasMore"]
    for i in respone:
        id = i["id"]
        title = i["displayTitle"]
        thumb = i["live"]["thumbnailUrl"]

        urllive = 'https://tv.kakao.com/katz/v1/ft/livelink/{}/readyNplay'.format(id)
        load2 = {
            'player': 'moment_html5',
            'profile': 'BASE',
            'contentType': 'HLS'
        }
        req2 = requests.get(url=urllive, params=load2).json()
        try:
            play = req2["videoLocation"]["url"]
            listset(title, thumb, play, False)

        except:
            folderlist('Error', 'Error', title, True, thumb)

    if page == True:
        folderlist(mod, mod1, 'NEXT', True, 'DefaultFolder.png')

    else:
        pass


def listset(title, thumb, play, isFolder):
    li = xbmcgui.ListItem(title, iconImage=thumb)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=play, listitem=li, isFolder=isFolder)


def folderlist(mode, mode1, name, isFolder, image):
    url = build_url({'mode': mode, 'mode1': mode1})
    li = xbmcgui.ListItem(name, iconImage=image)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=isFolder)

mode = args.get('mode', None)
mode1 = args.get('mode1', None)

if mode is None:
    folderlist('VOD', 'VOD',  'VOD', True, 'DefaultFolder.png')
    folderlist('LIVE', 'LIVE', 'LIVE', True, 'DefaultFolder.png')
    folderlist('SEARCH', 'SEARCH', 'SEARCH', True, 'DefaultFolder.png')
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'Error':
    dialog = xbmcgui.Dialog()
    ok = dialog.ok('Error Message', 'Need Login')

elif mode[0] == 'VOD':
    vod_list(1, '', '1', 'vod', False)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'LIVE':
    live_videos(1, '1', 'Live')
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'SEARCH':
    a = search()
    b = xbmcgui.Window(xbmcgui.getCurrentWindowId())
    b.setProperty('search', a)

    if mode1[0] == 'SEARCH':
        search_vod(1, '1', a, a)
        xbmcplugin.endOfDirectory(addon_handle)


elif mode[0] == '1':
    a = xbmcgui.Window(xbmcgui.getCurrentWindowId())
    b = a.getProperty('search')
    if mode1[0] == 'Live':
        live_videos(2, '2', 'Live')
        xbmcplugin.endOfDirectory(addon_handle)

    elif mode1[0] == 'vod':
        vod_list(2, vod_first(1, ''), '2', 'vod', False)
        xbmcplugin.endOfDirectory(addon_handle)

    elif mode1[0] == b:
        search_vod(2, '2', b, b)
        xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == '2':
    a = xbmcgui.Window(xbmcgui.getCurrentWindowId())
    b = a.getProperty('search')
    if mode1[0] == 'Live':
        live_videos(3, '3', 'Live')
        xbmcplugin.endOfDirectory(addon_handle)

    elif mode1[0] == 'vod':
        vod_list(3, vod_first(2, vod_first(1, '')), '3', 'vod', False)
        xbmcplugin.endOfDirectory(addon_handle)

    elif mode1[0] == b:
        search_vod(3, '3', b, b)
        xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == '3':
    a = xbmcgui.Window(xbmcgui.getCurrentWindowId())
    b = a.getProperty('search')
    if mode1[0] == 'Live':
        live_videos(4, '4', 'Live')
        xbmcplugin.endOfDirectory(addon_handle)

    elif mode1[0] == 'vod':
        vod_list(4, vod_first(3, vod_first(2, vod_first(1, ''))), '4', 'vod', False)
        xbmcplugin.endOfDirectory(addon_handle)

    elif mode1[0] == b:
        search_vod(4, '4', b, b)
        xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == '4':
    a = xbmcgui.Window(xbmcgui.getCurrentWindowId())
    b = a.getProperty('search')
    if mode1[0] == 'Live':
        live_videos(5, '5', 'Live')
        xbmcplugin.endOfDirectory(addon_handle)

    elif mode1[0] == 'vod':
        vod_list(5, vod_first(4, vod_first(3, vod_first(2, vod_first(1, '')))), '5', 'vod', False)
        xbmcplugin.endOfDirectory(addon_handle)

    elif mode1[0] == b:
        search_vod(5, '5', b, b)
        xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == '5':
    a = xbmcgui.Window(xbmcgui.getCurrentWindowId())
    b = a.getProperty('search')
    if mode1[0] == 'Live':
        live_videos(6, '6', 'Live')
        xbmcplugin.endOfDirectory(addon_handle)

    elif mode1[0] == 'vod':
        vod_list(6, vod_first(5, vod_first(4, vod_first(3, vod_first(2, vod_first(1, ''))))), '6', 'vod', False)
        xbmcplugin.endOfDirectory(addon_handle)

    elif mode1[0] == b:
        search_vod(6, '6', b, b)
        xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == '6':
    a = xbmcgui.Window(xbmcgui.getCurrentWindowId())
    b = a.getProperty('search')
    if mode1[0] == 'Live':
        live_videos(7, '7', 'Live')
        xbmcplugin.endOfDirectory(addon_handle)

    elif mode1[0] == 'vod':
        vod_list(7, vod_first(6, vod_first(5, vod_first(4, vod_first(3, vod_first(2, vod_first(1, '')))))), '7', 'vod', False)
        xbmcplugin.endOfDirectory(addon_handle)

    elif mode1[0] == b:
        search_vod(7, '7', b, b)
        xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == '7':
    a = xbmcgui.Window(xbmcgui.getCurrentWindowId())
    b = a.getProperty('search')
    if mode1[0] == 'Live':
        live_videos(8, '8', 'Live')
        xbmcplugin.endOfDirectory(addon_handle)

    elif mode1[0] == 'vod':
        vod_list(8, vod_first(7, vod_first(6, vod_first(5, vod_first(4, vod_first(3, vod_first(2, vod_first(1, ''))))))), '8', 'vod', False)
        xbmcplugin.endOfDirectory(addon_handle)

    elif mode1[0] == b:
        search_vod(8, '8', b, b)
        xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == '8':
    a = xbmcgui.Window(xbmcgui.getCurrentWindowId())
    b = a.getProperty('search')
    if mode1[0] == 'Live':
        live_videos(9, '9', 'Live')
        xbmcplugin.endOfDirectory(addon_handle)

    elif mode1[0] == 'vod':
        vod_list(9, vod_first(8, vod_first(7, vod_first(6, vod_first(5, vod_first(4, vod_first(3, vod_first(2, vod_first(1, '')))))))), '9', 'vod', False)
        xbmcplugin.endOfDirectory(addon_handle)

    elif mode1[0] == b:
        search_vod(9, '9', b, b)
        xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == '9':
    a = xbmcgui.Window(xbmcgui.getCurrentWindowId())
    b = a.getProperty('search')
    if mode1[0] == 'Live':
        live_videos(10, '10', 'Live')
        xbmcplugin.endOfDirectory(addon_handle)

    elif mode1[0] == 'vod':
        vod_list(10, vod_first(9, vod_first(8, vod_first(7, vod_first(6, vod_first(5, vod_first(4, vod_first(3, vod_first(2, vod_first(1, ''))))))))), '10', 'vod', False)
        xbmcplugin.endOfDirectory(addon_handle)

    elif mode1[0] == b:
        search_vod(10, '10', b, b)
        xbmcplugin.endOfDirectory(addon_handle)