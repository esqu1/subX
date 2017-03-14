import requests, zipfile, StringIO
import os, sys

# args: event name, X

def log_time(time, name, sub):
    '''
    Logs a given time into the sub-X list if the time is sub-X.
    '''
    if int(time) not in [0, -1, -2] and int(time) < int(sys.argv[2])*100:
        sub.setdefault(name, [0, 1000])
        sub[name][0] += 1
        if int(time) < sub[name][1]:
            sub[name][1] = int(time)

def string_rank(d):
    '''
    Returns a string containing the rankings of people that are sub-X.
    Takes in a dictionary of competitors with their name as the key
    and their # of sub-X's and best single as the value.
    '''
    s = sorted(sorted(d.items(), key=lambda x: x[1][1]), key=lambda x: -x[1][0])
    final_string = ""
    for i, t in enumerate(s):
        final_string += str(i + 1) + "\t" + t[0] + "\t" + str(t[1][0]) + "\n"
    return final_string


def main():
    try:
        l = "https://www.worldcubeassociation.org/results/misc/WCA_export.tsv.zip"
        print "Fetching database..."
        r = requests.get(l)
        r = zipfile.ZipFile(StringIO.StringIO(r.content))
        r.extractall("database")
    except requests.exceptions.ConnectionError:
        print "No connection detected. Using existing local database."
    f = open("database/WCA_export_Results.tsv", 'r')
    s = f.read().split("\n")
    f.close()

    database = [x.split("\t") for x in s][:-1]

    event_database = [i for i in database if i[1] == sys.argv[1]]

    sub = {}
    for result in event_database:
        name = result[6]
        for i in xrange(10, 15):
            log_time(result[i], name, sub)
    return sub

FINAL = "======================== SUB-%s ========================\n\n" % (sys.argv[2]) + string_rank(main())

g = open("sub.txt",'w')
g.write(FINAL)
g.close()

print "Done. List is in sub.txt."