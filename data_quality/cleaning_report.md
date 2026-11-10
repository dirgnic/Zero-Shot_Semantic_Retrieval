# Cleaning report: ZurichNLP/quotidiana (1997_2008)

- Documents in: **145,701**
- Kept (strict): **145,222** (99.67%)
- Kept (lenient): **145,226** (99.67%)
- Characters: 191,190,304 -> 191,101,098 (-0.05%)
- Whitespace tokens: 31,310,447 -> 31,277,262 (-0.11%)

## Stage 1 — repair rules (documents changed)

| rule | docs changed | share |
| --- | ---: | ---: |
| `decode_html_entities` | 1 | 0.00% |
| `strip_html_tags` | 0 | 0.00% |
| `nfc_normalize` | 5 | 0.00% |
| `strip_control` | 0 | 0.00% |
| `strip_soft_hyphen` | 23 | 0.02% |
| `expand_ligatures` | 37 | 0.03% |
| `normalize_quotes` | 141,533 | 97.14% |
| `normalize_dashes` | 34,224 | 23.49% |
| `strip_dot_leaders` | 1,111 | 0.76% |
| `strip_underscore_rules` | 1 | 0.00% |
| `strip_layout_glyphs` | 30,511 | 20.94% |
| `collapse_repeated_punct` | 284 | 0.19% |
| `join_wrap_hyphens` | 1,353 | 0.93% |
| `collapse_whitespace` | 31,130 | 21.37% |

## Stage 2/3 — quality flags (documents flagged)

| flag | docs | share |
| --- | ---: | ---: |
| `edited_reprint` | 350 | 0.24% |
| `garbled_extraction` | 58 | 0.04% |
| `fragmented_tokens` | 51 | 0.04% |
| `near_duplicate` | 41 | 0.03% |
| `too_short` | 28 | 0.02% |
| `too_long` | 4 | 0.00% |
| `empty` | 3 | 0.00% |

## Thresholds

```
{
  "min_tokens": 10,
  "max_tokens": 2500,
  "min_letter_ratio": 0.55,
  "max_digit_ratio": 0.3,
  "min_mean_token_len": 2.0,
  "max_ocr_suspicious": 0.1,
  "min_reprint_jaccard": 0.8,
  "max_single_letter_ratio": 0.25,
  "lid_doc_min_score": 0.9,
  "lid_zxx_min_score": 0.5,
  "lid_seg_min_tokens": 6,
  "lid_seg_max_tokens": 40,
  "lid_seg_min_score": 0.7,
  "lid_min_foreign_tokens": 10
}
```

## Markup (HTML)

- Documents with HTML entities decoded: **1**
- Documents with real HTML tags stripped: **0**
- Documents with angle-bracketed text **kept** (not HTML): **6**

| kept as text | occurrences |
| --- | ---: |
| `<Strom>` | 4 |
| `<Immortal>` | 1 |
| `<energia>` | 1 |
| `<http://www.drg.ch>` | 1 |
| `<http://www. fetters-sursetters.ch>` | 1 |
| `<vocabulari.surmiran@rumantsch.ch>` | 1 |
| `<rapportascha per la gasetta>` | 1 |

## OCR damage score

Share of word tokens per document matching a garbling pattern. Flag `ocr_damaged` above 10% (documents with >= 10 tokens).

| statistic | value |
| --- | ---: |
| mean | 0.01% |
| median | 0.00% |
| 90th percentile | 0.00% |
| 99th percentile | 0.00% |
| max | 7.03% |
| docs with >= 1 suspicious token | 1,322 |

| pattern | docs with >= 1 match |
| --- | ---: |
| `digit_in_word` | 125 |
| `symbol_in_word` | 155 |
| `letter_stutter` | 1,017 |
| `no_vowel` | 42 |

## Edited reprints (MinHash)

- 5-word shingles, 128 permutations, LSH 16 bands x 8 rows, threshold Jaccard >= 0.8
- Clusters with an edited reprint: **313**
- Documents flagged `edited_reprint`: **350** (excludes docs already flagged `near_duplicate`)

**estimated Jaccard 0.99**
- kept:    `Igl Teater Grischun Coira festivescha igl 20avel onn d'existenza. La producziun da giubileum "Jürg Jenatsch" da Rudolf Joho ò premiera sonda, igls 20 da mars 2004, allas 20.30 an sala da gimnastica a Lantsch. Anc 365 onn`
- flagged: `(cap/pi) Igl Teater Grischun Coira festivescha igl 20avel onn d'existenza. La producziun da giubileum "Jürg Jenatsch" da Rudolf Joho ò premiera sonda, igls 20 da mars 2004, allas 20.30 an sala da gimnastica a Lantsch. An`

