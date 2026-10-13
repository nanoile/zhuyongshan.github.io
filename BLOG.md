# Publishing a blog post

The blog is a static archive with real article URLs. Posts are stored in `content/posts.json`; each entry points to an HTML body in `content/`.

1. Add a body file, for example `content/my-research-note.html`. Write the article body using `<p>`, `<h2>`, `<ul>`, `<blockquote>`, `<pre><code>`, images and other semantic HTML. Content files are trusted local source.
2. Add an entry to `content/posts.json`:

```json
{
  "slug": "my-research-note",
  "title": "My research note",
  "category": "Research",
  "status": "",
  "date": "2026-10-13",
  "excerpt": "A short description for the blog list and homepage.",
  "body_file": "my-research-note.html"
}
```

3. Run `python3 scripts/build-blog.py` from the project directory. It updates the homepage blog module, `blog/index.html`, and the article pages. Read times are estimated automatically; dated posts are sorted newest first. Category filters are derived from the posts.
4. Preview the repository root, then commit and push to `master`. GitHub Pages publishes the updated site automatically.

The included welcome entry is clearly marked **Sample post**, has no invented publication date, and uses only the owner's supplied education information. Replace or remove it before using the blog for actual writing. To remove its generated article folder, remove that specific folder from `blog/` after updating the index.

Asset URLs inside a post are relative to `blog/<slug>/`. Use `../../assets/filename.png` for shared assets in `assets/`.
