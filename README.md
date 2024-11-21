script takes textfile as first positional argument.
File contains bsky-handles, one per line, which will be added to the list defined
in TARGET_LIST.


This is just a quick-and-dirty solution to be able to add multiple
profiles at once to lists.

This is nowhere near production ready.

Expect errors if you use it at this stage.

Also, saving the bsky session is not implemented yet.
If you use this you may expect rate-limiting (30/5m, 300/d)

PULL REQUESTS WELCOME!