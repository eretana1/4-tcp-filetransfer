# TCP- FileTransfer

Directory  `simple-echo`  includes a simple tcp echo server & client

Directory  `lib`  includes the params package required for many of the programs

Directory  `stammer-proxy`  includes stammerProxy, which is useful for demonstrating and testing framing

Directory `framing-os` includes tcp framing through messages. A server is able to send a message to a client as a whole even if it is fragmented during transmission. 

- Utilizes the basic concepts of in-band signaling to frame a message.

Your task: develop and implement a protocol to frame byte-array files in a manner that they will arrive intact even if they are fragmented during transmission. 

In short, send a file across a tcp stream.

-   `stammerProxy.py`  forwards tcp streams. It may delay the transmission of data but ensures all data will be forwarded, eventually. By default, it listens on port 50000 and forwards to localhost:50001. Use the -? option for help.

Some helpful emacs commands:

Windows

-   C-x 2 - split window horizontally
-   C-x 3 - split window vertically
-   C-x 0 - delete window
-   C-x o - (go to) other-window
-   C-x b - display buffer (in this window)

Shell

-   M-x shell - start shell in this window (named  _shell_)
-   M-x rename-buffer - rename this buffer
-   C-c C-c - send C-c
-   C-c C-d - send C-d
