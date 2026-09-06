# UNIFIX — Task: Android app distribution page (`/get`)

## Context

UNIFIX (repo `Unipulse-main`) is a Flask + Jinja2 campus grievance platform for GL Bajaj
Institute of Technology & Management. It is a PWA that will be wrapped as a Trusted Web
Activity (TWA) for Android.

**Distribution decision: we are NOT publishing to the Google Play Store.** The signed APK
will be hosted by the app itself and handed to staff via a link and a printed QR code.

This task adds the public landing page that link points at. It must work before the APK
exists, and degrade gracefully until then.

Do not add a build step, bundler, framework or npm dependency. This project is
server-rendered Jinja2, vanilla JS and hand-written CSS by deliberate design.

---

## Scope

Create two routes and one template:

| Path | Purpose |
| --- | --- |
| `GET /get` | Public landing page: download button, install walkthrough, PWA fallback |
| `GET /download/unifix.apk` | Serves the signed APK with the correct Android mimetype |

Both are unauthenticated — this is the first URL a staff member ever opens, before they
have an account session.

---

## 1. Routes — append to `blueprints/public/__init__.py`

First update the existing import line at the top of the file:

```python
from flask import Blueprint, Response, abort, render_template, send_file
```

(`os` is already imported. `GLB` and `CONTACT_EMAIL` already exist in this module — reuse
them, do not redefine.)

Then append:

```python
# ---------------------------------------------------------------------------
# Android app distribution
# ---------------------------------------------------------------------------

# Where the signed APK lives. Overridable so the file can sit outside the repo
# (e.g. on a Render disk) without a code change. Deliberately NOT under static/
# so Flask's static handler never serves it with the wrong mimetype.
APK_PATH = os.environ.get(
    "APK_PATH",
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "dist", "unifix.apk"))
APK_VERSION = os.environ.get("APK_VERSION", "1.0.0")


def _apk_size():
    try:
        mb = os.path.getsize(APK_PATH) / (1024 * 1024)
        return f"{mb:.1f} MB"
    except OSError:
        return ""


@bp.get("/get")
def get_app():
    """Public landing page for installing UNIFIX on Android.

    Deliberately unauthenticated: this is the link and QR target handed to staff
    before they have ever signed in. Serves both the sideloaded APK and, where
    Chrome supports it, the one-tap PWA install.
    """
    return render_template(
        "public/get.html",
        glb=GLB,
        contact=CONTACT_EMAIL,
        apk_available=os.path.exists(APK_PATH),
        apk_version=APK_VERSION,
        apk_size=_apk_size(),
    )


@bp.get("/download/unifix.apk")
def download_apk():
    """Serve the signed APK with the mimetype Android expects.

    Without application/vnd.android.package-archive some browsers save the file
    as plain binary and the installer refuses to open it.
    """
    if not os.path.exists(APK_PATH):
        abort(404)
    return send_file(
        APK_PATH,
        mimetype="application/vnd.android.package-archive",
        as_attachment=True,
        download_name="unifix.apk",
        max_age=0,          # never cache; a rebuilt APK must reach users immediately
        conditional=True,   # keep range requests so interrupted downloads resume
    )
```

---

## 2. Template — create `templates/public/get.html`

