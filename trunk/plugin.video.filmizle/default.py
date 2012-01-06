import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon

__settings__ = xbmcaddon.Addon(id='plugin.video.filmizle')
__language__ = __settings__.getLocalizedString


def MAIN():
        addDir(__language__(30000),'http://www.filmizle.com.tr/tur/boxset',2,'http://www.filmizle.com.tr/wp-content/themes/film/images/logo.png')
        addDir(__language__(30001),'http://www.filmizle.com.tr/tur/film-kisitlama',1,'http://www.filmizle.com.tr/wp-content/themes/film/images/logo.png')
        addDir(__language__(30002),'http://www.filmizle.com.tr/tur/turler',2,'http://www.filmizle.com.tr/wp-content/themes/film/images/logo.png')
def CATEGORIES():
        addDir(__language__(30003),'http://www.filmizle.com.tr/tur/yabanci-filmler',1,'http://www.filmizle.com.tr/wp-content/themes/film/images/logo.png')
        addDir(__language__(30004),'http://www.filmizle.com.tr/tur/yerli-filmler',1,'http://www.filmizle.com.tr/wp-content/themes/film/images/logo.png')
        addDir(__language__(30005),'http://www.filmizle.com.tr/tur/yesilcam-filmleri-izle',1,'http://www.filmizle.com.tr/wp-content/themes/film/images/logo.png')
        addDir(__language__(30006),'http://www.filmizle.com.tr/tur/film-kisitlama/altyazili-film-filmler-izle',1,'http://www.filmizle.com.tr/wp-content/themes/film/images/logo.png')
        addDir(__language__(30007),'http://www.filmizle.com.tr/tur/film-kisitlama/tek-part',1,'http://www.filmizle.com.tr/wp-content/themes/film/images/logo.png')
        addDir(__language__(30008),'http://www.filmizle.com.tr/tur/film-kisitlama/turkce-dublaj-film-izle',1,'http://www.filmizle.com.tr/wp-content/themes/film/images/logo.png')
        
def GENRES():
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()        
        match=re.compile('<a href="(.+?)" rel="bookmark" title="(.+?)filmini izle"><img src="(.+?)"').findall(link)
        for url,name,thumbnail in match:
                addDir(name,url,4,thumbnail)

def MAINMENU(url):
        addDir(__language__(30002),'http://diziport.com/','','special://home/addons/plugin.video.diziport/resources/images/main.jpg')
        
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



def addList(name,url,iconimage):
        pl=xbmc.PlayList(1)
        pl.clear()
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmc.PlayList(1).add(handle=int(sys.argv[1]),url=url, listitem=liz)
        xbmc.Player().play(pl)
        return ok

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
        MAIN()
elif mode==1:
        print ""+url
        CATEGORIES(url)
elif mode==2:
        print ""+url
        GENRES(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
