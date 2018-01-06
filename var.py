from tkinter import *
import tkinter.messagebox as tkm
from tkinter import filedialog as fd
import numpy as np
import numpy.linalg as npl
import requests



def coefficient_calc():
    window = Tk()

    window.minsize(width='650', height='400')
    window.maxsize(width='650', height='400')

    window.winfo_toplevel().title('Local coefficient of variation calculator')

    def file_save(txt):
        f = fd.asksaveasfile(mode='w', defaultextension=".txt")
        # if f is None:
        #     return
        f.write(txt)
        f.close()

    def info():
        msg = 'Contact me:\n{}'.format('kobas394@gmail.com')
        tkm.showinfo('Info',msg)

    def dialog1Display(msg):
        top = Toplevel()
        top.title("Solution")
        top.geometry('400x400')
        m = Message(top, text=msg)
        m.pack()

        button = Button(top, text="Ok", command=top.destroy, width='10')
        button.pack()


    def calculate():
        # Data input
        txt = ''
        i = 1
        A1 = ent_1.get()
        P1 = ent_2.get()
        L1 = ent_3.get()
        V1 = ent_V1.get()

        A2 = ent_4.get()
        P2 = ent_5.get()
        L2 = ent_6.get()
        V2 = ent_V2.get()

        # Matrix creation
        def Matrix_A(A):
            A = A.split(';')
            global rows
            global columns
            rows = len(A)
            liczby = []
            for wiersz in A:
                wiersz = wiersz.split(',')
                columns = len(wiersz)
                for liczba in wiersz:
                    liczby.append(liczba)
            int_list = []
            for number in liczby:
                number = int(number)
                int_list.append(number)
            A = np.matrix([int_list]).reshape(rows, columns)
            return A, int_list

        def Matrix_P(P):
            P = P.split(',')
            int_list = []
            for number in P:
                number = float(number)
                int_list.append(number)
            P = np.array(int_list)
            P = np.diag(P)
            return P

        def Matrix_L(L):
            L = L.split(',')
            int_list = []
            for number in L:
                number = float(number)
                int_list.append(number)
            L = np.matrix([int_list])
            L = np.transpose(L)
            return L

