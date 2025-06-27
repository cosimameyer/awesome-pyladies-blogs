import os
import json
import random
import requests
from datetime import datetime, timezone
from typing import Optional
import urllib.parse

fallback_images_dir = "img/fallback_images/"
fallback_images = [f for f in os.listdir(fallback_images_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
directory_path = "blogs/"

def load_svg_inline_from_url(icon_url, color="black", size=20):
    try:
        response = requests.get(icon_url)
        response.raise_for_status()
        svg_content = response.text

        svg_content = svg_content.replace('<svg ', f'<svg fill="{color}" width="{size}" height="{size}" ')
        return svg_content
    except requests.RequestException:
        return "" 

def build_social_icons(social_dict, icon_style='emoji'):
    socials = ""
    base_icon_url = "https://github.com/cosimameyer/awesome-pyladies-blogs/raw/main/img/icons/"

    ordered_platforms = ["website", "github", "mastodon", "bluesky", "instagram", "youtube", "linkedin", "twitter"]

    emoji_icons = {
        "website": "🌐",
        "github": "🐙",
        "mastodon": "🐘",
        "bluesky": "🦋",
        "instagram": "📸",
        "youtube": "▶️",
        "linkedin": "🧳",
        "twitter": "🐦"
    }

    for platform in ordered_platforms:
        handle = social_dict.get(platform)
        url = build_social_url(platform, handle)
        if not url:
            continue

        if icon_style == 'emoji':
            label = emoji_icons.get(platform, "🔗")
            socials += f'<a href="{url}" target="_blank" style="margin:0 4px; font-size:16px; text-decoration:none; color:black;">{label}</a> '
        else:
            if platform == "linkedin":
                socials += (
                    f''
                )
            else:
                icon_url = add_platform_icon(platform, base_icon_url, url)
                if not icon_url:
                    continue
                socials += (
                        f'<a href="{url}" target="_blank" style="margin:0 1px;">'
                        f'{icon_url}'
                        f'</a> '
                    )

    return socials


def add_platform_icon(platform: str, base_icon_url: str, url: Optional[str]) -> Optional[str]:
    """
    Construct the full icon URL for a given platform if a URL is provided.

    Args:
        platform: Name of the platform (e.g., "twitter", "website").
        base_icon_url: Base URL where icons are hosted.
        url: The URL to the user profile or site. If None or empty, returns None.

    Returns:
        A full URL to the platform icon, or None if no URL provided.
    """
    if platform == "website":
        platform = "safari"
    elif platform == "twitter":
        platform = "x"        

    if not url:
        return None
    
    icon_url = f"{base_icon_url}{platform}.svg"
    
    svg_icon_html = load_svg_inline_from_url(icon_url, color="#929dad", size=15)

    return svg_icon_html

def build_social_url(platform, handle):
    if not handle:
        return None
    
    handle = handle.strip()

    # Decode URL-encoded characters like %40 → @
    handle = urllib.parse.unquote(handle)

    # Remove leading @ for most platforms except Mastodon and Bluesky (which need them)
    if platform not in ["mastodon", "bluesky"]:
        handle = handle.lstrip("@")

    if platform == "twitter":
        if handle.startswith("http"):
            return handle
        return f"https://twitter.com/{handle}"

    elif platform == "mastodon":
        # Mastodon handle is @user@domain
        if handle.startswith("http"):
            return handle
        if "@" in handle[1:]:
            parts = handle.lstrip("@").split("@")
            if len(parts) == 2:
                user, domain = parts
                return f"https://{domain}/@{user}"
        return handle

    elif platform == "linkedin":
        if handle.startswith("http"):
            return handle
        handle = handle.rstrip("/")
        return f"https://www.linkedin.com/in/{handle}"

    elif platform == "github":
        if handle.startswith("http"):
            return handle
        return f"https://github.com/{handle}"

    elif platform == "youtube":
        # YouTube handles can be channel IDs or usernames, often URL encoded
        if handle.startswith("http"):
            return handle
        # If it starts with '@', it's a YouTube handle, e.g. @username → https://www.youtube.com/@username
        if handle.startswith("@"):
            return f"https://www.youtube.com/{handle}"
        else:
            return f"https://www.youtube.com/user/{handle}"

    elif platform == "website":
        if handle.startswith("http"):
            return handle
        else:
            return "http://" + handle

    elif platform == "bluesky":
        # Bluesky handles like @user.bsky.social → https://bsky.app/profile/user.bsky.social
        if handle.startswith("http"):
            return handle
        handle = handle.lstrip("@")
        return f"https://bsky.app/profile/{handle}"
    
    elif platform == "instagram":
        if handle.startswith("http"):
            return handle
        handle = handle.lstrip("@")
        return f"https://instagram.com/{handle}"

    return None

def image_exists(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Load JSON data
json_data = []
for filename in os.listdir(directory_path):
    if filename.endswith(".json"):
        with open(os.path.join(directory_path, filename), "r") as f:
            data = json.load(f)
            json_data.append(data)

json_data.sort(key=lambda x: x['authors'][0]['name'])

# Build contributors grid table
header = "| | | |"
first_row = "|:-------------------------:|:-------------------------:|:-------------------------:|"
grid_entries = ""
count = 0

for entry in json_data:
    count += 1
    name = entry['authors'][0]['name']
    photo_url = entry.get('photo_url')
    if not image_exists(photo_url):
        fallback_image = random.choice(fallback_images)
        photo_url = f"https://github.com/cosimameyer/awesome-pyladies-blogs/raw/main/{fallback_images_dir}{fallback_image}"
    blog_url = entry['url']
    
    social_dict = entry['authors'][0].get('social_media', [{}])[0]
    social_icons = build_social_icons(social_dict)

    grid_entry = f'<a href="{blog_url}"><img width="130" alt="Image of {name}" src="{photo_url}"><br></a><span class="caption">{name}</span><br>{social_icons}|'
    if count % 3 == 0:
        grid_entry += '\n|'
    grid_entries += grid_entry


# Build blog list and YouTube list
blogs = []
youtube = []

for entry in json_data:
    entry_type = entry.get("type", "")
    title = entry["title"]
    url = entry["url"]
    authors = ", ".join([a["name"] for a in entry["authors"]])
    line = f"- [{title}]({url}) by {authors}"
    if entry_type == "blog":
        blogs.append(line)
    elif entry_type == "youtube":
        youtube.append(line)

if count % 3 != 0:
    remaining = 3 - (count % 3)
    grid_entries += "| " * remaining + "\n|"

full_table = f"{header}\n{first_row}\n|{grid_entries}"

# Combine everything into README.md content
readme_content = f"""
# Awesome PyLadies' Repository  

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

## What Is This Repository About?  

It provides a curated list of awesome content by PyLadies and collects information to further promote content by [PyLadies on Mastodon](https://botsin.space/@pyladies_bot) 🤖  

To contribute, please see [contributing](CONTRIBUTING.md) ✨  

## List of Contributors as Tiles  

{full_table}

## List of Content  

### Blogs
{os.linesep.join(blogs)}

### YouTube Channels
{os.linesep.join(youtube)}

---

_Last updated on {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}_

## License  

[![CC0](https://upload.wikimedia.org/wikipedia/commons/6/69/CC0_button.svg)](https://creativecommons.org/publicdomain/zero/1.0/)
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)
