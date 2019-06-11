# Copyright (c) 2017 Civic Knowledge. This file is licensed under the terms of the
# Revised BSD License, included in this distribution as LICENSE

"""

"""


from os.path import basename, dirname, join

from metapack.exc import MetapackError, ResourceError
from metatab import DEFAULT_METATAB_FILE
from rowgenerators import DownloadError, FileUrl, Url, WebUrl, parse_app_url
from rowgenerators.appurl.util import (
    file_ext,
    parse_url_to_dict,
    unparse_url_dict
)


class SqlalchemyDatabaseUrl(Url):

    match_priority = 80

    def __init__(self, url=None, downloader=None, **kwargs):
        super().__init__(str(url), downloader=downloader, **kwargs)


    @classmethod
    def _match(cls, url, **kwargs):
        return url.proto in ('postgresql','sqlite','oracle','mysql','mssql')


    #
    # Sqlalchemy URL reverse the sense of scheme_extension and scheme; the optional
    # part is *after* the scheme, not before it. So, the dialect is always there, and may be
    # in the scheme or the extension, but if the driver is specified, it is always in the
    # scheme. So, the dialect should == proto
    #
    @property
    def dialect(self):
        return self.proto

    @property
    def driver(self):
        if self.scheme_extension:
            return self.scheme
        else:
            return self.scheme_extension