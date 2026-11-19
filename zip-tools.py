import os
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox

class SimpleZipApp:
    def __init__(self, root):
        self.root = root
        self.root.title("超シンプル圧縮・解凍ツール")
        self.root.geometry("420x250")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")

        title = tk.Label(
            root, text="ZIP 圧縮・解凍ソフト",
            font=("Meiryo", 14, "bold"), bg="#f5f5f5", fg="#333333"
        )
        title.pack(pady=(18, 12))

        btn_frame = tk.Frame(root, bg="#f5f5f5")
        btn_frame.pack(pady=5)

        btn_style = {
            "font": ("Meiryo", 11, "bold"),
            "width": 26,
            "height": 2,
            "bd": 0,
            "cursor": "hand2"
        }

        tk.Button(
            btn_frame, text="ファイルを圧縮する (.zip作成)",
            bg="#2b7de9", fg="white", command=self.compress_files, **btn_style
        ).pack(pady=5)

        tk.Button(
            btn_frame, text="フォルダを圧縮する (.zip作成)",
            bg="#34a853", fg="white", command=self.compress_folder, **btn_style
        ).pack(pady=5)

        tk.Button(
            btn_frame, text="ZIPファイルを解凍する",
            bg="#ea4335", fg="white", command=self.extract_zip, **btn_style
        ).pack(pady=5)

    def compress_files(self):
        files = filedialog.askopenfilenames(title="圧縮するファイルを選択（複数可）")
        if not files:
            return
        save_path = filedialog.asksaveasfilename(
            title="保存先のZIPファイル名",
            defaultextension=".zip",
            filetypes=[("ZIPファイル", "*.zip")]
        )
        if not save_path:
            return
        try:
            with zipfile.ZipFile(save_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for f in files:
                    zf.write(f, os.path.basename(f))
            messagebox.showinfo("完了", f"圧縮が完了しました！\n{save_path}")
        except Exception as e:
            messagebox.showerror("エラー", f"圧縮に失敗しました:\n{e}")

    def compress_folder(self):
        folder = filedialog.askdirectory(title="圧縮するフォルダを選択")
        if not folder:
            return
        save_path = filedialog.asksaveasfilename(
            title="保存先のZIPファイル名",
            initialfile=os.path.basename(folder) + ".zip",
            defaultextension=".zip",
            filetypes=[("ZIPファイル", "*.zip")]
        )
        if not save_path:
            return
        try:
            base_dir = os.path.dirname(folder)
            with zipfile.ZipFile(save_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for root_dir, _, filenames in os.walk(folder):
                    for filename in filenames:
                        full_path = os.path.join(root_dir, filename)
                        rel_path = os.path.relpath(full_path, base_dir)
                        zf.write(full_path, rel_path)
            messagebox.showinfo("完了", f"フォルダの圧縮が完了しました！\n{save_path}")
        except Exception as e:
            messagebox.showerror("エラー", f"圧縮に失敗しました:\n{e}")

    def extract_zip(self):
        zip_path = filedialog.askopenfilename(
            title="解凍するZIPファイルを選択",
            filetypes=[("ZIPファイル", "*.zip")]
        )
        if not zip_path:
            return
        dest_dir = filedialog.askdirectory(title="解凍先のフォルダを選択")
        if not dest_dir:
            return
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                for info in zf.infolist():
                    # 日本語ファイル名の文字化け対策
                    if not (info.flag_bits & 0x800):
                        try:
                            info.filename = info.filename.encode('cp437').decode('cp932')
                        except Exception:
                            pass
                    zf.extract(info, dest_dir)
            messagebox.showinfo("完了", f"解凍が完了しました！\n{dest_dir}")
        except Exception as e:
            messagebox.showerror("エラー", f"解凍に失敗しました:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleZipApp(root)
    root.mainloop()
