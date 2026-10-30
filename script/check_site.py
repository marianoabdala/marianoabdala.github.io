#!/usr/bin/env python3
"""Check the built site without extra Python dependencies. Run from repo root."""
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / '_site'
ORIGIN = 'https://zerously.com'
errors = []


def check(condition, message):
    if not condition:
        errors.append(message)


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.elements = []
        self.ids = set()
        self.jsonld = []
        self.in_jsonld = False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.elements.append((tag, attrs))
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.in_jsonld = True
            self.jsonld.append('')

    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_jsonld = False

    def handle_data(self, data):
        if self.in_jsonld:
            self.jsonld[-1] += data

    def attrs(self, tag):
        return [a for t, a in self.elements if t == tag]


def target(path):
    p = SITE / unquote(path).lstrip('/')
    return p / 'index.html' if p.is_dir() else p


check(SITE.is_dir(), 'Build the site before running this check.')
if errors:
    sys.exit('\n'.join(errors))

legacy = json.loads((ROOT / '_data/legacy_posts.json').read_text())
for post in legacy:
    source = ROOT / post['source']
    check(source.exists(), f'Missing original: {source}')
    if source.exists():
        check(hashlib.sha256(source.read_bytes()).hexdigest() == post['sha256'],
              f'Historical post changed: {source}')
    check(target(post['url']).is_file(), f'Missing historical URL: {post["url"]}')

pages = {}
for file in SITE.rglob('*.html'):
    path = '/' + str(file.relative_to(SITE))
    path = path.removesuffix('index.html')
    page = Page(file.read_text())
    pages[path] = page
    check(any(a.get('lang') for a in page.attrs('html')), f'Missing language: {path}')
    check(len(page.attrs('main')) == 1, f'Expected one main landmark: {path}')
    check(any(a.get('href') == '#main-content' for a in page.attrs('a')), f'Missing skip link: {path}')
    check(any(a.get('aria-label') for a in page.attrs('nav')), f'Missing named navigation: {path}')
    canonicals = [a.get('href') for a in page.attrs('link') if a.get('rel') == 'canonical']
    check(canonicals == [ORIGIN + path], f'Wrong canonical: {path}: {canonicals}')
    check(any(a.get('name') == 'description' and a.get('content') for a in page.attrs('meta')),
          f'Missing description: {path}')
    check(bool(page.jsonld), f'Missing structured data: {path}')
    for data in page.jsonld:
        try:
            json.loads(data)
        except ValueError:
            errors.append(f'Invalid JSON-LD: {path}')
    for tag, attrs in page.elements:
        if tag == 'img':
            check('alt' in attrs, f'Missing image alt: {path}')
        for attribute in ('href', 'src'):
            value = attrs.get(attribute, '')
            if not value or value.startswith(('mailto:', 'tel:', 'data:')):
                continue
            url = urlsplit(urljoin(ORIGIN + path, value))
            if attribute == 'src':
                check(url.scheme != 'http', f'Mixed-content resource: {path}: {value}')
            if url.netloc != 'zerously.com':
                continue
            check(target(url.path).is_file(), f'Broken internal link/resource: {path}: {value}')

home = pages.get('/')
check(home is not None, 'Missing homepage')
check('/read-me/' in pages, 'Missing Read.me')
if home:
    links = [a['href'] for a in home.attrs('a') if a.get('class') == 'post-link']
    check(len(links) >= 12 and len(set(links)) == len(links), 'Missing or repeated homepage posts')
    check(all(p['url'] in links for p in legacy), 'Historical posts absent from homepage')
    check(len([a for a in home.attrs('p') if a.get('class') == 'post-excerpt']) == len(links),
          'Missing homepage excerpts')
else:
    links = []

feed = ET.parse(SITE / 'feed.xml').getroot()
items = feed.findall('./channel/item')
check({i.findtext('link') for i in items} == {ORIGIN + p for p in links}, 'RSS does not match homepage posts')
for post in legacy:
    item = next((i for i in items if i.findtext('link') == ORIGIN + post['url']), None)
    check(item is not None, f'Missing RSS item: {post["url"]}')
    if item is not None:
        check(item.findtext('guid') == 'http://zerously.com' + post['url'], f'Changed RSS identity: {post["url"]}')
for item in items:
    for tag, attrs in Page(item.findtext('description', '')).elements:
        for attribute in ('href', 'src'):
            value = attrs.get(attribute, '')
            check(not value.startswith('/'), f'Non-absolute RSS URL: {value}')

sitemap = ET.parse(SITE / 'sitemap.xml')
locations = {e.text for e in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
check(all(ORIGIN + p in locations for p in links + ['/read-me/']), 'Missing sitemap URLs')
check(all(u.startswith(ORIGIN + '/') for u in locations), 'Non-HTTPS sitemap URLs')
check('Sitemap: ' + ORIGIN + '/sitemap.xml' in (SITE / 'robots.txt').read_text(), 'Wrong robots sitemap')
check((SITE / 'CNAME').read_text().strip() == 'zerously.com', 'Changed custom domain')
for excluded in ('docs', 'templates', 'script', 'README.md', 'README.html', 'Gemfile', 'Gemfile.lock'):
    check(not (SITE / excluded).exists(), f'Internal file published: {excluded}')

if errors:
    sys.exit('\n'.join(errors))
print(f'PASS: {len(legacy)} unchanged historical posts, {len(pages)} pages, {len(items)} RSS items; routes, local links, metadata and sitemap checked.')
