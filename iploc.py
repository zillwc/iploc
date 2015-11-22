import csv

class IpLoc(object):
    def __init__(self, loc_filename=None, ips_filename=None):
        self._locData = self.collect_location_data(loc_filename)
        self._ipData = self.collect_ip_data(ips_filename)

    def lookup(self, ip):
        """Searches for an ip address and returns the location associated with it"""
        ipint = self.convert_ip_to_int(ip)
        isFound = False
        isDivisible = False
        if self._ipData.get(str(ipint)) is not None:
            isFound = True
        if isFound is False and ipint % 2 is not 0:
            ipint -= 1
        while isFound is False and ipint > 16000000:
            if self._ipData.get(str(ipint)) is not None:
                isFound = True
                break
            if isDivisible:
                ipint = ipint - 2
                isDivisible = False
            while ipint % 256 is not 0:
                ipint = ipint - 2
                isDivisible = True
        if self._ipData.get(str(ipint)) is not None:
            locID = str(self._ipData[str(ipint)].get('locID'))
            return self._locData[locID]
        else:
            return str(ipint) + " does not exist inside data range"

    def collect_ip_data(self, ips_filename):
        """Reads the IP data csv file and stores the content into memory at the startrange index"""
        ip_data = {}
        print "Caching IP Data"
        try:
            fh = open(ips_filename, 'rt')
            reader = csv.reader(fh)
            index = 0
            startIndex = 2
            for row in reader:
                if index < startIndex:
                    index = index + 1
                    continue
                ip_data[row[0]] = {
                    "endRange": row[1],
                    "locID": row[2]
                }
        except IOError as ioexc:
            raise IOError(str(ioexc))
        except Exception as exc:
            raise ValueError(str(exc))
        else:
            return ip_data

    def collect_location_data(self, loc_filename):
        """Reads the location csv file and stores the content into memory at the locID index"""
        loc_data = {}
        print "Caching Location Data"
        try:
            fh = open(loc_filename, 'rt')
            reader = csv.reader(self.reencode(fh))
            index = 0
            startIndex = 2
            for row in reader:
                if index < startIndex:
                    index = index + 1
                    continue
                loc_data[row[0]] = {
                    "country": row[1],
                    "region": row[2],
                    "city": row[3],
                    "postalCode": row[4],
                    "latitude": row[5],
                    "longitude": row[6],
                    "metroCode": row[7],
                    "areaCode": row[8]
                }
        except IOError as ioexc:
            raise IOError(str(ioexc))
        except Exception as exc:
            raise ValueError(str(exc))
        else:
            return loc_data

    def convert_ip_to_int(self, ip_addr):
        """Converts the ip address into an integer"""
        (o1, o2, o3, o4) = ip_addr.split('.')
        integer_ip = (16777216 * int(o1)) + (65536 * int(o2)) + (256 * int(o3)) + int(o4)
        return integer_ip

    def reencode(self, file):
        """Reencoding the line to utf8"""
        for line in file:
            yield line.decode('windows-1250').encode('utf-8')
