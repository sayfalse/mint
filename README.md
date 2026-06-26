# MINT — The Unified OSINT & Media Command Center

```text
          ▄          
        ▄███▄        
       ▄█▒█▒█▄       
      ██▒█▓█▒██      
     ████▒▓▒████     
    ██████▓██████    
   ███████▓███████   
  ▄██▒████▓████▒██▄  
 ▀████▒███▓███▒████▀ 
  ██████▒██▓██▒██████ 
 ▄████████▒▓▒████████▄
  ▀████████▓████████▀ 
   ▀███████▓███████▀  
     ▀█████▓█████▀    
       ▀███▓███▀      
         ▀███▀        
           █          
           █          
```

**MINT** is an interactive, terminal-based command center that unifies industry-standard OSINT (Open Source Intelligence) tools and a robust media archiver into a single, cohesive interface. Built for researchers, security analysts, and developers, MINT simplifies target intelligence gathering, social media investigation, and media preservation under a clean, keyboard-driven environment.

---

## Key Features

1. **Sherlock (Username Scanner)**
   - Scans and locates target social media accounts by username across over 300 platforms simultaneously.
2. **Holehe (Email Checker)**
   - Analyzes email address registrations across more than 120 websites using password recovery endpoints, identifying registered accounts without alerting the target.
3. **SpiderFoot (OSINT Web Server)**
   - Launches a local web server interface to automate security audits, domain reconnaissance, and threat intelligence gathering.
4. **Toutatis (Instagram Extractor)**
   - Extracts associated emails, phone numbers, and detailed profile metadata from Instagram accounts.
5. **MINT Social Tool (Social Downloader)**
   - A native, interactive downloader to archive photos, videos, stories, and highlights from major platforms (Instagram, TikTok, Facebook, and X/Twitter). Powered by high-speed `gallery-dl` and `yt-dlp` engines.
6. **One-Click Update Manager**
   - Automatically pulls the latest updates directly from the official GitHub repositories for all 4 external OSINT tools and installs any updated dependencies.

---

## Smart Path-Resolution Installer

The MINT installer (`setup.py` / `setup.bat`) is designed to protect your file system from clutter. It prompts you once for a parent directory and automatically structures the installation cleanly:
* **Tools Directory:** Recreated as `<parent_folder>\MINT_Tools\` to hold all cloned OSINT scanners.
* **Media Directory:** Recreated as `<parent_folder>\mint-social\` to store downloaded media, profile logs, and cookies.
* **Global Wrappers:** Automatically registers a global `mint` command wrapper in your system path, allowing you to launch the Command Center from any terminal window.

---

## Installation & Setup

MINT automatically manages the environment checks, directory structures, tool cloning, and dependency installations.

### Prerequisites
* **Python 3.10+** (Windows, macOS, or Linux)
* **Git** (recommended for cloning and updates; falls back to ZIP downloads if Git is missing)

### Windows Installation (Recommended)
1. Clone this repository to your system:
   ```bash
   git clone https://github.com/sayfalse/mint.git
   cd mint
   ```
2. Run the interactive installer by double-clicking `setup.bat` or executing:
   ```cmd
   setup.bat
   ```
3. Enter your preferred parent directory (e.g., `E:\mint` or `G:\`). The installer will automatically configure and build the directory tree.

### macOS / Linux Installation
1. Clone the repository and navigate into it:
   ```bash
   git clone https://github.com/sayfalse/mint.git
   cd mint
   ```
2. Run the setup script:
   ```bash
   python setup.py
   ```

---

## How to Run

Once setup is complete, you can launch the Command Center globally:

1. Open a new terminal window.
2. Type **`mint`** and press **Enter**.
3. Use the **Up/Down arrow keys** to navigate the menu, and **Enter** to launch your selected tool.
4. Alternatively, use the quick keyboard hotkeys (**1 to 7**) to jump directly to options.

---

## Cookie Configuration for Media Downloader

To download content from private profiles or bypass rate limits on social networks, the MINT Social Tool utilizes session cookies. The installer automatically generates 4 empty template cookie files in the correct path:
* `<parent_folder>\mint-social\cookies\facebook.com_cookies.txt`
* `<parent_folder>\mint-social\cookies\instagram.com_cookies.txt`
* `<parent_folder>\mint-social\cookies\tiktok.com_cookies.txt`
* `<parent_folder>\mint-social\cookies\x.com_cookies.txt`

### How to export and use cookies:
1. Install a browser extension like **Get cookies.txt LOCALLY** or **EditThisCookie** (available for Chrome/Firefox).
2. Log into your account on the target social network (e.g., Instagram or X).
3. Open the extension and export the cookies in **Netscape format**.
4. Open the corresponding cookie file in a text editor (e.g., `instagram.com_cookies.txt`) and paste the exported content.
5. Save the file. The MINT Social Tool will automatically load these cookies on subsequent runs.

---

## Configuration File (`config.json`)

The installer generates a `config.json` file in the MINT root directory to map all system paths dynamically. You can edit this file manually to update paths if you move directories:
```json
{
    "tools_dir": "E:\\mint\\MINT_Tools",
    "social_dir": "E:\\mint\\mint-social",
    "mint_dir": "E:\\mint",
    "mint_py_path": "E:\\mint\\mint.py",
    "sherlock_path": "E:\\mint\\MINT_Tools\\sherlock",
    "holehe_path": "E:\\mint\\MINT_Tools\\holehe",
    "spiderfoot_path": "E:\\mint\\MINT_Tools\\spiderfoot",
    "toutatis_path": "E:\\mint\\MINT_Tools\\toutatis"
}
```

---

## Troubleshooting & Console Setup

* **Unicode Display Issues:** If block characters or box-drawing lines appear distorted in your Windows console, MINT automatically attempts to force UTF-8 encoding on startup. If issues persist, run the following command in your terminal before launching MINT:
  ```cmd
  chcp 65001
  ```
* **Git Credential Conflicts:** If the update manager fails to pull tools due to account conflicts, MINT operates a fallback mechanism that automatically downloads the latest zip archives from official repositories and extracts them cleanly, preserving your configuration.
* **Dependencies Failed to Install:** Ensure your terminal is running with sufficient write permissions for the target installation folders, and that Python is added to your system's PATH variable.
