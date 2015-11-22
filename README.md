# IPLoc

Exposes the GeoLite City dataset over HTTP in a quick efficient manner to retrieve location information for an IP

> GeoIP City dataset lets you discover information about a specific IP address

> GeoIP Dataset collected at http://dev.maxmind.com/geoip/legacy/csv/


### Toolset
* Python 2.7.9
* Flask - micro webdevelopment framework for Python


### Usage

Invoke the server by passing in the Location Data csv and IP Data csv to server.py (respectively)

```sh
$ python server.py Data/Location.csv Data/Blocks.csv
```

Alternatively, you can place the files inside the data directory as "Location.csv" and "Blocks.csv" and simply start the server. By default, the server runs on port 5000.
```sh
$ python server.py
Caching Location Data
Caching IP Data
 * Running on http://0.0.0.0:5000/
```
You can test the service by using the linux built in [curl] package to make requests to the server.
```sh
$ curl -L http://localhost:5000/24.45.187.127
{
  "areaCode": "631", 
  "city": "Bayport", 
  "country": "US", 
  "latitude": "40.7479", 
  "longitude": "-73.0559", 
  "metroCode": "501", 
  "postalCode": "11705", 
  "region": "NY"
}
```
You can request specific fields as well
```sh
$ curl -L http://localhost:5000/24.45.187.127/city
{
  "city": "Bayport"
}
```
To request multiple fields, separate field names by commas
```sh
$ curl -L http://localhost:5000/1.0.85.0/city,postalCode
{
  "city": "Okayama", 
  "postalCode": "700-0824"
}
```

The service will return appropriate headers based on the request [200, 301, 400, 500]
```sh
$ curl -i -L http://localhost:5000/1.0.85.0/
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 184
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Mon, 16 Nov 2015 08:40:02 GMT

{
  "areaCode": "", 
  "city": "Okayama", 
  "country": "JP", 
  "latitude": "34.6617", 
  "longitude": "133.9350", 
  "metroCode": "", 
  "postalCode": "700-0824", 
  "region": "31"
}
```

### Benchmarks

Although your mileage may vary, the following times were recorded on a 2013 Macbook Air using the time command [time python server.py]

* (init) Collecting & Storing Location Data [740,245 rows]: 5.938s
* (init) Collecting & Storing IP Data [2,106,714 rows]: 7.543s
* Total IP Retrieval [1.0.85.0]: 0.054s
* Total IP Retrieval [24.45.187.127]: 0.020s
* Total IP Retrieval [223.196.240.4]: 0.030s

### Notes
Considering the api consumes the entire 2 million records of location data directly into memory, it's recommended to host this on a machine with at least 2gb ram

### Todo

 - Allow insertion & deletion of ip addresses / locations
 - Push this onto a cache layer like redis so we can provide constant updates to data
 - Implement ip class bucketing for performance
 - Look into skip lists for ranges - might just be worth it


MIT License