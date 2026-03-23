import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile
import os
import shutil
from datetime import datetime

class GodotSourceInjector:
    def __init__(self, root):
        self.root = root
        self.root.title("Godot .gomodpak Source Injector")
        self.root.geometry("550x450")
        self.root.configure(bg="#1e1e1e")

        # Custom Styles
        label_cfg = {"bg": "#1e1e1e", "fg": "#e0e0e0", "font": ("Segoe UI", 10)}
        entry_cfg = {"bg": "#2d2d2d", "fg": "white", "insertbackground": "white", "relief": "flat"}
        btn_cfg = {"bg": "#3c3c3c", "fg": "white", "activebackground": "#505050", "relief": "flat", "padx": 10}

        # --- Mod Selection ---
        tk.Label(root, text="Step 1: Select Mod (.gomodpak)", **label_cfg).pack(pady=(20, 5))
        self.mod_entry = tk.Entry(root, width=60, **entry_cfg)
        self.mod_entry.pack(pady=5)
        tk.Button(root, text="Browse Mod File", command=self.browse_mod, **btn_cfg).pack()

        # --- Source Selection ---
        tk.Label(root, text="Step 2: Select Godot Source Folder", **label_cfg).pack(pady=(20, 5))
        self.src_entry = tk.Entry(root, width=60, **entry_cfg)
        self.src_entry.pack(pady=5)
        tk.Button(root, text="Browse Source Folder", command=self.browse_src, **btn_cfg).pack()

        # --- Action Buttons ---
        self.inject_btn = tk.Button(root, text="INJECT MOD", bg="#2c8a4c", fg="white", 
                                    font=("Segoe UI", 12, "bold"), command=self.inject, 
                                    width=25, height=2, activebackground="#3eb364")
        self.inject_btn.pack(pady=40)
        
        tk.Button(root, text="View Backups", command=self.open_backup_folder, **btn_cfg).pack()

    def browse_mod(self):
        path = filedialog.askopenfilename(filetypes=[("Godot Mod Pak", "*.gomodpak"), ("Zip files", "*.zip")])
        if path:
            self.mod_entry.delete(0, tk.END)
            self.mod_entry.insert(0, path)

    def browse_src(self):
        path = filedialog.askdirectory()
        if path:
            self.src_entry.delete(0, tk.END)
            self.src_entry.insert(0, path)

    def inject(self):
        mod_path = self.mod_entry.get()
        source_path = self.src_entry.get()

        if not mod_path or not source_path:
            messagebox.showwarning("Incomplete", "Please select both the mod file and the source folder.")
            return

        try:
            # 1. Create a Backup
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = os.path.join(os.path.dirname(source_path), f"godot_source_backup_{timestamp}")
            shutil.copytree(source_path, backup_dir)

            # 2. Extract and Swap
            # zipfile treats .gomodpak exactly like .zip
            with zipfile.ZipFile(mod_path, 'r') as zip_ref:
                # This extracts and overwrites existing files in the source_path
                zip_ref.extractall(source_path)

            messagebox.showinfo("Success", f"Mod Injected!\n\nBackup created at:\n{backup_dir}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to inject mod: {str(e)}")

    def open_backup_folder(self):
        path = os.path.dirname(self.src_entry.get()) if self.src_entry.get() else os.getcwd()
        os.startfile(path)

if __name__ == "__main__":
    window = tk.Tk()
    app = GodotSourceInjector(window)
    window.mainloop()
