#!/usr/bin/python
# coding: utf8
import os.path
from enum import Enum
from datetime import datetime
from time import gmtime, strftime


class MediaType(Enum):
    DRIVE = 0
    PICASA = 1
    DATABASE = 2
    ALBUM_LINK = 3
    NONE = 4


# base class for media model classes
class GoogleMedia(object):
    MEDIA_FOLDER = ""
    MEDIA_TYPE = MediaType.NONE
    TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    # todo remove relative path removed and determine it in derived classes
    # note that PicasaMedia and DataBaseMedia already do this
    def __init__(self, relative_folder, root_folder, **k_args):
        self.media_type = self.__class__.MEDIA_TYPE
        self.media_folder = self.__class__.MEDIA_FOLDER
        self._relative_folder = relative_folder
        self._root_folder = root_folder
        self.__duplicate_number = 0

    def save_to_db(self, db):
        now_time = strftime(GoogleMedia.TIME_FORMAT, gmtime())
        if isinstance(self.description, unicode):
            description = self.description
        else:
            description = unicode(self.description, 'utf8')
        data_tuple = (
            self.id, self.orig_name, self.local_folder,
            self.filename, self.duplicate_number, self.date,
            self.checksum, description, self.size,
            self.create_date, now_time, self.media_type
        )
        db.put_file(data_tuple)

    def format_date(self, date):
        return datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    @property
    def local_folder(self):
        return os.path.join(self._root_folder, self.media_folder,
                            self._relative_folder)

    @property
    def local_full_path(self):
        return os.path.join(self.local_folder, self.filename)

    @property
    def relative_path(self):
        return os.path.join(self._relative_folder, self.filename)

    @property
    def relative_folder(self):
        return self._relative_folder

    @property
    def duplicate_number(self):
        return self.__duplicate_number

    @duplicate_number.setter
    def duplicate_number(self, value):
        self.__duplicate_number = value

    @property
    def filename(self):
        if self.duplicate_number > 0:
            base, ext = os.path.splitext(os.path.basename(self.orig_name))
            return "%(base)s (%(duplicate)d)%(ext)s" % {
                'base': base,
                'ext': ext,
                'duplicate': self.duplicate_number
            }
        else:
            return self.orig_name

    # ----- Properties for override below -----
    @property
    def size(self):
        raise NotImplementedError

    @property
    def checksum(self):
        raise NotImplementedError

    @property
    def id(self):
        raise NotImplementedError

    @property
    def description(self):
        raise NotImplementedError

    @property
    def orig_name(self):
        raise NotImplementedError

    @property
    def create_date(self):
        raise NotImplementedError

    @property
    def date(self):
        raise NotImplementedError

    @property
    def mime_type(self):
        raise NotImplementedError
