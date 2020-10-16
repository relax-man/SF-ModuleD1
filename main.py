import requests
import sys


class TrelloRequests:

    def __init__(self):

        self.AUTH_PARAMS = {
            "key": "__Your key__",
            "token": "__Your token__"
        }

        self.BASE_URL = "https://api.trello.com/1/"
        self.BOARD_ID = "__Your board id__"

    def get_board(self):
        response = requests.get(
            self.BASE_URL + "boards/" + self.BOARD_ID + "/lists",
            params=self.AUTH_PARAMS
        )
        return response.json()

    def get_list(self, column_id):
        response = requests.get(
            self.BASE_URL + "lists/" + column_id + "/cards",
            params=self.AUTH_PARAMS
        )
        return response.json()

    def post_list(self, name):

        requests.post(
            self.BASE_URL + "boards/" + self.BOARD_ID + "/lists",
            params={
                'name': name,
                **self.AUTH_PARAMS
            }
        )
    
    def post_card(self, name, column_id):
        requests.post(
            self.BASE_URL + "cards",
            params={
                'name': name,
                'idList': column_id,
                **self.AUTH_PARAMS
            }
        )

    def put_card(self, column_id, task_id):

        requests.put(
            self.BASE_URL + "cards/" + task_id + "/idList",
            params={
                'value': column_id,
                **self.AUTH_PARAMS
            }
        )

    def delete_card(self, task_id):

        requests.delete(
           self.BASE_URL + "cards/" + task_id,
           params=self.AUTH_PARAMS
        )


def read():

    trello = TrelloRequests()
    data = trello.get_board()

    for column in data:

        column_tasks = trello.get_list(column['id'])

        print(column['name'], len(column_tasks))

        if not column_tasks:
            print("\t" + "Нет задач")
            continue

        for task in column_tasks:
            print("\t" + task['name'])


def create(card_name, column_name):

    trello = TrelloRequests()
    data = trello.get_board()

    column_exist = False
    for column in data: 
        if column['name'] == column_name:

            # Проверка на сопадение названий у задач
            column_tasks = trello.get_list(column['id'])
            for task in column_tasks:
                if task['name'] == card_name:
                    return False

            trello.post_card(card_name, column['id'])

            column_exist = True
            break

    if not column_exist:
        trello.post_list(column_name)
        create(card_name, column_name)

    return True


def move(card_name, column_name):

    trello = TrelloRequests()
    data = trello.get_board()
      
    task_id = None    
    for column in data:

        column_tasks = trello.get_list(column['id'])
        
        for task in column_tasks:
            if task['name'] == card_name:
                
                # Проверка, есть ли такая же задача в новой колонке
                if column['name'] == column_name:
                    return False
                
                task_id = task['id']

    if not task_id:
        return False

    for column in data:    
        if column['name'] == column_name:
            trello.put_card(column['id'], task_id)
            break

    return True


def delete(card_name, column_name):

    trello = TrelloRequests()
    data = trello.get_board()

    for column in data:
        if column['name'] == column_name:
            column_tasks = trello.get_list(column['id'])
            for task in column_tasks:
                if task['name'] == card_name:
                    trello.delete_card(task['id'])
                    return True

    return False


if __name__ == "__main__":

    if len(sys.argv) < 3:
        read()

    else:
        try:
            if globals()[sys.argv[1]](sys.argv[2], sys.argv[3]):
                print("Успешное выполнение")
            else:
                print("Возникла ошибка, Ваш запрос не выполнен")

        except KeyError:
            print("Неверное название функции")


