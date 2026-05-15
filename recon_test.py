import requests
import sys
from collections import defaultdict
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if len(sys.argv) != 2:
    print(f"Usage: python3 {sys.argv[0]} <subdomains.txt>")
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file, "r") as file:
    subdomains = [line.strip() for line in file if line.strip()]

results = defaultdict(list)

auth_keywords = [
    "login", "log in", "signin", "sign in",
    "signup", "sign up", "register",
    "password", "forgot password", "reset password",
    "otp", "verify", "verification"
]

search_keywords = [
    "search", "find", "query", "filter",
    "advanced search"
]

upload_keywords = [
    "upload", "file upload", "choose file",
    "attach", "drop file", "browse file"
]

chat_keywords = [
    "chat", "chatbot", "support chat",
    "live chat", "message", "messenger",
    "help bot", "assistant",
    "intercom", "drift", "tawk", "zendesk"
]

admin_keywords = [
    "admin", "dashboard", "control panel",
    "manage", "settings", "panel"
]

def detect_features(html):
    features = set()

    soup = BeautifulSoup(html, "html.parser")
    text = html.lower()

    title = soup.title.string.strip() if soup.title and soup.title.string else "No Title"

    if any(k in text for k in auth_keywords) or soup.find("input", {"type": "password"}):
        features.add("authentication")

    if any(k in text for k in search_keywords) or soup.find("input", {"type": "search"}):
        features.add("search")

    if any(k in text for k in upload_keywords) or soup.find("input", {"type": "file"}):
        features.add("file upload")

    if any(k in text for k in chat_keywords):
        features.add("chat")

    forms = soup.find_all("form")
    inputs = soup.find_all("input")

    if forms:
        features.add(f"{len(forms)} forms")

    if inputs:
        features.add(f"{len(inputs)} input fields")

    if any(k in text for k in admin_keywords) or "admin" in title.lower():
        features.add("admin panel")

    return features, title


for subdomain in subdomains:

    urls = [f"https://{subdomain}", f"http://{subdomain}"]

    for url in urls:
        try:
            response = requests.get(url, timeout=5, verify=False)

            status = response.status_code

            features, title = detect_features(response.text)

            print(
                f"{subdomain} : {status} : "
                f"{', '.join(features) if features else 'no features detected'} "
                f": Title -> {title}"
            )

            results[status].append(subdomain)

            break

        except requests.exceptions.RequestException:
            continue

    else:
        print(f"{subdomain} : NO RESPONSE")
        results["NO RESPONSE"].append(subdomain)

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

for status, domains in results.items():
    print(f"\n{status} : {len(domains)}")

    for d in domains:
        print(f"  - {d}")