#!/usr/bin/env python3
"""
Rewrites the shared shell (head boilerplate, header, footer) across every
page so the eleven copies cannot drift apart.

Run from aizpro-final/:   python build-shell.py
Verify without writing:   python build-shell.py --check
"""

import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).parent

# page -> (nav key, breadcrumb trail as [(label, href), ...] excluding Home)
PAGES = {
    "index.html":                     ("home",        []),
    "about.html":                     ("about",       [("About Us", None)]),
    "products.html":                  ("products",    [("AIZ Vault", None)]),
    "it-services.html":               ("it-services", [("IT Services", None)]),
    "ai-development-automation.html": ("it-services", [("IT Services", "it-services.html"), ("AI Development & Automation", None)]),
    "cloud-enablement.html":          ("it-services", [("IT Services", "it-services.html"), ("Cloud Enablement", None)]),
    "mobile-web-development.html":    ("it-services", [("IT Services", "it-services.html"), ("Mobile & Web Development", None)]),
    "custom-software-managed-it.html":("it-services", [("IT Services", "it-services.html"), ("Custom Software & Managed IT", None)]),
    "vendors.html":                   ("vendors",     [("Vendors", None)]),
    "become-a-partner.html":          ("partner",     [("Become a Partner", None)]),
    "contact.html":                   ("contact",     [("Contact", None)]),
    "thank-you.html":                 ("contact",     [("Contact", "contact.html"), ("Thank You", None)]),
}

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    'family=Inter:wght@400;500;600;700&'
    'family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600;6..72,700&'
    'family=IBM+Plex+Mono:wght@400;500&display=swap">\n'
    '<link rel="stylesheet" href="css/style.css">'
)


def nav_attr(key, current):
    return ' aria-current="page"' if key == current else ""


def header_html(current):
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <nav class="nav-wrap" aria-label="Primary">
    <a href="index.html" class="logo" aria-label="AIZ Professional Services &#8212; Home">
      <span class="logo-mark">AIZ</span>
      <span class="logo-rule"></span>
      <span class="logo-text"><span>Professional</span><span>Services</span></span>
    </a>
    <ul class="nav-links" id="primary-nav">
      <li><a href="index.html"{nav_attr("home", current)}>Home</a></li>
      <li><a href="about.html"{nav_attr("about", current)}>About</a></li>
      <li class="has-dropdown">
        <a href="products.html"{nav_attr("products", current)} aria-expanded="false">AIZ Vault <span class="caret" aria-hidden="true">&#9662;</span></a>
        <ul class="dropdown">
          <li><a href="products.html">Overview</a></li>
        </ul>
      </li>
      <li class="has-dropdown">
        <a href="it-services.html"{nav_attr("it-services", current)} aria-expanded="false">IT Services <span class="caret" aria-hidden="true">&#9662;</span></a>
        <div class="dropdown mega">
          <div class="mega-grid">
            <a href="ai-development-automation.html">
              <span class="mega-title">AI Development &amp; Automation</span>
              <span class="mega-desc">Document processing, workflow automation, and models trained on your own data.</span>
            </a>
            <a href="cloud-enablement.html">
              <span class="mega-title">Cloud Enablement</span>
              <span class="mega-desc">Assessment, migration, and ongoing management across Azure, AWS, and Google Cloud.</span>
            </a>
            <a href="mobile-web-development.html">
              <span class="mega-title">Mobile &amp; Web Development</span>
              <span class="mega-desc">iOS, Android, and web builds with accessibility and performance budgets set up front.</span>
            </a>
            <a href="custom-software-managed-it.html">
              <span class="mega-title">Custom Software &amp; Managed IT</span>
              <span class="mega-desc">Line-of-business systems, plus a service desk with published response targets.</span>
            </a>
            <div class="mega-foot">
              <p>Not sure which fits? Compare all four side by side.</p>
              <a class="btn btn-secondary" href="it-services.html">Compare services</a>
            </div>
          </div>
        </div>
      </li>
      <li><a href="vendors.html"{nav_attr("vendors", current)}>Vendors</a></li>
      <li><a href="become-a-partner.html"{nav_attr("partner", current)}>Partner</a></li>
    </ul>
    <div class="nav-cta">
      <a class="btn btn-primary" href="contact.html">Book a consultation</a>
      <button class="nav-toggle" aria-label="Toggle menu" aria-controls="primary-nav" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </nav>
