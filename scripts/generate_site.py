"""
Generate docs/index.html from data/ JSON files.
Reads the same data as generate_readme.py; outputs a static GitHub Pages site.
"""
import json
import os
import re
import urllib.parse
from datetime import datetime, timezone
from html import escape

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR  = os.path.join(ROOT, "data", "content")
PACKAGES_DIR = os.path.join(ROOT, "data", "packages")
SOFTWARE_DIR = os.path.join(ROOT, "data", "software")
OUT_FILE     = os.path.join(ROOT, "docs", "index.html")

# ── Inline SVG paths for social platforms ──────────────────────────────────────
SVG_PATHS = {
    "github":    "M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z",
    "linkedin":  "M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z",
    "mastodon":  "M23.268 5.313c-.35-2.578-2.617-4.61-5.304-5.004C17.51.242 15.792 0 11.813 0h-.03c-3.98 0-4.835.242-5.288.309C3.882.692 1.496 2.518.917 5.127.64 6.412.61 7.837.661 9.143c.074 1.874.088 3.745.26 5.611.118 1.24.325 2.47.62 3.68.55 2.237 2.777 4.098 4.96 4.857 2.336.792 4.849.923 7.256.38.265-.061.527-.132.786-.213.585-.184 1.27-.39 1.774-.753a.057.057 0 0 0 .023-.043v-1.809a.052.052 0 0 0-.02-.041.053.053 0 0 0-.046-.01 20.282 20.282 0 0 1-4.709.545c-2.73 0-3.463-1.284-3.674-1.818a5.593 5.593 0 0 1-.319-1.433.053.053 0 0 1 .066-.054c1.517.363 3.072.546 4.632.546.376 0 .75 0 1.125-.01 1.57-.044 3.224-.124 4.768-.422.038-.008.077-.015.11-.024 2.435-.464 4.753-1.92 4.989-5.604.008-.145.03-1.52.03-1.67.002-.512.167-3.63-.024-5.545zm-3.748 9.195h-2.561V8.29c0-1.309-.55-1.976-1.67-1.976-1.23 0-1.846.79-1.846 2.35v3.403h-2.546V8.663c0-1.56-.617-2.35-1.848-2.35-1.112 0-1.668.668-1.67 1.977v6.218H4.822V8.102c0-1.31.337-2.35 1.011-3.12.696-.77 1.608-1.164 2.74-1.164 1.311 0 2.302.5 2.962 1.498l.638 1.06.638-1.06c.66-.999 1.65-1.498 2.96-1.498 1.13 0 2.043.395 2.74 1.164.675.77 1.012 1.81 1.012 3.12z",
    "bluesky":   "M12 10.8c-1.087-2.114-4.046-6.053-6.798-7.995C2.566.944 1.561 1.266.902 1.565.139 1.908 0 3.08 0 3.768c0 .69.378 5.65.624 6.479.815 2.736 3.713 3.66 6.383 3.364.136-.02.275-.039.415-.056-.138.022-.276.04-.415.056-3.912.58-7.387 2.005-2.83 7.078 5.013 5.19 6.87-1.113 7.823-4.308.953 3.195 2.05 9.271 7.733 4.308 4.267-4.308 1.172-6.498-2.74-7.078a8.741 8.741 0 0 1-.415-.056c.14.017.279.036.415.056 2.67.297 5.568-.628 6.383-3.364.246-.828.624-5.79.624-6.478 0-.69-.139-1.861-.902-2.204-.659-.3-1.664-.62-4.3 1.24C16.046 4.748 13.087 8.687 12 10.8z",
    "youtube":   "M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z",
    "website":   "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z",
    "twitter":   "M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 6.231H2.744l7.737-8.835L1.254 2.25H8.08l4.259 5.63L18.244 2.25zm-1.161 17.52h1.833L7.084 4.126H5.117L17.083 19.77z",
    "instagram": "M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838a6.162 6.162 0 1 0 0 12.324 6.162 6.162 0 0 0 0-12.324zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.406-11.845a1.44 1.44 0 1 0 0 2.881 1.44 1.44 0 0 0 0-2.881z",
    # Archive/package box — represents PyPI (a package index)
    "pypi": "M1.5 9.75A.75.75 0 0 1 2.25 9h19.5a.75.75 0 0 1 0 1.5H2.25a.75.75 0 0 1-.75-.75zM2.25 4.5A2.25 2.25 0 0 0 0 6.75v.75c0 .414.336.75.75.75h22.5A.75.75 0 0 0 24 7.5v-.75A2.25 2.25 0 0 0 21.75 4.5H2.25zm-.75 6.75v7.5A2.25 2.25 0 0 0 3.75 21h16.5A2.25 2.25 0 0 0 22.5 18.75v-7.5H1.5zm9 2.25h3a.75.75 0 0 1 0 1.5h-3a.75.75 0 0 1 0-1.5z",
}

