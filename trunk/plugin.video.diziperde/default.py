import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon
#-*- coding: cp1254 -*-
__settings__ = xbmcaddon.Addon(id='plugin.video.diziperde')
__language__ = __settings__.getLocalizedString


def CATEGORIES():
        #addDir(__language__(30008),'Search',6,'special://home/addons/plugin.video.diziport/resources/images/search.png')
        addDir(__language__(30000),'http://www.diziperdem.com/',1,'special://home/addons/plugin.video.diziport/resources/images/yeni.png')
        addDir(__language__(30001),'http://www.diziperdem.com/',2,'special://home/addons/plugin.video.diziport/resources/images/main.jpg')
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
        match=re.compile('<a href="(.*?)" class="red-link" title=".*?"><img src="(.*?)" alt="(.*?)" style="border-width: 0px; height: 100px; width: 110px;"></a>').findall(link)
        #eger eslesme bulamassan kategorilere geri don komutu
        if match<= 0:
                CATEGORIES()
        #match i�inde bulduklar�n�n s�ras� budur
        for url,thumbnail,name in match:
                #bulduklar�n� bu s�raya g�re seviye 4 e g�nder komutu.web sayfas�ndan al�nan url eksik oldu�u i�in bas�na ek yapt�k.. 
                addDir(name,'http://diziperdem.com'+url,4,thumbnail)
        #sonraki sayfa y� almas� i�in sayfay� tekrar taratt�p yeni sayfan�n url sini bulma komutu
        #yukar�daki match i�ine taram��t� kar��mas�n diye bunu page ad� i�ine tarat�yorum.
        page=re.compile('<span class="current">.+?</span><a href="(.+?)" title="(.+?)">').findall(link)
        for url,name in page:
                #buldu�um sayfa zaten i�inde oldu�um sayfan�n ayn� dizilimine sahip sayfa 1 sayfa 2 gibi.
                #buldu�um linki tekrar bu kod blokunun ba��na g�nderiyorum seviye 1
                addDir(__language__(30006)+' >> '+name,url,1,'special://home/addons/plugin.video.diziport/resources/images/next.png')
       
def ALL(url):
        #sayfan�n solundaki t�m dizi listesini tar�yoruz.
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
        response.close()
        match=re.compile('<a href="(.*?)" title="(.+?)"><img src=').findall(link)
        for url,name in match:
                        addDir(name,'http://diziperdem.com'+url,3,'')#bulduklar�m�z� session bolumune yolluyoruz.url ye dikkat.
        
        MAINMENU(url)
def SESSION(url):
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile('<div class="product-image1"> <a href="(.*?)" class="red-link" title="(.*?)"><img src="(.*?)" alt=".*?"').findall(link)
                for url,name,thumbnail in match:
                                addDir(name,'http://diziperdem.com'+url,4,thumbnail)
                MAINMENU(url)
def final(url):
        #kullan�c�n�n son sayfas� her�eyin topland��� yer hem partl� sistemi hem tek linki
        #�al��t�r�p hangisi varsa listeleyecek
        trailer(url)
        parts(url)
        tek_link(url)

def trailer(url):
        #filmin kendisi yok traileri varsa onu bulup izleticez.
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
        response.close()
        match=re.compile('<param name="movie" value="(.*?)\&').findall(link)
        for url in match:
                xbmcPlayer = xbmc.Player()
                xbmcPlayer.play(url)        
        
def parts(url):
        #herbir sayfay� tek tek �ag�r�p parlar� al�caz.
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        #partlar�n sayfalar�n� buluyoruz "/behzat-c-54bolum-kisim-1.html,/behzat-c-54bolum-kisim-2.html,/behzat-c-54bolum-kisim-3.html"vs gibi
        response.close()
        match=re.compile('<a href="(.*?)" title="(.*?)">\n\t\t\t<span class="white-text">.*?</span></a></div>').findall(link)
        for url,name in match:
                        direct_link('http://diziperdem.com'+url)#her linki mp4 bulunmas� i�in g�nderiyoruz.url yine eklentili...


def direct_link(url):
        #part sayfas�ndan gelen linkleri al�r bunlar�n i�inde mp4 leri bulur ve listeler
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
        response.close()
        match=re.compile('encodeURIComponent\(\'(.*?)mp4').findall(link)
        for url in match:
                        addLink(name,url+'mp4','')#url ye dikkat ekleme yapt�k.thumbnail yok dolay�s� ile i�i bo� '' yapt�k
def tek_link(url):
        #tek link olan filmlerin �nce xml dosyas�n� sonrada i�inden mp4 leri bulaca��z.
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
        response.close()
#arad�g�m�z adres "settingsFile: "http://www.ddizi.com/xml.php?id=31333"
        match=re.compile('settingsFile: "(.*?)"').findall(link)
#daha sonra kullanmak �zere part isimlerini haz�rl�yorum.
        epname= 'part'
        a=0
#bu de�er artarak gidecek part 1,2,3,4 olmas�n� sa�layacak �nce tan�mlad�k 0 diye
        playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playList.clear()
#playlist tan�mlad�m ve i�inin bo� olmas�n� sa�lad�m.
        for url in match:
                #buldugumuz linki tekrar a��p i�inden mp4 leri al�caz (alt d�ng� yap�yoruz.)
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
                response.close()
                match=re.compile('<videoPath value="(.*?)"').findall(link)
#video linklerini bulduk
                for url in match:
                        a= a+1
#part numaras�n� 1 artt�rd�k
                        name = epname + ' - '+str(a)
#ismin "part" + metin olarak artan say� olmas�n� sa�lad�k.
#metin olarak ekledim ��nk� metin ile say�y� birle�tiremeyiz.
                        playList.add(url)
#buldu�um url yi playliste ekledim.bir sonraki turda bulunan url devam�na eklenecek.
                        addLink(name,url,'special://home/addons/plugin.video.dizihd/resources/images/izle.png')
#playlist iptal edildi�inde (stop yada esc ile)partlar liste olarak g�r�ls�n diye linkleri ekledim.(playlist ayr� bu ayr�)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playList)
#playlisti �al dedim otomatik �almaya ba�layacak


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
        final(url)
elif mode==5:
        print ""+url
        Download(url)
elif mode==6:
        print ""+url
        Search()


xbmcplugin.endOfDirectory(int(sys.argv[1]))
