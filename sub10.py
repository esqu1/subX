import requests, zipfile, StringIO, os

sub7, sub8, sub9, sub10 = {}, {}, {}, {}


def log_time(time, name):
    if int(time) not in [0, -1, -2]:
        if int(time) < 700:
            sub7.setdefault(name, [0, 1000])
            sub7[name][0] += 1
            if int(time) < sub7[name][1]:
                sub7[name][1] = int(time)
        if int(time) < 800:
            sub8.setdefault(name, [0,1000])
            sub8[name][0] += 1
            if int(time) < sub8[name][1]:
                sub8[name][1] = int(time)
        if int(time) < 900:
            sub9.setdefault(name, [0,1000])
            sub9[name][0] += 1
            if int(time) < sub9[name][1]:
                sub9[name][1] = int(time)
        if int(time) < 1000:
            sub10.setdefault(name, [0,1000])
            sub10[name][0] += 1
            if int(time) < sub10[name][1]:
                sub10[name][1] = int(time)


def string_rank(d):
    s = sorted(sorted(d.items(), key=lambda x: x[1][1]), key=lambda x: -x[1][0])
    final_string = ""
    for i, t in enumerate(s):
        final_string += str(i + 1) + "\t" + t[0] + "\t" + str(t[1][0]) + "\n"
    return final_string


def main():
    l = "https://www.worldcubeassociation.org/results/misc/WCA_export.tsv.zip"
    r = requests.get(l)
    r = zipfile.ZipFile(StringIO.StringIO(r.content))
    r.extractall("database")
    f = open("database/WCA_export_Results.tsv", 'r')
    s = f.read().split("\n")
    f.close()

    database = [x.split("\t") for x in s][:-1]

    sq1_database = [i for i in database if i[1] == "sq1"]

    for result in sq1_database:
        name = result[6]
        for i in xrange(10, 15):
            log_time(result[i], name)


main()

FINAL = "======================== SUB-7 ========================\n\n" + string_rank(sub7)
FINAL += "\n\n======================== SUB-8 ========================\n\n" + string_rank(sub8)
FINAL += "\n\n======================== SUB-9 ========================\n\n" + string_rank(sub9)
FINAL += "\n\n======================== SUB-10 ========================\n\n" + string_rank(sub10)

g = open("sq1sub10.txt",'w')
g.write(FINAL)
g.close()