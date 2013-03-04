# -*- coding: utf-8 -*-
import urllib,urllib2
import sys,re
import os,os.path,time,stat
from xml.dom.minidom import Document
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from BeautifulSoup import BeautifulStoneSoup

# Eklenti bildirimleri --------------------------------------------------------
addon_id = 'plugin.video.mc'
__settings__ = xbmcaddon.Addon(id=addon_id)
home = __settings__.getAddonInfo('path')
IMAGES_PATH = xbmc.translatePath(os.path.join(home, 'resoures','image'))
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:10.0.1)"
XMLYOLU = xbmc.translatePath(os.path.join(home,'resources','temp'))

#----------------------------------------------------------------------------

def name_fix(x):        
        x=x.replace('-',' ')
        return x[0].capitalize() + x[1:]

def get(url):
        print '****url okunuyor***'
        req = urllib2.urlopen(url) 
        encoding=req.headers['content-type'].split('charset=')[-1]   
        data = unicode(req.read(), encoding)
        return data
def get2(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        content = urllib2.urlopen(req)
        data = content.read()
        content.close()
        return data
def encode_fix(data):
        data=data.encode("utf-8")
        return data
def videoTitle_fix(videoTitle):
        videoTitle=videoTitle.replace(' Turkce Dublaj ',"TR").replace('izle',"").replace('Full',"").replace('(',"|").replace(')',"|")
        videoTitle=videoTitle.replace('\xe2\x80\x99'," ").replace('\xc3\xa4',"").replace('\xc3\xa8',"'").replace('\xc5\x9f',"s").replace('&#038;',"&").replace('&#8217;',"'").replace('\xc3\xbc',"u").replace('\xc3\x87',"C").replace('\xc4\xb1',"i").replace('&#8211;',"-").replace('\xc3\xa7',"c").replace('\xc3\x96',"O").replace('\xc5\x9e',"S").replace('\xc3\xb6',"o").replace('\xc3\xad',"i").replace('\xc4\x9f',"g").replace('\xc3\x9c',"u").replace('\xc4\xb0',"I").replace('\xe2\x80\x93',"-")
        videoTitle=videoTitle.replace('\u0131',"i").replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g").replace('&#8211;',"-")
        return videoTitle
def addFolder(fileName, name, method, url="", thumbnail=""):
    u = sys.argv[0]+"?fileName="+urllib.quote_plus(fileName)+"&method="+urllib.quote_plus(method)+"&url="+urllib.quote_plus(url)
    if thumbnail != "":
        thumbnail = os.path.join(IMAGES_PATH, thumbnail+".png")
        print ('Klasor Resim:'+thumbnail)
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)

def addVideoFolder(fileName,videoTitle, method, url, thumbnail, info):
    u = sys.argv[0]+"?fileName="+urllib.quote_plus(fileName)+"&videoTitle="+urllib.quote_plus(videoTitle)+"&method="+urllib.quote_plus(method)+"&url="+urllib.quote_plus(url)+"&thumbnail="+urllib.quote_plus(thumbnail)
    liz = xbmcgui.ListItem(videoTitle, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
    liz.setInfo(type="Video", infoLabels=info)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)


def addVideoLink(linkTitle, url, thumbnail=""):
    liz = xbmcgui.ListItem(linkTitle, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
    liz.setInfo(type="Video", infoLabels={"Title":linkTitle})
    liz.setProperty("IsPlayable", "true")
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)

def loadImports():
    yol = xbmc.translatePath(os.path.join(home, 'channels'))
    files = os.listdir(yol)
    global imps
    imps = []

    for i in range(len(files)):
        py_name = files[i].split('.')
        if len(py_name) > 1:
            if py_name[1] == 'py' and py_name[0] != '__init__':
               py_name = py_name[0]
               imps.append(py_name)
    file = open(yol+'/__init__.py','w')
    toWrite = '__all__ = '+str(imps)
    file.write(toWrite)
    file.close()