PLATFORM_ORDER = ["website", "github", "mastodon", "bluesky", "linkedin", "youtube", "twitter", "instagram"]


# ── Helpers ────────────────────────────────────────────────────────────────────

def load_json_files(path):
    entries = []
    if not os.path.exists(path):
        return entries
    for filename in sorted(os.listdir(path)):
        if filename.endswith(".json"):
            with open(os.path.join(path, filename), encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                entries.extend(data)
            else:
                entries.append(data)
    return entries


def build_social_url(platform, handle):
    if not handle:
        return None
    handle = handle.strip()
    handle = urllib.parse.unquote(handle)
    if platform not in ("mastodon", "bluesky"):
        handle = handle.lstrip("@")
    if platform == "twitter":
        return handle if handle.startswith("http") else f"https://twitter.com/{handle}"
    if platform == "mastodon":
        if handle.startswith("http"):
            return handle
        parts = handle.lstrip("@").split("@")
        return f"https://{parts[1]}/@{parts[0]}" if len(parts) == 2 else None
    if platform == "linkedin":
        return handle if handle.startswith("http") else f"https://www.linkedin.com/in/{handle.rstrip('/')}"
    if platform == "github":
        return handle if handle.startswith("http") else f"https://github.com/{handle}"
    if platform == "youtube":
        if handle.startswith("http"):
            return handle
        return f"https://www.youtube.com/{handle}" if handle.startswith("@") else f"https://www.youtube.com/user/{handle}"
    if platform == "website":
        return handle if handle.startswith("http") else f"http://{handle}"
    if platform == "bluesky":
        return handle if handle.startswith("http") else f"https://bsky.app/profile/{handle.lstrip('@')}"
    if platform == "instagram":
        return handle if handle.startswith("http") else f"https://instagram.com/{handle.lstrip('@')}"
    return None


def social_icon_svg(platform, size=14):
    path = SVG_PATHS.get(platform)
    if not path:
        return ""
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" '
        f'fill="currentColor" aria-hidden="true"><path d="{path}"/></svg>'
    )


def render_social_icons_html(social_dict, size=14):
    icons = []
    for platform in PLATFORM_ORDER:
        handle = social_dict.get(platform)
        url = build_social_url(platform, handle)
        if not url:
            continue
        svg = social_icon_svg(platform, size)
        if svg:
            icons.append(f'<a href="{escape(url)}" target="_blank" rel="noopener" title="{platform}" class="social-icon" onclick="event.stopPropagation()">{svg}</a>')
    return "\n".join(icons)


FALLBACK_IMAGES = [
    "https://github.com/cosimameyer/awesome-pyladies-creations/raw/main/img/fallback_images/pyladies_bot.png",
    "https://github.com/cosimameyer/awesome-pyladies-creations/raw/main/img/fallback_images/pyladies_small.png",
]

def avatar_fallback(name):
    # stable hash so adding more images to FALLBACK_IMAGES rotates evenly
    import hashlib
    idx = int(hashlib.md5(name.encode()).hexdigest(), 16) % len(FALLBACK_IMAGES)
    return FALLBACK_IMAGES[idx]


TAG_CLASS = {
    "blog": "tag-blog", "youtube": "tag-youtube",
    "podcast": "tag-podcast", "package": "tag-package",
}
TYPE_LABEL = {
    "blog": "Blog", "youtube": "YouTube",
    "podcast": "Podcast", "package": "Package",
}
BADGE_CLASS = {
    "blog": "badge-blog", "youtube": "badge-youtube", "podcast": "badge-podcast",
}


def badge_class(content_type):
    return BADGE_CLASS.get(content_type, "badge-blog")


