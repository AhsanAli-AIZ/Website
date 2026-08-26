# AIZ Pro — website

Static marketing site for AIZ Professional Services. No build step, no dependencies:
every page is plain HTML with one stylesheet and one script.

## Viewing it

Open `index.html` in a browser. Nothing needs to be installed and no server is
required — there is no `fetch`, no XHR, and no ES modules, so `file://` works.

An internet connection is needed for the webfonts (Newsreader, Inter, IBM Plex
Mono, all from Google Fonts). Offline, the page falls back to system serif/sans
and will not look right.

## Structure

```
index.html                        Home
about.html                        About + leadership
products.html                     AIZ Vault overview
it-services.html                  Service comparison hub
  ai-development-automation.html
  cloud-enablement.html
  mobile-web-development.html
  custom-software-managed-it.html
vendors.html                      Vendor & partner roster
become-a-partner.html             Partner program + inquiry form
contact.html                      Contact + inquiry form
thank-you.html                    Form redirect target (noindex)

css/style.css                     Design system + all components
js/main.js                        Nav, tabs, accordions, scroll-spy, reveal
images/                           Photography and brand assets
build-shell.py                    Keeps the shared shell in sync (see below)
```

## The shared shell

The header, footer, breadcrumb, and `<head>` boilerplate are identical on every
page. Rather than maintain twelve copies by hand, they are generated:

```bash
python build-shell.py          # rewrite the shell across all pages
python build-shell.py --check  # verify nothing has drifted; non-zero exit if it has
```

Edit the templates inside `build-shell.py` — not the HTML — when changing the nav
or footer, then re-run it. Page-specific content between `<main>` and `</footer>`
is never touched.

`PAGES` in that file maps each page to its nav highlight and breadcrumb trail; add
new pages there.

## Forms

Both forms post to [FormSubmit](https://formsubmit.co) — there is no backend.

- Recipient: `ahsan@aizpro.com`, CC `badar@`, `azam@`, `noor@`
- On success they redirect to `https://aizpro.com/thank-you.html`
- A hidden `_honey` honeypot field is present; FormSubmit's own captcha is left
  enabled

**Submitting a form sends a real email**, including from a local copy. Do not use
the live forms for testing.

## Conventions

- US English throughout (`organization`, `inquiry`, `license`). `CentreStack` is a
  brand name and keeps its spelling.
- Copy: specific and concrete over aspirational. No "military-grade",
  "best-in-class", "cutting-edge", or "seamless".
- Every page uses a different section rhythm; no two pages should read as the same
  template.
- Reveal animations are gated behind a `.has-js` class and a 2.5s timeout fallback,
  so content can never be left invisible. All motion respects
  `prefers-reduced-motion`.