#         A1 = '1,-1;1,1;1,-1'
#         A2 = '0,0;1,-1;0,1'
#         P1 = '1000,2000.50,1500'
#         P2 = '1500.40,1500,1500'
#         L1 = '123.50,125,150'
#         L2 = '127,189.50,141'
#         V1 = '0.005,0.001,0.003'
#         V2 = '0.002,0.000,0.001'

        A1, list1 = Matrix_A(A1)
        A2, list2 = Matrix_A(A2)
        P1 = Matrix_P(P1)
        P2 = Matrix_P(P2)
        L1 = Matrix_L(L1)
        L2 = Matrix_L(L2)
        V1 = Matrix_L(V1)
        V2 = Matrix_L(V2)

        A = list1 + list1
        A = np.matrix(A).reshape(2*rows,columns)

        L = L1.tolist() + L2.tolist()
        L = np.matrix(L)

        # Further counting
        def iteration(i,P1,P2,txt):
            print(i)
            P = np.diagonal(P1).tolist() + np.diagonal(P2).tolist()
            P = np.diag(P)
            P = np.matrix(P)

            N1 = np.transpose(A1)*P1*A1
            N2 = np.transpose(A2)*P2*A2

            Q = np.transpose(A)*P*A
            Q = npl.inv(Q)

            a1 = np.trace(N1 * Q)
            a2 = np.trace(N2 * Q)
            b1 = np.trace((N1 * Q)**2)
            b2 = np.trace((N2 * Q)**2)
            c1 = np.trace(N1*Q*N2*Q)

            f1 = rows - 2 * a1 + b1
            f2 = rows - 2 * a2 + b2
            g1 = np.transpose(V1) * P1 * V1
            g2 = np.transpose(V2) * P2 * V2

            F = np.matrix([f1,c1,c1,f2]).reshape(2,2)
            g = np.array([g1,g2]).reshape(2,1)
            y = npl.inv(F)*g
            m1, m2 = np.sqrt(y)

            P1 = np.matrix((1/(float(m1)))**2 * P1)

            # >>>>>>>>>>>>Tu randomowa liczba bo wychodzi zespolona<<<<<
            P2 = np.matrix((1/2)**2 * P2)

            P = np.diagonal(P1).tolist() + np.diagonal(P2).tolist()
            P = np.diag(P)
            P = np.matrix(P)

            X = -1 * npl.inv(np.transpose(A) * P * A)
            X = X * np.transpose(A) * P * L
            V = A * X + L
            m0 = np.sqrt( (np.transpose(V) * P * V)/(len(V)-columns) )
            if m0 > 0.95 and m0 < 1.05:
                full_mess = 'iteration nr {}\nm0={} \nP=\n{}\n'.format(i,m0, P)
                mess = 'iterations:{}\nm0={} \nP=\n{}\n'.format(i, m0, P)
                dialog1Display(mess)
                txt = txt + full_mess
            elif i == 20:
                full_mess = 'iteration nr {}\nm0={} \nP=\n{}\n'.format(i,m0, P)
                mess = 'iterations:{}\nm0={} \nP=\n{}\n'.format(i,m0, P)
                dialog1Display(mess)
                txt = txt + full_mess
            else:
                full_mess = 'iteration nr {}\nm0={} \nP=\n{}\n'.format(i, m0, P)
                i += 1
                txt = txt + full_mess
                txt = iteration(i,P1,P2,txt)
            return txt

        txt = iteration(i, P1, P2, txt)
        file_save(txt)

    #       **** INTERFACE ****

    # MENU
    def quit():
        quit = tkm.askyesno('Quit', 'Are you sure you wanna quit, bro?')
        if quit:
            window.destroy()

    menu = Menu(window)
    window.config(menu=menu)

    fileMenu = Menu(menu)
    menu.add_cascade(label='File', menu=fileMenu)
    fileMenu.add_command(label='New', command=coefficient_calc)
    fileMenu.add_command(label='Save')
    fileMenu.add_separator()
    fileMenu.add_command(label='Quit', command=quit)

    editMenu = Menu(menu)
    menu.add_cascade(label='Nothing here yet...', menu=editMenu)

    # MAIN WINDOW

    lab_top = Label(window, text='Welcome to the local coefficient of variation calculator!',
                    font=('Arial',15))
    lab_gr1 = Label(window, text='Group 1:')
    lab_gr2 = Label(window, text='Group 2:')

    ent_1 = Entry(window)
    ent_2 = Entry(window)
    ent_3 = Entry(window)
    ent_4 = Entry(window)
    ent_5 = Entry(window)
    ent_6 = Entry(window)
    ent_V1 = Entry(window)
    ent_V2 = Entry(window)

    lab_1 = Label(window, text='A1')
    lab_2 = Label(window, text='P1')
    lab_3 = Label(window, text='L1')
    lab_4 = Label(window, text='A2')
    lab_5 = Label(window, text='P2')
    lab_6 = Label(window, text='L2')
    lab_V1 = Label(window, text='V1')
    lab_V2 = Label(window, text='V2')

    but_calc = Button(window, text='Calculate',width='10',command=calculate)
    but_info = Button(window,text='Info',width='10', command=info)

    lab_down = Label(window,
    text='This matrix calculator is free. If you enjoyed it, please donate. Every dollar counts ;) \n'
         'This is version 1.1 /2017. Created by Jakub Nowakowski.', relief=SUNKEN,
                     fg='red')

    # Softcapping grid
    rn = 2    #row number
    cn = 1    #column number

    # LAYOUT POSITIONING
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)
    window.columnconfigure(2, weight=1)
    window.columnconfigure(3, weight=1)
    window.columnconfigure(4, weight=1)
    window.columnconfigure(5, weight=1)
    window.columnconfigure(6, weight=1)

    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=1)
    window.rowconfigure(2, weight=1)
    window.rowconfigure(3, weight=1)
    window.rowconfigure(4, weight=1)
    window.rowconfigure(5, weight=1)
    window.rowconfigure(6, weight=1)
    window.rowconfigure(7, weight=1)
    window.rowconfigure(8, weight=1)
    window.rowconfigure(9, weight=1)
    window.rowconfigure(10, weight=28)
    window.rowconfigure(11, weight=1)
    window.rowconfigure(12, weight=1)

    lab_top.grid(in_=window, row=rn-2, column=cn, columnspan=4, pady = '30')
    lab_gr1.grid(row=rn-1, column=cn, columnspan=2)
    lab_gr2.grid(row=rn - 1, column=cn+2, columnspan=2)

    lab_1.grid(in_=window, row=rn, column=cn, sticky=E, padx=10)
    lab_2.grid(in_=window, row=rn+1, column=cn, sticky=E, padx=10)
    lab_3.grid(in_=window, row=rn+2, column=cn, sticky=E, padx=10)
    ent_1.grid(in_=window, row=rn, column=cn+1, sticky=W)
    ent_2.grid(in_=window, row=rn+1, column=cn+1, sticky=W)
    ent_3.grid(in_=window, row=rn+2, column=cn+1, sticky=W)

    lab_4.grid(in_=window, row=rn, column=cn+2, sticky=E, padx=10)
    lab_5.grid(in_=window, row=rn + 1, column=cn+2, sticky=E, padx=10)
    lab_6.grid(in_=window, row=rn + 2, column=cn+2, sticky=E, padx=10)
    ent_4.grid(in_=window, row=rn, column=cn+3, sticky=W)
    ent_5.grid(in_=window, row=rn+1, column=cn+3, sticky=W)
    ent_6.grid(in_=window, row=rn+2, column=cn+3, sticky=W)

    lab_V1.grid(row=rn+3, column=cn, sticky=E, padx=10)
    lab_V2.grid(row=rn+3, column=cn+2, sticky=E, padx=10)
    ent_V1.grid(row=rn+3, column=cn+1, sticky=W)
    ent_V2.grid(row=rn+3, column=cn+3, sticky=W)

    but_calc.grid(row=cn+9, column=2, sticky=E)
    but_info.grid(row=cn + 9, column=3)
    lab_down.grid(row=cn + 10, column=cn, columnspan=4)
    # lab_down2.grid(row=cn + 11, column=cn, sticky=W, columnspan=4)

    window.mainloop()


def start_page():
    def login(event):
        url = 'http://varcal.interiowo.pl/'
        string = requests.get(url).text
        correct_password = re.search(r'password=(.+)\s', string)
        correct_password = correct_password.group(1)
        input_password = ent_1.get()
        ent_1.delete(0, 'end')

        if correct_password == input_password:
            start_window.destroy()
            coefficient_calc()
        else:
            message = 'You typed: "{}" \nPlease type the correct password.'.format(input_password)
            tkm.showinfo('Wrong password', message)

    global start_window
    start_window = Tk()

    lab_login = Label(start_window, text='Welcome to the local coefficient of variation calculator!'
                                         ' Please log in: ', bg='white',fg='black')
    lab_1 = Label(start_window, text='password:')
    ent_1 = Entry(start_window)
    but_1 = Button(start_window, text='Continue')
    but_1.bind('<Button-1>', login)

    rn = 4
    cn = 1

    lab_login.grid(row=rn-4, columnspan=3)
    lab_1.grid(row=rn, column=cn)
    ent_1.grid(row=rn, column=cn+1)
    but_1.grid(row=rn+1, column=cn+1)
    start_window.mainloop()

start_page()
