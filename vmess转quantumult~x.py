import base64
import json
import tkinter as tk
from tkinter import scrolledtext
from urllib.parse import urlparse, parse_qs

def decode_vmess():
    link = entry.get().strip()
    if link.startswith("vmess://"):
        data = link[len("vmess://"):]
    else:
        data = link

    try:
        raw = base64.b64decode(data).decode('utf-8')
        cfg = json.loads(raw)
    except Exception as e:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"❌ 解码失败: {e}")
        return

    address = cfg.get('add', '')
    port = cfg.get('port', '')
    uuid = cfg.get('id', '')
    net = cfg.get('net', '')
    host = cfg.get('host', '')
    path = cfg.get('path', '')
    tag = cfg.get('ps', '')
    scy = cfg.get('scy', '')
    tls = cfg.get('tls', '')

    # 处理路径和查询参数
    if path:
        parsed_uri = urlparse(path)
        if parsed_uri.query:
            query_params = parse_qs(parsed_uri.query)
            # 仅保留参数名，去除值
            new_query = '&'.join(query_params.keys())
            path = parsed_uri.path + ('?' + new_query if new_query else '')
        else:
            path = parsed_uri.path

    obfs = net if tls.lower() != 'tls' else 'wss'
    aead = 'true' if scy.lower() == 'auto' else 'false'

    result = (
        f"vmess={address}:{port}, method=aes-128-gcm, password={uuid}, "
        f"obfs={obfs}, obfs-host={host}, obfs-uri={path}, "
        f"tls-verification=false, fast-open=false, udp-relay=false, "
        f"aead={aead}, tag={tag}"
    )

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, result)

# GUI部分保持不变
root = tk.Tk()
root.title("VMess 链接解码器")
root.geometry('700x400')

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill='both', expand=True)

label = tk.Label(frame, text="输入 vmess 链接:")
label.pack(anchor='w')

entry = tk.Entry(frame, width=80)
entry.pack(fill='x', pady=5)

btn = tk.Button(frame, text="解码", command=decode_vmess)
btn.pack(pady=5)

output_label = tk.Label(frame, text="解码结果:")
output_label.pack(anchor='w', pady=(10, 0))

output_text = scrolledtext.ScrolledText(frame, height=10)
output_text.pack(fill='both', expand=True)

root.mainloop()
