#======== Select a file for opening:
#--------------------------------------------------- import Tkinter,tkFileDialog
#----------------------------------------------------------- root = Tkinter.Tk()
#-- file = tkFileDialog.askopenfile(parent=root,mode='rb',title='Choose a file')
#-------------------------------------------------------------- if file != None:
    #-------------------------------------------------------- data = file.read()
    #-------------------------------------------------------------- file.close()
    #------------------------ print "I got %d bytes from this file." % len(data)

from Tkinter import *

root = Tk()

def key(event):
    print "pressed", repr(event.char)

def callback(event):
    frame.focus_set()
    print "clicked at", event.x, event.y

frame = Frame(root, width=100, height=100)
frame.bind("<Key>", key)
frame.bind("<Button-1>", callback)
frame.pack()

root.mainloop()