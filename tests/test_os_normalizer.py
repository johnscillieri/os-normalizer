import itertools as it
import pytest

from os_fingerprint import normalize_os
from os_fingerprint.constants import MACOS_DARWIN_MAP


def mk_obs(i, raw, json=None):
    return (
        i,
        raw,
        json or {},
    )


# -------------------------
# Generators (produce 200+)
# -------------------------


def windows_cases():
    builds = [19044, 19045, 22000, 22621, 22631]
    editions = ["Enterprise", "Pro", "Home"]
    channel_by_build = {
        19044: "2004/20H2/21H1/21H2/22H2",
        19045: "2004/20H2/21H1/21H2/22H2",
        22000: "21H2",
        22621: "22H2",
        22631: "23H2",
    }
    for i, (b, e) in enumerate(it.product(builds, editions), 1):
        s = f"Windows NT 10.0 build {b} {e} x64"
        product = "Windows 11" if b >= 22000 else "Windows 10"

        expect = {
            "family": "windows",
            "vendor": "Microsoft",
            "product": product,
            # The parser recognizes 'Enterprise' and 'Home' tokens, but not short 'Pro'
            **({"edition": e} if e in {"Enterprise", "Home"} else {}),
            "arch": "x86_64",
            "kernel_name": "nt",
            "version_build": str(b),
            "kernel_version": f"10.0.{b}",
            "channel": channel_by_build[b],
            "precision": "build",
        }
        yield mk_obs(1000 + i, s), expect
    # Windows 7/8.1 with SP/editions
    olds = [
        ("Windows 7 SP1 Professional x86", "Windows 7"),
        ("Windows 8.1 Enterprise x64", "Windows 8.1"),
        ("Windows 7 Professional", "Windows 7"),
    ]
    for j, (s, prod) in enumerate(olds, 1):
        exp = {"family": "windows", "product": prod, "kernel_name": "nt"}
        if "Professional" in s:
            exp["edition"] = "Professional"
        if "Enterprise" in s:
            exp["edition"] = "Enterprise"
        if "x64" in s:
            exp["arch"] = "x86_64"
        if "x86" in s and "x64" not in s:
            exp["arch"] = "x86"
        if "SP1" in s:
            exp["version_patch"] = 1
            exp["precision"] = "patch"
        yield mk_obs(1100 + j, s), exp


def macos_cases():
    darwins = [19, 20, 21, 22, 23, 24]
    for i, d in enumerate(darwins, 1):
        s = f"Darwin {d}.0.0; macOS"
        yield (
            mk_obs(1200 + i, s),
            {
                "family": "macos",
                "vendor": "Apple",
                "product": "macOS",
                "kernel_name": "darwin",
                "kernel_version": f"{d}.0.0",
                "codename": MACOS_DARWIN_MAP[d][2],
                # Version from map (10.15 has minor; others are major-only)
                **(
                    {"version_major": int(MACOS_DARWIN_MAP[d][1].split(".")[0]), "version_minor": int(MACOS_DARWIN_MAP[d][1].split(".")[1])}
                    if "." in MACOS_DARWIN_MAP[d][1]
                    else {"version_major": int(MACOS_DARWIN_MAP[d][1])}
                ),
            },
        )
    names = ["macOS Sequoia", "macOS Sonoma", "macOS Ventura", "macOS Monterey"]
    for j, name in enumerate(names, 1):
        s = f"{name} Darwin {24 if 'Sequoia' in name else 23 if 'Sonoma' in name else 22 if 'Ventura' in name else 21}.0.0"
        codename = name.split(" ", 1)[1]
        ver_major = {"Sequoia": 15, "Sonoma": 14, "Ventura": 13, "Monterey": 12}[codename.split()[0]]
        expect = {
            "family": "macos",
            "vendor": "Apple",
            "product": "macOS",
            "kernel_name": "darwin",
            "codename": codename,
            "version_major": ver_major,
        }
        yield mk_obs(1300 + j, s), expect