def type_label(content_type):
    return TYPE_LABEL.get(content_type, content_type.title())


# ── Person registry ────────────────────────────────────────────────────────────

class PersonProfile:
    def __init__(self):
        self.types    = []   # ordered, deduplicated list of type strings
        self.social   = {}   # merged {platform: handle}, first value wins per platform
        self.url      = ""   # primary link (first content entry > first package)
        self.photo_url = ""  # first non-empty photo URL


def build_person_registry(content_data, all_package_data):
    """
    Walk every content entry and every package, collecting each person's
    types, social handles, primary URL, and photo. Handles appearing in
    multiple entries get their types unioned and their social dicts merged
    (first non-empty value per platform wins, so explicit data is never
    overwritten by a sparser duplicate entry).
    """
    registry = {}

    def merge_social(profile, social_media_list):
        for sm in social_media_list:
            for platform, handle in sm.items():
                if handle and platform not in profile.social:
                    profile.social[platform] = handle

    for entry in content_data:
        ctype = entry.get("type", "blog")
        for author in entry.get("authors", []):
            name = author.get("name", "")
            if not name or author.get("pyladies") is False:
                continue
            if name not in registry:
                registry[name] = PersonProfile()
            p = registry[name]
            if ctype not in p.types:
                p.types.append(ctype)
            if not p.url:
                p.url = entry.get("url", "#")
            if not p.photo_url:
                p.photo_url = entry.get("photo_url", "")
            merge_social(p, author.get("social_media", []))

    for pkg in all_package_data:
        for m in pkg.get("maintainers", []):
            name = m.get("name", "")
            if not name or m.get("pyladies") is False:
                continue
            if name not in registry:
                registry[name] = PersonProfile()
            p = registry[name]
            if "package" not in p.types:
                p.types.append("package")
            if not p.url:
                p.url = (pkg.get("pypi_url") or pkg.get("repo_url")
                         or pkg.get("website_url") or "#")
            merge_social(p, m.get("social_media", []))

    return registry


# ── Card renderers ─────────────────────────────────────────────────────────────

def render_person_card(name, profile):
    fallback = avatar_fallback(name)
    photo_src = escape(profile.photo_url) if profile.photo_url else fallback
    social_html = render_social_icons_html(profile.social)
    data_types = " ".join(profile.types)
    tags_html = "".join(
        f'<span class="person-tag {TAG_CLASS.get(t, "tag-blog")}">{TYPE_LABEL.get(t, t.title())}</span>'
        for t in profile.types
    )
    url = escape(profile.url)
    search_text = escape(name.lower())
    # div wrapper avoids invalid <a> inside <a> (social icon links inside card link)
    return f"""
        <div class="person-card" data-type="{escape(data_types)}" data-search="{search_text}"
             onclick="window.open('{url}','_blank','noopener')" role="link" tabindex="0"
             onkeydown="if(event.key==='Enter')window.open('{url}','_blank','noopener')">
          <img class="person-avatar" src="{photo_src}" alt="{escape(name)}" loading="lazy"
               onerror="this.src='{fallback}'"/>
          <div class="person-info">
            <h3 class="person-name">{escape(name)}</h3>
            <div class="person-tags">{tags_html}</div>
          </div>
          <div class="person-social">{social_html}</div>
        </div>"""


def render_content_card(entry):
    title       = escape(entry.get("title", "Untitled"))
    url         = escape(entry.get("url", "#"))
    raw_photo   = entry.get("photo_url", "")
    ctype       = entry.get("type", "blog").lower()
    badge       = badge_class(ctype)
    label       = type_label(ctype)
    description = escape(entry.get("description") or entry.get("subtitle") or "")
    language    = escape((entry.get("language") or "en").upper())
    raw_title   = entry.get("title", "")
    raw_desc    = entry.get("description") or entry.get("subtitle") or ""
    authors     = entry.get("authors", [])
    author_names = ", ".join(a.get("name", "") for a in authors if a.get("name"))
    author_html = f'<p class="content-author">by {escape(author_names)}</p>' if author_names else ""
    search_text = escape(f"{raw_title} {raw_desc} {author_names}".lower())
    fallback    = avatar_fallback(raw_title)
    photo_src   = escape(raw_photo) if raw_photo else fallback
    return f"""
        <a class="content-card" href="{url}" target="_blank" rel="noopener"
           data-type="{ctype}" data-search="{search_text}">
          <div class="content-card-header">
            <img class="content-thumb" src="{photo_src}" alt="" loading="lazy"
                 onerror="this.src='{fallback}'"/>
            <span class="content-type-badge {badge}">{label}</span>
          </div>
          <div class="content-card-body">
            <h3>{title}</h3>
            {author_html}
            <p>{description}</p>
          </div>
          <div class="content-card-footer">
            <span class="lang-badge">{language}</span>
            <span class="arrow">→</span>
          </div>
        </a>"""


