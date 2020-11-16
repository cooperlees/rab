# rab

RA Blocker (`rab`) stops RAs while your WAN is down. The code is written
abstractly so we can insert different firewalls to drive + run arbitrary
amounts of "checks" to detect if your WAN is currently down. `rab` will
also keep checking and allow sending of RAs once X checks have passed
Y times again.

## Planned

- Multiple WAN interface support
  - Today we have only tested with 1 WAN interface and 1 check (sure there is bugs)
- On failure also send a RA with lifetime of 0 to encourage clients to defactivate Autoconf + remove this devices as a Gateway
  - This helps fail over to your backup IPv6 connection *(that is recommended to have a lower priority RA advertising)*
- Per interface RA blocking rules
  - Today if any interface fails we block all Outgoing RAs

Will use this a POC to show `system-networkd` and other RA daemons that this functionality is useful for a home/office router.

## Overview

RA Blocker (`rab` for short) takes a config file of "WAN" interface(s) and runs a series of checks
on that interface. If any fail it will block RAs into your "INTERNAL" interface(s) using a firewall.

## Firewalls Supported

`rab` is coded in a way that any firewall support can be added. You just need to subclass Firewall and add
the methods to add and remove the blocking rule(s).

- [nftables](https://nftables.org/)

## Checks

A check is a condition that if it fails, RAs will be blocked on internal ports. Current checks:

- Default route exists on all WAN interfaces

## rab Config

Please refer to [default_config.json](default_config.json). Will document once finalized.

## rab + Docker

rab is designed to run with host networking + capabilities to allow it to manipulate netlink.
Commands to start rab in this mode:

Capabilities:

- `CAP_NET_ADMIN`: Allow manipulation of nftable rules (today via `nft` cli 😢)

Docker Commands:

- `docker pull cooperlees/rab:latest` - Coming once working ...
  - `docker build -t rab .`
- `docker run --name=rab --cap-add=NET_ADMIN --network=host ...`

## Code Design

Remove this when done.

rab/:

- `__init__.py` - Entry point
- `checks.py`
  - Check class
  - DefaultRouteCheck class
- `firewalls.py`
  - Firewall class
  - Nftables class
- `ra.py`
  - RA class class: async send out a RA with lifetime 0 to urge clients to stop using this router + prefixes

## Manual Firewall Commands

### nftables

The manual CLI commands to what `rab` uese. One day we'll hopefully use the nftables netlink API.

#### add rule

```shell
nft insert rule inet filter OUTPUT position 0 icmpv6 type {nd-router-advert} drop
```

#### del rule

```shell
nft delete rule inet filter OUTPUT handle X
```

- X == handle ID integer. To find the handle int:
  - `nft [--json] -n -a list table inet filter`
