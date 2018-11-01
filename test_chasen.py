#!/usr/bin/env python3
import subprocess

def strip_cmd_injection(instr):
    inj = [";", "|", "&", "`", "(", ")", "$", "<", ">", "*", "?", "{", "}", "[", "]", "!", "\n"]
    for s in inj:
        instr = instr.replace(s,"")
    return instr

def chasen(arg):
    arg = strip_cmd_injection(arg)
    cmd = "echo {0} | chasen -iw".format(arg)
    proc = subprocess.Popen(
        cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if stderr != b'':
        raise(Exception(stderr.decode("utf-8")))

    for line in stdout.decode('utf-8').split("\n"):
        if (line == "EOS"):
            break
        yield line.split("\t")

if __name__ == '__main__':
    import sys
    for line in sys.stdin:
        for cha in chasen(line):
            print (cha)

            
#echo "これはてすとです。" | python3 test_chasen.py
#['これ', 'コレ', 'これ', '名詞-代名詞-一般', '', '']
#['はて', 'ハテ', 'はて', '副詞-一般', '', '']
#['す', 'ス', 'す', '名詞-一般', '', '']
#['と', 'ト', 'と', '助詞-格助詞-一般', '', '']
#['で', 'デ', 'で', '助詞-格助詞-一般', '', '']
#['す', 'ス', 'する', '動詞-自立', 'サ変・スル', '文語基本形']
#['。', '。', '。', '記号-句点', '', '']
