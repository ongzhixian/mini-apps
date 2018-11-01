# Demo market
################################################################################
# Import statements
################################################################################

import json
import logging
import random
import threading
import time
import uuid
from datetime import datetime


################################################################################
# Setup logging configuration
################################################################################

logging_format = '%(asctime)-15s %(levelname)-8s %(message)s'
#logging_format = '%(asctime)-15s %(levelname)-8s %(module)-16s %(funcName)-24s %(message)s'
logging.basicConfig(filename='demo-market.log', level=logging.DEBUG, format=logging_format) # Log to file
console_logger = logging.StreamHandler() # Log to console as well
console_logger.setFormatter(logging.Formatter(logging_format))
logging.getLogger().addHandler(console_logger)

################################################################################
# Constants
################################################################################

PRODUCTS=[ 
    { "name" : "apple", "tickSize" : 0.01 }, 
    { "name" : "banana", "tickSize" : 0.01 }
]
TRADER_COUNT = 1

order_books = {}
order_books_lock = threading.Lock()
startTradingEvent = threading.Event()


################################################################################
# Classes
################################################################################


class ThreadSafeCounter(object):
    def __init__(self, start_value = 0):
        self.lock = threading.Lock()
        self.counter = start_value

    def increment(self, fn = None):
        with self.lock:
            self.counter = self.counter + 1
            if fn == None:
                return
            logging.info("Increment; Counter is now {0}".format(self.counter))
            fn(self)

    def get_counter_value(self):
        return self.counter;

traders_count = ThreadSafeCounter()

class Portfolio:
    def __init__(self):
        pass
    

class TraderProfile:
    def __init__(self, trader_id, capital):
        self.trader_id = trader_id
        self.capital = capital
        self.decision_time = random.randint(1, 5)
        self.portfolio = Portfolio()
        instrument = "apple" if random.randint(1, 10) % 2 == 0 else "banana"
    
    def generate_portfolio(self):
        pass

    def DoWork(self):
        while (True):
            side = "bid" if random.randint(1, 10) % 2 == 0 else "ask"
            instrument = "apple" if random.randint(1, 10) % 2 == 0 else "banana"
            logging.info("trader_id {0} will {1} for {2}".format(self.trader_id, side, instrument))
            add_order(instrument, 1, side, 1)
            time.sleep(self.decision_time)
        


################################################################################
# Functions
################################################################################

########################################
# Order book functions
########################################

def init_order_books():
    global order_books
    with order_books_lock:
        for instrument in PRODUCTS:
            instrument_name = instrument["name"]
            logging.info("Initializing order book for {0}".format(instrument_name))
            if instrument_name in order_books:
                continue
            order_books[instrument_name] = {}
    # order_books_lock.acquire()
    # try:
    #     for instrument in PRODUCTS:
    #         instrument_name = instrument["name"]
    #         logging.info("Initializing order book for {0}".format(instrument_name))
    #         if instrument_name in order_books:
    #             continue
    #         order_books[instrument_name] = {}
    #         # order_books["name"] = {
    #         #     "price" : 1.01,
    #         #     "bid" : [
    #         #         {"quantity" : 1, "id": "traderA"}
    #         #     ],
    #         #     "ask" : [
    #         #         {"quantity" : 2, "id": "traderB"}
    #         #     ]
    #         # }
    # finally:
    #     order_books_lock.release()
    # end - init_order_books()

def dump_order_book(instrument_name):
    global order_books
    if instrument_name not in order_books.keys():
        return None
    order_book = order_books[instrument_name]
    for px in order_book:
        #logging.info("PX {0}".format(px))
        logging.info("{0} {1} bid {2}".format(instrument_name, px, order_book[px]["bid"]))
        logging.info("{0} {1} ask {2}".format(instrument_name, px, order_book[px]["ask"]))

