import os
import subprocess
import sys
import tkinter as tk
from os import getcwd
from threading import Thread
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk, Tk, Text
from tkinter.ttk import Label, Entry, Button

from PIL import Image, ImageTk
from ttkbootstrap.constants import *


class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        self.text_space.insert(END, string)
        self.text_space.yview('end')

    @staticmethod
    def flush():
        pass

    def __exit__(self):
        pass


def call(exe, kz='Y', out=0, shstate=False, sp=0):
    if kz == "Y":
        cmd = f'{getcwd()}{os.sep}{exe}'
    else:
        cmd = exe
    if os.name != 'posix':
        conf = subprocess.CREATE_NO_WINDOW
    else:
        if sp == 0:
            cmd = cmd.split()
        conf = 0
    try:
        ret = subprocess.Popen(cmd, shell=shstate, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, creationflags=conf)
        for i in iter(ret.stdout.readline, b""):
            if out == 0:
                print(i.decode("utf-8", "ignore").strip())
    except subprocess.CalledProcessError as e:
        for i in iter(e.stdout.readline, b""):
            if out == 0:
                print(e.decode("utf-8", "ignore").strip())
    ret.wait()
    return ret.returncode


def cz(func, *args):
    Thread(target=func, args=args, daemon=True).start()


def unlock_miacc():
    print("请将手机连接到TWRP模式")
    lines = ['adb wait-for-device',
             'adb push rec/miacc_unlock.zip /sdcard/miacc_unlock.zip'
             'adb shell twrp install /sdcard/miacc_unlock.zip'
             'adb shell mke2fs -t ext4 /dev/block/by-name/userdata',
             'adb shell reboot system'
             ]
    for cmd in lines:
        if cmd.split()[0] == 'choice':
            call(cmd, kz='N')
        else:
            if call(cmd) != 0:
                print(f"运行{cmd}出现了错误")
            else:
                print(f'[{cmd.split()[0]}] 成功.')
    print('解锁MI账号成功！')


def end():
    print('正在关闭进程...')
    for t in [1, 2, 3]:
        call('taskkill /im fastboot.exe /f', kz='N')
        call('taskkill /im adb.exe /f', kz='N')
    root.destroy()


