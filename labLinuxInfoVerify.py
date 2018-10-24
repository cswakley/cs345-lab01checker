##################################################################
# labLinuxInfoVerify.py
#
# Author: Curtis Wakley, July 2018
#
# Version: 1.0.0
#
# Purpose: For the verification of output from the shell scripts
#          for Lab01 of the Operating Systems class.
#
#          To run, run the command $ python labLinuxInfoVerify.py
#          The program will find all of the files in your current
#          working directory labeled .sh and check them with the
#          sample code. If you want to specify a file, you can.
#          $ python labLinuxInfoVerify.py yourFile.sh
#          These details are also listed with a -h flag.
#          
#          The program will output whether each line of the student's
#          script has a valid answer or not. Any errors will be 
#          indicated with red text and a message afterwards. For
#          example, if the student uses three spaces for the answer
#          instead of four, the output could look something like this:
#
#          ERROR: Mismatch. If your results match expected, double check your spaces.
#          Student :   4 processors
#          Expected:    4 processors
#
##################################################################

import sys
import pexpect
import re
from subprocess import call
from os import listdir
from os.path import isfile, join

# This global variable will be the directory where your sample code is. Change this as needs be.
SAMPLE_CODE = "./labLinuxInfoSample"

##################################################################
# Colors to improve the look of the output on the terminal
##################################################################
class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class nocolors:
    HEADER = ''
    OKBLUE = ''
    OKGREEN = ''
    WARNING = ''
    FAIL = ''
    ENDC = ''
    BOLD = ''
    UNDERLINE = ''

##################################################################
# Outputs the OK statement as desired.
##################################################################
def okMsg(bcolors, line, end=False):
    print(bcolors.OKGREEN + "OK" + bcolors.ENDC + ": %s" % line)
    if end:
        print("")

##################################################################
# Outputs the ERROR statement, with a message that depends on the issue.
##################################################################
def errorMsg(bcolors, message, student="NULL", expected="NULL"):
    availMessages = ["Mismatch. If your results match expected, double check your spaces.", "Value for uptime is incorrect.", "Value for seconds is incorrect.", 
    "Result does not fall under the percent difference.", "Double check your spaces.", "Result does not fall between the before and after check.", 
    "Unneeded comma found at the end of the previous statement."]
    print(bcolors.FAIL + "ERROR" + bcolors.ENDC + ": " + availMessages[message])
    if student != "NULL":
        print("Student :%s" % student)
    if expected != "NULL":
        print("Expected:%s" % expected.replace("\\", ""))
    print("")

