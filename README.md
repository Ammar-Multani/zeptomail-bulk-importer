# ZeptoMail Bulk Template Importer & Multi-Language Architecture

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A blazing-fast, automated Python script to bulk upload HTML email templates into Zoho ZeptoMail via their Template API. 

If you are currently uploading templates manually through the ZeptoMail UI one by one, **this script will save you hours of tedious work.** It allows you to push dozens or hundreds of templates in seconds, completely avoiding the sluggish UI.

Additionally, this repository outlines an architecture for SaaS applications to bypass ZeptoMail's strict 100-template limit when localizing transactional emails into multiple languages.

## 🚀 Why use this?

1. **Massive Time Savings:** Uploading templates manually via the ZeptoMail dashboard is incredibly slow. With this script, you can deploy 100 templates in under 2 minutes.
2. **Automated Title Extraction:** The script automatically reads the `<title>` tag from your HTML files and sets it as the Email Subject in ZeptoMail.
3. **Smart Rate Limiting:** ZeptoMail will throttle you (HTTP 422/401) if you upload too fast. This script handles the API pacing automatically so you never hit a rate limit.
4. **Bypass the 100-Template Limit:** ZeptoMail enforces a strict hard limit of exactly 100 templates per Mail Agent. If you run a multi-lingual SaaS (e.g., 20 emails × 7 languages = 140 templates), you will hit this wall immediately.

---

## 🏗️ Multi-Language Architecture (Bypassing the Limit)

To bypass the 100-template limit for multi-lingual apps, you must adopt a **"One Mail Agent per Language"** architecture.

Instead of putting all localized templates into a single agent, create dedicated Mail Agents in ZeptoMail (e.g., `Pontora EN`, `Pontora FR`, `Pontora ES`). Each agent will hold the identical set of templates, translated for that specific language. 

### How it works on your Backend
Each Mail Agent in ZeptoMail has its own unique `Send Mail Token`. You do not need to change the template alias names in your code. You simply swap the authorization token dynamically based on the user's language:

```javascript
const zeptoTokens = {
  en: process.env.ZEPTO_TOKEN_EN,
  fr: process.env.ZEPTO_TOKEN_FR,
  es: process.env.ZEPTO_TOKEN_ES,
};

// If sending to a Spanish user, just use the Spanish Agent Token!
const sendToken = zeptoTokens[user.language] || zeptoTokens['en'];

const response = await fetch("https://api.zeptomail.com/v1.1/email/template", {
  method: "POST",
  headers: {
    "Authorization": `Zoho-enczapikey ${sendToken}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    template_alias: "deletion-reminder", // Alias remains identical across all agents!
    to: [{ email_address: { address: user.email } }]
  })
});
```

---

## ⚙️ Setup & Usage

Here is the exact step-by-step process you need to follow to configure the script:

### Step 1: Get your Agent Alias
1. Log in to your ZeptoMail Dashboard.
2. Click on **Mail Agents** in the left sidebar and select the agent you are using.
3. Click on the **SMTP/API** tab.
4. Copy the **Agent Alias** (it's usually a short string). Save this somewhere for a moment.

### Step 2: Create a Zoho "Self Client"
1. Open a new browser tab and go to the [Zoho API Console](https://api-console.zoho.com/).
2. Click **Get Started** (or "Add Client" if you already have others).
3. Choose the **Self Client** option and click **Create Now**.
4. Click **OK** to confirm.
5. In the Client Secret tab that appears, you will see a Client ID and a Client Secret. Leave this tab open.

### Step 3: Generate a Temporary Authorization Code
1. Still in the Zoho API Console (for your Self Client), click on the **Generate Code** tab.
2. In the Scope field, copy and paste this exact text: `ZeptoMail.MailTemplates.ALL`
3. Set the Time Duration to 10 minutes (or whatever is available).
4. Enter any random text (like "Template Import") in the Description field, and click **Generate**.
5. A window will pop up with a long Authorization Code. Copy it!

### Step 4: Exchange for OAuth Token
Exchange that temporary code for an OAuth Access Token. (You can do this by making a quick POST request to Zoho's token endpoint).

### Step 5: Configure the Script
Open `bulk_import.py` and modify the configuration block:
- Set your `OAUTH_TOKEN` (or allow the script to prompt you for the exchange).
- Set your `BASE_URL` based on your region (e.g., `.com`, `.eu`, `.in`).
- Set the `AGENTS` dictionary mapping your language codes to their respective ZeptoMail Agent Aliases.

### 3. Run the Importer
Place your HTML files in the `outputs/` directory. Name them with a language suffix (e.g., `welcome-email-fr.html`).

Run the script:
```bash
python3 bulk_import.py
```

The script will:
1. Scan the folder for templates matching the language code.
2. Extract the `<title>` for the subject line.
3. Automatically push them to the correct ZeptoMail Mail Agent.
4. Pause for 1 second between uploads to prevent ZeptoMail from throttling the requests.

---

## 🔍 Fetching the Master Template Registry
Once you have uploaded all your templates across all agents, your developers will need to know the exact **Template Aliases** or **Template Keys** to use when calling the Send Mail API.

Instead of hunting through the ZeptoMail UI, use the included `fetch_aliases.py` script to automatically generate a beautiful Markdown table of every template in your account.

1. Configure `fetch_aliases.py` with your OAuth token and Agent Aliases.
2. Run the script:
   ```bash
   python3 fetch_aliases.py
   ```
3. A file named `zepto_mail_master_registry.md` will be generated, containing a perfect list of both the Readable Aliases (`template_name`) and the Immutable Keys (`template_key`) for every single template across all languages!

---

## 📄 License
MIT License. Feel free to use and modify for your own projects!
