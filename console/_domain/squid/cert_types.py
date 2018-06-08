import base64

#
#
#
class Certificate:

    def __init__(self, pem, is_missing=False):

    	# we do import here to let it run on windows when developing
    	from OpenSSL import crypto

        assert(pem)

        # save members
        self.pem  = pem
        self.x509 = crypto.load_certificate(crypto.FILETYPE_PEM, pem)

        # parse out extensions
        self.extensions = self.collect_extensions(self.x509)
        self.subject    = str(self.x509.get_subject())
        self.issuer     = str(self.x509.get_issuer())

        # the flag indicating we have additionally downloaded this certificate
        self.missing    = is_missing

    def is_missing(self):
        return self.missing

    def common_name(self):
        return self.x509.get_subject().CN

    def valid_from(self):
        return self.x509.get_notBefore()

    def valid_until(self):
        return self.x509.get_notAfter()

    def as_data_uri(self):

        prefix  = 'data:text/plain;base64,'    
        payload = base64.b64encode(self.pem)
        
        return prefix + payload

    def hex_sn(self):

        hex_sn = '{0:X}'.format(int(self.x509.get_serial_number()))
        hex_sn = ':'.join(hex_sn[i:i+2] for i in range(0, len(hex_sn), 2))

        return hex_sn

    def is_ca(self):

        if "basicConstraints" not in self.extensions:
            return False

        name = "basicConstraints"
        value = self.extensions[name]

        if value.find("CA:TRUE") != -1:
            return  True

        return False

    def subjectAltNames(self):

        if "subjectAltName" not in self.extensions:
            return ""

        name = "subjectAltName"
        value = self.extensions[name]

        return str(value)


    def authorityInfoAccess(self):

        if "authorityInfoAccess" not in self.extensions:
            return ("", "")

        name  = "authorityInfoAccess"
        value = self.extensions[name]

        # parse the return values
        ocsp       = ""
        ca_issuers = ""

        # split the value into
        items = value.split("\n")
        for item in items:
            if item.startswith("OCSP"):
                pos = item.find("URI:")
                if pos != -1:
                    temp = item[pos + len("URI:"):]
                    ocsp = temp.strip()

            if item.startswith("CA Issuers"):
                pos = item.find("URI:")
                if pos != -1:
                    temp       = item[pos + len("URI:"):]
                    ca_issuers = temp.strip()

        return (ocsp, ca_issuers)

    def collect_extensions(self, x509):

        extensions = {}

        index = 0
        count = x509.get_extension_count()

        while index < count:

            extension = x509.get_extension(index)
            index    += 1

            # ignore all errors and hope for the best
            try:
                name  = extension.get_short_name()
                if name:
                    extensions[name] = str(extension)
            except Exception as e:
                pass

        return extensions