**estimated Jaccard 0.86**
- kept:    `Raduond 250 töffists s'han inscuntrats a Scuol pel seguond inscunter da töfs internaziunal dal Club da töfs d'Engiadina Bassa. Els sun rivats da tuot las varts da la Svizra, da l'Italia dal nord da l'Austria e blers eir `
- flagged: `Raduond 250 töffists s'han inscuntrats a Scuol pel seguond inscunter da töfs internaziunal dal Club da töfs d'Engiadina Bassa. Els sun rivats da tuot las varts da la Svizra, da l'Italia dal nord da l'Austria e blers eir `

**estimated Jaccard 0.78**
- kept:    `La pagina dallas "opiniuns" ei ina plattaforma d'opiniuns per lecturas e lecturs davart temas d'interess general. Pli cuorta che l'opiniun ei e pli gronda che la schanza ei ch'ella vegni era publicada. Contribuziuns anon`
- flagged: `La pagina dallas "opiniuns" ei ina plattafuorma d'opiniuns per lecturas e lecturs davart temas d'interess general. Pli cuorta che l'opiniun ei e pli gronda che la schanza ei ch'ella vegni era publicada. Contribuziuns ano`

**estimated Jaccard 0.84**
- kept:    `Pel giuven club da nodar in Engiadina Bassa, il Club da nodar da Scuol (CDNS) es quai üna gronda onur ed ün grond plaschair da pudair organisar quist on las maestranzas da nodar avertas grischunas, chi vegnan manadas tra`
- flagged: `Pel giuven club da nodar in Engiadina Bassa, il Club da nodar da Scuol (CDNS) es quai üna gronda onur ed ün grond plaschair da pudair organisar quist on las Maestranzas da nodar avertas grischunas, chi vegnan manadas tra`

## Language identification (GlotLID)

Not run (no `--lid-model`).

## Metadata checks

- Columns checked: variety, pub_date, post_id, file_name
- Unique post_ids: 145,701
- Expected years: 1997-2008

| issue | docs |
| --- | ---: |
| (none) | 0 |

### Documents per variety and year

| variety | 1997 | 1998 | 1999 | 2000 | 2001 | 2002 | 2003 | 2004 | 2005 | 2006 | 2007 | 2008 | total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `rm-puter` | 135 | 323 | 847 | 704 | 645 | 553 | 336 | 439 | 387 | 350 | 312 | 306 | 5,337 |
| `rm-rumgr` | 281 | 1,762 | 2,366 | 2,616 | 2,476 | 2,718 | 2,541 | 2,960 | 2,654 | 2,984 | 3,177 | 3,344 | 29,879 |
| `rm-surmiran` | 228 | 781 | 754 | 881 | 1,061 | 1,107 | 844 | 916 | 792 | 1,069 | 1,142 | 1,178 | 10,753 |
| `rm-sursilv` | 1,961 | 5,676 | 5,363 | 5,328 | 5,680 | 5,134 | 6,110 | 6,054 | 6,422 | 6,673 | 6,740 | 6,058 | 67,199 |
| `rm-sutsilv` | 168 | 667 | 666 | 623 | 408 | 393 | 337 | 415 | 457 | 315 | 287 | 272 | 5,008 |
| `rm-vallader` | 1,150 | 3,504 | 3,205 | 3,199 | 2,316 | 2,333 | 2,141 | 1,939 | 1,897 | 1,703 | 1,956 | 2,182 | 27,525 |

## Largest recurring formats (kept, not flagged)

Documents sharing their first or last 6 normalized tokens. Members share a format but little text (median 5-gram Jaccard ~0.01 in family_check.py), so the column `recurring_format` is information for downstream use, not a filter.

| documents | edge signature |
| ---: | --- |
| 243 | `HEAD: situaziun generala ina zona da pressiun` |
| 96 | `HEAD: situaziun generala la zona da pressiun` |
| 72 | `TAIL: lavur lieu da lavur termin dannunzia` |
| 40 | `HEAD: la davosa fin d jamna ha` |
| 38 | `HEAD: in special engraziament admettein nus a` |
| 34 | `HEAD: la fin d eivna passada ha` |
| 33 | `HEAD: in grond dieus paghi admettein nus` |
| 31 | `HEAD: la davosa fin d jamna han` |
| 30 | `HEAD: la partida cristiandemocratica pcd dal grischun` |
| 28 | `HEAD: in occasiun da la tschanteda dals` |
| 27 | `HEAD: il cussagl cumünal da scuol ha` |
| 26 | `HEAD: la fracziun da la partida cristiandemocratica` |

