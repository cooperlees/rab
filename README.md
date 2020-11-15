# rab

RA Blocker stops RAs while your WAN is down. This helps having RA's stop
advertising to your Internal LAN when your WAN.

- On failure we also send a RA with lifetime of 0 to encourage clients to remove Autoconf + Gateway
  - This helps fail over to your backup IPv6 connection (that you'll generally have a lower priority RA advertising)

Will use this a POC to show `system-networkd` and other RA daemons that this functionality is useful for a home router.

## Overview

RA Blocker (drb for short) takes a config file of "WAN" interface(s) and runs a series of checks
on that interface and if any fail it will block RAs into your "INTERNAL" interface(s) using a firewalls

## Firewalls Supported

rab is coded in a way that any firewall support can be added. You just need to subclass Firewall and add
the methods to add and remove the blocking rules.

- [nftables](https://nftables.org/)

## Checks

A check is a condition that if it fails, RAs will be blocked on internal ports. Current checks:

- Default route on a/all WAN interfaces

## rab Config

Please refer to [default_config.json](default_config.json). Will document once finalized.

## rab + Docker

rab is designed to run with host networking + capabilities to allow it to manipulate netlink.
Commands to start rab in this mode:

Capabilities:

- `CAP_NET_ADMIN`: Allow manipulation of nftable rules

Docker Commands:

- `docker pull cooperlees/rab:latest` - Coming once working ...
  - `docker build -t rab .`
- `docker run --name=rab --cap-add=NET_ADMIN --network=host ...`

## Code Design

Remove this when done.

rab/:

```console
- __init__.py - Entry point
- checks.py
    - Check class
    - DefaultRouteCheck class
- firewalls.py
    - Firewall class
    - Nftables class
- ra.py
    - RA class class (async send out a RA with lifetime 0)
```

## Manual Firewall Commands

### nftables

The manual CLI commands to what `rab` will do via nftables API.

#### add rule

```shell
nft insert rule inet filter OUTPUT position 0 icmpv6 type {nd-router-advert} drop
```

#### del rule

```shell
nft delete rule inet filter OUTPUT handle X
```

- X == handle ID integer. To find:
  - `nft list table inet filter -n -a`
