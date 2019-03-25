# 2. A Short Digression

This memo does not specify how a client host enters mail into the
transport system, although a method consistent with the philosophy of
this memo is presented here:

When the user agent on a client host wishes to enter a message
into the transport system, it establishes an SMTP connection to
its relay host and sends all mail to it.  This relay host could
be, but need not be, the POP3 server host for the client host.  Of
course, the relay host must accept mail for delivery to arbitrary
recipient addresses, that functionality is not required of all
SMTP servers.