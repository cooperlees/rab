#!/usr/bin/env python3

import json


NFTABLES_TABLE_JSON_NO_RULE = json.loads(
    """\
{
  "nftables": [
    {
      "metainfo": {
        "version": "0.9.6",
        "release_name": "Capital Idea #2",
        "json_schema_version": 1
      }
    },
    {
      "table": {
        "family": "inet",
        "name": "filter",
        "handle": 9
      }
    },
    {
      "chain": {
        "family": "inet",
        "table": "filter",
        "name": "INPUT",
        "handle": 1,
        "type": "filter",
        "hook": "input",
        "prio": 0,
        "policy": "drop"
      }
    },
    {
      "rule": {
        "family": "inet",
        "table": "filter",
        "chain": "INPUT",
        "handle": 5,
        "expr": [
          {
            "match": {
              "op": "==",
              "left": {
                "payload": {
                  "protocol": "icmp",
                  "field": "type"
                }
              },
              "right": 8
            }
          },
          {
            "counter": {
              "packets": 0,
              "bytes": 0
            }
          },
          {
            "accept": null
          }
        ]
      }
    },
    {
      "rule": {
        "family": "inet",
        "table": "filter",
        "chain": "INPUT",
        "handle": 6,
        "expr": [
          {
            "match": {
              "op": "==",
              "left": {
                "payload": {
                  "protocol": "ip6",
                  "field": "nexthdr"
                }
              },
              "right": 58
            }
          },
          {
            "counter": {
              "packets": 0,
              "bytes": 0
            }
          },
          {
            "accept": null
          }
        ]
      }
    },
    {
      "rule": {
        "family": "inet",
        "table": "filter",
        "chain": "INPUT",
        "handle": 7,
        "expr": [
          {
            "match": {
              "op": "in",
              "left": {
                "ct": {
                  "key": "state"
                }
              },
              "right": [
                2,
                4
              ]
            }
          },
          {
            "counter": {
              "packets": 12666,
              "bytes": 59890465
            }
          },
          {
            "accept": null
          }
        ]
      }
    },
    {
      "rule": {
        "family": "inet",
        "table": "filter",
        "chain": "INPUT",
        "handle": 8,
        "expr": [
          {
            "match": {
              "op": "in",
              "left": {
                "ct": {
                  "key": "state"
                }
              },
              "right": 1
            }
          },
          {
            "counter": {
              "packets": 0,
              "bytes": 0
            }
          },
          {
            "drop": null
          }
        ]
      }
    },
    {
      "rule": {
        "family": "inet",
        "table": "filter",
        "chain": "INPUT",
        "handle": 9,
        "expr": [
          {
            "match": {
              "op": "==",
              "left": {
                "meta": {
                  "key": "iifname"
                }
              },
              "right": "lo"
            }
          },
          {
            "counter": {
              "packets": 103,
              "bytes": 8763
            }
          },
          {
            "accept": null
          }
        ]
      }
    },
    {
      "rule": {
        "family": "inet",
        "table": "filter",
        "chain": "INPUT",
        "handle": 10,
        "expr": [
          {
            "match": {
              "op": "==",
              "left": {
                "payload": {
                  "protocol": "tcp",
                  "field": "dport"
                }
              },
              "right": 22
            }
          },
          {
            "counter": {
              "packets": 1,
              "bytes": 64
            }
          },
          {
            "accept": null
          }
        ]
      }
    },
    {
      "rule": {
        "family": "inet",
        "table": "filter",
        "chain": "INPUT",
        "handle": 11,
        "expr": [
          {
            "match": {
              "op": "==",
              "left": {
                "payload": {
                  "protocol": "udp",
                  "field": "dport"
                }
              },
              "right": {
                "range": [
                  67,
                  68
                ]
              }
            }
          },
          {
            "counter": {
              "packets": 0,
              "bytes": 0
            }
          },
          {
            "accept": null
          }
        ]
      }
    },
    {
      "rule": {
        "family": "inet",
        "table": "filter",
        "chain": "INPUT",
        "handle": 12,
        "expr": [
          {
            "match": {
              "op": "==",
              "left": {
                "payload": {
                  "protocol": "udp",
                  "field": "dport"
                }
              },
              "right": 547
            }
          },
          {
            "counter": {
              "packets": 0,
              "bytes": 0
            }
          },
          {
            "accept": null
          }
        ]
      }
    },
    {
      "rule": {
        "family": "inet",
        "table": "filter",
        "chain": "INPUT",
        "handle": 13,
        "expr": [
          {
            "counter": {
              "packets": 341,
              "bytes": 75782
            }
          },
          {
            "jump": {
              "target": "LOGGING"
            }
          }
        ]
      }
    },
    {
      "chain": {
        "family": "inet",
        "table": "filter",
        "name": "FORWARD",
        "handle": 2,
        "type": "filter",
        "hook": "forward",
        "prio": 0,
        "policy": "drop"
      }
    },
    {
      "chain": {
        "family": "inet",
        "table": "filter",
        "name": "OUTPUT",
        "handle": 3,
        "type": "filter",
        "hook": "output",
        "prio": 0,
        "policy": "accept"
      }
    },
    {
      "chain": {
        "family": "inet",
        "table": "filter",
        "name": "LOGGING",
        "handle": 4
      }
    },
    {
      "rule": {
        "family": "inet",
        "table": "filter",
        "chain": "LOGGING",
        "handle": 14,
        "expr": [
          {
            "limit": {
              "rate": 2,
              "per": "minute"
            }
          },
          {
            "counter": {
              "packets": 105,
              "bytes": 22995
            }
          },
          {
            "log": {
              "prefix": "nft-dropped: "
            }
          }
        ]
      }
    },
    {
      "rule": {
        "family": "inet",
        "table": "filter",
        "chain": "LOGGING",
        "handle": 15,
        "expr": [
          {
            "counter": {
              "packets": 341,
              "bytes": 75782
            }
          },
          {
            "drop": null
          }
        ]
      }
    }
  ]
}
"""
)