Self-contained (does not extend `base_public.html`) because this is a landing page, not a
document page. Styling matches the existing navy `#0e2f5c` / `#1e5fbf` palette.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="theme-color" content="#0e2f5c">
  <title>Get UNIFIX &middot; {{ glb.short }}</title>
  <link rel="manifest" href="{{ url_for('static', filename='manifest.webmanifest') }}">
  <link rel="icon" href="{{ url_for('static', filename='icons/icon-192.png') }}">
  <style>
    *{box-sizing:border-box}
    body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
         background:#f4f7fb;color:#12243a;-webkit-text-size-adjust:100%}
    .wrap{max-width:520px;margin:0 auto;padding:0 18px 56px}
    header{background:#0e2f5c;color:#fff;padding:34px 18px 30px;text-align:center}
    header img{height:54px;width:auto;display:block;margin:0 auto 14px}
    header h1{margin:0;font-size:26px;letter-spacing:.4px}
    header p{margin:6px 0 0;font-size:14px;opacity:.85;line-height:1.5}
    .card{background:#fff;border:1px solid #e2e8f2;border-radius:14px;
          padding:20px;margin-top:18px}
    .btn{display:block;width:100%;padding:16px;border:0;border-radius:11px;
         font-size:17px;font-weight:600;text-align:center;text-decoration:none;
         cursor:pointer;font-family:inherit}
    .btn-primary{background:#0e2f5c;color:#fff}
    .btn-primary:active{background:#0a2246}
    .btn-secondary{background:#fff;color:#0e2f5c;border:1.5px solid #0e2f5c;margin-top:10px}
    .meta{text-align:center;font-size:12.5px;color:#7c8ba1;margin:10px 0 0}
    .warn{background:#fff8e6;border:1px solid #f2dfae;border-radius:11px;
          padding:14px 16px;margin-top:18px;font-size:14px;line-height:1.55}
    .warn b{display:block;margin-bottom:6px;color:#8a6100}
    h2{font-size:15px;margin:22px 0 10px;color:#0e2f5c;text-transform:uppercase;
       letter-spacing:.6px}
    ol{margin:0;padding-left:20px}
    ol li{line-height:1.65;font-size:14.5px;margin-bottom:10px}
    .quote{background:#f0f3f8;border-radius:7px;padding:7px 10px;margin-top:5px;
           font-size:13.5px;color:#3c4a5e;font-style:italic}
    .hide{display:none}
    footer{text-align:center;font-size:12.5px;color:#8798ad;margin-top:30px;line-height:1.8}
    footer a{color:#1e5fbf;text-decoration:none}
  </style>
</head>
<body>

<header>
  <img src="{{ url_for('static', filename='img/glb-logo.webp') }}" alt="{{ glb.short }}">
  <h1>UNIFIX</h1>
  <p>Campus Grievance &amp; Infrastructure Portal<br>{{ glb.name }}</p>
</header>

<div class="wrap">

  <!-- Shown only inside WhatsApp / Instagram / Facebook in-app browsers -->
  <div class="warn hide" id="inapp">
    <b>Open this page in Chrome first</b>
    Downloads do not work inside the WhatsApp browser. Tap the
    <strong>&vellip;</strong> or <strong>&bull;&bull;&bull;</strong> menu in the top corner and choose
    <strong>“Open in Chrome”</strong> or <strong>“Open in browser”</strong>, then come back here.
  </div>

  <div class="card">
    {% if apk_available %}
      <a class="btn btn-primary" href="{{ url_for('public.download_apk') }}" id="dl">
        Download UNIFIX for Android
      </a>
      <p class="meta">Version {{ apk_version }} &middot; {{ apk_size }} &middot; Android 6.0 or newer</p>
    {% else %}
      <button class="btn btn-primary" disabled style="opacity:.45">
        Android app coming soon
      </button>
      <p class="meta">Use the instant install option below in the meantime.</p>
    {% endif %}

    <!-- Revealed only when Chrome offers a real PWA install prompt -->
    <button class="btn btn-secondary hide" id="pwa">
      Or install instantly (no download)
    </button>
  </div>

  {% if apk_available %}
  <div class="warn">
    <b>Android will show you two warnings. Both are normal.</b>
    UNIFIX is distributed by {{ glb.short }} directly instead of through the Play Store,
    so Android cannot recognise it automatically. Nothing is wrong with the app.
  </div>

  <h2>What you will see</h2>
  <ol>
    <li>
      Chrome asks whether to keep the file.
      <div class="quote">“This type of file can harm your device. Keep unifix.apk anyway?”</div>
      Tap <strong>Download anyway</strong> or <strong>OK</strong>.
    </li>
    <li>
      Open the downloaded file. Android says this source is not allowed yet.
      <div class="quote">“Your phone isn’t allowed to install unknown apps from this source”</div>
      Tap <strong>Settings</strong>, turn on <strong>Allow from this source</strong>, then press back.
    </li>
    <li>
      Tap <strong>Install</strong>.
    </li>
    <li>
      Play Protect may block it once.
      <div class="quote">“Unsafe app blocked”</div>
      Tap <strong>More details</strong>, then <strong>Install anyway</strong>.
    </li>
    <li>Open UNIFIX and sign in with the username and PIN given to you by the campus administrator.</li>
  </ol>

  <h2>After installing</h2>
  <p style="font-size:14.5px;line-height:1.6;margin:0">
    You never need to download this file again. UNIFIX updates itself automatically
    whenever the campus system is updated.
  </p>
  {% endif %}

  <footer>
    Accounts are created by the campus administrator.<br>
    <a href="/login">Open UNIFIX in your browser</a> &middot;
    <a href="/privacy">Privacy</a><br>
    Need help? {{ contact }}
  </footer>
</div>

<script>
(function () {
  // 1. Warn users stuck in an in-app webview, where APK downloads silently fail.
  var ua = navigator.userAgent || "";
  if (/WhatsApp|FBAN|FBAV|Instagram|Line\//i.test(ua)) {
    document.getElementById("inapp").classList.remove("hide");
  }

  // 2. Offer the native PWA install dialog when Chrome makes one available.
  //    Chrome requires a user gesture, so we stash the event and fire it on tap.
  var deferred = null;
  var pwaBtn = document.getElementById("pwa");
  window.addEventListener("beforeinstallprompt", function (e) {
    e.preventDefault();
    deferred = e;
    pwaBtn.classList.remove("hide");
  });
  pwaBtn.addEventListener("click", function () {
    if (!deferred) return;
    deferred.prompt();
    deferred.userChoice.then(function () { deferred = null; pwaBtn.classList.add("hide"); });
  });

  // 3. Already installed — send them straight in.
  window.addEventListener("appinstalled", function () { location.href = "/login"; });
})();
</script>
</body>
</html>
```

---

## 3. Integration points — do not skip these

### 3a. PIN-change gate in `app.py`

`_enforce_pin_change()` redirects any logged-in user flagged `must_change_pin` away from
every path not in its `allowed` set. A newly created employee who taps the install link
mid-PIN-reset would be bounced to `/set-pin`. Add both paths:

```python
allowed = {"/profile", "/profile/pin", "/logout", "/set-pin", "/set-pin/submit",
           "/get", "/download/unifix.apk"}
```

### 3b. `.gitignore`

```
dist/*.apk
android.keystore
```

`android.keystore` may already be covered — verify. It must never be committed.

### 3c. APK placement

The APK is expected at `dist/unifix.apk` relative to the repo root, or wherever
`APK_PATH` points. Create `dist/.gitkeep` so the directory exists in a fresh clone.

Note for deployment: Render builds from the repo, so either commit the APK (simple,
bloats history) or attach a Render disk and set `APK_PATH` to a path on it (cleaner).
This is a deployment decision, not a code one — do not solve it in code.

### 3d. Link it from the login page

Add a small link under the existing sign-in footer text in `templates/login.html`:

```html
<p style="text-align:center;font-size:13px;margin-top:14px">
  <a href="/get">Get the Android app</a>
</p>
```

---

## 4. Manifest defect to fix while you are here

`static/manifest.webmanifest` declares two screenshots:

```
/static/screenshots/report.png
/static/screenshots/admin.png
```

That directory does not exist — both URLs 404. PWABuilder reads this manifest when
generating the Android package and should not be fed dead URLs.

Either create `static/screenshots/` with two real captures, or remove the `screenshots`
key from the manifest. Removing it is acceptable; screenshots are only needed for a Play
Store listing, which we are not doing.

---

## 5. Tests — add `tests/test_get_page.py`

Follow the existing conventions in `tests/` (in-memory backend, real HTTP stack via the
Flask test client). Cover:

1. `GET /get` returns 200 **while unauthenticated** — this is the critical property.
2. `GET /get` with no APK present returns 200 and does **not** contain the download link.
3. `GET /download/unifix.apk` with no APK present returns 404.
4. With a temporary file monkeypatched at `APK_PATH`: `/get` contains
   `/download/unifix.apk`, and the download route returns 200 with
   `Content-Type: application/vnd.android.package-archive`.
5. A user flagged `must_change_pin` can still reach `/get` (guards 3a from regressing).

The full suite must stay green — 215 tests passing before this change.

---

## 6. Acceptance criteria

- [ ] `/get` renders for anonymous users, and for users mid-PIN-change
- [ ] With no APK on disk: page renders, button is disabled, no 500, no broken link
- [ ] With an APK on disk: download serves with mimetype
      `application/vnd.android.package-archive` and filename `unifix.apk`
- [ ] PWA install button stays hidden unless `beforeinstallprompt` fires
- [ ] No new dependency in `requirements.txt`; no build step; no npm
- [ ] `dist/*.apk` and `android.keystore` are gitignored
- [ ] Full pytest suite green

---

## 7. Out of scope for this task

Listed so they are not attempted here — they are environment and deployment work:

- Creating the signing keystore (`keytool`)
- Setting `TWA_SHA256_CERT_FINGERPRINTS` (the `/.well-known/assetlinks.json` route
  already exists and reads it)
- Building the APK via PWABuilder or Bubblewrap
- Provisioning the production host or custom domain
- Generating the QR code image

`targetSdkVersion` is irrelevant to this project — it is a Play Store submission
requirement, and we are distributing outside Play.
