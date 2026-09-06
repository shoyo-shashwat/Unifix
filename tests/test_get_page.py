"""Phase — Android APK distribution. UNIFIX is sideloaded, not on the Play
Store, so `/get` is the public link/QR target and must work before the APK
exists and for users who have not signed in yet."""
from db import users


def _login(c, u="prof.rao", p="1234"):
    return c.post("/login", data={"username": u, "pin": p})


def test_get_page_renders_without_login(client):
    r = client.get("/get")
    assert r.status_code == 200 and b"UNIFIX" in r.data


def test_get_page_without_apk_hides_download_link(client):
    r = client.get("/get")
    assert r.status_code == 200
    assert b"/download/unifix.apk" not in r.data


def test_download_without_apk_is_404(client):
    assert client.get("/download/unifix.apk").status_code == 404


def test_download_serves_apk_with_android_mimetype(client, monkeypatch, tmp_path):
    apk = tmp_path / "unifix.apk"
    apk.write_bytes(b"PK\x03\x04 not really an apk")
    monkeypatch.setattr("blueprints.public.APK_PATH", str(apk))

    page = client.get("/get")
    assert page.status_code == 200 and b"/download/unifix.apk" in page.data

    r = client.get("/download/unifix.apk")
    assert r.status_code == 200
    assert r.mimetype == "application/vnd.android.package-archive"


def test_user_mid_pin_change_can_still_reach_get(client):
    uid = users.get_by_username("prof.rao")["id"]
    users.set_must_change_pin(uid, True)
    _login(client)
    assert client.get("/get").status_code == 200
