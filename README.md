# Godot Engine Modding Pipeline Utility

Welcome to the official documentation for the **Godot Source Pipeline**. This utility bridges the gap between raw reverse-engineering frameworks and consumer-safe distribution. It features a dual-mode interface designed to make mod deployment seamless for players and asset compilation secure for developers using a **Smart Delta Comparison Engine**, **Regex Code Minification**, and **Symmetric XOR Archive Encryption**.

---

## 📋 Essential Prerequisites (For Both Users & Developers)

Before utilizing this pipeline, both players and developers must download and set up the following free tools. 

> 🟥 **THE GOLDEN ENGINE RULE:** > You **must** download the exact version of the Godot Editor that the target game was originally built with (e.g., Godot 4.2). Do not open an older game project inside a newer Godot version (e.g., using Godot 4.7 to edit a 4.2 game). A newer editor will silently force a project conversion, altering syntax and internal metadata, which completely breaks the delta-packer and causes the compiled game to **instantly crash on launch**.

### 1. ⚙️ Godot Engine Editor (Version-Matched)
* **Who needs it:** Both Users and Developers.
* **Why it's required:** Developers use it to edit the game source and build the mod. Users/Players must use it at the end of the installation process to re-compile the source code back into a playable game executable.
* **Where to get it:** Download the standalone, portable executable matching your game directly from the [Official Godot Engine Download Archive](https://godotengine.org/download/archive/).

### 2. 🔍 GDRE Tools (gdsdecomp)
* **Who needs it:** Both Users and Developers.
* **Why it's required:** This software decompiles and recovers the original, human-readable project code from the compiled game's production files. Both parties need it to extract a clean baseline of the game source onto their computers.
* **Where to get it:** [GDRE Tools GitHub Repository](https://github.com/bruvzg/gdsdecomp)

---

## 🏗️ The End-to-End Modding Lifecycle

A typical Godot modding pipeline flows through three major phases:

1. **Extraction (GDRE Tools):** The developer uses a decompression utility like **GDRE Tools** (`gdsdecomp`) to extract a compiled game's `.pck` or `.exe` binary structure back into an uncompiled, human-readable Godot project directory.
2. **Modification (Godot Editor):** The developer imports that extracted directory into the official **Godot Engine Editor**. They test modifications, add assets, and write custom code natively inside a fully functional workspace.
3. **Distribution (This Tool):** To prevent distributing the full game (which creates massive file sizes and facilitates software piracy), the developer uses this utility to isolate *only* the new or modified files, encrypting them into a lightweight `.gomodpak`.

---

## 📥 Player Guide: Full Modding & Compiling Tutorial

Because this tool injects modifications directly into the raw source files of a game, players must follow a three-phase workflow: **Extract** the original game, **Inject** the mod files, and **Compile** the final playable version using the official Godot Engine editor.

---

### 📋 Phase 1: Extracting the Base Game Source
Before running the injector, you need to turn the game's compiled executable into a moddable source folder:

1. Open your downloaded copy of **GDRE Tools**.
2. Select **Select Key/PCK/EXE to Decompile** and open the game's main `.exe` or `.pck` file.
3. Choose a destination folder on your computer and click **Extract/Recover Project**.
4. Once completed, you will have a folder containing the uncompiled source code of the game. **This folder will be your target workspace.**

---

### 🛠️ Phase 2: Injecting the Mod

> ⚠️ **Crucial Requirement:** Ensure your Godot Editor is **completely closed** before executing an injection. The tool automatically clones a complete backup directory (`godot_source_backup_[TIMESTAMP]`) right next to your project folder before altering any data.

1. **Launch the Utility:** Run the script or executable. By default, it opens to the **Player Injector** tab.
2. **Select the Mod File (Step 1):** Click **Browse** next to Step 1 and select the target `.gomodpak` file.
3. **Select the Game Folder (Step 2):** Click **Browse** next to Step 2 and choose the root folder of the uncompiled/decompiled Godot game source you generated in Phase 1.
4. **Inject:** Click the large green **INJECT MOD SYSTEM** button.

---

### 🚀 Phase 3: Compiling Your Game Natively in Godot

Now that the modded files have been injected into the game source, you need to use the free, official Godot Engine editor to compile it back into a playable game executable.

#### Step 1: Import the Project
1. Open the standalone, **version-matched Godot Engine executable** that you downloaded in the Prerequisites section. 
2. In the Godot Project Manager, click the **Import** button on the right-hand side.
3. Click **Browse**, navigate into the decompiled/modded game folder from Phase 1, select the `project.godot` file, and click **Open**.
4. Click **Import & Edit**. Godot will open the full workspace and automatically scan your new modded scripts.

#### Step 2: Configure the Export Template
1. In the top-left menu bar of Godot, go to **Project** -> **Export...**
2. In the Export window, click the **Add...** button at the top and choose your platform target (e.g., **Windows Desktop**, **Mac OSX**, or **Linux/X11**).
3. If you see a red warning at the bottom saying *"Export templates missing"*, click the **Manage Export Templates** link right next to it, download the official engine templates, and return to the Export window.

#### Step 3: Compile and Play
1. At the bottom of the Export window, click **Export Project...**
2. Uncheck **Export With Debug** (unless you intend to run real-time error logging).
3. Select a target folder where you want your final modded game to live, name your executable (e.g., `ModdedGame.exe`), and click **Save**.
4. Godot will package your modded source code and custom assets back into a fully optimized distribution build. 

Open your newly generated folder and run your custom game!

---

## 🛠️ Developer Guide: Complete Engineering Workflow

This section outlines how to use reverse-engineering software to obtain the raw source code, implement features safely, and securely pack the final distribution delta file.

### 📋 Phase 1: Acquiring the Raw Source via GDRE
Before editing anything, you must acquire a full, readable copy of the target game files to interact with:
1. Boot up **GDRE Tools**.
2. Click **Select Key/PCK/EXE to Decompile** and target the game's production `.pck` or `.exe` binary.
3. Choose a dedicated workspace location and trigger **Extract/Recover Project**.
4. **CRITICAL STEP:** Duplicate this folder immediately. Keep one copy perfectly clean as your **Unmodified Baseline Folder**. Use the other copy as your active development workspace.

### 💻 Phase 2: Modifying Source inside Godot Engine
You must use the official Godot Editor to build your mod cleanly without breaking backward-compatibility references:

> 🟥 **CRITICAL PIPELINE RULE:** > Do not use a newer version of Godot to edit your mod workspace. If Godot forces you to run a "Project Upgrade/Conversion," close the editor immediately. Launch the standalone, version-matched Godot executable instead. Forced upgrades change background scene IDs and configuration schemas, which causes the **Developer Packer** to output a bloated file containing false-positive engine modifications, breaking the final mod entirely.

1. Fire up the portable, version-matched **Godot Engine Editor**.
2. Click **Import**, locate the `project.godot` file inside your development workspace folder, and open it.
3. Implement your game logic, alter nodes, rewrite mechanics, or drop new variables into scripts natively. This system fully supports deeply nested folders (3+ folders deep, e.g., `\assets\scripts\entities\enemies\new_ai.gd`).
4. Test and debug your changes thoroughly in-editor. When complete, close the Godot Editor.

### 📦 Phase 3: Automated Delta Packaging Pipeline
Now compress and obfuscate your custom creations into an anti-pirate format using this utility:
1. Navigate to your modified development folder on your hard drive. Compress the **entire modified project folder** into a standard `.zip` archive.
2. Fire up this pipeline utility and switch over to the **DEVELOPER PACKER** tab.
3. **Load Your Modified Code (Step 1):** Click **Browse** and select the `.zip` archive of your full modified development folder.
4. **Load the Clean Baseline (Step 2):** Click **Browse** and select the **clean/unmodified baseline game folder** you saved from Phase 1. This acts as the anchor for the system to run cross-checks.
5. **Set Output Destination (Step 3):** Click **Save As** and name your release target (e.g., `release_v1.gomodpak`).
6. **Generate:** Hit the blue **GENERATE MINIFIED .GOMODPAK** button.

---

## 🔒 Automated Anti-Piracy & Protection Layers

When you click generate, the tool runs your files through three distinct operational defenses to protect your work and the original game assets:

### 1. Smart Delta Separation (Anti-Piracy)
If a game contains 10,000 core files and your mod only edits 5 scripts, the tool calculates the precise delta difference. It completely drops the 9,995 identical files. A user trying to unzip your mod will *never* get a complete, compilable copy of the base game. Deleted files from the modded workspace are simply bypassed, leaving original game files cleanly intact.

### 2. Regular Expression Source Minification
Before compressing your scripts, the tool passes all `.gd` (GDScript) and `.cs` (C#) files through an automated `re` parsing engine. 
* It uses regular expressions to rip out single-line comments (`#` and `//`), structural developer block notes (`/* ... */`), and extraneous formatting whitespaces.
* This leaves an abstracted, dense code layout that runs natively in Godot but strips out your private programming documentation, making manual reverse-engineering highly frustrating.

### 3. Symmetric XOR Binary Scrambling
The final output is wrapped in a symmetric XOR bit-flipper using a custom hardware mask. 
* If a malicious user attempts to drag and drop your `.gomodpak` back into extraction software like **GDRE Tools**, or standard archive managers like WinRAR or 7-Zip, the utility will fail to read the file headers and throw a fatal **"File is corrupted or invalid format"** exception.
* **Zero Disk Footprint:** When a legitimate player runs the injector, the payload is decrypted directly into the system's volatile RAM (`io.BytesIO`). The unencrypted zip structure is never written to the local storage drive, preventing runtime scraping.

# 🛠️ Troubleshoot

### 🚨 The "Inside-Out" Zip Rule (Fixes Blank .gomodpak Files)
When compressing your modified project files for the **Developer Packer**, **do not zip the outer root folder itself.** Zipping the folder adds an extra directory layer that breaks the utility's file-path comparison, causing it to generate an empty mod file.

* **❌ WRONG:** `modded.zip` ➡️ `modded_folder/` ➡️ `project.godot`
* **✅ CORRECT:** `modded.zip` ➡️ `project.godot`, `scenes/`, `assets/`

**How to package properly:**
1. Open your active `modded` workspace folder in File Explorer.
2. Select all files and folders *inside* this directory (`Ctrl + A`).
3. Right-click any highlighted file and choose **Compress to ZIP file** (or use 7-Zip/WinRAR). 

---

### 🔓 Fixing "Ghost Saves" (Windows Read-Only Lock)
If your source files came from a web repository (like GitHub), Windows often locks them. This prevents the Godot Editor from writing changes to your hard drive, even though your new nodes appear perfectly live in the editor.

#### 🔴 Symptoms:
* Your modifications (like a new `Label` node) show up perfectly inside the Godot Editor.
* When you open the corresponding `.tscn` file in a text editor like Notepad++, your modifications are completely missing.

#### 🛠️ The Fix:
1. **Close the Godot Editor completely** to release file handles.
2. Right-click your main `modded` source folder and select **Properties**.
3. Under the *General* tab, look at the **Attributes** section at the bottom.
4. Click the checkbox next to **Read-only** until the box is completely **empty/blank** (no checkmark, no solid square).
5. Click **Apply**, choose **"Apply changes to this folder, subfolders, and files"**, and click **OK**.
6. Open your workspace folder and delete the hidden **`.godot`** (or **`.import`** for Godot 3) cache directory.
7. Re-open Godot, make a minor tweak to force a rewrite, and click **Scene -> Save All Scenes**.

---

### 🔍 Quick Pipeline Verification
Before running the injector, right-click your generated `.gomodpak` file and open it in **Notepad++**. Press `Ctrl + F` and search for your modified node (e.g., `"Label"`). 

If the file is completely scrambled but contains your node text, your pipeline worked perfectly! If it cannot find your text, re-verify **The "Inside-Out" Zip Rule** above.
