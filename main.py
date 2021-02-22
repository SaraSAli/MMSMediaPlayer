from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *

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
    song = songBox.get(ACTIVE)
    song = f'C:/Users/Sara Said/PycharmProjects/MMSMusicPlayer/audio/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()


##Stop song
def stop_song():
    pygame.mixer.music.stop()
    songBox.selection_clear(ACTIVE)


global paused
paused = False


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


def next_song():
    next_one = songBox.curselection()
    next_one = next_one[0] + 1

    song = songBox.get(next_one)
    song = f'C:/Users/Sara Said/PycharmProjects/MMSMusicPlayer/audio/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()

    songBox.selection_clear(0, END)
    songBox.activate(next_one)
    songBox.select_set(next_one)


def previous_song():
    previous_one = songBox.curselection()
    previous_one = previous_one[0] - 1

    song = songBox.get(previous_one)
    song = f'C:/Users/Sara Said/PycharmProjects/MMSMusicPlayer/audio/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()

    songBox.selection_clear(0, END)
    songBox.activate(previous_one)
    songBox.select_set(previous_one)


def delete_song():
    songBox.delete(ANCHOR)
    pygame.mixer.music.stop()
    

def delete_all_songs():
    songBox.delete(0, END)
    pygame.mixer.music.stop()


root = Tk()
root.title('MMS Music Player')
root.iconbitmap('images/Music.ico')
root.geometry('800x500')
root.resizable(0, 0)

##Label
label = Label(root, text='Music Player')
label.pack()

##List box
songBox = Listbox(root, width=80, bg='grey', fg='green', selectbackground='white', selectforeground='black')
songBox.pack(pady=20)

##Create Frame Which Contains Buttons
controlFrame = Frame(root)
controlFrame.pack()

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

addToList = Button(root, text='Add to list', command=add_song).place(x=670, y=10)

delete_song = Button(root, text='Remove a song', command=delete_song).place(x=670, y=40)

delete_all_songs = Button(root, text='Remove all songs', command=delete_all_songs).place(x=670, y=70)

root.mainloop()