## What each repair rule changed (sampled)

### `normalize_quotes`

- **before:** `Sco tuot las structuras turisticas es eir l’organisaziun da tet grischuna pel mumaint landervia dad elavurar ün concept nouv chi definescha sias lezchas e sia rolla aint illa structura turistica in Chantun. Il concept, c`
  **after:**  `Sco tuot las structuras turisticas es eir l'organisaziun da tet grischuna pel mumaint landervia dad elavurar ün concept nouv chi definescha sias lezchas e sia rolla aint illa structura turistica in Chantun. Il concept, c`
- **before:** `La musicanta, Heidi König da Dresden, es attachada cun grond’amur a l’Engiadina. Our da quel motiv vegn il public engiadinais adüna darcheu i’l giodimaint da differentas producziuns da la paletta variada da musica, cha l`
  **after:**  `La musicanta, Heidi König da Dresden, es attachada cun grond'amur a l'Engiadina. Our da quel motiv vegn il public engiadinais adüna darcheu i'l giodimaint da differentas producziuns da la paletta variada da musica, cha l`
- **before:** `Es il contrat d’ingaschamaint lura suottascrit, cumainzan fingià ils preparativs pel prüm on da scoula. Las aspettativas creschan, ma eir l’intschertezza e l’agitaziun. Ursina Pinggera ha intant fat sias prümas experienz`
  **after:**  `Es il contrat d'ingaschamaint lura suottascrit, cumainzan fingià ils preparativs pel prüm on da scoula. Las aspettativas creschan, ma eir l'intschertezza e l'agitaziun. Ursina Pinggera ha intant fat sias prümas experienz`
- **before:** `La radunanza cumünala da mardi saira da Samignun nun es statta pronta da far üna votumaziun consultativa per dar la directiva per ün dals progets per ün concept da trafic e structuraziun dal territori public illas fraczi`
  **after:**  `La radunanza cumünala da mardi saira da Samignun nun es statta pronta da far üna votumaziun consultativa per dar la directiva per ün dals progets per ün concept da trafic e structuraziun dal territori public illas fraczi`

### `join_wrap_hyphens`

- **before:** `La fin d’eivna passada ha gnü lö i’l Signuradi a Malans la radunanza da delegats da l’Associaziun da musica chantunala dal Grischun (AMG). L’associaziun quinta hoz ün nomer da commembers da passa 100 societats da musica `
  **after:**  `La fin d'eivna passada ha gnü lö i'l Signuradi a Malans la radunanza da delegats da l'Associaziun da musica chantunala dal Grischun (AMG). L'associaziun quinta hoz ün nomer da commembers da passa 100 societats da musica `
- **before:** `La sfüfla ordinaria, la previsiun da l’ora, la nota diplomatica, la comunicaziun ufficiala e la statistica. Pensand inavo als ultims ans, ans vegn adimmaint ils kils da palperi cha tuotta sorts uniuns (hoz plütost clamad`
  **after:**  `La sfüfla ordinaria, la previsiun da l'ora, la nota diplomatica, la comunicaziun ufficiala e la statistica. Pensand inavo als ultims ans, ans vegn adimmaint ils kils da palperi cha tuotta sorts uniuns (hoz plütost clamad`
- **before:** `Tschiervi marcà dürant il temp da chalur illa Val Trupchun. Quista bes-cha han tschüf ils guardians da sulva- Ingün god sulvadi, però tuottüna ün god fich natüral illa Val dal Spöl. Il PNS ans muossa co cha la natüra fun`
  **after:**  `Tschiervi marcà dürant il temp da chalur illa Val Trupchun. Quista bes-cha han tschüf ils guardians da sulva- Ingün god sulvadi, però tuottüna ün god fich natüral illa Val dal Spöl. Il PNS ans muossa co cha la natüra fun`
