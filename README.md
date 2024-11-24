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


Adding a file to a Bsky-list:

    python3 bskylisttool.py list add <target_list_name> <file>

Fetch any Bsky list to a file:

    python3 bskylisttool.py fetch list <list_owner_handle> <list_name> <output_file>

Fetch all followers of a profile to a file:

    python3 bskylisttool.py fetch followers <handle> <file>

Fetch all likers of a post:

    python3 bskylisttool.py fetch likes <post-url> <file>

Be warned, whatever you specify as outfile, this script will overwrite it   
without warning.

Oh, and i don't know if this runs on windows. You can try out.


Roadmap
--------------------------------

- Refactor the code
- Implement error handling
- Implement status messages
- Maybe interactive mode?
- Build a GUI





