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

def chk(val, n0, offset):
    """Finds a list of palindromes from substring given a position within the string.
    Offset

    Args:
        val (string):
            The string that we are examining for palindromes.
        n0 (integer):
            Position of the pivot character that we using to find palindromes.
        offset (offset):
            The amount of expansion offset that we want to use to 
            examine further expansion of found palindromes.

    Returns:
        List, a list of palindromes found.
    """
    # List of palindromes found
    result = []
    
    # Stop if we cannot expand any further to the left.
    if (n0-offset) < 0:
        return result
    
    # Stop if we cannot expand any further to the right.
    if (n0+1+offset) >= len(val):
        return result

    # c0 is the pivot character.
    # c1 is the immediate character following pivot character.
    # c2 is the immediate character following c1 (if length of 'val' permits).
    c0 = val[n0-offset]
    c1 = val[n0+1+offset]

    if (n0+2+offset) < len(val):
        c2 = val[n0+2+offset]
    else:
        c2 = None

    if c0 == c2:
        # If c0 matches c2; means we have a palindrome of "middle-pivot character" variant
        #print "Found2 text: [{0}, {1}] {2}".format(n0-offset, n0+1+offset+2, val[n0-offset:n0+1+offset+2])
        # Save this match to list
        result.append(
            (val[n0-offset:n0+1+offset+2], n0-offset, (n0+1+offset+2) - (n0-offset))
        )
        # Attempts to find palindromes based on expansion of found palindrome.
        found_list = chk(val, n0, offset+1)
        # Save any found expansion of palindromes to result list
        for e in found_list:
            result.append(e)
    elif c0 == c1:
        # If c0 matches c1; means we have a palindrome of "next-matching" variant
        #print "Found1 text: [{0}, {1}] {2}".format(n0-offset, n0+1+offset+1, val[n0-offset:n0+1+offset+1])
        # Save this match to list
        result.append(
            (val[n0-offset:n0+1+offset+1], n0-offset, (n0+1+offset+1) - (n0-offset))
        )
        # Attempts to find palindromes based on expansion of found palindrome.
        found_list = chk(val, n0, offset+1)
        # Save any found expansion of palindromes to result list
        for e in found_list:
            result.append(e)
    # Return result; list of palindrome found.
    return result
        

def find_palindrome(val, top=3):
    """Finds a list of unique palindromes from a given string

    Args:
        val (string):
            The string that we want to search to find palindromes in.
        top (integer, default=3):
            The number of lengthiest palindromes to return; defaults to 3
            Specify None to get all palindromes found

    Returns:
        List, a list of palindromes found.
    """
    result = [] # list of palindromes found
    
    # Examine each substring to find possibilities of palindrome in the substring
    i = 0
    val_len = len(val)
    for i in xrange(val_len):
        found_list = chk(val, i, 0)
        for e in found_list:
            # filter for unique palindromes
            if e[0] not in [x[0] for x in result]:
                result.append(e)
    # Sort by length and grab the top results
    return sorted(result, key=lambda x: "{0}_{1}".format(x[2], x[1]) , reverse=True)[:top]
    

################################################################################
# Setup commonly used routes
################################################################################

@route('/palindrome', method=['POST','GET'])
def display_home_page(errorMessages=None):
    context = get_default_context(request)

    if request.method == 'POST':
        if 'test_text_input' in request.forms.keys():
            # Process text into array of urls
            #url_list = make_url_list(request.forms['save_text_textarea'].split("\n"))
            test_text = request.forms['test_text_input']
            logging.debug("Text to be tested is {0}".format(test_text))
            palindromes = find_palindrome(test_text, None)

            if len(palindromes) > 0:
                context["notification"] = "%d palindromes(s) found in [%s]." % (len(palindromes), test_text)
                context["palindromes"] = palindromes

    return jinja2_env.get_template('html/palindrome/home-page.html').render(context)

################################################################################
# Notes
################################################################################
# Buggy? Try testing  [mmddmm]