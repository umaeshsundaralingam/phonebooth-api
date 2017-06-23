import os
import sys

sys.path.append(os.getcwd())

from pbapi.core import app

if __name__ == "__main__":
    app.run(debug=True)

