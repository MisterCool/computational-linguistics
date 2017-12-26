import requests, json, re
from lxml import html

s = requests.Session()


def init_session(qid):
    r = s.get(
        'http://www.opentests.ru/component/option,com_ariquiz/quizId,%i/task,quiz/tmpl,component/index.php' % qid)
    try:
        match = re.search(r'[из ]\d+[ вопрос]', r.text)
        return int(match.group(0))
    except:
        return 0


def get_ticket(qid):
    r = s.post(
        'http://www.opentests.ru/component/option,com_ariquiz/quizId,%i/task,quiz/tmpl,component/index.php' % qid,
        data={
            'tmpl': 'component',
            'task': 'get_ticket',
            'quizId': qid,
            'option': 'com_ariquiz',
            'Itemid': '0'
        })
    tree = html.fromstring(r.text)
    ticket_id = tree.xpath('//*[@id="ticketId"]/@value')
    return ticket_id[0]


def get_question(ticket_id):
    r = s.post('http://www.opentests.ru/index.php',
               data={
                   'option': 'com_ariquiz',
                   'ticketId': ticket_id,
                   'task': 'question$ajax|getQuestion',
                   'parseTag': '0'
               })
    return json.loads(r.content.decode(r.encoding))


def save_question(answer, ticket_id, qid):
    r = s.post('http://www.opentests.ru/index.php',
               data={'tbxAnswer_' + qid: answer,
                     'tmpl': 'component',
                     'task': 'question$ajax|saveQuestion',
                     'option': 'com_ariquiz',
                     'ticketId': ticket_id,
                     'timeOver': 'false',
                     'Itemid': '0',
                     'option': 'com_ariquiz',
                     'qid': qid
                     })
    return json.loads(r.content.decode(r.encoding))


def get_result_link(ticket_id):
    return 'http://www.opentests.ru/component/option,com_ariquiz/task,question/ticketId,%s/tmpl,component/' % ticket_id
