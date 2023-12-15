#!/usr/bin/python3
from tkinter import *
from tkinter import messagebox
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto import Random
import os

def popup(msg):
    messagebox.showinfo("message",msg)

def encrypt(key,filename):
    chunksize = 64*1024
    op = "en_"+filename
    filez = str(os.path.getsize(filename)).zfill(16)
    iv = Random.new().read(16)
    encryptor = AES.new(key,AES.MODE_CBC,iv)

    with open(filename,"rb") as infile:
        with open(op,"wb") as outfile:
            outfile.write(filez.encode('utf-8'))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0: break
                elif len(chunk) % 16 != 0:
                    chunk+=b' '*(16-len(chunk)%16)

                outfile.write(encryptor.encrypt(chunk))

def decrypt(key,filename):
    chunksize = 64*1024
    op = filename[3:]

    with open(filename,"rb") as infile:
        filesize = int(infile.read(16))
        IV = infile.read(16)
        decryptor = AES.new(key,AES.MODE_CBC,IV)
        with open(op,"wb") as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0: break

                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(filesize)


def getkey(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()






def padd(r,s,e):
    for i in range(s,e):
        l = Label(root,text="")
        l.grid(row=r,column=i)
        del l

def enroll():
    if(op.get()==1):
        fn = filename.get()
        pword = password.get()
        encrypt(getkey(pword),fn)
        os.remove(fn)
        print("Done encryption")
        popup("done Encryption")
        exit(0)
    else:
        fn = filename.get()
        pword = password.get()
        decrypt(getkey(pword),fn)
        os.remove(fn)
        print("Done decryption")
        popup("done Decryption")
        exit(0)

root = Tk()
# root['bg']
root.title("cryptor")
op = IntVar()
op.set(1)
# padd(0,0,1)
l1 = Label(text="CRYPTOR").grid(row=0,column=26)
padd(0,27,52)
l2 = Label(text="filename").grid(row=1,column=0)
filename = Entry(root,width=15,border=5,font=15)
filename.grid(row=1,column=1)
l3 = Label(text="password").grid(row=2,column=0)
password = Entry(root,width=15,border=5,font=15)
password.grid(row=2,column=1)
r1 = Radiobutton(root,text="encrypt",variable=op,value=1).grid(row=3)
r2 = Radiobutton(root,text="decrypt",variable=op,value=2).grid(row=4)
process = Button(text="done",command=lambda:enroll()).grid(row=5,column=0)

exit_ = Button(text="exit",command=lambda:exit()).grid(row=5,column=1,columnspan=3)
root.mainloop()
