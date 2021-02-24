from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from mutagen.mp3 import MP3
import time
from tkinter import messagebox

import pygame

pygame.mixer.init()


##Add Song Function
def add_song():
    ##Add one song
    # song = filedialog.askopenfilename(initialdir='audio/', title='Choose a song', filetypes=(("Mp3 Files", "*.mp3"),))
    # song = song.replace("C:/Users/Sara Said/PycharmProjects/MMSMusicPlayer/audio/", "")
    # song = song.replace(".mp3", "")
    # songBox.insert(END, song)
    # print(song)

    ##Add many songs
    songs = filedialog.askopenfilenames(initialdir='audio/', title='Choose a song', filetypes=(("Mp3 Files", "*.mp3"),))
    for song in songs:
        song = song.replace("C:/Users/Sara Said/PycharmProjects/MMSMusicPlayer/audio/", "")
        song = song.replace(".mp3", "")
        songBox.insert(END, song)


##Play Song Function
def play_song():
    global stopped
    stopped = False
    try:
        if stopped:
            return

        global paused
        global playing

        if not playing:
            song = songBox.get(ACTIVE)
            song = f'C:/Users/Sara Said/PycharmProjects/MMSMusicPlayer/audio/{song}.mp3'
            pygame.mixer.music.load(song)
            pygame.mixer.music.play()

            play_button['image'] = pauseBtnImg
            playing = True
            play_time()

            slider_position = int(song_length)
            my_slider.config(to=slider_position, value=0)
            print(paused)

        else:
            if paused:
                pygame.mixer.music.unpause()
                paused = False
                play_button['image'] = pauseBtnImg
                print(paused)

            else:
                pygame.mixer.music.pause()
                paused = True
                play_button['image'] = playBtnImg
                print(paused)
    except:
        messagebox.showerror('Error', 'No file found to play.')


##Pause song
def pause_song(is_paused):
    global paused
    paused = is_paused

    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True


global stopped
stopped = False


##Stop song
def stop_song():
    timeLabel.config(text='Time Elapsed: 00:00:00 of 00:00:00')
    my_slider.config(value=0)

    pygame.mixer.music.stop()
    songBox.selection_clear(ACTIVE)

    global stopped
    stopped = True

    timeLabel.config(text='Time Elapsed: 00:00:00 of 00:00:00')


global paused
paused = False


def next_song():
    global song_length
    convert_song_length = time.strftime('%H:%M:%S', time.gmtime(song_length))

    timeLabel.config(text=f'Time Elapsed: 00:00:00 of {convert_song_length}')
    my_slider.config(value=0)

    current_song_index = songBox.curselection()
    if current_song_index[0] != songBox.size() - 1:
        next_one = songBox.curselection()
        next_one = next_one[0] + 1

        song = songBox.get(next_one)
        song = f'C:/Users/Sara Said/PycharmProjects/MMSMusicPlayer/audio/{song}.mp3'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()

        songBox.selection_clear(0, END)
        songBox.activate(next_one)
        songBox.select_set(next_one)
    else:
        song = songBox.get(0)
        song = f'C:/Users/Sara Said/PycharmProjects/MMSMusicPlayer/audio/{song}.mp3'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()

        songBox.selection_clear(0, END)
        songBox.activate(0)
        songBox.select_set(0)


def previous_song():
    global song_length
    convert_song_length = time.strftime('%H:%M:%S', time.gmtime(song_length))

    timeLabel.config(text=f'Time Elapsed: 00:00:00 of {convert_song_length}')
    my_slider.config(value=0)

    current_song_index = songBox.curselection()

    if current_song_index[0] != 0:
        previous_one = songBox.curselection()
        previous_one = previous_one[0] - 1

        song = songBox.get(previous_one)
        song = f'C:/Users/Sara Said/PycharmProjects/MMSMusicPlayer/audio/{song}.mp3'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()

        songBox.selection_clear(0, END)
        songBox.activate(previous_one)
        songBox.select_set(previous_one)
    else:
        song = songBox.get(songBox.size() - 1)
        song = f'C:/Users/Sara Said/PycharmProjects/MMSMusicPlayer/audio/{song}.mp3'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()

        songBox.selection_clear(0, END)
        songBox.activate(songBox.size() - 1)
        songBox.select_set(songBox.size() - 1)


def delete_song():
    stop_song()
    songBox.delete(ANCHOR)
    pygame.mixer.music.stop()


def delete_all_songs():
    stop_song()
    songBox.delete(0, END)
    pygame.mixer.music.stop()


