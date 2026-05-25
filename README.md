# 🎨 AI Watermark & Metadata Remover (GUI)

This GUI application is a visual, user-friendly wrapper built on top of the incredible [noai-watermark](https://github.com/mertizci/noai-watermark) library. 

**What does this GUI do?** 
Instead of forcing you to use complex command-line scripts to clean your images, this tool provides a simple, native Windows interface. It allows you to:
1. Select a folder of images with a single click.
2. Automatically scan and detect which images contain hidden AI watermarks or invisible C2PA metadata tracking.
3. Visually preview the specific metadata found in each image.
4. Clean the entire folder using advanced GPU-accelerated diffusion model regeneration, fully stripping all AI fingerprints while preserving image quality.

![GUI Screenshot](gui_screenshot.png)

## 🌟 Acknowledgements & A Touch of Irony

First and foremost, massive praise goes to **[mertizci](https://github.com/mertizci)**, the original creator of the underlying `noai-watermark` library. This project operates entirely as a frontend dependent on their library. The heavy lifting—the diffusion model regeneration attacks, the CUDA optimizations, and the metadata stripping—is all thanks to their brilliant work!

**The Irony:** It is not lost on us that this GUI was built through a pair-programming session between a human developer and an AI assistant. Together, an AI and a human collaborated to build a tool designed specifically to remove AI watermarks! A beautiful paradox. 🤖🤝👨‍💻

## 💻 Prerequisites

Before running this application, your system must have:
* **Windows 10/11** (for the automated installer)
* **Python 3.10 or higher**: You can download this from [python.org](https://www.python.org/downloads/). 
  > **CRITICAL:** When installing Python, you **must** check the box that says "Add Python to PATH" on the very first installation screen.

## 🚀 Installation & Usage

There are two ways to install and run this application depending on your preference:

### Method 1: The One-Click Windows Installer (Recommended)

If you just want the software to work without messing with code:
1. Go to the [Releases](https://github.com/joseRey/noai-watermark-pyGUI/releases) page on this GitHub repository.
2. Download the `WatermarkRemover_Setup.exe` file and double click it to install.
3. This will create a Desktop Shortcut and a Start Menu entry. 
4. **First Run:** When you open the shortcut for the first time, a terminal window will temporarily appear to download the heavy AI models and libraries (~4 GB). Please be patient! Once finished, the graphical interface will open.

### Method 2: Manual Installation for Developers

If you prefer to run the code directly from the source:

```powershell
# Clone this repository
git clone https://github.com/joseRey/noai-watermark-pyGUI.git
cd noai-watermark-pyGUI

# Run the smart launcher script
# This script will automatically create a virtual environment, 
# download the dependencies, and launch the GUI silently!
launcher.bat
```

## 🛠️ Building the Installer Yourself

If you are a developer and want to compile the `.exe` installer yourself:
1. Download and install [Inno Setup Compiler](https://jrsoftware.org/isdl.php).
2. Open the `installer.iss` file included in this repository.
3. Click the "Compile" button. A fully standalone setup executable will be generated instantly.