def render_package_card(pkg):
    name        = pkg.get("name", "")
    title       = escape(pkg.get("title") or name)
    description = escape(pkg.get("description", ""))
    pypi_url    = escape(pkg.get("pypi_url", "#"))
    repo_url    = escape(pkg.get("repo_url", "#"))
    docs_url    = pkg.get("docs_url") or ""
    logo_url    = pkg.get("logo_url") or ""
    maintainers = pkg.get("maintainers", [])
    maintainer_names = ", ".join(m.get("name", "") for m in maintainers[:3])
    if len(maintainers) > 3:
        maintainer_names += f" + {len(maintainers) - 3} others"
    maintainer_names = escape(maintainer_names)

    logo_html = (
        f'<img class="package-logo" src="{escape(logo_url)}" alt="{title} logo" loading="lazy" onerror="this.style.display=\'none\'"/>'
        if logo_url else
        f'<div class="package-logo-placeholder">{escape(name[:2].upper())}</div>'
    )

    # Suppress docs link only when it points to the same URL as pypi_url
    _pypi_url = (pkg.get("pypi_url") or "").rstrip("/")
    _docs_url = docs_url.rstrip("/")
    docs_link = (
        f'<a href="{escape(docs_url)}" class="pkg-link" title="Docs" target="_blank" rel="noopener">'
        f'{social_icon_svg("website")}</a>'
        if docs_url and _docs_url != _pypi_url else ""
    )

    raw_name  = pkg.get("title") or pkg.get("name", "")
    raw_desc  = pkg.get("description", "")
    raw_maint = " ".join(m.get("name", "") for m in maintainers)
    search_text = escape(f"{raw_name} {raw_desc} {raw_maint}".lower())
    # div wrapper avoids invalid <a> inside <a> (pkg-link anchors inside card link)
    return f"""
        <div class="package-card" data-search="{search_text}"
             onclick="window.open('{pypi_url}','_blank','noopener')"
             role="link" tabindex="0"
             onkeydown="if(event.key==='Enter')window.open('{pypi_url}','_blank','noopener')">
          <div class="package-card-top">
            {logo_html}
            <div class="package-links">
              {docs_link}
              <a href="{repo_url}" class="pkg-link" title="GitHub" target="_blank" rel="noopener"
                 onclick="event.stopPropagation()">{social_icon_svg("github")}</a>
              <a href="{pypi_url}" class="pkg-link" title="PyPI" target="_blank" rel="noopener"
                 onclick="event.stopPropagation()">{social_icon_svg("pypi")}</a>
            </div>
          </div>
          <h3 class="package-name">{title}</h3>
          <p class="package-desc">{description}</p>
          <div class="package-maintainers">
            <span class="maintainer-label">Maintained by</span>
            <span class="maintainers">{maintainer_names}</span>
          </div>
        </div>"""


# ── Counts & stats ─────────────────────────────────────────────────────────────

FEATURED_PEOPLE   = 10
FEATURED_CONTENT  = 9
FEATURED_PACKAGES = 6


def count_unique_people(content_data, package_data):
    names = set()
    for e in content_data:
        for a in e.get("authors", []):
            names.add(a.get("name", ""))
    for p in package_data:
        for m in p.get("maintainers", []):
            names.add(m.get("name", ""))
    names.discard("")
    return len(names)


def build_stats_html(n_people, n_blogs, n_youtube, n_podcasts, n_packages):
    items = [
        (n_people,   "Creators"),
        (n_blogs,    "Blogs"),
        (n_youtube,  "YouTube Channels"),
        (n_podcasts, "Podcasts"),
        (n_packages, "Packages"),
    ]
    parts = []
    for num, label in items:
        if num == 0:
            continue
        if parts:
            parts.append('<div class="stat-divider"></div>')
        parts.append(f'<div class="stat"><span class="stat-num">{num}</span><span class="stat-label">{label}</span></div>')
    return "".join(parts)


