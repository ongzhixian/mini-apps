# 5. The TRANSACTION State

Once the client has successfully identified itself to the POP3 server
and the POP3 server has locked and opened the appropriate maildrop,
the POP3 session is now in the TRANSACTION state.  The client may now
issue any of the following POP3 commands repeatedly.  After each
command, the POP3 server issues a response.  Eventually, the client
issues the QUIT command and the POP3 session enters the UPDATE state.
Here are the POP3 commands valid in the TRANSACTION state:

<div class="page-break"></div> 
<a name="stat-command">STAT</a>
STAT

Arguments: none

Restrictions:  

may only be given in the TRANSACTION state

Discussion:  

The POP3 server issues a positive response with a line
containing information for the maildrop.  This line is
called a "drop listing" for that maildrop.

In order to simplify parsing, all POP3 servers are
required to use a certain format for drop listings.  The
positive response consists of "+OK" followed by a single
space, the number of messages in the maildrop, a single
space, and the size of the maildrop in octets.  This memo
makes no requirement on what follows the maildrop size.
Minimal implementations should just end that line of the
response with a CRLF pair.  More advanced implementations
may include other information.

NOTE: This memo STRONGLY discourages implementations
from supplying additional information in the drop
listing.  Other, optional, facilities are discussed
later on which permit the client to parse the messages
in the maildrop.

Note that messages marked as deleted are not counted in
either total.

Possible Responses:

+OK nn mm

Examples:

C: STAT

S: +OK 2 320

<div class="page-break"></div> 
<a name="list-command">LIST</a>
LIST [msg]

Arguments:

a message-number (optional), which, if present, may NOT
refer to a message marked as deleted

Restrictions:

may only be given in the TRANSACTION state

Discussion:

If an argument was given and the POP3 server issues a
positive response with a line containing information for
that message.  This line is called a "scan listing" for
that message.

If no argument was given and the POP3 server issues a
positive response, then the response given is multi-line.
After the initial +OK, for each message in the maildrop,
the POP3 server responds with a line containing
information for that message.  This line is also called a
"scan listing" for that message.  If there are no
messages in the maildrop, then the POP3 server responds
with no scan listings--it issues a positive response
followed by a line containing a termination octet and a
CRLF pair.

In order to simplify parsing, all POP3 servers are
required to use a certain format for scan listings.  A
scan listing consists of the message-number of the
message, followed by a single space and the exact size of
the message in octets.  Methods for calculating the exact
size of the message are described in the "Message Format"
section below.  This memo makes no requirement on what
follows the message size in the scan listing.  Minimal
implementations should just end that line of the response
with a CRLF pair.  More advanced implementations may
include other information, as parsed from the message.

NOTE: This memo STRONGLY discourages implementations
from supplying additional information in the scan
listing.  Other, optional, facilities are discussed
later on which permit the client to parse the messages
in the maildrop.

Note that messages marked as deleted are not listed.

Possible Responses:
```
+OK scan listing follows
-ERR no such message
```

Examples:
```
C: LIST
S: +OK 2 messages (320 octets)
S: 1 120
S: 2 200
S: .
...
C: LIST 2
S: +OK 2 200
...
C: LIST 3
S: -ERR no such message, only 2 messages in maildrop
```

<div class="page-break"></div> 
<a name="retr-command">RETR</a>
RETR msg

Arguments:
    a message-number (required) which may NOT refer to a
    message marked as deleted

Restrictions:
    may only be given in the TRANSACTION state

Discussion:
    If the POP3 server issues a positive response, then the
    response given is multi-line.  After the initial +OK, the
    POP3 server sends the message corresponding to the given
    message-number, being careful to byte-stuff the termination
    character (as with all multi-line responses).

Possible Responses:
    +OK message follows
    -ERR no such message

Examples:
    C: RETR 1
    S: +OK 120 octets
    S: &lt;the POP3 server sends the entire message here&gt;
    S: .

<div class="page-break"></div> 
<a name="dele-command">DELE</a>
DELE msg

Arguments:
    a message-number (required) which may NOT refer to a
    message marked as deleted

Restrictions:
    may only be given in the TRANSACTION state


Discussion:
    The POP3 server marks the message as deleted.  Any future
    reference to the message-number associated with the message
    in a POP3 command generates an error.  The POP3 server does
    not actually delete the message until the POP3 session
    enters the UPDATE state.

Possible Responses:
    +OK message deleted
    -ERR no such message

Examples:
    C: DELE 1
    S: +OK message 1 deleted
    ...
    C: DELE 2
    S: -ERR message 2 already deleted


<div class="page-break"></div> 
<a name="noop-command">NOOP</a>
NOOP

Arguments: none

Restrictions:
    may only be given in the TRANSACTION state

Discussion:
    The POP3 server does nothing, it merely replies with a
    positive response.

Possible Responses:
    +OK

Examples:
    C: NOOP
    S: +OK

<div class="page-break"></div> 
<a name="rset-command">RSET</a>
RSET

Arguments: none

Restrictions:
    may only be given in the TRANSACTION state

Discussion:
    If any messages have been marked as deleted by the POP3
    server, they are unmarked.  The POP3 server then replies
    with a positive response.

Possible Responses:
    +OK

Examples:
    C: RSET
    S: +OK maildrop has 2 messages (320 octets)