##################################################################
# Does the job of comparing the student's file to the base file.
##################################################################
def compare(filename, expected, bcolors):
    try:
        assert (filename[-3:] == ".sh"), "Only files ending in .sh can be used in this program!"
    except AssertionError:
        print("Only files ending in .sh can be used in this program!\n")
        exit(1)
    
    file = "./" + filename

    try:
        f = open(file[:-3] + ".txt", "w")
    except:
        print(bcolors.FAIL + "Error opening up a text file to write to. Stopping...\n" + bcolors.ENDC)
        return

    try:
        call([file], stdout=f)
        f.close()
        child = pexpect.spawn("cat " + file[:-3] + ".txt")
    except:
        print(bcolors.FAIL + "Unable to open student's code, " + filename + ". Stopping...\n" + bcolors.ENDC)
        call(["rm", file[:-3] + ".txt"])
        return

    try:
        afterCheck = pexpect.spawn(SAMPLE_CODE)
    except:
        print(bcolors.FAIL + "Error opening up the sample code for the after check. Stopping...\n" + bcolors.ENDC)
        call(["rm", file[:-3] + ".txt"])
        return

    # What is the CPU type and model?
    try:
        i = child.expect([expected[0] + '[ ]?', '[^\r\n]+'])
    except pexpect.EOF:
        print(bcolors.WARNING + "End of file reached before expected end. Stopping check...\n" + bcolors.ENDC)
        call(["rm", file[:-3] + ".txt"])
        return
    line = child.after
    if i==0:
        okMsg(bcolors, line)
    elif i==1:
        errorMsg(bcolors, 0, line, expected[0])

    # Answer 1
    try: 
        i = child.expect([expected[1] + '[ ]?', '[^\r\n]+'])
    except pexpect.EOF:
        print(bcolors.WARNING + "End of file reached before expected end. Stopping check...\n" + bcolors.ENDC)
        call(["rm", file[:-3] + ".txt"])
        return
    line = child.after
    if i==0:
        okMsg(bcolors, line, True)
    elif i==1:
        errorMsg(bcolors, 0, line, expected[1])

    # How many processors on this system?
    try:
        i = child.expect([expected[2] + '[ ]?', '[^\r\n]+'])
    except pexpect.EOF:
        print(bcolors.WARNING + "End of file reached before expected end. Stopping check...\n" + bcolors.ENDC)
        call(["rm", file[:-3] + ".txt"])
        return
    line = child.after
    if i==0:
        okMsg(bcolors, line)
    elif i==1:
        errorMsg(bcolors, 0, line, expected[2])

    # Answer 2
    try:
        i = child.expect([expected[3] + '[ ]?', '[^\r\n]+'])
    except pexpect.EOF:
        print(bcolors.WARNING + "End of file reached before expected end. Stopping check...\n" + bcolors.ENDC)
        call(["rm", file[:-3] + ".txt"])
        return
    line = child.after
    if i==0:
        okMsg(bcolors, line, True)
    elif i==1:
        errorMsg(bcolors, 0, line, expected[3])

    # What version of the Linux kernel is being used?
    try:
        i = child.expect([expected[4] + '[ ]?', '[^\r\n]+'])
    except pexpect.EOF:
        print(bcolors.WARNING + "End of file reached before expected end. Stopping check...\n" + bcolors.ENDC)
        call(["rm", file[:-3] + ".txt"])
        return
    line = child.after
    if i==0:
        okMsg(bcolors, line)
    elif i==1:
        errorMsg(bcolors, 0, line, expected[4])

    # Answer 3
    try:
        i = child.expect([expected[5] + '[ ]?', '[^\r\n]+'])
    except pexpect.EOF:
        print(bcolors.WARNING + "End of file reached before expected end. Stopping check...\n" + bcolors.ENDC)
        call(["rm", file[:-3] + ".txt"])
        return
    line = child.after
    if i==0:
        okMsg(bcolors, line, True)
    elif i==1:
        errorMsg(bcolors, 0, line, expected[5])
    
    # How long has it been since the system was last booted?
    try:
        i = child.expect([expected[6] + '[ ]?', '[^\r\n]+'])
    except pexpect.EOF:
        print(bcolors.WARNING + "End of file reached before expected end. Stopping check...\n" + bcolors.ENDC)
        call(["rm", file[:-3] + ".txt"])
        return
    line = child.after
    if i==0:
        okMsg(bcolors, line)
    elif i==1:
        errorMsg(bcolors, 0, line, expected[6])

    # Answer 4
    try:
        i = child.expect(['    up \d+ day[s]?, \s?\d+[:]\d\d[ ]?', '[^\r\n]+'])
    except pexpect.EOF:
        print(bcolors.WARNING + "End of file reached before expected end. Stopping check...\n" + bcolors.ENDC)
        call(["rm", file[:-3] + ".txt"])
        return
    line = child.after
    afterCheck.expect('up \d+ day[s]?, \s?\d+[:]\d\d')
    check = afterCheck.after.decode('UTF-8')
    if i==0:
        stnt = line.decode('UTF-8')
        stntNum = [int(s) for s in re.findall("\d+", stnt)]
        beforeNum = [int(s) for s in re.findall("\d+", expected[7])]
        afterNum = [int(s) for s in re.findall("\d+", check)]

        studentTime = (stntNum[0] * 24 * 60) + (stntNum[1] * 60) + stntNum[2]
        beforeTime = (beforeNum[0] * 24 * 60) + (beforeNum[1] * 60) + beforeNum[2]
        afterTime = (afterNum[0] * 24 * 60) + (afterNum[1] * 60) + afterNum[2]

        if beforeTime <= studentTime and studentTime <= afterTime:
            okMsg(bcolors, line, True)
        else:
            errorMsg(bcolors, 1, line, expected[7])
    elif i==1:
        errorMsg(bcolors, 0, line, expected[7])

    try:
        i = child.expect([',', ''])
    except pexpect.EOF:
        print(bcolors.WARNING + "End of file reached before expected end. Stopping check...\n" + bcolors.ENDC)
        call(["rm", file[:-3] + ".txt"])
        return
    if i==0:
        errorMsg(bcolors, 6, ",", "")

    # How much CPU execution time has been spent in user, system and idle modes?
    try:
        i = child.expect([expected[8] + '[ ]?', '[^\r\n]+'])
    except pexpect.EOF:
        print(bcolors.WARNING + "End of file reached before expected end. Stopping check...\n" + bcolors.ENDC)
        call(["rm", file[:-3] + ".txt"])
        return
    line = child.after
    if i==0:
        okMsg(bcolors, line)
    elif i==1:
        errorMsg(bcolors, 0, line, expected[8])

    # Answer 5
    try:
        i = child.expect(['    USER: \d+[.]\d\d seconds[ ]?', '[^\r\n]+'])
    except pexpect.EOF:
        print(bcolors.WARNING + "End of file reached before expected end. Stopping check...\n" + bcolors.ENDC)
        call(["rm", file[:-3] + ".txt"])
        return
    line = child.after
    afterCheck.expect('USER: \d+[.]\d\d seconds')
    check = afterCheck.after
    if i==0:
        if expected[9].encode('UTF-8') <= line and line <= check:
            okMsg(bcolors, line)
        else:
            errorMsg(bcolors, 2, line, expected[9])
    elif i==1:
        errorMsg(bcolors, 0, line, expected[9])

    # Answer 6
    try:
        i = child.expect(['    SYSTEM: \d+[.]\d\d seconds[ ]?', '[^\r\n]+'])
    except pexpect.EOF:
        print(bcolors.WARNING + "End of file reached before expected end. Stopping check...\n" + bcolors.ENDC)
        call(["rm", file[:-3] + ".txt"])
        return
    line = child.after
    afterCheck.expect('SYSTEM: \d+[.]\d\d seconds')
    check = afterCheck.after
    if i==0:
        if expected[10].encode('UTF-8') <= line and line <= check:
            okMsg(bcolors, line)
        else:
            errorMsg(bcolors, 2, line, expected[10])
    elif i==1:
        errorMsg(bcolors, 0, line, expected[10])

    # Answer 7
    try:
        i = child.expect(['    IDLE: \d+[.]\d\d seconds[ ]?', '[^\r\n]+'])
    except pexpect.EOF:
        print(bcolors.WARNING + "End of file reached before expected end. Stopping check...\n" + bcolors.ENDC)
        call(["rm", file[:-3] + ".txt"])
        return
    line = child.after
    afterCheck.expect('IDLE: \d+[.]\d\d seconds')
    check = afterCheck.after
    if i==0:
        if expected[11].encode('UTF-8') <= line and line <= check:
            okMsg(bcolors, line, True)
        else:
            errorMsg(bcolors, 2, line, expected[11])
    elif i==1:
        errorMsg(bcolors, 0, line, expected[11])

    # How much memory is on the machine?
    try:
        i = child.expect([expected[12] + '[ ]?', '[^\r\n]+'])
    except pexpect.EOF:
        print(bcolors.WARNING + "End of file reached before expected end. Stopping check...\n" + bcolors.ENDC)
        call(["rm", file[:-3] + ".txt"])
        return
    line = child.after
    if i==0:
        okMsg(bcolors, line)
    elif i==1:
        errorMsg(bcolors, 0, line, expected[12])

    # Answer 8
    try:
        i = child.expect([expected[13] + '[ ]?', '[^\r\n]+'])
    except pexpect.EOF:
        print(bcolors.WARNING + "End of file reached before expected end. Stopping check...\n" + bcolors.ENDC)
        call(["rm", file[:-3] + ".txt"])
        return
    line = child.after
    if i==0:
        okMsg(bcolors, line, True)
    elif i==1:
        errorMsg(bcolors, 0, line, expected[13])

    # How much memory is currently available?
    try:
        i = child.expect([expected[14] + '[ ]?', '[^\r\n]+'])
    except pexpect.EOF:
        print(bcolors.WARNING + "End of file reached before expected end. Stopping check...\n" + bcolors.ENDC)
        call(["rm", file[:-3] + ".txt"])
        return
    line = child.after
    if i==0:
        okMsg(bcolors, line)
    elif i==1:
        errorMsg(bcolors, 0, line, expected[14])

    # Answer 9
    # Need to check the % difference
    try:
        i = child.expect(['    MemFree:\s+\d+ kB[ ]?', '[^\r\n]+'])
    except pexpect.EOF:
        print(bcolors.WARNING + "End of file reached before expected end. Stopping check...\n" + bcolors.ENDC)
        call(["rm", file[:-3] + ".txt"])
        return
    line = child.after
    afterCheck.expect('MemFree:\s+\d+ kB')
    check = afterCheck.after.decode('UTF-8')
    if i==0:
        stnt = line.decode('UTF-8')
        stntNum = [int(s) for s in re.findall("\d+", stnt)]
        beforeNum = [int(s) for s in re.findall("\d+", expected[15])]
        afterNum = [int(s) for s in re.findall("\d+", check)]

        # Now check for % difference. Tolerance is 2.0%
        fault = False
        res = stntNum[0] - beforeNum[0]
        res = (res / beforeNum[0]) * 100

        if res > 2.0 and res < -2.0:
            fault = True
        res = afterNum[0] - stntNum[0]
        res = (res / stntNum[0]) * 100

        if res > 2.0 and res < -2.0:
            fault = True
        # If fault was set to true, then the error will be shown.
        if fault:
            errorMsg(bcolors, 3, line, expected[15])
        else:
            okMsg(bcolors, line, True)
    elif i==1:
        errorMsg(bcolors, 0, line, expected[15])

    # How many kBytes have been read and written to the disk since the last reboot?
    try:
        i = child.expect([expected[16] + '[ ]?', '[^\r\n]+'])
    except pexpect.EOF:
        print(bcolors.WARNING + "End of file reached before expected end. Stopping check...\n" + bcolors.ENDC)
        call(["rm", file[:-3] + ".txt"])
        return
    line = child.after
    if i==0:
        okMsg(bcolors, line)
    elif i==1:
        errorMsg(bcolors, 0, line, expected[16])
    
    # Answer 10
    try:
        i = child.expect(['    Read: \d+ kB[ ]?', '[^\r\n]+'])
    except pexpect.EOF:
        print(bcolors.WARNING + "End of file reached before expected end. Stopping check...\n" + bcolors.ENDC)
        call(["rm", file[:-3] + ".txt"])
        return
    line = child.after
    afterCheck.expect('Read: \d+ kB')
    check = afterCheck.after
    if i==0:
        if expected[17].encode('UTF-8') <= line and line <= check:
            okMsg(bcolors, line)
        else:
            errorMsg(bcolors, 5, line, expected[17])
    elif i==1:
        errorMsg(bcolors, 0, line, expected[17])

    # Answer 11
    try:
        i = child.expect(['    Written: \d+ kB[ ]?', '[^\r\n]+'])
    except pexpect.EOF:
        print(bcolors.WARNING + "End of file reached before expected end. Stopping check...\n" + bcolors.ENDC)
        call(["rm", file[:-3] + ".txt"])
        return
    line = child.after
    afterCheck.expect('Written: \d+ kB')
    check = afterCheck.after
    if i==0:
        if expected[18].encode('UTF-8') <= line and line <= check:
            okMsg(bcolors, line, True)
        else:
            errorMsg(bcolors, 5, line, expected[18])
    elif i==1:
        errorMsg(bcolors, 0, line, expected[18])

    # How many processes have been created since the last reboot?
    try:
        i = child.expect([expected[19] + '[ ]?', '[^\r\n]+'])
    except pexpect.EOF:
        print(bcolors.WARNING + "End of file reached before expected end. Stopping check...\n" + bcolors.ENDC)
        call(["rm", file[:-3] + ".txt"])
        return
    line = child.after
    if i==0:
        okMsg(bcolors, line)
    elif i==1:
        errorMsg(bcolors, 0, line, expected[19])

    # Answer 12
    try:
        i = child.expect(['    Processes created: \d+[ ]?', '[^\r\n]+'])
    except pexpect.EOF:
        print(bcolors.WARNING + "End of file reached before expected end. Stopping check...\n" + bcolors.ENDC)
        call(["rm", file[:-3] + ".txt"])
        return
    line = child.after
    afterCheck.expect('Processes created: \d+')
    check = afterCheck.after
    if i==0:
        if expected[20].encode('UTF-8') <= line and line <= check:
            okMsg(bcolors, line, True)
        else:
            errorMsg(bcolors, 5, line, expected[20])
    elif i==1:
        errorMsg(bcolors, 0, line, expected[20])

    # How many context switches have been performed since the last reboot?
    try:
        i = child.expect([expected[21] + '[ ]?', '[^\r\n]+'])
    except pexpect.EOF:
        print(bcolors.WARNING + "End of file reached before expected end. Stopping check...\n" + bcolors.ENDC)
        call(["rm", file[:-3] + ".txt"])
        return
    line = child.after
    if i==0:
        okMsg(bcolors, line)
    elif i==1:
        errorMsg(bcolors, 0, line, expected[21])

    # Answer 13
    try:
        i = child.expect(['    Context switches: \d+[ ]?', '[^\r\n]+'])
    except pexpect.EOF:
        print(bcolors.WARNING + "End of file reached before expected end. Stopping check...\n" + bcolors.ENDC)
        call(["rm", file[:-3] + ".txt"])
        return
    line = child.after
    afterCheck.expect('Context switches: \d+')
    check = afterCheck.after
    if i==0:
        if expected[22].encode('UTF-8') <= line and line <= check:
            okMsg(bcolors, line, True)
        else:
            errorMsg(bcolors, 5, line, expected[22])
    elif i==1:
        errorMsg(bcolors, 0, line, expected[22])

    # What is the current load average for the last 1, 5 and 15 minutes?
    try:
        i = child.expect([expected[23] + '[ ]?', '[^\r\n]+'])
    except pexpect.EOF:
        print(bcolors.WARNING + "End of file reached before expected end. Stopping check...\n" + bcolors.ENDC)
        call(["rm", file[:-3] + ".txt"])
        return
    line = child.after
    if i==0:
        okMsg(bcolors, line)
    elif i==1:
        errorMsg(bcolors, 0, line, expected[23])

    # Answer 14
    try:
        i = child.expect(['    Load average: \d+[.]\d\d, \d+[.]\d\d, \d+[.]\d\d[ ]?', '[^\r\n]+'])
    except pexpect.EOF:
        print(bcolors.WARNING + "End of file reached before expected end. Stopping check...\n" + bcolors.ENDC)
        call(["rm", file[:-3] + ".txt"])
        return
    line = child.after
    afterCheck.expect('Load average: \d+[.]\d\d, \d+[.]\d\d, \d+[.]\d\d')
    check = afterCheck.after.decode('UTF-8')
    if i==0:
        stnt = line.decode('UTF-8')
        stntNum = [float(s) for s in re.findall("\d+[.]\d\d", stnt)]
        beforeNum = [float(s) for s in re.findall("\d+[.]\d\d", expected[24])]
        afterNum = [float(s) for s in re.findall("\d+[.]\d\d", check)]

        # Now check for % difference
        fault = False
        for x in range(3):
            res = stntNum[x] - beforeNum[x]
            if beforeNum[x] == 0:
                beforeNum[x] = 0.001
            res = (res / beforeNum[x]) * 100
            if res > 1.0 and res < -1.0:
                fault = True
        
        for x in range(3):
            res = afterNum[x] - stntNum[x]
            if stntNum[x] == 0:
                stntNum[x] = 0.001
            res = (res / stntNum[x]) * 100
            if res > 1.0 and res < -1.0:
                fault = True
        
        if fault:
            errorMsg(bcolors, 3, line, expected[24])
        else:
            okMsg(bcolors, line, True)
    elif i==1:
        errorMsg(bcolors, 0, line, expected[24])

    assert (filename[-3:] == ".sh"), "Only files ending in .sh can be used in this program!"
    call(["rm", file[:-3] + ".txt"])

    return

