import logging, requests, json
import utils

logger = logging.getLogger('mail_ru_parser')


def get_answers(question):
    try:
        clear_question = utils.clear_html_tags(question)
        r = requests.get('https://go.mail.ru/answer_json?q=' + clear_question)
        j = json.loads(r.content.decode(r.encoding))
        answers = []
        for result in j['results']:
            if 'banswer' in result:
                answers.append(result['banswer'])
            elif 'answer' in result:
                answers.append(result['answer'])
        return answers
    except:
        logger.error('Houston, We\'ve Got a Problem With Mail.ru')
        return []
