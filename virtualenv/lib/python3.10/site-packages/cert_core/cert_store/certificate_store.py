"""Retrieves certificates from mongodb."""
import logging

from cert_core.cert_store import helpers
from cert_core.cert_model import model
from cert_core import URN_UUID_PREFIX


def certificate_uid_to_filename(uid):
    return uid + '.json'


class CertificateStore:
    def __init__(self, kv_store=None):
        """Create a CertificateStore
        :param kv_store: key value store; subclass of KeyValueStore
        """
        self.kv_store = kv_store

    def get_certificate(self, certificate_uid):
        """
        Returns a certificate. Propagates KeyError if key isn't found
        :param certificate_uid:
        :return:
        """
        certificate_json = self.get_certificate_json(certificate_uid)
        return model.to_certificate_model(certificate_json)

    def get_certificate_json(self, certificate_uid):
        """
        Returns certificate as json. Propagates KeyError if key isn't found
        :param certificate_uid:
        :return:
        """

        if certificate_uid.startswith(URN_UUID_PREFIX):
            uid = certificate_uid[len(URN_UUID_PREFIX):]
        elif certificate_uid.startswith('http'):
            last_slash = certificate_uid.rindex('/')
            uid = certificate_uid[last_slash + 1:]
        else:
            uid = certificate_uid
        logging.debug('Retrieving certificate for uid=%s', uid)
        certificate_bytes = self._get_certificate_raw(uid)
        logging.debug('Found certificate for uid=%s', uid)
        certificate_json = helpers.certificate_bytes_to_json(certificate_bytes)
        return certificate_json

    def _get_certificate_raw(self, certificate_uid):
        """
        Returns certificate as raw bytes. Per kvstore contract, raises an KeyError if key isn't found.
        :param certificate_uid:
        :return:
        """
        cert_file_bytes = self.kv_store.get(certificate_uid_to_filename(certificate_uid))
        return cert_file_bytes


class V1AwareCertificateStore(CertificateStore):
    """Retrieves certificates from mongodb."""

    def __init__(self,
                 kv_store=None,
                 db=None):
        """Create a CertificateStore
        :param kv_store: key value store; subclass of KeyValueStore
        :param db: certificates mongodb table (stores txid for verifying v1 certificates)
        """
        super(V1AwareCertificateStore, self).__init__(kv_store)
        self.db = db

    def get_certificate(self, certificate_uid):
        """
        Returns certificate as byte array. We need this for v1 certs, which compute a binary hash. Raises
        KeyError if not found
        :param certificate_uid:
        :return:
        """
        logging.debug('Retrieving certificate for uid=%s', certificate_uid)

        is_v1_uid = model.is_v1_uid(certificate_uid)
        if not is_v1_uid:
            return super(V1AwareCertificateStore, self).get_certificate(certificate_uid)

        # else it's V1.1 (if not valid, it will throw)
        certificate = self._find_certificate_metadata(uid=certificate_uid)
        if certificate:
            certificate_bytes = self._get_certificate_raw(certificate_uid)
            certificate_json = helpers.certificate_bytes_to_json(certificate_bytes)
            return model.to_certificate_model(certificate_json, certificate['txid'], certificate_bytes)

        message = 'Certificate metadata not found for certificate uid=%s' % certificate_uid
        logging.error(message)
        raise KeyError(message)

    def _find_certificate_metadata(self, uid=None):
        """
        Find certificate by certificate uid
        :param uid: certificate uid
        :return: certificate from certificates collection
        """
        certificate = self.db.certificates.find_one({'uid': uid})
        return certificate
