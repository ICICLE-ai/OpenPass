#!/usr/bin/python3
#
# This script creates a repository and sets it up with a post receive
# hook that checks out the code to the desired directory.
#
# Really nice for setting up an easy way to push code to a remote
# server without lots of overhead.
#
# After running this script simply add a remote locally like
#
#   git remote add web ssh://you@server/path/to/repo.git
#
# Then pushing to the remote is as easy as
#
#   git push web
#
# Jeremy Keeshin
#               September 23, 2012
#   updated     March 31, 2013
#   updated     December 1, 2013
#               - print out resulting command
#
#
#Updated for the ICICLE environment by Christopher Stewart
# Jan 10, 2023
#
#

import os
import sys
import re




if len(sys.argv) != 2:
    print ("This command takes one argument.  Name of repo")
    sys.exit(1)
else:
    repo = sys.argv[1]

    if re.search("^[a-zA-Z0-9]+$",repo):
        print (repo + "is a valid name")
    else:
        print (repo + " is not a valid repo name.  Alhpanumeric characters only")
        sys.exit(1)
    repoDir = repo+".git"

    githome = "/volume/devel"
    doesExist = os.path.exists(githome)
    if (doesExist == False):
        print ("Error: The configured GitHome repo "+githome+" does not exist.  Mount it?")
        sys.exit(1)
    os.chdir('%s' % githome)
        
    scratch = "/volume/devel/scratch"
    path = "/volume/devel/scratch/" + repo
    #ensure the directory does not exist
    doesExist = os.path.exists(path)
    if (doesExist == True):
        print ("This repo "+repo+" already exists in " + path)
        sys.exit(1)
    doesExist = os.path.exists(repoDir)
    if (doesExist == True):
        print ("This repo "+repo+" already exists in current directory")
        sys.exit(1)

    # Make the git directory
    os.system('mkdir %s' % repoDir)
    os.chdir('%s' % repoDir)
    
    # Initialize a new bare repo
    os.system('git init --bare')
    
    
    # Now create icicle.firstfile and check out to the Scratch directory
    os.system('mkdir %s' % path)
    os.chdir(path)
   
    os.system('bash /home/devel/bin/gitconfig.sh')
    os.system('git init')
    os.system('mkdir cgi-bin/')
    os.system('cp -r /home/devel/icicleDABWeb/README .')
    os.system('cp -r /home/devel/icicleDABWeb/css .')
    os.system('cp -r /home/devel/icicleDABWeb/js .')
    os.system('cp -r /home/devel/icicleDABWeb/cgi-bin/embedhtml.py cgi-bin/embedhtml.py')
    os.system('git add *')
    os.system('git commit -m \'Initial commit\'')
    os.system('git remote add origin devel@localhost:/volume/devel/'+repoDir)
    os.system('git push origin master')
    

