import os
import sys

sys.path.append(os.getcwd())

from app.factory import create_app
from app import config

if __name__ == "__main__":
    context = (config.settings['SSL_CERT_FILE'], config.settings['SSL_PKEY_FILE'])
    app = create_app(config=config)
    app.run(debug=config.settings['DEBUG'], ssl_context=context)

