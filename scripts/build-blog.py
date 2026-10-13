"""Generate the homepage blog module, archive, and article pages from local content."""
import html
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT
CONTENT = ROOT / 'content'
SCHOLAR = 'https://scholar.google.com/citations?user=9sh3BnsAAAAJ&amp;hl=en'
e = html.escape
posts = json.loads((CONTENT / 'posts.json').read_text())
slugs = set()
for p in posts:
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', p['slug']) or p['slug'] in slugs:
        raise ValueError('Post slugs must be unique lowercase URL names.')
    slugs.add(p['slug'])
    body_path = (CONTENT / p['body_file']).resolve()
    if not body_path.is_relative_to(CONTENT):
        raise ValueError('Post body must be inside content/.')
    p['body'] = body_path.read_text()
    if p.get('date'):
        p['date_label'] = date.fromisoformat(p['date']).strftime('%b %d, %Y')
    else:
        p['date_label'] = ''
    p['minutes'] = max(1, round(len(re.sub('<[^>]+>', ' ', p['body']).split()) / 200))
posts.sort(key=lambda p: p.get('date') or '', reverse=True)

def meta(p):
    bits = [e(p['category'])]
    if p.get('status'):
        bits.append(f'<span class="post-status">{e(p["status"])}</span>')
    if p['date_label']:
        bits.append(f'<time datetime="{e(p["date"])}">{e(p["date_label"])}</time>')
    bits.append(f'{p["minutes"]} min read')
    return ' <span aria-hidden="true">·</span> '.join(bits)

def row(p, prefix, filterable=False):
    data = ''
    if filterable:
        data = f' data-post data-category="{e(p["category"])}" data-search="{e(p["title"] + " " + p["excerpt"] + " " + p["category"])}"'
    return f'''<article class="blog-row"{data}><div><p class="post-meta">{meta(p)}</p><h3><a href="{prefix}{p['slug']}/">{e(p['title'])}</a></h3><p class="post-excerpt">{e(p['excerpt'])}</p></div><a class="post-arrow" href="{prefix}{p['slug']}/" aria-label="Read {e(p['title'])}">↗</a></article>'''

def page(title, description, content, prefix, script=''):
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{e(description)}"><meta name="theme-color" content="#c18c9e"><title>{e(title)} — Yongshan Zhu</title><link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}styles.css"><link rel="stylesheet" href="{prefix}blog.css">{script}</head>
<body class="writing-page"><a class="skip-link" href="#main">Skip to content</a><header class="header writing-header"><a class="wordmark" href="{prefix}index.html" aria-label="Yongshan Zhu, home">YZ<span class="logo-sun" aria-hidden="true"></span></a><nav aria-label="Main navigation"><a href="{prefix}index.html#about">About</a><a href="{prefix}index.html#publications">Publications</a><a href="{prefix}blog/" aria-current="page">Blog</a><a href="{SCHOLAR}" target="_blank" rel="noopener noreferrer">Scholar ↗</a></nav></header><main id="main">{content}</main><footer class="wrap"><p>© {date.today().year} Yongshan Zhu</p><a href="{prefix}index.html">Back to the homepage ↗</a></footer></body></html>'''

preview_rows = '\n'.join(row(p, 'blog/') for p in posts[:3])
if not posts:
    preview_rows = '<p class="empty-blog">No posts yet. New writing will appear here.</p>'
module = f'''<section class="blog-section section wrap" id="blog" aria-labelledby="blog-title"><div class="section-heading"><div><p class="section-kicker">04 / NOTEBOOK</p><h2 id="blog-title">Notes along the way<span class="accent-dot">.</span></h2></div><a class="text-link" href="blog/">View the blog ↗</a></div><p class="blog-intro">Research notes, ideas in progress, and the occasional reflection.</p>{preview_rows}</section>'''
home_path = DIST / 'index.html'
home = home_path.read_text()
home, count = re.subn(r'<!-- BLOG:START -->.*?<!-- BLOG:END -->', f'<!-- BLOG:START -->\n    {module}\n    <!-- BLOG:END -->', home, flags=re.S)
if count != 1:
    raise ValueError('The homepage must have exactly one pair of blog markers.')
home_path.write_text(home)

blog_dir = DIST / 'blog'
blog_dir.mkdir(exist_ok=True)
categories = sorted({p['category'] for p in posts})
buttons = '<button class="category-button" type="button" data-filter="All" aria-pressed="true">All posts</button>'
buttons += ''.join(f'<button class="category-button" type="button" data-filter="{e(c)}" aria-pressed="false">{e(c)}</button>' for c in categories)
rows = '\n'.join(row(p, '', True) for p in posts)
archive = f'''<section class="writing-masthead"><div class="wrap"><p class="section-kicker">THE NOTEBOOK</p><h1>Notes along<br>the way<span>.</span></h1><p>Research notes, ideas in progress, and the occasional reflection.</p></div></section><section class="blog-archive wrap"><div class="blog-controls"><div class="category-filters" aria-label="Filter posts by category">{buttons}</div><div class="blog-search"><label for="post-search">Search the notebook</label><input type="search" id="post-search" placeholder="Search titles and topics…"></div></div><p id="post-count" class="results-count" aria-live="polite">{len(posts)} {'post' if len(posts) == 1 else 'posts'}</p><div id="post-list">{rows}</div><div id="no-posts" class="empty-blog" {'hidden' if posts else ''}><h2>No posts found.</h2><p>Try another keyword or category.</p><button type="button" id="reset-search">Show all posts ↗</button></div><noscript><p class="noscript-note">All posts are shown. Search and category filters require JavaScript.</p></noscript></section>'''
(blog_dir / 'index.html').write_text(page('Blog', 'Notes on research, ideas, and the journey from Xidian University to Westlake University.', archive, '../', '<script src="blog.js" defer></script>'))

for p in posts:
    dest = blog_dir / p['slug']
    dest.mkdir(exist_ok=True)
    article = f'''<article class="article-page"><header class="article-header wrap"><a class="text-link" href="../">← All posts</a><p class="post-meta">{meta(p)}</p><h1>{e(p['title'])}</h1><p class="article-byline">Yongshan Zhu <span lang="zh">朱永山</span></p></header><div class="article-body">{p['body']}</div><div class="article-end"><span class="end-sun" aria-hidden="true"></span><p>The next question is just over the horizon.</p><a class="text-link" href="../">← Back to the notebook</a></div></article>'''
    (dest / 'index.html').write_text(page(p['title'], p['excerpt'], article, '../../'))
print(f'Generated blog archive, homepage module, and {len(posts)} article page(s).')
