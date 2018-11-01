# !/usr/bin/env python3
import subprocess
import csv

def strip_cmd_injection(instr):
    inj = [";", "|", "&", "`", "(", ")", "$", "<", ">", "*", "?", "{", "}", "[", "]", "!", "\n"]
    for s in inj:
        instr = instr.replace(s, "")
    return instr


def doChasen(arg):
    cmd = " echo " + arg + " | chasen -iw "
    proc = subprocess.Popen(
        cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if stderr != b'':
        raise (Exception(stderr.decode("utf-8")))

    title = [['キーワード', '原形', '品詞']]
    top_list = []

    for line in stdout.decode('utf-8').split("\n"):
        if (line == "EOS"):
            break
        strList = line.split("\t")
        top_list.append([strList[0], strList[2], strList[3]])
    with open(r'/opt/ChaSen.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(title)
        writer.writerows(top_list)


if __name__ == '__main__':
    text = '独自ブランドであるカジュアルブランドのユニクロを創り上げ、急成⻑を遂げました'
    doChasen(text)