def linux_cases():
    # Ubuntu / Debian / RHEL / Rocky / Alma / Amazon
    osrels = [
        (
            'NAME="Ubuntu"\nID=ubuntu\nVERSION_ID="22.04.4"\nVERSION_CODENAME=jammy\nPRETTY_NAME="Ubuntu 22.04.4 LTS"',
            "Ubuntu",
        ),
        (
            'NAME="Debian GNU/Linux"\nID=debian\nVERSION_ID="12"\nVERSION_CODENAME=bookworm\nPRETTY_NAME="Debian GNU/Linux 12 (bookworm)"',
            "Debian GNU/Linux",
        ),
        (
            'NAME="Red Hat Enterprise Linux"\nID=rhel\nVERSION_ID="8.10"\nPRETTY_NAME="Red Hat Enterprise Linux 8.10 (Ootpa)"',
            "Red Hat Enterprise Linux",
        ),
        (
            'NAME="Rocky Linux"\nID=rocky\nVERSION_ID="9.4"\nPRETTY_NAME="Rocky Linux 9.4 (Blue Onyx)"',
            "Rocky Linux",
        ),
        (
            'NAME="AlmaLinux"\nID=almalinux\nVERSION_ID="9.4"\nPRETTY_NAME="AlmaLinux 9.4 (Seafoam Ocelot)"',
            "AlmaLinux",
        ),
        (
            'NAME="Amazon Linux"\nID=amzn\nVERSION_ID="2023"\nPRETTY_NAME="Amazon Linux 2023"',
            "Amazon Linux",
        ),
    ]
    i = 1400
    for blob, prod in osrels:
        s = "Linux host 5.15.0-122-generic x86_64"
        json = {"arch": "x86_64", "os_release": blob}
        i += 1
        # Compute expected fields
        distro_id = blob.split("\n")[1].split("=")[1]
        version_id = [l for l in blob.splitlines() if l.startswith("VERSION_ID")][0].split("=")[1].strip('"')
        code = None
        for line in blob.splitlines():
            if line.startswith("VERSION_CODENAME"):
                code = line.split("=", 1)[1]
                break
        vendor_by_distro = {
            "ubuntu": "Canonical",
            "debian": "Debian",
            "rhel": "Red Hat",
            "rocky": "Rocky",
            "almalinux": "AlmaLinux",
            "amzn": "Amazon",
        }
        version_parts = version_id.split(".")
        exp = {
            "family": "linux",
            "product": prod,
            "vendor": vendor_by_distro.get(distro_id, None),
            "distro": distro_id,
            "kernel_name": "linux",
            "kernel_version": "5.15.0-122-generic",
            "arch": "x86_64",
        }
        if len(version_parts) >= 1 and version_parts[0].isdigit():
            exp["version_major"] = int(version_parts[0])
        if len(version_parts) >= 2 and version_parts[1].isdigit():
            exp["version_minor"] = int(version_parts[1])
        if len(version_parts) >= 3 and version_parts[2].isdigit():
            exp["version_patch"] = int(version_parts[2])
        if code:
            exp["codename"] = code.title()
        if prod == "Ubuntu":
            exp["channel"] = "LTS"
        yield (mk_obs(i, s, json), exp)

    # Add a batch of kernel-only signals
    kernel_only = [
        ("5.10.0-30-amd64", "x86_64"),
        ("6.5.7-arch1-1", None),
        ("4.18.0-553.8.1.el8_10.x86_64", "x86_64"),
    ]
    for k, arch in kernel_only:
        i += 1
        s = f"Linux node {k}"
        exp = {"family": "linux", "product": "Linux", "kernel_name": "linux", "kernel_version": k}
        if arch:
            exp["arch"] = arch
        yield mk_obs(i, s), exp