- **before:** `E lura es gnü Markus landervia. Schi, ch’el haja durmi bain la not avant, ha’l respus a la prüma dumonda. «Eu nu d’eira nervus.» – Gnanca zich? «Na», ha el respus cun tun franc. Che ch’els hajan imprais la prüm’eivna e m`
  **after:**  `E lura es gnü Markus landervia. Schi, ch'el haja durmi bain la not avant, ha'l respus a la prüma dumonda. "Eu nu d'eira nervus." - Gnanca zich? "Na", ha el respus cun tun franc. Che ch'els hajan imprais la prüm'eivna e m`

### `normalize_dashes`

- **before:** `A Gluorn ha lö quists dis la seguonda «Vinschgauer Leistungsschau», üna exposiziun regiunala da commerzi e mansteranza. Alch special vi da quella exposiziun es il fat cha quella es gnüda coorganisada dal proget european `
  **after:**  `A Gluorn ha lö quists dis la seguonda "Vinschgauer Leistungsschau", üna exposiziun regiunala da commerzi e mansteranza. Alch special vi da quella exposiziun es il fat cha quella es gnüda coorganisada dal proget european `
- **before:** `Fat ün film davart il forum pels giuvenils da l’Europa Las partecipantas e’ls partecipants dal lavuratori «ir suot aua – la schanza da l’aua» als Bogns curativs a San Murezzan han erui las differentas fuormas da l’aua e `
  **after:**  `Fat ün film davart il forum pels giuvenils da l'Europa Las partecipantas e'ls partecipants dal lavuratori "ir suot aua - la schanza da l'aua" als Bogns curativs a San Murezzan han erui las differentas fuormas da l'aua e `
- **before:** `Dürant il mais da settember han lö las quatter sairadas da las raspadas Ftan ed Ardez ingiò chi vegnan trattadas dumandas davart la Bibla respectivmaing davart la Bibla in relaziun cun psicologia e scienza natürala. A la`
  **after:**  `Dürant il mais da settember han lö las quatter sairadas da las raspadas Ftan ed Ardez ingiò chi vegnan trattadas dumandas davart la Bibla respectivmaing davart la Bibla in relaziun cun psicologia e scienza natürala. A la`
- **before:** `Illa cuortsuot da la chasa Furger a Guarda sun amo fin in october expostas fotografias cha’l fotograf Ernst Brunner ha fat tanter ils ans 1938 e 1940. I’s tratta da documaints impreschiunants dad ün temp oramai svani chi`
  **after:**  `Illa cuortsuot da la chasa Furger a Guarda sun amo fin in october expostas fotografias cha'l fotograf Ernst Brunner ha fat tanter ils ans 1938 e 1940. I's tratta da documaints impreschiunants dad ün temp oramai svani chi`

### `strip_dot_leaders`

- **before:** `PREIR La pumpa es be ün simbol per la grondeza da la Baselgia. Eir aint il ornat, il sacerdot es nüd e pchader sco eu e tü. La baselgia es üna buna cluotscha davant Dieu; ella protegia a seis pulschins. PLAVAN ... güstif`
  **after:**  `PREIR La pumpa es be ün simbol per la grondeza da la Baselgia. Eir aint il ornat, il sacerdot es nüd e pchader sco eu e tü. La baselgia es üna buna cluotscha davant Dieu; ella protegia a seis pulschins. PLAVAN güstifiche`
- **before:** `Cuntinuaziun dal numer 11 Ils predschs croudan di per di. Marchandants, cromers e barattaders da Varese, dal milanais as fan pro e cumpran insembel tuot quai chi pon schgnaffar, cumpran fin cha l’ögl tendscha e charrasà `
  **after:**  `Cuntinuaziun dal numer 11 Ils predschs croudan di per di. Marchandants, cromers e barattaders da Varese, dal milanais as fan pro e cumpran insembel tuot quai chi pon schgnaffar, cumpran fin cha l'ögl tendscha e charrasà `
- **before:** `I dà umans chi nun han ün access normal al pled. Per els restan na be ils cudeschs – sco cha rav. Alistair Murray s’ha express – serrats, ma els restan exclus da bleras «cuntradas» dal muond e da la vita. Suot il titul «`
  **after:**  `I dà umans chi nun han ün access normal al pled. Per els restan na be ils cudeschs - sco cha rav. Alistair Murray s'ha express - serrats, ma els restan exclus da bleras "cuntradas" dal muond e da la vita. Suot il titul "`
