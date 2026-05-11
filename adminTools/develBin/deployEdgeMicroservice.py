#!/usr/bin/python3
# Delegates to the canonical script in bin/ to avoid duplication.
import os, sys, subprocess
canonical = os.path.join(os.path.dirname(__file__), '../../bin/deployEdgeMicroservice.py')
sys.exit(subprocess.call([sys.executable, os.path.realpath(canonical)] + sys.argv[1:]))
