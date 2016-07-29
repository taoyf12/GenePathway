"""
Common functions for proppr helpers.
"""
import sys
import os
import subprocess
import logging

MAX_FILE_LINES_TO_ECHO = 15

def getResourceFile(opts,filename):
    if '--n' not in opts: #not dry run
        if not os.access(filename,os.W_OK):
            if os.access(filename,os.R_OK):
                logging.warn("Can't update %s, running with existing copy" % filename)
                return filename
        src = os.path.join( '%s/scripts/proppr-helpers/%s' % (os.environ['PROPPR'], filename))
        dst = filename
        fp = open(dst,'w')
        for line in open(src):
            fp.write(line)
        logging.info('copied %s to current directory' % src)
    return filename

def catfile(fileName,msg):
    """Print out a created file - for  debugging"""
    print msg
    ret = '+------------------------------\n'
    k = 0
    with open(fileName) as f:
        for line in f:
            if line.startswith("#"): continue # skip comments [kmm]
            ret += ' | '+line
            k += 1
            if k>MAX_FILE_LINES_TO_ECHO:
                ret += ' | ...\n'
                break
    ret += '+------------------------------'
    return ret

def makeOutput(opts,filename):
   """Create an output filename with the requested filename, in the -C directory if requested."""
   outdir = opts.get('--C','')
   if not outdir: 
       return filename
   elif filename.startswith(outdir): 
       return filename
   else:
       return os.path.join(outdir,filename)

def invokeProppr(opts,*args):
    procArgs = ['%s/scripts/proppr' % os.environ['PROPPR']]
    #deal with proppr's global options
    if '--C' in opts:
        procArgs.extend(['-C'+opts['--C']])
    if '--n' in opts:
        procArgs.extend(['-n'])
    procArgs.extend(args)
    procArgs.extend(opts['PROPPR_ARGS'])
    _callProcess(opts,procArgs)
            
def invokeHelper(opts,cmd,*args):
    procArgs = ['%s/scripts/proppr-helpers/%s' % (os.environ['PROPPR'],cmd)]
    procArgs.extend(args)
    _callProcess(opts,procArgs)
            
def _callProcess(opts,args,**kw):
   """Call a process, tracing the actual call."""
   logging.info('calling: ' + ' '.join(args))
   if "--n" in opts: return
   stat = subprocess.call(args,**kw)
   if stat:
      logging.info(('call failed (status %d): ' % stat) + ' '.join(args))
      sys.exit(stat) #propagate failure
    
