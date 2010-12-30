import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon
from BeautifulSoup import BeautifulSoup

__settings__ = xbmcaddon.Addon(id='plugin.video.diziizle')
__language__ = __settings__.getLocalizedString
sort = __settings__.getSetting('sort_by')


def CATEGORIES():
        addDir(__language__(30000),'http://www.dizi-izleyin.com',1,'http://www.dizi-izleyin.com/images/yasemin/logo.gif')
        addDir(__language__(30001),'http://www.dizi-izleyin.com/yeniler.html',2,'http://www.dizi-izleyin.com/images/yasemin/logo.gif')               
def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
        response.close()
        match=re.compile('<li class="alt"><a href="(.+?)" title=".+?">(.+?)</a></li>').findall(link)
        for url,name in match:
                 addDir(name,'http://www.dizi-izleyin.com'+url,3,'')
def RECENT(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
        response.close()
        match=re.compile('<img src=".+?" alt=".+?" style=".+?" title=""></div>\r\n\t\t\t\t\t<div class="product-disc"> <a href="(.+?)" class="red-link" title="(.+?)"').findall(link)
        for url,name in match:
                addDir(name,'http://www.dizi-izleyin.com'+url,3,'')
def SERIES(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<img src="(.+?)" alt="(.+?)" .+?"></div>\n\t\t\t\t\t<div class="product-disc"><a href="(.*?)"').findall(link)
        for thumbnail,name,url in match:
                addDir(name,'http://www.dizi-izleyin.com'+url,4,'')
        page=re.compile('<b>Sayfalar : </b>\n\t\t\t\t\t\t\t\t\t<b>.+?</b>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t <a href="(.+?)">.+?</a>').findall(link)
        if len(page)>1:del page[0];del page[0]
        for url in page:
                addDir(__language__(30001),'http://www.dizi-izleyin.com'+url,2,'special://home/addons/plugin.video.DİZİİZLE/resources/images/next.png')
def EPISODES(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<div class="kisim-.+?"><a href="(.+?)"><span class="white-text" title="(.+?)">.+?</span></a>').findall(link)
        for url,name in match:
                addDir(name,'http://www.dizi-izleyin.com'+url,5,'')        
def VIDEOLINKS(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()    
        match=re.compile('file=(.+?)&logo').findall(link)
        for url in match:
                addLink(name,match[0],'')
        

                
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
        INDEX(url)
elif mode==2:
        print ""+url
        RECENT(url,name)
elif mode==3:
        print ""+url
        SERIES(url,name)        
elif mode==4:
        print ""+url
        EPISODES(url,name)
elif mode==5:
        print ""+url
        VIDEOLINKS(url,name)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
