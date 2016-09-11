from OpenSSL.crypto import FILETYPE_PEM, load_certificate
from django.conf import settings  # type: ignore
from rest_framework.exceptions import APIException


class CertificateConfiguration:
    def __init__(self) -> None:
        self.validate_certs = settings.VALIDATE_CERTIFICATES


class InvalidSignatureException(APIException):
    pass


class InvalidCertificateException(APIException):
    pass


class CertificateValidator:
    """
    See https://pyopenssl.readthedocs.io/en/stable/api/crypto.html#signing
    -and-verifying-signatures
    """

    def __init__(self, config: CertificateConfiguration) -> None:
        self.config = config

    def validate_signature(self, certificate: str, signature: str,
                           data: str) -> None:
        """
        Tests if a value is a valid certificate using SHA512
        Logs an error if self.config.validate_certs is False
        :param certificate: the certificate to use
        :param signature: the signature string to test
        :param data: the SHA512 value (e.g. archive SHA512 checksum)
        :raises: InvalidSignatureException if the signature is invalid
        :return: None
        """
        pass

    def validate_certificate(self, certificate: str, chain: str,
                             crl: str) -> None:
        """
        Tests if a certificate has been signed by the chain, is not revoked
        and has not yet been expired. Logs an error if
        self.config.validate_certs is False
        :param certificate: the certificate to test
        :param chain: the certificate chain file content
        :param crl: the certificate revocation list file content
        :raises: InvalidCertificateException if the certificate is invalid
        :return: None
        """
        pass

    def get_cn(self, certificate: str) -> str:
        """
        Extracts the CN from a certificate and removes the leading
        slash, e.g. /news should return news
        :param certificate: certificate
        :return: the certificate's subject without the leading slash
        """
        cert = load_certificate(FILETYPE_PEM, certificate.encode())
        return cert.get_subject().CN[1:]