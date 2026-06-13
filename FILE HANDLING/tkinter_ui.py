import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from pathlib import Path
import os

# ── Theme colours ─────────────────────────────────────────────────────────────
BG       = "#0f1117"
PANEL    = "#1e2a3a"
ACCENT   = "#00d4ff"
FG       = "#e0e0e0"
FG_DIM   = "#a0c4d8"
SUCCESS  = "#00ff88"
DANGER   = "#ff4444"
FONT     = ("Courier New", 11)
FONT_SM  = ("Courier New", 9)
FONT_LG  = ("Courier New", 14, "bold")


# ── Helpers ───────────────────────────────────────────────────────────────────

def list_items():
    return list(Path('').rglob('*'))


def refresh_tree(tree):
    tree.delete(*tree.get_children())
    for i, item in enumerate(list_items(), 1):
        tag = "folder" if item.is_dir() else "file"
        tree.insert("", "end", values=(i, str(item)), tags=(tag,))


def status(label, msg, colour=SUCCESS):
    label.config(text=msg, fg=colour)


# ── Window setup ──────────────────────────────────────────────────────────────

root = tk.Tk()
root.title("🗂  File Manager  –  CRUD Operations")
root.configure(bg=BG)
root.geometry("900x620")
root.resizable(True, True)

# ── Layout: left panel (ops) + right panel (tree) ─────────────────────────────
pane = tk.PanedWindow(root, orient=tk.HORIZONTAL, bg=BG, sashwidth=4, sashrelief=tk.FLAT)
pane.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

left  = tk.Frame(pane, bg=BG)
right = tk.Frame(pane, bg=BG)
pane.add(left,  minsize=420)
pane.add(right, minsize=260)

# ── Title ─────────────────────────────────────────────────────────────────────
tk.Label(left, text="🗂  File Manager", font=("Courier New", 16, "bold"),
         bg=BG, fg=ACCENT).pack(pady=(6, 2))
tk.Label(left, text="CRUD Operations · Files & Folders", font=FONT_SM,
         bg=BG, fg=FG_DIM).pack(pady=(0, 8))

# ── Notebook (tabs for each operation) ───────────────────────────────────────
style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook",          background=BG,    borderwidth=0)
style.configure("TNotebook.Tab",      background=PANEL, foreground=FG_DIM,
                font=FONT_SM,         padding=(10, 4))
style.map("TNotebook.Tab",
          background=[("selected", ACCENT)],
          foreground=[("selected", BG)])
style.configure("TFrame",             background=BG)

nb = ttk.Notebook(left)
nb.pack(fill=tk.BOTH, expand=True, padx=4)

status_label = tk.Label(left, text="", font=FONT_SM, bg=BG, fg=SUCCESS, wraplength=400)
status_label.pack(pady=6)


def make_tab(parent, title):
    frame = ttk.Frame(parent)
    parent.add(frame, text=title)
    return frame


def lbl(parent, text):
    return tk.Label(parent, text=text, bg=BG, fg=FG_DIM, font=FONT_SM, anchor="w")


def entry(parent):
    e = tk.Entry(parent, bg=PANEL, fg=FG, insertbackground=ACCENT,
                 font=FONT, relief=tk.FLAT, bd=4)
    return e


def btn(parent, text, cmd, danger=False):
    colour = DANGER if danger else ACCENT
    b = tk.Button(parent, text=text, command=cmd,
                  bg=PANEL, fg=colour, activebackground=colour,
                  activeforeground=BG, font=FONT, relief=tk.FLAT,
                  bd=0, padx=12, pady=6, cursor="hand2")
    return b


# ── Tab helpers ───────────────────────────────────────────────────────────────

def pad_frame(tab):
    f = tk.Frame(tab, bg=BG)
    f.pack(fill=tk.BOTH, expand=True, padx=16, pady=12)
    return f


# ── 1. Create File ────────────────────────────────────────────────────────────
t1 = make_tab(nb, "📄 Create")
f1 = pad_frame(t1)
lbl(f1, "File name:").pack(fill=tk.X)
e1_name = entry(f1); e1_name.pack(fill=tk.X, pady=(2, 8))
lbl(f1, "Content:").pack(fill=tk.X)
e1_content = scrolledtext.ScrolledText(f1, height=6, bg=PANEL, fg=FG,
                                        insertbackground=ACCENT, font=FONT,
                                        relief=tk.FLAT, bd=4)
e1_content.pack(fill=tk.X, pady=(2, 10))

def do_create():
    name = e1_name.get().strip()
    if not name:
        status(status_label, "⚠ Enter a file name.", DANGER); return
    p = Path(name)
    if p.exists():
        status(status_label, "⚠ File already exists!", DANGER); return
    try:
        p.write_text(e1_content.get("1.0", tk.END).rstrip("\n"))
        status(status_label, f"✅ '{name}' created!", SUCCESS)
        refresh_tree(tree)
    except Exception as e:
        status(status_label, f"❌ {e}", DANGER)