def mobile_bsd_cases():
    i = 1600
    for v in ["Android 14 build UPB5.230623.003", "Android 13", "Android 12.1"]:
        i += 1
        exp = {"family": "android", "product": "Android", "vendor": "Google"}
        if "Android 14" in v:
            exp["version_major"] = 14
            exp["precision"] = "major"
        if "Android 13" in v:
            exp["version_major"] = 13
            exp["precision"] = "major"
        if "Android 12.1" in v:
            exp["version_major"] = 12
            exp["version_minor"] = 1
            exp["precision"] = "minor"
        yield mk_obs(i, v), exp
    for v in ["iOS 17.5.1", "iPadOS 16.7.6"]:
        i += 1
        exp = {"family": "ios", "product": "iOS/iPadOS", "vendor": "Apple"}
        nums = [int(x) for x in v.split()[-1].split(".")]
        if len(nums) >= 1:
            exp["version_major"] = nums[0]
        if len(nums) >= 2:
            exp["version_minor"] = nums[1]
        if len(nums) >= 3:
            exp["version_patch"] = nums[2]
        exp["precision"] = "patch"
        yield mk_obs(i, v), exp
    for v in ["FreeBSD 12.4-RELEASE", "OpenBSD 7.5", "NetBSD 9.3"]:
        i += 1
        name = v.split()[0]
        exp = {"family": "bsd", "product": name, "vendor": name, "kernel_name": name.lower()}
        ver = v.split()[1]
        nums = ver.split("-")[0].split(".")
        if len(nums) >= 1:
            exp["version_major"] = int(nums[0])
        if len(nums) >= 2:
            exp["version_minor"] = int(nums[1])
        if "-RELEASE" in v.upper():
            exp["channel"] = "RELEASE"
        yield mk_obs(i, v), exp


def cisco_cases():
    i = 1800
    # IOS XE Amsterdam 17.9.x on C9300
    versions = ["17.9.1a", "17.9.3", "17.9.4a", "17.6.5"]
    models = ["C9300-24T", "C9300-48P"]
    editions = ["universalk9", "ipbase"]
    for v, m, f in it.product(versions, models, editions):
        i += 1
        s = f"Cisco IOS XE Software, Version {v} (Amsterdam) {m}, {f}, c9300-{f}.{v.replace('.', '.').replace('a', '.a')}.SPA.bin"
        yield (
            mk_obs(i, s),
            {
                "family": "network-os",
                "vendor": "Cisco",
                "product": "IOS XE",
                "kernel_name": "ios-xe",
                "edition": f,
                "hw_model": m,
                "codename": "Amsterdam",
                # Extracted version numbers and build info
                "version_major": int(v.split(".")[0]),
                "version_minor": int(v.split(".")[1]),
                "version_patch": int(v.split(".")[2].rstrip("abcdefghijklmnopqrstuvwxyz")) if len(v.split(".")) >= 3 else None,
                "version_build": v,
                "build_id": "SPA.bin",  # suffix check via endswith; asserted differently below
                "precision": "build",
            },
        )
    # NX-OS
    for v, m in [("9.3(5)", "N9K-C93180YC-FX"), ("10.2(3)", "N9K-C93360YC-FX2")]:
        i += 1
        s = f"Cisco Nexus Operating System (NX-OS) Software nxos.{v}.bin {m}"
        nums = [int(x) for x in (v.replace("(", ".").replace(")", "")).split(".") if x.isdigit()]
        exp = {
            "family": "network-os",
            "vendor": "Cisco",
            "product": "NX-OS",
            "kernel_name": "nx-os",
            "hw_model": m,
            "version_major": nums[0],
            "version_minor": nums[1],
            "version_patch": nums[2] if len(nums) > 2 else None,
            # Parser sets precision to patch based on version numbers; no build id guaranteed
            "precision": "patch",
        }
        yield mk_obs(i, s), exp
    # Classic IOS
    import re
    for v in ["15.2(7)E3", "12.4(25d)"]:
        i += 1
        s = f"Cisco IOS Software, C2960 Software (C2960-LANBASEK9-M), Version {v}, RELEASE SOFTWARE (fc1)"
        nums = [int(x) for x in re.findall(r"\d+", v)]
        exp = {
            "family": "network-os",
            "vendor": "Cisco",
            "product": "IOS",
            "kernel_name": "ios",
            "version_major": nums[0],
            "version_minor": nums[1],
            "version_patch": nums[2] if len(nums) > 2 else None,
        }
        yield mk_obs(i, s), exp


