'''
Created on Jul 2, 2014

@author: Felix Rao
'''

import argparse
import configparser
import functools
import os
import csv
from datetime import datetime

'''
Accumulates the log lines in pair with open & close tags
The results are stored in a list named tags

Paired Tags interpretation is simple, so a stack like behavior is enough
'''
class PairedTagsAccumulator:
    def __init__(self, openTag, closeTag):
        self._tags = []
        self._openStr = ''
        self._openTag = openTag
        self._closeTag = closeTag

    def GetResult(self):
        return self._tags
    
    def Restart(self):
        self._openStr = ''

    def Accumulate(self, line):
        if line.find(self._openTag) >= 0:
            if self._openStr:
                # Unexpected open tag
                pass
            # Update current open line to the latest one
            self._openStr = line
                
        elif line.find(self._closeTag) >= 0:
            if not self._openStr:
                # Unexpected close tag
                pass
            else:
                self._tags.append((self._openStr, line))
                self._openStr = ''

'''
Accumulates the log lines in pair with open & intermediate & close tags
The results are stored in a list named tags

Triad tags are a bit complex to deal with. This is a naive implementation
A good & robust implementation should use state machine
'''
class TriadTagsAccumulator(PairedTagsAccumulator):
    def __init__(self, openTag, closeTag, tag3):
        PairedTagsAccumulator.__init__(self, openTag, closeTag)
        self._interTag = tag3
        self._interStr = ''
        self._interFlag = False
        
    def GetResult(self):
        return PairedTagsAccumulator.GetResult(self)
    
    def Restart(self):
        self._interStr = ''
        PairedTagsAccumulator.Restart()

    def Accumulate(self, line):
        if (line.find(self._openTag) >= 0):
            if (self._openStr or self._interStr):
                # Unclosed open tag
                pass
            else:
                self._openStr = line
        elif (line.find(self._interTag) >= 0):
            if (not self._openStr):
                # Unexpected intermediate tag
                pass
            elif (self._interFlag):
                PairedTagsAccumulator.GetResult(self).append((self._interStr, line))
                self._interStr = line
            elif (self._openStr):
                #self.tags.append((self.openStr, line))
                self._interStr = line
                self._interFlag = True
        elif (line.find(self._closeTag) >= 0):
            if (not (self._openStr and self._interStr)):
                # Unexpected close tag
                pass
            else:
                if (self._interFlag):
                    #self.tags.append((self.interStr, line))
                    pass
                else:
                    #self.tags.append((self.interStr, line))
                    pass
                self._openStr = ''
                self._interFlag = False
                self._interStr = ''

'''
State machine is best choice to implementation this

The naive implementation below just works. It's not generic and robust
'''
class PairedTagsAccumulatorWith2PreCond:
    def __init__(self, strPreCond1, strBeginTag, strPreCond2, strEndTag):
        self._beginAccu = PairedTagsAccumulator(strPreCond1, strBeginTag)
        self._endAccu = PairedTagsAccumulator(strPreCond2, strEndTag)
        self._tags = []

    def Accumulate(self, line):
        self._beginAccu.Accumulate(line)
        if (self._beginAccu.GetResult()):
            self._endAccu.Accumulate(line)
    
    def GetResult(self):
        beginTags = self._beginAccu.GetResult()
        endTags = self._endAccu.GetResult()
        for i in range(0, len((beginTags if len(beginTags) < len(endTags) else endTags))):
            self._tags.append((beginTags[i][-1], endTags[i][-1]))
        return self._tags

    def Restart(self):
        self._beginAccu.Restart()
        self._endAccu.Restart()

'''
Accumulates the log lines in pair with open & close tags
The count of close tag is more than 1
The results are stored in a list named tags

Paired Tags interpretation is simple, so a stack like behavior is enough
'''
class PairedTagsAccumulatorWithCloseTagOccurencies(PairedTagsAccumulator):
    def __init__(self, openTag, closeTag, nCount):
        PairedTagsAccumulator.__init__(self, openTag, closeTag)
        self._tags = []
        self._count = nCount
        self._curCount = nCount

    def GetResult(self):
        return self._tags
    
    def Restart(self):
        PairedTagsAccumulator.Restart(self)
        self._curCount = self._count

    def Accumulate(self, line):
        if line.find(self._closeTag) >= 0:
            self._curCount -= 1
            if self._curCount == 0:
                PairedTagsAccumulator.Accumulate(self, line)
                self._curCount = self._count
        else:
            PairedTagsAccumulator.Accumulate(self, line)

