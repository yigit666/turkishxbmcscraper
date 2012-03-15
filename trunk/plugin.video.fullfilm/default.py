import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon
#-*- coding: cp1254 -*-
__settings__ = xbmcaddon.Addon(id='plugin.video.fullfilm')
__language__ = __settings__.getLocalizedString



def CATEGORIES():
        addDir('Tum eklentiler ve daha fazlası -- xbmcTr.com---','Search',3,'special://home/addons/plugin.video.fullfilm/resources/images/search.png')
        addDir(__language__(30003),'Search',3,'special://home/addons/plugin.video.fullfilm/resources/images/search.png')
        addDir(__language__(30000),'http://www.filmifullizle.com/',1,'special://home/addons/plugin.video.fullfilm/resources/images/main.png')
        addDir(__language__(30006),'http://www.filmifullizle.com/kategori/filmler/yerli-filmler',1,'special://home/addons/plugin.video.fullfilm/resources/images/tag.png')
        addDir(__language__(30007),'http://www.filmifullizle.com/kategori/filmler/yabanci-filmler',1,'special://home/addons/plugin.video.fullfilm/resources/images/eye.png')
        addDir(__language__(30008),'http://www.filmifullizle.com/kategori/filmler/yabanci-filmler/turkce-dublaj',1,'special://home/addons/plugin.video.fullfilm/resources/images/star.png')
        url='http://www.filmifullizle.com/'
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<li class=".*?"><a href="(.*?)" title=".*?">(.*?)</a>\n</li>').findall(link)
        for url,name in match:
                addDir('>> '+name,url,1,'')


def Main(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    link=link.replace('\xc5\x9f',"s").replace('&#038;',"&").replace('&#8217;',"'").replace('\xc3\xbc',"u").replace('\xc3\x87',"C").replace('\xc4\xb1',"ı").replace('&#8211;',"-").replace('\xc3\xa7',"c").replace('\xc3\x96',"O").replace('\xc5\x9e',"S").replace('\xc3\xb6',"o").replace('\xc4\x9f',"g").replace('\xc4\xb0',"I").replace('\xe2\x80\x93',"-")
    main=re.compile('<div style="float: left;">\n<a href="(.*?)"><img src="(.*?)" alt="(.*?)"').findall(link)
    for url,thumbnail,name in main:
        addDir(name,url,2,thumbnail)
    top=re.compile('<li>    <a href="(.*?)" title=".*?"><img src="(.*?)" alt="(.*?) izle " WIDTH=147 HEIGHT=205 class="guncover"/></a>\n    </li>').findall(link)
    for url,thumbnail,name in top:
        addDir(name,url,2,thumbnail)
    page=re.compile('<li class="active_page"><a href=".*?">.*?</a></li>\n<li><a href="(.*?)">(.*?)</a></li>').findall(link)
    for url,name in page:
        addDir(__language__(30001)+name,url,1,'')
            
def playList(url):
        ok = True
        url= url +':;'+url+'/2:;' +url+'/3:;' +url+'/4:;'+url+'/5:;'+url+'/6:;'
        print url
        playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playList.clear()
        pDialog = xbmcgui.DialogProgress()
        ret = pDialog.create('Loading playlist...')
        links = url.split(':;')
        print links
        del links [6]
        totalLinks = len(links)
        loadedLinks = 0
        remaining_display = __language__(30004)+'[B]' +str(loadedLinks)+' / '+str(totalLinks)+'[/B]'+ __language__(30005)
        pDialog.update(0,__language__(30002),remaining_display)
        a=0
        for url in links:
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile('<embed src=\'http:\/\/www.filmifullizle.com\/img\/player\.swf\?file=(.*?)&a').findall(link)
                for partLink in match:
                        name='Part'
                        a=a+1
                        name= name+' '+str(a)
                        addLink(name,partLink,'')
                        playList.add(partLink)
                        loadedLinks = loadedLinks + 1
                        percent = (loadedLinks * 100)/totalLinks
                        remaining_display = __language__(30004)+'[B]' +str(loadedLinks)+' / '+str(totalLinks)+'[/B]'+ __language__(30005)
                        pDialog.update(percent,__language__(30002),remaining_display)
                        if (pDialog.iscanceled()):
                                return False

        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playList)
        if not xbmcPlayer.isPlayingVideo():
                d = xbmcgui.Dialog()
                d.ok('Video Yok', 'Calamiyorum','Geri don.')
        return ok

def Search():
        keyboard = xbmc.Keyboard("", 'Search', False)
        keyboard.doModal()
        if keyboard.isConfirmed():
            query = keyboard.getText()
            url = ('http://www.filmifullizle.com/index.php?s=' + query)
            Main(url)

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param



def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        xbmc.Player().play(liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
elif mode==1:
        print ""+url
        Main(url)
elif mode==2:
        print ""+url
        playList(url)
elif mode==3:
        print ""+url
        Search()





xbmcplugin.endOfDirectory(int(sys.argv[1]))