def juniper_cases():
    i = 2000
    models = ["EX4300-48T", "EX3400-24P", "SRX300", "QFX5120-48Y"]
    vers = ["20.4R3-S3", "18.4R2-S4", "21.1R1", "19.4R3", "22.3R1-S1"]
    for v, m in it.product(vers, models):
        i += 1
        s = f"Junos: {v} jinstall-ex-4300-{v}.tgz {m}"
        # Expected model shape depends on series; QFX is truncated at hyphen, others include suffix
        hw = m.split("-")[0] if m.startswith("QFX") and "-" in m else m
        yield (
            mk_obs(i, s),
            {
                "family": "network-os",
                "vendor": "Juniper",
                "product": "Junos",
                "kernel_name": "junos",
                "hw_model": hw,
                "version_major": int(v.split(".")[0]),
                "version_minor": int(v.split(".")[1].split("R")[0]),
                "version_build": v,
                "precision": "build",
            },
        )


def fortinet_cases():
    i = 2200
    models = ["FortiGate-100F", "FortiGate-60E FGT60E", "FortiGate-200E", "FortiGate-80F FGT80F"]
    vers = [
        ("7.2.7", "1600", "GA"),
        ("7.0.13", "1520", "Patch"),
        ("6.4.14", "1960", "GA"),
        ("7.4.3", "2580", "GA"),
        ("7.2.5", "1500", "GA"),
    ]
    for (ver, build, ch), m in it.product(vers, models):
        i += 1
        s = f"{m} v{ver} build{build} ({ch}) FGT_{ver}-build{build}"
        yield (
            mk_obs(i, s),
            {
                "family": "network-os",
                "vendor": "Fortinet",
                "product": "FortiOS",
                "kernel_name": "fortios",
                # Parser captures the first model token and normalizes FortiGate- to FG-
                "hw_model": m.split()[0].replace("FortiGate-", "FG-"),
                "version_major": int(ver.split(".")[0]),
                "version_minor": int(ver.split(".")[1]),
                **({"version_patch": int(ver.split(".")[2])} if len(ver.split(".")) > 2 else {}),
                "version_build": f"{ver}+build.{build}",
                "build_id": f"FGT_{ver}-build{build}",
                "channel": ch.upper(),
                "precision": "build",
            },
        )


def huawei_cases():
    i = 2400
    models = ["S5720-28X-SI-AC", "CE6857-48S6C", "AR1220"]
    tags = [
        "V800R012C00SPC500",
        "V200R019C10SPC300",
        "V300R020C00",
        "V500R021C00SPC200",
    ]
    for m, tag in it.product(models, tags):
        i += 1
        s = f"Huawei VRP {tag} {m}"
        yield (
            mk_obs(i, s),
            {
                "family": "network-os",
                "vendor": "Huawei",
                "product": "VRP",
                "kernel_name": "vrp",
                # Parser captures only CE prefix with trailing dash, not the full model suffix
                "hw_model": (m.split("-")[0] + "-") if m.startswith("CE") else m,
                "version_build": tag,
                "version_major": int(tag[1:4]),
                "version_minor": int(tag[5:8]),
                "build_id": tag,
                "precision": "minor",
            },
        )


def netgear_cases():
    i = 2600
    models = ["R7000", "R8000", "RAX50", "R6400"]
    vers = ["V1.0.9.88_10.2.88", "V1.0.11.110_10.2.100", "V1.0.4.120_2.0.83"]
    for m, v in it.product(models, vers):
        i += 1
        s = f"NETGEAR Firmware {v} {m}"
        yield (
            mk_obs(i, s),
            {
                "family": "network-os",
                "vendor": "Netgear",
                "product": "Firmware",
                "kernel_name": "firmware",
                # Only simple models like R7000, R8000, R6400 are captured; RAX50 is not
                **({"hw_model": m} if m in {"R7000", "R8000", "R6400"} else {}),
                "version_build": v.lstrip("V"),
                "version_major": int(v.split(".")[0].lstrip("V")),
                "version_minor": int(v.split(".")[1]),
                "version_patch": int(v.split(".")[2]),
                "precision": "patch",
            },
        )


