# The web application start file
################################################################################
# Import statements
################################################################################

import json
import logging
from datetime import datetime

################################################################################
# Setup logging configuration
################################################################################

logging_format = '%(asctime)-15s %(levelname)-8s %(message)s'
#logging_format = '%(asctime)-15s %(levelname)-8s %(module)-16s %(funcName)-24s %(message)s'
logging.basicConfig(filename='python-apps.log', level=logging.DEBUG, format=logging_format) # Log to file
console_logger = logging.StreamHandler() # Log to console as well
console_logger.setFormatter(logging.Formatter(logging_format))
logging.getLogger().addHandler(console_logger)

################################################################################
# Import helper modules
################################################################################

from helpers import page_helpers, app_helpers, jinja2_helpers

################################################################################
# Setup appconfig
################################################################################

appconfig = app_helpers.appconfig

################################################################################
# Setup bottle and fetch configuration
################################################################################

app = application = page_helpers.get_app()

################################################################################
# Setup jinja2 environment
################################################################################

jinja2_env = jinja2_helpers.jinja2_env

################################################################################
# Import api modules
################################################################################

from api import *

################################################################################
# Import pages modules
################################################################################

from pages import *

################################################################################
# Main function
################################################################################

if __name__ == '__main__':
    logging.info("[PROGRAM START]")
    logging.info("Running on [{0}]".format(app_helpers.hostname))
    logging.critical("%8s test message %s" % ("CRITICAL", str(datetime.utcnow())))
    logging.error("%8s test message %s" % ("ERROR", str(datetime.utcnow())))
    logging.warning("%8s test message %s" % ("WARNING", str(datetime.utcnow())))
    logging.info("%8s test message %s" % ("INFO", str(datetime.utcnow())))
    logging.debug("%8s test message %s" % ("DEBUG", str(datetime.utcnow())))
    
    # Initialize modules that requires it
    from modules import project_mgmt
    project_mgmt.init()
    
    #url_dump.init()
    page_helpers.run(host="0.0.0.0", port=50001, debug=True, reloader=False)
    logging.info("[PROGRAM END]")