# ── Wordmark ────────────────────────────────────────────────────────────────────

_WORDMARK_PATH = os.path.join(ROOT, "docs", "assets", "pyladies_wordmark.svg")

def hero_wordmark_html(color="#EE264D"):
    """
    Read the locally stored PyLadies wordmark SVG, replace all fills with the
    brand color, and return it as an inline SVG with positioning styles applied.
    Falls back to an <img> tag if the file is missing.
    """
    if not os.path.exists(_WORDMARK_PATH):
        return '<img src="assets/pyladies_wordmark.svg" alt="PyLadies" class="hero-wordmark" />'

    with open(_WORDMARK_PATH, encoding="utf-8") as f:
        svg = f.read()

    # Replace only non-black fills with the brand red (preserves black outline/shadow)
    def recolor(m):
        h = m.group(1).lstrip('#')
        h = (h[0]*2 + h[1]*2 + h[2]*2) if len(h) == 3 else h  # expand shorthand
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return m.group(0) if r < 40 and g < 40 and b < 40 else f'fill:{color}'
    svg = re.sub(r'fill:(#[0-9a-fA-F]{3,6})', recolor, svg)

    # Add viewBox from the existing width/height so CSS scaling preserves aspect ratio
    w_m = re.search(r'\bwidth="([^"]+)"', svg)
    h_m = re.search(r'\bheight="([^"]+)"', svg)
    if w_m and h_m and 'viewBox' not in svg:
        svg = re.sub(r'(<svg\b)', rf'\1 viewBox="0 0 {w_m.group(1)} {h_m.group(1)}"', svg, count=1)

    # Remove presentational width/height so our CSS height+auto-width scales correctly
    svg = re.sub(r'\s*\bwidth="[^"]*"', '', svg, count=1)
    svg = re.sub(r'\s*\bheight="[^"]*"', '', svg, count=1)

    # Positioning styles to inject onto the root <svg> element
    our_style = (
        "height:130px;width:auto;display:block;"
        "margin:-28px auto 12px;"
        "transform:rotate(-15deg);"
        "transform-origin:center bottom;"
    )
    # Merge with any existing style attribute rather than adding a duplicate
    if re.search(r'<svg\b[^>]*style=', svg, re.DOTALL):
        svg = re.sub(r'(style=")([^"]*)"', lambda m: f'style="{our_style}{m.group(2)}"', svg, count=1)
    else:
        svg = re.sub(r'(<svg\b)', rf'\1 style="{our_style}"', svg, count=1)
    return svg


# ── Shared page chrome ─────────────────────────────────────────────────────────

def nav_html(css_path="assets/style.css", home="index.html", active=""):
    gh_svg = social_icon_svg("github", 16)
    def nav_link(href, label, key):
        cls = ' class="nav-active"' if active == key else ""
        return f'<li><a href="{href}"{cls}>{label}</a></li>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="stylesheet" href="{css_path}" />
</head>
<body>
  <header class="site-header">
    <nav class="nav-inner">
      <a href="{home}" class="nav-logo">
        <img src="assets/pylady_geek.png"
             alt="PyLadies geek logo" class="nav-geek-logo" />
        <span>Awesome PyLadies</span>
      </a>
      <ul class="nav-links">
        {nav_link("people.html", "People", "people")}
        {nav_link("content.html", "Content", "content")}
        {nav_link("packages.html", "Packages", "packages")}
        {nav_link("about.html", "About", "about")}
      </ul>
      <a class="nav-cta" href="https://github.com/cosimameyer/awesome-pyladies-creations" target="_blank" rel="noopener">
        {gh_svg} Contribute
      </a>
    </nav>
  </header>"""


def footer_html(updated):
    return f"""
  <section class="cta-section">
    <div class="container cta-inner">
      <h2>Are you a PyLady?</h2>
      <p>Add your blog, package, YouTube channel, or other work to the directory — it takes just one JSON file.</p>
      <a href="https://github.com/cosimameyer/awesome-pyladies-creations/blob/main/CONTRIBUTING.md"
         class="btn-primary" target="_blank" rel="noopener">Read the Contributing Guide</a>
    </div>
  </section>
  <footer class="site-footer">
    <div class="container footer-inner">
      <span>Built from <a href="https://github.com/cosimameyer/awesome-pyladies-creations" target="_blank" rel="noopener">awesome-pyladies-creations</a> · CC0 · updated {updated}</span>
      <span class="footer-pyladies">Part of the <a href="https://pyladies.com" target="_blank" rel="noopener">PyLadies</a> community</span>
    </div>
  </footer>
