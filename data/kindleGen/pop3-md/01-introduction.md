# 1. Introduction

On certain types of smaller nodes in the Internet it is often
impractical to maintain a message transport system (MTS).  For
example, a workstation may not have sufficient resources (cycles,
disk space) in order to permit a SMTP server [RFC821] and associated
local mail delivery system to be kept resident and continuously
running.  Similarly, it may be expensive (or impossible) to keep a
personal computer interconnected to an IP-style network for long
amounts of time (the node is lacking the resource known as
"connectivity").

Despite this, it is often very useful to be able to manage mail on
these smaller nodes, and they often support a user agent (UA) to aid
the tasks of mail handling.  To solve this problem, a node which can
support an MTS entity offers a maildrop service to these less endowed
nodes.  The Post Office Protocol - Version 3 (POP3) is intended to
permit a workstation to dynamically access a maildrop on a server
host in a useful fashion.  Usually, this means that the POP3 protocol
is used to allow a workstation to retrieve mail that the server is
holding for it.

POP3 is not intended to provide extensive manipulation operations of
mail on the server; normally, mail is downloaded and then deleted.  A
more advanced (and complex) protocol, IMAP4, is discussed in
[RFC1730].

For the remainder of this memo, the term "client host" refers to a
host making use of the POP3 service, while the term "server host"
refers to a host which offers the POP3 service.
