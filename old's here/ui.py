import tkinter
import PIL.ImageTk,PIL.Image
from DSA import dsa
import isstring



need_dict = {}
filename123 = ''

get_file_but_text = ' Open File '
create_sig_but_text = ' Create Signature '
go_check_but_text = ' Check Signature '

def writeinfile(file, dict):
    from tkinter import messagebox
    #(need_dict, file)
    if not isstring.isstring(dict):
        if file != '':
            pos_of_dot = file.rfind('.')

            if pos_of_dot != -1:

                signed_file = file[:pos_of_dot] + '.crf'


                list1 = dict.get('result',0)
                list2 = dict.get('params',0)
                hash = dict.get('hash',0)
                #(list1)
                if all([list1,list2,hash]):

                    out_file = open(signed_file, 'w')

                    i = 0
                    for elem in list1:
                        out_file.write(str(elem))

                        if i < len(list1)-1:
                            out_file.write(' ')
                            i += 1

                    out_file.write('/')

                    i = 0
                    for elem in list2:
                        out_file.write(str(elem))
                        if i < len(list2)-1:
                            out_file.write(' ')
                            i += 1

                    out_file.write('|')
                    out_file.write(str(hash))
                    out_file.close()

            else:
                messagebox.showerror('Error', 'Wrong file path')
        else:
            messagebox.showerror('Error', 'Wrong filename')
    else:
        messagebox.showerror('Error',dict)

def sig_nframe():

    def GoCheck(**kwargs):
        sigframe.destroy()
        check_sig()

    def VerPhoto(path,width,height,x,y):
        im = PIL.Image.open(path)
        photo = PIL.ImageTk.PhotoImage(im)
        label = tkinter.Label(sigframe, image=photo, width=width, height=height)
        label.image = photo  # keep a reference!
        label.place(relx=x, rely=y)

    def openFile(**kwargs):
        from tkinter import messagebox
        from tkinter.filedialog import askopenfilename

        filename = askopenfilename()
        if filename != '':
            kek = True
            try:
                p = int(p_entry.get())
                q = int(q_entry.get())
                x = int(x_entry.get())
                h = int(h_entry.get())
                k = int(k_entry.get())
            except:
                messagebox.showerror('Error','One of parameters is missing')
                kek = False

            if kek:
                global need_dict
                global filename123
                filename123 = filename
                need_dict = dsa(filename,p=p,q=q,x=x,k=k,h=h,mode='signature')
                if not isstring.isstring(need_dict):
                    label_6['text'] = 'Hash: '+str(need_dict.get('hash',0))[:17]+'...'
                    label_7['text'] = 'Y: '+str(need_dict.get('result',0)[0])
                    label_8['text'] = 'G: ' + str(need_dict.get('result', 0)[1])
                else:
                    messagebox.showerror('Error',need_dict)

            else:
                messagebox.showerror('Error','One of parametrs is false')
        else:
            messagebox.showerror('File.Error','Wrong file name!')

    def createSIG(**kwargs):
        writeinfile(filename123,need_dict)





    sigframe = tkinter.Tk()
    sigframe.geometry('500x400')
    sigframe.title('Signature (DSA)')
    sigframe.resizable(width=False,height=False)

    #Main_Window.iconbitmap('img/icon.ico')

    # Buttons:

    button_get_file = tkinter.Button(sigframe,text=get_file_but_text, bg='Dodger Blue', fg='White', width=15,
                                     command=(lambda : openFile()))
    button_get_file.place(relx=0.65,rely=0.45)

    button_create_sig = tkinter.Button(sigframe, text=create_sig_but_text, bg='Dodger Blue', fg='White', width=15,
                                       command=(lambda : createSIG()))
    button_create_sig.place(relx=0.65, rely=0.55)

    button_go_check = tkinter.Button(sigframe, text=go_check_but_text, bg='Dodger Blue', fg='White', width=15,
                                     command=(lambda : GoCheck()))
    button_go_check.place(relx=0.65, rely=0.65)

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

    label_1 = tkinter.Label(sigframe, text='Enter p: ', height=1)
    label_1.place(relx=.1, rely=.14)

    label_2 = tkinter.Label(sigframe, text='Enter q: ', height=1)
    label_2.place(relx=.1, rely=.29)

    label_3 = tkinter.Label(sigframe, text='Enter h: ', height=1)
    label_3.place(relx=.1, rely=.44)

    label_4 = tkinter.Label(sigframe, text='Enter x: ', height=1)
    label_4.place(relx=.1, rely=.59)

    label_5 = tkinter.Label(sigframe, text='Enter k: ', height=1)
    label_5.place(relx=.1, rely=.74)

    label_6 = tkinter.Label(sigframe,text='',height=1)
    label_6.place(relx=.5,rely=.1)

    label_7 = tkinter.Label(sigframe, text='', height=1)
    label_7.place(relx=.5, rely=.2)

    label_8 = tkinter.Label(sigframe, text='', height=1)
    label_8.place(relx=.5, rely=.3)






    sigframe.mainloop()

