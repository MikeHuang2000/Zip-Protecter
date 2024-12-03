import os
import tkinter as tk
#import tkinterdnd2
#DND_FILES = tkinterdnd2.DND_FILES
#TkinterDnD = tkinterdnd2.TkinterDnD
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import messagebox

#模块------------------------------------------------------------------
def enprotect(file_path):
    with open(file_path, 'rb') as f:
        patch = "50 4B 03 04 0A 00 00 00 00 00 98 A9 3E 3E 00 00 00 00 00 00 00 00 00 00 00 00 08 00 00 00 FF 2E 72 73 64 61 74 61 50 4B 01 02 3F 00 0A 00 00 00 00 00 98 A9 3E 3E 00 00 00 00 00 00 00 00 00 00 00 00 08 00 24 00 00 00 00 00 00 00 20 00 00 00 00 00 00 00 FF 2E 72 73 64 61 74 61 0A 00 20 00 00 00 00 00 01 00 18 00 96 BD CF 0F BA C0 CB 01 B5 82 C7 2D BB C0 CB 01 1C C5 DC 00 BA C0 CB 01 50 4B 05 06 00 00 00 00 01 00 01 00 5A 00 00 00 26 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"
        patch_bytes = bytearray.fromhex(patch.replace(' ', ''))
        data = f.read()
        if data[0:160] == patch_bytes:
            messagebox.showinfo(title="提示", message="已经保护了！")
        else:
            data = patch_bytes + data
            with open(file_path, 'wb') as f:
                f.write(data)
                messagebox.showinfo(title="提示", message="保护完成！")


def read_and_store_binary_file(file_path, skip_bytes, store_path):
    with open(file_path, 'rb') as f:
        patch = "50 4B 03 04 0A 00 00 00 00 00 98 A9 3E 3E 00 00 00 00 00 00 00 00 00 00 00 00 08 00 00 00 FF 2E 72 73 64 61 74 61 50 4B 01 02 3F 00 0A 00 00 00 00 00 98 A9 3E 3E 00 00 00 00 00 00 00 00 00 00 00 00 08 00 24 00 00 00 00 00 00 00 20 00 00 00 00 00 00 00 FF 2E 72 73 64 61 74 61 0A 00 20 00 00 00 00 00 01 00 18 00 96 BD CF 0F BA C0 CB 01 B5 82 C7 2D BB C0 CB 01 1C C5 DC 00 BA C0 CB 01 50 4B 05 06 00 00 00 00 01 00 01 00 5A 00 00 00 26 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"
        patch_bytes = bytearray.fromhex(patch.replace(' ', ''))
        data = f.read()
        if data[0:160] == patch_bytes:
            # 跳过开头的指定长度的字节
            f.seek(skip_bytes)
            # 读取剩余的字节
            data = f.read()
            # 将读取的字节存储到指定文件
            with open(store_path, 'wb') as store_f:
                store_f.write(data)
                messagebox.showinfo(title="提示", message="解除保护完成！")
        else:
            messagebox.showinfo(title="提示", message="已经解除保护了！")

def on_drag(event):
    event.widget.delete(0, tk.END)  # 清空输入框内容
    event.widget.insert(tk.END, event.data)  # 将文件路径插入输入框

#初始化-------------------------------------------------------------------

#传递参数会改变工作路径，更改工作路径以在接受参数时正确运行和读取ini
os.chdir(os.path.dirname(os.path.abspath(__file__)))



#GUI-------------------------------------------------------------------
root = TkinterDnD.Tk()
root.title('zipprotecter')

file_label = tk.Label(root, text="待处理文件（支持拖入）：", anchor="w")
file_label.pack(anchor='w')

file_entry = tk.Entry(root, width=40)
file_entry.pack(pady=10)
file_entry.drop_target_register(DND_FILES)
file_entry.dnd_bind('<<Drop>>', on_drag)

frame1 = tk.Frame(root) # 生成第一组按钮的容器
frame1.pack(anchor="w",pady=1,ipadx=20)

en_button = tk.Button(frame1,text="保护", width=20,command=lambda: enprotect(file_entry.get()))
#en_button = tk.Button(frame1,text="加密", width=20,command=lambda: os.system("copy /b /Y "+"patch.txt + "+str(file_entry.get()).replace("/","\\")+" "+str(file_entry.get()).replace("/","\\")))
#en_button = tk.Button(frame1,text="加密", width=20,command=lambda: print("copy /b /Y "+"patch.txt + "+str(file_entry.get()).replace("/","\\")+" "+str(file_entry.get()).replace("/","\\")))
en_button.pack(side='left')

un_button = tk.Button(frame1,text="解除", width=20,command=lambda: read_and_store_binary_file(file_entry.get(), 160, file_entry.get()))
un_button.pack(side='right')

root.mainloop() 