- **before:** `Sco terz referent in ün ciclus da referats s’ha occupà Arno Arquint dal «Respet invers la vita». El s’ha avischinà dal tema in congualand il pensar dal budissem, dal cristianissem e dals Indians da Dakota. Intant chi’d e`
  **after:**  `Sco terz referent in ün ciclus da referats s'ha occupà Arno Arquint dal "Respet invers la vita". El s'ha avischinà dal tema in congualand il pensar dal budissem, dal cristianissem e dals Indians da Dakota. Intant chi'd e`

### `collapse_whitespace`

- **before:** `LQ «Giuventüna sainza drogas», e tuot tschels eir, es ün postuvoul güdar a schoglier quist problem. Il parlamaint ha refüsà il lat chi s’inclegia insè da sai. text e voul cuntinuar cun las Ingio es però il cunfin tanter `
  **after:**  `LQ "Giuventüna sainza drogas", e tuot tschels eir, es ün postuvoul güdar a schoglier quist problem. Il parlamaint ha refüsà il lat chi s'inclegia insè da sai. text e voul cuntinuar cun las Ingio es però il cunfin tanter `
- **before:** `Puonch quatter Stadi actual: nus vain gnü üna stà bletscha; id ha plovü da gröss in mai, in gün; la terra ha trat aint quai ch’ella pudaiva. Vus faivat surasèn da quai vi dals flüms chi cuorran ots e vi dals auals chi sg`
  **after:**  `Puonch quatter Stadi actual: nus vain gnü üna stà bletscha; id ha plovü da gröss in mai, in gün; la terra ha trat aint quai ch'ella pudaiva. Vus faivat surasèn da quai vi dals flüms chi cuorran ots e vi dals auals chi sg`
- **before:** `Quista uniun, fundada ils 26 d’october 1977 da dudesch amatuors dal rumantsch, pudet festagiar seis 20avel cumplean als 24/25 d’october l’an scuors in ün ram plü grand e plü commemorativ. Trais arrandschamaints dan perdü`
  **after:**  `Quista uniun, fundada ils 26 d'october 1977 da dudesch amatuors dal rumantsch, pudet festagiar seis 20avel cumplean als 24/25 d'october l'an scuors in ün ram plü grand e plü commemorativ. Trais arrandschamaints dan perdü`
- **before:** `Dal rest: Chi chi dumonda ingio cha seis raps van ch’el affida a las ouvras d’agüd manzunadas, sto far quista dumonda eir in oters reguards. Ün exaimpel: Ultimamaing sun gnüdas comunichadas in ün’emischiun da la televisi`
  **after:**  `Dal rest: Chi chi dumonda ingio cha seis raps van ch'el affida a las ouvras d'agüd manzunadas, sto far quista dumonda eir in oters reguards. Ün exaimpel: Ultimamaing sun gnüdas comunichadas in ün'emischiun da la televisi`

### `strip_soft_hyphen`

- **before:** `Ella reflecteschan savens in malesser cul stan actual e cun soluziuns cattadas sin plaun politic. Cu La victura Julia Tschepalova survain ün bütsch da gratulaziun dal victur, Gerhard Urain. KEYSTONE varga 100 000 burghei`
  **after:**  `Ella reflecteschan savens in malesser cul stan actual e cun soluziuns cattadas sin plaun politic. Cu La victura Julia Tschepalova survain ün bütsch da gratulaziun dal victur, Gerhard Urain. KEYSTONE varga 100 000 burghei`
- **before:** `Pertge ò l’uniun turistica angal reagea cun dar cunsegls e mademamaintg mai duvro en pled arisguard ena contribuziun da sia vart pigls costs dall’expertisa? Egoissem, vanaglorgia? Metter sot pressiun igls politichers e m`
  **after:**  `Pertge ò l'uniun turistica angal reagea cun dar cunsegls e mademamaintg mai duvro en pled arisguard ena contribuziun da sia vart pigls costs dall'expertisa? Egoissem, vanaglorgia? Metter sot pressiun igls politichers e m`
- **before:** `Ubain ch’in sa partecipescha sez documentand cun resultats pli u main buns sia atgna sportivitad, ubain ch’ins perseguitescha cun tschera d’expert il travasch sin e sper la pista, renconuschend per mintga commentari ch’i`
  **after:**  `Ubain ch'in sa partecipescha sez documentand cun resultats pli u main buns sia atgna sportivitad, ubain ch'ins perseguitescha cun tschera d'expert il travasch sin e sper la pista, renconuschend per mintga commentari ch'i`

### `collapse_repeated_punct`

