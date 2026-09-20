#!/usr/bin/env python3
from pathlib import Path
import PySide6

path = Path(PySide6.__file__).resolve().parent / "scripts" / "deploy_lib" / "android" / "buildozer.py"
if not path.exists():
    raise SystemExit(f"Cannot find PySide6 Android deploy generator: {path}")

text = path.read_text(encoding="utf-8")
tag = "# AUCTION_RETRO_STORE_ANDROID_PATCH"
if tag in text:
    print(f"Already patched: {path}")
    raise SystemExit(0)

needle = 'self.set_value("app", "requirements", "python3,shiboken6,PySide6")'
if needle not in text:
    raise SystemExit(f"Unsupported PySide6 deploy generator; requirements marker not found in {path}")

requirements = (
    "python3,shiboken6,PySide6,"
    "requests==2.31.0,charset-normalizer==2.1.1,urllib3==2.2.3,idna==3.10,"
    "certifi==2025.8.3,beautifulsoup4==4.13.5,soupsieve==2.8,"
    "telethon==1.41.2,pyaes==1.6.1,rsa==4.9.1,pyasn1==0.6.1,tzdata==2025.2"
)
replacement = f'''{tag}
self.set_value("app", "requirements", "{requirements}")
self.set_value("app", "title", "Auction Retro Store")
self.set_value("app", "package.name", "auctionretrostore")
self.set_value("app", "package.domain", "com.namsilat")
self.set_value("app", "version", "1.0.2")
self.set_value("app", "source.include_exts", "py,png,jpg,jpeg,ico,json,wav,txt")
self.set_value("app", "source.include_patterns", "Assets/*,Settings/*,Sounds/*")
self.set_value("app", "android.permissions", "INTERNET,ACCESS_NETWORK_STATE")
self.set_value("app", "android.minapi", "28")
self.set_value("app", "android.api", "34")
self.set_value("app", "android.accept_sdk_license", "True")
self.set_value("app", "orientation", "all")
self.set_value("app", "fullscreen", "0")'''
text = text.replace(needle, replacement, 1)
path.write_text(text, encoding="utf-8")
print(f"Patched: {path}")
