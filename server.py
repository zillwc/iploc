# -*- coding: utf-8 -*-
"""
    IPLoc
    Retrieve location information for an IP
"""

import sys
from iploc import IpLoc
from flask import Flask, jsonify, abort, make_response

app = Flask(__name__)

@app.route("/<ip_addr>/")
def ip_search(ip_addr=None):
    if ip_addr is None:
        abort(make_response("Error: Missing IP Address", 400))
    if not is_valid_ipv4(ip_addr):
        abort(make_response("Error: Invalid IP Address", 400))
    loc_data = iploc.lookup(ip_addr)
    return jsonify(loc_data)

@app.route("/<ip_addr>/<key>/")
def ip_search_by_key(ip_addr=None, key=None):
    if ip_addr is None or key is None:
        abort(make_response("Error: Invalid parameters provided", 400))
    if not is_valid_ipv4(ip_addr):
        abort(make_response("Error: Invalid IP Address", 400))
    loc_data = iploc.lookup(ip_addr)
    response_obj = {}
    keys = key.split(',')
    for k in keys:
        if loc_data.get(str(k)) is not None:
            response_obj[k] = loc_data.get(str(k))
    return jsonify(response_obj)

def is_valid_ipv4(addr):
    pieces = addr.split('.')
    if len(pieces) != 4: return False
    try: return all(0<=int(p)<256 for p in pieces)
    except ValueError: return False

defaults = {
    "loc_data_file": 'data/Location.csv',
    "ips_data_file": 'data/Blocks.csv'
}

if len(sys.argv) < 3:
    loc_file = defaults['loc_data_file']
    ips_file = defaults['ips_data_file']
else:
    loc_file = sys.argv[1]
    ips_file = sys.argv[2]

iploc = IpLoc(loc_file, ips_file)
app.run(host='0.0.0.0')