from tkinter import *
from deal import Function  # 导入功能模块
import tkinter.messagebox
from connect_mysql import connect_mysql  # 导入数据库链接模块

# 创建数据库操作对象，链接数据库
conn, cursor = connect_mysql()


# 创建窗口和功能
class Main:
    # 窗口初始化
    def __init__(self):
        self.window = Tk()
        self.window.title('课堂学习状态管理系统 登录')
        self.window.geometry('600x400')
        self.window.resizable(False, False)
        self.canvas = Canvas(self.window, height=400, width=600)
        self.bg_image = PhotoImage(file="image/bg.GIF")
        self.canvas.pack(side='top')
        self.image = self.canvas.create_image(0, 0, anchor='nw', image=self.bg_image)
        self.lb1 = Label(self.window, text='用户名：', width=7, height=2).place(x=200, y=150)
        self.lb2 = Label(self.window, text=' 密码：', width=7, height=2).place(x=200, y=200)
        self.get_user_name = StringVar()
        self.en_user_name = Entry(self.window, textvariable=self.get_user_name)
        self.en_user_name.place(x=260, y=150, height=40)
        self.get_user_pwd = StringVar()
        self.en_user_pwd = Entry(self.window, textvariable=self.get_user_pwd, show='*')
        self.en_user_pwd.place(x=260, y=200, height=40)
        self.bt_login = Button(self.window, text='登陆', command=self.user_login, width=10, height=2)
        self.bt_login.place(x=150, y=300)
        self.bt_logup = Button(self.window, text='注册', command=self.user_register, width=10, height=2)
        self.bt_logup.place(x=250, y=300)
        self.bt_quit = Button(self.window, text='退出', command=self.window.destroy, width=10, height=2)
        self.bt_quit.place(x=350, y=300)
        self.window.mainloop()

    # 用户登录功能
    def user_login(self):
        user_name = self.get_user_name.get()
        user_pwd = self.get_user_pwd.get()
        try:
            sql = "select * from users where user_name ='" + user_name + "' and password='" + user_pwd + "'"
            cursor.execute(sql)
            result = cursor.fetchone()
            if user_name == "" or user_pwd == "":
                tkinter.messagebox.showerror(title="Error", message="用户名或密码不能为空！")
            elif result is not None:
                tkinter.messagebox.showinfo(title="welcome", message="欢迎" + str(user_name))
                self.window.destroy()
                Function()
            else:
                tkinter.messagebox.showerror(title="Error", message="用户名或密码错误，再试一次吧！")
        except Exception:
            tkinter.messagebox.showerror("登录异常！")

    # 用户注册功能
    def user_register(self):
        window_sign_up = tkinter.Toplevel(self.window)
        window_sign_up.title("python学生信息管理系统-bhml 注册")
        window_sign_up.geometry('600x400')
        window_sign_up.resizable(False, False)
        canvas_sign = Canvas(window_sign_up, height=400, width=600)
        canvas_sign.pack(side='top')
        image_sign = canvas_sign.create_image(0, 0, anchor='nw', image=self.bg_image)
        lb3 = Label(window_sign_up, text="用户名：", width=7, height=2).place(x=200, y=100)
        lb4 = Label(window_sign_up, text="密码：", width=7, height=2).place(x=200, y=150)
        lb5 = Label(window_sign_up, text="确认密码:", width=7, height=2).place(x=200, y=200)
        self.new_user_name = tkinter.StringVar()
        en_new_name = Entry(window_sign_up, textvariable=self.new_user_name)
        en_new_name.place(x=260, y=100, height=40)
        self.new_user_pwd = tkinter.StringVar()
        en_use_pwd = Entry(window_sign_up, textvariable=self.new_user_pwd, show='*')
        en_use_pwd.place(x=260, y=150, height=40)
        self.new_pwd_again = tkinter.StringVar()
        en_pwd_again = Entry(window_sign_up, textvariable=self.new_pwd_again, show='*')
        en_pwd_again.place(x=260, y=200, height=40)
        bt1 = Button(window_sign_up, text="注册", command=self.sign_up, width=10, height=2)
        bt1.place(x=200, y=280)
        bt2 = Button(window_sign_up, text="取消", command=self.no_sig, width=10, height=2)
        bt2.place(x=300, y=280)

    # 用户注册功能实现
    def sign_up(self):
        new_name = self.new_user_name.get()
        new_pwd = self.new_user_pwd.get()
        pwd_again = self.new_pwd_again.get()
        try:
            sql = "select user_name from users where user_name='" + new_name + "'"
            cursor.execute(sql)
            result = cursor.fetchone()
            if new_pwd == "" or pwd_again == "" or new_name == "":
                tkinter.messagebox.showerror(title="Error", message="用户名或密码不能为空")
            elif result != None:
                tkinter.messagebox.showerror(title="Error", message="用户名已被注册")
            elif new_pwd == pwd_again:
                try:
                    sql2 = 'insert into users(user_name, password) values ("'"%s"'", "'"%s"'")' % (new_name, new_pwd)
                    cursor.execute(sql2)
                    conn.commit()
                    tkinter.messagebox.showinfo(title="注册成功", message="恭喜你注册成功，请前往登陆")
                except Exception as e:
                    tkinter.messagebox.showerror(e)
            else:
                tkinter.messagebox.showerror(title="Error", message="两次密码不一致")
        except Exception as e:
            tkinter.messagebox.showerror(e)

    # 取消注册
    def no_sig(self):
        conn.close()
        self.window.destroy()
        Main()


# 执行程序，创建窗口
Main()
