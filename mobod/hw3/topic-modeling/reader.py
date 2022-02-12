import string
import time
from nltk.corpus import stopwords

import pyspark
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.ml.feature import CountVectorizer
from pyspark.mllib.clustering import LDA
from pyspark.mllib.linalg import Vectors as MLlibVectors


def read_txt(data_path, min_token_tf, max_token_tf, min_token_length, min_doc_length=50, is_vw_format=False):
    time_start = time.time()
    sqlContext = SQLContext(sc)

    def parse_file(kv):
        line = kv if is_vw_format else kv[1]
        line = line.replace('\n', ' ').replace('\t', ' ')
        
        if is_vw_format:
            line_list = []
            for token in line.split(' ')[1: ]:
                lst = token.split(':')
                if len(lst) == 1:
                    line_list.append(token)
                else:
                    line_list += [lst[0]] * int(float(lst[1]))
            line = ' '.join(line_list)
        
        for p in string.punctuation:
            line = line.replace(p, ' ')
        
        tokens = [e.strip().lower() for e in line.strip().split(' ') if len(e) > 0]
        if is_vw_format:
            return tokens
        else:
            return (kv[0], tokens)


    def filter_token(kv):
        token = kv[0]
        value = kv[1]

        if value > max_token_tf or value < min_token_tf:
            return False

        if len(token) < min_token_length:
            return False

        if token in stopwords_:
            return False

        for i in '0123456789':
            if i in token:
                return False

        return True


    def get_tokens(tokens):
        if is_vw_format:
            return tokens
        return tokens[1]


    def parseVectors(line):
        return [int(line[2]), line[0]]


    if is_vw_format:
        dataset = sc.textFile(data_path)
    else:
        dataset = sc.wholeTextFiles(f'{data_path}/*')
    dataset = dataset.map(parse_file)
    
    word_counts = (dataset
                   .flatMap(lambda path_with_tokens: ((token, 1) for token in get_tokens(path_with_tokens)))
                   .reduceByKey(lambda cnt_1, cnt_2: cnt_1 + cnt_2)
                   .sortBy(lambda token_with_cnt: -token_with_cnt[1]))

    stopwords_ = set(stopwords.words('english'))

    word_counts = word_counts.filter(filter_token)
    vocab = set([e[0] for e in word_counts.collect()])

    print(f'Total number of tokens: {len(vocab)}')

    if is_vw_format:
        dataset = (dataset
                   .map(lambda kv: (0, list(filter(lambda t: t in vocab, kv))))
                   .filter(lambda kv: len(kv[1]) > min_doc_length))
    else:
        dataset = (dataset
                   .map(lambda kv: (kv[0].split('/')[-1], list(filter(lambda t: t in vocab, kv[1]))))
                   .filter(lambda kv: len(kv[1]) > min_doc_length))
    
    print(f'Total number of documents: {dataset.count()}')
    
    data_df = sqlContext.createDataFrame(dataset, ['id', 'tokens'])

    cv = CountVectorizer(inputCol="tokens", outputCol="vectors")
    cv_model = cv.fit(data_df)
    df_vect = cv_model.transform(data_df)

    bow = (df_vect
           .select('vectors', 'tokens', 'id')
           .rdd.map(parseVectors)
           .mapValues(MLlibVectors.fromML)
           .map(list))
    
    nnz = sum(bow.map(lambda x: list(x[1].values)).reduce(lambda x, y: x + y))
    print('Total collection size: {}'.format(nnz))

    print(f'Elapsed time : {int(time.time() - time_start)} sec.')
    return bow, cv_model, nnz
