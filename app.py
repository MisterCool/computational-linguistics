import logging, solver

logging.basicConfig(filename='app.log', level=logging.INFO)

logging.info('start app exec')

question = """Вставьте слово из трех букв, которое завершает первое слово и начинает второе.
КОНТРА(. . .)НЯ"""
answer = solver.get_possible_answer(question)
print(answer)

logging.info('end app exec')
