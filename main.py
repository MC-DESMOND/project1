import module 
import sys
try:
    module.TerminalApp(list(sys.argv)).run()
except:
    module.App('#010F14').run()