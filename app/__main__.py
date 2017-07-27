import os
import sys

sys.path.append(os.getcwd())

from app.factory import create_app
from app import config

if __name__ == "__main__":
    app = create_app(config=config)
    app.run(debug=config.settings['DEBUG'])