btn(f1, "Create File", do_create).pack(pady=4)


# ── 2. Read File ──────────────────────────────────────────────────────────────
t2 = make_tab(nb, "📖 Read")
f2 = pad_frame(t2)
lbl(f2, "File name:").pack(fill=tk.X)
e2_name = entry(f2); e2_name.pack(fill=tk.X, pady=(2, 8))
out2 = scrolledtext.ScrolledText(f2, height=8, bg=PANEL, fg=ACCENT,
                                  font=FONT, relief=tk.FLAT, bd=4, state=tk.DISABLED)
out2.pack(fill=tk.X, pady=(0, 8))

def do_read():
    name = e2_name.get().strip()
    if not name:
        status(status_label, "⚠ Enter a file name.", DANGER); return
    p = Path(name)
    if not p.exists():
        status(status_label, "⚠ File not found!", DANGER); return
    try:
        text = p.read_text()
        out2.config(state=tk.NORMAL)
        out2.delete("1.0", tk.END)
        out2.insert(tk.END, text)
        out2.config(state=tk.DISABLED)
        status(status_label, f"📖 Reading '{name}'", ACCENT)
    except Exception as e:
        status(status_label, f"❌ {e}", DANGER)

btn(f2, "Read File", do_read).pack(pady=4)


# ── 3. Update File ────────────────────────────────────────────────────────────
t3 = make_tab(nb, "✏️ Update")
f3 = pad_frame(t3)
lbl(f3, "File name:").pack(fill=tk.X)
e3_name = entry(f3); e3_name.pack(fill=tk.X, pady=(2, 8))
lbl(f3, "New content:").pack(fill=tk.X)
e3_content = scrolledtext.ScrolledText(f3, height=5, bg=PANEL, fg=FG,
                                        insertbackground=ACCENT, font=FONT,
                                        relief=tk.FLAT, bd=4)
e3_content.pack(fill=tk.X, pady=(2, 8))
update_mode = tk.StringVar(value="overwrite")
fr_radio = tk.Frame(f3, bg=BG)
fr_radio.pack(fill=tk.X, pady=(0, 8))
for val, txt in [("overwrite", "Overwrite"), ("append", "Append")]:
    tk.Radiobutton(fr_radio, text=txt, variable=update_mode, value=val,
                   bg=BG, fg=FG, selectcolor=PANEL, activebackground=BG,
                   activeforeground=ACCENT, font=FONT).pack(side=tk.LEFT, padx=8)

def do_update():
    name = e3_name.get().strip()
    if not name:
        status(status_label, "⚠ Enter a file name.", DANGER); return
    p = Path(name)
    if not p.exists():
        status(status_label, "⚠ File not found!", DANGER); return
    try:
        flag = 'w' if update_mode.get() == "overwrite" else 'a'
        with open(name, flag) as f:
            f.write(e3_content.get("1.0", tk.END).rstrip("\n"))
        status(status_label, f"✅ '{name}' updated!", SUCCESS)
    except Exception as e:
        status(status_label, f"❌ {e}", DANGER)

btn(f3, "Update File", do_update).pack(pady=4)


# ── 4. Delete File ────────────────────────────────────────────────────────────
t4 = make_tab(nb, "🗑️ Del File")
f4 = pad_frame(t4)
lbl(f4, "File name:").pack(fill=tk.X)
e4_name = entry(f4); e4_name.pack(fill=tk.X, pady=(2, 12))

def do_delete_file():
    name = e4_name.get().strip()
    if not name:
        status(status_label, "⚠ Enter a file name.", DANGER); return
    p = Path(name)
    if not p.exists():
        status(status_label, "⚠ File not found!", DANGER); return
    if messagebox.askyesno("Confirm", f"Delete '{name}'?"):
        try:
            os.remove(p)
            status(status_label, f"🗑 '{name}' deleted.", SUCCESS)
            refresh_tree(tree)
        except Exception as e:
            status(status_label, f"❌ {e}", DANGER)

btn(f4, "Delete File", do_delete_file, danger=True).pack(pady=4)


# ── 5. Rename File ────────────────────────────────────────────────────────────
t5 = make_tab(nb, "🔄 Rename")
f5 = pad_frame(t5)
lbl(f5, "Current name:").pack(fill=tk.X)
e5_old = entry(f5); e5_old.pack(fill=tk.X, pady=(2, 8))
lbl(f5, "New name:").pack(fill=tk.X)
e5_new = entry(f5); e5_new.pack(fill=tk.X, pady=(2, 12))

