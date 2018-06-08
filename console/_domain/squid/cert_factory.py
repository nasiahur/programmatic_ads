from cert_types import Certificate

#
#
#
class CertificateFactory:

    def construct(self, pems):

        result = []
        for pem in pems:
            result.append(self.construct_certificate(pem))

        return result

    def construct_certificate(self, pem):

    	return Certificate(pem)
        