import os
import sys
import time
import subprocess
import msvcrt
import json
import shutil
import urllib.request
import zipfile
import io

# Force UTF-8 encoding on Windows to prevent UnicodeEncodeErrors with box-drawing characters
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

OPTIONS = [
    {"name": "Sherlock (Username Scanner)", "desc": "Hunts down social media accounts by username across 300+ sites"},
    {"name": "Holehe (Email Checker)", "desc": "Checks if an email address is registered on 120+ different websites"},
    {"name": "SpiderFoot (OSINT Web Server)", "desc": "Automates intelligence gathering via a local web interface"},
    {"name": "Toutatis (Instagram Extractor)", "desc": "Extracts associated emails and phone numbers from Instagram profiles"},
    {"name": "MINT Social Tool (Social Downloader)", "desc": "Downloads photos, videos, stories, and highlights from profiles"},
    {"name": "Update Tools (GitHub Pull)", "desc": "Pull the latest updates for all 4 external OSINT tools from their official repositories"},
    {"name": "Exit", "desc": "Close the MINT Command Center"}
]

# Constants and Paths for MINT Social Tool (dynamically resolved from config.json if available)
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

# Dynamic defaults based on user's home directory (standard writeable location across Windows users)
user_home = os.path.expanduser("~")
BASE = os.path.join(user_home, "mint-social")
COOKIES_DIR = os.path.join(BASE, "cookies")

if os.path.exists(config_path):
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)
            if "social_dir" in config_data:
                BASE = config_data["social_dir"]
                COOKIES_DIR = os.path.join(BASE, "cookies")
    except:
        pass

BROWSER = "chrome"
PYTHON = sys.executable
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

PHOTO_FILTER = "extension in ('jpg','jpeg','png','gif','webp','bmp','jfif','heic','avif','tiff','svg')"
VIDEO_FILTER = "extension in ('mp4','webm','mkv','mov','avi','m4v','flv','wmv','3gp','mpeg','mpg','ts','f4v','mts','m2ts')"
MEDIA_EXTS = ["jpg", "jpeg", "png", "gif", "webp", "bmp", "jfif", "heic", "avif", "tiff", "svg", "mp4", "webm", "mkv", "mov", "avi", "m4v", "flv", "wmv", "3gp", "mpeg", "mpg", "ts", "f4v", "mts", "m2ts"]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_terminal_width():
    try:
        width = os.get_terminal_size().columns
        return width if width > 20 else 80
    except:
        return 80

