# 4. The AUTHORIZATION State

Once the TCP connection has been opened by a POP3 client, the POP3
server issues a one line greeting.  This can be any positive
response.  An example might be:

   S:  +OK POP3 server ready

The POP3 session is now in the AUTHORIZATION state.  The client must
now identify and authenticate itself to the POP3 server.  Two
possible mechanisms for doing this are described in this document,
the USER and PASS command combination and the APOP command.  Both
mechanisms are described later in this document.  Additional
authentication mechanisms are described in [RFC1734].  While there is
no single authentication mechanism that is required of all POP3
servers, a POP3 server must of course support at least one
authentication mechanism.

Once the POP3 server has determined through the use of any
authentication command that the client should be given access to the
appropriate maildrop, the POP3 server then acquires an exclusive-
access lock on the maildrop, as necessary to prevent messages from
being modified or removed before the session enters the UPDATE state.
If the lock is successfully acquired, the POP3 server responds with a
positive status indicator.  The POP3 session now enters the
TRANSACTION state, with no messages marked as deleted.  If the
maildrop cannot be opened for some reason (for example, a lock can
not be acquired, the client is denied access to the appropriate
maildrop, or the maildrop cannot be parsed), the POP3 server responds
with a negative status indicator.  (If a lock was acquired but the
POP3 server intends to respond with a negative status indicator, the
POP3 server must release the lock prior to rejecting the command.)
After returning a negative status indicator, the server may close the
connection.  If the server does not close the connection, the client
may either issue a new authentication command and start again, or the
client may issue the QUIT command.

After the POP3 server has opened the maildrop, it assigns a message-
number to each message, and notes the size of each message in octets.
The first message in the maildrop is assigned a message-number of
"1", the second is assigned "2", and so on, so that the nth message
in a maildrop is assigned a message-number of "n".  In POP3 commands
and responses, all message-numbers and message sizes are expressed in
base-10 (i.e., decimal).

Here is the summary for the QUIT command when used in the
AUTHORIZATION state:

<a name="quit-command">QUIT</a>
QUIT

Arguments: none

Restrictions: none

Possible Responses:

   +OK

Examples:

   C: QUIT
   
   S: +OK dewey POP3 server signing off