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

def fileAppendLine(fname, line):
    f=open(fname,'a+')
    if (f.writable() == True):
        f.writelines(line)
    f.close()


if len(sys.argv) != 2:
    print ("This command takes one argument.  Name of microservice")
    sys.exit(1)
else:
    repo = sys.argv[1]

    if re.search("^[0-9]+[a-zA-Z0-9]+$",repo):
        print (repo + "is a valid name")
    else:
        print (repo + " is not a valid repo name.  Microservices must begin with a number N and the descriptive name D.  Regular expression is [0-9]*[a-zA-Z0-9]+")
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
        print ("This repo "+repo+" already exists in " + githome)
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
    fileAppendLine("world.icicle","0")
    fileAppendLine("devel.icicle","0")    

    # Chris Stewart comments
    # When this script was first created, the startup scripts were
    # by default empty.  The presumption was that these scripts could
    # vary substantially between microservices.  This was Jan 2023.
    # As of June 2023, it is clear that the simplicity of a plug-and-play
    # microservice as default will help developers.  Thus the original
    # code has been commented (below).
    # The new code simply pulls the startup scripts as they appear in the
    # webservice.  Of course, developers can customize as needed.
    # CS - 6/23
    #fileAppendLine("readme.icicle","This is a new Microservice. Please add the spec here as well as additional details.\n")
    #fileAppendLine("softwareenv.sh","#!/usr/bin/bash\n")
    #fileAppendLine("softwareenv.sh","apt-get install wget\n")
    #fileAppendLine("code.sh","#!/bin/bash\n")
    #fileAppendLine("code.sh","#Add commands to download code here\n")
    #fileAppendLine("data.sh","#!/bin/bash\n")
    #fileAppendLine("data.sh","#Add commands to download data here\n")
    #fileAppendLine("setup.sh","#!/bin/bash\n")
    #fileAppendLine("setup.sh","#Add commands to move/organize the Docker container here\n")
    #fileAppendLine("unittest.py","#!/bin/bash\n")
    #fileAppendLine("unittest.py","#Add commands to ensure your microservice is up and working correctly.  Write output test.log and test.success.  The latter, test.success, should have one value inside 0/1\n")
    #fileAppendLine("unittest.py","echo 1 > test.success \n")
    os.system('cp /home/devel/30080website/softwareenv.sh .')
    os.system('cp /home/devel/30080website/code.sh .')    
    os.system('cp /home/devel/30080website/data.sh .')
    os.system('cp /home/devel/30080website/setup.sh .')
    os.system('cp /home/devel/30080website/unittest.py .')
    os.system('cp /home/devel/30080website/jayzgotdakeys.sh .')
    
    os.system('git add *')    
    os.system('git commit -m \'Initial commit\'')
    os.system('git remote add origin devel@localhost:/volume/devel/'+repoDir)
    os.system('git push origin master')
    

