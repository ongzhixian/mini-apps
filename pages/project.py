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


@route('/project/')
@route('/project')
def display_project_home_page(errorMessages=None):
    context = get_default_context(request)
    #response.set_cookie('username', 'the username')
    return jinja2_env.get_template('html/project/home-page.html').render(context)


@route('/project/list')
def display_project_trading_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/project/list-page.html').render(context)


@route('/project/kanban')
def display_project_trading_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/project/kanban-page.html').render(context)

@route('/project/task')
def display_project_lottery_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/project/task-page.html').render(context)

@route('/project/gantt')
def display_project_gantt_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/project/gantt-page.html').render(context)




@route('/project/add')
def display_project_add_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/project/add-page.html').render(context)

@route('/project/add', method="POST")
def post_project_add_page(errorMessages=None):
    context = get_default_context(request)
    # Get values from form
    frm = request.forms
    project_name = frm['project_name']
    project_category = frm['project_category']
    project_status = frm['project_status']
    # Validate values from forms; Skip for now
    # Write record to database.
    return jinja2_env.get_template('html/project/add-page.html').render(context)


@route('/project/update')
def display_project_update_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/project/update-page.html').render(context)

@route('/project/delete')
def display_project_delete_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/project/delete-page.html').render(context)
