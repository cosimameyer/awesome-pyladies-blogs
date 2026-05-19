# Adding Yourself to the People Directory

This folder is for PyLadies members who want to appear on the website but don't have content (blog, YouTube, package) to add yet — or simply want to be listed alongside their community.

## How to add yourself

1. Create a new file named `<your-name>.json` (e.g., `jane_doe.json`) in this folder.
2. Use the format from `TEMPLATE.json.example` as a starting point.
3. Fill in your name and any social media handles you'd like to share — all fields are optional except `name`.

```json
{
  "name": "Jane Doe",
  "photo_url": "https://github.com/janedoe.png",
  "chapter": "",
  "social_media": [
    {
      "website":   "https://janedoe.com",
      "github":    "janedoe",
      "linkedin":  "janedoe",
      "mastodon":  "@jane@fosstodon.org",
      "bluesky":   "@janedoe.bsky.social",
      "instagram": "",
      "youtube":   "",
      "twitter":   ""
    }
  ]
}
```

4. Open a pull request — that's it!

## Chapter organizers

If you're a PyLadies chapter organizer, add your chapter name to the `"chapter"` field:

```json
{
  "name": "Jane Doe",
  "chapter": "PyLadies Berlin",
  ...
}
```

This will add a **Chapter Organizer** tag to your card and display your chapter name below your name.  
Leave `"chapter"` empty (or omit it) if you're not an organizer.

## Notes

- `photo_url` should be a publicly accessible image.  
  GitHub avatar: `https://github.com/<username>.png`
- Leave any social fields empty (`""`) that you don't want to share.
- If you have content (blog, package, etc.) in `data/content/` or `data/packages/`, you don't need an entry here — you're already in the directory.
