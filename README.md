# TNSR-Prefix-list-Gen

### Description

A program to create and update prefix lists for Netgate TNSR installations.

### Requirements
- [bgpq4](https://github.com/bgp/bgpq4)
- Python3

### Arguments

- --host \<str>
  ```The address which the restconf server is listening.```
- --asn \<int>
  ```AS number```
- --addressfamily <4/6>
  ```The IP version, '4' for IPv4, '6' for IPv6. '4' is the default value.```
- --auth \<str>
  ```Base64 encoded HTTP basic auth credentials```
- --action <permit/deny>
  ```Action for the prefix list, 'permit' is the default value.```
- --listname \<str>
  ```The name of prefix list```

### Caution

This is a prototype, use it at your own risk.