'''
Calculator the time delta between start time and end time in a pair
The input is a list of start time & end time pairs
After call to CalculateMilliSeconds, the results are stored in a list named results

This class can be transformed to a function
'''
class TimeDeltaCalculator:
    def __init__(self, timeFmt, listTimeAccu):
        self.count = len(listTimeAccu)
        self.timeFmt = timeFmt
        self.listTimeAccu = listTimeAccu
        self.results = []
        
    def CalculateMilliSeconds(self):
        for tup in self.listTimeAccu:
            timeBegin = datetime.strptime(tup[0], self.timeFmt)
            timeEnd = datetime.strptime(tup[-1], self.timeFmt)
            if timeEnd != timeBegin:
                delta = timeEnd - timeBegin
                self.results.append((delta.days * 24 * 60 * 60
                                     + delta.seconds * 1000
                                     + delta.microseconds / 1000
                                     ))
    def CalculateAverage(self):
        if self.count > 0:
            return functools.reduce(lambda x, y: x + y, self.results) * 1.0 / self.count
        else:
            return 0

'''
Extract timestamp from a string.
The result is the timestamp string without any other info
'''
def ExtractTimestamp(line, nStartPos = 0, nLen = 0, strBeginTag = '', strEndTag = ''):
    if (strBeginTag and strEndTag):
        return line[line.find(strBeginTag) : line.find(strEndTag)]
    else:
        if (nLen == 0):
            return ''
        else:
            return line[nStartPos : nStartPos + nLen]

def FormatResults(timeCalculator, strName, strTag1 = '', strTag2 = '', strTag3 = '', strTag4 = '', count = 0):
    print('*---------- ' + strName + ' ----------*')
    print('Tag1    = ' + strTag1)
    print('Tag2    = ' + strTag2)
    print('Tag3    = ' + strTag3)
    print('Tag4    = ' + strTag4)
    print('Count   = ' + str(timeCalculator.count))
    print('Results = ' + ' '.join(map(lambda x: str(x) + 'ms', timeCalculator.results)))
    print('Average = ' + str(timeCalculator.CalculateAverage()) + 'ms')
    if (timeCalculator.CalculateAverage() != 0.0):
        if (strTag2 and strTag3):
            print('Rate    = ' + str(1000.0 / timeCalculator.CalculateAverage()) + 'fps')
        if (count != 0):
            print('Rate    = ' + str(1000.0 / timeCalculator.CalculateAverage() * count) + 'fps')
    print('*---------- ' + strName + ' ----------*')
    
def WriteResultsToCsv(file, timeCalculator, strName):
    delim = ',' # Default for windows
    csvWriter = csv.writer(csvFile, delimiter=delim)
    csvWriter.writerow([strName, '', 'Unit: ms'])
    csvWriter.writerow(['', 'Count', timeCalculator.count])
    csvWriter.writerow(['', 'Average', timeCalculator.CalculateAverage()])
    csvWriter.writerow(['', 'Results'] + timeCalculator.results)
    #csvWriter.writerows([['', result] for result in timeCalculator.results])

'''
POD class to pack timestamp info in a string
'''
class TimestampFmt:
    def __init__(self, nPos, nLen, strBeginTag, strEndTag, strFmt):
        self.nPos = nPos
        self.nLen = nLen
        self.beginTag = strBeginTag
        self.endTag = strEndTag
        self.fmt = strFmt

'''
Generates the timestamp pair (begin, end) from accumulator into a list
'''
def GeneratePairedTimestamps(pairedAccu, timestampFmt):
    beginTimes = map(lambda x: ExtractTimestamp(x,
                                                int(timestampFmt.nPos),
                                                int(timestampFmt.nLen),
                                                timestampFmt.beginTag,
                                                timestampFmt.endTag),
                     [beginTime[0] for beginTime in pairedAccu.GetResult()])
    endTimes   = map(lambda x: ExtractTimestamp(x,
                                                int(timestampFmt.nPos),
                                                int(timestampFmt.nLen),
                                                timestampFmt.beginTag,
                                                timestampFmt.endTag),
                     [endTime[-1] for endTime in pairedAccu.GetResult()])
    return list(zip(beginTimes, endTimes))