def listChannels():

    for fileName in imps:
        addFolder(fileName, fileName ,"main()", "",fileName)

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def xml_yap(fileName,bolum,MAINRESULT):
    doc = Document()
    liste = doc.createElement("liste")
    doc.appendChild(liste)


    for videoTitle,url,thumbnail,description in MAINRESULT:
            print ('xml yap DOKUM',videoTitle)
            kanal = doc.createElement("channel")
            liste.appendChild(kanal)
            

            ad = doc.createElement("title")
            kanal.appendChild(ad)
            veri_ad = doc.createTextNode(videoTitle.encode( "utf-8" ))
            ad.appendChild(veri_ad)

            adres = doc.createElement("stream_url")
            kanal.appendChild(adres)
            veri_adres = doc.createTextNode(url)
            adres.appendChild(veri_adres)

            resim = doc.createElement("logo_30x30")
            kanal.appendChild(resim)
            veri_resim = doc.createTextNode(thumbnail)
            resim.appendChild(veri_resim)

            info = doc.createElement("description")
            kanal.appendChild(info)
            veri_info = doc.createTextNode(description)
            info.appendChild(veri_info)
    os.chmod(XMLYOLU, stat.S_IRWXO)
    os.chmod(XMLYOLU, stat.S_IRWXG)
    os.chmod(XMLYOLU, stat.S_IRWXU)
    filepath = xbmc.translatePath(os.path.join(XMLYOLU,str(fileName)+'_'+bolum+'.xml'))
    try:
            os.chmod(filepath, stat.S_IRWXO)
            os.chmod(filepath, stat.S_IRWXG)
            os.chmod(filepath, stat.S_IRWXU)
    except:
            pass

    f = open(filepath, "w")
    try:
        f.write(doc.toprettyxml(indent="",encoding="utf-8"))
    finally:
        f.close()
    return filepath

def open_xml(filepath):
        finalResult=[]
        handler=open(filepath,"r")
        handler = handler.read()
        soup=BeautifulStoneSoup(handler)
        print 'ENCODING : ',soup.originalEncoding
        
        channels =soup.findAll('channel')
        for channel in channels:
                title=channel.title
                videoTitle=title.text
                logo=channel.logo_30x30
                thumbnail=contents = "".join([str(item) for item in logo.contents])
                thumbnail=re.sub(r'\s', '', thumbnail)            #bosluklari kesiyoruz
                desc=channel.description
                desc=re.compile(']]>(.*?)</description>').findall(str(desc))
                purl=channel.playlist_url
                surl=channel.stream_url
                if desc:
                        print desc
                else:
                        desc='Bilgi Yok'
                if purl:
                        url=purl.text
                else:
                        if surl:
                                url=surl.text
                        else:
                                print 'xml den url alinmadi.'
                                pass #Hata kodu yazilacak
                finalResult.append((videoTitle, url, thumbnail))
##        print 'finalResult:'+str(finalResult)                
        return finalResult

def check_time(xml):
        try:
                status=''
                t = os.path.getmtime(xml)
                today = time.time()
                diff=today-t
                print diff
                if diff <= 86400:
                        status="GUNCEL"
                else:
                        status="ESKI"
                return status
        except:
                return ["/unable to control " + xml]

def check_xml_status(kanal,marker,url):
        print ('check xml giris:',kanal,marker)
        finalResult=''
        xml=XMLYOLU +'\\'+kanal+'_'+marker+'.xml'
        Sonuc=check_empty_xml(xml)
        if Sonuc == 'YOK':
                print 'XML YOK'
                exec "import "+kanal+" as channel"
                exec "channel.SCAN(marker,url)"
                print 'XML OLUSTURULDU'
        else:
                print 'XML BULUNDU'
                pass

        status=check_time(xml)
        print "XML DOSYA DURUMU : " +str(status)
        if status == "ESKI":
                print "xml dosya = ESKI / YENIDEN TARANIYOR."
                exec "import "+kanal+" as channel"
                exec "channel.SCAN(marker,url)"
                print 'XML YENILENDI'
        
        elif status == "GUNCEL":
                print "VAROLAN XML OKUNUYOR:"+kanal+'_'+marker+'.xml'
                finalResult=open_xml(xml)
        else:
                print 'RECENT SONUC :xml degerlendirilemedi'
        
        return finalResult

def check_empty_xml(xml):
        print xml
        if os.path.isfile(xml):
                Sonuc='VAR'
        else:
                Sonuc='YOK'
       
        return Sonuc

