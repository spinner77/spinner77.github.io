# Beechview Crafts website

A Jekyll site for GitHub Pages. GitHub builds it for you, so there's nothing to install.

## Putting it live (first time)

1. On GitHub, create a new **public** repository.
   - Call it `YOUR-USERNAME.github.io` for an address like `https://your-username.github.io/`, or
   - call it something like `beechview-crafts` for `https://your-username.github.io/beechview-crafts/`.
2. Upload all these files to it (Add file → Upload files, or push with git).
3. If you used a name like `beechview-crafts`, open `_config.yml` and set
   `baseurl: "/beechview-crafts"`. If you used `YOUR-USERNAME.github.io`, leave it as `""`.
4. Go to **Settings → Pages**. Under "Build and deployment", choose
   **Deploy from a branch**, branch **main**, folder **/ (root)**, and Save.
5. Wait a minute or two, then refresh the Pages settings to see the link.

## Everyday jobs

### Write a blog post
Add a file to `_posts/` named `YYYY-MM-DD-short-title.md`, starting with:

```
---
title: Your post title
summary: One line shown in the post list.
tags: [plants, folklore]
---

Your post here, in Markdown.

## Unravelling

Your closing question.
```

Posts dated in the future don't appear until a rebuild after that date
(any commit triggers a rebuild).

### Add something to Made by Hand
Edit `_data/makes.yml`. Copy an entry, change the details, and put the newest at the top.
For a photo, add it to `assets/images/makes/` and set `image: your-photo.jpg` and a short `alt` description.
Keep photos under about 300 KB (resize to about 1200 px wide).

### Add a colour to Colours of the Plot
Edit `_data/colours.yml`. Copy the first entry, give it the next number, and set `status: done`.
Entries with `status: to try` show as empty swatches.

### Contact and social links
Fill in `email`, `instagram` and `youtube` in `_config.yml`. Empty ones stay hidden.

### Change the colours or fonts
The colours are the first few lines of `assets/css/style.css`.

## Previewing on your own computer (optional)
Install Ruby, then run `bundle install` and `bundle exec jekyll serve`, and open http://localhost:4000.
