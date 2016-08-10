import argparse
import os
import fnmatch
import subprocess
import sys
import threading
import glob

class CmdLineParser:
    def __init__(self):
        self.srcDir = ''
        self.tagTool = ''
        self.cleanOnly = False
        self.noTags = False
        self.noCscope = False
        self.parser = argparse.ArgumentParser(prog = 'gen_cscope_tags.py', description = 'Generate cscope files and tags for c/cpp/sx/java source files')
        # Mandatory arguments
        self.parser.add_argument('-d', dest = 'srcDir', required = True, type = str,
                                 help = 'The root directory of source code')
        # Optional arguments
        self.parser.add_argument('--tag-tool', dest = 'tagTool', type = str,
                                 help = 'path to ctags')
        self.parser.add_argument('-c', dest = 'cleanOnly', action = 'store_true',
                                 help = 'Only clean up cscoope and tags files')
        self.parser.add_argument('--no-tags', dest = 'noTags', action = 'store_true',
                                 help = 'Don\'t build tags')
        self.parser.add_argument('--no-cscope', dest = 'noCscope', action = 'store_true',
                                 help = 'Don\'t build cscope')

    def parseArgs(self):
        parsedArgs = self.parser.parse_args()
        self.srcDir = os.path.abspath(parsedArgs.srcDir.strip())
        self.cleanOnly = parsedArgs.cleanOnly
        self.noTags = parsedArgs.noTags
        self.noCscope = parsedArgs.noCscope
        if parsedArgs.tagTool:
            self.tagTool = parsedArgs.tagTool.strip()

fileNamePatterns = ['*.[cCsShH]', '*.sh', '*.csh', '*.prg', '*.in',
                    '*.cpp', '*.java', '*.cxx', '*.cc', '*.hxx',
                    '*.hpp', '*.inl', '*.config', '*.ti']

def rmOldCscopeFiles(srcDir):
    os.chdir(srcDir)
    for f in glob.glob('cscope.*'):
        print(' Removing ' + f)
        os.remove(f)

def rmOldTagFiles(srcDir):
    for f in glob.glob('TAGS'):
        print(' Removing ' + f)
        os.remove(f)

def genSrcFileList(srcDir):
    tmpFile = os.path.join(srcDir, 'cscope.files')

    try:
        fp = open(tmpFile, 'w')
        for root, dirnames, filenames in os.walk(srcDir):
            for p in fileNamePatterns:
                for filename in fnmatch.filter(filenames, p):
                    fp.write(os.path.join(root, filename) + "\n")

        fp.close()
        return tmpFile
    except (KeyboardInterrupt, IOError) as e:
        print(' Failed to open ' + tmpFile)
        return -1

def genCscopeFiles(srcDir):
    os.chdir(srcDir)
    try:
        return subprocess.check_call(['cscope', '-k', '-b', '-q', '-R'],
                                     stderr = open(os.devnull, 'w'))
    except (KeyboardInterrupt, subprocess.CalledProcessError) as e:
        print(' Faile to generate cscope files!')
        return -1

def removeTmpFile(tmpFile):
    try:
        os.remove(tmpFile)
    except (KeyboardInterrupt, OSError) as e:
        return -1

def genTags(srcDir, tagProg = 'ctags'):
    nullDev = open(os.devnull, 'w')
    try:
        subprocess.check_call([tagProg, '--help'],
                              stdout = nullDev, stderr = nullDev)
    except (KeyboardInterrupt, subprocess.CalledProcessError) as e:
        print(tagProg + ' not installed')
        return -1

    try:
        tagsArgForEmacs = '-e'
        tagsArgLang = '--languages=Scheme,c++'
        tagsArgField = '--fields=+afikKlmnsSzt'
        tagsArgLangMap = '--langmap=Scheme:+.sx.sxdef'
        tagsArgXtra = '--extra=+q'
        tagsArgXlude = '--exclude=\"*.png\"'
        if tagProg == 'etags':
            tagsArgForEmacs = ''
            tagsArgLang = '--language=Scheme,c++'
            tagsArgField = ''
            tagsArgLangMap = ''
            tagsArgXtra = ''
            tagsArgXlude = ''
        return subprocess.check_call([tagProg, tagsArgForEmacs, tagsArgLang, tagsArgField,
                                      tagsArgLangMap, tagsArgXtra,
                                      tagsArgXlude, '-R', srcDir],
                                      stdout = nullDev, stderr = nullDev)
    except (KeyboardInterrupt, subprocess.CalledProcessError) as e:
        print(' Faile to generate tags!')
        return -1

class RepeatTimer:
    def __init__(self, step):
        self.indicator = '|'
        self.step = step
        self.msg = ''
        #secUsed = 0

    def printMessage(self, msg):
        self.msg = msg
        self.timer = threading.Timer(self.step, self.printMessage, args = [self.msg])
        self.timer.start()
        from sys import stdout
        stdout.write('\r' + self.msg + ' ' + self.indicator + '\r')
        if self.indicator == '|':
            self.indicator = '/'
        elif self.indicator == '/':
            self.indicator = '-'
        elif self.indicator == '-':
            self.indicator = '\\'
        elif self.indicator =='\\':
            self.indicator = '|'

    def stop(self, err):
        self.timer.cancel()
        if not err == -1:
            print('\r' + self.msg + ' ' + 'Done')
        else:
            print('\r' + self.msg + ' ' + 'Error! EXIT!')
            exit(err)

# Main
print('+--------- Begin ---------+')

cmdParser = CmdLineParser()
cmdParser.parseArgs()
srcDir = cmdParser.srcDir
tagTool = cmdParser.tagTool
noCscope = cmdParser.noCscope
noTags = cmdParser.noTags
print(' Working directory = ' + srcDir)
# Remove old tag files
if not noCscope:
    rmOldCscopeFiles(srcDir)

if not noTags:
    rmOldTagFiles(srcDir)

if not cmdParser.cleanOnly:
    rptmr = RepeatTimer(0.3)

    if not noCscope:
        # Generate cscope input files list
        rptmr.printMessage(' Generating files list ...')
        tmpFile = genSrcFileList(srcDir)
        rptmr.stop(tmpFile)

        # Generate cscope files
        rptmr.printMessage(' Generating cscope files ...')
        ret = genCscopeFiles(srcDir)
        rptmr.stop(ret)
        # removeTmpFile(tmpFile)

    if not noTags:
        # Generate TAGS
        rptmr.printMessage(' Generating TAGS ...')
        if tagTool == '':
            ret = genTags(srcDir)
        else:
            ret = genTags(srcDir, tagTool)
        rptmr.stop(ret)

print('+--------- End ---------+')
