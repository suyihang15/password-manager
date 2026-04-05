import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
from cryptography.fernet import Fernet

# 密钥文件名
KEY_FILE = "secret.key"
# 密码数据文件名
DATA_FILE = "passwords.json"

# 加载密钥，不存在则生成
def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    with open(KEY_FILE, "rb") as f:
        return f.read()

# 初始化加密器
key = load_key()
cipher = Fernet(key)

# 保存数据（加密）
def save_data(data):
    json_data = json.dumps(data).encode()
    encrypted_data = cipher.encrypt(json_data)
    with open(DATA_FILE, "wb") as f:
        f.write(encrypted_data)

# 加载数据（解密）
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "rb") as f:
        encrypted_data = f.read()
    decrypted_data = cipher.decrypt(encrypted_data).decode()
    return json.loads(decrypted_data)

# 主窗口
root = tk.Tk()
root.title("密码记录本")
root.geometry("600x400")

# 表格
columns = ("网站", "账号", "密码", "备注")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# 刷新表格
def refresh_list():
    for item in tree.get_children():
        tree.delete(item)
    data = load_data()
    for item in data:
        tree.insert("", tk.END, values=(item["site"], item["user"], item["pwd"], item["note"]))

# 添加密码窗口
def add_window():
    win = tk.Toplevel(root)
    win.title("添加密码")
    win.geometry("400x250")

    tk.Label(win, text="网站/应用：").grid(row=0, column=0, padx=10, pady=10)
    site_entry = tk.Entry(win)
    site_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(win, text="账号：").grid(row=1, column=0, padx=10, pady=10)
    user_entry = tk.Entry(win)
    user_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(win, text="密码：").grid(row=2, column=0, padx=10, pady=10)
    pwd_entry = tk.Entry(win)
    pwd_entry.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(win, text="备注：").grid(row=3, column=0, padx=10, pady=10)
    note_entry = tk.Entry(win)
    note_entry.grid(row=3, column=1, padx=10, pady=10)

    def save_new():
        site = site_entry.get()
        user = user_entry.get()
        pwd = pwd_entry.get()
        note = note_entry.get()
        if not site or not user or not pwd:
            messagebox.showwarning("提示", "网站、账号、密码不能为空！")
            return
        data = load_data()
        data.append({"site": site, "user": user, "pwd": pwd, "note": note})
        save_data(data)
        refresh_list()
        win.destroy()
        messagebox.showinfo("成功", "保存成功！")

    tk.Button(win, text="保存", command=save_new).grid(row=4, column=0, columnspan=2, pady=10)

# 删除选中
def delete_selected():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("提示", "请先选择一条记录！")
        return
    data = load_data()
    idx = tree.index(selected[0])
    del data[idx]
    save_data(data)
    refresh_list()
    messagebox.showinfo("成功", "删除成功！")

# 按钮
frame = tk.Frame(root)
frame.pack(pady=5)
tk.Button(frame, text="添加", command=add_window).pack(side=tk.LEFT, padx=5)
tk.Button(frame, text="删除选中", command=delete_selected).pack(side=tk.LEFT, padx=5)

# 启动
refresh_list()
root.mainloop()