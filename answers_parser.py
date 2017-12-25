import logging
import requests, json, utils

logger = logging.getLogger('mail_ru_parser')


def get_answers(question):
    try:
        clear_question = utils.clear_html_tags(question)
        r = requests.get('https://go.mail.ru/answer_json?q=' + clear_question, timeout=20)
        # logger.info('request time: %s' % (r.elapsed.total_seconds()))
        j = json.loads(r.content.decode(r.encoding))
        answers = []
        for result in j['results']:
            if 'banswer' in result:
                answers.append(result['banswer'])
            elif 'answer' in result:
                answers.append(result['answer'])
        return answers
    except:
        logger.warning('Houston, We\'ve Got a Problem With Mail.ru')
        return []
