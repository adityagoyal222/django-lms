import logging

from simplekv import KeyValueStore


class GridfsKeyValueStore(KeyValueStore):
    def __init__(self, gfs_connection):
        self.gfs = gfs_connection

    def _delete(self, key):
        pass

    def iter_keys(self):
        pass

    def __contains__(self, key):
        the_file = self.gfs.find_one({'filename': key})
        return the_file is not None

    def _open(self, key):
        the_file = self.gfs.find_one({'filename': key})
        if the_file:
            logging.debug('Found content for key=%s', key)
            return the_file

        message = 'Did not find content for key={}'.format(key)
        logging.error(message)
        raise KeyError(message)

    def _put_file(self, key, file):
        self.gfs.put(file, filename=key, encoding='utf-8')
