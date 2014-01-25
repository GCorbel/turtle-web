import cherrypy, os, sys, getopt
from mako.template import Template
from mako.lookup import TemplateLookup
from optparse import OptionParser

lookup = TemplateLookup(directories=['public'])
PUBLIC_DIR = os.path.join(os.path.abspath("."), u"public")

class TurtleWeb(object):
    @cherrypy.expose
    def index(self):
        tmpl = lookup.get_template("index.html")
        return tmpl.render()

    @cherrypy.expose
    def submit(self,
            elevator = None,
            throttle = None,
            rudder = None,
            aileron = None):
        if elevator:
            print(self.percent_to_mu(elevator))
        if throttle:
            print(self.percent_to_mu(throttle))
        if rudder:
            print(self.percent_to_mu(rudder))
        if aileron:
            print(self.percent_to_mu(aileron))
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return b"ok"
    index.exposed = True

    def percent_to_mu(self, percent):
        return 1090 + int(percent) * 810 / 100

config = {'/public': {
    'tools.staticdir.on': True,
    'tools.staticdir.dir': PUBLIC_DIR,
    } }

def main(argv):
    parser = OptionParser()
    parser.add_option("-s",
            "--socket_host",
            dest="socket_host",
            help="Address of the server")
    (options, args) = parser.parse_args()

    cherrypy.tree.mount(TurtleWeb(), '/', config=config)
    cherrypy.config.update({
        'server.socket_host': options.socket_host,
        'server.socket_port': 8080, })
    cherrypy.engine.start()

if __name__ == "__main__":
    main(sys.argv[1:])
