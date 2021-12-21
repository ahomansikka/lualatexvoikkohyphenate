Lualatexvoikkohyphenate tarkistaa LuaLaTeXin tavutuksen.

Lualatexvoikkohyphenate on vapaa ohjelma, jota voidaan levittää ja
muuttaa GNU General Public License'n versiolla 3 tai uudemmalla.


Käyttö
======

LaTeX tavuttaa väärin etenkin yhdyssanoja (esimerkiksi nime-nomaan),
voikkohyphenate tekee paljon parempaa työtä (ni-men-o-maan).

Koska LaTeXin tavutus perustuu tavutuskaavoihin, sitä ei voi korvata
suoraan voikkohyphenate-ohjelmalla. Siksi olen tehnyt python3:lla
ohjelman, joka tarkistaa LaTeXin tavutuksen. Valitettavasti se toimii
vain LuaLaTeXissa.

Ohjelma käyttää LuaLaTeXin lua-check-hyphen -pakettia. Se on
ainakin TeXLivessä. Katso tiedosto luacheckhyphenmanual.pdf.

Kun LaTeX-tiedostoon nimi.tex lisää rivin

`\usepackage{lua-check-hyphen}`

lualatex kirjoittaa tiedoston nimi.uhy, jossa ovat kaikki LuaLaTeXin
tavuttamat sanat.

Komento

`./lualatexvoikkohyphenate.py nimi.uhy`

lukee tiedoston nimi.uhy, tavuttaa sanat voikkohyphenate-ohjelmalla
(tai siis vastaavalla python3-funktiolla) ja tulostaa ne sanat, jotka
voikkohyphenate on tavuttanut eri tavalla, jolloin LuaLaTeXin tavutus
on luultavasti väärin.


Copyright (©) 2021 Hannu Väisänen

Lualatexvoikkohyphenate checks LuaLaTeX hyphenation (for texts written in
Finnish).

Lualatexvoikkohyphenate is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.
