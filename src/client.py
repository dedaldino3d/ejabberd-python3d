import xmlrpc





class EjabberdAPI(object):
    """Pytho client for ejabberd XML-RPC Adminitration API."""

    def __init__(self, host, username, password, 
                protocol='http', server='127.0.0.1', port=4560, 
                admin=True, verbose=False):
        """XML-RPC server proxy."""

        self.params = {'user': username, 
                        'password': password, 
                        'server': host, 'admin':admin}
        self.errors = {
            'connect': 'ERROR: cannot connect to the server',
            'access': 'ERROR: access denied, account unprevilged',
            'bad_arg': 'ERROR: call failed, bad input argument',
            'missing_arg': 'ERROR: call failed, missing input argument'
        }
        self._proxy = None
        self.xmlrpc_server = xmlrpc.ServerProxy(uri, verbose=verbose)
    
    @property
    def service_url(self):
        """
        Return the FQDN to the ejabberd server's XML-RPC endpoint
        """
        return "{}://{}:{}".format(protocol, host, port)

    @property
    def proxy(self)    :
        """
        Retun the proxy object that is used to perform the calls to the
        XML-RPC endpoint
        :return xmlrpc.ServerProxy
        """
        if self._proxy is None:
            self._proxy = xmlrpc.client.ServerProxy(self.service_url, verbose=self.verbose)
        return self._proxy            

    @property
    def auth(self):
        """
        Return a dictionay containing the basic authorization info
        """
        return {
            'user': self.username,
            'server': self.host,
            'password': self.password
        }
    
    def call_api(self, command, payload=None):
        """
            Run the ejabberd command.
        """
        fn = getattr(self.xmlrpc_server, command)
        try:
            if payload:
                return fn(self.params, payload)
            return fn(self.params)
        except BadStatusLine as e:
            raise Exception("{}\n{}".format(self.errors['connect'],
            e.message))
        except xmlrpc.Fault as e:
            if 'account_unprivileged' in e.message:
                raise Exception('{}\n{}'.format(self.errors['access'], e.message))
            if 'bad_argument' in e.message:
                raise Exception("{}\n{}".format(self.errors['bad_arg'], e.message))
            if 'Required attribute' in e.message and 'not found' in e.message:
                raise Exception("{}\n{}".format(self.errors[ 'missing_arg'], e.message))
            raise Exception(e)
    
