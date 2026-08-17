import os
import glob
import requests
import time

# ==========================================
# CONFIGURATION
# ==========================================

# 1. Your ZeptoMail API Domain (e.g., api.zeptomail.com, api.zeptomail.eu, api.zeptomail.in)
BASE_URL = "https://api.zeptomail.com/v1.1"

# 2. Directory containing your HTML templates
TEMPLATES_DIR = "./templates"

# 3. OAuth Token (Generate via Zoho API Console using a Self Client)
OAUTH_TOKEN = "YOUR_OAUTH_ACCESS_TOKEN_HERE"

# 4. Map your Language Codes to ZeptoMail Agent Aliases
# (You can find your Agent Alias in ZeptoMail -> Agents -> SMTP/API)
AGENTS = {
    "en": "AGENT_ALIAS_FOR_ENGLISH",
    "fr": "AGENT_ALIAS_FOR_FRENCH",
    "es": "AGENT_ALIAS_FOR_SPANISH",
    # Add more as needed...
}

# ==========================================

def extract_title(html_content):
    import re
    match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return "Transactional Email Template"

def upload_templates():
    headers = {
        "Authorization": f"Zoho-oauthtoken {OAUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    
    total_success = 0
    total_errors = 0
    
    for lang, agent_alias in AGENTS.items():
        print(f"\n{'='*40}")
        print(f" Processing Language: {lang.upper()} ")
        print(f" Agent Alias: {agent_alias}")
        print(f"{'='*40}")
        
        endpoint = f"{BASE_URL}/agents/{agent_alias}/templates"
        
        # We assume templates are named like: welcome-email-en.html
        search_pattern = f"*-{lang}.html"
        html_files = glob.glob(os.path.join(TEMPLATES_DIR, search_pattern))
            
        if not html_files:
            print(f"❌ No templates found for language code '{lang}'. Skipping.")
            continue
            
        print(f"Found {len(html_files)} templates. Uploading...")
        
        for i, file_path in enumerate(html_files, 1):
            filename = os.path.basename(file_path)
            template_name = os.path.splitext(filename)[0]
            
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
                
            payload = {
                "template_name": template_name,
                "subject": extract_title(html_content),
                "htmlbody": html_content
            }
            
            print(f"[{i}/{len(html_files)}] Uploading {template_name}...", end=" ")
            
            try:
                response = requests.post(endpoint, headers=headers, json=payload)
                if response.status_code in [200, 201]:
                    print("✅ Success")
                    total_success += 1
                else:
                    print(f"❌ Failed: {response.status_code} - {response.text}")
                    total_errors += 1
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                total_errors += 1
                
            # Crucial: Sleep 1s to respect ZeptoMail API throttling limits across batches
            time.sleep(1)

    print("\n" + "="*40)
    print(" ALL IMPORTS COMPLETE ")
    print("="*40)
    print(f"Total Successful Uploads: {total_success}")
    print(f"Total Failed Uploads: {total_errors}")

if __name__ == "__main__":
    if OAUTH_TOKEN == "YOUR_OAUTH_ACCESS_TOKEN_HERE":
        print("Please edit this script and insert your OAUTH_TOKEN and AGENTS mapping before running.")
    else:
        upload_templates()
