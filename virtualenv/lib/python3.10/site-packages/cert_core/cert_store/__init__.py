import logging.config
import os

import gridfs
from cert_core.cert_store.gridfs_key_value_store import GridfsKeyValueStore
from pymongo import MongoClient
from simplekv.fs import FilesystemStore

from cert_core.cert_store.certificate_store import CertificateStore
from cert_core.cert_store.certificate_store import V1AwareCertificateStore, CertificateStore

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

cert_store = None
log = None


def configure_app(configuration):
    logging.config.fileConfig(os.path.join(BASE_DIR, 'logging.conf'))
    global log
    log = logging.getLogger(__name__)

    mongo_client = MongoClient(host=configuration.mongodb_uri)
    conn = mongo_client[
        configuration.mongodb_uri[configuration.mongodb_uri.rfind('/') + 1:len(configuration.mongodb_uri)]]
    global mongo_connection
    mongo_connection = conn

    if configuration.cert_store_type == 'simplekv_fs':
        kv_store = FilesystemStore(configuration.cert_store_path)
    elif configuration.cert_store_type == 'simplekv_gridfs':
        gfs = gridfs.GridFS(conn)
        kv_store = GridfsKeyValueStore(gfs)

    global cert_store
    if configuration.v1_aware:
        cert_store = V1AwareCertificateStore(kv_store, mongo_connection)
    else:
        cert_store = CertificateStore(kv_store)