def check_sig():
    promej_dict = ()

    def readfile(**kwargs):
        global promej_dict

        from tkinter.filedialog import askopenfilename

        filename = askopenfilename()
        if filename != '':
            filename_new = filename[:filename.rfind('.')]+'.crf'
            file_in = open(filename_new,'r')
            main_str = file_in.read()
            file_in.close()
            raw_str_1 = main_str[:main_str.find('/')]
            raw_str_2 = main_str[main_str.find('/')+1:main_str.find('|')]
            y = int(raw_str_1[:raw_str_1.find(' ')])
            g = int(raw_str_1[raw_str_1.find(' ')+1:raw_str_1.rfind(' ')])

            r = int(raw_str_2[:raw_str_2.find(' ')])
            s = int(raw_str_2[raw_str_2.find(' ')+1:])
            #print(r,s)
            promej_dict = (int(r),int(s),int(y),int(g))

            p = int(p_entry.get())
            q = int(q_entry.get())
            #print(r,s,y,g,p,q)
            check = dsa(filename,mode='check',p=p,q=q,r=r,s=s,y=y,g=g)
            if not isstring.isstring(check):
                if check.get('params')[0] == r:
                    VerPhoto('img/ver.png',100,80,0.1,0.6)
                else:
                    VerPhoto('img/unver.png', 100, 80, 0.1, 0.6)
            else:
                from tkinter import messagebox
                messagebox.showerror('Error',check)


    def GoCheck(**kwargs):
        checkframe.destroy()
        sig_nframe()

    def VerPhoto(path,width,height,x,y):
        im = PIL.Image.open(path)
        photo = PIL.ImageTk.PhotoImage(im)
        label = tkinter.Label(checkframe, image=photo, width=width, height=height)
        label.image = photo  # keep a reference!
        label.place(relx=x, rely=y)

    checkframe = tkinter.Tk()
    checkframe.geometry('500x250')
    checkframe.title('Signature (DSA)')
    checkframe.resizable(width=False, height=False)

    button_go_check = tkinter.Button(checkframe, text=create_sig_but_text, bg='Dodger Blue', fg='White', width=15,
                                     command=(lambda: GoCheck()))
    button_go_check.place(relx=0.65, rely=0.45)

    button_get_file = tkinter.Button(checkframe, text=get_file_but_text, bg='Dodger Blue', fg='White', width=15,
                                     command=(lambda: readfile()))
    button_get_file.place(relx=0.65, rely=0.25)

    p_var = tkinter.IntVar()
    q_var = tkinter.IntVar()
    p_var = ''
    q_var = ''

    p_entry = tkinter.Entry(checkframe,textvariable=p_var)
    p_entry.place(relx=.1, rely=.2, width=100)

    q_entry = tkinter.Entry(checkframe,textvariable=q_var)
    q_entry.place(relx=.1, rely=.4, width=100)

    label_1 = tkinter.Label(checkframe, text='Enter p: ', height=1)
    label_1.place(relx=.1, rely=.10)

    label_2 = tkinter.Label(checkframe, text='Enter q: ', height=1)
    label_2.place(relx=.1, rely=.29)

    checkframe.mainloop()

if __name__ == '__main__':
    sig_nframe()