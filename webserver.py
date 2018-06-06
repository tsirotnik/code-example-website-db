"""
web.py webserver

serves static html content and assets

serves json content through rest interface for population
of the sitter information list
"""

import os
import web
from example.tables.sitter_list import SitterList

class WebServer(object):
    """
    web.py webserver
    """

    def __init__(self):
        """
        webserver initialization

        args: --
        """

        self._urls = (
            # index page
            '/', 'index',
            # all static content assets
            '/(js|css|images|libs)/(.*)', 'static',
            # any html page in the root directory
            '/(.*\.html)', 'static_html',
            # request for sitter information
            # /items/<beginning item index>/<over score filter threshold>
            '/items/(\d+)/([\d\.]+)', 'items'
        )
        self.app = web.application(self._urls, globals())
        self.app.internalerror = web.debugerror
        self.app.run()

    def start(self):
        """
        start the webserver

        args: --
        returns: None
        """
        self.app.run()

    def stop(self):
        """
        stop the webserver

        args: --
        returns: None
        """
        self.app.stop()


class items:
    """
    process web requests with this signature:
        /items/(\d+)/([\d\.]+)
    """
    def GET(self, begin_index, filterby):
        """
        handles GET requests for sitter information

        args:
            begin_index : offset from sorted list used for pagination
            filterby : overall_rank to filter sorted list by

        returns:
            json data to be served by webserver
        """
        sitterlist = SitterList()
        data = sitterlist.data(begin_index, filterby)
        web.header('Content-Type', 'application/json')
        return data


class static:
    """
    process web requests with this signature:
        /(js|css|images|libs)/(.*)
    """
    def GET(self, subdir, file):
        """
        handles GET requests for static content assets
        """
        try:
            # change content type for css
            if file.endswith(".css"):
                web.header('Content-Type', 'text/css')
            path = os.path.join("static", subdir, file)
            fh = open(path, 'r')
            return fh.read()
        except Exception as e:
            # universally return 404 if error
            return web.notfound()  # 404


class static_html:
    """
    process web requests with this signature:
        /(.*\.html)
    """
    def GET(self, file):
        """
        handles GET requests for .html files in root path
        """
        try:
            path = os.path.join("static", file)
            print path
            fh = open(path, 'r')
            return fh.read()
        except:
            return web.notfound()  # 404


class index:
    """
    process web requests with this signature:
        /
    """
    def GET(self):
        """
        handles GET Requests for default html page
        """
        try:
            path = "static/index.html"
            fh = open(path, 'r')
            return fh.read()
        except:
            return web.notfound()


if __name__ == "__main__":
    WebServer().start()