def print_centered(text, visible_len, color=""):
    width = get_terminal_width()
    padding = max(0, (width - visible_len) // 2)
    print(" " * padding + color + text)

def wrap_text(text, max_len=52):
    words = text.split()
    lines = []
    current_line = []
    current_len = 0
    for word in words:
        if current_len + len(word) + len(current_line) > max_len:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_len = len(word)
        else:
            current_line.append(word)
            current_len += len(word)
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def draw_header(subtitle="Select a tool to launch from the menu below:"):
    logo_lines = [
        "          ▄          ",
        "        ▄███▄        ",
        "       ▄█▒█▒█▄       ",
        "      ██▒█▓█▒██      ",
        "     ████▒▓▒████     ",
        "    ██████▓██████    ",
        "   ███████▓███████   ",
        "  ▄██▒████▓████▒██▄  ",
        " ▀████▒███▓███▒████▀ ",
        " ██████▒██▓██▒██████ ",
        "▄████████▒▓▒████████▄",
        " ▀████████▓████████▀ ",
        "  ▀███████▓███████▀  ",
        "    ▀█████▓█████▀    ",
        "      ▀███▓███▀      ",
        "        ▀███▀        ",
        "          █          ",
        "          █          "
    ]
    
    current_workspace = os.getcwd()
    
    for line in logo_lines:
        print_centered(line, 21, Fore.GREEN)
        
    print()
    print_centered("M I N T   v1.0", 14, Fore.GREEN + Style.BRIGHT)
    print_centered("─" * 50, 50, Fore.LIGHTBLACK_EX)
    print_centered("The Unified OSINT & Media Command Center", 40, Fore.WHITE + Style.BRIGHT)
    print_centered(f"Workspace: {current_workspace}", len(f"Workspace: {current_workspace}"), Fore.LIGHTBLACK_EX)
    print_centered(Fore.LIGHTBLACK_EX + "GitHub: " + Fore.BLUE + "https://github.com/sayfalse", 36)
    print_centered("Environment: Windows  •  Python: 3.14", 37, Fore.LIGHTBLACK_EX)
    print()
    print_centered(subtitle, len(subtitle), Fore.WHITE)
    print()

def draw_menu(selected_index):
    clear_screen()
    draw_header()
    
    menu_width = 43
    width = get_terminal_width()
    menu_padding = max(0, (width - menu_width) // 2)
    
    for i, opt in enumerate(OPTIONS):
        if i == selected_index:
            print(" " * menu_padding + Fore.GREEN + Style.BRIGHT + "  ❯ " + Back.GREEN + Fore.BLACK + f" {opt['name'].ljust(38)} " + Style.RESET_ALL)
        else:
            print(" " * menu_padding + Fore.WHITE + f"    {opt['name']}")
    print()
    
    desc_width = 50
    desc_padding = max(0, (width - desc_width) // 2)
    
    print(" " * desc_padding + Fore.LIGHTBLACK_EX + "─" * 50)
    current_desc = OPTIONS[selected_index]['desc']
    wrapped_desc = wrap_text(current_desc, 44)
    for idx, d_line in enumerate(wrapped_desc):
        if idx == 0:
            print(" " * desc_padding + Fore.YELLOW + "Info: " + Fore.WHITE + d_line)
        else:
            print(" " * desc_padding + "      " + Fore.WHITE + d_line)
    print(" " * desc_padding + Fore.LIGHTBLACK_EX + "─" * 50)
    print()
    
    print_centered(Fore.BLACK + Back.LIGHTBLACK_EX + "  ↑/↓: Move  •  Enter: Run  •  1-7: Hotkey  •  Esc: Exit  ", 58)
    print()

def get_key():
    ch = msvcrt.getch()
    if ch in (b'\x00', b'\xe0'):
        ch = msvcrt.getch()
        if ch == b'H': return 'up'
        if ch == b'P': return 'down'
    elif ch == b'\r':
        return 'enter'
    elif ch == b'\x1b':
        return 'esc'
    else:
        try:
            return ch.decode('utf-8')
        except:
            return None

def prompt_input(label):
    print(Fore.GREEN + f"  ❯ {label}: " + Fore.WHITE, end="")
    sys.stdout.flush()
    return input().strip()

def run_command(cmd_string):
    try:
        subprocess.run(cmd_string, shell=True)
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n  [!] Process stopped by user.")
    except Exception as e:
        print(Fore.RED + f"\n  [!] Error executing command: {e}")

def parse_profile_url(url, platform):
    url = url.strip()
    if not url:
        return None
    if not url.lower().startswith("http"):
        url = "https://" + url
    t = url.replace("http://", "").replace("https://", "")
    if t.startswith("/"):
        t = t[1:]
    parts = t.split("/")
    if len(parts) < 2:
        return None
    dom = parts[0].replace("www.", "").lower()
    usr = parts[1]
    
    if platform == "instagram" and dom != "instagram.com": return None
    if platform == "tiktok" and dom != "tiktok.com": return None
    if platform == "facebook" and dom != "facebook.com": return None
    if platform == "x" and dom not in ["x.com", "twitter.com"]: return None
    
    username = usr.replace("@", "")
    for char in ["?", "#", "/"]:
        username = username.split(char)[0]
    return username if username else None

def get_cookies_arg(platform):
    if platform == "tiktok":
        return f"--cookies-from-browser {BROWSER}"
        
    possible_dirs = [d for d in [COOKIES_DIR, BASE] if d and os.path.exists(d)]
    possible_names = [
        f"{platform}.com_cookies.txt",
        f"{platform}_cookies.txt",
        f"{platform}.com_cookies.txt"
    ]
    
    possible_paths = [os.path.join(d, name) for d in possible_dirs for name in possible_names]
    for path in possible_paths:
        if os.path.exists(path):
            return f'--cookies "{path}"'
            
    return ""

def check_archive(directory, archive_path):
    if not os.path.exists(directory):
        if os.path.exists(archive_path):
            try: os.remove(archive_path)
            except: pass
        return
    
    media_count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            ext = file.split(".")[-1].lower()
            if ext in MEDIA_EXTS:
                media_count += 1
                
    archive_lines = 0
    if os.path.exists(archive_path):
        try:
            with open(archive_path, "r", encoding="utf-8", errors="ignore") as f:
                archive_lines = len(f.readlines())
        except:
            pass
            
    if media_count == 0:
        if os.path.exists(archive_path):
            try:
                os.remove(archive_path)
                print("    Empty, archive cleared.")
            except:
                pass
    elif archive_lines == 0:
        print(f"    {media_count} files, rebuilding...")
    else:
        print(f"    {media_count} files, archive ok.")

def run_gallery_dl(gdir, gfil, gck, gurl):
    os.makedirs(gdir, exist_ok=True)
    archive_path = os.path.join(gdir, "archive.txt")
    cmd = f'"{PYTHON}" -m gallery_dl -D "{gdir}" --filter "{gfil}" {gck} -o "user-agent={UA}" --download-archive "{archive_path}" --sleep-request 5 "{gurl}"'
    return subprocess.run(cmd, shell=True).returncode

def run_yt_dlp(ydir, yck, yurl):
    os.makedirs(ydir, exist_ok=True)
    cmd = f'"{PYTHON}" -m yt_dlp -o "{ydir}\\%(title)s.%(ext)s" {yck} --no-playlist --user-agent "{UA}" "{yurl}"'
    return subprocess.run(cmd, shell=True).returncode

def download_photos(dest_dir, cookies_arg, url):
    check_archive(os.path.join(dest_dir, "Photos"), os.path.join(dest_dir, "Photos", "archive.txt"))
    print("    [Photos]")
    ret = run_gallery_dl(os.path.join(dest_dir, "Photos"), PHOTO_FILTER, cookies_arg, url)
    if ret != 0:
        print("    [ERROR]")

def download_videos(dest_dir, cookies_arg, url):
    check_archive(os.path.join(dest_dir, "Videos"), os.path.join(dest_dir, "Videos", "archive.txt"))
    print("    [Videos]")
    ret = run_gallery_dl(os.path.join(dest_dir, "Videos"), VIDEO_FILTER, cookies_arg, url)
    if ret != 0:
        print("    Trying yt-dlp...")
        ret_yt = run_yt_dlp(os.path.join(dest_dir, "Videos"), cookies_arg, url)
        if ret_yt != 0:
            print("    [ERROR]")

def download_stories(dest_dir, cookies_arg, platform, username):
    if platform != "instagram":
        return
    check_archive(os.path.join(dest_dir, "Stories"), os.path.join(dest_dir, "Stories", "archive.txt"))
    print("    [Stories]")
    url = f"https://www.instagram.com/stories/{username}/"
    ret = run_gallery_dl(os.path.join(dest_dir, "Stories"), "true", cookies_arg, url)
    if ret != 0:
        print("    [ERROR]")

def download_highlights(dest_dir, cookies_arg, platform, username):
    if platform != "instagram":
        return
    check_archive(os.path.join(dest_dir, "Highlights"), os.path.join(dest_dir, "Highlights", "archive.txt"))
    print("    [Highlights]")
    url = f"https://www.instagram.com/{username}/highlights/"
    ret = run_gallery_dl(os.path.join(dest_dir, "Highlights"), "true", cookies_arg, url)
    if ret != 0:
        print("    [ERROR]")

def download_profile(username, dest_dir, platform, original_url, media_choice):
    cookies_arg = get_cookies_arg(platform)
    url = original_url.strip()
    while url.endswith("/"):
        url = url[:-1]
        
    if media_choice in ["1", "5", "7"]:
        download_photos(dest_dir, cookies_arg, url)
    if media_choice in ["2", "5", "7"]:
        download_videos(dest_dir, cookies_arg, url)
    if media_choice in ["3", "6", "7"]:
        download_stories(dest_dir, cookies_arg, platform, username)
    if media_choice in ["4", "6", "7"]:
        download_highlights(dest_dir, cookies_arg, platform, username)

def run_social_tool_downloads(media_choice):
    os.makedirs(BASE, exist_ok=True)
    os.makedirs(COOKIES_DIR, exist_ok=True)
    
    platforms = ["instagram", "tiktok", "facebook", "x"]
    for platform in platforms:
        profile_file = os.path.join(BASE, f"{platform}_profiles.txt")
        if os.path.exists(profile_file):
            if platform == "x":
                print(Fore.CYAN + "\n  [X/TWITTER]")
            else:
                print(Fore.CYAN + f"\n  [{platform.upper()}]")
                
            try:
                with open(profile_file, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
            except Exception as e:
                print(Fore.RED + f"  [!] Error reading profiles: {e}")
                continue
                
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if line.startswith("#") or line.startswith(";"):
                    continue
                    
                username = parse_profile_url(line, platform)
                if username and username != "INVALID_URL":
                    print(Fore.WHITE + f"  --- {username}")
                    dest_dir = os.path.join(BASE, platform, username)
                    download_profile(username, dest_dir, platform, line, media_choice)

def draw_social_menu(selected_index):
    clear_screen()
    draw_header("Running: MINT Social Tool (Social Downloader)")
    
    print_centered("=== MINT Social Tool ===", 24, Fore.GREEN + Style.BRIGHT)
    print()
    print_centered("What do you want to download?", 29, Fore.WHITE + Style.BRIGHT)
    print()
    
    menu_options = [
        "Photos only",
        "Videos only",
        "Stories only",
        "Highlights only",
        "Photos + Videos",
        "Stories + Highlights",
        "All",
        "Back to Main Menu"
    ]
    
    menu_width = 30
    width = get_terminal_width()
    menu_padding = max(0, (width - menu_width) // 2)
    
    for i, opt in enumerate(menu_options):
        if i == selected_index:
            print(" " * menu_padding + Fore.GREEN + Style.BRIGHT + f"  ❯ " + Back.GREEN + Fore.BLACK + f" [{i+1}] {opt.ljust(20)} " + Style.RESET_ALL)
        else:
            print(" " * menu_padding + Fore.WHITE + f"    [{i+1}] {opt}")
            
    print()
    print_centered("  ↑/↓: Move  •  Enter: Select  •  1-8: Hotkey  ", 48, Fore.BLACK + Back.LIGHTBLACK_EX)
    print()

def run_social_tool_tui():
    selected_index = 0
    while True:
        draw_social_menu(selected_index)
        key = get_key()
        
        if key == 'up':
            selected_index = (selected_index - 1) % 8
        elif key == 'down':
            selected_index = (selected_index + 1) % 8
        elif key == 'esc':
            break
        elif key in ['1', '2', '3', '4', '5', '6', '7', '8']:
            selected_index = int(key) - 1
            key = 'enter'
            
        if key == 'enter':
            if selected_index == 7:
                break
            
            clear_screen()
            media_choice = str(selected_index + 1)
            draw_header(f"Running: MINT Social Tool - Mode [{media_choice}]")
            
            print(Fore.GREEN + Style.BRIGHT + f"  === MINT Social Tool - Mode [{media_choice}] ===")
            print()
            print(Fore.YELLOW + f"  [+] Starting downloads in mode [{media_choice}]...")
            print(Fore.LIGHTBLACK_EX + "  " + "─" * 50)
            
            try:
                run_social_tool_downloads(media_choice)
            except KeyboardInterrupt:
                print(Fore.YELLOW + "\n  [!] Downloads interrupted by user.")
            except Exception as e:
                print(Fore.RED + f"\n  [!] Error running downloads: {e}")
                
            print(Fore.LIGHTBLACK_EX + "\n  " + "─" * 50)
            print(Fore.GREEN + "  [+] Done.")
            print()
            input("  Press Enter to return to MINT Social Tool menu...")

def update_single_tool(key, name, path):
    if os.path.exists(os.path.join(path, ".git")):
        try:
            print(Fore.LIGHTBLACK_EX + "    Running git pull...")
            subprocess.run(["git", "-C", path, "pull"], check=True)
            
            req_file = os.path.join(path, "requirements.txt")
            if os.path.exists(req_file):
                if key == "spiderfoot":
                    try:
                        with open(req_file, "r", encoding="utf-8") as f:
                            content = f.read()
                        if "lxml>=4.9.2,<5" in content:
                            content = content.replace("lxml>=4.9.2,<5", "lxml>=4.9.2")
                            with open(req_file, "w", encoding="utf-8") as f:
                                f.write(content)
                    except Exception as e:
                        print(Fore.RED + f"    [!] Warning: Failed to patch SpiderFoot requirements: {e}")

                print(Fore.LIGHTBLACK_EX + "    Upgrading dependencies...")
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_file], check=True)
                
            print(Fore.GREEN + f"    [+] {name} updated successfully.")
        except Exception as e:
            print(Fore.RED + f"    [!] Error updating {name}: {e}")
        return

    print(Fore.LIGHTBLACK_EX + "    Not a git repo. Attempting re-download from GitHub...")
    try:
        repos = {
            "sherlock": "sherlock-project/sherlock",
            "holehe": "megadose/holehe",
            "spiderfoot": "smicallef/spiderfoot",
            "toutatis": "leogout/toutatis"
        }
        
        repo = repos.get(key)
        if not repo:
            return
            
        zip_url = f"https://github.com/{repo}/archive/refs/heads/master.zip"
        try:
            req = urllib.request.Request(zip_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                zip_data = response.read()
        except:
            zip_url = f"https://github.com/{repo}/archive/refs/heads/main.zip"
            req = urllib.request.Request(zip_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                zip_data = response.read()
                
        temp_dir = os.path.join(os.path.dirname(path), f"{key}_temp_update")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir, exist_ok=True)
        
        with zipfile.ZipFile(io.BytesIO(zip_data)) as zip_ref:
            zip_ref.extractall(temp_dir)
            
        extracted_folder = None
        for folder in os.listdir(temp_dir):
            if folder.startswith(key) or folder.startswith(name.lower()):
                extracted_folder = os.path.join(temp_dir, folder)
                break
                
        if extracted_folder:
            for item in os.listdir(extracted_folder):
                s = os.path.join(extracted_folder, item)
                d = os.path.join(path, item)
                if os.path.isdir(s):
                    if os.path.exists(d):
                        shutil.rmtree(d)
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)
                    
            req_file = os.path.join(path, "requirements.txt")
            if os.path.exists(req_file):
                if key == "spiderfoot":
                    try:
                        with open(req_file, "r", encoding="utf-8") as f:
                            content = f.read()
                        if "lxml>=4.9.2,<5" in content:
                            content = content.replace("lxml>=4.9.2,<5", "lxml>=4.9.2")
                            with open(req_file, "w", encoding="utf-8") as f:
                                f.write(content)
                    except Exception as e:
                        print(Fore.RED + f"    [!] Warning: Failed to patch SpiderFoot requirements: {e}")
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_file], check=True)
                
            print(Fore.GREEN + f"    [+] {name} re-downloaded and updated successfully.")
        else:
            print(Fore.RED + f"    [!] Could not locate extracted files in zip.")
            
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
    except Exception as e:
        print(Fore.RED + f"    [!] Error downloading update: {e}")

def run_tools_update():
    clear_screen()
    draw_header("Updating OSINT Tools from GitHub")
    
    print(Fore.GREEN + Style.BRIGHT + "  === Update OSINT Tools ===")
    print()
    
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    if not os.path.exists(config_path):
        print(Fore.RED + "  [!] Configuration file (config.json) not found.")
        print(Fore.YELLOW + "  [+] Please run setup.py/setup.bat first to configure and install the tools.")
        print()
        input("  Press Enter to return to menu...")
        return
        
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception as e:
        print(Fore.RED + f"  [!] Error reading config.json: {e}")
        print()
        input("  Press Enter to return to menu...")
        return
        
    tools = {
        "sherlock": ("Sherlock", config.get("sherlock_path")),
        "holehe": ("Holehe", config.get("holehe_path")),
        "spiderfoot": ("SpiderFoot", config.get("spiderfoot_path")),
        "toutatis": ("Toutatis", config.get("toutatis_path"))
    }
    
    print(Fore.YELLOW + "  [+] Checking for updates from official GitHub repositories...\n")
    
    for key, (name, path) in tools.items():
        if not path or not os.path.exists(path):
            print(Fore.RED + f"  [!] {name} path not configured or directory does not exist.")
            continue
            
        print(Fore.WHITE + f"  ❯ Updating {name} at {path}...")
        update_single_tool(key, name, path)
        print()
        
    print(Fore.GREEN + Style.BRIGHT + "  [+] Update process finished.")
    print()
    input("  Press Enter to return to menu...")

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--social":
            run_social_tool_tui()
            sys.exit(0)
        elif sys.argv[1] == "--update":
            run_tools_update()
            sys.exit(0)

    selected_index = 0
    
    while True:
        draw_menu(selected_index)
        key = get_key()
        
        if key == 'up':
            selected_index = (selected_index - 1) % len(OPTIONS)
        elif key == 'down':
            selected_index = (selected_index + 1) % len(OPTIONS)
        elif key == 'esc':
            break
        elif key in ['1', '2', '3', '4', '5', '6', '7']:
            idx = int(key) - 1
            selected_index = idx
            key = 'enter'
            
        if key == 'enter':
            clear_screen()
            
            if selected_index == 0:  # Sherlock
                draw_header("Running: Sherlock (Username Scanner)")
                print(Fore.GREEN + Style.BRIGHT + "  === Sherlock (Username Scanner) ===")
                print()
                username = prompt_input("Enter target username")
                if not username:
                    continue
                if username.lower() == "/update":
                    run_tools_update()
                    continue
                
                print(Fore.YELLOW + f"\n  [+] Querying 300+ platforms for '{username}'...\n")
                run_command(f"sherlock {username}")
                print()
                input("  Press Enter to return to menu...")
                
            elif selected_index == 1:  # Holehe
                draw_header("Running: Holehe (Email Checker)")
                print(Fore.GREEN + Style.BRIGHT + "  === Holehe (Email Checker) ===")
                print()
                email = prompt_input("Enter target email address")
                if not email:
                    continue
                if email.lower() == "/update":
                    run_tools_update()
                    continue
                
                print(Fore.YELLOW + f"\n  [+] Querying registration endpoints for '{email}'...\n")
                run_command(f"holehe {email}")
                print()
                input("  Press Enter to return to menu...")
                
            elif selected_index == 2:  # SpiderFoot
                draw_header("Running: SpiderFoot (OSINT Web Server)")
                print(Fore.GREEN + Style.BRIGHT + "  === SpiderFoot (OSINT Web Server) ===")
                print()
                print(Fore.GREEN + "  [+] Starting SpiderFoot local web server...")
                print(Fore.YELLOW + "  [+] Dashboard URL: http://127.0.0.1:5001")
                print(Fore.RED + "  [+] Press Ctrl+C inside this window to stop the server.")
                print()
                run_command("spiderfoot")
                print()
                input("  Press Enter to return to menu...")
                
            elif selected_index == 3:  # Toutatis
                draw_header("Running: Toutatis (Instagram Extractor)")
                print(Fore.GREEN + Style.BRIGHT + "  === Toutatis (Instagram Extractor) ===")
                print()
                username = prompt_input("Enter target Instagram username")
                if not username:
                    continue
                if username.lower() == "/update":
                    run_tools_update()
                    continue
                
                sessionid = prompt_input("Enter Instagram Session ID (optional - press Enter to skip)")
                if sessionid:
                    cmd = f"toutatis -u {username} -s {sessionid}"
                else:
                    cmd = f"toutatis -u {username}"
                print(Fore.YELLOW + f"\n  [+] Querying Instagram API for '{username}'...\n")
                run_command(cmd)
                print()
                input("  Press Enter to return to menu...")
                
            elif selected_index == 4:  # MINT Social Tool (Social Downloader)
                run_social_tool_tui()
                
            elif selected_index == 5:  # Update Tools
                run_tools_update()
                
            elif selected_index == 6:  # Exit
                break

    clear_screen()
    print(Fore.GREEN + Style.BRIGHT + "========================================")
    print(Fore.GREEN + Style.BRIGHT + "   Thank you for using MINT. Goodbye!   ")
    print(Fore.GREEN + Style.BRIGHT + "========================================")
    time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print(Fore.GREEN + "\nGoodbye!")
        sys.exit(0)
