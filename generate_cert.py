# generate_cert.py
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import datetime

def generate_self_signed_cert():
    print("Generating private key...")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    print("Generating certificate...")
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"RW"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Kigali"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Kigali"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Server"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName(u"localhost"),
            x509.DNSName(u"127.0.0.1"),
        ]),
        critical=False,
    ).sign(private_key, hashes.SHA256())
    
    print("Writing server.key...")
    with open("server.key", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    print("Writing server.crt...")
    with open("server.crt", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    print("\n✅ SSL certificate files created successfully!")
    print("   - server.key (private key)")
    print("   - server.crt (certificate)")
    print("\nYou can now run: python server.py")

if __name__ == "__main__":
    try:
        generate_self_signed_cert()
    except ImportError:
        print("❌ Error: 'cryptography' module not installed")
        print("\nPlease install it first:")
        print("pip install cryptography")
        