class MyTool(Tk):
    def __init__(self):
        super().__init__()
        self.title('MEDL845 V3.2')
        self.protocol("WM_DELETE_WINDOW", end)
        self.resizable(False, False)
        self.folder_path = tk.StringVar()
        self.number = tk.StringVar()
        self.subwin = ttk.LabelFrame(self, text='功能')
        self.logwin = ttk.LabelFrame(self, text='日志')
        self.init_log()
        self.logwin.pack(fill=BOTH, side=LEFT, expand=True, pady=5)
        self.subwin.pack(fill=BOTH, side=LEFT, expand=True, padx=5)
        self.notepad = ttk.Notebook(self.subwin)
        self.notepad.pack(fill=BOTH)
        self.tab = ttk.Frame(self.notepad)
        self.tab1 = ttk.Frame(self.notepad)
        self.flash = ttk.Frame(self.notepad)
        self.djt = ttk.Frame(self.notepad)
        self.about = ttk.Frame(self.notepad)
        self.notepad.add(self.tab, text="刷机救砖")
        self.notepad.add(self.flash, text="线刷工具箱")
        self.notepad.add(self.djt, text="短接图")
        self.notepad.add(self.tab1, text="其他")
        self.notepad.add(self.about, text="关于")
        self.init_tab()
        self.init_tab1()
        self.init_flash()
        self.init_djt()
        self.init_about()
        print("欢迎使用本工具。\n本工具永久免费,禁止倒卖!\n开发者： ColdWindScholar & XEKNICE & "
              "AGXMX\n开源地址:https://github.com/ColdWindScholar/MEDL845")

    def init_tab(self):
        # ----
        Frame = ttk.Frame(self.tab)
        self.folder_label = Label(Frame, text='救砖包文件夹:')
        self.folder_label.pack(side=LEFT, padx=5, pady=5)
        self.folder_entry = Entry(Frame, textvariable=self.folder_path)
        self.folder_entry.pack(side=LEFT, padx=5, pady=5)
        self.folder_button = Button(Frame, text='浏览', command=self.select_folder)
        self.folder_button.pack(side=LEFT, padx=5, pady=5)
        Frame.pack(fill=X)
        # -----
        # -----
        Frame = ttk.Frame(self.tab)
        self.number_label = Label(Frame, text='9008端口号：')
        self.number_label.pack(side=LEFT, padx=5, pady=5)
        self.number_entry = Entry(Frame, textvariable=self.number)
        self.number_entry.pack(side=LEFT, padx=5, pady=5)
        Frame.pack(fill=X)
        # -----
        self.start_button = Button(self.tab, text='开始刷入', command=lambda: cz(self.start_running))
        self.start_button.pack(padx=5, pady=5)
        self.start_edl = Button(self.tab, text='进入9008模式', command=lambda: cz(self.edl))
        self.start_edl.pack()
        self.close_button = Button(self.tab, text='关闭此程序', command=end)
        self.close_button.pack(side=BOTTOM)
        # 刷入____

    def init_tab1(self):

        self.fix_button = Button(self.tab1, text='安装/修复驱动', command=self.FIX, width=20)
        self.fix_button.pack(padx=5, pady=5)
        self.fix_button = Button(self.tab1, text='绕MIUI账号锁', command=lambda: cz(self.ZHS), width=20)
        self.fix_button.pack(padx=5, pady=5)
        self.fix_button = Button(self.tab1, text='强解bootloader锁', command=self.BL, width=20)
        self.fix_button.pack(padx=5, pady=5)
        self.GY_button = Button(self.tab1, text='MIX2S专用FB镜像工具箱',
                                command=lambda: cz(os.system, "start res\\fbimg.bat"), width=20)
        self.GY_button.pack(padx=5, pady=5)

    def init_flash(self):
        def disable():
            self.file_entry.configure(state='disabled')
            self.flash_reboot.configure(state='disabled')
            self.flash_run.configure(state='disabled')

        def able():
            self.file_entry.configure(state='normal')
            self.flash_reboot.configure(state='normal')
            self.flash_run.configure(state='normal')

        def set_img():
            if path := self.select_file():
                self.file_entry.delete(0, END)
                self.file_entry.insert(0, path)

        def run():
            if not self.file_entry.get():
                print("请输入镜像路径")
                return
            self.flash_run.configure(text='正在执行')
            disable()
            if self.flash_cz.get() == 1:
                if call(f'fastboot flash {self.part.get()} {self.file_entry.get()}') != 0: print("操作失败！")
            elif self.flash_cz.get() == 2:
                if call(f'fastboot erase {self.part.get()}') != 0: print("操作失败！")
            elif self.flash_cz.get() == 3:
                if call(f'fastboot boot {self.file_entry.get()}') != 0:
                    print("操作失败！")
            self.flash_run.configure(text='执行')
            able()

        def reboot():
            self.flash_reboot.configure(text='正在重启')
            disable()
            call('fastboot reboot')
            self.flash_reboot.configure(text='重启')
            able()

        Label(self.flash, text='线刷工具箱', font=(None, 15)).pack(side=TOP, padx=5, pady=5)
        # ----
        Frame = ttk.Frame(self.flash)
        Label(Frame, text='镜像文件:').pack(side=LEFT, padx=5, pady=5)
        self.file_entry = Entry(Frame)
        self.file_entry.pack(side=LEFT, padx=5, pady=5)
        self.file_button = Button(Frame, text='浏览', command=set_img)
        self.file_button.pack(side=LEFT, padx=5, pady=5)
        Frame.pack(fill=X, padx=5, pady=5)
        # -----
        # ---
        Frame = ttk.Frame(self.flash)
        Label(Frame, text='操作分区:').pack(side=LEFT, padx=5, pady=5)
        self.part = ttk.Combobox(Frame, values=['recovery', 'boot', 'system', 'vendor'])
        self.part.current(0)
        self.part.pack(side=LEFT)
        Frame.pack(fill=X, padx=5, pady=5)
        # ---
        Frame = ttk.Frame(self.flash)
        Label(Frame, text='操作:').pack(side=LEFT, padx=5, pady=5)
        self.flash_cz = tk.IntVar()
        self.flash_cz.set(1)
        cs = 0
        for v in ['刷入', '擦除', '临时启动']:
            cs += 1
            ttk.Radiobutton(Frame, text=v, variable=self.flash_cz, value=cs).pack(side=LEFT, padx=2, pady=2)
        Frame.pack(fill=X, padx=5, pady=5)
        self.flash_run = Button(self.flash, text='执行', command=lambda: cz(run))
        self.flash_run.pack(fill=X, padx=5, pady=5)
        self.flash_reboot = Button(self.flash, text='重启手机', command=lambda: cz(reboot))
        self.flash_reboot.pack(fill=X, padx=5, pady=5)

    def init_djt(self):
        def next(name):
            pics = {
                'MI MIX2S': 'res/MIX2S.jpeg',
                'MI MIX3': 'res/MIX3.png',
                'MI 8': 'res/MI8.jpg',
                'MI8探索/屏幕指纹版': 'res/MI8EE.jpg'
            }
            global img
            try:
                img = Image.open(pics[self.qh.get()]).resize((400, 450))
            except:
                img = Image.open(pics['MI MIX2S']).resize((400, 450))
            global photo
            photo = ImageTk.PhotoImage(img)
            self.djt_.configure(image=photo)

        self.djt_ = Label(self.djt, width=200)
        self.djt_.pack(fill=BOTH)
        self.qh = ttk.Combobox(self.djt, values=['MI MIX2S', 'MI MIX3', 'MI 8', 'MI8探索/屏幕指纹版'], state='readonly')
        self.qh.current(0)
        self.qh.bind('<<ComboboxSelected>>', next)
        next(self)
        self.qh.pack()

    def init_about(self):
        Label(self.about, text='MEDL845 V3.2', font=(None, 17)).pack(padx=5, pady=5)
        self.GY_button = Button(self.about, text='查看说明', command=lambda: cz(os.system, 'start res/SM.png'),
                                width=20)
        self.GY_button.pack(padx=5, pady=5)
        self.number_label = Label(self.about, text='官网链接：miui845.agxmx.top\nAGXMX & ColdWindScholar保留所有权利。')
        self.number_label.pack(side=BOTTOM)

    def init_log(self):
        self.log = Text(self.logwin)
        self.log.pack(padx=5, pady=5)
        Frame = ttk.Frame(self.logwin)
        Button(Frame, text='清空', command=lambda: cz(self.log.delete, 1.0, END)).pack(side=LEFT, padx=5, pady=5)
        Frame.pack(fill=X, side=BOTTOM)
        sys.stdout = StdoutRedirector(self.log)
        sys.stderr = StdoutRedirector(self.log)

    def select_folder(self):
        if path := filedialog.askdirectory():
            self.folder_path.set(path)

    def select_file(self):
        if path := filedialog.askopenfilename(filetypes=[('bin', '*.bin'), ('image', '*.img')]):
            return path
        else:
            return None

    def start_running(self):
        if not self.folder_path.get() or not self.number.get().isdigit():
            messagebox.showerror('错误', '请确保文件夹路径已选择且端口号为数字')
            return None
        else:
            path = self.folder_path.get()
            converted_path = path.replace('/', '\\')
            a = os.path.normpath(converted_path)
            self.start_button.config(state='disabled')
            self.close_button.config(state='disabled')
            self.start_edl.config(state='disabled')
            self.fix_button.config(state='disabled')
            if errorlevel := call(f'MIQC845Flash.exe -P {self.number.get()} {a} exit') == 0:
                messagebox.showinfo('刷机结束', '刷机进程结束！ 请长按电源键尝试重启？')
            else:
                messagebox.showerror('刷机错误！', f'很抱歉， 刷机错误！错误代码：{errorlevel}')
        self.start_button.config(state='normal')
        self.close_button.config(state='normal')
        self.start_edl.config(state='normal')
        self.fix_button.config(state='normal')

    def edl(self):
        self.start_edl.config(state='disabled', text="正在等待设备")
        call('fastboot.exe oem edl')
        os.system('start devmgmt.msc')
        self.start_edl.config(state='normal', text='进入9008模式')

    def FIX(self):
        messagebox.showinfo('注意', '本功能需要程序拥有管理员权限！\n执行后请将电脑重新启动！')
        call('res/FIX.exe')
        call('res/USB.bat')

    def ZHS(self):
        messagebox.showinfo('注意', '此功能仅限于845系列\n手机先进入TWRP模式')
        unlock_miacc()

    def BL(self):
        messagebox.showinfo('注意',
                            '机型、MIUI版本支持列表\n小米6: MIUI 9.6.3.0 \n小米6X: MIUI 9.6.4.0 \n小米8: MIUI 9.6.6.0 \n小米8SE: MIUI '
                            '9.5.11.0 \n小米8探索版: MIUI 9.6.7.0 \n小米Note 3: MIUI 9.6.3.0 \n小米MAX 3: MIUI 9.6.9.0 \n小米MIX '
                            '2: MIUI 9.6.3.0 \n小米MIX 2S: MIUI 9.6.8.0 \n小米平板4: MIUI 9.6.23.0 \n红米Note 5: MIUI 9.6.4.0 '
                            '\n版本以上系统自行拆机短接9008降级到MIUI9.6以下最好是出厂系统后再用此工具解锁BL')
        call('res/BL.exe')


if __name__ == '__main__':
    root = MyTool()
    root.mainloop()