NFTABLES_TABLE_JSON_ONE_RULE = json.loads(
    """\
{
  "nftables": [
    {
      "metainfo": {
        "version": "0.9.6",
        "release_name": "Capital Idea #2",
        "json_schema_version": 1
      }
    },
    {
      "table": {
        "family": "inet",
        "name": "filter",
        "handle": 9
      }
    },
    {
      "chain": {
        "family": "inet",
        "table": "filter",
        "name": "INPUT",
        "handle": 1,
        "type": "filter",
        "hook": "input",
        "prio": 0,
        "policy": "drop"
      }
    },
    {
      "rule": {
        "family": "inet",
        "table": "filter",
        "chain": "INPUT",
        "handle": 5,
        "expr": [
          {
            "match": {
              "op": "==",
              "left": {
                "payload": {
                  "protocol": "icmp",
                  "field": "type"
                }
              },
              "right": 8
            }
          },
          {
            "counter": {
              "packets": 0,
              "bytes": 0
            }
          },
          {
            "accept": null
          }
        ]
      }
    },
    {
      "rule": {
        "family": "inet",
        "table": "filter",
        "chain": "INPUT",
        "handle": 6,
        "expr": [
          {
            "match": {
              "op": "==",
              "left": {
                "payload": {
                  "protocol": "ip6",
                  "field": "nexthdr"
                }
              },
              "right": 58
            }
          },
          {
            "counter": {
              "packets": 0,
              "bytes": 0
            }
          },
          {
            "accept": null
          }
        ]
      }
    },
    {
      "rule": {
        "family": "inet",
        "table": "filter",
        "chain": "INPUT",
        "handle": 7,
        "expr": [
          {
            "match": {
              "op": "in",
              "left": {
                "ct": {
                  "key": "state"
                }
              },
              "right": [
                2,
                4
              ]
            }
          },
          {
            "counter": {
              "packets": 14799,
              "bytes": 60069204
            }
          },
          {
            "accept": null
          }
        ]
      }
    },
    {
      "rule": {
        "family": "inet",
        "table": "filter",
        "chain": "INPUT",
        "handle": 8,
        "expr": [
          {
            "match": {
              "op": "in",
              "left": {
                "ct": {
                  "key": "state"
                }
              },
              "right": 1
            }
          },
          {
            "counter": {
              "packets": 0,
              "bytes": 0
            }
          },
          {
            "drop": null
          }
        ]
      }
    },
    {
      "rule": {
        "family": "inet",
        "table": "filter",
        "chain": "INPUT",
        "handle": 9,
        "expr": [
          {
            "match": {
              "op": "==",
              "left": {
                "meta": {
                  "key": "iifname"
                }
              },
              "right": "lo"
            }
          },
          {
            "counter": {
              "packets": 118,
              "bytes": 10014
            }
          },
          {
            "accept": null
          }
        ]
      }
    },
    {
      "rule": {
        "family": "inet",
        "table": "filter",
        "chain": "INPUT",
        "handle": 10,
        "expr": [
          {
            "match": {
              "op": "==",
              "left": {
                "payload": {
                  "protocol": "tcp",
                  "field": "dport"
                }
              },
              "right": 22
            }
          },
          {
            "counter": {
              "packets": 1,
              "bytes": 64
            }
          },
          {
            "accept": null
          }
        ]
      }
    },
    {
      "rule": {
        "family": "inet",
        "table": "filter",
        "chain": "INPUT",
        "handle": 11,
        "expr": [
          {
            "match": {
              "op": "==",
              "left": {
                "payload": {
                  "protocol": "udp",
                  "field": "dport"
                }
              },
              "right": {
                "range": [
                  67,
                  68
                ]
              }
            }
          },
          {
            "counter": {
              "packets": 0,
              "bytes": 0
            }
          },
          {
            "accept": null
          }
        ]
      }
    },
    {
      "rule": {
        "family": "inet",
        "table": "filter",
        "chain": "INPUT",
        "handle": 12,
        "expr": [
          {
            "match": {
              "op": "==",
              "left": {
                "payload": {
                  "protocol": "udp",
                  "field": "dport"
                }
              },
              "right": 547
            }
          },
          {
            "counter": {
              "packets": 0,
              "bytes": 0
            }
          },
          {
            "accept": null
          }
        ]
      }
    },
    {
      "rule": {
        "family": "inet",
        "table": "filter",
        "chain": "INPUT",
        "handle": 13,
        "expr": [
          {
            "counter": {
              "packets": 669,
              "bytes": 152685
            }
          },
          {
            "jump": {
              "target": "LOGGING"
            }
          }
        ]
      }
    },
    {
      "chain": {
        "family": "inet",
        "table": "filter",
        "name": "FORWARD",
        "handle": 2,
        "type": "filter",
        "hook": "forward",
        "prio": 0,
        "policy": "drop"
      }
    },
    {
      "chain": {
        "family": "inet",
        "table": "filter",
        "name": "OUTPUT",
        "handle": 3,
        "type": "filter",
        "hook": "output",
        "prio": 0,
        "policy": "accept"
      }
    },
    {
      "rule": {
        "family": "inet",
        "table": "filter",
        "chain": "OUTPUT",
        "handle": 17,
        "expr": [
          {
            "match": {
              "op": "==",
              "left": {
                "payload": {
                  "protocol": "icmpv6",
                  "field": "type"
                }
              },
              "right": {
                "set": [
                  134
                ]
              }
            }
          },
          {
            "drop": null
          }
        ]
      }
    },
    {
      "chain": {
        "family": "inet",
        "table": "filter",
        "name": "LOGGING",
        "handle": 4
      }
    },
    {
      "rule": {
        "family": "inet",
        "table": "filter",
        "chain": "LOGGING",
        "handle": 14,
        "expr": [
          {
            "limit": {
              "rate": 2,
              "per": "minute"
            }
          },
          {
            "counter": {
              "packets": 222,
              "bytes": 47940
            }
          },
          {
            "log": {
              "prefix": "nft-dropped: "
            }
          }
        ]
      }
    },
    {
      "rule": {
        "family": "inet",
        "table": "filter",
        "chain": "LOGGING",
        "handle": 15,
        "expr": [
          {
            "counter": {
              "packets": 669,
              "bytes": 152685
            }
          },
          {
            "drop": null
          }
        ]
      }
    }
  ]
}
"""
)