</body>
</html>"""


def search_bar_html(placeholder="Search…"):
    return f"""
      <div class="search-wrap">
        <input class="search-input" type="search" placeholder="{placeholder}" aria-label="{placeholder}" />
      </div>"""


# ── Shared JS blocks ────────────────────────────────────────────────────────────

JS_PEOPLE = """
  <script>
    function applyPeopleFilters() {
      const q = (document.querySelector('.search-input')?.value || '').toLowerCase();
      const f = document.querySelector('.filter-btn.active')?.dataset.filter || 'all';
      document.querySelectorAll('.person-card').forEach(card => {
        const typeMatch = f === 'all' || card.dataset.type.split(' ').includes(f);
        const textMatch = !q || card.dataset.search.includes(q);
        card.style.display = (typeMatch && textMatch) ? '' : 'none';
      });
    }
    document.querySelectorAll('.filter-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        applyPeopleFilters();
      });
    });
    document.querySelector('.search-input')?.addEventListener('input', applyPeopleFilters);
  </script>"""

JS_CONTENT = """
  <script>
    function applyContentFilters() {
      const q = (document.querySelector('.search-input')?.value || '').toLowerCase();
      const f = document.querySelector('.tab.active')?.dataset.tab || 'all';
      document.querySelectorAll('.content-card').forEach(card => {
        const typeMatch = f === 'all' || card.dataset.type === f;
        const textMatch = !q || card.dataset.search.includes(q);
        card.style.display = (typeMatch && textMatch) ? '' : 'none';
      });
    }
    document.querySelectorAll('.tab').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.tab').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        applyContentFilters();
      });
    });
    document.querySelector('.search-input')?.addEventListener('input', applyContentFilters);
  </script>"""

JS_PACKAGES = """
  <script>
    document.querySelector('.search-input')?.addEventListener('input', function() {
      const q = this.value.toLowerCase();
      document.querySelectorAll('.package-card').forEach(card => {
        card.style.display = (!q || card.dataset.search.includes(q)) ? '' : 'none';
      });
    });
  </script>"""


# ── Section builders ────────────────────────────────────────────────────────────

def section_people_full(people_cards, n_podcasts):
    podcast_btn = "<button class='filter-btn' data-filter='podcast'>Podcasters</button>" if n_podcasts else ""
    return f"""
  <section class="section" id="people">
    <div class="container">
      <div class="section-header">
        <div>
          <p class="section-label">Community</p>
          <h2 class="section-title">The People</h2>
        </div>
        <p class="section-desc">PyLadies members sharing knowledge, code, and passion with the world.</p>
      </div>
      {search_bar_html("Search by name…")}
      <div class="filter-bar">
        <button class="filter-btn active" data-filter="all">All</button>
        <button class="filter-btn" data-filter="blog">Bloggers</button>
        <button class="filter-btn" data-filter="youtube">YouTubers</button>
        {podcast_btn}
        <button class="filter-btn" data-filter="package">Package Maintainers</button>
      </div>
      <div class="people-grid">{"".join(people_cards)}</div>
    </div>
  </section>"""


def section_content_full(content_cards, n_podcasts):
    podcast_tab = "<button class='tab' data-tab='podcast'>Podcasts</button>" if n_podcasts else ""
    return f"""
  <section class="section section-alt" id="content">
    <div class="container">
      <div class="section-header">
        <div>
          <p class="section-label">Reading &amp; Watching</p>
          <h2 class="section-title">Content</h2>
        </div>
        <p class="section-desc">Blogs, YouTube channels, and podcasts produced by PyLadies members.</p>
      </div>
      {search_bar_html("Search blogs and channels…")}
      <div class="tabs">
        <button class="tab active" data-tab="all">All</button>
        <button class="tab" data-tab="blog">Blogs</button>
        <button class="tab" data-tab="youtube">YouTube</button>
        {podcast_tab}
      </div>
      <div class="content-grid">{"".join(content_cards)}</div>
    </div>
  </section>"""


def section_packages_full(package_cards):
    return f"""
  <section class="section" id="packages">
    <div class="container">
      <div class="section-header">
        <div>
          <p class="section-label">Open Source</p>
          <h2 class="section-title">Packages &amp; Tools</h2>
        </div>
        <p class="section-desc">Python packages and software built and maintained by PyLadies members.</p>
      </div>
      {search_bar_html("Search packages…")}
      <div class="packages-grid">{"".join(package_cards)}</div>
    </div>
  </section>"""


def section_featured(label, title, desc, cards, grid_class, view_all_href, section_id, alt_bg=False):
    bg = " section-alt" if alt_bg else ""
    return f"""
  <section class="section{bg}" id="{section_id}">
    <div class="container">
      <div class="section-header">
        <div>
          <p class="section-label">{label}</p>
          <h2 class="section-title">{title}</h2>
        </div>
        <p class="section-desc">{desc}</p>
      </div>
      <div class="{grid_class}">{"".join(cards)}</div>
      <div class="view-all-wrap">
        <a href="{view_all_href}" class="view-all-btn">View all →</a>
      </div>
    </div>
  </section>"""


def section_about():
    return """
  <section class="section">
    <div class="container about-wrap">

      <div class="section-header">
        <div>
          <p class="section-label">About</p>
          <h2 class="section-title">About This Directory</h2>
        </div>
      </div>

      <div class="about-body">
        <h3>Where does this content come from?</h3>
        <p>
          Everything featured here is sourced from the open-source repository
          <a href="https://github.com/cosimameyer/awesome-pyladies-creations"
             target="_blank" rel="noopener">awesome-pyladies-creations</a> on GitHub —
          a community-curated list of blogs, YouTube channels, podcasts, and Python packages
          created by PyLadies members. The site is rebuilt automatically whenever new entries
          are added to the repository.
        </p>

        <h3>Want to be added?</h3>
        <p>
          If you're a PyLadies member and would like your work featured, contributions are
          very welcome! Check out the
          <a href="https://github.com/cosimameyer/awesome-pyladies-creations/blob/main/CONTRIBUTING.md"
             target="_blank" rel="noopener">contributing guide</a> — it only takes one JSON file.
        </p>

        <h3>Don't want to be featured?</h3>
        <p>
          If you'd prefer your content or profile not to appear on this site, please don't
          hesitate to reach out. You can
          <a href="https://github.com/cosimameyer/awesome-pyladies-creations/issues/new"
             target="_blank" rel="noopener">open an issue on GitHub</a>
          or contact me directly via
          <a href="https://cosimameyer.com" target="_blank" rel="noopener">cosimameyer.com</a>
          and I'll take care of it as soon as possible.
        </p>
      </div>

    </div>
  </section>"""


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    content_data  = load_json_files(CONTENT_DIR)
    package_data  = load_json_files(PACKAGES_DIR)
    software_data = load_json_files(SOFTWARE_DIR)

    content_data.sort(key=lambda x: x.get("authors", [{}])[0].get("name", ""))
    package_data.sort(key=lambda x: x.get("name", ""))
    software_data.sort(key=lambda x: x.get("name", ""))

    all_data = package_data + software_data

    n_blogs    = sum(1 for e in content_data if e.get("type") == "blog")
    n_youtube  = sum(1 for e in content_data if e.get("type") == "youtube")
    n_podcasts = sum(1 for e in content_data if e.get("type") == "podcast")
    n_packages = len(all_data)

    registry = build_person_registry(content_data, all_data)
    n_people   = len(registry)  # count after pyladies:false filter is applied
    registry_sorted = sorted(registry.items(), key=lambda kv: kv[0])

    all_people_cards  = [render_person_card(n, p) for n, p in registry_sorted]
    all_content_cards = [render_content_card(e) for e in content_data]
    all_package_cards = [render_package_card(p) for p in all_data]

    # Pass all cards — JS on the index page will randomly pick N to show on each load

    stats = build_stats_html(n_people, n_blogs, n_youtube, n_podcasts, n_packages)
    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    gh_svg = social_icon_svg("github", 16)

    os.makedirs(os.path.join(ROOT, "docs"), exist_ok=True)

    # ── index.html ────────────────────────────────────────────────────────────
    index = nav_html(active="") + f"""
  <section class="hero">
    <div class="hero-inner">
      <div class="hero-badge">Open Source · Community · Python</div>
      <h1>Awesome</h1>
      {hero_wordmark_html()}
      <p class="hero-sub">A curated directory of content, tools, and packages created by PyLadies — celebrating the voices and work of our community members in the Python ecosystem.</p>
      <div class="hero-stats">{stats}</div>
      <div class="hero-actions">
        <a href="people.html" class="btn-primary">Explore the Directory</a>
        <a href="https://github.com/cosimameyer/awesome-pyladies-creations/blob/main/CONTRIBUTING.md"
           class="btn-ghost" target="_blank" rel="noopener">Add Your Work</a>
      </div>
    </div>
    <div class="hero-grid-bg" aria-hidden="true"><div class="dot-grid"></div></div>
  </section>

  {section_featured("Community", "The People", "PyLadies members sharing knowledge, code, and passion with the world.",
      all_people_cards, "people-grid", "people.html", "featured-people", alt_bg=False)}

  {section_featured("Reading &amp; Watching", "Content", "Blogs, YouTube channels, and podcasts produced by PyLadies members.",
      all_content_cards, "content-grid", "content.html", "featured-content", alt_bg=True)}

  {section_featured("Open Source", "Packages &amp; Tools", "Python packages and software built and maintained by PyLadies members.",
      all_package_cards, "packages-grid", "packages.html", "featured-packages", alt_bg=False)}
