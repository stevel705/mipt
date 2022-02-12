# Results 

Запускаем pyspark с --num-executors=5

Перед проведением экспериментов, проверим, что данные разбиты на достаточное число партиций и что среди них нет вырожденных (существенно меньших по объёму, чем прочие). 

Наши данные по умолчанию разбились на 2 партиции: 8038 и 7991 соответственно. Особенно не видно, чтобы одна из партиций была существенно больше, чем другая. 

Если же разбить на 5 партиций с помощью partitionBy(5), то получим разбиение: 3206, 3206, 3207, 3205, 3205. Будем использовать такое разбиение для проведение экспериментов.

Примечание: Время сильно зависит от загруженности кластера

## Без brodcast переменной

| num_topics | num_document_passes | num_collection_passes | time (sec) |
|------------|---------------------|-----------------------|------------|
| 10         | 5                   | 10                    |4559        |
| 20         | 5                   | 10                    |9360        |
| 50         | 5                   | 10                    |18573       |


## С brodcast переменной

| num_topics | num_document_passes | num_collection_passes | time (sec) |
|------------|---------------------|-----------------------|------------|
| 10         | 5                   | 10                    |3970        |
| 20         | 5                   | 10                    |8107        |
| 50         | 5                   | 10                    |18398       |


После проделанных экспериментов, мы можем сказать, что обучение с помощью brodcast переменной уменьшает скорость обучение на +-15%, при количестве тем 10 и 20. При количестве тем 50, скорость существенно не отличается. Хотя как было сказано выше, скорость очень сильно зависит от загруженности сервера. 


| num_topics | num_document_passes | num_collection_passes | time (sec) |
|------------|---------------------|-----------------------|------------|
| 20         | 1                   | 10                    |745         |
| 20         | 2                   | 10                    |1059        |
| 20         | 5                   | 10                    |2143        |
| 20         | 10                  | 10                    |3019        |


### num_document_passes = 1

| topic_id: 0 | topic_id: 1 | topic_id: 2 | topic_id: 3 | topic_id: 4 | topic_id: 5 | topic_id: 6 | topic_id: 7 | topic_id: 8 | topic_id: 9 | topic_id: 10 | topic_id: 11 | topic_id: 12 | topic_id: 13 | topic_id: 14 | topic_id: 15 | topic_id: 16 | topic_id: 17 | topic_id: 18 | topic_id: 19 |
|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|
| town        | river       | film        | park        | film        | film        | party       | game        | game        | king        | film         | film         | album        | club         | league       | film         | town         | film         | league       | film         |
| party       | district    | song        | army        | club        | party       | song        | club        | film        | system      | game         | church       | club         | game         | film         | league       | league       | road         | film         | church       |
| game        | system      | london      | album       | album       | river       | church      | development | league      | center      | league       | party        | party        | party        | town         | album        | song         | son          | party        | album        |
| union       | church      | party       | man         | record      | song        | town        | league      | party       | album       | father       | club         | town         | song         | art          | town         | system       | support      | town         | man          |
| king        | film        | album       | political   | king        | church      | building    | park        | road        | army        | station      | album        | road         | album        | song         | river        | station      | cup          | london       | record       |
| cup         | game        | king        | award       | radio       | game        | station     | william     | river       | league      | album        | london       | radio        | league       | road         | church       | band         | system       | park         | art          |
| station     | album       | road        | black       | station     | station     | road        | book        | album       | club        | children     | king         | art          | park         | game         | support      | film         | community    | station      | park         |
| club        | road        | building    | book        | works       | art         | right       | system      | band        | england     | party        | england      | law          | london       | son          | station      | man          | london       | man          | party        |
| art         | army        | support     | research    | next        | building    | river       | cup         | king        | women       | night        | women        | research     | community    | center       | law          | church       | king         | president    | community    |
| band        | version     | community   | street      | party       | education   | full        | next        | club        | games       | show         | power        | form         | version      | park         | german       | said         | building     | game         | works        |

Значение преплексии на каждом проходе:

[2.0031400293603694, 11590.876243136421, 11589.343341274445, 11589.343320963952, 11589.343320691012, 11589.343320685926, 11589.343320685866, 11589.343320685866, 11589.343320685866, 11589.343320685988]


