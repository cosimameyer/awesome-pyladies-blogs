import os
import json
import random
import requests
from datetime import datetime

fallback_images_dir = "fallback_images/"
fallback_images = [f for f in os.listdir(fallback_images_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
directory_path = "blogs/"

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
        photo_url = f"https://github.com/YOURUSERNAME/YOURREPO/raw/main/{fallback_images_dir}{fallback_image}"
    blog_url = entry['url']

    grid_entry = f'<a href="{blog_url}"><img width="100" alt="Image of {name}" src="{photo_url}"><br></a><span class="caption">{name}</span>|'
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

# Combine everything into README.md content
readme_content = f"""
# Awesome PyLadies' Repository  

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

## What Is This Repository About?  

It provides a curated list of awesome content by PyLadies and collects information to further promote content by [PyLadies on Mastodon](https://botsin.space/@pyladies_bot) 🤖  

To contribute, please see [contributing](CONTRIBUTING.md) ✨  

## List of Contributors as Tiles  

{header}
{first_row}
|
{grid_entries}

## List of Content  

### Blogs
{os.linesep.join(blogs)}

### YouTube Channels
{os.linesep.join(youtube)}

---

_Last updated on {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}_  

## License  

[![CC0](https://upload.wikimedia.org/wikipedia/commons/6/69/CC0_button.svg)](https://creativecommons.org/publicdomain/zero/1.0/)
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)
