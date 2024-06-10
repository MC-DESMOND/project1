from customtkinter.windows.widgets.font import CTkFont
from customtkinter.windows.widgets.image import CTkImage
from tkinter.filedialog import askdirectory
from PIL import Image , ImageTk
from selenium import webdriver
import moviepy.editor as edit
from bs4 import BeautifulSoup
import threading as threader
from customtkinter import *
from tkinter import Canvas
from typing import Tuple
from time import sleep
import tkinter
import webbrowser
import requests
import colorama
import os , sys
import pytube 
import time


colorama.init()
colors = colorama.Fore
VideosList = []
Downloadlist = []
result = None
onTime = time.time()

def GlobalInfo(text ,error=False,success=False,color=colors.LIGHTCYAN_EX):
    global onTime
    reset = colors.RESET
    if error:
        color = colors.LIGHTRED_EX
    elif success:
        color = colors.LIGHTGREEN_EX
    print(f"{colors.CYAN}XDownloader {round(time.time()-onTime ,4):2f} {colors.LIGHTRED_EX}::{colors.RESET} {color} {text} {reset}")
    onTime = time.time()


GlobalInfo('-- DESDROID inc --',color=colors.LIGHTRED_EX)
GlobalInfo('LOADING...',color=colors.LIGHTBLUE_EX)



def Async(func):
    global result
    result = None
    def wrapper(*args, **kwargs):
        def f():
            global result
            result = func(*args, **kwargs)
        Function = threader.Thread(target=f)
        GlobalInfo(f"Thread: {func.__name__}")
        Function.start()
        return result
    return wrapper