### num_document_passes = 2
| topic_id: 0 | topic_id: 1 | topic_id: 2 | topic_id: 3 | topic_id: 4   | topic_id: 5 | topic_id: 6 | topic_id: 7  | topic_id: 8 | topic_id: 9  | topic_id: 10 | topic_id: 11 | topic_id: 12 | topic_id: 13 | topic_id: 14 | topic_id: 15 | topic_id: 16 | topic_id: 17 | topic_id: 18 | topic_id: 19 |
|-------------|-------------|-------------|-------------|---------------|-------------|-------------|--------------|-------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|
| film        | party       | league      | station     | king          | game        | game        | regiment     | model       | song         | league       | linear       | saint        | district     | church       | film         | matter       | film         | trust        | party        |
| production  | castle      | cup         | research    | emperor       | station     | air         | foot         | species     | chart        | club         | socorro      | king         | town         | art          | game         | park         | miss         | bgcolor      | congress     |
| center      | chateau     | album       | london      | china         | version     | book        | raised       | town        | championship | album        | peak         | roman        | french       | show         | album        | system       | park         | community    | indian       |
| church      | parties     | club        | book        | province      | london      | station     | film         | water       | episode      | player       | kitt         | sur          | church       | children     | love         | file         | album        | nhs          | india        |
| research    | region      | football    | railway     | empire        | right       | engine      | bus          | support     | club         | band         | spacewatch   | les          | party        | german       | award        | game         | poland       | road         | army         |
| system      | river       | guitar      | students    | roman         | published   | using       | park         | power       | film         | goals        | anderson     | des          | president    | district     | club         | town         | president    | hospital     | london       |
| cause       | building    | vocals      | royal       | site          | air         | island      | battalion    | system      | version      | game         | mount        | air          | children     | site         | band         | party        | aircraft     | white        | william      |
| museum      | england     | track       | center      | dehydrogenase | film        | even        | river        | given       | singles      | film         | station      | song         | street       | hall         | isbn         | william      | song         | programs     | river        |
| education   | league      | games       | council     | period        | church      | character   | division     | similar     | play         | football     | river        | church       | election     | building     | system       | washington   | party        | foundation   | son          |
| file        | democratic  | video       | established | william       | control     | film        | championship | units       | points       | show         | neat         | total        | court        | written      | take         | election     | road         | ret          | battle       |

Значение преплексии на каждом проходе:

[2.002166420435021, 11525.038954980118, 11488.647874276287, 11432.740235584848, 11354.367263654498, 11254.982155642618, 11133.267272163981, 10982.580921302015, 10788.087364622208, 10529.36571757355]


### num_document_passes = 5

| topic_id: 0 | topic_id: 1 | topic_id: 2 | topic_id: 3  | topic_id: 4 | topic_id: 5 | topic_id: 6 | topic_id: 7 | topic_id: 8 | topic_id: 9 | topic_id: 10 | topic_id: 11 | topic_id: 12 | topic_id: 13 | topic_id: 14 | topic_id: 15 | topic_id: 16 | topic_id: 17 | topic_id: 18 | topic_id: 19 |
|-------------|-------------|-------------|--------------|-------------|-------------|-------------|-------------|-------------|-------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|
| royal       | album       | show        | championship | law         | league      | church      | saint       | film        | league      | chinese      | river        | station      | film         | power        | system       | force        | book         | india        | park         |
| army        | song        | film        | race         | president   | club        | linear      | aircraft    | father      | division    | system       | water        | party        | episode      | engine       | using        | battle       | published    | indian       | site         |
| regiment    | band        | star        | points       | political   | game        | socorro     | air         | award       | football    | china        | trust        | road         | television   | car          | example      | forces       | art          | museum       | castle       |
| foot        | records     | big         | round        | court       | cup         | william     | german      | daughter    | town        | support      | health       | railway      | director     | production   | theory       | military     | magazine     | island       | building     |
| infantry    | songs       | radio       | racing       | king        | students    | isbn        | africa      | mother      | club        | version      | areas        | district     | character    | prince       | form         | navy         | works        | canada       | street       |
| battalion   | chart       | award       | win          | act         | games       | peak        | population  | married     | stadium     | web          | species      | route        | game         | model        | research     | army         | show         | party        | design       |
| bgcolor     | king        | red         | men          | french      | education   | james       | france      | sir         | game        | memory       | lake         | street       | production   | energy       | space        | air          | story        | village      | hall         |
| men         | guitar      | man         | event        | social      | player      | opera       | squadron    | role        | district    | mobile       | mountain     | election     | show         | vehicle      | information  | attack       | arts         | population   | buildings    |
| ship        | love        | little      | tournament   | minister    | goals       | kitt        | language    | children    | baseball    | food         | region       | highway      | films        | speed        | data         | training     | written      | temple       | chateau      |
| corps       | track       | video       | champion     | rights      | football    | spacewatch  | airport     | london      | england     | windows      | sea          | bridge       | characters   | electric     | different    | command      | festival     | liberal      | hill         |