</header>'''


def breadcrumb_html(trail):
    if not trail:
        return ""
    items = ['      <li><a href="index.html">Home</a></li>']
    for label, href in trail:
        if href:
            items.append(f'      <li><a href="{href}">{label}</a></li>')
        else:
            items.append(f'      <li aria-current="page">{label}</li>')
    inner = "\n".join(items)
    return f'''  <nav class="breadcrumb" aria-label="Breadcrumb">
    <div class="container">
      <ol>
{inner}
      </ol>
    </div>
  </nav>
'''


FOOTER = '''<footer class="site-footer">
  <div class="container">
    <div class="footer-top">
      <div class="footer-brand">
        <span class="logo" aria-hidden="true">
          <span class="logo-mark">AIZ</span>
          <span class="logo-rule"></span>
          <span class="logo-text"><span>Professional</span><span>Services</span></span>
        </span>
        <p class="footer-blurb">Enterprise IT services and secure file management for organizations working across borders.</p>
      </div>
      <div class="footer-col">
        <h2>Services</h2>
        <ul>
          <li><a href="ai-development-automation.html">AI &amp; Automation</a></li>
          <li><a href="cloud-enablement.html">Cloud Enablement</a></li>
          <li><a href="mobile-web-development.html">Mobile &amp; Web</a></li>
          <li><a href="custom-software-managed-it.html">Software &amp; Managed IT</a></li>
          <li><a href="it-services.html">Compare all services</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h2>Company</h2>
        <ul>
          <li><a href="about.html">About Us</a></li>
          <li><a href="about.html#leadership">Leadership</a></li>
          <li><a href="vendors.html">Vendors &amp; Partners</a></li>
          <li><a href="become-a-partner.html">Become a Partner</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h2>Get in touch</h2>
        <ul>
          <li><a href="contact.html">Book a consultation</a></li>
          <li><a href="mailto:ahsan@aizpro.com">ahsan@aizpro.com</a></li>
          <li><a href="products.html">AIZ Vault</a></li>
          <li><a href="https://portal.aizvault.com" target="_blank" rel="noopener">Vault sign-in</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <div>&#169; 2026 AIZ Pro. All rights reserved.</div>
      <ul>
        <li><a href="contact.html">Contact</a></li>
        <li><a href="vendors.html">Vendors</a></li>
        <li><a href="become-a-partner.html">Partners</a></li>
      </ul>
    </div>
  </div>
</footer>'''


def apply(path: pathlib.Path, nav_key: str, trail, check: bool) -> bool:
    src = path.read_text(encoding="utf-8")
    out = src

    # 1. font + stylesheet block in <head>
    out = re.sub(
        r'<link rel="preconnect" href="https://fonts\.googleapis\.com">.*?'
        r'<link rel="stylesheet" href="css/style\.css">',
        lambda _: FONTS, out, flags=re.S)

    # 2. header (plus skip link)
    out = re.sub(
        r'(?:<a class="skip-link".*?</a>\s*)?<header class="site-header">.*?</header>',
        lambda _: header_html(nav_key), out, flags=re.S)

    # 3. breadcrumb directly after <main>
    out = re.sub(r'<main[^>]*>\n(?:  <nav class="breadcrumb".*?</nav>\n)?',
                 lambda _: '<main id="main">\n' + breadcrumb_html(trail), out, flags=re.S)

    # 4. footer
    out = re.sub(r'<footer class="site-footer">.*?</footer>',
                 lambda _: FOOTER, out, flags=re.S)

    if out != src and not check:
        path.write_text(out, encoding="utf-8")
    return out != src


def main():
    check = "--check" in sys.argv
    changed = []
    for name, (nav_key, trail) in PAGES.items():
        p = ROOT / name
        if not p.exists():
            print(f"  skip (missing): {name}")
            continue
        if apply(p, nav_key, trail, check):
            changed.append(name)

    if check:
        if changed:
            print("DRIFT — these pages do not match the canonical shell:")
            for c in changed:
                print("   ", c)
            sys.exit(1)
        print("OK — shell is identical across all pages.")
    else:
        print(f"Updated {len(changed)} page(s):")
        for c in changed:
            print("   ", c)


if __name__ == "__main__":
    main()