- **before:** `I van a chasa dond dal cheu, sainza star insembel in gruppettas, sco pel solit davo radunanza, davo baselgia. Illas bleras chasas esa amo glüm. Las duonnas e’ls uffants spettan a gnir, cun buonder, cun pisser. *** Il di `
  **after:**  `I van a chasa dond dal cheu, sainza star insembel in gruppettas, sco pel solit davo radunanza, davo baselgia. Illas bleras chasas esa amo glüm. Las duonnas e'ls uffants spettan a gnir, cun buonder, cun pisser. * Il di da`
- **before:** `d. impegn d’almain d’üna part dals genituors, nempe da promouver pro l’uffantin da prüm davent la chöntschezza e da svagliar la simpatia invers l’armonia dal pled rumantsch udibel. *** Duos fats istorics am paran esser r`
  **after:**  `d. impegn d'almain d'üna part dals genituors, nempe da promouver pro l'uffantin da prüm davent la chöntschezza e da svagliar la simpatia invers l'armonia dal pled rumantsch udibel. * Duos fats istorics am paran esser rel`
- **before:** `L’imprender rg sco lingua «estra» – confuorm al model d’üna vaira lingua estra (frances, talian, inglais e.o.) – quetant nu güda bler per intant i’l territori rumantsch: Il scolar nu chattarà guera occasiuns da pratichar`
  **after:**  `L'imprender rg sco lingua "estra" - confuorm al model d'üna vaira lingua estra (frances, talian, inglais e.o.) - quetant nu güda bler per intant i'l territori rumantsch: Il scolar nu chattarà guera occasiuns da pratichar`
- **before:** `Quist appel sün la fatschada d’üna chasa engiadinaisa (adattà da mai svess a quai chi segua) pudess ans güdar inavant illa discussiun sur da la Tualetta rumantscha. Vè dimena nan sül banc da mia vantporta, fa la posa e t`
  **after:**  `Quist appel sün la fatschada d'üna chasa engiadinaisa (adattà da mai svess a quai chi segua) pudess ans güdar inavant illa discussiun sur da la Tualetta rumantscha. Vè dimena nan sül banc da mia vantporta, fa la posa e t`

### `strip_layout_glyphs`

- **before:** `■ (mj) Fingià dalönch al passà appartegna la 3. etappa da la Tour de Suisse chi ha manà la cuorsa venderdi fin in Engiadina Bassa. Brich fingià svapuri es il plaschair e l’algrezcha da Samignun da l’onur da pudair retsch`
  **after:**  `(mj) Fingià dalönch al passà appartegna la 3. etappa da la Tour de Suisse chi ha manà la cuorsa venderdi fin in Engiadina Bassa. Brich fingià svapuri es il plaschair e l'algrezcha da Samignun da l'onur da pudair retschai`
- **before:** `■ Avant duos mais ha cumanzà Fadri Juon da Brail sia lavur sco mainagestiun da la Società da trafic da Zernez. El, l’uschènomnada “boja da salvamaint”, s’ha büttà cun grond svung, cun elan e be entusiassem ill’aua fraida`
  **after:**  `Avant duos mais ha cumanzà Fadri Juon da Brail sia lavur sco mainagestiun da la Società da trafic da Zernez. El, l'uschènomnada "boja da salvamaint", s'ha büttà cun grond svung, cun elan e be entusiassem ill'aua fraida. `
- **before:** `■ (ms) Ün orgelin svizzer, ün cello, üna gïa, clarinettas e saxofons, flötas da lain e flötas a travers, keyboards e battaria – es quai pussibel cha vainch uffants e giuvenils cun uschè blers differents instrumaints fuor`
  **after:**  `(ms) Ün orgelin svizzer, ün cello, üna gïa, clarinettas e saxofons, flötas da lain e flötas a travers, keyboards e battaria - es quai pussibel cha vainch uffants e giuvenils cun uschè blers differents instrumaints fuorma`
- **before:** `■ (ht) D’avair accumpli las pretaisas per survgnir il diplom da manster voul dir d’avair fat ün pass inavant illa vita. Quai ha dit in gövgia davomezdi Stefan Eisenring, il manader da l’Uffizi chantunal per fuormaziun pr`
  **after:**  `(ht) D'avair accumpli las pretaisas per survgnir il diplom da manster voul dir d'avair fat ün pass inavant illa vita. Quai ha dit in gövgia davomezdi Stefan Eisenring, il manader da l'Uffizi chantunal per fuormaziun prof`

