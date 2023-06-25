# About 

This repository relies heavily on the [Awesome R-Ladies blogs repository](https://github.com/rladies/awesome-rladies-blogs), to whom all credit goes. I can only repeat their words and their excellent description of how to submit a new entry below:

It has a similar goal and collects PyLadies blogs. This includes those who identify as a minority gender (including but not limited to cis/trans women, trans men, non-binary, genderqueer, & agender). It would be great to have contributions to this list! If you identify with PyLadies and have a blog, please add yourself.

With your submission, you agree that these entries will be used for the [PyLadies' Mastodon bot](https://botsin.space/@pyladies_bot), which will post (new) PyLadies' blog entries to promote the work of PyLadies around the world. 

# Contributing Checklist

 - [ ] The entry will be added to the [blogs/](blogs/) folder.
 - [ ] The filename of the entry ends with `.json'.
 - [ ] The json contains at least 
     - [ ] title (blog title)
     - [ ] type ("blog" or "youtube")
     - [ ] url (blog URL)
     - [ ] rss_feed (if you wish to have your blog posts being promoted by the Mastodon bot; the RSS feed should be for Python-related posts)
     - [ ] rss_feed_youtube (if you wish to have your YouTube channel being promoted by the Mastodon bot; the RSS feed should be for Python-related videos)
     - [ ] photo_url (logo or profile)
     - [ ] language (one of the [ISO 639-1 language codes](https://www.w3schools.com/tags/ref_language_codes.asp))
     - [ ] authors (list of authors)

# Contribution Details

All blogs are listed in the [blogs](blogs/) folder, where each blog is in its own json file. These files will be used to render a table on the upcoming redesigned R-Ladies website. Follow the instructions below to add to the list. If you have any problems, please create an issue so we can help you.

Depending on how you are most comfortable, there are several ways to add new entries. 

## Option 1: Not Too Familiar with JSON/GitHub?

If you're not familiar with JSON, you can [open an issue](https://github.com/cosimameyer/awesome-pyladies-blogs/issues/new/choose) with your blog info and I'll create the JSON for you!

## Option 2: Create a New File

Create a new file in the [blogs/](blogs/) folder by [using this link](https://github.com/cosimameyer/awesome-pyladies-blogs/new/main/?filename=blogs/your-blog-url.com.json&value=%7B%0A%20%20%22title%22%3A%20%22Your%20title%22%2C%20%2F%2Frequired%0A%20%20%22subtitle%22%3A%20%22subtitle%20or%20tagline%22%2C%20%2F%2Foptional%0A%20%20%22type%22%3A%20%22blog%22%2C%20%2F%2Frequired%0A%20%20%22url%22%3A%20%22https%3A%2F%2Fyour_blog.com%22%2C%20%2F%2Frequired%0A%20%20%22photo_url%22%3A%20%22https%3A%2F%2Fyour_blog.com%2Fyour_photo.png%22%2C%20%2F%2Frequired%0A%20%20%22description%22%3A%20%22Short%20description%20of%20what%20you%20blog%20about%22%2C%0A%20%20%22language%22%3A%20%22en%22%2C%20%2F%2Frequired%0A%20%20%22rss_feed%22%3A%20%22%5Burl%5D%2Ffile.xml%22%2C%20%2F%2Frequired%20if%20you%20want%20your%20feed%20to%20be%20promoted%20on%20Mastodon%0A%20%20%22rss_feed_youtube%22%3A%20%22%5Burl%5D%3Dchannel_or_playlist_id%22%2C%20%2F%2Frequired%20if%20you%20want%20your%20feed%20to%20be%20promoted%20on%20Mastodon%0A%20%20%22authors%22%3A%20%5B%20%2F%2Frequired%0A%20%20%20%20%7B%0A%20%20%20%20%20%20%22name%22%3A%20%22Your%20Name%22%2C%20%2F%2Frequired%0A%20%20%20%20%20%20%22social_media%22%3A%20%5B%7B%0A%20%20%20%20%20%20%20%20%20%22twitter%22%3A%20%22username%22%2C%0A%20%20%20%20%20%20%20%20%20%22mastodon%22%3A%20%22%40username%40server.org%22%2C%0A%20%20%20%20%20%20%20%20%20%22github%22%3A%20%22username%22%2C%0A%20%20%20%20%20%20%20%20%20%22instagram%22%3A%20%22username%22%2C%0A%20%20%20%20%20%20%20%20%20%22youtube%22%3A%20%22username%2Fend-url%22%2C%0A%20%20%20%20%20%20%20%20%20%22tiktok%22%3A%20%22username%22%2C%0A%20%20%20%20%20%20%20%20%20%22periscope%22%3A%20%22username%22%2C%0A%20%20%20%20%20%20%20%20%20%22researchgate%22%3A%20%22username%22%2C%0A%20%20%20%20%20%20%20%20%20%22website%22%3A%20%22url%22%2C%0A%20%20%20%20%20%20%20%20%20%22linkedin%22%3A%20%22username%22%2C%0A%20%20%20%20%20%20%20%20%20%22facebook%22%3A%20%22username%22%2C%0A%20%20%20%20%20%20%20%20%20%22orcid%22%3A%20%22member%20number%22%2C%0A%20%20%20%20%20%20%20%20%20%22meetup%22%3A%20%22end-url%22%0A%20%20%20%20%20%20%7D%5D%0A%20%20%20%20%7D%0A%20%20%5D%0A%7D).

This link will fork the repository to your user account, and initiate a new file with some template content in it. After filling the file, please [create a PR to the main branch](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).

### File Name

The name of the file should be the site url (without `www` or `http(s)://` . This way we can ensure each file has a unique name and that duplication does not happen.

### File Content

Using the link above will create a template for you to start with.
Fill inn all the information that is relevant for your blog.
There are several adaptations to an entry you can make that are not highlighted in every entry.
Remove all mentions of `\\required`, these are just for making it clear which information you _must_ provide for the file to be valid.
Any optional field you don't want to add, you may delete entirely.
For instance, if you don't have a subtitle or tagline for your blog, remove the entire line of `"subtite": "subtitle or tagline"` rather than leaving it empty with `"subtite": ""`

#### Photo

The photo url you provide will be displayed as your blogs thumbnail. 
This may be a picture of you, or if you have a logo for your blog/website, it may be best to use this in stead.


#### RSS Feed Website

Please add a content-specific feed in `rss_feed`. Ideally, you have a specific RSS feed for Python-related posts. A title-based RSS feed is fine.

Depending on how your website is set up, the implementation may differ. If you need more input on how to get your RSS, have a look [here](https://zapier.com/blog/how-to-find-rss-feed-url/). If you want to check how your RSS looks like, you can use [simple pie](https://simplepie.org/demo/). We collected a few of the most common approaches below: 

<details><summary>Quarto</summary>
- Change the code in `index.qmd` as (under listing, also described [here](https://quarto.org/docs/websites/website-blog.html#rss-feed)):

  ```
  feed:
    categories: [Python]
    
  ```
  
- Note to new users that the category names will be the names of your category tags used in the blogs (not `posts`, which are the posts folder for Quarto blogs)
- Then provide the RSS feed links as, `[url]/blog/index-r.xml` for R category posts (`[url]/blog/index.xml` will be the RSS feed link for main posts only)

</details>

<details><summary>Distill</summary>
There is currently a [workaround](https://github.com/rladies/awesome-rladies-blogs/pull/54#issuecomment-1501263818) for adding RSS feeds in distill that works as follows:

- In distill, there is a categories folder generated when a post is rendered which gets deleted when the blog is rendered
- Store the folder and add it later because we need a categories folder, containing each specified category with an `index.xml` for each category
</details>

<details><summary>Hugo</summary>

###### Hugo Academic

- Apparently the RSS feed is enabled by default and you can access it by using the field `category` in the YAML of your posts
- Further readings for [Hugo Academic](https://cosimameyer.com/post/adding-your-hugo-academic-blog-to-r-bloggers-and-python-bloggers/)

###### Hugo Portio

- Copy and paste the content of [this file](https://github.com/gohugoio/hugo/blob/master/tpl/tplimpl/embedded/templates/_default/rss.xml) (it’s Hugo’s default RSS settings)
- Store it under `layouts/_default/rss.xml` (if there is no file, you need to create this one).
- Exchange one line. Instead of `<description>{{ .Summary | html }}</description>`, we want `<description>{{ .Content | html }}</description>` (it’s at the very bottom of the file). This way, you RSS feed doesn’t show an excerpt but the full text.
- More about [Hugo Portio](https://cosimameyer.com/post/adding-your-hugo-academic-blog-to-r-bloggers-and-python-bloggers/)
</details>

<details><summary>Medium</summary>
Medium nicely describes on their website how to [get your RSS feed](https://help.medium.com/hc/en-us/articles/214874118-Using-RSS-feeds-of-profiles-publications-and-topics). Unfortunately it's not possible to have a tag specific feed (yet). To keep the bot sorted, please make sure to only post about Python-related topics (= things that could be interesting to the followers of the bot).</details>

#### RSS feed for YouTube videos

The channel or playlist RSS feed will be used to build the RSS feed for your YouTube videos. You first need to get your channel or playlist ID. How to add get them is described [here](https://www.youtube.com/watch?v=vdk8dx08ExU). 
In the last step, you need to assemble them together with the base URL:

- For *channels*: `https://www.youtube.com/feeds/videos.xml?channel_id=` + `CHANNEL_ID` 
- For *playlists*: `https://www.youtube.com/feeds/videos.xml?paylist_id=` + `PLAYLIST_ID` 

#### Authors

The entry may have several authors. This is for blogs where maybe there are several blogging together. If it is a blog that mainly has guest bloggers, its better to list the editors/maintainers of the blog and add "guest bloggers" as authors also.

Adding several authors means duplicating the content between the curlies `{}` in the author section, and adding a comma between each one.

```json
"authors": [
  {
    "name": "Athanasia Mo  Mowinckel",
    "social_media": [{
      "twitter": "DrMowinckels",
      "github": "Athanasiamo"
    }]
  },
  {
    "name": "Mary Johnson",
    "social_media": [{
      "linkedin": "maryj",
      "youtube": "maryj"
    }]
  },
  {
    "name": "Guest bloggers"
  }
]
```

#### Social Media

```json
"twitter": "username"
"mastodon": "@username@instance"
"github": "username"
"instagram": "username"
"youtube": "username/end-url"
"tiktok": "username"
"periscope": "username"
"researchgate": "username"
"website": "url"
"linkedin": "username"
"facebook": "username"
"orcid": "member number"
"meetup": "end-url"
```

#### Language
The language field should be populated with the [ISO 639-1 Language Codes](https://www.w3schools.com/tags/ref_language_codes.asp) of the site content.
Please be thorough when entering this information.

#### Help Needed?

If there is help needed, feel free to reach out to [me directly](mailto:contact@cosimameyer.com).