def path(path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath('.')
    return os.path.join(base_path,path)

@Async
def SetTimeOut(handler,int):
    sleep((int/1000))
    handler()

def GetHTMLContent(playlistUrl , use_requests):
    if use_requests == False:
        driver:webdriver.Chrome
        try:
            driver = webdriver.Chrome()
        except:
            try:
                driver = webdriver.Firefox()
            except Exception as e:
                GlobalInfo('please install Google Chrome or Mozilla Firefox on your system',error=True)
                webbrowser.open_new_tab('https://www.google.com/chrome/')
                exit()
        # driver.minimize_window()
        driver.get(playlistUrl)
        content = driver.page_source.encode('utf-8').strip()
    else:
        res = requests.get(playlistUrl)
        content = res.content
        open('content.html','wb').write(content)
        content = content.decode().encode()
    return content



def ScrapPlaylistContext(playlistUrl):
    content = GetHTMLContent(playlistUrl,False)
    soup = BeautifulSoup(content,'lxml')
    nameofplist = soup.find('yt-formatted-string',id='text',class_="style-scope yt-dynamic-sizing-formatted-string yt-sans-28").text
    titles = soup.findAll('a',id='video-title')
    views  = soup.findAll('yt-formatted-string',id="video-info")
    creator= soup.findAll('a',class_="yt-simple-endpoint style-scope yt-formatted-string")
    images = soup.findAll('img', class_="yt-core-image")
    urls = [i.get('href') for i in titles]
    context = {nameofplist:{}}
    for index,url in enumerate(urls):
        littleContext = {
            "url":f"https://www.youtube.com{url}",
            "title":f"{str(titles[index].text).strip('          ').strip('\n         ')}",
            "video-info":f"{views[index].text}",
            "image":f"{images[index].get('src')}",
            "creator":f"{creator[index].text}"
            
        }
        context[nameofplist][f"playIndex{index}"] = littleContext
    return context

font_color = '#00cccc'
def ontopSaveRead(option = None):
    def offTopReport():
        GlobalInfo(f'To "Keep Window {"off" if '0' in ist else "on"} Top" run Application on Administrator mode',error=True)
    ist = '0'
    try:
        if option == None:
            try:
                with open(path('ist'),'r') as f:
                    ist = f.read()
                    if ist == '':
                        raise 
                    f.close()
            except Exception as e:
                GlobalInfo(e,error=True)
                offTopReport()
                with open(path('ist'),'w') as f:
                    ist = '0'
                    f.write(ist)
                    f.close()
        else:
            with open(path('ist'),'w') as f:
                    ist = str(option)
                    f.write(ist)
                    f.close()
    except Exception as e:
        GlobalInfo(e,error=True)
        offTopReport()
        if option == None:
            pass
        else:
            ist = str(option)

            
    return int(ist)         


class Entry (CTkEntry):
    def __init__(self, master,app, **kwargs):
        super().__init__(
            master, 
            font          = (app.font_family,app.font_size),
            width         = 400,
            height        = 50,
            text_color    = font_color,
            fg_color      = app.fgcolor,
            corner_radius = 10,
            border_color  = '#004555',
            border_width  = 2,
            **kwargs
        )
    def run_grid(self):
        self.grid(row=2,column=1,padx=10,pady=5,columnspan=5)



class LLabel (CTkLabel):
    def __init__(self, master,app:CTk, **kwargs):
        super().__init__(
            master,
            text_color  = '#015C60',
            font        = (app.font_family,app.font_size),
            **kwargs
        )



class RFframe(CTkScrollableFrame):
    def __init__(self,app,master):
        self.RFadjust = 10
        self.RFWidth = (int(app.width/2)-(app.width/app.win_Div))-self.RFadjust
        super().__init__(master,scrollbar_button_color = '#062C3B',scrollbar_button_hover_color='#004E67',fg_color='#04161C',corner_radius=20,height=((app.height-app.console['height'])-35)-self.RFadjust,width=self.RFWidth)



class VideoComponent(CTkFrame):
    def __init__(self,app,link,text,**kwargs):
        self.height = 50
        
        super().__init__(
            app.RightFrame, 
            height=self.height,
            fg_color='transparent',
            width=app.RightFrame.RFWidth,
            corner_radius=20,
            **kwargs
        )
        self.link = link
        self.textAllLength = 25
        self.Index = VideosList.__len__()+1
        self.inVideoListPosition = VideosList.__len__()
        self.calctext = lambda t:(''.join([t[i] for i in range(self.textAllLength)])+'...' if len(t) > self.textAllLength else t)
        self.Text = self.calctext(text)
        self.DownloadAttr = False
        self.font = (app.font_family,15)
        self.IndexLabel = CTkLabel(self,text=self.Index,height=self.height,font=(self.font[0],20))
        self.TextLabel = CTkLabel(self,text=self.Text,font=self.font,width=app.RightFrame.RFWidth-60,height=self.height)
        self.ImageProcessd = Image.open(path('downloadIcon.png'))
        self.downi = CTkImage(dark_image=self.ImageProcessd)
        self.anipd = Image.open(path('anidown.png'))
        self.anid = CTkImage(dark_image=self.anipd)
        self.anipu = Image.open(path('aniup.png'))
        self.aniu = CTkImage(dark_image=self.anipu)
        self.ImageProcessf = Image.open(path('done.png'))
        self.fini = CTkImage(dark_image=self.ImageProcessf)
        self.ImageProcesse = Image.open(path('error.png'))
        self.errori = CTkImage(dark_image=self.ImageProcesse)
        self.iconLabel = CTkLabel(self,image=self.downi,text='',height=self.height)
        self.IndexLabel.grid(row =1,column =1,padx =(10,0))
        self.TextLabel.grid(row=1,column =2)
        self.iconLabel.grid(row=1,column =3,padx =(0,10))
        self.TextLabel.bind('<ButtonPress>',lambda e :self.openGivenLink(self.link))
        self.run_Pack()
        self.run_append()
        self.isanimate = True

    @property
    def icon(self):
        return self.iconLabel._image
    
    @Async
    def openGivenLink(self , link):
        GlobalInfo(f'opening {link}',color=colors.YELLOW)
        webbrowser.open_new_tab(link)
    
    @icon.setter
    def icon(self,icon):
        self.iconLabel.configure(image=icon)

    @Async
    def animate(self):
        while self.isanimate:
            self.icon = self.aniu
            time.sleep(0.5)
            self.icon = self.anid
            time.sleep(0.5)
    
    def unanimate(self):
        self.isanimate = False
        time.sleep(0.5)
        self.icon = self.fini

    @property
    def text(self):
        return self.TextLabel._text
    
    @text.setter
    def text(self,text):
        self.TextLabel.configure(text=self.calctext(text))

    def run_Pack(self):
        self.grid(row=VideosList.__len__()+1, column =1,)
    
    @property
    def DownloadAttr(self):
        return Downloadlist[self.inVideoListPosition]

    @DownloadAttr.setter
    def DownloadAttr(self, attr):
        try:
            Downloadlist[self.inVideoListPosition] = attr
        except:
            Downloadlist.append(attr)
  
    def un_pack(self):
        self.grid_forget()
        
    
    def run_append(self):
        VideosList.append(self)



class Button(CTkButton):
    def __init__(self,master ,**kwargs):
        super().__init__(master,**kwargs)

    @property
    def disabled(self):
        if self._state == 'normal':
            return True
        else:
            return False
    
    @disabled.setter
    def disabled(self,attr):
        if attr:
            self.configure(state = 'normal')
        else:
            self.configure(state = 'disabled')
    
    @property
    def on_click(self):
        return self._command
    
    @on_click.setter
    def on_click(self,command):
        self.configure(command = command)

    @property
    def bgcolor(self):
        return self._fg_color
    
    @bgcolor.setter
    def bgcolor(self,color):
        self.configure(fg_color = color)


class TerminalApp:
    def __init__(self,argv:list) -> None:
        self.isVideo = True
        self.isMp3 = False
        self.url:str
        self.audiofile:str
        self.args:list = argv
        self.isTerminal = True
        self.dlist = []
        self.location = ''
        self.DICTALL = f"""


{colors.RED} ⚠️  please read very well and understand ⚠️ {colors.RESET}
{colors.CYAN}
    first Arg      :    -3 or -4 (blank is -3)  

    second Arg     :    -v or -p (blank is auto) 

    third is video :    url to video or playlist 

    like this      :     XD -3 -v <url> 

{colors.RESET}

        """
        self.initialiseVariables()
    def initialiseVariables(self):
        try:
            if self.args.__len__() == 4:
                if self.args[1].lower() == '-3' or self.args[2].lower() == '-3':
                    self.isMp3 = True
                elif self.args[1].lower() == '-p' or self.args[2].lower() == '-p':
                    self.isVideo = False
                self.url == self.args[3]

            elif self.args.__len__() == 3:
                if self.args[1].lower() == '-3' :
                    self.isMp3 = True
                elif self.args[1].lower() == '-p':
                    self.isVideo = False
                self.url == self.args[2]

            elif self.args.__len__() == 2:
                if self.args[1].lower() == '-h':
                    self.info(self.DICTALL)
                    self.isTerminal = False
                else:
                    self.url == self.args[1]
            else:
                self.isTerminal = False
        except:
            GlobalInfo(self.DICTALL)

        
    
    def info(self,text,error = False,success = False,color = colors.RESET):
        GlobalInfo(text,error,success,color)

    @Async
    def LittleDownload(self,url,location,index=0):
        mp3 = self.isMp3
        try:
            self.dlist.append (False)
            self.info(f'index: {index} is getting video ...')
            video = pytube.YouTube(url)
            vtitle = f"{str(video.title)}"
            self.info(vtitle)
            self.info(f'index: {index} is streaming ...')
            video = video.streams.get_highest_resolution()
            self.info(f'index: {index} is downloading ...')
            videolocation = video.download(location)
            self.info(f'index: {index} downloaded ',success=True)
            if mp3:
                self.info(f'index: {index} is convering video ...') 
                videoForAudio = edit.VideoFileClip(videolocation)
                self.info(f'index: {index} is writing audio ...')
                videoForAudio.audio.write_audiofile(f"{videolocation.replace('.mp4','')}_Audio.mp3")
                self.info(f'index: {index} downloaded ',success=True)
            self.dlist[index] = True
            if False in self.dlist:
                pass
            else:
                self.info(f'downloaded',success=True)
        except Exception as e:
            self.info(e,error = True)
            self.info('Error :: could not find video',error=True)
        if False in self.dlist:
            pass
        else:
            self.info(f'downloaded',success=True)

    def AskTDir(self):
        r = CTk()
        self.info('select a folder.')
        r.title("Choose Directory")
        r.attributes('-topmost',1)
        location = askdirectory()
        r.destroy()
        self.info('good.')
        self.location = location
        return location

    def Download(self):
        link = self.url
        location =self.location
        if self.isVideo:
            self.LittleDownload(url=link,location=location)
        else:
            try:
                self.info('getting playlist ...')
                self.DownloadButtonsState(True)
                context = ScrapPlaylistContext(link)
                playname = list(context.keys())[0]
                originpname = playname
                for i in '!"£$%^&*()_+-=<>?:@{}|\\/;@#¬%`"[]'+"'":
                    originpname = originpname.replace(i,'')
                self.info(originpname)
                
                if '\\' in location:
                    location = location + '\\'
                else:
                    location = location + '/'
                location = location + originpname
                for j,i in enumerate(context[playname].keys()):
                    d = context[playname][i]
                    time.sleep(0.3)
                    
                    self.LittleDownload(url =self.url,location=location,index=j)
            except Exception as e:
                self.info(e,error=True)
                self.DownloadButtonsState(False)
                self.info('input a url to a youtube video',error = True)
                

    def run(self):
        if self.isTerminal:
            self.AskTDir()
            self.Download()
        else:
            raise "NONE"

            
class App(CTk):
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        set_appearance_mode('dark')
        set_default_color_theme('dark-blue')
        #*App Configure
        super().__init__(fg_color, **kwargs)
        
        self.height = 650
        self.width = 900
        self.ADDEDwidth = self.width+10
        self.ADDEDheight = self.height+30
        self.fgcolor = fg_color
        self.isvideo = True
        self.window_center_width = int((int(self.winfo_screenwidth())/2)-(self.width)/2)
        self.window_center_height = int((int(self.winfo_screenheight())/2)-(self.height/2))
        self.geometry(f'{self.ADDEDwidth}x{self.ADDEDheight}+{self.window_center_width}+{self.window_center_height}')
        # self.resizable(False,False)
        self.minsize(self.ADDEDwidth,self.ADDEDheight)
        # self.wm_attributes('-transparent','black')
        # self.state('zoomed') # set the state of the window to full screen with out interupting the task bar
        self.iconbitmap(path('appicon.ico'))
        self.title('XDownloader Pro')
        self.font_family = 'roboto'
        self.font_size = 18
        self.font_color = font_color
        self.font_weight = 'bold'
        self.font_style = 'normal'
        self.font = (self.font_family,self.font_size)
        self.white = '#DBDBDB'
        #* Parents Configure
        self.win_Div = 8
        
        self.base = CTkCanvas(self,bg=self.fgcolor)
        self.base.pack(fill = 'both',expand = True , padx =10,pady = 10)
        self.PackBaseBackgroundImage()
        
        self.root = CTkFrame(self.base,fg_color=self.fgcolor,corner_radius=15)
        self.root.pack(expand = True)
        self.DIip = Image.open(path('logo.png'))
        self.DIImage = CTkImage(self.DIip,size=(30,27))
        self.DESDROIDIdentification = CTkLabel(self.base,text=' DESDROID inc',font=('courier',20),text_color=self.font_color,image=self.DIImage,compound='left')
        self.DESDROIDIdentification.pack(fill = 'x',ipady =10)
        self.console = CTkLabel(self.root,text='INFO ::',font=self.font,height=40,text_color=font_color,corner_radius=10)
        
        self.MainFrame = CTkFrame(self.root,fg_color='transparent',corner_radius=10,height=self.height,width=(int(self.width/2)+(self.width/self.win_Div)-40))
        self.RightFrame = RFframe(self,self.root)
        self.MainFrame.grid(row=1,column =1,rowspan =2)
        self.RightFrame.grid(row=2,column=2,pady=10,padx =(0,10))
        self.console.grid(row =1,column =2,ipadx=10,pady = (10,0))
        
        #* MainFrame children Configure
        self.MainFrameXCenter = int((int(self.width/2)+(self.width/self.win_Div)-10)/2 )
        self.MainFrameYCenter = int(self.height/2 )
        self.ontopVar = IntVar(self.MainFrame,value=ontopSaveRead())
        self.ontopBTN = CTkSwitch(self.MainFrame,command=self.ontopState,variable=self.ontopVar,text_color=self.white,text='Keep Window On Top',button_color='#00BDC6',button_hover_color='#00D8E2',progress_color='#006C83',fg_color='#001C25')
        self.ontopBTN.place(x=30,y=30,anchor = 'nw')
        self.MainChildrenGap = 30

        #* VPswitch and VPchildren Configure
        self.VPBradius = 20
        self.VPSCgap = 8
        self.VPSheight = 50+self.VPSCgap
        self.VPSwidth = 350
        self.VPSwitch = CTkFrame(self.MainFrame,width=self.VPSwidth,height=self.VPSheight,fg_color='#002E3D',corner_radius=self.VPBradius+10)
        self.VPSwitch.place(x=self.MainFrameXCenter,y =(self.MainFrameYCenter-int(self.MainFrameYCenter/2)-(self.VPSheight/2)),anchor='center')
        self.hover_color = '#114E67'
        self.unhover_color = '#002E3D'
        self.isvideoBTN = Button(self.VPSwitch,hover_color=self.hover_color,command=lambda :(self.UpdateIsBTNstate(self.isvideoBTN)),fg_color='#004E67',text='Video',font=(self.font_family,self.font_size),corner_radius=self.VPBradius,width=int(self.VPSwidth/2)-self.VPSCgap*2,height=int(self.VPSheight-self.VPSCgap*2))
        self.isPlayBTN = Button(self.VPSwitch,hover_color=self.hover_color,command=lambda :(self.UpdateIsBTNstate(self.isPlayBTN)),fg_color='transparent',text='Playlist',font=(self.font_family,self.font_size),corner_radius=self.VPBradius,width=int(self.VPSwidth/2)-self.VPSCgap*2,height=int(self.VPSheight-self.VPSCgap*2))
        self.isvideoBTN.grid(row=1,column = 1,pady =self.VPSCgap ,padx = self.VPSCgap)
        self.isPlayBTN.grid(row=1,column = 2,pady = self.VPSCgap,padx = (0,self.VPSCgap))

        #*LinkLabels And Entrys
        self.LinkParent = CTkFrame(self.MainFrame,fg_color='transparent')
        self.LinkParent.place(x=self.MainFrameXCenter,y =(self.MainFrameYCenter-int(self.MainFrameYCenter/2)+self.MainChildrenGap),anchor='n')
        self.LinkLabel = LLabel(self.LinkParent,app=self,text='YouTube Link')
        self.linkEntry = Entry(self.LinkParent,app = self, )
        self.LinkLabel.grid(row=1,column=1,padx=10,pady=5)
        self.linkEntry.run_grid()

        #*LocationLabels And Entrys
        self.LocParent = CTkFrame(self.MainFrame,fg_color='transparent')
        self.LocParent.place(x=self.MainFrameXCenter,y =(self.MainFrameYCenter-int(self.MainFrameYCenter/7)+self.MainChildrenGap),anchor='n')
        self.LocLabel = LLabel(self.LocParent,app=self,text='local Location')
        self.LocEntry = Entry(self.LocParent,app = self, )
        self.BrowseBTN = Button(self.LocParent,text='browse',font=(self.font[0],self.font[1]-3),fg_color='#00424B',corner_radius=20,width=110,height=35)
        self.BrowseBTN.grid(row=3,column =1,pady=(10,0))
        self.BrowseBTN.on_click = self.askdir
        self.LocLabel.grid(row=1,column=1,padx=10,pady=5)
        self.LocEntry.run_grid()

        
        #* RightFrame children Configure
        self.RightFrameXCenter = int((int(self.width/2)-(self.width/self.win_Div))/2 )
        self.RightFrameYCenter = int(self.height/2 )

        #* Download BTN configure
        self.DWBradius = 25
        self.DWSCgap = 8
        self.DWSheight = 50+self.DWSCgap
        self.DWSwidth = 450
        self.DWSwitch = CTkFrame(self.MainFrame,width=self.DWSwidth,height=self.DWSheight,fg_color='#011B20',corner_radius=self.DWBradius+10)
        self.DWSwitch.place(x=self.MainFrameXCenter,y =(self.MainFrameYCenter+int(self.MainFrameYCenter/2)+(self.DWSheight/2)),anchor='center')
        self.hover_color = '#03595F'
        self.unhover_color = '#002E3D'
        self.ismp4BTN = Button(self.DWSwitch,hover_color=self.hover_color,fg_color='#013D41',text='Download mp4',font=(self.font_family,self.font_size),corner_radius=self.DWBradius,width=int(self.DWSwidth/2)-self.DWSCgap*2,height=int(self.DWSheight-self.DWSCgap*2))
        self.ismp34BTN = Button(self.DWSwitch,hover_color=self.hover_color,fg_color='transparent',text='Download mp3 & mp4',font=(self.font_family,self.font_size),corner_radius=self.DWBradius,width=int(self.DWSwidth/2)-self.DWSCgap*2,height=int(self.DWSheight-self.DWSCgap*2))
        self.ismp4BTN.grid(row=1,column = 1,pady =self.DWSCgap ,padx = self.DWSCgap)
        self.ismp34BTN.grid(row=1,column = 2,pady = self.DWSCgap,padx = (0,self.DWSCgap))
        self.ismp4BTN.on_click = lambda :self.download()
        self.ismp34BTN.on_click = lambda :self.download(True)
        self.info('start XDownloading')
        self.ontopState()

    def ontopState(self):
        value = self.ontopBTN.get()
        self.ontopVar.set(value)
        ontopSaveRead(value)
        self.attributes('-topmost',value)
        if value ==1:
            self.ontopBTN.configure(
                text_color = self.font_color
            )
        else:
            self.ontopBTN.configure(
                text_color = self.white
            )

    def askdir(self):
        folder = askdirectory()
        self.LocEntry.insert(0,folder)

    def UpdateIsBTNstate(self,e:Button):
        if e._text == 'Video':
            self.isvideo = True
        elif e._text == 'Playlist':
            self.isvideo = False
        self.isvideoBTN.configure(fg_color='transparent')
        self.isPlayBTN.configure(fg_color='transparent')
        e.configure(fg_color='#004E67')

    
    def PackBaseBackgroundImage(self):
            size = (int(self.winfo_screenwidth()),int(self.winfo_screenheight()))
            self.baseImage = Image.open(path('background.png'))
            self.baseImage = self.baseImage.resize(size)
            self.baseBg = CTkImage(dark_image=self.baseImage,size=size)
            self.imagelabel = CTkLabel(self.base,image = self.baseBg)
            self.baseMainBg = self.base.create_window(0,0,window=self.imagelabel,anchor='nw')

    def updatePBBI(self):
        size = (int(self.winfo_screenwidth()),int(self.winfo_screenheight()))
        self.baseImage = Image.open(path('background.png'))
        self.baseImage = self.baseImage.resize(size)
        self.baseBg = CTkImage(dark_image=self.baseImage,size=size)
        self.imagelabel.configure(image = self.baseBg )

    def OnSizeShifted(self):
        self.updatePBBI()

    @Async
    def DownloadButtonsState(self,disabled = False):
        self.ismp4BTN.disabled = not disabled
        self.ismp34BTN.disabled = not disabled
        
        if disabled:
            self.ismp4BTN.on_click = None
            self.ismp34BTN.on_click = None
        else:
            self.ismp4BTN.on_click = lambda :self.download()
            self.ismp34BTN.on_click = lambda :self.download(True)
            self.ismp4BTN.bgcolor = '#013D41'
            self.ismp4BTN.color = 'white'
            self.ismp34BTN.bgcolor = 'transparent'
            self.ismp34BTN.color = 'white'
    @Async
    def LittleDownload(self,url,location,mp3=False):
        self.DownloadButtonsState(True)
        videoTag =  VideoComponent(self,text=url,link=url)
        videoTag.animate()
        try:
            self.info(f'index: {videoTag.Index} is getting video ...')
            video = pytube.YouTube(url)
            vtitle = f"{str(video.title)}"
            videoTag.text = vtitle
            self.info(f'index: {videoTag.Index} is streaming ...')
            video = video.streams.get_highest_resolution()
            self.info(f'index: {videoTag.Index} is downloading ...')
            videolocation = video.download(location)
            self.info(f'index: {videoTag.Index} downloaded ',success=True)
            if mp3:
                self.info(f'index: {videoTag.Index} is convering video ...') 
                videoForAudio = edit.VideoFileClip(videolocation)
                self.info(f'index: {videoTag.Index} is writing audio ...')
                videoForAudio.audio.write_audiofile(f"{videolocation.replace('.mp4','')}_Audio.mp3")
                self.info(f'index: {videoTag.Index} downloaded ',success=True)
            videoTag.DownloadAttr = True
            videoTag.unanimate()
            videoTag.icon = videoTag.fini
            if False in Downloadlist:
                pass
            else:
                self.DownloadButtonsState(False)
                self.info(f'downloaded',success=True)
        except Exception as e:
            GlobalInfo(e)
            self.DownloadButtonsState(False)
            videoTag.isanimate = False
            videoTag.icon = videoTag.errori
            self.info('Error :: could not find video',error=True)
        videoTag.DownloadAttr = True
        if False in Downloadlist:
            pass
        else:
            self.DownloadButtonsState(False)
        
        videoTag.isanimate = False
        
    @Async
    def info(self,text:str,error = False,success = False):
        textfilter = f'INFO :: {text.title()}'
        self.console.configure(text = textfilter)
        if error:
            self.console.configure(fg_color='red',text_color = 'black')
            time.sleep(2)
            self.console.configure(text_color = '#ff0000')
        elif success:
            self.console.configure(fg_color='#00aa00',text_color = 'black')
            time.sleep(2)
            self.console.color = '#00ff00'
            self.console.configure(text_color = '#00ff00')
        else:
            self.console.configure(fg_color='#00ffff',text_color = '#000000')
            time.sleep(2)
            self.console.color = '#00ffff'
            self.console.configure(text_color = '#00ffff')
        self.console.configure(fg_color=self.fgcolor)

    @Async
    def download(self,mp3=False):
        self.VideoListClear()
        if self.linkEntry.get().strip() == '' or self.LocEntry.get().strip() == '' :
                if self.linkEntry.get().strip() == '':
                    self.info('input a url to a youtube video',error = True)
                elif self.LocEntry.get().strip() == '':
                    self.info('input the video location',error = True)
        else:
            link = self.linkEntry.get()
            location = self.LocEntry.get()
            if self.isvideo:
                self.LittleDownload(url=link,location=location,mp3=mp3)
            else:
                try:
                    self.info('getting playlist ...')
                    self.DownloadButtonsState(True)
                    context = ScrapPlaylistContext(link)
                    playname = list(context.keys())[0]
                    originpname = playname
                    for i in '!"£$%^&*()_+-=<>?:@{}|\\/;@#¬%`"[]'+"'":
                        originpname = originpname.replace(i,'')
                    GlobalInfo(originpname)
                    
                    if '\\' in location:
                        location = location + '\\'
                    else:
                        location = location + '/'
                    location = location + originpname
                    for j,i in enumerate(context[playname].keys()):
                        d = context[playname][i]
                        time.sleep(0.3)
                        
                        self.LittleDownload(url = d.get('url'),location=location,mp3=mp3)
                except Exception as e:
                    GlobalInfo(e)
                    self.DownloadButtonsState(False)
                    self.info('input a url to a youtube video',error = True)
                    

    def VideoListClear(self):
        for i in VideosList:
            i.un_pack()
        Downloadlist.clear()
        VideosList.clear()

    def run(self):
        self.mainloop()

