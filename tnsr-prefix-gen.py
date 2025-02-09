#! /bin/python3

import requests
import json
import subprocess
import argparse

# Function to generate prefix list
def prefix_gen(ASN, AF):
    # Generate bgpq4 command
    cmd = f"bgpq4 -A -F '%n/%l ' -{AF} AS{ASN}"
    try:
        # Run bgpq4 command
        bgpq4_result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        prefixlist = bgpq4_result.stdout.strip().split()
        return prefixlist
    except subprocess.CalledProcessError as e:
        print(f"Error running bgpq4: {e}")
        return []

def main():

    # Define the arguments
    parser = argparse.ArgumentParser(
        prog="TNSR prefix-list generator",
        description="Generate prefix list for specific ASN and address family, then push to TNSR instance via RESTCONF API"
    )

    parser.add_argument("--host", default="localhost", type=str, required=True)
    parser.add_argument("--asn", type=int, required=True)
    parser.add_argument("--addressfamily", default="4", choices=["4", "6"])
    parser.add_argument("--auth", type=str, required=True)
    parser.add_argument("--action", choices=["permit", "deny"], default="permit")
    parser.add_argument("--listname", type=str, required=True)

    args = parser.parse_args()

    # Generate prefix list and generate JSON payload
    prefixlist = prefix_gen(str(args.asn), args.addressfamily)

    rule = []
    sequence = 101

    for prefix in prefixlist:
        rule.append(
            {
                "sequence": sequence,
                "action": args.action,
                "prefix": prefix,
            }
        )
        sequence += 1

    payload = {
        "netgate-frr:rules": {
            "rule": rule
        }
    }
    # Push prefix list to TNSR
    auth = "Basic " + args.auth
    url = f"{args.host}/restconf/data/netgate-route:route-config/dynamic/netgate-frr:prefix-lists/list={args.listname}/rules"
    try:
        commit = requests.put(url, data=json.dumps(payload), headers={"Authorization": auth, "Content-Type": "application/yang-data+json"})
        print("Status:" + str(commit.status_code))
        if commit.status_code not in [201, 204]:
            print("Error pushing prefix list to TNSR:", commit.text)
    except requests.RequestException as e:
        print(f"Error making request to TNSR: {e}")

if __name__ == "__main__":
    main()