def add_order(instrument_name, price, side, quantity):
    # order_books["name"] = {
    #     1.01 : {
    #         "bid" : [
    #             {"quantity" : 1, "id": "traderA"}
    #         ],
    #         "ask" : [
    #             {"quantity" : 2, "id": "traderB"}
    #         ]
    #     }
    # }
    global order_books, order_books_lock
    if instrument_name not in order_books.keys():
        return None
    with order_books_lock:
        order_book = order_books[instrument_name]
        if price not in order_book.keys():
            order_book = {
                price : {
                    "bid" : [],
                    "ask" : []
                }
            }
            order_books[instrument_name] = order_book
        opposite_side = "bid" if side == "ask" else "ask"
        proc_qty = quantity

        while proc_qty > 0:
            #logging.debug("proc_qty: {0}".format(proc_qty))
            if len(order_book[price][opposite_side]) == 0:
                order_id = uuid.uuid4().hex
                order_book[price][side].append({"order_qty" : quantity, "fill_qty" : quantity - proc_qty, "id": order_id})
                logging.debug("New order: [{0} {1} {2} @ {3}]".format(side, quantity, instrument_name, price))
                proc_qty = proc_qty - proc_qty
                # Send execution report for NEW ORDER
                dump_order_book(instrument_name)
                return order_id
            else:
                client_order = order_book[price][opposite_side][0]
                leaves_qty = client_order["order_qty"] - client_order["fill_qty"]
                #logging.debug("leaves_qty is {0}".format(leaves_qty))
                # FILL vs PARTIAL FILL
                if proc_qty >= leaves_qty:
                    # order_qty >= leaves_qty; may have remainder
                    # New order qty CAN fill order; and we may have remainder
                    client_order["fill_qty"] = client_order["fill_qty"] + leaves_qty
                    proc_qty = proc_qty - leaves_qty
                    # "Pop" order
                    order_book[price][opposite_side] = order_book[price][opposite_side][1:]
                    # Send execution report for FILL
                else:
                    # order_qty < leaves_qty; is a Partial fill
                    # New order qty cannot fill order
                    client_order["fill_qty"] = client_order["fill_qty"] + proc_qty
                    proc_qty = proc_qty - quantity
                    # Send execution report for PARTIAL FILL
        



########################################
# Trader (thread) functions
########################################

def get_daemon_thread(thread_target, thread_name, thread_args):
    try:
        job_thread = threading.Thread(
            group=None
            , target=thread_target
            , name=thread_name
            , args=thread_args
            , kwargs={})
        job_thread.daemon = True
        return job_thread
    except Exception as ex:
        logging.error(ex)
    finally:
        logging.info("Generating [{0}] daemon thread.".format(thread_name))

def startTrading(tsc):
    logging.info("Check 1")
    if tsc.counter >= 2:
        startTradingEvent.set()


def run_trader(trader_id):
    # defining characteristics of trader
    capital = random.randint(1, 10) * 10000
    logging.info("trader_id {0} has ${1}".format(trader_id, capital))
    trader_profile = TraderProfile(trader_id, capital)
    #traders_count.increment(startTrading)
    traders_count.increment(lambda tsc : startTradingEvent.set() if tsc.counter >= TRADER_COUNT  else logging.debug("Waiting for everyone..."))
    startTradingEvent.wait()
    trader_profile.DoWork()
    del trader_profile

################################################################################
# Main function
################################################################################

trader_thread_list = []

if __name__ == '__main__':
    logging.info("[PROGRAM START]")
    # logging.critical("%8s test message %s" % ("CRITICAL", str(datetime.utcnow())))
    # logging.error("%8s test message %s" % ("ERROR", str(datetime.utcnow())))
    # logging.warning("%8s test message %s" % ("WARNING", str(datetime.utcnow())))
    # logging.info("%8s test message %s" % ("INFO", str(datetime.utcnow())))
    # logging.debug("%8s test message %s" % ("DEBUG", str(datetime.utcnow())))
    # Initial modules that requires it
    init_order_books()

    for num in xrange(TRADER_COUNT):
        trader_id = "trader{0:0>2d}".format(num)
        new_trader = get_daemon_thread(
            run_trader, 
            trader_id, 
            (trader_id,))
        trader_thread_list.append(new_trader)
        new_trader.start()

    # while (True):
    #     time.sleep(5)
    for trader_thread in trader_thread_list:
        trader_thread.join()

    # order_id = add_order("apple", 1.01, "bid", 10)
    # order_id = add_order("apple", 1.01, "bid", 12)

    # logging.debug("==========")

    # order_id = add_order("apple", 1.01, "ask", 5)
    # dump_order_book("apple")
    # order_id = add_order("apple", 1.01, "ask", 15)
    # dump_order_book("apple")
    # order_id = add_order("apple", 1.01, "ask", 10)
    # dump_order_book("apple")

    #logging.debug("[CURRENT] {0}".format(order_books))
    
    #logging.info("order_id is {0}".format(order_id))
    # Run a couple of threads to simulate traders trading
    logging.info("[PROGRAM END]")

