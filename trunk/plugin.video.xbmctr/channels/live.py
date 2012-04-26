import urllib
import urllib2
import re
import os,sys
import xbmcplugin,xbmcgui,xbmc,xbmcaddon 
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP
try:
    import json
except:
    import simplejson as json
import scraper, xbmctools

# -*- coding: iso-8859-9 -*-
Addon = xbmcaddon.Addon('plugin.video.xbmcTR')
profile = xbmc.translatePath(Addon.getAddonInfo('profile'))
__settings__ = xbmcaddon.Addon(id='plugin.video.xbmcTR')
__language__ = __settings__.getLocalizedString

Url =xbmctools.setUrl

FILENAME = "live"

url='http://drascom.dyndns.org/site/t.xml'

def main():
     xbmctools.addFolder(FILENAME,"Sadece Turk Kanalları vardır.Diğer kanallar 15/04/2012 de hazır olacaktır", "BuildPage(code='tr')",url)
     xbmctools.addFolder(FILENAME,__language__(30030), "BuildPage(code='tr')", "")
     xbmctools.addFolder(FILENAME,__language__(30031), "BuildPage(code='de')", "")
     xbmctools.addFolder(FILENAME,__language__(30032), "BuildPage(code='en')", "")
     xbmctools.addFolder(FILENAME,__language__(30033), "BuildPage(code='it')", "")
     xbmctools.addFolder(FILENAME,__language__(30034), "BuildPage(code='ru')", "")
     xbmctools.addFolder(FILENAME,__language__(30035), "BuildPage(code='fr')", "")
     xbmctools.addFolder(FILENAME,__language__(30036), "BuildPage(code='ye')", "")
     xbmctools.addFolder(FILENAME,__language__(30037), "BuildPage(code='ca')", "")
     xbmctools.addFolder(FILENAME,__language__(30038), "BuildPage(code='ca2')", "")


def BuildPage(code):
    url=xbmctools.setUrl()
    link=xbmctools.get_url(url)
    tr=re.compile('<name>Turkish</name>.*?<title>(.*?)</title>.*?<link>(.*?)</link>.*?<thumbnail>(.*?)</thumbnail>').findall(link)
    de=re.compile('<name>German</name>.*?<title>(.*?)</title>.*?<link>(.*?)</link>.*?<thumbnail>(.*?)</thumbnail>').findall(link)
    en=re.compile('<name>English</name>.*?<title>(.*?)</title>.*?<link>(.*?)</link>.*?<thumbnail>(.*?)</thumbnail>').findall(link)
    it=re.compile('<name>Italy</name>.*?<title>(.*?)</title>.*?<link>(.*?)</link>.*?<thumbnail>(.*?)</thumbnail>').findall(link)
    ru=re.compile('<name>Russian</name>.*?<title>(.*?)</title>.*?<link>(.*?)</link>.*?<thumbnail>(.*?)</thumbnail>').findall(link)
    fr=re.compile('<name>French</name>.*?<title>(.*?)</title>.*?<link>(.*?)</link>.*?<thumbnail>(.*?)</thumbnail>').findall(link)
    ye=re.compile('<name>yesil</name>.*?<title>(.*?)</title>.*?<link>(.*?)</link>.*?<thumbnail>(.*?)</thumbnail>').findall(link)
    ca=re.compile('<name>cizgi-tr</name>.*?<title>(.*?)</title>.*?<link>(.*?)</link>.*?<thumbnail>(.*?)</thumbnail>').findall(link)
    ca2=re.compile('<name>cizgi-de</name>.*?<title>(.*?)</title>.*?<link>(.*?)</link>.*?<thumbnail>(.*?)</thumbnail>').findall(link)
    if code is 'tr':
        for linkTitle,Url,thumbnail in tr:
            xbmctools.addVideoLink(linkTitle,Url, thumbnail)
    else:
        pass
    if code is 'de':
         for linkTitle,Url,thumbnail in de:
            xbmctools.addVideoLink(linkTitle,Url, thumbnail)
    else:
        pass
    
    if code is 'en':
         for linkTitle,Url,thumbnail in en:
            xbmctools.addVideoLink(linkTitle,Url, thumbnail)
    else:
        pass
    if code is 'it':
         for linkTitle,Url,thumbnail in it:
            xbmctools.addVideoLink(linkTitle,Url, thumbnail)
    else:
        pass
    if code is 'ru':
         for linkTitle,Url,thumbnail in ru:
            xbmctools.addVideoLink(linkTitle,Url, thumbnail)
    else:
        pass
    if code is 'fr':
         for linkTitle,Url,thumbnail in fr:
            xbmctools.addVideoLink(linkTitle,Url, thumbnail)
    else:
        pass
    if code is 'ye':
         for linkTitle,Url,thumbnail in ye:
            xbmctools.addVideoLink(linkTitle,Url, thumbnail)
    else:
        pass
    if code is 'ca':
         for linkTitle,Url,thumbnail in ca:
            xbmctools.addVideoLink(linkTitle,Url, thumbnail)
    else:
        pass
    if code is 'ca2':
         for linkTitle,Url,thumbnail in ca2:
            xbmctools.addVideoLink(linkTitle,Url, thumbnail)
    else:
        pass
    
'''
def getSoup(url):
        if url.startswith('http://'):
            try:
                req = urllib2.Request(url)
                response = urllib2.urlopen(req)
                data = response.read()
                response.close()
            except urllib2.URLError, e:
                # errorStr = str(e.read())
                if hasattr(e, 'code'):
                    print 'We failed with error code - %s.' % e.code
                    xbmc.executebuiltin("XBMC.Notification(error code - "+str(e.code)+",10000,"+icon+")")
                elif hasattr(e, 'reason'):
                    print 'We failed to reach a server.'
                    print 'Reason: ', e.reason
                    xbmc.executebuiltin("XBMC.Notification(failed to reach a server. - "+str(e.reason)+",10000,"+icon+")")
        else:
            data = open(url, 'r').read()
        soup = BeautifulSOAP(data, convertEntities=BeautifulStoneSoup.XML_ENTITIES)
        return soup
def getData(url,fanart):
    if len(soup('channels')) > 0:
            channels = soup('channel')
            for channel in channels:
                name = channel('name')[0].string
                thumbnail = channel('thumbnail')[0].string
                if thumbnail == None:
                    thumbnail = ''
            xbmctools.addFolder(FILENAME,name,"getChannelItems(name,url)",url,thumbnail)

def getChannelItems(name,url):
        soup = getSoup(url)
        channel_list = soup.find('channel', attrs={'name' : name})
        items = channel_list('item')
        
        for channel in channel_list('subchannel'):
            name = channel('name')[0].string
            try:
                thumbnail = channel('thumbnail')[0].string
                if thumbnail == None:
                    raise
            except:
                thumbnail = ''
            try:
                xbmctools.addFolder(FILENAME,name,"getSubChannelItems(name,url)",url,thumbnail)
            except:
                print 'There was a problem adding directory - '+name.encode('utf-8', 'ignore')

'''
