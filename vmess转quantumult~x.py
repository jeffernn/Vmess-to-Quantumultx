import base64
import json
import tkinter as tk
from tkinter import ttk, scrolledtext
from urllib.parse import urlparse, parse_qs

# 现代配色方案
COLOR_SCHEME = {
    "primary": "#2c3e50",
    "secondary": "#3498db",
    "success": "#27ae60",
    "background": "#ecf0f1",
    "text": "#2c3e50",
    "highlight": "#e67e22"
}


def decode_vmess():
    # 清空状态栏
    status_bar.config(text="")

    link = entry.get().strip()
    if not link:
        show_status("⚠️ 请输入VMess链接", "warning")
        return

    try:
        data = link[len("vmess://"):] if link.startswith("vmess://") else link
        raw = base64.b64decode(data + '=' * (-len(data) % 4)).decode('utf-8')
        cfg = json.loads(raw)
    except Exception as e:
        output_text.delete(1.0, tk.END)
        show_status(f"❌ 解码失败: {str(e)}", "error")
        return

    # 解析字段
    address = cfg.get('add', '')
    port = cfg.get('port', '')
    uuid = cfg.get('id', '')
    net = cfg.get('net', '')
    host = cfg.get('host', '')
    path = cfg.get('path', '')
    tag = cfg.get('ps', '未命名配置')
    scy = cfg.get('scy', 'auto')
    tls = cfg.get('tls', '').lower()

    # 处理路径参数
    if path:
        parsed_uri = urlparse(path)
        if parsed_uri.query:
            query_params = parse_qs(parsed_uri.query)
            new_query = '&'.join(query_params.keys())
            path = parsed_uri.path + (f"?{new_query}" if new_query else "")

    # 构建结果
    result = (
        f"vmess={address}:{port}, method=aes-128-gcm, password={uuid},\n"
        f"obfs={'wss' if tls == 'tls' else net}, obfs-host={host},\n"
        f"obfs-uri={path}, tls-verification=false,\n"
        f"fast-open=false, udp-relay=false, aead={'true' if scy == 'auto' else 'false'},\n"
        f"tag={tag}"
    )

    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, result)
    output_text.config(state=tk.DISABLED)
    show_status("✅ 解码成功", "success")


def show_status(message, status_type="info"):
    colors = {
        "success": COLOR_SCHEME["success"],
        "error": "#e74c3c",
        "warning": COLOR_SCHEME["highlight"],
        "info": COLOR_SCHEME["secondary"]
    }
    status_bar.config(text=message, fg=colors.get(status_type, COLOR_SCHEME["text"]))


def copy_to_clipboard(event):
    content = output_text.get(1.0, tk.END).strip()
    if content:
        root.clipboard_clear()
        root.clipboard_append(content)
        show_status("📋 已复制到剪贴板", "success")
        # 添加动画效果
        root.after(100, lambda: output_text.config(bg="#f0f8ff"))
        root.after(200, lambda: output_text.config(bg="white"))


# GUI初始化
root = tk.Tk()
root.title("vmess加密链接转Quantumult x本地链接 By:Jeffern")
root.geometry('800x550')
root.configure(bg=COLOR_SCHEME["background"])

# 设置现代主题
style = ttk.Style()
style.theme_use('clam')
style.configure('TButton', font=('微软雅黑', 10), padding=6)
style.map('TButton',
          foreground=[('active', COLOR_SCHEME["primary"])],
          background=[('active', COLOR_SCHEME["background"])])

# 主框架
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill=tk.BOTH, expand=True)

# 标题
header = ttk.Label(main_frame,
                   text="vmess加密链接→Quantumult x本地链接",
                   font=('微软雅黑', 16, 'bold'),
                   foreground=COLOR_SCHEME["primary"])
header.pack(pady=(0, 15))

# 输入区域
input_frame = ttk.Frame(main_frame)
input_frame.pack(fill=tk.X, pady=5)

ttk.Label(input_frame,
          text="输入 VMess 链接：",
          font=('微软雅黑', 10)).pack(side=tk.LEFT, anchor=tk.W)

entry = ttk.Entry(input_frame, width=70)
entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
entry.focus()

# 解码按钮
decode_btn = ttk.Button(main_frame,
                        text="开始解码",
                        command=decode_vmess,
                        style='TButton')
decode_btn.pack(pady=10)

# 输出区域
output_frame = ttk.LabelFrame(main_frame,
                              text="解码结果",
                              padding=10,
                              style='TLabelframe')
output_frame.pack(fill=tk.BOTH, expand=True)

output_text = scrolledtext.ScrolledText(output_frame,
                                        height=8,
                                        font=('Consolas', 10),
                                        wrap=tk.WORD,
                                        padx=10,
                                        pady=10)
output_text.pack(fill=tk.BOTH, expand=True)
output_text.bind("<Button-1>", copy_to_clipboard)
output_text.config(state=tk.DISABLED)

# 状态栏
status_bar = ttk.Label(root,
                       text="就绪",
                       anchor=tk.W,
                       font=('微软雅黑', 9),
                       foreground=COLOR_SCHEME["text"])
status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=5)

# 绑定回车键
root.bind('<Return>', lambda event: decode_vmess())

root.mainloop()