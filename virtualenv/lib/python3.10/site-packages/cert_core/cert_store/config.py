import os

import configargparse

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def create_config():
    p = configargparse.getArgumentParser(default_config_files=[os.path.join(BASE_DIR, 'conf_test.ini'),
                                                               os.path.join(BASE_DIR, 'conf_local.ini'),
                                                               os.path.join(BASE_DIR, 'conf.ini'),
                                                               '/etc/cert-issuer/conf.ini'])
    p.add('-c', '--my-config', required=False, is_config_file=True, help='config file path')
    p.add_argument('--mongodb_uri', default='mongodb://localhost:27017/test', type=str, env_var='MONGODB_URI',
                   help='Mongo connection string, including db containing certificates')
    p.add_argument('--cert_store_type', type=str, help='type of key value store to use for Cert Store')
    p.add_argument('--cert_store_path', type=str, help='path to file system Cert Store')
    p.add_argument('--v1_aware', action='store_true', help='Whether to support v1 certs')
    args, _ = p.parse_known_args()
    return args


parsed_config = None


def get_config():
    global parsed_config
    if parsed_config:
        return parsed_config
    parsed_config = create_config()
    return parsed_config