def do_rename():
    old = e5_old.get().strip(); new = e5_new.get().strip()
    if not old or not new:
        status(status_label, "⚠ Fill in both fields.", DANGER); return
    p = Path(old)
    if not p.exists():
        status(status_label, "⚠ File not found!", DANGER); return
    try:
        p.rename(new)
        status(status_label, f"✅ Renamed to '{new}'!", SUCCESS)
        refresh_tree(tree)
    except Exception as e:
        status(status_label, f"❌ {e}", DANGER)

btn(f5, "Rename File", do_rename).pack(pady=4)


# ── 6. Create Folder ──────────────────────────────────────────────────────────
t6 = make_tab(nb, "📁 New Folder")
f6 = pad_frame(t6)
lbl(f6, "Folder name:").pack(fill=tk.X)
e6_name = entry(f6); e6_name.pack(fill=tk.X, pady=(2, 12))

def do_create_folder():
    name = e6_name.get().strip()
    if not name:
        status(status_label, "⚠ Enter a folder name.", DANGER); return
    p = Path(name)
    if p.exists():
        status(status_label, "⚠ Folder already exists!", DANGER); return
    try:
        p.mkdir(parents=True)
        status(status_label, f"✅ Folder '{name}' created!", SUCCESS)
        refresh_tree(tree)
    except Exception as e:
        status(status_label, f"❌ {e}", DANGER)

btn(f6, "Create Folder", do_create_folder).pack(pady=4)


# ── 7. Delete Folder ──────────────────────────────────────────────────────────
t7 = make_tab(nb, "🗑️ Del Folder")
f7 = pad_frame(t7)
lbl(f7, "Folder name:").pack(fill=tk.X)
e7_name = entry(f7); e7_name.pack(fill=tk.X, pady=(2, 12))

def do_delete_folder():
    name = e7_name.get().strip()
    if not name:
        status(status_label, "⚠ Enter a folder name.", DANGER); return
    p = Path(name)
    if not p.exists():
        status(status_label, "⚠ Folder not found!", DANGER); return
    if messagebox.askyesno("Confirm", f"Delete folder '{name}'?"):
        try:
            p.rmdir()
            status(status_label, f"🗑 Folder '{name}' deleted.", SUCCESS)
            refresh_tree(tree)
        except OSError:
            status(status_label, "⚠ Folder not empty!", DANGER)
        except Exception as e:
            status(status_label, f"❌ {e}", DANGER)

btn(f7, "Delete Folder", do_delete_folder, danger=True).pack(pady=4)


# ── Right panel: directory tree ───────────────────────────────────────────────
tk.Label(right, text="📂 Directory", font=FONT_LG,
         bg=BG, fg=ACCENT).pack(pady=(6, 4))

style.configure("Treeview",
                background=PANEL, foreground=FG,
                fieldbackground=PANEL, font=FONT_SM,
                rowheight=22, borderwidth=0)
style.configure("Treeview.Heading",
                background=PANEL, foreground=ACCENT,
                font=("Courier New", 9, "bold"))
style.map("Treeview", background=[("selected", ACCENT)],
          foreground=[("selected", BG)])

cols = ("#", "Path")
tree = ttk.Treeview(right, columns=cols, show="headings", selectmode="browse")
tree.heading("#",    text="#");    tree.column("#",    width=36, anchor="center")
tree.heading("Path", text="Path"); tree.column("Path", width=220, anchor="w")
tree.tag_configure("folder", foreground="#ffd700")
tree.tag_configure("file",   foreground=FG_DIM)

sb = ttk.Scrollbar(right, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=sb.set)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(4, 0), pady=4)
sb.pack(side=tk.LEFT, fill=tk.Y, pady=4)

refresh_btn = tk.Button(right, text="⟳ Refresh", command=lambda: refresh_tree(tree),
                        bg=PANEL, fg=ACCENT, activebackground=ACCENT,
                        activeforeground=BG, font=FONT_SM, relief=tk.FLAT,
                        bd=0, padx=8, pady=4, cursor="hand2")
refresh_btn.pack(pady=(0, 6))

refresh_tree(tree)

# ── Double-click tree row → fill active tab's first entry ─────────────────────
entry_map = {0: e1_name, 1: e2_name, 2: e3_name, 3: e4_name, 4: e5_old, 6: e7_name}

def on_tree_select(event):
    sel = tree.selection()
    if not sel:
        return
    path = tree.item(sel[0])["values"][1]
    tab_idx = nb.index(nb.select())
    target = entry_map.get(tab_idx)
    if target:
        target.delete(0, tk.END)
        target.insert(0, path)

tree.bind("<<TreeviewSelect>>", on_tree_select)

root.mainloop()