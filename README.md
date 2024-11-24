Bsky List Tools by Chaosbengel
==============================

Initially I wanted to create a short script that makes adding a list of   
Bsky-handles to a Bsky list more easy and less cumbersome. Then,  
a user requested a list-backup function and now i've got ideas for  
a complete toolset for Bsky-related tasks, so theres more to come.

Description
------------------------------

This script is able to add a text file containing Bsky-handles or dids, one  
per line, to a bsky-list.

Also, you can convert any Bsky-list to a textfile containing the dids  
of the profiles the list contains.

Warning
-------------------------------

This is a very early version of these tools. They're not very sophisticated  
at this stage, so expect errors, and if you find some, open an issue!

Installation
-------------------------------

The script depends on the atproto package (Available at Pypi)  
https://pypi.org/project/atproto/

- Install the atproto package listed above
- download and copy bskylisttool.py and config.example to a   
location of your choice
- rename config.example to config
- replace the values in config with your own Bluesky credentials  
  (For security reasons, make sure to use an app password!)

Usage
--------------------------------

There are just two commands yet:

Adding a file to a Bsky-list:

    python3 bskylisttool.py list add <target_list_name> <file>

Download any Bsky list to a file:

    python3 bskylisttool.py list download <list_owner_handle> <list_name> <output_file>

Be warned, whatever you specify as outfile, this script will overwrite it   
without warning.

Oh, and i don't know if this runs on windows. You can try out.


Roadmap
--------------------------------

- Store request-auth token and use it instead of password if its valid.
- Add a function do download a profiles followers to a textfile
- Add a function to get the profiles of all likers of a post
- Make this more 'userfriendly'





