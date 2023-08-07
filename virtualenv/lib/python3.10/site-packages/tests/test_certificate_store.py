import os
import unittest

from cert_core.cert_store import FilesystemStore, CertificateStore

PATH = os.path.join(os.path.abspath(__file__), os.pardir)
TEST_DATA = os.path.join(PATH, 'data', '1.2')


class TestCertificateModel(unittest.TestCase):
    def test_basic(self):
        kv_store = FilesystemStore(TEST_DATA)
        cert_store = CertificateStore(kv_store)
        cert = cert_store.get_certificate('609c2989-275f-4f4c-ab02-b245cfb09017')
        self.assertIsNotNone(cert)
        self.assertEqual('1AAGG6jirbu9XwikFpkHokbbiYpjVtFe1G', cert.recipient_public_key)
        self.assertEqual('8623beadbc7877a9e20fb7f83eda6c1a1fc350171f0714ff6c6c4054018eb54d', cert.txid)

    def test_uuid_prefix(self):
        kv_store = FilesystemStore(TEST_DATA)
        cert_store = CertificateStore(kv_store)
        cert = cert_store.get_certificate('urn:uuid:609c2989-275f-4f4c-ab02-b245cfb09017')
        self.assertIsNotNone(cert)
        self.assertEqual('1AAGG6jirbu9XwikFpkHokbbiYpjVtFe1G', cert.recipient_public_key)
        self.assertEqual('8623beadbc7877a9e20fb7f83eda6c1a1fc350171f0714ff6c6c4054018eb54d', cert.txid)

    def test_http_prefix(self):
        kv_store = FilesystemStore(TEST_DATA)
        cert_store = CertificateStore(kv_store)
        cert = cert_store.get_certificate('https://www.domain.edu/certificates/609c2989-275f-4f4c-ab02-b245cfb09017')
        self.assertIsNotNone(cert)
        self.assertEqual('1AAGG6jirbu9XwikFpkHokbbiYpjVtFe1G', cert.recipient_public_key)
        self.assertEqual('8623beadbc7877a9e20fb7f83eda6c1a1fc350171f0714ff6c6c4054018eb54d', cert.txid)


if __name__ == '__main__':
    unittest.main()