### `expand_ligatures`

- **before:** `Incumbenzas Caposecziun Sustegn general da la manadra dal servezzan d’abitants (servezzan da telefon e da fanestrigl, lavuors pel ufﬁzi da lavur, pell’SVA, etc.). Facturaziun da taxas da cura, taxas pella promoziun dal t`
  **after:**  `Incumbenzas Caposecziun Sustegn general da la manadra dal servezzan d'abitants (servezzan da telefon e da fanestrigl, lavuors pel uffizi da lavur, pell'SVA, etc.). Facturaziun da taxas da cura, taxas pella promoziun dal `
- **before:** `Nus purschin: – vendita da cameras digitalas da CANON, OLYMPUS, SONY, HP . . . – differentas cameras digitalas d‘emprova – accessori per tuttas cameras digitalas: Akkus, cartas da segirar datas, indrez da leger cartas di`
  **after:**  `Nus purschin: - vendita da cameras digitalas da CANON, OLYMPUS, SONY, HP . . . - differentas cameras digitalas d'emprova - accessori per tuttas cameras digitalas: Akkus, cartas da segirar datas, indrez da leger cartas di`
- **before:** `Sin igl 1. duost 2005 encurin nus in(a) emprendist(a) mercantil(a) Ti eis ina persuna ﬂexibla cun iniziativa, sas romontsch e tudestg a bucca ed a scret. Ti has bugen il contact persunal cun in publicum multifar e prefer`
  **after:**  `Sin igl 1. duost 2005 encurin nus in(a) emprendist(a) mercantil(a) Ti eis ina persuna flexibla cun iniziativa, sas romontsch e tudestg a bucca ed a scret. Ti has bugen il contact persunal cun in publicum multifar e prefe`
- **before:** `Purtai ina chapellina! Na, nagina tema – nus n’As faschain betg ir sin ina lingia al liber, mabain As prendain cun nus sin in viadi captivant tras il mund da la Rätia Energie. Il pli nov ﬁlm mussa impressiuns fascinantas`
  **after:**  `Purtai ina chapellina! Na, nagina tema - nus n'As faschain betg ir sin ina lingia al liber, mabain As prendain cun nus sin in viadi captivant tras il mund da la Rätia Energie. Il pli nov film mussa impressiuns fascinanta`

### `nfc_normalize`


### `decode_html_entities`


### `strip_underscore_rules`

- **before:** `Name: ___________________________________________________________________________________________________________________ __________________________________________________________ _______________________________________`
  **after:**  `Name: Vorname: Strasse, Nr.: PLZ, Ort:`


## What each filter flagged (sampled)

### `edited_reprint`

- `- intagliar lain e far intarsas cun sar Otto Gaudenz - cuschinar cun dna. Nicolina Marugg - cusir cun dna. Martina Parli - tesser cul taler da maisa cun dna. Matilda Pernisch - mosaïcs cul crötsch (schanfigger) cun dna. `
- `Raduond 250 töffists s'han inscuntrats a Scuol pel seguond inscunter da töfs internaziunal dal Club da töfs d'Engiadina Bassa. Els sun rivats da tuot las varts da la Svizra, da l'Italia dal nord da l'Austria e blers eir `
- `L'ultim da tuot ils chatschaders dad uors es mort sar Anton Pfister. El eira nat a Scuol l'an 1853 ed es mort a Samedan l'an 1950, vegl damaja bod sco Metusalem. Sco tut ils Pfisters è'l stat ün tregant non plus ultra. C`
- `Sar Anton nu stübgia ne üna ne duos. Fingià ha'l seis Vetterle a masella. I va üna giaischlada metallica suravia la val. La grippa survart respuonda cul schuschuri d'üna lavina chi's precipita giò tanter la zondra oura e`

### `near_duplicate`

- `Daspö als 1. avrigl 1995 sun ils districts respuonsabels per eleger las autoritats d'intermediaziun per dispitta sin fats da fittanza, quai chi reguarda las abitaziuns e'ls affars. Las directivas federalas da l'an 1990 s`
- `Il rendaquint ed il rapport annual da l'organisaziun regiunala da l'Engiadina Bassa es gnü scumparti quists dis. Ils cuosts da la Pro Engiadina Bassa (PEB) pel 1997, chi van i'l scumpart a charg dals cumüns, importan bun`
- `31 persunas han tut part a la radunanza cumünala da Tschlin da marcurdi saira. Quai sun nouv pertschient da la populaziun cun dret da vuschar. La radunanza ha approvà ün pêr müdamaints da la ledscha da fabrica ed aboli l`
- `Jachen Ulrich Gaudenz Il prüm inscunter ch'eu n'ha gnü cun quista veidra Bibla rumantscha es stat agià a Zernez, ch'eu d'eira uffant. Eu giaiva vi'l stüdi da bap, e là d'eira sün üna curuna ün cudeschun chi surpassaiva t`

