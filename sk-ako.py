# Python application to scrape for software news
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
logging.basicConfig(filename='watch.log', level=logging.DEBUG, format=logging_format) # Log to file
console_logger = logging.StreamHandler() # Log to console as well
console_logger.setFormatter(logging.Formatter(logging_format))
logging.getLogger().addHandler(console_logger)

################################################################################
# Import helper modules
################################################################################

from helpers import *

################################################################################
# Setup appconfig
################################################################################

appconfig = app_helpers.appconfig

################################################################################
# Import api modules
################################################################################

#from api import *

################################################################################
# Import pages modules
################################################################################

#from pages import *

################################################################################
# Functions
################################################################################



################################################################################
# Main function
################################################################################

if __name__ == '__main__':
    logging.info("[PROGRAM START]")
    logging.critical("%8s test message %s" % ("CRITICAL", str(datetime.utcnow())))
    logging.error("%8s test message %s" % ("ERROR", str(datetime.utcnow())))
    logging.warning("%8s test message %s" % ("WARNING", str(datetime.utcnow())))
    logging.info("%8s test message %s" % ("INFO", str(datetime.utcnow())))
    logging.debug("%8s test message %s" % ("DEBUG", str(datetime.utcnow())))
    
    import sklearn
    from sklearn import datasets, svm

    # Load data
    iris= datasets.load_iris()
    
    # Print shape of data to confirm data is loaded
    print(iris.data.shape)
    print(iris.target.shape)

    print(iris.target)


    clf = svm.LinearSVC()

    # learn from the data
    clf.fit(iris.data, iris.target)

    # predict for unseen data
    a = clf.predict([[ 5.0,  3.6,  1.3,  0.25]])
    print("Test1a: [{0}]".format(a))

    a = clf.predict([[ 6.3,  3.3,  4.7,  1.6]])
    print("Test2a: [{0}]".format(a))

    # Parameters of model can be changed by using the attributes ending with an underscore
    # print(clf.coef_ )
    # print(y[0])

    import pickle
    s = pickle.dumps(clf)
    
    clf2 = pickle.loads(s)

    a = clf2.predict([[ 5.0,  3.6,  1.3,  0.25]])
    print("Test1b: [{0}]".format(a))

    a = clf2.predict([[ 6.3,  3.3,  4.7,  1.6]])
    print("Test2b: [{0}]".format(a))
    
    logging.info("[PROGRAM END]")



# reference
# https://www.journaldev.com/18341/python-scikit-learn-tutorial
