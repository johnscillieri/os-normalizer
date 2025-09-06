# OS Fingerprint

A Python library for identifying and parsing operating system information from various sources.

## Overview

The OS Fingerprint library is designed to parse raw operating system strings and JSON data to identify the OS family, version, architecture, and other details. It supports parsing of:

- Windows (NT builds, versions)
- macOS (Darwin versions, codenames)
- Linux distributions (Ubuntu, Debian, Red Hat, etc.)
- iOS and Android mobile OS
- BSD variants (FreeBSD, OpenBSD, NetBSD)
- Network operating systems (Cisco IOS, Junos, FortiOS, etc.)

## Installation

```bash
pip install os-fingerprint
```

## Usage

The main entry point is the `normalize_os` function, which takes an `OSObservation` object and returns a structured `OSParse` result.

### Basic Usage

```python
from os_fingerprint import normalize_os
from os_fingerprint.models import OSObservation

# Create an observation with raw OS string
observation = OSObservation(
    observation_id="1",
    asset_anchor_kind="hostname",
    asset_anchor_value="pc-01",
    source="agent-a",
    observed_at="2023-01-01T00:00:00Z",
    raw_os_string="Windows NT 10.0 build 22631 Enterprise x64"
)

# Parse the OS information
result = normalize_os(observation)
print(result.family)  # windows
print(result.product)  # Windows 11
print(result.version_major)  # 11
```

### Using Raw OS JSON Data

```python
from os_fingerprint import normalize_os
from os_fingerprint.models import OSObservation

# Create an observation with both raw string and JSON data
observation = OSObservation(
    observation_id="2",
    asset_anchor_kind="hostname",
    asset_anchor_value="mac-01",
    source="agent-b",
    observed_at="2023-01-01T00:00:00Z",
    raw_os_string="Darwin 24.0.0; macOS Sequoia arm64",
    raw_os_json={
        "arch": "arm64",
        "os_release": 'NAME="Ubuntu"\nID=ubuntu\nVERSION_ID="22.04.4"\nVERSION_CODENAME=jammy\nPRETTY_NAME="Ubuntu 22.04.4 LTS"'
    }
)

result = normalize_os(observation)
print(result.family)  # macos
print(result.product)  # macOS
print(result.codename)  # Sequoia
print(result.arch)  # arm64
```

### Parsing Linux Distributions

```python
from os_fingerprint import normalize_os
from os_fingerprint.models import OSObservation

# Parse Ubuntu Linux
observation = OSObservation(
    observation_id="3",
    asset_anchor_kind="hostname",
    asset_anchor_value="lin-01",
    source="agent-c",
    observed_at="2023-01-01T00:00:00Z",
    raw_os_string="Linux host 5.15.0-122-generic x86_64",
    raw_os_json={
        "arch": None,
        "os_release": 'NAME="Ubuntu"\nID=ubuntu\nVERSION_ID="22.04.4"\nVERSION_CODENAME=jammy\nPRETTY_NAME="Ubuntu 22.04.4 LTS"'
    }
)

result = normalize_os(observation)
print(result.family)  # linux
print(result.product)  # Ubuntu
print(result.version_major)  # 22
print(result.version_minor)  # 4
```

### Parsing Network Operating Systems

```python
from os_fingerprint import normalize_os
from os_fingerprint.models import OSObservation

# Parse Cisco IOS XE
observation = OSObservation(
    observation_id="4",
    asset_anchor_kind="hostname",
    asset_anchor_value="sw-01",
    source="agent-d",
    observed_at="2023-01-01T00:00:00Z",
    raw_os_string="Cisco IOS XE Software, Version 17.9.4a (Amsterdam) C9300-24T, universalk9, c9300-universalk9.17.09.04a.SPA.bin"
)

result = normalize_os(observation)
print(result.family)  # network-os
print(result.vendor)  # Cisco
print(result.product)  # IOS XE
```

## Models

### OSObservation

Represents raw observation data supplied to the normalizer:

- `observation_id`: Unique identifier for the observation
- `asset_anchor_kind`: Type of asset (e.g., "hostname")
- `asset_anchor_value`: Value of the asset anchor (e.g., "pc-01")
- `source`: Source of the observation (e.g., "agent-a")
- `observed_at`: Timestamp when observed
- `raw_os_string`: Raw OS string to parse
- `raw_os_json`: Additional JSON data for parsing (optional)
- `agent_version`: Agent version (optional)
- `collection_method`: Method of collection (optional)
- `hash`: Hash value (optional)

### OSParse

Represents structured operating system information:

- `observation_id`: Reference to the observation ID
- `family`: OS family (windows, linux, macos, ios, android, bsd, network-os)
- `vendor`: Vendor name (Microsoft, Apple, Cisco, etc.)
- `product`: Product name (Windows 11, Ubuntu, macOS, etc.)
- `edition`: Edition information (Pro, Enterprise, etc.)
- `codename`: Release codename (Sequoia, Ventura, etc.)
- `channel`: Release channel (GA, LTS, etc.)
- `version_major`, `version_minor`, `version_patch`, `version_build`: Version components
- `kernel_name`, `kernel_version`: Kernel details
- `arch`: Architecture (x86_64, arm64, etc.)
- `flavor`: Flavor (desktop, server, mobile, etc.)
- `distro`: Distribution name
- `like_distros`: List of similar distributions
- `pretty_name`: Pretty formatted name
- `hw_model`, `build_id`: Network device details
- `precision`: Precision level (family, product, major, minor, patch, build)
- `confidence`: Confidence score (0.0 to 1.0)
- `evidence`: Evidence used for parsing decisions
- `os_key`: Canonical key for deduplication

## Architecture

The library follows a modular architecture:

- **orchestrator.py**: Main orchestration logic that delegates to appropriate parsers
- **parsers/**: OS-specific parsers (macOS, Linux, Windows, Network, Mobile, BSD)
- **models.py**: Data models for observations and parsed results
- **constants.py**: Static lookup tables (aliases, build maps, codenames)
- **helpers.py**: Utility functions (architecture extraction, confidence calculation)

## Contributing

Contributions are welcome! Please ensure that any new parsers or improvements follow the existing code patterns and include appropriate tests.

## License

MIT