##################################################################
# This function opens and runs the Sample shell script to get a baseline output
# to compare the students script with.
##################################################################
def getExpected(bcolors):
    try:
        exp = pexpect.spawn(SAMPLE_CODE)
    except:
        print(bcolors.FAIL + "Sample file not found. Please double check the global variable in\n\
the beginning of this code to make sure it contains a valid file." + bcolors.ENDC)
        exit(2)

    exp.expect('What is the CPU type and model\?')
    a = exp.after
    exp.expect('[^\r\n]+') # Yay regex!
    b = exp.after

    result = [a, b[4:]]

    exp.expect('How many processors on this system\?')
    result.append(exp.after)
    exp.expect('[^\r\n]+')
    result.append(exp.after[4:])

    exp.expect('What version of the Linux kernel is being used\?')
    result.append(exp.after)
    exp.expect('[^\r\n]+')
    result.append(exp.after[4:])

    exp.expect('How long has it been since the system was last booted\?')
    result.append(exp.after)
    exp.expect('up \d+ day[s]?, \s?\d+[:]\d\d')
    result.append(exp.after)

    exp.expect('How much CPU execution time has been spent in user, system and idle modes\?')
    result.append(exp.after)
    exp.expect('USER: \d+[.]\d\d seconds')
    result.append(exp.after)
    exp.expect('SYSTEM: \d+[.]\d\d seconds')
    result.append(exp.after)
    exp.expect('IDLE: \d+[.]\d\d seconds')
    result.append(exp.after)

    exp.expect('How much memory is on the machine\?')
    result.append(exp.after)
    exp.expect('MemTotal:        \d+ kB')
    result.append(exp.after)

    exp.expect('How much memory is currently available\?')
    result.append(exp.after)
    exp.expect('MemFree:         \s?\d+ kB')
    result.append(exp.after)

    exp.expect('How many kBytes have been read and written to the disk since the last reboot\?')
    result.append(exp.after)
    exp.expect('Read: \d+ kB')
    result.append(exp.after)
    exp.expect('Written: \d+ kB')
    result.append(exp.after)

    exp.expect('How many processes have been created since the last reboot\?')
    result.append(exp.after)
    exp.expect('Processes created: \d+')
    result.append(exp.after)

    exp.expect('How many context switches have been performed since the last reboot\?')
    result.append(exp.after)
    exp.expect('Context switches: \d+')
    result.append(exp.after)

    exp.expect('What is the current load average for the last 1, 5 and 15 minutes\?')
    result.append(exp.after)
    exp.expect('Load average: \d[.]\d\d, \d[.]\d\d, \d[.]\d\d')
    result.append(exp.after)

    return result