""" + footer_html(updated) + f"""
  <script>
    window.addEventListener('DOMContentLoaded', function() {{
      [
        ['#featured-people .person-card',   {FEATURED_PEOPLE}],
        ['#featured-content .content-card', {FEATURED_CONTENT}],
        ['#featured-packages .package-card',{FEATURED_PACKAGES}]
      ].forEach(function(pair) {{
        var sel = pair[0], n = pair[1];
        var cards = Array.from(document.querySelectorAll(sel));
        cards.forEach(function(c) {{ c.style.display = 'none'; }});
        cards.sort(function() {{ return Math.random() - 0.5; }})
             .slice(0, n)
             .forEach(function(c) {{ c.style.display = ''; }});
      }});
    }});
  </script>"""

    with open(os.path.join(ROOT, "docs", "index.html"), "w", encoding="utf-8") as f:
        f.write(index)

    # ── people.html ───────────────────────────────────────────────────────────
    people_page = nav_html(home="index.html", active="people") + \
        section_people_full(all_people_cards, n_podcasts) + \
        footer_html(updated) + JS_PEOPLE

    with open(os.path.join(ROOT, "docs", "people.html"), "w", encoding="utf-8") as f:
        f.write(people_page)

    # ── content.html ──────────────────────────────────────────────────────────
    content_page = nav_html(home="index.html", active="content") + \
        section_content_full(all_content_cards, n_podcasts) + \
        footer_html(updated) + JS_CONTENT

    with open(os.path.join(ROOT, "docs", "content.html"), "w", encoding="utf-8") as f:
        f.write(content_page)

    # ── packages.html ─────────────────────────────────────────────────────────
    packages_page = nav_html(home="index.html", active="packages") + \
        section_packages_full(all_package_cards) + \
        footer_html(updated) + JS_PACKAGES

    with open(os.path.join(ROOT, "docs", "packages.html"), "w", encoding="utf-8") as f:
        f.write(packages_page)

    # ── about.html ────────────────────────────────────────────────────────────
    about_page = nav_html(home="index.html", active="about") + \
        section_about() + footer_html(updated)

    with open(os.path.join(ROOT, "docs", "about.html"), "w", encoding="utf-8") as f:
        f.write(about_page)

    print(
        f"Generated index.html (shows {FEATURED_PEOPLE}/{len(all_people_cards)} people, "
        f"{FEATURED_CONTENT}/{len(all_content_cards)} content, "
        f"{FEATURED_PACKAGES}/{len(all_package_cards)} packages randomly) + "
        f"people.html · content.html · packages.html"
    )


if __name__ == "__main__":
    main()
