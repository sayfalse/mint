# MINT — The Unified OSINT & Media Command Center

MINT is an interactive terminal-based command center that unifies industry-standard OSINT tools and a powerful media downloader into a single, cohesive interface. Built for researchers, analysts, and developers, MINT simplifies target intelligence gathering and media archiving.

---

## Key Features

1. **Sherlock (Username Scanner)**
   - Scans and locates social media accounts by username across over 300 platforms.
2. **Holehe (Email Checker)**
   - Checks email address registrations across more than 120 websites using password recovery endpoints without alerting the target.
3. **SpiderFoot (OSINT Web Server)**
   - Integrates a local web server interface to automate security audits and threat intelligence gathering.
4. **Toutatis (Instagram Extractor)**
   - Extracts associated emails, phone numbers, and profile details from Instagram accounts.
5. **MINT Social Tool (Social Downloader)**
   - A native, interactive downloader to archive photos, videos, stories, and highlights from major platforms (Instagram, TikTok, Facebook, and X/Twitter). Powered by `gallery-dl` and `yt-dlp`.
6. **One-Click Update Manager**
   - Automatically pulls the latest updates and manages dependency upgrades for all integrated OSINT tools from their official repositories.

---

## Installation & Setup

MINT automatically manages the environment check, directory setup, and tool downloads.

### Prerequisites
- **Python 3.10+** (Windows, macOS, or Linux)
- **Git** (recommended for automatic updates; falls back to ZIP downloads if not found)

### Steps
1. Clone or download this repository to your system:
   ```bash
   git clone https://github.com/sayfalse/mint.git
   cd mint
   ```
2. Run the interactive installer:
   - **Windows**: Double-click `setup.bat` or run:
     ```cmd
     setup.bat
     ```
   - **macOS / Linux**: Run:
     ```bash
     python setup.py
     ```
3. During setup, you will be prompted to choose installation locations for the OSINT tools and downloaded media. Default paths in your user home directory will be proposed automatically.

---

## How to Run

Once installed, a global `mint` command wrapper is registered in your environment.

1. Open a new terminal window.
2. Type **`mint`** and press Enter to launch the interactive command center.
3. Use the **Up/Down arrow keys** to navigate the menu, **Enter** to run a tool, or press **1-7** as quick hotkeys.

---

## Environment Configuration

The installer generates a `config.json` file in the installation root, containing paths for all configured tools and download destinations:
```json
{
    "tools_dir": "C:\\Users\\<username>\\MINT_Tools",
    "social_dir": "C:\\Users\\<username>\\mint-social",
    "mint_dir": "E:\\mint",
    "mint_py_path": "E:\\mint\\mint.py",
    "sherlock_path": "C:\\Users\\<username>\\MINT_Tools\\sherlock",
    "holehe_path": "C:\\Users\\<username>\\MINT_Tools\\holehe",
    "spiderfoot_path": "C:\\Users\\<username>\\MINT_Tools\\spiderfoot",
    "toutatis_path": "C:\\Users\\<username>\\MINT_Tools\\toutatis"
}
```

---

## Dependencies & Third-Party Engines
MINT coordinates several highly specialized command-line engines:
- **gallery-dl**: Handles high-speed image and metadata extraction.
- **yt-dlp**: Handles video extraction and streaming downloads.
- **colorama**: Powering the beautiful terminal interface colors and layouts.