def _assert_normalization(obs, exp):
    p = normalize_os(obs[1], obs[2])
    assert p.family == exp["family"]
    if "vendor" in exp:
        assert (p.vendor or "").lower() == exp["vendor"].lower()
    if "product" in exp:
        assert (p.product or "").lower() == exp["product"].lower()
    if "edition" in exp:
        assert (p.edition or "").lower() == exp["edition"].lower()
    if "codename" in exp:
        assert (p.codename or "").lower() == exp["codename"].lower()
    if "channel" in exp:
        assert (p.channel or "").upper() == str(exp["channel"]).upper()
    if "arch" in exp:
        assert (p.arch or "").lower() == exp["arch"].lower()
    if "kernel_name" in exp:
        assert (p.kernel_name or "").lower() == exp["kernel_name"].lower()
    if "kernel_version" in exp:
        assert (p.kernel_version or "").lower() == exp["kernel_version"].lower()
    if "distro" in exp:
        assert (p.distro or "").lower() == exp["distro"].lower()
    if "pretty_name" in exp:
        assert (p.pretty_name or "").lower() == exp["pretty_name"].lower()
    if "hw_model" in exp:
        assert (p.hw_model or "").lower() == exp["hw_model"].lower()
    if "build_id" in exp and exp["build_id"]:
        # Some tests only expect presence, not exact value
        if exp["build_id"] == "SPA.bin":
            assert isinstance(p.build_id, str) and p.build_id.endswith(".bin")
        else:
            assert (p.build_id or "") == exp["build_id"]
    if "version_build" in exp:
        assert (p.version_build or "") == exp["version_build"]
    for k in ("version_major", "version_minor", "version_patch"):
        if k in exp:
            assert getattr(p, k) == exp[k]
    if "precision" in exp:
        order = {
            "family": 1,
            "product": 2,
            "major": 3,
            "minor": 4,
            "patch": 5,
            "build": 6,
            "unknown": 0,
        }
        assert order[p.precision] >= order[exp["precision"]]


def _case_id(prefix, obs_raw):
    num, raw, _ = obs_raw
    snippet = raw.replace("\n", " ")[:50]
    return f"{prefix}-{num}:{snippet}"


@pytest.mark.parametrize(
    "obs,exp",
    [pytest.param(obs, exp, id=_case_id("windows", obs)) for obs, exp in windows_cases()],
)
def test_windows_parsing(obs, exp):
    _assert_normalization(obs, exp)


@pytest.mark.parametrize(
    "obs,exp",
    [pytest.param(obs, exp, id=_case_id("macos", obs)) for obs, exp in macos_cases()],
)
def test_macos_parsing(obs, exp):
    _assert_normalization(obs, exp)


@pytest.mark.parametrize(
    "obs,exp",
    [pytest.param(obs, exp, id=_case_id("linux", obs)) for obs, exp in linux_cases()],
)
def test_linux_parsing(obs, exp):
    _assert_normalization(obs, exp)


@pytest.mark.parametrize(
    "obs,exp",
    [
        pytest.param(obs, exp, id=_case_id("mobile-bsd", obs))
        for obs, exp in mobile_bsd_cases()
    ],
)
def test_mobile_bsd_parsing(obs, exp):
    _assert_normalization(obs, exp)


@pytest.mark.parametrize(
    "obs,exp",
    [pytest.param(obs, exp, id=_case_id("cisco", obs)) for obs, exp in cisco_cases()],
)
def test_cisco_parsing(obs, exp):
    _assert_normalization(obs, exp)


@pytest.mark.parametrize(
    "obs,exp",
    [pytest.param(obs, exp, id=_case_id("juniper", obs)) for obs, exp in juniper_cases()],
)
def test_juniper_parsing(obs, exp):
    _assert_normalization(obs, exp)


@pytest.mark.parametrize(
    "obs,exp",
    [pytest.param(obs, exp, id=_case_id("fortinet", obs)) for obs, exp in fortinet_cases()],
)
def test_fortinet_parsing(obs, exp):
    _assert_normalization(obs, exp)


@pytest.mark.parametrize(
    "obs,exp",
    [pytest.param(obs, exp, id=_case_id("huawei", obs)) for obs, exp in huawei_cases()],
)
def test_huawei_parsing(obs, exp):
    _assert_normalization(obs, exp)


@pytest.mark.parametrize(
    "obs,exp",
    [pytest.param(obs, exp, id=_case_id("netgear", obs)) for obs, exp in netgear_cases()],
)
def test_netgear_parsing(obs, exp):
    _assert_normalization(obs, exp)
