import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon

__settings__ = xbmcaddon.Addon(id='plugin.video.dizihd')
__language__ = __settings__.getLocalizedString


def CATEGORIES():
        #addDir(__language__(30008),'Search',6,'special://home/addons/plugin.video.diziport/resources/images/search.png')
        addDir(__language__(30000),'http://www.dizihd.com/',1,'special://home/addons/plugin.video.diziport/resources/images/yeni.png')
        addDir(__language__(30001),'http://www.dizihd.com/',2,'special://home/addons/plugin.video.diziport/resources/images/main.jpg')
        addDir(__language__(30007),'http://www.dizihd.com/dizi-izle/belgesel-izle/',1,'special://home/addons/plugin.video.diziport/resources/images/main.jpg')
def Search():
        keyboard = xbmc.Keyboard("", 'Search', False)
        keyboard.doModal()
        if keyboard.isConfirmed():
            query = keyboard.getText()
            url = ('http://www.dizihd.com/?s='+ query +'&x=0&y=0')
            RECENT(url)
def RECENT(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xf6',"o").replace('&amp;',"&").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
        response.close()
        MAINMENU(url)        
        match=re.compile('<a href="(.+?)"><img src="(.+?)" ></a>\r\n\t\t\t\t\t\t<h2><a href=".+?">(.+?)izle.*?</a>').findall(link)
        #http://www.dizihd.com/the-mentalist-4-sezon-11-bolum-izle
        if match<= 0:
                CATEGORIES()
        for url,thumbnail,name in match:
                addDir(name,url,4,thumbnail)
        page=re.compile('<span class="current">.+?</span><a href="(.+?)" title="(.+?)">').findall(link)
        for url,name in page:
                addDir(__language__(30006)+' >> '+name,url,1,'special://home/addons/plugin.video.diziport/resources/images/next.png')
       
def ALL(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
        response.close()
        match=re.compile('<li class="cat-item cat-item-.+?"><a href="(.+?)" title=".+?">(.+?)izle</a>\r\n</li>').findall(link)
        #http://www.dizihd.com/dizi-izle/alin-yazisi-izle
        for url,name in match:
                        addDir(name,url,3,'')
        
        MAINMENU(url)
def SESSION(url):
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
                response.close()
                match=re.compile('<a href="(.+?)"><img src="(.+?)" ></a>\r\n\t\t\t\t\t\t<h2><a href=".+?">(.+?)izle.*?</a>').findall(link)
                for url,thumbnail,name in match:
                                addDir(name,url,4,thumbnail)
                MAINMENU(url)

def VIDEOLINKS(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
        response.close()
#xml okuma
        page=re.compile('xmlAddress = \'(.+?)\'').findall(link)
        epname= 'part'
        a=0
#Create playlist
        playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playList.clear()
#xmlAddress = 'http://www.dizihd.com/player/dizihd/supernaturals07e01hd.xml'
        for url in page:
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
                response.close()
                #<videoPath value="http://www.dizihd.com/dizihdd.php?git=http://video.ak.fbcdn.net/cfs-ak-ash4/344221/498/112810335493302_60183.mp4"/>
                match=re.compile('<videoPath value="(.+?)"').findall(link)
                del match [0]
                for url in match:
                        a= a+1
                        name = epname + ' - '+str(a)
                        playList.add(url)
                        addLink(name,url,'special://home/addons/plugin.video.dizihd/resources/images/izle.png')
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playList)
                
def Download(url):
        #rename file with end of url
        filename = name+'.mp4'
        def download(url, dest):
                        dialog = xbmcgui.DialogProgress()
                        dialog.create('Downloading Movie','From Source', filename)
                        urllib.urlretrieve(url, dest, lambda nb, bs, fs, url = url: _pbhook(nb, bs, fs, url, dialog))
        def _pbhook(numblocks, blocksize, filesize, url = None,dialog = None):
                        try:
                                        percent = min((numblocks * blocksize * 100) / filesize, 100)
                                        dialog.update(percent)
                        except:
                                        percent = 100
                                        dialog.update(percent)
                        if dialog.iscanceled():
                                        dialog.close()
        if (__settings__.getSetting('download') == ''):
                        __settings__.openSettings('download')
        filepath = xbmc.translatePath(os.path.join(__settings__.getSetting('download'),filename))
        download(url, filepath)
        
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
        CATEGORIES()
elif mode==1:
        print ""+url
        RECENT(url)
elif mode==2:
        print ""+url
        ALL(url)
elif mode==3:
        print ""+url
        SESSION(url)
elif mode==4:
        print ""+url
        VIDEOLINKS(url)
elif mode==5:
        print ""+url
        Download(url)
elif mode==6:
        print ""+url
        Search()


xbmcplugin.endOfDirectory(int(sys.argv[1]))