### `garbled_extraction`

- `Eni ro d s s c n e t l m a e ocp eetrl p l c o a reschenta La Qu t o id a a q e t' m a l s p s z u s in us en a oiin d lscniaa edl cnias a a addts as addt d l c s e l n z u a e d m na usg ainl n ao dscnrlsd l pltc sir. a`
- `L L s h n Fi u i r a r a i c a a dzai S a Sul eit usa dsö A co xsa os ap va n h o s Qu i e s a p l i c n . a s tt es I cselg l u s g rond vegn era a discutar schebein ils mistrals san appartener era egl avegnir al parlam`
- `Co q i t i Vu m g i ra l s t au n e s s i l u r a iu zu dslt dla fnna f i n e o a a a l s i a z s ed ra a ? Nu s o ve n r s a e ls a t g i p rgnau e nua quinteis Vu s ve re a t a n s a r c l g r ova e t s n radas? Marco `
- `Hans-Peter P e s h Tavau lic, P rt d p p l r a ia ouaa sir vza I n praetso l ov a l m n t esr p n d d c s e ro t a e id r d va p s a e a rt u s iva msrs d ls eia a sag, tatr a p r n r n e ut r e i s c u d l re u re t d's`

### `fragmented_tokens`

- `Eni ro d s s c n e t l m a e ocp eetrl p l c o a reschenta La Qu t o id a a q e t' m a l s p s z u s in us en a oiin d lscniaa edl cnias a a addts as addt d l c s e l n z u a e d m na usg ainl n ao dscnrlsd l pltc sir. a`
- `L L s h n Fi u i r a r a i c a a dzai S a Sul eit usa dsö A co xsa os ap va n h o s Qu i e s a p l i c n . a s tt es I cselg l u s g rond vegn era a discutar schebein ils mistrals san appartener era egl avegnir al parlam`
- `Co q i t i Vu m g i ra l s t au n e s s i l u r a iu zu dslt dla fnna f i n e o a a a l s i a z s ed ra a ? Nu s o ve n r s a e ls a t g i p rgnau e nua quinteis Vu s ve re a t a n s a r c l g r ova e t s n radas? Marco `
- `Hans-Peter P e s h Tavau lic, P rt d p p l r a ia ouaa sir vza I n praetso l ov a l m n t esr p n d d c s e ro t a e id r d va p s a e a rt u s iva msrs d ls eia a sag, tatr a p r n r n e ut r e i s c u d l re u re t d's`

### `too_short`

- `Co as voula garantir la gestiun a lunga vista?`
- `Previu el baghetg niev ein:`
- `O, ils glimaris ein savens umeneris senza auter nuot.`
- `Num dil chor: predicat:`

### `too_long`

- `Gl'era eneda betg a cò ena famiglia da meirs. Els abitavan ainten ena tgesa viglia vigliurda betg schi gronda, seglple 1 m3 grond. La mamma Julia fo gist igl giantar. Igl bab Stefan, la feglia Atonia ed igl fegl Hopser t`
- `I scaligna, gl'è las diesch. Igls scolars digl scalem superiour bandungan las stanzas. Ainten igl pierta ins sainta discurs cun temas da mintga de. Kai, Yves, Jan, Nicole ed Eliane s'antopan segl plaz da possa. Els èn en`
- `(cc) Suenter avair prendì invista da las propostas da la gruppa da lavur departamentala sco er da las posiziuns entradas vegn la regenza a la suandanta conclusiun. Cun la decisiun dal cussegl grond d'edir a partir da l'o`
- `Schuders; Joos-Nay Manuela, Tamins; Jordi Bettina, Ilanz; Josche Michaela, Guarda; Jossi Anni, Winterthur; Jost Stefan, Sursee; Jost Stefan, Derendingen; Jost-Pedotti Ursina, Aschera; Josty Chatrina, Cuira; Jud Beatrice,`

### `empty`

- ``
- ``
- ``
