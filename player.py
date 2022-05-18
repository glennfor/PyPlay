
from utils import *


isAudioFile = lambda file: os.path.splitext(file)[-1] in SUPPORTED_EXTENSIONS 

class AudioPlayerControls(object):
    def __init__(self):
            #initliases all imported modules
        pygame.init()
        pygame.mixer.pre_init()
        pygame.mixer.init()#(frequency = 22050, size = 16, channels = 2, buffer = 4096)
        self.is_playing = False
        self._default_volume = 0.5
        pygame.mixer.music.set_volume(self._default_volume)
        self.current = -1
        self.playlist = []
        sample_music = [os.path.join(PATH_TO_SAMPLE_MUSIC,file) for file in os.listdir(PATH_TO_SAMPLE_MUSIC) if isAudioFile(file)]
        self.playlist += sample_music
        self.start=0

        self.timer = tkinter.StringVar(value = ' [00:00] ')#how long has the song played so far
        self.length_of_current_song = tkinter.StringVar()#length of song being played
        self.song_len=tkinter.IntVar()
        
        self.current_song = tkinter.StringVar(value=self.playlist[self.current])

        #[when playback stops]
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

        #[set whether or not a song should be repeated
        self.loop = False

        #[handle commmand line args]
        if len(sys.argv) > 1:
            for item in sys.argv[1:]:
                if os.path.isfile(item):
                    if self._isaudiofile(item):
                        self.playlist.append(item)
                elif os.path.isdir(item):
                    self._add_to_list(item)

        #[a single  thread to take care of checking for a stop in playng the song
        thread1=threading.Thread(target=self.play_list_repeat)
        thread1.start()
        
    def add_file(self):
        pass
    
    def _add_to_list(self, directory):
        if not os.path.exists(directory):
            return
        for file in list(filter(lambda file: self._isaudiofile(file),
                                os.listdir(directory))):
            self.playlist.append(os.path.join(directory, file))


    def create_playlist(self):
        #self.current = 0
        dir_path = tkinter.filedialog.askdirectory(initialdir=os.environ['USERPROFILE'])
        self._add_to_list(dir_path)
                    
    def play(self, song):
        #self.current_song.set(self.playlist[self.current])
        self.is_playing = True
        try:
            self.start=0
            mlen=340
            
            self.song_len.set(mlen)#use in the progressbar
            
            self.length_of_current_song.set(' [{:02d}:{:02d}] '.format(int(mlen//60), round(mlen%60)))
            pygame.mixer.music.load(song) 
            pygame.mixer.music.play(loops=self.loop)
        except pygame.error as problem:
            tkinter.messagebox.showerror('Error', problem)
            print(problem)
            self.playlist.remove(song)

            self.playnext()
        else:
            #threading.Thread(target=self.play_list_repeat).start()
            pass #for now
        finally:
            pass
        #when playing all
        #self.current += 1
        #self.current %= len(self.playlist)
        #if play all
        #pygame.mixer.music.queue(self.playlist[self.current])
        
    def play_list_repeat(self):#update the timer variable here maybe
        print('checking...')
        self.checking = True
        while self.checking:
           for event in pygame.event.get():
                if event.type==pygame.USEREVENT:
                    print('boom->got it')
                    print('THIS SONG HAS ENDED <{}>'.format(self.playlist[self.current]))
                    self.playnext()
                    print('No Exit--Now {} threads are running'.format(threading.active_count()))
                    break
        print('Exit Passed--Now {} threads are running'.format(threading.active_count()))
        

    def pause(self):
        pygame.mixer.music.pause()
        self.is_playing=False

    def resume(self):
        pygame.mixer.music.unpause()
        self.is_playing=True

    def playnext(self):

        #this functions sets an explicit stop before moving on
        #pygame.mixer.music.stop()
        self.current += 1

        if(len(self.playlist)==0):return

        self.current %= len(self.playlist)
        self.current_song.set(self.playlist[self.current])
        #donot handle playing error, leave the gui to do so
        self.play(self.playlist[self.current])
        #self.timer.set(' [00:00] ')
        self.start=0
        #pygame.mixer.music.queue(self.playlist[(self.current+1)%len(self.playlist)])
        if not self.is_playing:
            self.pause()
        
        
    def playprev(self):
        self.current -= 1
        self.current %= len(self.playlist)
        self.current_song.set(self.playlist[self.current])
        self.play(self.playlist[self.current])
        if not self.is_playing:
            self.pause()
        
        
    def restart(self):
        #start back the current song
        #simply by loading back the current song and palying it
        self.current_song.set(self.playlist[self.current])
        self.play(self.playlist[self.current])
        
        
    def rewind(self, pos):
        relpos = pos
        try:
            cur_pos= pygame.mixer.music.get_pos()
            pygame.mixer.music.set_pos(cur_pos-relpos)
        except:
            self.restart()
    def fast_forward(self, pos):
        relpos = pos
        try:
            cur_pos= pygame.mixer.music.get_pos()
            pygame.mixer.music.set_pos(cur_pos+relpos)
        except:
            print('cannot fast forward anymore')

    def tell_pos(self):
        return pygame.mixer.music.get_pos()

    def seek(self, offset):
        pygame.mixer.music.set_pos(offset)
        
    def shuffle(self):
        #shuffle play list
        pass

    def order(self):
        #play the songs in order
        pass

    def play_all(self):
        pass

    def repeat(self):
        self.loop=True

    def repeat_all(self):
        pass
    
    def set_volume(self, vol):
        #from a slider
        pygame.mixer.music.set_volume(vol)
        
    def stop(self):
        pygame.mixer.music.fadeout(4000)
        #pygame.mixer.music.stop()

            
    def show_list(self):
        pass
        #use options menu

    def quit_(self):
        self.checking = False
        pygame.mixer.quit()
        pygame.quit()









class MusicPlayer(object):
    def __init__(self):
      
        Digital_Clock_Font_Setting=("DS_Digital",20 ,"bold")
        Songs_playing_Font_Setting="Verdana 13"
        duration_time_Font_Setting="arial 10"

        #PlayerWindow
        #self.window = tkinter.Tk()
        self.window = ttkthemes.ThemedTk(theme='equilux')
        #self.window.wm_attributes('-alpha', 0.3)
        self.window.wm_title('PyPlay ~ Python Music Player')
        self.window.minsize(width=800, height=450)
        self.window.iconbitmap(PATH_TO_ICON)
        self.frame = tkinter.Frame(self.window)
        self.frame.pack(fill=tkinter.BOTH, expand=True)
        self.style = ttk.Style()
  
        #[MAIN DATA]
        #controls object

        self.PlayerControls =  AudioPlayerControls()
        #[play song when player starts]
        self.PlayerControls.playnext()
        
        self.volume = tkinter.IntVar(value=self.PlayerControls._default_volume*100)
        self.repeat = tkinter.IntVar(value=-1)#currently as repeat all
        
        self.slist=[os.path.basename(os.path.splitext(f)[0]) for f in self.PlayerControls.playlist]

        #[check every second, if song is done play next]
        #self.window.after(1000, self.PlayerControls.play_list_repeat)
        def on_volume_change(var, index, mode):
            self.PlayerControls.set_volume(round(float(self.volume.get()/100), 1))
            if float(self.volume.get())/100 == 0.00:
                self.mute_button.configure(image=self.muteicon)
                self.mute_button.icon=self.muteicon
            elif float(self.volume.get())/100 > 0.0 and self.mute_button.icon==self.muteicon:
                self.mute_button.configure(image=self.unmuteicon)
                self.mute_button.icon=self.unmuteicon
    

        
        self.PlayerControls.current_song.trace('w', lambda v, i ,m :self.create_label())
        self.prev=0#traces the index of the song last played

        self.PlayerControls.current_song.trace_add("write", lambda v, i ,m:self._update_list())
        self.volume.trace('w', on_volume_change)

        def update_len():
            self.progressbar['maximum']=self.PlayerControls.song_len.get()
            
        #self.PlayerControls.song_len.trace('w', lambda v, i, m:update_len())
        
        self.stats={'song':tkinter.StringVar(), 'timer':tkinter.StringVar()}
        
        self.style.configure('x.TLabel', height=3, borderwidth=10, relief=tkinter.RAISED)
        self.style.configure('stat2.TLabel', anchor=tkinter.W, justify=tkinter.LEFT, font=Digital_Clock_Font_Setting,width=14)
        self.style.configure('stat1.TLabel', anchor=tkinter.E, font=Digital_Clock_Font_Setting, width=14)
        self.style.configure('vol.Horizontal.TScale',  label = 'Volume',showvalue=True)
        self.style.configure('progress.Horizontal.TProgressbar', anchor='center')

        #[CONTAINERS]componenets of the window (containers)
        self.controlsframe =ttk.Frame(self.frame)
        self.canvas = tkinter.Canvas(self.frame, width=600, height=400, bg='#002020')

        self.statsframe = ttk.Frame(self.frame)#holds the progressbar, timer and lenght
        #maximum = current song lenght
        #

        
        ttk.Label(self.statsframe,style='stat1.TLabel',font=Digital_Clock_Font_Setting,
                  textvariable=self.PlayerControls.timer).pack(side=tkinter.LEFT)#, variable = self.PlayerControls.timer


        ttk.Label(self.statsframe, style='stat2.TLabel',font=Digital_Clock_Font_Setting,
                  textvariable=self.PlayerControls.length_of_current_song).pack(side=tkinter.RIGHT)
        self.progressbar=ttk.Progressbar(self.statsframe, mode='determinate', cursor='plus'
                        ,maximum=self.PlayerControls.song_len.get(),
                         style='progress.Horizontal.TProgressbar',
                        length = self.window.winfo_screenwidth()//1.8,
                        orient=tkinter.HORIZONTAL)
        self.progressbar.pack(side=tkinter.RIGHT, expand=True)

        try:
            #self.animatethread = threading.Thread(target=lambda:self.animate())#, kwargs={'speed':10})
            self.timerthread=threading.Thread(target=self.update_timer_progress)
            self.timerthread.start()
##            self.timerthread.join()
            #self.animatethread.start()
            print('REVALUTE THIS PART')
        except RuntimeError as err:
            print('\n-------------------------------')
            print('Interpreter Lock-Thread failed')
            print('-------------------------------')
            print(err)
            print('-------------------------------\n\n')



        #[update the progress bar every second]
        #self.statsframe.after(1000,self.update_timer_progress)
        
        #stats frame components
        self.statslabel = ttk.Label(self.frame,style='x.TLabel',
                    text='FROM JG::PO SOFT ~~ PYSOUND $$ AUDIO<->MUSIC PLAYER',
                                      font = ('Courier New', 18, 'bold'))
       

        #controls
        #play and pause icons swap onclick also(mute and unmute)

       # self.controls={}
       # self.controls['volume'] = Scale(self.frame, from_=0, to=100)
        self.init_win()

        #[BINDINGS]
        #self.window.bind('<space>', lambda ev:self.toggle_pause())
        
        #self.window.bind('<Key>', lambda ev:self.PlayerControls.toggle_pause() if ev.keysym==' ')
        self.window.bind('<Left>', lambda ev:self.PlayerControls.playprev())
        self.window.bind('<Right>', lambda ev:self.PlayerControls.playnext())
        'volume'
##      self.window.bind('<Up>', lambda ev:self.PlayerControls.inc_vol)
##      self.window.bind('<Down>', lambda ev:self.PlayerControls.dec_vol)
##        
        self.canvas.bind('<Button-3>', self.pop_up)
        self.window.protocol('WM_DELETE_WINDOW', self.exitplayer)
        
        
    def init_win(self):
       
        add_fileicon=tkinter.PhotoImage(file="./assets/Icons/add_file.gif")
        add_directoryicon=tkinter.PhotoImage(file="./assets/Icons/add_directory.gif")
        exiticon=tkinter.PhotoImage(file="./assets/Icons/exit.gif")
        
        self.playicon=tkinter.PhotoImage(file="./assets/Icons/play.gif")
        self.pauseicon=tkinter.PhotoImage(file="./assets/Icons/pause.gif")
        
        stopicon=tkinter.PhotoImage(file="./assets/Icons/stop.gif")
        rewindicon=tkinter.PhotoImage(file="./assets/Icons/rewind.gif")
        fast_forwardicon=tkinter.PhotoImage(file="./assets/Icons/fast_forward.gif")
        previous_trackicon=tkinter.PhotoImage(file="./assets/Icons/previous_track.gif")
        next_trackicon=tkinter.PhotoImage(file="./assets/Icons/next_track.gif")
        
        self.muteicon=tkinter.PhotoImage(file="./assets/Icons/mute.gif")
        self.unmuteicon=tkinter.PhotoImage(file="./assets/Icons/unmute.gif")
        
        delete_selectedicon=tkinter.PhotoImage(file="./assets/Icons/delete_selected.gif")

        
        conframe, volframe = ttk.Frame(self.controlsframe),ttk.Frame(self.controlsframe)
        tips=['Add file', 'Add folder', 'Stop playback', 'Rewind','Previous track'
              ]
        for i, (icon, cmd) in enumerate([(add_fileicon,self.PlayerControls.add_file),
                                (add_directoryicon,self.PlayerControls.create_playlist),
                                (stopicon, self.PlayerControls.stop)
                                  ,(rewindicon, lambda:self.PlayerControls.rewind(0.5))
                                  ,(previous_trackicon, self.PlayerControls.playprev)],start=0):                    
            button=ttk.Button(conframe, image=icon, command = cmd)
            create_tool_tip(button, tips[i])
            button.grid(row=0,column=i,padx=4, pady=2)
            button.icon=icon

            #play button
        self.play_button=ttk.Button(conframe, image=self.pauseicon, command = self.toggle_pause)
        create_tool_tip(self.play_button, 'Play|Pause')
        self.play_button.icon = self.pauseicon
        self.play_button.grid(row=0,column=5, padx=6, pady=2)

        tips=['Next track', 'Fast forward', 'Remove from list', 'Exit'
              ]
        for i, (icon, cmd) in enumerate([(next_trackicon, self.PlayerControls.playnext),
                                         (fast_forwardicon, lambda:self.PlayerControls.fast_forward(0.5))
                                          ,(delete_selectedicon, lambda:print("Dummmy For Now\4567")),
                                         (exiticon, self.exitplayer)], start=6):
            button=ttk.Button(conframe, image=icon, command = cmd)
            create_tool_tip(button, tips[i-6])
            button.grid(row=0,column=i,padx=4, pady=2)
            button.icon=icon

                                        
        #mute//umute button
        self.mute_button=ttk.Button(volframe, image=self.unmuteicon, command = self.toggle_mute)
        self.mute_button.grid(row=0,padx=4, pady=2)
        self.mute_button.icon=self.unmuteicon
        create_tool_tip(self.mute_button, 'Mute|Unmute')
         #[volume scale]
        self.volscale = ttk.Scale(volframe, from_=0, to=100, orient = tkinter.HORIZONTAL,style='vol.Horizontal.TScale',variable=
                                  self.volume, command=lambda ev:self.PlayerControls.set_volume(round(float(self.volume.get()/100),1)))
        self.volscale.grid(row=0,column=1,padx=4, pady=2)
        create_tool_tip(self.volscale, 'Volume')
        
        conframe.pack(side = tkinter.RIGHT, expand=True)
        volframe.pack(side=tkinter.RIGHT)
          
        
        #[Canvas]
        self.canvas.image = ImageTk.PhotoImage(Image.open(PATH_TO_CANVAS_IMAGE).resize((400,400)))
        self.canvas.create_image(self.canvas.winfo_screenwidth()//4,
                   0, image = self.canvas.image, anchor="nw")

        self.create_label()

        #[LABEL]
        #[GRID OUT]
        self.controlsframe.pack(fill=tkinter.X, side=tkinter.TOP)
        self.statsframe.pack(fill=tkinter.X)
        self.canvas.pack(fill = tkinter.BOTH,expand=True)
        self.statslabel.pack(fill=tkinter.X, side = tkinter.BOTTOM )

    def toggle_pause(self):
        #controls playing and pausing
        if self.PlayerControls.is_playing:                   
            self.PlayerControls.pause()
            self.play_button.configure(image=self.playicon)
            self.play_button.icon=self.playicon
            
        else:
            self.PlayerControls.resume()
            self.play_button.configure(image=self.pauseicon)
            self.play_button.icon=self.pauseicon


    def toggle_mute(self):
        if round(float(self.volume.get())/100,1)<0.02:
                #alreadymute
                self.volume.set(self.PlayerControls._default_volume*100)
                self.mute_button.configure(image=self.unmuteicon)
                self.mute_button.icon=self.unmuteicon
        else:
                self.volume.set(0.0)
                self.mute_button.configure(image=self.muteicon)
                self.mute_button.icon=self.muteicon
                
    def create_label(self):
        def click(ev):
            print('at >',(ev.x, ev.y))
        self.canvas.delete('song')

        #self.canvas.bind('<Button-1>', click)
        self.canvas.update_idletasks()
        self.window.update_idletasks()
        w = int(self.canvas['width'])
        h = int(self.canvas['height'])
        #print(w,h)
        self.canvas.create_text(405, 30,
                                text='Now Playing ...', fill='skyblue', font='times 30 bold', tag='play')
        col = random.choice(['coral1', 'coral4', 'wheat2', 'burlywood2', 'sienna3','Rosybrown3',
                             'cyan3','alice blue', 'blue', 'linen', 'snow','green yellow'])
        self.canvas.create_text(170,150,anchor=tkinter.SW, 
                text= os.path.basename(os.path.splitext(self.PlayerControls.current_song.get())[0]),
                    fill=col,font='times 25', tag='song')


    def create_menu(self):
        self.menubar = tkinter.Menu(self, font=('script MT bold', 15, 'bold italic'))
        self.menubar.add_cascade(self.menubar, text= 'Open  Music Folder', command=self.opendir)

    def animate(self, speed=0):
        #tix.Ballon()
        '''print(speed)
        self.stop = False
        self.canvas.create_oval(200, 400,100,100, fill='white', outline='blue', tag='me')
        #self.canvas.create_text(200, 400, text='PYSOUND from JG-P..O..', font='elephant 38 bold', anchor=tkinter.NW,
         #                       fill='tomato', activefill='saddle brown', activestipple='gray55', tag='me')
        '''
        self.stop=False
        x,  y = 200, 400
        while True:
            if self.stop:
                break
            
            #self.canvas.coords('me', x, y)
            #time.sleep(0.3)
            #x = (x+10)%1000 + 200
            
            for i in range(25):
                x, y = random.randint(40, 100), random.randint(40, 100)
                w, h = random.randint(40, 500), random.randint(40, 500)
                cols =['green', 'red', 'white', 'blue', 'pink','aqua', 'skyblue', 'brown',
                       'khaki', 'violet', 'teal', 'olive', 'yellow']
                color = random.choice(cols) ,random.choice(cols),
                self.canvas.create_oval(x,y,w,h, fill=color[0], outline=color[1], tag=f'{i}')
                self.canvas.delete('{}'.format(random.randint(1, 100)))
            

    def _update_list(self):
        try:
            self.song_list.activate(self.PlayerControls.current)
            self.song_list.selection_clear(0, tkinter.END)#len(self.slist))
            self.song_list.see(self.PlayerControls.current)
            #self.song_list.selection_set(self.PlayerControls.current)
           
            self.song_list.itemconfig(self.prev
                                      , background='#EEE', foreground='black',
                                      selectbackground=self.song_list['selectbackground']
                                      ,selectforeground=self.song_list['selectforeground'])
                
            
            self.song_list.itemconfig(self.PlayerControls.current
                                      , background='#454545', foreground='#64EEAA',
                                      selectbackground='#0000CC',selectforeground='white')
            self.prev=self.PlayerControls.current
        except NameError:
            pass
        except AttributeError:
            pass

        
    def show_list(self):
        '''
        This function shows the list of playing songs and can be invoked by choosing
        and option from the right click
        '''
        self.slist=[os.path.basename(os.path.splitext(f)[0]) for f in self.PlayerControls.playlist]
        self.song_list = ttk.tkinter.Listbox(self.frame, selectmode = tkinter.SINGLE,width=32, foreground='#202000',
                                 background='#efefef',activestyle=tkinter.DOTBOX,selectforeground='#20FFFF',
                                 height=15,highlightcolor='teal', font=('doulos sil', 13))
        for pos, song in enumerate(self.slist):
            self.song_list.insert(pos,song)
        self.song_list.bind('<Double-Button-1>', lambda *ignore:self.on_dblclick())
        self.canvas.create_window(700,6,anchor=tkinter.NW,window = self.song_list, tag='list')
       
        self._update_list()
            
    def hide_list(self):
        self.canvas.delete('list')
        
    def pop_up(self, event):
        '''
        The pop up menu for use to show list, next song etc
        The event is obviously a mouse right click
        '''
        self.__create_pop_up_menu()
        self.pop_menu.tk_popup(event.x_root+10, event.y_root+5)
        #or
        #self.pop_menu.post(ev.x_root, ev.y_root)
    def __create_pop_up_menu(self):
        list_font = ('gabriola', 13, 'italic bold')
        
        self.pop_menu = tkinter.Menu(self.window, tearoff=0)
        for text, task in [('Show Playlist', self.show_list), ('Hide Playlist',self.hide_list),
                           ('Next',self.PlayerControls.playnext), ('Previous',self.PlayerControls.playprev),
                           ('Play/Pause',self.toggle_pause)]:
            self.pop_menu.add_command(label=text, font = list_font , command = task)#self.user.next
        self.pop_menu.add_checkbutton(label='Shuffle' ,font = list_font ,command=self.PlayerControls.shuffle)
        self.pop_menu.add_radiobutton(label='Repeat Current Song', font = list_font , value=1, variable = self.repeat, command=self.PlayerControls.repeat)
        self.pop_menu.add_radiobutton(label='Repeat List', font = list_font , value=-1, variable = self.repeat,command=self.PlayerControls.repeat_all)
        self.pop_menu.add_radiobutton(label='Turn Off Repeat', font = list_font , variable = self.repeat,value=0)

    def update_timer_progress(self):
        #update the time if and only if the song is being played currently
        self.stop=False
        while not self.stop:
            t=self.PlayerControls.start
            if self.PlayerControls.is_playing:

                #or simply sleep for a second
                #time.sleep(1)
                p=time.time()
                while time.time()-p < 1.0:
                    time.sleep(.9)
                self.PlayerControls.start += 1
                try:
                    self.progressbar['value']=t
                    self.PlayerControls.timer.set(' [{:02d}:{:02d}] '.format(t//60, round(t%60)))
                except (tkinter.TclError, RuntimeError) as err:
                    print(']]]]]]]]]]]]]]]]]]]')
                    print('Timer update error-->>',err)
                    print('[[[[[[[[[[[[[[[[[[[')
              
    def exitplayer(self):
        if tkinter.messagebox.askyesnocancel('Quit Player', 'Are You Sure You Want to Quit This Player?'):
            self.stop = True
            #write code to stop all threads
            self.PlayerControls.checking=False #stop checking for song ending
            self.PlayerControls.stop()
            self.PlayerControls.quit_()
            time.sleep(0.5)#wait for threads to round off
            self.window.quit()
            self.window.destroy()
            sys.exit(0)
            
    def on_dblclick(self):
        #double clicking in the listbox
        try:
            index=self.song_list.curselection()[0]
        except IndexError:
            return
        self.PlayerControls.current=index-1
        try:
            self.PlayerControls.playnext()
        except LookupError:
            self.show_list()
        self._update_list()  
    def run(self):
        self.window.mainloop()


