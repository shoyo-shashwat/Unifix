"""Unauthenticated pages required for Google Play: privacy policy, account
deletion information, and the Digital Asset Links file that verifies the TWA."""
import os

from flask import Blueprint, Response, abort, render_template, send_file

from domain.constants import GLB

bp = Blueprint("public", __name__, template_folder="../../templates")

CONTACT_EMAIL = os.environ.get("PRIVACY_CONTACT_EMAIL", "").strip() \
    or f"unifix@{GLB['email_domain']}"


@bp.get("/privacy")
def privacy():
    return render_template("public/privacy.html", contact=CONTACT_EMAIL, glb=GLB)


@bp.get("/account-deletion")
def account_deletion():
    return render_template("public/account_deletion.html", contact=CONTACT_EMAIL, glb=GLB)


@bp.get("/.well-known/assetlinks.json")
def assetlinks():
    """Digital Asset Links — lets Chrome verify the Android TWA owns this origin
    so it launches without a URL bar. Populated from the app signing key's
    SHA-256 fingerprint(s)."""
    pkg = os.environ.get("TWA_PACKAGE_NAME", "in.ac.glbitm.unifix").strip()
    fps = [f.strip() for f in
           os.environ.get("TWA_SHA256_CERT_FINGERPRINTS", "").split(",") if f.strip()]
    body = [{
        "relation": ["delegate_permission/common.handle_all_urls"],
        "target": {"namespace": "android_app", "package_name": pkg,
                   "sha256_cert_fingerprints": fps},
    }]
    return Response(__import__("json").dumps(body, indent=2),
                    mimetype="application/json")


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
