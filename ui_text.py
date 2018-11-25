import tkinter

butt_1 = 'Create signature.'
butt_2 = 'Check signature.'

def frame_1():

    def change_labels(lol,**kwargs):
        label_6['text'] = 'Hash: '+str(lol[3])
        label_7['text'] = 'Y: '+str(lol[2])
        label_8['text'] = 'G: '+str(lol[4])
        label_9['text'] = 'Hash(Hex): '+hex(lol[3])[3:]


    def goCheck(**kwargs):

        frame.destroy()
        frame_2()

    def create_signature(**kwargs):

        from tkinter import messagebox
        from tkinter.filedialog import askopenfilename


        from DSA_text import dsa_sign
        try:

            p = int(p_entry.get())
            q = int(q_entry.get())
            h = int(h_entry.get())
            x = int(x_entry.get())
            k = int(k_entry.get())

        except ValueError:
            messagebox.showerror('ValueError','Wrong params.')
            return

        filename = askopenfilename()
        if filename != '':
            check = dsa_sign(p=p,q=q,h=h,x=x,k=k,filename=filename)
            if not isinstance(check, str):
                change_labels(check)
            else:
                messagebox.showerror('Error', check)
        else:
            messagebox.showerror('File error.','Wrong filename.')




    frame = tkinter.Tk()

    frame.geometry('500x400')
    frame.title('Signature (DSA)')
    frame.resizable(width=False, height=False)

    # Entrys

    p_var = tkinter.IntVar()
    q_var = tkinter.IntVar()
    h_var = tkinter.IntVar()
    x_var = tkinter.IntVar()
    k_var = tkinter.IntVar()

    q_var = ''
    p_var = ''
    h_var = ''
    x_var = ''
    k_var = ''

    p_entry = tkinter.Entry(textvariable=p_var)
    p_entry.place(relx=.1, rely=.2, width=100)

    q_entry = tkinter.Entry(textvariable=q_var)
    q_entry.place(relx=.1, rely=.35, width=100)

    h_entry = tkinter.Entry(textvariable=h_var)
    h_entry.place(relx=.1, rely=.5, width=100)

    x_entry = tkinter.Entry(textvariable=x_var)
    x_entry.place(relx=.1, rely=.65, width=100)

    k_entry = tkinter.Entry(textvariable=k_var)
    k_entry.place(relx=.1, rely=.8, width=100)

    # labels

    label_1 = tkinter.Label(frame, text='Enter p: ', height=1)
    label_1.place(relx=.1, rely=.14)

    label_2 = tkinter.Label(frame, text='Enter q: ', height=1)
    label_2.place(relx=.1, rely=.29)

    label_3 = tkinter.Label(frame, text='Enter h: ', height=1)
    label_3.place(relx=.1, rely=.44)

    label_4 = tkinter.Label(frame, text='Enter x: ', height=1)
    label_4.place(relx=.1, rely=.59)

    label_5 = tkinter.Label(frame, text='Enter k: ', height=1)
    label_5.place(relx=.1, rely=.74)

    # buttons

    button_create_sig = tkinter.Button(frame, text=butt_1, bg='Dodger Blue', fg='White', width=15,
                                       command=(lambda: create_signature()))
    button_create_sig.place(relx=0.65, rely=0.55)

    button_go_check = tkinter.Button(frame, text=butt_2, bg='Dodger Blue', fg='White', width=15,
                                     command=(lambda: goCheck()))
    button_go_check.place(relx=0.65, rely=0.65)

    # label

    label_6 = tkinter.Label(frame, text='', height=1)
    label_6.place(relx=.32, rely=.1)

    label_7 = tkinter.Label(frame, text='', height=1)
    label_7.place(relx=.5, rely=.3)

    label_8 = tkinter.Label(frame, text='', height=1)
    label_8.place(relx=.5, rely=.4)

    label_9 = tkinter.Label(frame, text='', height=1)
    label_9.place(relx=.32, rely=.2)


    frame.mainloop()

def frame_2():

    def verPhoto(path,width,height,x,y):
        from PIL import Image,ImageTk
        im = Image.open(path)
        photo = ImageTk.PhotoImage(im)
        label = tkinter.Label(frame, image=photo, width=width, height=height)
        label.image = photo  # keep a reference!
        label.place(relx=x, rely=y)


    def gosig(**kwargs):

        frame.destroy()
        frame_1()

    def check_signature(**kwargs):
        from tkinter import messagebox
        from tkinter.filedialog import askopenfilename
        from DSA_text import check_sign_dsa

        try:
            p = int(p_entry.get())
            q = int(q_entry.get())
            h = int(h_entry.get())
            y = int(y_entry.get())
        except ValueError:
            messagebox.showerror('Error','Wrong params')
            return

        filename = askopenfilename()
        from DSA_text import isPrime
        if filename != '' and 1 < h < p-1 and isPrime(p) and isPrime(q) and (p-1) % q == 0:
            check = check_sign_dsa(p=p,q=q,h=h,y=y,filename=filename)
            if not isinstance(check,str):
                if check == True:
                    verPhoto('img/ver.png',100,80,0.6,0.2)
                else:
                    verPhoto('img/unver.png', 100, 80, 0.6, 0.2)

            else:
                messagebox.showerror('Error',check)
        else:
            messagebox.showerror('Error','Wrong filename or h, or p, or q.')




    frame = tkinter.Tk()

    frame.geometry('500x400')
    frame.title('Check Signature (DSA)')
    frame.resizable(width=False, height=False)


    # buttons
    button_go_check = tkinter.Button(frame, text=butt_1, bg='Dodger Blue', fg='White', width=15,
                                     command=(lambda: gosig()))
    button_go_check.place(relx=0.65, rely=0.65)

    button_get_file = tkinter.Button(frame, text=butt_2, bg='Dodger Blue', fg='White', width=15,
                                     command=(lambda: check_signature()))
    button_get_file.place(relx=0.65, rely=0.55)

    # entrys

    p_var = tkinter.IntVar()
    q_var = tkinter.IntVar()
    h_var = tkinter.IntVar()
    y_var = tkinter.IntVar()

    q_var = ''
    p_var = ''
    h_var = ''
    y_var = ''

    p_entry = tkinter.Entry(textvariable=p_var)
    p_entry.place(relx=.1, rely=.2, width=100)

    q_entry = tkinter.Entry(textvariable=q_var)
    q_entry.place(relx=.1, rely=.35, width=100)

    h_entry = tkinter.Entry(textvariable=h_var)
    h_entry.place(relx=.1, rely=.5, width=100)

    y_entry = tkinter.Entry(textvariable=y_var)
    y_entry.place(relx=.1, rely=.65, width=100)

    # labels

    label_1 = tkinter.Label(frame, text='Enter p: ', height=1)
    label_1.place(relx=.1, rely=.14)

    label_2 = tkinter.Label(frame, text='Enter q: ', height=1)
    label_2.place(relx=.1, rely=.29)

    label_3 = tkinter.Label(frame, text='Enter h: ', height=1)
    label_3.place(relx=.1, rely=.44)

    label_4 = tkinter.Label(frame, text='Enter y: ', height=1)
    label_4.place(relx=.1, rely=.59)
    frame.mainloop()


if __name__ == '__main__':
    frame_1()