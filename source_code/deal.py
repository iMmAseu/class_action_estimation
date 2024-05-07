"""
项目名称：python+mysql+tkinter的学生信息管理系统
作者：bhml
时间：2022/11/28
代码功能：功能界面实现，以及对学生信息的处理
"""
# 导入所需模块
import tkinter
from tkinter import *
from tkinter import ttk, messagebox
from connect_mysql import connect_mysql

# 链接数据库
conn, cursor = connect_mysql()


# 主界面的初始化
class Function:
    # 界面设计
    def __init__(self):
        self.window = Tk()
        self.window.title('python学生信息管理系统-bhml')
        self.window.geometry('750x450')
        self.canvas = Canvas(self.window, height=450, width=750)
        self.bg_image = PhotoImage(file="image/bg2.GIF")
        self.window.resizable(False, False)
        self.canvas.pack(side='top')
        self.image = self.canvas.create_image(0, 0, anchor='nw', image=self.bg_image)
        bt1 = Button(self.window, text='添加学生信息', command=self.insertItem, width=10, height=2)
        bt1.place(x=70, y=190)
        bt2 = Button(self.window, text='删除学生信息', command=self.deleteItem, width=10, height=2)
        bt2.place(x=70, y=260)
        bt3 = Button(self.window, text='修改学生信息', command=self.updateItem, width=10, height=2)
        bt3.place(x=70, y=330)
        lb4 = Label(self.window, text='学号：', width=7, height=2).place(x=200, y=20)
        lb5 = Label(self.window, text='姓名：', width=7, height=2).place(x=200, y=70)
        lb6 = Label(self.window, text='班级：', width=7, height=2).place(x=200, y=120)
        bt4 = Button(self.window, text='           查询           ', command=self.search, width=10, height=2).place(
            x=450, y=120)
        bt5 = Button(self.window, text="退出系统", width=10, height=2, command=self.exit)
        bt5.place(x=550, y=120)

        bt6 = Button(self.window, text="刷新数据", width=10, height=2, command=self.refresh)
        bt6.place(x=650, y=120)

        self.sdut_id = StringVar()
        self.en_sdut_id = Entry(self.window, textvariable=self.sdut_id)
        self.en_sdut_id.place(x=270, y=20, height=40)

        self.sdut_name = StringVar()
        self.en_sdut_name = Entry(self.window, textvariable=self.sdut_name)
        self.en_sdut_name.place(x=270, y=70, height=40)

        self.sdut_class = StringVar()
        self.en_sdut_class = Entry(self.window, textvariable=self.sdut_class)
        self.en_sdut_class.place(x=270, y=120, height=40)
        self.tree = ttk.Treeview(self.window, show="headings")
        self.tree["columns"] = ("0", "1", "2", "3", "4")
        self.tree.place(x=200, y=180)
        self.tree.column('0', width=100, anchor='center')
        self.tree.column('1', width=100, anchor='center')
        self.tree.column('2', width=100, anchor='center')
        self.tree.column('3', width=100, anchor='center')
        self.tree.column('4', width=100, anchor='center')
        self.tree.heading('0', text='学号')
        self.tree.heading('1', text='姓名')
        self.tree.heading('2', text='性别')
        self.tree.heading('3', text='班级')
        self.tree.heading('4', text='成绩')
        result = self.show()
        for res in result:
            li = [res[0], res[1], res[2], res[3], res[4]]
            self.tree.insert('', 'end', values=li)
        self.window.mainloop()

    # 修改功能
    def update_mysql(self):
        for item in self.tree.selection():
            item_text = self.tree.item(item, "values")
            new_id = self.new_id.get()
            new_name = self.new_name.get()
            new_sex = self.new_sex.get()
            new_class = self.new_class.get()
            new_score = self.new_score.get()
            try:
                sql2 = 'update information set id="' + new_id + '", name="' + new_name + '", sex="' + new_sex + '", class="' + new_class + '", score="' + new_score + '" where id="' + \
                       item_text[0] + '"'
                cursor.execute(sql2)
                conn.commit()
                tkinter.messagebox.showinfo(title="修改成功", message="恭喜你修改成功，请前往操作")
            except Exception:
                tkinter.messagebox.showerror("修改数据异常，修改失败！")

    # 修改按钮事件(按键操作)
    def updateItem(self):
        if self.tree.selection() == ():
            tkinter.messagebox.showinfo(title="提示", message="请先选择需要修改的学生")
        else:
            for item in self.tree.selection():
                item_text = self.tree.item(item, "values")
                window_insert = tkinter.Toplevel(self.window)
                window_insert.title("修改学生信息")
                window_insert.geometry('500x400')
                window_insert.resizable(False, False)
                canvas_insert = Canvas(window_insert, height=400, width=500)
                canvas_insert.pack(side="top")
                i_insert = canvas_insert.create_image(0, 0, anchor='nw', image=self.bg_image)
                Label(window_insert, text="学号：").place(x=100, y=70)
                Label(window_insert, text="姓名：").place(x=100, y=110)
                Label(window_insert, text="性别:").place(x=100, y=150)
                Label(window_insert, text="班级:").place(x=100, y=190)
                Label(window_insert, text="分数:").place(x=100, y=230)
                self.new_id = tkinter.StringVar()
                en_new_id = Entry(window_insert, textvariable=self.new_id)
                en_new_id.place(x=160, y=70)
                en_new_id.insert(10, item_text[0])
                self.new_name = tkinter.StringVar()
                en_use_name = Entry(window_insert, textvariable=self.new_name)
                en_use_name.place(x=160, y=110)
                en_use_name.insert(10, item_text[1])
                self.new_sex = tkinter.StringVar()
                en_new_sex = Entry(window_insert, textvariable=self.new_sex)
                en_new_sex.place(x=160, y=150)
                en_new_sex.insert(10, item_text[2])
                self.new_class = tkinter.StringVar()
                en_class = Entry(window_insert, textvariable=self.new_class)
                en_class.place(x=160, y=190)
                en_class.insert(10, item_text[3])
                self.new_score = tkinter.StringVar()
                en_new_score = Entry(window_insert, textvariable=self.new_score)
                en_new_score.place(x=160, y=230)
                en_new_score.insert(10, item_text[4])
                bt1 = Button(window_insert, text="修改", command=self.update_mysql, width=10, height=2)
                bt1.place(x=100, y=300)
                bt2 = Button(window_insert, text="取消", command=window_insert.destroy, width=10, height=2)
                bt2.place(x=300, y=300)

    # 增加按钮事件(按键操作)
    def insertItem(self):
        window_insert = tkinter.Toplevel(self.window)
        window_insert.title("增加学生信息")
        window_insert.geometry('500x400')
        window_insert.resizable(False, False)
        canvas_insert = Canvas(window_insert, height=400, width=500)
        canvas_insert.pack(side='top')
        image_insert = canvas_insert.create_image(0, 0, anchor='nw', image=self.bg_image)
        Label(window_insert, text="学号：").place(x=100, y=70)
        Label(window_insert, text="姓名：").place(x=100, y=110)
        Label(window_insert, text="性别:").place(x=100, y=150)
        Label(window_insert, text="班级:").place(x=100, y=190)
        Label(window_insert, text="分数:").place(x=100, y=230)
        self.new_id = tkinter.StringVar()
        en_new_id = Entry(window_insert, textvariable=self.new_id)
        en_new_id.place(x=160, y=70)
        self.new_name = tkinter.StringVar()
        en_use_name = Entry(window_insert, textvariable=self.new_name)
        en_use_name.place(x=160, y=110)
        self.new_sex = tkinter.StringVar()
        en_new_sex = Entry(window_insert, textvariable=self.new_sex)
        en_new_sex.place(x=160, y=150)
        self.new_class = tkinter.StringVar()
        en_class = Entry(window_insert, textvariable=self.new_class)
        en_class.place(x=160, y=190)
        self.new_score = tkinter.StringVar()
        en_new_score = Entry(window_insert, textvariable=self.new_score)
        en_new_score.place(x=160, y=230)
        bt1 = Button(window_insert, text="添加", command=self.insert_mysql, width=10, height=2)
        bt1.place(x=100, y=290)
        bt2 = Button(window_insert, text="取消", command=window_insert.destroy, width=10, height=2)
        bt2.place(x=280, y=290)

    # 数据库的添加学生信息
    def insert_mysql(self):
        new_id = self.new_id.get()
        new_name = self.new_name.get()
        new_sex = self.new_sex.get()
        new_class = self.new_class.get()
        new_score = self.new_score.get()
        try:
            sql = "select * from information where id='" + new_id + "' and name='" + new_name + "'"
            cursor.execute(sql)
            result = cursor.fetchone()
            if result is not None:
                tkinter.messagebox.showerror(title="Error", message="该学生信息已存在")
            else:
                try:
                    sql2 = 'insert into information(id, name, sex, class, score) values ("'"%s"'", "'"%s"'", "'"%s"'", "'"%s"'", "'"%s"'")' % (
                        new_id, new_name, new_sex, new_class, new_score)
                    cursor.execute(sql2)
                    conn.commit()
                    tkinter.messagebox.showinfo(title="添加成功", message="恭喜你添加成功，请前往操作")
                except Exception:
                    tkinter.messagebox.showerror("添加异常！")
        except Exception:
            tkinter.messagebox.showerror("添加异常！")

    # 删除单条记录
    def deleteItem(self):
        for item in self.tree.selection():
            if item is None:
                tkinter.messagebox.showinfo(title="提示", message="错误!请先选择需要删除的学生")
            else:
                item_text = self.tree.item(item, "values")
                print(item_text[0], item_text[1], item_text[2], item_text[3], item_text[4])  # 输出所选行的第一列的值
                try:
                    print(item_text[0])
                    sql = "delete from information where id='" + item_text[0] + "' and name='" + item_text[1] + "'"
                    cursor.execute(sql)
                    conn.commit()
                    result = self.show()
                    x = self.tree.get_children()
                    for item in x:
                        self.tree.delete(item)
                    for res in result:
                        li = [res[0], res[1], res[2], res[3], res[4]]
                        self.tree.insert('', 'end', values=li)
                except Exception:
                    tkinter.messagebox.showerror("删除失败")
                    conn.rollback()  # 回滚（数据库数据回到删除前的状态）

    # 单条记录进行查询
    def search(self):
        id = self.sdut_id.get()
        name = self.sdut_name.get()
        sdut_class = self.sdut_class.get()
        if name == '' and sdut_class == '' and id == '':
            tkinter.messagebox.showinfo(title="提示", message="请填写查询信息！")
        else:
            try:
                sql = "select * from information where id='" + id + "' or name='" + name + "' or class='" + sdut_class + "'"
                cursor.execute(sql)
                result = cursor.fetchall()
                print(result)
                if result is None:
                    tkinter.messagebox.showinfo(title="提示", message="未查询到该学生")
                else:
                    x = self.tree.get_children()
                    for item in x:
                        self.tree.delete(item)
                    for res in result:
                        li = [res[0], res[1], res[2], res[3], res[4]]
                        self.tree.insert('', 'end', values=li)
            except Exception:
                tkinter.messagebox.showerror("数据查询异常！")

    # 查询所有信息
    def show(self):
        try:
            sql = "select * from information"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except:
            tkinter.messagebox.showerror("查询异常！")

    # 刷新页面
    def refresh(self):
        result = self.show()
        self.sdut_class = StringVar()
        self.en_sdut_class = Entry(self.window, textvariable=self.sdut_class)
        self.en_sdut_class.place(x=270, y=120, height=40)
        self.tree = ttk.Treeview(self.window, show="headings")
        self.tree["columns"] = ("0", "1", "2", "3", "4")
        self.tree.place(x=200, y=180)
        self.tree.column('0', width=100, anchor='center')
        self.tree.column('1', width=100, anchor='center')
        self.tree.column('2', width=100, anchor='center')
        self.tree.column('3', width=100, anchor='center')
        self.tree.column('4', width=100, anchor='center')
        self.tree.heading('0', text='学号')
        self.tree.heading('1', text='姓名')
        self.tree.heading('2', text='性别')
        self.tree.heading('3', text='班级')
        self.tree.heading('4', text='成绩')
        for res in result:
            li = [res[0], res[1], res[2], res[3], res[4]]
            self.tree.insert('', 'end', values=li)

    # 退出系统
    def exit(self):
        conn.close()
        self.window.destroy()
