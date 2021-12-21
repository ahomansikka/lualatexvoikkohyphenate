#!/usr/bin/env python3

# Copyright (©) 2021 Hannu Väisänen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import argparse
import codecs
import libvoikko
import sys

parser = argparse.ArgumentParser (formatter_class=argparse.RawDescriptionHelpFormatter,
                                  add_help = False,
                                  description='''Tarkista LuaLaTeXin tavutus.''')
def read_config():
    parser.add_argument ('-h',     action = 'store_true', dest = 'help', help = 'Tulosta ohjeet ja lopeta.')
    parser.add_argument ('--help', action = 'store_true', dest = 'help', help = 'Tulosta ohjeet ja lopeta.')
    parser.add_argument ('-d',     nargs = 1, dest = 'dictionary', choices = ['fi', 'fi-x-sukija'], default = ['fi'],
                         help = 'fi = Voikon oikolukusanasto, fi-x-sukija = Sukijan indeksointisanasto.')
    parser.add_argument ('files', nargs=argparse.REMAINDER, help = 'Luettavat tiedostot (*.uhy).')
    return parser.parse_args();


# Kuinka monta merkkiä C on merkkijonossa S?
#
def count (s, c):
    n = 0
    for i in range(0,len(s)):
        if s[i] == c:
            n = n + 1
    return n


# Onko S vokaali?
#
def isvowel (s):
    return (s == "a") or (s == "e") or (s == "i") or (s == "o") or \
           (s == "u") or (s == "y") or (s == "ä") or (s == "ö")


# Poistetaan ta-vu-tus paitsi esimerkiksi linja-autosta.
#
def dehyphen (s):
    u = ""
    for i in range(0,len(s)):
        if s[i] != "-" or (s[i] == "-" and isvowel(s[i-1]) and s[i-1] == s[i+1]):
            u = u + s[i]
    return u


# LuaLaTeX ei aina tavuta sanoja kokonaan, mutta tarkistetaan,
# että tavutuskohdat ovat samat kuin voikkohyphenate'ssa.
#
# p = LuaLaTeXin tavutus.
# u = voikkohyphenate'n tavutus.
#
def xtest (p, u):
    a = p.split("-")
    b = u.split("-")
    c = []
    m = 0
    for i in range (0, count(p,'-')+1):
      v = ""
      for j in range (m, len(b)):
         v = "".join([v,b[j]])
         if v == a[i]:
             c.append(v)
             m = j + 1
             break
    if a != c:       # LuaLaTeXin ja Voikon tavutus on erilainen.
        print (p, u) #### , "|", a, c)


def parse_file (voikko, file):
    infile = codecs.open (file, "r", "UTF-8")
    while True:
        line = infile.readline()
        if line == "":
            break
        line = line[:-1]
        p = line.replace ("''", "") # Poistetaan lainausmerkit.
        q = voikko.hyphenate(p)     # Tavutetaan LuaLaTeXin osittain tavuttama sana.
        s = str(dehyphen(p))        # Poistetaan LuaLaTeXin tavutus.
        u = voikko.hyphenate(s)     # Tavutetaan sana Voikossa.
        if q != u:                  # Jos LuaLaTeXin ja Voikon tavutus voi olla erilainen...
            xtest (p, u)
    infile.close()


def main():
    c = read_config()
    if c.help:
        parser.print_help()
        exit (1)
    if c.files == []:
        print ("Ei tiedostoja.")
        exit(1)

    voikko = libvoikko.Voikko (c.dictionary[0])

    for i in range (0, len(c.files)):
        parse_file (voikko, c.files[i])
    voikko.terminate()


if __name__ == '__main__':
    main()