##################################################################
# Main - Take arguments from the command line, given they are provided.
##################################################################
def main(argv):
    bcolors = colors()
    try:
        filenames = [argv[0]]
    # If the user fails to provide a file, the program will now search in the user's current
    # working directory and find all the files that end in .sh
    except IndexError:
        filenames = [f for f in listdir("./") if isfile(join("./", f))]
        for i in xrange(len(filenames) - 1, -1, -1):
            if filenames[i][-3:] != '.sh':
                del filenames[i]

    if filenames[0] == '-h':
        print("\tUSAGE:\n\t$ python labLinuxInfoVerify.py\n\t- Runs the program, checking all \
files that end in .sh in your current directory.\n\n\t$ python labLinuxInfoVerify.py <FILENAME>\n\t\
- Runs the program, checking only the specified .sh file.\n\n\t$ python labLinuxInfoVerify.py -h\
\n\t- Displays this help screen.\n\n\t$ python labLinuxInfoVerify.py <FILENAME> -c\n\t$ python\
 labLinuxInfoVerify.py -c\n\t- Removes the colors from the output. The flag must be put after the\
 file name.\n\n\t- To pipe the output to a text file, use the -c flag, and put > results.txt at the\
 end of the command.\n\n\t- If labLinuxInfoVerify.py is not in your working directory,\n\
\tyou can find it at /home/cs345/labLinuxInfo/labLinuxInfoVerify.py\n")
        exit(0)

    # Colors flag
    if filenames[0] == '-c':
        bcolors = nocolors()
        filenames = [f for f in listdir("./") if isfile(join("./", f))]
        for i in xrange(len(filenames) - 1, -1, -1):
            if filenames[i][-3:] != '.sh':
                del filenames[i]

    try:
        color = argv[1]
        if color == '-c':
            bcolors = nocolors()
    except IndexError:
        pass

    # Open and read in the expected output file
    expected = getExpected(bcolors)

    # Adding escape characters to the list of expected.
    # For whatever reason--probably because pexpect supports regex--when the characters
    # '?', '(', and ')' are found in an expected string, pexpect freaks out. To fix this, 
    # an escape character, '\', is required in front of these characters.
    for e in range(len(expected)):
        expected[e] = expected[e].decode('UTF-8')
        f = 0
        while f < len(expected[e]):
            if expected[e][f] in ('?', '(', ')'):
                expected[e] = expected[e][:f] + "\\" + expected[e][f:]
                f += 1
            f += 1
        if e in (1, 3, 5, 7, 9, 10, 11, 13, 15, 17, 18, 20, 22, 24):
            expected[e] = "    " + expected[e][0:]
    # I miss curly brackets and semicolons.

    for filename in filenames:
        print(bcolors.HEADER + "========================================================" + bcolors.ENDC)
        print("Comparing %s with expected output..." % filename)
        print(bcolors.HEADER + "========================================================\n" + bcolors.ENDC)
        compare(filename, expected, bcolors)

    print("\nEnd of program")

if __name__ == "__main__":
    main(sys.argv[1:])
