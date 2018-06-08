import urllib2

from cert_types import Certificate

#
# here we assume the first cert IS the site cert (leaf)!
#
class CertChainResolver:

    def resolve(self, certs):

        # there must be at least ONE certificate in the chain
        assert(certs)

        # we will be building a resolved copy of certification chain here
        resolved = []

        # make a copy of certs
        cloned = certs[:]

        # now analyze the rest
        while len(cloned) > 0:

            # get item at index 0
            cert = cloned.pop(0)

            # see if the issuer certificate is found
            issuer = self.pop_issuer(cloned, cert)
            if issuer is None:

                # no, there is NO issuer in the certificate chain, download it
                issuer = self.download_issuer(cert)

                # here issue may still be none if download failed

            # good we have the issuer, push it back as first element
            if issuer is not None:
                cloned.insert(0, issuer)

            # do not forget to add the resolved cert
            resolved.append(cert)

        # when we get here there should be fully resolved certificate chain in 'resolved'
        assert(len(resolved) >= len(certs))

        # there are may be some dangling certificates left, add them too
        resolved.extend(cloned)

        # and return the resolved chain
        return resolved

    def pop_issuer(self, cloned, cert):

        issuer = str(cert.x509.get_issuer())

        index = 0        
        for element in cloned:
            
            subject = str(element.x509.get_subject())
            if issuer == subject:

                # found it, remove from list
                del cloned[index]

                # and return
                return element

        # if we got here no such element exists
        return None

    def download_issuer(self, cert):

        result = None
        error  = ""

        try:
            (ocsp, ca_issuers) = cert.authorityInfoAccess()
            if ca_issuers:

                if ca_issuers.startswith("http://") or ca_issuers.startswith("https://"):

                    response     = urllib2.urlopen(ca_issuers)
                    content_type = response.info().type
                    payload      = response.read()

                    if payload.startswith("-----BEGIN CERTIFICATE-----"):
                        return Certificate(payload, True)
                    else:
                        raise Exception("Cannot parse the AIA field of URI '%s', Content-Type: '%s'" % (ca_issuers, content_type))

        except Exception as e:
            result = None
            error  = str(e)

        return result