# 3. Basic Operation

Initially, the server host starts the POP3 service by listening on
TCP port 110.  When a client host wishes to make use of the service,
it establishes a TCP connection with the server host.  When the
connection is established, the POP3 server sends a greeting.  The
client and POP3 server then exchange commands and responses
(respectively) until the connection is closed or aborted.

Commands in the POP3 consist of a case-insensitive keyword, possibly
followed by one or more arguments.  All commands are terminated by a
CRLF pair.  Keywords and arguments consist of printable ASCII
characters.  Keywords and arguments are each separated by a single
SPACE character.  Keywords are three or four characters long. Each
argument may be up to 40 characters long.

Responses in the POP3 consist of a status indicator and a keyword
possibly followed by additional information.  All responses are
terminated by a CRLF pair.  Responses may be up to 512 characters
long, including the terminating CRLF.  There are currently two status
indicators: positive ("+OK") and negative ("-ERR").  Servers MUST
send the "+OK" and "-ERR" in upper case.

Responses to certain commands are multi-line.  In these cases, which
are clearly indicated below, after sending the first line of the
response and a CRLF, any additional lines are sent, each terminated
by a CRLF pair.  When all lines of the response have been sent, a
final line is sent, consisting of a termination octet (decimal code
046, ".") and a CRLF pair.  If any line of the multi-line response
begins with the termination octet, the line is "byte-stuffed" by
pre-pending the termination octet to that line of the response.
Hence a multi-line response is terminated with the five octets
"CRLF.CRLF".  When examining a multi-line response, the client checks
to see if the line begins with the termination octet.  If so and if
octets other than CRLF follow, the first octet of the line (the
termination octet) is stripped away.  If so and if CRLF immediately
follows the termination character, then the response from the POP
server is ended and the line containing ".CRLF" is not considered
part of the multi-line response.

A POP3 session progresses through a number of states during its
lifetime.  Once the TCP connection has been opened and the POP3
server has sent the greeting, the session enters the AUTHORIZATION
state.  In this state, the client must identify itself to the POP3
server.  Once the client has successfully done this, the server
acquires resources associated with the client's maildrop, and the
session enters the TRANSACTION state.  In this state, the client
requests actions on the part of the POP3 server.  When the client has
issued the QUIT command, the session enters the UPDATE state.  In
this state, the POP3 server releases any resources acquired during
the TRANSACTION state and says goodbye.  The TCP connection is then
closed.

A server MUST respond to an unrecognized, unimplemented, or
syntactically invalid command by responding with a negative status
indicator.  A server MUST respond to a command issued when the
session is in an incorrect state by responding with a negative status
indicator.  There is no general method for a client to distinguish
between a server which does not implement an optional command and a
server which is unwilling or unable to process the command.

A POP3 server MAY have an inactivity autologout timer.  Such a timer
MUST be of at least 10 minutes' duration.  The receipt of any command
from the client during that interval should suffice to reset the
autologout timer.  When the timer expires, the session does NOT enter
the UPDATE state--the server should close the TCP connection without
removing any messages or sending any response to the client.