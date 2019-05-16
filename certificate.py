import socket
import os
from OpenSSL import crypto


def create_self_signed_cert(name=None):
    CERT_FILE = os.path.join("certificates", name + "_cert.pem" if name else "cert.pem")
    KEY_FILE = os.path.join("certificates", name + "_key.pem" if name else "key.pem")

    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 1024)

    cert = crypto.X509()
    cert.get_subject().C = "RU"
    cert.get_subject().ST = "SPB"
    cert.get_subject().L = "SPB"
    cert.get_subject().O = "Lambda Corp."
    cert.get_subject().OU = "Lambda Corp."
    cert.get_subject().CN = "lambda.com"
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)
    cert.sign(key, "sha256")

    with open(CERT_FILE, "wt") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode())
    with open(KEY_FILE, "wt") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key).decode())
    return KEY_FILE, CERT_FILE


if __name__ == "__main__":
    create_self_signed_cert()