'''
Parses the command line arguments
'''
class CmdLineParser:
    def __init__(self):
        self.iniFile = ''
        self.csvPath = ''
        self.logFiles = []
        self.parser = argparse.ArgumentParser(prog='log2time.py',
                                description='Parse AoL log files containing timestamp')
        self.parser.add_argument('--log', dest='logFiles', required=True, type=str,
                                 metavar='LOGFILE', nargs='+', action='append',
                                 help='path to log file')
        self.parser.add_argument('--csvpath', dest='csvPath', type=str,
                                 metavar='CSVPATH',
                                 help='path to log file')
        self.parser.add_argument('--ini', dest='iniFile', type=str,
                                 help='coverity check build')
    def ParseArgs(self):
        parsedArgs = self.parser.parse_args()
        if parsedArgs.iniFile:
            self.iniFile = os.path.abspath(parsedArgs.iniFile.strip())
        #self.csvPath = os.path.dirname(os.path.abspath(parsedArgs.csvPath.strip()))
        if parsedArgs.csvPath:
            self.csvPath = os.path.abspath(parsedArgs.csvPath.strip())
        self.logFiles = [f[0] for f in parsedArgs.logFiles]
        map(lambda x: os.path.abspath(x.strip()), self.logFiles)

'''
Main routine
'''
if __name__ == '__main__':
    # Parses the command line arguments
    cmdLineParser = CmdLineParser()
    cmdLineParser.ParseArgs()
    iniFile = cmdLineParser.iniFile
    csvPath = cmdLineParser.csvPath
    # set ini file to default if not specified from command line
    if (not iniFile):
        iniFile = './config.ini'
    # Parses ini file
    iniConf = configparser.ConfigParser()
    with open(iniFile, 'r') as inifile:
        iniConf.read_file(inifile)
    
    # Reads timestamp settings
    timestampFmt = TimestampFmt(iniConf['GLOBAL']['log_time_start_pos'],
                                iniConf['GLOBAL']['log_time_length'],
                                iniConf['GLOBAL']['log_time_prefix'],
                                iniConf['GLOBAL']['log_time_postfix'],
                                iniConf['GLOBAL']['log_time_format'])        

    # Parses log files into section specific accumulator
    # One accumulator per section
    for section in iniConf.sections():
        # GLOBAL section contains only global settings
        if (section == 'GLOBAL'):
            pass
        else:
            accumulator = None
            tag3 = ''
            tag4 = ''
            count = 0
            if 'intermediate' in iniConf[section]:
                # For sections with 3 tags: open, intermediate, close
                tag3 = iniConf[section]['intermediate']
                accumulator = TriadTagsAccumulator(iniConf[section]['start'],
                                                   iniConf[section]['end'],
                                                   tag3)
            elif ('precond1' in iniConf[section] and 'precond2' in iniConf[section]):
                tag3 = iniConf[section]['precond1']
                tag4 = iniConf[section]['precond2']
                accumulator = PairedTagsAccumulatorWith2PreCond(tag3,
                                                                iniConf[section]['start'],
                                                                tag4,
                                                                iniConf[section]['end'])
            else:
                # For sections with 2 tags: open, close
                if 'count' in iniConf[section]:
                    count = int(iniConf[section]['count'])
                    accumulator = PairedTagsAccumulatorWithCloseTagOccurencies(iniConf[section]['start'],
                                                                               iniConf[section]['end'],
                                                                               count)
                else:
                    accumulator = PairedTagsAccumulator(iniConf[section]['start'],
                                                        iniConf[section]['end'])
    
            for logFileName in cmdLineParser.logFiles:
                    with open(logFileName, 'r') as logFile:
                        for line in logFile.readlines():
                            accumulator.Accumulate(line)
                    accumulator.Restart()
    
            calc = TimeDeltaCalculator(timestampFmt.fmt,
                                       GeneratePairedTimestamps(accumulator, timestampFmt))
            calc.CalculateMilliSeconds()
            FormatResults(calc, section, iniConf[section]['start'], iniConf[section]['end'], tag3, tag4, count)
            try:
                if csvPath:
                    # Remove millisecond, length 6
                    csvFile = open(csvPath + os.sep +
                                   datetime.now().isoformat(sep='-').replace(':', '-')[:-len('.000000')] +
                                   '-' + section + '.csv',
                                   'w',
                                   newline='')
                    WriteResultsToCsv(csvFile, calc, section)
            except:
                csvFile.close()
                
