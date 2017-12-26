import logging, nltk, re
import utils, answers_parser

logger = logging.getLogger('solver')

# define extend stop words
# see https://github.com/nltk/nltk/issues/1367
extend_stop_words = [
    u'я', u'а', u'да', u'но', u'тебе', u'мне', u'ты', u'и', u'у', u'на', u'ща', u'ага',
    u'так', u'там', u'какие', u'который', u'какая', u'туда', u'давай', u'короче', u'кажется', u'вообще',
    u'ну', u'не', u'чет', u'неа', u'свои', u'наше', u'хотя', u'такое', u'например', u'кароч', u'как-то',
    u'нам', u'хм', u'всем', u'нет', u'да', u'оно', u'своем', u'про', u'вы', u'м', u'тд',
    u'вся', u'кто-то', u'что-то', u'вам', u'это', u'эта', u'эти', u'этот', u'прям', u'либо', u'как', u'мы',
    u'просто', u'блин', u'очень', u'самые', u'твоем', u'ваша', u'кстати', u'вроде', u'типа', u'пока', u'ок',
    u'ответ', u'слово', u'число', u'буква', u'точно'
]


# remove stop words from tokens
def clear_stop_words(tokens):
    stop_words = nltk.corpus.stopwords.words('russian')
    stop_words.extend(extend_stop_words)
    return [t for t in tokens if (t not in stop_words)]


def get_most_freq_words(sentence, output_count=100, need_char=False):
    clear_sentence = utils.clear_html_tags(sentence)
    tokens = nltk.word_tokenize(clear_sentence)
    tokens = utils.clear_not_alpha_tokens(tokens)
    tokens = clear_stop_words(tokens)
    if need_char:
        tokens = [w for w in tokens if len(w) == 1]
    freq_words = nltk.FreqDist(tokens)
    return freq_words.most_common(output_count)


# heuristic for find count of dots in (. . .)
def get_possible_answer_len(question):
    match = re.search(r'\([\. ]+\)', question)
    if (match):
        return match.group(0).count('.')
    return 0

# TODO: need heuristic for number and pictures
def get_possible_answer(question):
    mail_ru_answers = '\n '.join(answers_parser.get_answers(question))
    # logger.info('mail.ru answers: %s' % mail_ru_answers)
    need_char = question.find("букв") != -1 & question.find("слово") == -1
    freq_words = get_most_freq_words(mail_ru_answers, need_char=need_char)
    # logger.info('freq words answer: %s' % freq_words)
    possible_answer_len = get_possible_answer_len(question)
    if (possible_answer_len > 0):
        for answer in freq_words:
            if (len(answer[0]) == possible_answer_len):
                # logger.info('heuristic: dots (%i)' % possible_answer_len)
                return answer[0]
    if (freq_words):
        return freq_words[0][0]
    return '' # don't know :(...
