import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon

__settings__ = xbmcaddon.Addon(id='plugin.video.diziport')
__language__ = __settings__.getLocalizedString


def CATEGORIES():
        addDir(__language__(30000),'http://diziport.com/index.php?bolum=dizi&obje=default&sayfa=0',1,'special://home/addons/plugin.video.diziport/resources/images/yeni.png')
        addDir(__language__(30001),'http://diziport.com/',2,'special://home/addons/plugin.video.diziport/resources/images/main.jpg')
        
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
        page=re.compile('class=\'current\'><a><b>.+?</b></a></li>\n<li><a href=\'(.+?)\' rel=\'nofollow\'><b>(.+?)</b></a></li>').findall(link)
        for url,name in page:
                addDir(__language__(30006)+' >> '+name,'http://diziport.com/'+url,1,'special://home/addons/plugin.video.diziport/resources/images/next.png')
       
def ALL(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
        response.close()
        match=re.compile('<li><a href="(.+?)" alt=".+?" title="(.+?)">').findall(link)
        for url,name in match:
                addDir(name,'http://diziport.com/'+url,3,'')
        MAINMENU(url)
def SESSION(url):
        try:
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
                response.close()
                match=re.compile('src="(.+?)" alt="" width="113" height="113" align="center"  />\n<a href="(.+?)" title="(.+?)"').findall(link)
                for thumbnail,url,name in match:
                        addDir(name,'http://diziport.com/'+url,4,'http://diziport.com/'+thumbnail)
        except:
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
                response.close()
                match=re.compile('<a href="(.+?)"><img src="(.+?)" alt="(.+?)"').findall(link)
                for url,thumbnail,name in match:
                        addDir(name,url,4,thumbnail)
        MAINMENU(url)
def EPISODES(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
        response.close()
        match=re.compile('<a href="(.+?)"><img src="(.+?)" alt="(.+?)"').findall(link)
        for url,thumbnail,name in match:
                addDir(name,'http://diziport.com/'+url,5,'http://diziport.com/'+thumbnail)
        MAINMENU(url)

def VIDEOLINKS(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
        response.close()
        page=re.compile('<li><a href="(.+?)".+? rel="nofollow">.+?</a></li> \n\t').findall(link)
        try:
                if page[0]>1:
                        video(page[0])
                else:
                        pass
                if page[1]>1:
                        video(page[1])
                else:
                        pass
                if page[2]>1:
                        video(page[2])
                else:
                        pass
                if page[3]>1:
                        video(page[3])
                else:
                        pass
                if page[4]>1:
                        video(page[4])
                else:
                        pass
                if page[5]>1:
                        video(page[5])
                else:
                        pass
                if page[6]>1:
                        video(page[6])
                else:
                        pass
        except:
                pass
def video(url):
        http='http://diziport.com/'
        url=http+url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
        response.close()
        match=re.compile('islem\("(.+?)","get","(.+?)"').findall(link)
        for path,code in match:
        	p= path
        	c= code
        vurl='http://diziport.com/%s?%s' % (p, c)
        req = urllib2.Request(vurl)
        req.add_header('Referer',url)
        response = urllib2.urlopen(req)
        link2=response.read()
        response.close()
        movie=re.compile('strSource=(.+?)\'').findall(link2)
        for url in movie:
                addLink(name,url,'special://home/addons/plugin.video.diziport/resources/images/izle.png')
		MAINMENU(url)
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
        EPISODES(url)
elif mode==5:
        print ""+url
        VIDEOLINKS(url)
elif mode==6:
        print ""+url
        video(url)
elif mode==8:
        print ""+url
        PlayVid(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