Значение преплексии на каждом проходе:

[1.9810176955803374, 11259.338319260123, 10871.226215878696, 10136.359941594508, 8984.999570865597, 7742.519186072006, 6843.55439305915, 6304.399992353714, 5975.885641456235, 5755.43352870641]


### num_document_passes = 10

| topic_id: 0 | topic_id: 1 | topic_id: 2  | topic_id: 3 | topic_id: 4 | topic_id: 5 | topic_id: 6 | topic_id: 7 | topic_id: 8 | topic_id: 9 | topic_id: 10 | topic_id: 11 | topic_id: 12 | topic_id: 13 | topic_id: 14 | topic_id: 15 | topic_id: 16 | topic_id: 17 | topic_id: 18 | topic_id: 19 |
|-------------|-------------|--------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|
| million     | law         | league       | party       | station     | river       | album       | system      | league      | london      | german       | army         | film         | texas        | air          | students     | road         | linear       | club         | species      |
| development | president   | championship | church      | japan       | town        | band        | using       | cup         | william     | germany      | battle       | episode      | california   | aircraft     | research     | india        | game         | radio        | foot         |
| economic    | party       | football     | political   | japanese    | building    | song        | model       | club        | book        | russian      | military     | show         | florida      | washington   | education    | indian       | socorro      | miss         | form         |
| oil         | court       | game         | social      | opera       | park        | records     | type        | emperor     | published   | republic     | forces       | television   | oklahoma     | squadron     | science      | route        | peak         | del          | often        |
| business    | election    | stadium      | movement    | railway     | village     | songs       | design      | division    | isbn        | soviet       | force        | award        | ohio         | island       | institute    | airport      | kitt         | winner       | common       |
| power       | saint       | games        | christian   | episode     | jpg         | chart       | engine      | district    | george      | european     | regiment     | role         | angeles      | fort         | program      | station      | spacewatch   | league       | usually      |
| companies   | canada      | cup          | god         | stations    | church      | guitar      | systems     | goals       | art         | russia       | attack       | films        | carolina     | road         | center       | highway      | games        | spanish      | tree         |
| production  | elected     | win          | book        | tokyo       | lake        | video       | standard    | cricket     | married     | van          | killed       | story        | star         | park         | society      | railway      | character    | awards       | example      |
| services    | canadian    | coach        | women       | network     | site        | rock        | available   | total       | james       | french       | command      | directed     | gordon       | wing         | technology   | hong         | player       | cup          | light        |
| health      | council     | player       | religious   | channel     | street      | track       | car         | england     | son         | dutch        | division     | movie        | comics       | mile         | schools      | kong         | anderson     | san          | animals      |

Значение преплексии на каждом проходе:

[1.9539752532315, 10788.128738534579, 9658.761839116385, 8109.908301100955, 6926.145901190617, 6275.731027385971, 5907.875953679706, 5676.900583304337, 5517.366150706584, 5399.501576395475, 5308.210064133085, 5235.350622086657, 5176.46696157842, 5128.810649762238]


Как можно видеть, что при num_document_passes=[1,2,5] значения перплексии очень большие и почти не уменьшаются (кроме 5) и адекватные значения начинают появляется при num_document_passes=10. Также это можно посмотреть на примере топиков. При малых значениях алгоритм очень плохо выделяет топики, и часто одни и те же слова, могут быть в нескольких топиках сразу. 

На примере num_document_passes=10 можно хорошо выделить topic_id: 6 связанный с музыкой, в topic_id: 11 почти все слова связанные с армией, а в topic_id: 1 и в topic_id: 2 хорошо выделяются слова связанные с политикой и играми соответственно.

После проведенных экспериментов, я могу сказать, что чем больше num_document_passes, тем точнее, но тем самым и дольше работает модель.  


## Значения перплексии при разных beta:
Beta = 0.0

Преплексия:
[6374.922999087668, 5971.94906111582, 5703.743190814501, 5520.280327351867, 5390.4614142650835, 5294.094546009813, 5220.546188067603, 5163.953001849265, 5119.300763980135, 5083.667488426292]

Разряженность матрицы: 0.925

----------------------------------------
Beta = -0.1

Преплексия:


Разряженность матрицы: 
----------------------------------------
Beta = -1.0

Преплексия:


Разряженность матрицы: 