def play_time():
    current_time = pygame.mixer.music.get_pos() / 1000

    convert_current_time = time.strftime('%H:%M:%S', time.gmtime(current_time))

    song = songBox.get(ACTIVE)
    song = f'C:/Users/Sara Said/PycharmProjects/MMSMusicPlayer/audio/{song}.mp3'

    ##Load song with murtagen
    song_length_mut = MP3(song)

    ##Get song duration with  mutagen
    global song_length
    song_length = song_length_mut.info.length

    convert_song_length = time.strftime('%H:%M:%S', time.gmtime(song_length))

    current_time += 1

    if int(my_slider.get()) == int(song_length):
        timeLabel.config(text=f'Time Elapsed: {convert_song_length} of {convert_song_length} ')
        next_song()

    elif paused:
        pass

    elif int(my_slider.get()) == int(current_time):
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))

    else:
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=my_slider.get())

        convert_current_time = time.strftime('%H:%M:%S', time.gmtime(int(my_slider.get())))
        timeLabel.config(text=f'Time Elapsed: {convert_current_time} of {convert_song_length} ')

        ##Move slider along by one second
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)

    timeLabel.after(1000, play_time)


def slide(x):
    song = songBox.get(ACTIVE)
    song = f'C:/Users/Sara Said/PycharmProjects/MMSMusicPlayer/audio/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(start=int(my_slider.get()))


def volume(val):
    pygame.mixer.music.set_volume(volume_slider.get())


def mute():
    pygame.mixer.music.set_volume(0)
    volume_slider.set(0)


def unmute():
    pygame.mixer.music.set_volume(1)
    volume_slider.set(1)


root = Tk()
root.title('MMS Music Player')
root.iconbitmap('images/Music.ico')
root.geometry('600x500')
root.resizable(0, 0)

## Create Master Frame
master_frame = Frame(root)
master_frame.pack()

##Label
label = Label(master_frame, text='Music Player')
label.pack(pady=10)

##Buttons Frame
buttonFrame = Frame(master_frame)
buttonFrame.pack()

topframe = Frame(master_frame)
topframe.pack()

##Volume Frame
volumeframe = LabelFrame(topframe, text='Volume')
volumeframe.grid(row=0, column=1, pady=20, padx=10)

##Design and Create Mute Button
muteImg = PhotoImage(file='images/mute.png')
muteButton = Button(volumeframe, image=muteImg, command=mute).grid(row=0, column=0, padx=10)

##Design and Create Unmute Button
unmuteImg = PhotoImage(file='images/vol.png')
ummuteButton = Button(volumeframe, image=unmuteImg, command=unmute).grid(row=2, column=0)

##Create Volume Slider
volume_slider = Scale(volumeframe, from_=0, to=1, orient=VERTICAL, value=1, command=volume, length=80)
volume_slider.grid(row=1, column=0, pady=10)

##List box
songBox = Listbox(topframe, width=50, bg='grey', fg='green', selectbackground='white', selectforeground='black')
songBox.grid(row=0, column=0, pady=20)

##Song Duration Label
timeLabel = Label(master_frame, text='Time Elapsed: 00:00:00 of 00:00:00', relief=GROOVE, anchor=E)
timeLabel.pack()

##Song Progress Slider
my_slider = Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.pack(pady=15)

##Create Frame Which Contains Buttons
controlFrame = Frame(master_frame)
controlFrame.pack(pady=15, padx=15)

##Design Buttons
playBtnImg = PhotoImage(file='images/Play.png')
backBtnImg = PhotoImage(file='images/prev.png')
stopBtnImg = PhotoImage(file='images/stop.png')
forwardBtnImg = PhotoImage(file='images/next.png')
pauseBtnImg = PhotoImage(file='images/pause.png')

##Create Player Control Buttons
pause_button = Button(controlFrame, image=pauseBtnImg, command=lambda: pause_song(paused)).grid(row=0, column=2)
play_button = Button(controlFrame, image=playBtnImg, command=play_song).grid(row=0, column=1)
prev_button = Button(controlFrame, image=backBtnImg, command=previous_song).grid(row=0, column=0)
stop_button = Button(controlFrame, image=stopBtnImg, command=stop_song).grid(row=0, column=3)
next_button = Button(controlFrame, image=forwardBtnImg, command=next_song).grid(row=0, column=4)
#
# addToList = Button(root, text='Add to list', command=add_song).place(x=670, y=10)
#
# delete_song = Button(root, text='Remove a song', command=delete_song).place(x=670, y=40)
#
# delete_all_songs = Button(root, text='Remove all songs', command=delete_all_songs).place(x=670, y=70)


addToList = Button(buttonFrame, text='Add to list', command=add_song).grid(row=0, column=0)

delete_song = Button(buttonFrame, text='Remove a song', command=delete_song).grid(row=0, column=1)

delete_all_songs = Button(buttonFrame, text='Remove all songs', command=delete_all_songs).grid(row=0, column=2)

root.mainloop()
