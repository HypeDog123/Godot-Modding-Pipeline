import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import zipfile
import os
import shutil
import io
from datetime import datetime

# =====================================================================
# CONFIGURATION
# =====================================================================
XOR_KEY = 0x5A 

class ModernGodotTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Godot Engine Modding Pipeline Utility")
        self.root.geometry("650x540")
        self.root.resizable(False, False)
        
        # Color Palette
        self.bg_dark = "#121212"
        self.bg_panel = "#1e1e1e"
        self.bg_input = "#2d2d2d"
        self.fg_light = "#ffffff"
        self.fg_muted = "#aaaaaa"
        self.accent_green = "#2c8a4c"
        self.accent_green_hover = "#3eb364"
        self.accent_blue = "#2a6496"
        self.accent_blue_hover = "#3a7cbd"
        self.accent_gray = "#3c3c3c"
        self.accent_gray_hover = "#4a4a4a"

        self.root.configure(bg=self.bg_dark)

        # Style Configuration for Tabs
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TNotebook", background=self.bg_dark, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=self.bg_panel, foreground=self.fg_muted, padding=[15, 5], font=("Segoe UI", 10, "bold"))
        self.style.map("TNotebook.Tab", background=[("selected", self.bg_dark)], foreground=[("selected", self.fg_light)])

        # Header
        self.create_header()

        # Tabs Container
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=(10, 0))

        # Build Tabs
        self.tab_injector = tk.Frame(self.notebook, bg=self.bg_dark)
        self.tab_packer = tk.Frame(self.notebook, bg=self.bg_dark)

        self.notebook.add(self.tab_injector, text="  📥 PLAYER INJECTOR  ")
        self.notebook.add(self.tab_packer, text="  🛠️  DEVELOPER PACKER  ")

        self.build_injector_tab()
        self.build_packer_tab()
        self.create_footer()

    def create_header(self):
        header_frame = tk.Frame(self.root, bg=self.bg_panel, height=55)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)

        title_label = tk.Label(header_frame, text="⚙️  GODOT SOURCE PIPELINE", font=("Segoe UI", 11, "bold"), bg=self.bg_panel, fg=self.fg_light)
        title_label.pack(side="left", padx=20, pady=15)

        version_label = tk.Label(header_frame, text="v3.0 (Delta Engine)", font=("Segoe UI", 9, "italic"), bg=self.bg_panel, fg=self.fg_muted)
        version_label.pack(side="right", padx=20, pady=18)

    def create_footer(self):
        footer_frame = tk.Frame(self.root, bg=self.bg_panel, height=40)
        footer_frame.pack(fill="x", side="bottom")
        footer_frame.pack_propagate(False)

        btn_backup = tk.Button(footer_frame, text="📂 Open Workspace Directory", font=("Segoe UI", 9), bg=self.bg_panel, fg=self.fg_muted, activebackground=self.bg_input, activeforeground="white", relief="flat", bd=0, command=self.open_workspace)
        btn_backup.pack(side="left", fill="y", padx=15)
        self.bind_hover(btn_backup, self.bg_panel, self.bg_input)

    def bind_hover(self, button, normal_color, hover_color):
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=normal_color))

    # =====================================================================
    # TAB 1: INJECTOR UI
    # =====================================================================
    def build_injector_tab(self):
        frame = tk.Frame(self.tab_injector, bg=self.bg_dark)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Step 1
        tk.Label(frame, text="STEP 1: SELECT PROTECTED MOD (.GOMODPAK)", font=("Segoe UI", 8, "bold"), bg=self.bg_dark, fg=self.fg_muted).grid(row=0, column=0, sticky="w", pady=(10, 5))
        self.inj_mod_entry = tk.Entry(frame, width=52, font=("Segoe UI", 10), bg=self.bg_input, fg=self.fg_light, insertbackground="white", relief="flat", bd=6)
        self.inj_mod_entry.grid(row=1, column=0, sticky="we", ipady=2)
        btn_mod = tk.Button(frame, text="Browse", font=("Segoe UI", 9, "bold"), bg=self.accent_gray, fg=self.fg_light, relief="flat", padx=15, command=self.browse_inj_mod)
        btn_mod.grid(row=1, column=1, padx=(10, 0), sticky="ns")
        self.bind_hover(btn_mod, self.accent_gray, self.accent_gray_hover)

        # Step 2
        tk.Label(frame, text="STEP 2: SELECT TARGET GODOT SOURCE FOLDER", font=("Segoe UI", 8, "bold"), bg=self.bg_dark, fg=self.fg_muted).grid(row=2, column=0, sticky="w", pady=(25, 5))
        self.inj_src_entry = tk.Entry(frame, width=52, font=("Segoe UI", 10), bg=self.bg_input, fg=self.fg_light, insertbackground="white", relief="flat", bd=6)
        self.inj_src_entry.grid(row=3, column=0, sticky="we", ipady=2)
        btn_src = tk.Button(frame, text="Browse", font=("Segoe UI", 9, "bold"), bg=self.accent_gray, fg=self.fg_light, relief="flat", padx=15, command=self.browse_inj_src)
        btn_src.grid(row=3, column=1, padx=(10, 0), sticky="ns")
        self.bind_hover(btn_src, self.accent_gray, self.accent_gray_hover)

        # Action Action
        self.inject_btn = tk.Button(frame, text="INJECT MOD SYSTEM", font=("Segoe UI", 11, "bold"), bg=self.accent_green, fg=self.fg_light, activebackground=self.accent_green_hover, activeforeground="white", relief="flat", cursor="hand2", command=self.run_injector)
        self.inject_btn.grid(row=4, column=0, columnspan=2, pady=(50, 0), sticky="we", ipady=12)
        self.bind_hover(self.inject_btn, self.accent_green, self.accent_green_hover)

    # =====================================================================
    # TAB 2: PACKER UI (YOUR NEW DEV SYSTEM)
    # =====================================================================
    def build_packer_tab(self):
        frame = tk.Frame(self.tab_packer, bg=self.bg_dark)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Dev Step 1
        tk.Label(frame, text="STEP 1: SELECT FULL MODIFIED SOURCE ARCHIVE (.ZIP)", font=("Segoe UI", 8, "bold"), bg=self.bg_dark, fg=self.fg_muted).grid(row=0, column=0, sticky="w", pady=(10, 5))
        self.pck_zip_entry = tk.Entry(frame, width=52, font=("Segoe UI", 10), bg=self.bg_input, fg=self.fg_light, insertbackground="white", relief="flat", bd=6)
        self.pck_zip_entry.grid(row=1, column=0, sticky="we", ipady=2)
        btn_zip = tk.Button(frame, text="Browse", font=("Segoe UI", 9, "bold"), bg=self.accent_gray, fg=self.fg_light, relief="flat", padx=15, command=self.browse_pck_zip)
        btn_zip.grid(row=1, column=1, padx=(10, 0), sticky="ns")
        self.bind_hover(btn_zip, self.accent_gray, self.accent_gray_hover)

        # Dev Step 2
        tk.Label(frame, text="STEP 2: SELECT CLEAN/UNMODIFIED REPO FOLDER (FOR DELTA CHECK)", font=("Segoe UI", 8, "bold"), bg=self.bg_dark, fg=self.fg_muted).grid(row=2, column=0, sticky="w", pady=(25, 5))
        self.pck_clean_entry = tk.Entry(frame, width=52, font=("Segoe UI", 10), bg=self.bg_input, fg=self.fg_light, insertbackground="white", relief="flat", bd=6)
        self.pck_clean_entry.grid(row=3, column=0, sticky="we", ipady=2)
        btn_clean = tk.Button(frame, text="Browse", font=("Segoe UI", 9, "bold"), bg=self.accent_gray, fg=self.fg_light, relief="flat", padx=15, command=self.browse_pck_clean)
        btn_clean.grid(row=3, column=1, padx=(10, 0), sticky="ns")
        self.bind_hover(btn_clean, self.accent_gray, self.accent_gray_hover)

        # Dev Step 3
        tk.Label(frame, text="STEP 3: SAVE OUT TARGET MOD PATH (.GOMODPAK)", font=("Segoe UI", 8, "bold"), bg=self.bg_dark, fg=self.fg_muted).grid(row=4, column=0, sticky="w", pady=(25, 5))
        self.pck_out_entry = tk.Entry(frame, width=52, font=("Segoe UI", 10), bg=self.bg_input, fg=self.fg_light, insertbackground="white", relief="flat", bd=6)
        self.pck_out_entry.grid(row=5, column=0, sticky="we", ipady=2)
        btn_out = tk.Button(frame, text="Save As", font=("Segoe UI", 9, "bold"), bg=self.accent_gray, fg=self.fg_light, relief="flat", padx=15, command=self.browse_pck_out)
        btn_out.grid(row=5, column=1, padx=(10, 0), sticky="ns")
        self.bind_hover(btn_out, self.accent_gray, self.accent_gray_hover)

        # Pack Action
        self.pack_btn = tk.Button(frame, text="GENERATE DELTA .GOMODPAK", font=("Segoe UI", 11, "bold"), bg=self.accent_blue, fg=self.fg_light, activebackground=self.accent_blue_hover, activeforeground="white", relief="flat", cursor="hand2", command=self.run_packer)
        self.pack_btn.grid(row=6, column=0, columnspan=2, pady=(35, 0), sticky="we", ipady=12)
        self.bind_hover(self.pack_btn, self.accent_blue, self.accent_blue_hover)

    # --- BROWSE WRAPPERS ---
    def browse_inj_mod(self):
        p = filedialog.askopenfilename(filetypes=[("Godot Mod Pak", "*.gomodpak"), ("Zip files", "*.zip")])
        if p: self.inj_mod_entry.delete(0, tk.END); self.inj_mod_entry.insert(0, p)

    def browse_inj_src(self):
        p = filedialog.askdirectory()
        if p: self.inj_src_entry.delete(0, tk.END); self.inj_src_entry.insert(0, p)

    def browse_pck_zip(self):
        p = filedialog.askopenfilename(filetypes=[("ZIP Source Archive", "*.zip")])
        if p: self.pck_zip_entry.delete(0, tk.END); self.pck_zip_entry.insert(0, p)

    def browse_pck_clean(self):
        p = filedialog.askdirectory()
        if p: self.pck_clean_entry.delete(0, tk.END); self.pck_clean_entry.insert(0, p)

    def browse_pck_out(self):
        p = filedialog.asksaveasfilename(defaultextension=".gomodpak", filetypes=[("Godot Mod Pak", "*.gomodpak")])
        if p: self.pck_out_entry.delete(0, tk.END); self.pck_out_entry.insert(0, p)

    # =====================================================================
    # INJECTOR PROCESSING LOGIC
    # =====================================================================
    def run_injector(self):
        mod_path = self.inj_mod_entry.get()
        source_path = self.inj_src_entry.get()
        if not mod_path or not source_path:
            messagebox.showwarning("Incomplete", "Please complete all fields.")
            return

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = os.path.join(os.path.dirname(source_path), f"godot_source_backup_{timestamp}")
            shutil.copytree(source_path, backup_dir)

            with open(mod_path, 'rb') as f:
                scrambled_data = f.read()
            unscrambled_data = bytearray(b ^ XOR_KEY for b in scrambled_data)

            new_count, up_count, skip_count = 0, 0, 0

            with zipfile.ZipFile(io.BytesIO(unscrambled_data), 'r') as zip_ref:
                for file_info in zip_ref.infolist():
                    if file_info.is_dir(): continue
                    target_file_path = os.path.join(source_path, file_info.filename)
                    should_extract = False
                    
                    if not os.path.exists(target_file_path):
                        should_extract = True; new_count += 1
                    else:
                        if os.path.getsize(target_file_path) != file_info.file_size:
                            should_extract = True; up_count += 1
                        else:
                            local_dt = datetime.fromtimestamp(os.path.getmtime(target_file_path))
                            zip_dt = datetime(*file_info.date_time)
                            if zip_dt > local_dt:
                                should_extract = True; up_count += 1
                            else:
                                skip_count += 1

                    if should_extract:
                        zip_ref.extract(file_info, source_path)

            messagebox.showinfo("Success", f"Mod Injected Successfully!\n\n🆕 New: {new_count}\n🔄 Updated: {up_count}\n⏸️ Untouched: {skip_count}\n\nBackup folder generated.")
        except Exception as e:
            messagebox.showerror("Error", f"Execution failed: {str(e)}")

    # =====================================================================
    # THE CREATOR/PACKER LOGIC: GENERATE GOMODPAK FROM TWO SOURCES
    # =====================================================================
    def run_packer(self):
        modified_zip_path = self.pck_zip_entry.get()
        clean_folder_path = self.pck_clean_entry.get()
        output_pak_path = self.pck_out_entry.get()

        if not modified_zip_path or not clean_folder_path or not output_pak_path:
            messagebox.showwarning("Incomplete", "Please assign all fields inside Developer configurations.")
            return

        try:
            # Setup a dynamic byte buffer to build a normal zip archive entirely in RAM
            in_memory_zip = io.BytesIO()
            
            packed_files_count = 0

            # 1. Inspect your modified full code ZIP file
            with zipfile.ZipFile(modified_zip_path, 'r') as mod_zip:
                with zipfile.ZipFile(in_memory_zip, 'w', zipfile.ZIP_DEFLATED) as export_zip:
                    
                    for file_info in mod_zip.infolist():
                        if file_info.is_dir(): continue
                        
                        # Find the matching file in the clean project directory
                        clean_file_path = os.path.join(clean_folder_path, file_info.filename)
                        
                        include_in_pak = False
                        
                        if not os.path.exists(clean_file_path):
                            # It is a brand new custom script or asset!
                            include_in_pak = True
                        else:
                            # It exists in clean base; compare size to see if it changed
                            if os.path.getsize(clean_file_path) != file_info.file_size:
                                include_in_pak = True
                            else:
                                # Compare file contents or modified times if sizes match
                                with open(clean_file_path, 'rb') as cf:
                                    clean_bytes = cf.read()
                                modified_bytes = mod_zip.read(file_info.filename)
                                
                                if clean_bytes != modified_bytes:
                                    include_in_pak = True
                        
                        # 2. If it is verified altered or new code, save it to our extraction cache
                        if include_in_pak:
                            file_data = mod_zip.read(file_info.filename)
                            export_zip.writestr(file_info, file_data)
                            packed_files_count += 1

            # 3. Read the clean raw compiled ZIP, drop the XOR encryption mask, and write it
            in_memory_zip.seek(0)
            raw_zip_data = in_memory_zip.read()
            
            if packed_files_count == 0:
                messagebox.showwarning("No Changes", "Delta test complete: Your modified ZIP is identical to the clean folder. No modified files found.")
                return

            scrambled_pak_data = bytearray(b ^ XOR_KEY for b in raw_zip_data)
            
            with open(output_pak_path, 'wb') as out_f:
                out_f.write(scrambled_pak_data)

            messagebox.showinfo("Success", f"Protected Pack Created Successfully!\n\n📦 Extracted and Packed: {packed_files_count} files.\n\nAll untouched files skipped. File is protected from extraction!")
            
        except Exception as e:
            messagebox.showerror("Packer Error", f"Failed to calculate system changes:\n{str(e)}")

    def open_workspace(self):
        p = os.path.dirname(self.inj_src_entry.get()) if self.inj_src_entry.get() else os.getcwd()
        if os.path.exists(p): os.startfile(p)


if __name__ == "__main__":
    window = tk.Tk()
    app = ModernGodotTool(window)
    window.mainloop()
