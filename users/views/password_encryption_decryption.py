from base64 import b64decode

from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA


class Password:
    def __init__(self):
        self.private_key = b"""-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: DES-EDE3-CBC,730D453524243B3E

b/50LXgQqZRl7dAO7lv4fskiHwHjtmLfj1Glz9XQPTn7LFDi1uHPM8VaBJSGvUrz
0czCRMrrDMylkGbjzp8W9NBEwWSEk4iea3+ymfJRiwRqcDfz7x0wo+4CPhvOCNQW
lihBN+p9KkqVbLnEMmDJqpuz67jYqhGelE7MLjpR1Jwh2CT7/Tp2NMixOvMSMIsZ
ODohoKKu3g9npPCltrT7tH0xiSY3Id6DfDlEtQlyUZ6Qrw7mG0TurGCU1v2V5GD7
reKQv5Sllu1VzKROJBlnppTilcAoVZLQomYektq1SYaTDwN28qQxfZvfReS0jM4M
Nnzvxl4HWmc3ta02oLxZoUYwoQZ4iHcmsdylKfKeGfwUd9z18e/4e18iK8ACrWFn
jEVUeRCTNzktf1TONrgk7wnluxIXMYD/ofCpedWk4mRyiQOllJqeKsqJK4eh3lix
X/0Wj81iWWFNrCv7dNWI24wLGmWIsWxyboumxv667AzdtwqV0mySKlbO/Cci1Hhu
FlXyA3F7iYF4RiUVCaPknCJuIbBHTGUqsLuf1pU7xoJptsjms7Lh9+sOaH8vjUkQ
vS6Urw2K5K5aU7SO3C01Hgv2nUVsjYunP4GjUQRwy2RYxFeqlNBIYfyHKWynn7d5
V7NqhxT3sCH6Z49/5MNYFZMxGNZQIWUGGN5IsZnF4KgVPDV8FyaV6eIC+leFK46G
5UtfGzOyl8z5sez9nb4wf3vnQmo6zzhLsvBNqXuPqzsQalPdKdQDJrOeM0EFRepk
AOmyfUUKcHp0ASQkgRR/XfHe0YQzPCVypPl7hsqc/y+1TpnNyC1NBkkgia1Bw9py
Vcs44eSFL5mLmMlI+P8taO3NkN13MDc8Lj07gl5OPT8NlmRlLoRyc1aMwMLZiJEi
KKDMIguIlUvigkUQJMu2TYVqGIVuThzGiJum2FS/5lsMMrn4GOSDJihJF92/NtPZ
DXKbFkbbCOprVJ3zZbe2CmtGpcb53oqScpAr9LCR34t5yGfSFhKBpl94ZdBy/hIW
98zgib1zfPbeCOvRU7eVtqHRkYdhKsOMjf5rn1qw2JKGEUoG9KRAR/oiZVWuHUGB
WF+2AQfvRPHKPJIUk7It3e+eIftYRVUShvh0WjYyqFl2D7gHuqS9+Ns0j5f9QAWF
CidQVfqXHIr/2zhoJe5LnSAigVrudOppnZpVhCdS0wvVRJL9uOqZLbbzSTGPbKfo
Swv6dCMj2BQpY1s948aDqc8PQBc4QYMd/+CJtNQ6vjqEXpUYltVTnqP0TzFp9qOK
iLaeElJ/tsth9zhM8e6o6InSKbBZUxa9JVffGs1IbjB/cyfYeilGNVg1IIsSgfis
DihnCUffTkRcJlSlSAxsCF9whxH2X3cwkmjMB/mA4z9BUQEJ9zYlUPEIcTK2kyVK
NmLAAud4sdn3C7hRbOdQven/5vCiiIHZN0Xdej96l3AhO+jw9IpMhXy1f+BKuKiB
7IKa4FQotAb63bAEm7xV96CgvVmZ5s/wGpw6TCb1TeC01HcuofOiUbrFPiqMU6en
uTS2KAea4231Uh4HHGZLUUStub0Ev+uH+m5BJsCHBfvNkuLDd2Z0XdyMTU3VJ6kW
-----END RSA PRIVATE KEY-----
"""
        self.public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApEPCmRRaAclJFVOGArG5
tbfafLUNj+gMqkIolp2T/jxk4N1K2OKrlfKkr8o69ATYEzAWZ5+HNSIjBB6XYq6A
bEr1TP33VTcXN/5aMKm3kXbjFbVxBgaUgvGt7RnI1QwEHLs79M1sctihjWozWoSG
+Z0hGmcdSgQBC46BTPEi6h+Bh5hYeFacIHQvdQpzzvJfLWBJ8WDXMEx7Iad5Nv6C
sYdv6kA7HlWFx29YxVfihzfLGsKUBNDV0jhqRAiIaxOmaybAuErJgQStImSg/Zyv
oKuCDEUDlvJR+OXb9Uqlvj+mEP4gQc+5EvUsK+yzIjADrIOQD5+aHMzhmY/H0W1b
swIDAQAB
-----END PUBLIC KEY-----"""

    def decode_password(self, password):
        private_key = RSA.importKey(self.private_key, "Subex@123")
        private_key = PKCS1_v1_5.new(private_key)
        password = b64decode(password)
        password = private_key.decrypt(password, None).decode()
        return password

    def get_public_key(self):
        return self.public_key
