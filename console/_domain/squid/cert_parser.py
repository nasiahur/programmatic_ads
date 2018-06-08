import re

#
#
#
class CertificateParser:

    def parse(self, pem_str):

        result  = []
        cert_re = re.compile("(-----BEGIN CERTIFICATE-----.+?-----END CERTIFICATE-----)", re.DOTALL)

        for match in cert_re.finditer(pem_str):
            result.append(match.group(1))

        return result


#path = "test.pem"
#with open(path, "rb") as fin:
#    pem_str = fin.read()

#parser = CertificateParser()
#pems   = parser.parse(pem_str)
#for pem in pems:
#    print pem
