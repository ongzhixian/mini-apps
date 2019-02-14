################################################################################
# Modules and functions import statements
################################################################################

import pdb
from helpers.app_helpers import *
from helpers.page_helpers import *
from helpers.jinja2_helpers import *

################################################################################
# Setup helper functions
################################################################################

# N/A

################################################################################
# Setup commonly used routes
################################################################################


@route('/game/')
@route('/game')
def display_game_home_page(errorMessages=None):
    context = get_default_context(request)
    #response.set_cookie('username', 'the username')
    return jinja2_env.get_template('html/game/home-page.html').render(context)

@route('/game/trading')
def display_game_trading_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/game/trading-page.html').render(context)

@route('/game/lottery')
def display_game_lottery_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/game/lottery-page.html').render(context)
