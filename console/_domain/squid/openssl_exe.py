import os

#
#
#
from _domain.core import System

#
#
#
from binary_openssl import BinaryOpenSsl

#
#
#
class OpenSslParser:

    def parse(self, data):

        certs      = []
        collecting = False
        cert       = ""

        for line in data:
            if not collecting:

                if line.find("-----BEGIN CERTIFICATE-----") != -1:
                    cert       = line
                    collecting = True

                else:
                    continue

            else:
                cert += line        
    
                if line.find("-----END CERTIFICATE-----") != -1:
                    collecting  = False
                    certs.append(cert)
                
        return certs

#
#
#
class OpenSslExe:

    def run(self, server_name, server_port, output_file):

        if System.name() == System.WS_WINDOWS:
            return self.debug_certs(server_name)

        openssl_exe = BinaryOpenSsl.full_path()
        command     = "%s s_client -showcerts -connect %s:%d </dev/null >%s 2>&1" % (openssl_exe, server_name, server_port, output_file)
        exit_code   = os.system(command)
        if exit_code != 0:
            raise Exception("Failed to run: %s" % command)

        contents = []
        with open(output_file, "r") as fin:
            contents = fin.readlines()

        return contents

    def debug_certs(self, server_name):

        if server_name == "www.diladele.com":
            return self.debug_certs_diladele()

        if server_name == "www.google.com":
            return self.debug_certs_google()

        if server_name == "www.apexclearing.com":
            return self.debug_certs_apexclearing()

        if server_name == "pcwebshop.co.uk":
            return self.debug_certs_pcwebshop_co_uk()

        return self.debug_certs_diladele()

    def debug_certs_diladele(self):

        intermediate_cert_pem = """-----BEGIN CERTIFICATE-----
MIIE3DCCA8SgAwIBAgIQPiM0Wu0sClF7Jt7UgB0QqjANBgkqhkiG9w0BAQsFADCB
rjELMAkGA1UEBhMCVVMxFTATBgNVBAoTDHRoYXd0ZSwgSW5jLjEoMCYGA1UECxMf
Q2VydGlmaWNhdGlvbiBTZXJ2aWNlcyBEaXZpc2lvbjE4MDYGA1UECxMvKGMpIDIw
MDggdGhhd3RlLCBJbmMuIC0gRm9yIGF1dGhvcml6ZWQgdXNlIG9ubHkxJDAiBgNV
BAMTG3RoYXd0ZSBQcmltYXJ5IFJvb3QgQ0EgLSBHMzAeFw0xNDA2MTAwMDAwMDBa
Fw0yNDA2MDkyMzU5NTlaMGUxCzAJBgNVBAYTAlVTMRUwEwYDVQQKEwx0aGF3dGUs
IEluYy4xHTAbBgNVBAsTFERvbWFpbiBWYWxpZGF0ZWQgU1NMMSAwHgYDVQQDExd0
aGF3dGUgRFYgU1NMIFNIQTI1NiBDQTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCC
AQoCggEBALOsDX+tuxNNlF9nQmrQiXGp7XQEkyTITVah8JGWhNmEas9SIeMasVRM
5saenks4qZZUHfWz7ZIE0G5UkG4v6X2YtIotEqO0Qkcdf19A4fx/kaYB3FWkUHgq
Yz+EfizIKyG2xg5evLix1BuYs8b44ego7TJEG8t/9+SxEevGCLBb7qjC7Eaqjynf
ubekA6A1elg/iylHwdIi+izGx2zN0/dYMpOU0W+pKpwPCiiSqxQKtt/tQHpkB1TO
6nWXMrmWoHXJdzECdK9Ud0+ZooFLeVm4kj/5B+pCdFcuNexVivxhPD5XcZI7q+TB
4RcsZDYAhLV8Gn2wQTN8I/ZOd1oswUsCAwEAAaOCATwwggE4MC4GCCsGAQUFBwEB
BCIwIDAeBggrBgEFBQcwAYYSaHR0cDovL3Quc3ltY2QuY29tMBIGA1UdEwEB/wQI
MAYBAf8CAQAwQQYDVR0gBDowODA2BgpghkgBhvhFAQc2MCgwJgYIKwYBBQUHAgEW
Gmh0dHBzOi8vd3d3LnRoYXd0ZS5jb20vY3BzMDQGA1UdHwQtMCswKaAnoCWGI2h0
dHA6Ly90LnN5bWNiLmNvbS9UaGF3dGVQQ0EtRzMuY3JsMA4GA1UdDwEB/wQEAwIB
BjApBgNVHREEIjAgpB4wHDEaMBgGA1UEAxMRU3ltYW50ZWNQS0ktMS02OTUwHQYD
VR0OBBYEFH0pMS/BHm6uMQVqs+sczandroCaMB8GA1UdIwQYMBaAFK1sqpRgnO3k
//o+CnQrYwP3tlm/MA0GCSqGSIb3DQEBCwUAA4IBAQA2/6LxHH65UXuU01p7SCXT
N6KCKi1fOB6HZ+zJMavXkjO4vTXKsYBwBIJ8iMw3LhZ0bpNAY8qNe/8HKOb5M6vw
YY09yoPFUNi9aTkfrry37hXFjQQGIDMoBJnFnBH1AQ9HXtiJmaXOwoD+Rvrvthuo
kbKDs+JXDRrkltW8971tA/hifuv4Qgn+CWSkyVy40jkLeQKeFTkdwNnNHF9odo3z
Hi36v6dJog2X9ZbC6WzUzUcLi4oBi9v6z5J1Lt4+p3O1/gNRp0LDx0JrqW++9iDh
jr+fCY7lCOiSk3c+SUScf+l5nf9Lr+A4VzQNXxEyEpKpYYiBpR74oPBFWoZxIIWF
-----END CERTIFICATE-----
"""
        intermediate_server_cert_pem = """-----BEGIN CERTIFICATE-----
MIIGhjCCBW6gAwIBAgIQbeUfUMelWFHuQp7HqsVLsDANBgkqhkiG9w0BAQsFADBl
MQswCQYDVQQGEwJVUzEVMBMGA1UEChMMdGhhd3RlLCBJbmMuMR0wGwYDVQQLExRE
b21haW4gVmFsaWRhdGVkIFNTTDEgMB4GA1UEAxMXdGhhd3RlIERWIFNTTCBTSEEy
NTYgQ0EwHhcNMTYwOTIxMDAwMDAwWhcNMTkwOTIxMjM1OTU5WjAbMRkwFwYDVQQD
DBB3d3cuZGlsYWRlbGUuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKC
AQEAxOXJj9StP8tZKW5fwSkf1Ph3R0ovDa5Xw2No/3EF0eSxyH3ceTWuygnvM6rV
PTST9yZcDVDZDj6u98HK952pxWIi6XrIZU2TWbZHuZBQs9faY2qCRzkl/yrPcppp
xO+j4szHn4lNeRj+I6QJWoMaPGsqUQjVDGcIyK62Js66wez+HQOllUyic+dyZc2H
F8s6piwKc94E3A0tL6UUrCQ2qLcsMLbcqit1X0d103gxHjZkyywLGZuLSglMZirb
mcV96t9agcgb/Pnl3FXTJ0Y+/NOz+IW17oi4Nhy0gCR2Pj9S6PYZmmUiAy55fBsl
BqbfjkXwwvv12aFZljV7WcIduwIDAQABo4IDejCCA3YwKQYDVR0RBCIwIIIQd3d3
LmRpbGFkZWxlLmNvbYIMZGlsYWRlbGUuY29tMAkGA1UdEwQCMAAwKwYDVR0fBCQw
IjAgoB6gHIYaaHR0cDovL3RtLnN5bWNiLmNvbS90bS5jcmwwbgYDVR0gBGcwZTBj
BgZngQwBAgEwWTAmBggrBgEFBQcCARYaaHR0cHM6Ly93d3cudGhhd3RlLmNvbS9j
cHMwLwYIKwYBBQUHAgIwIwwhaHR0cHM6Ly93d3cudGhhd3RlLmNvbS9yZXBvc2l0
b3J5MB8GA1UdIwQYMBaAFH0pMS/BHm6uMQVqs+sczandroCaMA4GA1UdDwEB/wQE
AwIFoDAdBgNVHSUEFjAUBggrBgEFBQcDAQYIKwYBBQUHAwIwVwYIKwYBBQUHAQEE
SzBJMB8GCCsGAQUFBzABhhNodHRwOi8vdG0uc3ltY2QuY29tMCYGCCsGAQUFBzAC
hhpodHRwOi8vdG0uc3ltY2IuY29tL3RtLmNydDCCAfYGCisGAQQB1nkCBAIEggHm
BIIB4gHgAHYA3esdK3oNT6Ygi4GtgWhwfi6OnQHVXIiNPRHEzbbsvswAAAFXS9rG
owAABAMARzBFAiBjmnEFWwh2nQA2nZ9HQmGiMbnUp7KerMsVr+nUSJ28DwIhALEy
TGekJd42UrtMvG0IXbhfogFyj8u/LV4c12YMev2nAHcAaPaY+B9kgr46jO65KB1M
/HFRXWeT1ETRCmesu09P+8QAAAFXS9rGwAAABAMASDBGAiEAn2Lqv/ZnljhGLaHW
A1rpQ4sS6VY9S//vpZ1GjImh/okCIQCC71yLn+MKo6cCIuyzFvKpM9FIIJwwubUu
VWWgo8Z/ZQB2AO5Lvbd1zmC64UJpH6vhnmajD35fsHLYgwDEe4l6qP3LAAABV0va
yKYAAAQDAEcwRQIgDQtrxk+ogO2GpfAVG3gfJXz69GbJ5gwxG0kL6K+Eum0CIQCE
tnmY9OvnP0de3PUbeYbafKse1+8d1bW9LTbifTXi/QB1ALx44d/F9jxoRkkzTaEP
oV8JeWkgCcCBtPP2kX8+2bilAAABV0vax5MAAAQDAEYwRAIgSMTy1CFYtcrx8c0o
5a0LOLRO7kCzSrSbTUZ8xUWLjY4CIGoFayzzsUEt/AMbVRURzsDlDkfx7fYYzhnv
GfbvybmWMA0GCSqGSIb3DQEBCwUAA4IBAQB+XDiXwZBkgcwXqDm6kACuF6kcTlBV
ecAnRV8r7kEPpv0P5iOWqGBn77yjDUMzPKUQ6PCLkjlOa1VvmuMcrfGGH42ywqsw
GXyy8QWPU1H8vZ/9r+YYl2DV551TOg9bGe0RWmHdV6zXBi6SK0UIH1LvQ4CklPc+
V4pzQeApsCHLqsq4hlPOGZlGNTuB+oNqo6Bl7rB1WVXf/NZ5zIi3VCoeSUbGpbm1
2UQhDEsv55e0U89oHhL8hFCEpbVEAMD17DnPZDAMcTO7etS3t/oJYcXfI1ky84pH
bBE4nELBFF6/CqQna2LEggQKTvr5J0RCTP+6Lc62LWz5zNGYHiiQcwzO
-----END CERTIFICATE-----
"""

        lines1 = intermediate_server_cert_pem.split('\n')
        lines2 = intermediate_cert_pem.split('\n')

        result = []
        for line in lines1:
            result.append(line + "\n")
        for line in lines2:
            result.append(line + "\n")

        return result

    def debug_certs_pcwebshop_co_uk(self):

        leaf_pem = """-----BEGIN CERTIFICATE-----
MIIFDTCCA/WgAwIBAgISESE0thXW5HF9cIwD53nSHbYHMA0GCSqGSIb3DQEBCwUA
MGAxCzAJBgNVBAYTAkJFMRkwFwYDVQQKExBHbG9iYWxTaWduIG52LXNhMTYwNAYD
VQQDEy1HbG9iYWxTaWduIERvbWFpbiBWYWxpZGF0aW9uIENBIC0gU0hBMjU2IC0g
RzIwHhcNMTQwNDEwMDc0NzI4WhcNMTgwMTEwMTQzNzAzWjBDMSEwHwYDVQQLExhE
b21haW4gQ29udHJvbCBWYWxpZGF0ZWQxHjAcBgNVBAMMFSouc2VjdXJlLXNlY3Vy
ZS5jby51azCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAMDiJQGwDqkr
iHmWBDBlBcnqmbBHBE1kjfNAwA7RdQ0+/GLF17G5xIkB9cGodSwXjpHv4GYHaKJ9
dlB/ItJKIt0o5ELg0qn2co7c6AofJRju7AN1nX3via4+B9CDWuE4PnNYYykTCu0S
xSruUzaNMclQdZDpPVOvqF9mJPMi+v+AbXaCjas/4lGxwatPAHhmz0iXr0rjEANI
uk6jL9CvOI5nu48hRtOTLM/6s85AAhduD0GrvoPzwfxOoeSL6luLNOljuuekbzGG
kI4k9WoE6lNvKhgFc2b1+pqNnthDWfdYj5vUTSZa8y1Y0TaALBLwShvxzg20rM8m
ggvmMrGftvMCAwEAAaOCAdwwggHYMA4GA1UdDwEB/wQEAwIFoDBJBgNVHSAEQjBA
MD4GBmeBDAECATA0MDIGCCsGAQUFBwIBFiZodHRwczovL3d3dy5nbG9iYWxzaWdu
LmNvbS9yZXBvc2l0b3J5LzA1BgNVHREELjAsghUqLnNlY3VyZS1zZWN1cmUuY28u
dWuCE3NlY3VyZS1zZWN1cmUuY28udWswCQYDVR0TBAIwADAdBgNVHSUEFjAUBggr
BgEFBQcDAQYIKwYBBQUHAwIwQwYDVR0fBDwwOjA4oDagNIYyaHR0cDovL2NybC5n
bG9iYWxzaWduLmNvbS9ncy9nc2RvbWFpbnZhbHNoYTJnMi5jcmwwgZQGCCsGAQUF
BwEBBIGHMIGEMEcGCCsGAQUFBzAChjtodHRwOi8vc2VjdXJlLmdsb2JhbHNpZ24u
Y29tL2NhY2VydC9nc2RvbWFpbnZhbHNoYTJnMnIxLmNydDA5BggrBgEFBQcwAYYt
aHR0cDovL29jc3AyLmdsb2JhbHNpZ24uY29tL2dzZG9tYWludmFsc2hhMmcyMB0G
A1UdDgQWBBRIHT4DDamF8yvrtpgZeS/xfXa0tDAfBgNVHSMEGDAWgBTqTnzUgC3l
FYGGJoyCbcCYpM+XDzANBgkqhkiG9w0BAQsFAAOCAQEACY5Fzl3iEmONLbuu+q0C
Taq+JkJ4LbjWG5mCD+f0wDVoLeY9LkkkJIz5iMw9sfPIEnBhX2/68XUNqRz3IdHk
jjLV7CYyOgnjEJSC6wWO/UprY7GCs+UQZOOM8PafgO7etc9WXYCC/+yOBaH0isI2
GuZePcWZKw6XB6ZAVMXdbi75LJdGR4y8gMQig7LwKAMzVR94zsgRPcFofOv1TXvN
cMsJ3WuRp5GsUJ/9ryGz7apx4ZNA9wPK0nqW1zU4MojgYl4U96zcYX+WXeXkvtLr
BK94FeTA003iDTNGyU4SdUQQ2G2g/LTxy7KhLlSMc0rnZs2GPiJ6owght1TIlsWh
nw==
-----END CERTIFICATE-----
"""
        lines1 = leaf_pem.split('\n')

        result = []
        for line in lines1:
            result.append(line + "\n")

        return result

    def debug_certs_apexclearing(self):

        leaf_pem = """-----BEGIN CERTIFICATE-----
MIIHRTCCBi2gAwIBAgIINRAybAs0n7gwDQYJKoZIhvcNAQELBQAwgbQxCzAJBgNV
BAYTAlVTMRAwDgYDVQQIEwdBcml6b25hMRMwEQYDVQQHEwpTY290dHNkYWxlMRow
GAYDVQQKExFHb0RhZGR5LmNvbSwgSW5jLjEtMCsGA1UECxMkaHR0cDovL2NlcnRz
LmdvZGFkZHkuY29tL3JlcG9zaXRvcnkvMTMwMQYDVQQDEypHbyBEYWRkeSBTZWN1
cmUgQ2VydGlmaWNhdGUgQXV0aG9yaXR5IC0gRzIwHhcNMTUwNTE1MjMwMzQ3WhcN
MTcwNTE1MjMwMzQ3WjCB0jETMBEGCysGAQQBgjc8AgEDEwJVUzEWMBQGCysGAQQB
gjc8AgECEwVUZXhhczEdMBsGA1UEDxMUUHJpdmF0ZSBPcmdhbml6YXRpb24xEzAR
BgNVBAUTCjgwMDAyMjcxNCAxCzAJBgNVBAYTAlVTMQ4wDAYDVQQIEwVUZXhhczEP
MA0GA1UEBxMGRGFsbGFzMSIwIAYDVQQKExlBcGV4IENsZWFyaW5nIENvcnBvcmF0
aW9uMR0wGwYDVQQDExR3d3cuYXBleGNsZWFyaW5nLmNvbTCCASIwDQYJKoZIhvcN
AQEBBQADggEPADCCAQoCggEBAMndx4jDwkQ1ig9BM2MnPElIWV8Cs3Ks+w/fCN6V
clD7srVOVpqixNAZovd36bK0kcJQH8MLOBSwTOdYWcBdmEkR7+23cUuBlUFATpBQ
xgquYhn1JwotI4pe9zFKwVF6U+wHhCdUNwoHJDBKSHL0dOmLaMk9lQyaB7BnyRoA
H/W7EmaYlQku6WYupyevQkV5JGYvaPe0lDr+B3OfCndfJhfHXhaUEdrF3ike7Tst
jc2Ol3vJ8MhVBZVDVe+hDCNyOOiPbVyHCYOP3QHznhbv57ThKLNDzrHjSftKJoeh
tUQFVY+yVqW4WTwwqZoUUehJBwb8JW9ACykNIHbWS0tsHZMCAwEAAaOCAzkwggM1
MAwGA1UdEwEB/wQCMAAwHQYDVR0lBBYwFAYIKwYBBQUHAwEGCCsGAQUFBwMCMA4G
A1UdDwEB/wQEAwIFoDA1BgNVHR8ELjAsMCqgKKAmhiRodHRwOi8vY3JsLmdvZGFk
ZHkuY29tL2dkaWcyczMtMS5jcmwwUwYDVR0gBEwwSjBIBgtghkgBhv1tAQcXAzA5
MDcGCCsGAQUFBwIBFitodHRwOi8vY2VydGlmaWNhdGVzLmdvZGFkZHkuY29tL3Jl
cG9zaXRvcnkvMHYGCCsGAQUFBwEBBGowaDAkBggrBgEFBQcwAYYYaHR0cDovL29j
c3AuZ29kYWRkeS5jb20vMEAGCCsGAQUFBzAChjRodHRwOi8vY2VydGlmaWNhdGVz
LmdvZGFkZHkuY29tL3JlcG9zaXRvcnkvZ2RpZzIuY3J0MB8GA1UdIwQYMBaAFEDC
vSeOzDSDMKIz1/tss/C0LIDOMDEGA1UdEQQqMCiCFHd3dy5hcGV4Y2xlYXJpbmcu
Y29tghBhcGV4Y2xlYXJpbmcuY29tMB0GA1UdDgQWBBQvphM4qQ4yE04jXXxcXi/S
81e3mjCCAX0GCisGAQQB1nkCBAIEggFtBIIBaQFnAHUAVhQGmi/XwuzT9eG9RLI+
x0Z2ubyZEVzA75SYVdaJ0N0AAAFNWdJNQAAABAMARjBEAiA4c3bXwC3liptBCvgs
YwCdQmlWE2P8tSRCVIRg4A6VhwIgErIlpSi9HrEl5y9oB7Rdm1W1rzoiRtPaB0+a
s4cRYagAdwBo9pj4H2SCvjqM7rkoHUz8cVFdZ5PURNEKZ6y7T0/7xAAAAU1Z0k98
AAAEAwBIMEYCIQCFQnjL3t8q4F/H39AtUS31NQvcXE+7/Ywgd8FarDfuNgIhAOX1
sg8gr4Ol4lyt0iBZGiGS13Ca8zCP3ZQRrofo7LXbAHUApLkJkLQYWBSHuxOizGdw
Cjw1mAT5G9+443fNDsgN3BAAAAFNWdJRdgAABAMARjBEAiAGsbRfzsaL7hvDPD+c
U+9qm2wC/eX5/Rcf24hmdTJafQIgPNZ2ZfbdeVVvhP11bfOS+8OeCDfQmL6e8uiI
bMTDXYUwDQYJKoZIhvcNAQELBQADggEBAA90C14GfTRxFSSBlad6NX3vpfS46If4
mut+0sAM4HcMAy//tToQpeuDGGmh6NhL72VEKJ+u7r7evqGYr32Dxs1s+c1LD6oV
N8mPcnUJYmtGnkDMzqFZLuJCwyT9eyfD2LSnx8sa1Rs0ZIGsPaGUXF37ZLWQpL3B
zPMpBVJ491UOFjOchNhIbiRVKbpnGfFsycI/7/prpBI2+9FxPh6duSm4S8MQoxGn
R/z8o1gPDg8jQPr9OM8f5v0lK/wQlT6fJ1v/ohLxpdI0NQf5YNWbn8wnPV8vwPwR
LHT71kRsjy4bL2foGYlI67emDasZL2vgOwh82v0x/W9UhWJJW2WPk6o=
-----END CERTIFICATE-----
"""
        lines1 = leaf_pem.split('\n')

        result = []
        for line in lines1:
            result.append(line + "\n")

        return result


    def debug_certs_google(self):

        intermediate2_pem = """-----BEGIN CERTIFICATE-----
MIIDfTCCAuagAwIBAgIDErvmMA0GCSqGSIb3DQEBBQUAME4xCzAJBgNVBAYTAlVT
MRAwDgYDVQQKEwdFcXVpZmF4MS0wKwYDVQQLEyRFcXVpZmF4IFNlY3VyZSBDZXJ0
aWZpY2F0ZSBBdXRob3JpdHkwHhcNMDIwNTIxMDQwMDAwWhcNMTgwODIxMDQwMDAw
WjBCMQswCQYDVQQGEwJVUzEWMBQGA1UEChMNR2VvVHJ1c3QgSW5jLjEbMBkGA1UE
AxMSR2VvVHJ1c3QgR2xvYmFsIENBMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB
CgKCAQEA2swYYzD99BcjGlZ+W988bDjkcbd4kdS8odhM+KhDtgPpTSEHCIjaWC9m
OSm9BXiLnTjoBbdqfnGk5sRgprDvgOSJKA+eJdbtg/OtppHHmMlCGDUUna2YRpIu
T8rxh0PBFpVXLVDviS2Aelet8u5fa9IAjbkU+BQVNdnARqN7csiRv8lVK83Qlz6c
JmTM386DGXHKTubU1XupGc1V3sjs0l44U+VcT4wt/lAjNvxm5suOpDkZALeVAjmR
Cw7+OC7RHQWa9k0+bw8HHa8sHo9gOeL6NlMTOdReJivbPagUvTLrGAMoUgRx5asz
PeE4uwc2hGKceeoWMPRfwCvocWvk+QIDAQABo4HwMIHtMB8GA1UdIwQYMBaAFEjm
aPkr0rKV10fYIyAQTzOYkJ/UMB0GA1UdDgQWBBTAephojYn7qwVkDBF9qn1luMrM
TjAPBgNVHRMBAf8EBTADAQH/MA4GA1UdDwEB/wQEAwIBBjA6BgNVHR8EMzAxMC+g
LaArhilodHRwOi8vY3JsLmdlb3RydXN0LmNvbS9jcmxzL3NlY3VyZWNhLmNybDBO
BgNVHSAERzBFMEMGBFUdIAAwOzA5BggrBgEFBQcCARYtaHR0cHM6Ly93d3cuZ2Vv
dHJ1c3QuY29tL3Jlc291cmNlcy9yZXBvc2l0b3J5MA0GCSqGSIb3DQEBBQUAA4GB
AHbhEm5OSxYShjAGsoEIz/AIx8dxfmbuwu3UOx//8PDITtZDOLC5MH0Y0FWDomrL
NhGc6Ehmo21/uBPUR/6LWlxz/K7ZGzIZOKuXNBSqltLroxwUCEm2u+WR74M26x1W
b8ravHNjkOR/ez4iyz0H7V84dJzjA1BOoa+Y7mHyhD8S
-----END CERTIFICATE-----
"""

        intermediate1_pem = """-----BEGIN CERTIFICATE-----
MIID8DCCAtigAwIBAgIDAjqSMA0GCSqGSIb3DQEBCwUAMEIxCzAJBgNVBAYTAlVT
MRYwFAYDVQQKEw1HZW9UcnVzdCBJbmMuMRswGQYDVQQDExJHZW9UcnVzdCBHbG9i
YWwgQ0EwHhcNMTUwNDAxMDAwMDAwWhcNMTcxMjMxMjM1OTU5WjBJMQswCQYDVQQG
EwJVUzETMBEGA1UEChMKR29vZ2xlIEluYzElMCMGA1UEAxMcR29vZ2xlIEludGVy
bmV0IEF1dGhvcml0eSBHMjCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEB
AJwqBHdc2FCROgajguDYUEi8iT/xGXAaiEZ+4I/F8YnOIe5a/mENtzJEiaB0C1NP
VaTOgmKV7utZX8bhBYASxF6UP7xbSDj0U/ck5vuR6RXEz/RTDfRK/J9U3n2+oGtv
h8DQUB8oMANA2ghzUWx//zo8pzcGjr1LEQTrfSTe5vn8MXH7lNVg8y5Kr0LSy+rE
ahqyzFPdFUuLH8gZYR/Nnag+YyuENWllhMgZxUYi+FOVvuOAShDGKuy6lyARxzmZ
EASg8GF6lSWMTlJ14rbtCMoU/M4iarNOz0YDl5cDfsCx3nuvRTPPuj5xt970JSXC
DTWJnZ37DhF5iR43xa+OcmkCAwEAAaOB5zCB5DAfBgNVHSMEGDAWgBTAephojYn7
qwVkDBF9qn1luMrMTjAdBgNVHQ4EFgQUSt0GFhu89mi1dvWBtrtiGrpagS8wDgYD
VR0PAQH/BAQDAgEGMC4GCCsGAQUFBwEBBCIwIDAeBggrBgEFBQcwAYYSaHR0cDov
L2cuc3ltY2QuY29tMBIGA1UdEwEB/wQIMAYBAf8CAQAwNQYDVR0fBC4wLDAqoCig
JoYkaHR0cDovL2cuc3ltY2IuY29tL2NybHMvZ3RnbG9iYWwuY3JsMBcGA1UdIAQQ
MA4wDAYKKwYBBAHWeQIFATANBgkqhkiG9w0BAQsFAAOCAQEACE4Ep4B/EBZDXgKt
10KA9LCO0q6z6xF9kIQYfeeQFftJf6iZBZG7esnWPDcYCZq2x5IgBzUzCeQoY3IN
tOAynIeYxBt2iWfBUFiwE6oTGhsypb7qEZVMSGNJ6ZldIDfM/ippURaVS6neSYLA
EHD0LPPsvCQk0E6spdleHm2SwaesSDWB+eXknGVpzYekQVA/LlelkVESWA6MCaGs
eqQSpSfzmhCXfVUDBvdmWF9fZOGrXW2lOUh1mEwpWjqN0yvKnFUEv/TmFNWArCbt
F4mmk2xcpMy48GaOZON9muIAs0nH5Aqq3VuDx3CQRk6+0NtZlmwu9RY23nHMAcIS
wSHGFg==
-----END CERTIFICATE-----
"""
        leaf_pem = """-----BEGIN CERTIFICATE-----
MIIEgDCCA2igAwIBAgIINyDCnCO0MiMwDQYJKoZIhvcNAQELBQAwSTELMAkGA1UE
BhMCVVMxEzARBgNVBAoTCkdvb2dsZSBJbmMxJTAjBgNVBAMTHEdvb2dsZSBJbnRl
cm5ldCBBdXRob3JpdHkgRzIwHhcNMTcwMzIyMTYyNzEwWhcNMTcwNjE0MTYxNjAw
WjBoMQswCQYDVQQGEwJVUzETMBEGA1UECAwKQ2FsaWZvcm5pYTEWMBQGA1UEBwwN
TW91bnRhaW4gVmlldzETMBEGA1UECgwKR29vZ2xlIEluYzEXMBUGA1UEAwwOd3d3
Lmdvb2dsZS5jb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCVrVNv
L6B81zNgm56bilaXuOe7g8AKbgmYIkV+Ad41nCivyNRWXtRjfuyk2qY/+fbyphVp
m1lEDWJBbZy+AN4MW3FbOqtMsbggEUTcdw82DgjRRMOnqAZI4ng2IebDYMildb0h
CJMw+r3Cu8eCMRrwstBCbmxe+GrVv76kFxIsi3Zk29wqgiFylVGNs2GO6aWtA6fz
Lj52yLHNh+DTO/rWjgFbuAybeUdwE3Q5rG775rZExtFp3SVjaIx9tg+oF+SecUgu
p3Ou2Vv51W4Gy91JILVhV8LI4KdEIyn5HELT3wxo6HSse5AzwsIJBYcRdBJHse4A
8Q7W6Lwz4hgGvC+fAgMBAAGjggFLMIIBRzAdBgNVHSUEFjAUBggrBgEFBQcDAQYI
KwYBBQUHAwIwGQYDVR0RBBIwEIIOd3d3Lmdvb2dsZS5jb20waAYIKwYBBQUHAQEE
XDBaMCsGCCsGAQUFBzAChh9odHRwOi8vcGtpLmdvb2dsZS5jb20vR0lBRzIuY3J0
MCsGCCsGAQUFBzABhh9odHRwOi8vY2xpZW50czEuZ29vZ2xlLmNvbS9vY3NwMB0G
A1UdDgQWBBRcBQJNWi/xVq/0QRhuiMBZiA+pEzAMBgNVHRMBAf8EAjAAMB8GA1Ud
IwQYMBaAFErdBhYbvPZotXb1gba7Yhq6WoEvMCEGA1UdIAQaMBgwDAYKKwYBBAHW
eQIFATAIBgZngQwBAgIwMAYDVR0fBCkwJzAloCOgIYYfaHR0cDovL3BraS5nb29n
bGUuY29tL0dJQUcyLmNybDANBgkqhkiG9w0BAQsFAAOCAQEANbjJt2SUvv2FZZbE
yEAiPXAYS9XkH+EmcwNPrs3I2nUpRrKNxIJvn8K5+g8Zbo1PIPuUra7/T1HGAi28
9exGwTk9Lam/NHBOafBX6JlSaD8y/NTO0KirUyl8S/8Wq+uJLJDy5hDhg+jabaGw
QEu4Xs/dm4sUn1e29OOyL9X6GOLRuU0dFRZIpfRyhj8xejq1UqnYtIz2xBog/oID
JMoKmt0COGM9N/qnJib6QQqhvaJefy6IqWooLxIh/nD7ttZmZ62JKXSSDO3nA9nO
6uDbwJQAspmgF0uj4YTc7mTxojwMVovrNR2ea/9SngQjEOrZRCLQn6iK2ToauegC
33L1Ag==
-----END CERTIFICATE-----
"""

        lines0 = leaf_pem.split('\n')
        lines1 = intermediate1_pem.split('\n')
        lines2 = intermediate2_pem.split('\n')

        result = []
        for line in lines0:
            result.append(line + "\n")
        for line in lines1:
            result.append(line + "\n")
        for line in lines2:
            result.append(line + "\n")

        return result