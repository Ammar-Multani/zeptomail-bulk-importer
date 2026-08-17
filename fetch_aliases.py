import requests
import json
import os

# ==========================================
# CONFIGURATION
# ==========================================

# 1. Your ZeptoMail API Domain (e.g., api.zeptomail.com, api.zeptomail.eu, api.zeptomail.in)
BASE_URL = "https://api.zeptomail.com/v1.1"

# 2. Map your Language Codes to ZeptoMail Agent Aliases
AGENTS = {
    "en": "AGENT_ALIAS_FOR_ENGLISH",
    "fr": "AGENT_ALIAS_FOR_FRENCH",
    "es": "AGENT_ALIAS_FOR_SPANISH",
    # Add more as needed...
}

# 3. OAuth Token (Generate via Zoho API Console using a Self Client)
OAUTH_TOKEN = "YOUR_OAUTH_ACCESS_TOKEN_HERE"

# ==========================================

def fetch_all():
    headers = {"Authorization": f"Zoho-oauthtoken {OAUTH_TOKEN}"}
    
    with open("zepto_mail_master_registry.md", "w") as f:
        f.write("# ZeptoMail Master Template Registry\n\n")
        f.write("This document contains the exact templates successfully fetched directly from the ZeptoMail API for each language Agent.\n\n")
        f.write("You can use **EITHER** the readable `template_name` (Alias) OR the immutable `template_key` when calling the Send Mail API.\n\n")
        
        for lang, alias in AGENTS.items():
            print(f"Fetching templates for {lang.upper()} ({alias})...")
            res = requests.get(f"{BASE_URL}/agents/{alias}/templates", headers=headers)
            
            if res.status_code == 200:
                templates = res.json().get("data", [])
                
                f.write(f"## {lang.upper()} Agent (Alias: `{alias}`)\n\n")
                f.write("| Readable Alias (`template_name`) | Immutable Key (`template_key`) |\n")
                f.write("| :--- | :--- |\n")
                
                for t in sorted(templates, key=lambda x: x.get("template_name", "")):
                    name = t.get("template_name", "UNKNOWN")
                    key = t.get("template_key", "UNKNOWN")
                    f.write(f"| `{name}` | `{key}` |\n")
                    
                f.write("\n---\n\n")
            else:
                print(f"❌ Error fetching {lang}: {res.status_code} - {res.text}")
                
    print("\n✅ Done! Master registry saved to zepto_mail_master_registry.md")

if __name__ == "__main__":
    if OAUTH_TOKEN == "YOUR_OAUTH_ACCESS_TOKEN_HERE":
        print("Please edit this script and insert your OAUTH_TOKEN and AGENTS mapping before running.")
    else:
        fetch_all()
