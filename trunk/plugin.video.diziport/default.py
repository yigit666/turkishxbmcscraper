import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon

__settings__ = xbmcaddon.Addon(id='plugin.video.diziport')
__language__ = __settings__.getLocalizedString




            
def CATEGORIES():
        addDir(__language__(30011),'search',9,'special://home/addons/plugin.video.diziport/resources/images/search.png')
        addDir(__language__(30000),'http://diziport.com/index.php?bolum=dizi&obje=default&sayfa=0',1,'special://home/addons/plugin.video.diziport/resources/images/plusone.png')
        addDir(__language__(30001),'http://diziport.com/index.php?bolum=uyelik&obje=uyekayit',2,'special://home/addons/plugin.video.diziport/resources/images/all.png')
        addDir(__language__(30004),'http://diziport.com/index.php?bolum=dizi&obje=diziler&tip=belgesel',6,'special://home/addons/plugin.video.diziport/resources/images/yeni.png')
        addDir(__language__(30007),'http://diziport.com/index.php?bolum=dizi&obje=diziler&tip=asya_dizileri',6,'special://home/addons/plugin.video.diziport/resources/images/main.jpg')
def search():
        keyboard = xbmc.Keyboard("", 'Search', False)
        keyboard.doModal()
        if keyboard.isConfirmed():
            query = keyboard.getText()
            print query
            url = ('http://diziport.com/index.php?eleman=' + query + '&buton.x=19&buton.y=6&bolum=dizi&obje=diziler&olay=arama')
            print url
            Documentary(url)
def RECENT(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xf6',"o").replace('&amp;',"&").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
        response.close()        
        MAINMENU(url)
        match=re.compile('<img src="(.+?)" alt=".+?" width="113" height="113" align="center" /></a>\n\t<h1 class="yellow"><a href="(.+?)" title="(.+?)">').findall(link)
        for thumbnail,url,name in match:
                addDir(name,url,5,'http://diziport.com/'+thumbnail)
                
        #next page        
        page=re.compile('class=\'current\'><a><b>.+?</b></a></li>\n<li><a href=\'(.+?)\' rel=\'nofollow\'><b>(.+?)</b></a></li>').findall(link)
        for url,name in page:
                addDir(__language__(30006)+' >> '+name,'http://diziport.com/'+url,1,'special://home/addons/plugin.video.diziport/resources/images/next.png')

def Documentary(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xf6',"o").replace('&amp;',"&").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
        response.close()
        MAINMENU(url)
        match=re.compile('<img src="(.*?)\?hash=123" alt=".*?" width="113" height="113" />\n<a href="(.*?)" title="(.*?)">').findall(link)
        for thumbnail,url,name in match:
                addDir(name,'http://diziport.com/'+url,3,'http://diziport.com/'+thumbnail)
        #next
        page=re.compile('class=\'current\'><a><b>.+?</b></a></li>\n<li><a href=\'(.+?)\' rel=\'nofollow\'><b>(.+?)</b></a></li>').findall(link)
        for url,name in page:
                addDir(__language__(30006)+' >> '+name,'http://diziport.com/'+url,6,'special://home/addons/plugin.video.diziport/resources/images/next.png')
        #previous
        page=re.compile('<li><a href=\'(.*?)\' rel=\'nofollow\'><b>(.*?)</b>').findall(link)
        for url,name in page:
                addDir(__language__(30005)+' >> '+name,'http://diziport.com/'+url,6,'special://home/addons/plugin.video.diziport/resources/images/next.png')

        
def ALL(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
        response.close()
        MAINMENU(url)
        match=re.compile('<li><a href="(.+?)" alt=".+?" title="(.+?)">').findall(link)
        for url,name in match:
                        addDir(name,'http://diziport.com/'+url,3,'')
        
def SESSION(url):
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
                response.close()
                match=re.compile('src="(.+?)" alt="" width="113" height="113" align="center"  />\n<a href="(.+?)" title="(.+?)"').findall(link)
                if match>[1]:
                        print 'sezonlu'
                        for thumbnail,url,name in match:
                                addDir(name,'http://diziport.com/'+url,4,'http://diziport.com/'+thumbnail)
                else:
                        print 'sezonsuz'
                        req = urllib2.Request(url)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                        response = urllib2.urlopen(req)
                        link=response.read()
                        link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
                        response.close()
                        new=re.compile('content="0;url=http://diziport.com/(.+?)"').findall(link)
                        if new<[1]:
                                print 'yonlendirmesiz'
                                EPISODES(url)
                        else:
                                print 'yonlendirmeli'
                                for url in new:
                                        EPISODES ('http://diziport.com/'+url)
                
def EPISODES(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
        response.close()
        MAINMENU(url)
        match=re.compile('<a href="(.+?)"><img src="(.+?)" alt="(.+?)"').findall(link)
        for url,thumbnail,name in match:
                addDir(name,'http://diziport.com/'+url,5,'http://diziport.com/'+thumbnail)

def VIDEOLINKS(name,url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
        response.close()
        match=re.compile('<b class="yellow"><a href="http://diziport.com/(.*?)-tekpartizle/(.*?)/1" title=".*?"><b class="yellow">Tek</b> Part</a>').findall(link)
        for u1,u2 in match:
            url='http://diziport.com/playlist.php?bolum='+u2+'&dizi='+u1
            #print url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xf6',"o").replace('&amp;',"&").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
        response.close()
        match=re.compile('<title>(.*?)</title>\n\t  <jwplayer:file>(.*?)</jwplayer:file>').findall(link)
#dialog
        dialog = xbmcgui.Dialog()
        ret = dialog.select(__language__(30008), [__language__(30009), __language__(30010)])
        if ret == 0:
                for mname,url in match:
                        a = name+'-'+mname
                        addLink(a,url,'special://home/addons/plugin.video.diziport/resources/images/izle.png')
                iscanceled = True
                return iscanceled
        if ret == 1:
                for mname,url in match:
                        a = name+'-'+mname
                        print a
                        addDir(a,url,8,'special://home/addons/plugin.video.diziport/resources/images/izle.png')
                iscanceled = True
                xbmc.executebuiltin('Notification("Diziport","Downloading")')
                return iscanceled


def Download(url):
                filename = (name+'.mp4')
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
        EPISODES(url)
elif mode==5:
        print ""+url
        VIDEOLINKS(name,url)
elif mode==6:
        print ""+url
        Documentary(url)
elif mode==8:
        print ""+url
        Download(url)
elif mode==9:
        print ""+url
        search()


xbmcplugin.endOfDirectory(int(sys.argv[1]))
