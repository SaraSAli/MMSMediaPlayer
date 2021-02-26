from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from mutagen.mp3 import MP3
import time
from tkinter import messagebox
import pygame
from moviepy.editor import *

pygame.mixer.init()


class GUI:
    def __init__(self, master):
        self.master = master

        pygame.init()

        master.title('MMS Music Player')
        master.iconbitmap('images/Music.ico')
        master.geometry('600x500')
        master.resizable(0, 0)

        ## Create Master Frame
        self.master_frame = Frame(master)
        self.master_frame.pack()

        ##Label
        self.label = Label(self.master_frame, text='Music Player')
        self.label.pack(pady=10)

        ##Buttons Frame
        self.buttonFrame = Frame(self.master_frame)
        self.buttonFrame.pack()

        self.topframe = Frame(self.master_frame)
        self.topframe.pack()

        ##Volume Frame
        self.volumeframe = LabelFrame(self.topframe, text='Volume')
        self.volumeframe.grid(row=0, column=1, pady=20, padx=10)

        ##Design and Create Mute Button
        self.muteImg = PhotoImage(file='images/mute.png')
        self.muteButton = Button(self.volumeframe, image=self.muteImg, command=self.mute).grid(row=0, column=0, padx=10)

        ##Design and Create Unmute Button
        self.unmuteImg = PhotoImage(file='images/vol.png')
        ummuteButton = Button(self.volumeframe, image=self.unmuteImg, command=self.unmute).grid(row=2, column=0)

        ##Create Volume Slider
        self.volume_slider = Scale(self.volumeframe, from_=0, to=1, orient=VERTICAL, value=1, command=self.volume,
                                   length=80)
        self.volume_slider.grid(row=1, column=0, pady=10)

        ##List box
        self.songBox = Listbox(self.topframe, width=50, bg='grey', fg='green', selectbackground='white',
                               selectforeground='black')
        self.songBox.grid(row=0, column=0, pady=20)

        ##Song Duration Label
        self.timeLabel = Label(self.master_frame, text='Time Elapsed: 00:00:00 of 00:00:00', relief=GROOVE, anchor=E)
        self.timeLabel.pack()

        ##Song Progress Slider
        self.my_slider = Scale(self.master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=self.slide,
                               length=360)
        self.my_slider.pack(pady=15)

        ##Create Frame Which Contains Buttons
        self.controlFrame = Frame(self.master_frame)
        self.controlFrame.pack(pady=15, padx=15)

        ##Design Buttons
        self.playBtnImg = PhotoImage(file='images/Play.png')
        self.backBtnImg = PhotoImage(file='images/prev.png')
        self.stopBtnImg = PhotoImage(file='images/stop.png')
        self.forwardBtnImg = PhotoImage(file='images/next.png')
        self.pauseBtnImg = PhotoImage(file='images/pause.png')

        ##Create Player Control Buttons
        self.pause_button = Button(self.controlFrame, image=self.pauseBtnImg, command=self.pause_song).grid(row=0,
                                                                                                            column=2)
        self.play_button = Button(self.controlFrame, image=self.playBtnImg, command=self.play_song).grid(row=0,
                                                                                                         column=1)
        self.prev_button = Button(self.controlFrame, image=self.backBtnImg, command=self.previous_song).grid(row=0,
                                                                                                             column=0)
        self.stop_button = Button(self.controlFrame, image=self.stopBtnImg, command=self.stop_song).grid(row=0,
                                                                                                         column=3)
        self.next_button = Button(self.controlFrame, image=self.forwardBtnImg, command=self.next_song).grid(row=0,
                                                                                                            column=4)

        self.addToList = Button(self.buttonFrame, text='Add to list', command=self.add_song).grid(row=0, column=0)

        self.delete_song = Button(self.buttonFrame, text='Remove a song', command=self.delete_song).grid(row=0,
                                                                                                         column=1)

        self.delete_all_songs = Button(self.buttonFrame, text='Remove all songs', command=self.delete_all_songs).grid(
            row=0, column=2)

        self.play_video_button = Button(self.buttonFrame, text='Play Video', command=self.play_video).grid(row=0,
                                                                                                           column=3)

    # -------FUNCTIONS-------------
    ##Add Song Function
    def add_song(self):
        ##Add one song
        # song = filedialog.askopenfilename(initialdir='audio/', title='Choose a song', filetypes=(("Mp3 Files", "*.mp3"),))
        # song = song.replace("C:/Users/Sara Said/PycharmProjects/MMSMusicPlayer/audio/", "")
        # song = song.replace(".mp3", "")
        # songBox.insert(END, song)
        # print(song)

        ##Add many songs
        songs = filedialog.askopenfilenames(initialdir='audio/', title='Choose a song',
                                            filetypes=(("Mp3 Files", "*.mp3"),))
        for song in songs:
            song = song.replace("C:/Users/Sara Said/PycharmProjects/MMSMusicPlayer/audio/", "")
            song = song.replace(".mp3", "")
            self.songBox.insert(END, song)

    def play_video(self):
        movie = filedialog.askopenfilename(initialdir='audio/', title='Choose a video',
                                           filetypes=(("Mp4 Files", "*.mp4"),))

        pygame.display.set_caption('Stay Safe .. Stay Home')
        clip = VideoFileClip(movie)
        clip.preview()
        pygame.quit()

    global playing
    playing = False

    ##Play Song Function
    def play_song(self):
        try:
            global stopped
            stopped = False

            if stopped:
                return

            song = self.songBox.get(ACTIVE)
            song = f'C:/Users/Sara Said/PycharmProjects/MMSMusicPlayer/audio/{song}.mp3'
            pygame.mixer.music.load(song)
            pygame.mixer.music.play()

            self.play_time()

            slider_position = int(song_length)
            self.my_slider.config(to=slider_position, value=0)
        except:
            messagebox.showinfo('Error', 'PlayList is Empty Add some songs')

    ##Pause song
    def pause_song(self):
        global paused

        if paused:
            pygame.mixer.music.unpause()
            paused = False
        else:
            pygame.mixer.music.pause()
            paused = True

        print(paused)

    global stopped
    stopped = False

    ##Stop song
    def stop_song(self):
        self.timeLabel.config(text='Time Elapsed: 00:00:00 of 00:00:00')
        self.my_slider.config(value=0)

        pygame.mixer.music.stop()
        self.songBox.selection_clear(ACTIVE)

        global stopped
        stopped = True

        self.timeLabel.config(text='Time Elapsed: 00:00:00 of 00:00:00')

    global paused
    paused = False

    def next_song(self):
        global song_length
        convert_song_length = time.strftime('%H:%M:%S', time.gmtime(song_length))

        self.timeLabel.config(text=f'Time Elapsed: 00:00:00 of {convert_song_length}')
        self.my_slider.config(value=0)

        current_song_index = self.songBox.curselection()
        if current_song_index[0] != self.songBox.size() - 1:
            next_one = self.songBox.curselection()
            next_one = next_one[0] + 1

            song = self.songBox.get(next_one)
            song = f'C:/Users/Sara Said/PycharmProjects/MMSMusicPlayer/audio/{song}.mp3'
            pygame.mixer.music.load(song)
            pygame.mixer.music.play()

            self.songBox.selection_clear(0, END)
            self.songBox.activate(next_one)
            self.songBox.select_set(next_one)
        else:
            song = self.songBox.get(0)
            song = f'C:/Users/Sara Said/PycharmProjects/MMSMusicPlayer/audio/{song}.mp3'
            pygame.mixer.music.load(song)
            pygame.mixer.music.play()

            self.songBox.selection_clear(0, END)
            self.songBox.activate(0)
            self.songBox.select_set(0)

    def previous_song(self):
        global song_length
        convert_song_length = time.strftime('%H:%M:%S', time.gmtime(song_length))

        self.timeLabel.config(text=f'Time Elapsed: 00:00:00 of {convert_song_length}')
        self.my_slider.config(value=0)

        current_song_index = self.songBox.curselection()

        if current_song_index[0] != 0:
            previous_one = self.songBox.curselection()
            previous_one = previous_one[0] - 1

            song = self.songBox.get(previous_one)
            song = f'C:/Users/Sara Said/PycharmProjects/MMSMusicPlayer/audio/{song}.mp3'
            pygame.mixer.music.load(song)
            pygame.mixer.music.play()

            self.songBox.selection_clear(0, END)
            self.songBox.activate(previous_one)
            self.songBox.select_set(previous_one)
        else:
            song = self.songBox.get(self.songBox.size() - 1)
            song = f'C:/Users/Sara Said/PycharmProjects/MMSMusicPlayer/audio/{song}.mp3'
            pygame.mixer.music.load(song)
            pygame.mixer.music.play()

            self.songBox.selection_clear(0, END)
            self.songBox.activate(self.songBox.size() - 1)
            self.songBox.select_set(self.songBox.size() - 1)

    def delete_song(self):
        self.stop_song()
        self.songBox.delete(ANCHOR)
        pygame.mixer.music.stop()

    def delete_all_songs(self):
        self.stop_song()
        self.songBox.delete(0, END)
        pygame.mixer.music.stop()

    def play_time(self):
        current_time = pygame.mixer.music.get_pos() / 1000

        convert_current_time = time.strftime('%H:%M:%S', time.gmtime(current_time))

        song = self.songBox.get(ACTIVE)
        song = f'C:/Users/Sara Said/PycharmProjects/MMSMusicPlayer/audio/{song}.mp3'

        ##Load song with murtagen
        song_length_mut = MP3(song)

        ##Get song duration with  mutagen
        global song_length
        song_length = song_length_mut.info.length

        convert_song_length = time.strftime('%H:%M:%S', time.gmtime(song_length))

        current_time += 1

        if int(self.my_slider.get()) == int(song_length):
            self.timeLabel.config(text=f'Time Elapsed: {convert_song_length} of {convert_song_length} ')
            self.next_song()

        elif paused:
            pass

        elif int(self.my_slider.get()) == int(current_time):
            slider_position = int(song_length)
            self.my_slider.config(to=slider_position, value=int(current_time))

        else:
            slider_position = int(song_length)
            self.my_slider.config(to=slider_position, value=self.my_slider.get())

            convert_current_time = time.strftime('%H:%M:%S', time.gmtime(int(self.my_slider.get())))
            self.timeLabel.config(text=f'Time Elapsed: {convert_current_time} of {convert_song_length} ')

            ##Move slider along by one second
            next_time = int(self.my_slider.get()) + 1
            self.my_slider.config(value=next_time)

        self.timeLabel.after(1000, self.play_time)

    def slide(self, x):
        song = self.songBox.get(ACTIVE)
        song = f'C:/Users/Sara Said/PycharmProjects/MMSMusicPlayer/audio/{song}.mp3'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(start=int(self.my_slider.get()))

    def volume(self, val):
        pygame.mixer.music.set_volume(self.volume_slider.get())

    def mute(self):
        pygame.mixer.music.set_volume(0)
        self.volume_slider.set(0)

    def unmute(self):
        pygame.mixer.music.set_volume(1)
        self.volume_slider.set(1)


root = Tk()
length = StringVar()
my_gui = GUI(root)
root.mainloop()
