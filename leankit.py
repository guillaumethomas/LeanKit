from requests import post, get
from collections import defaultdict
import json

company = 'isilon'
web_auth = "https://{}.leankit.com/io/reporting/auth".format(company)
web_a = 'https://{}.leankit.com/io/reporting/export/'.format(company)
output = 'json'


class leankit_token():
    def __init__(self, web, login):
        r = post(web, data=login)
        try:
            self.token = r.json()['token']
            self.expires = r.json()['expires']
        except ValueError:
            self.token = None
            self.expires = None


class Leankit_Board():
    def __init__(self, boardid, token):
        self.boardid = boardid
        self.token = token
        self.raw_cards = cards_leankit(self.boardid, self.token)
        self.raw_lanes = lanes_leankit(self.boardid, self.token)
        self.raw_users = users_leankit(self.boardid, self.token)
        self.raw_tags = ''
        self.raw_positions = positions_leankit(self.boardid, self.token)
        self.card = self.merge_cards()

    def get_card_num(self, field='cardId'):
        return [card[field] for card in self.raw_cards]

    def get_card_nam(self):
        return self.get_card_num('cardTitle')

    def get_types(self, field='cardType', field2='cardId'):
        ''' raw card is a list of dict '''
        cdict = defaultdict(list)
        for card in list(self.raw_cards.values()):
            cdict[card[field]].append(card[field2])
        return cdict

    def projects_lst(self, field='Project', c_field='cardTitle', u_field='assignedUserFullName'):
        p_cards = self.get_types()[field]
        lst = list()
        for card in p_cards:
            item = [card, self.raw_cards[card][c_field]]
            if card in self.raw_users:
                item.append(self.raw_users[card][u_field])
            lst.append(item)
        return lst

    def requests_lst(self, field='Request'):
        return self.projects_lst(field)

    def epics_lst(self, field='Epic'):
        return self.projects_lst(field)

    def tasks_lst(self, field='Task'):
        return self.projects_lst(field)

    def users_lst(self, field='assignedUserFullName', field_2='cardId'):
        lst = list(self.raw_users.values())
        ddict = defaultdict(list)
        for card in lst:
            ddict[card[field]].append(card[field_2])
        # return ddict
        tmp_dict = dict()
        for key, value in ddict.items():
            lst = list()
            for Id in value:
                tmp = [self.raw_cards[Id]['cardType'], Id]
                lst.append(tmp)
            tmp_dict[key] = lst

        result_dict = dict()
        for key, value in tmp_dict.items():
            t_dict = defaultdict(list)
            for i in value:
                t_dict[i[0]].append(i[1])
            result_dict[key] = dict(t_dict)
    
        return result_dict

    def projects_cards(self, field_1='parentCardId', field_2='cardId'):
        '''
            for project that have sub cards if give a list of these card
        '''
        d = defaultdict(list)
        for card in self.raw_cards.values():
            d[card[field_1]].append(card[field_2])
        return d

    def merge_cards(self, field='cardId'):
        pass
        '''

        '''




class Leankit_cards():
    pass


class Leankit_lanes():
    pass


class Leankit_users():
    pass


def data_leankit(
                 web_a, token, output='',
                 type_d='', board='',):
    if output is not '':
        output = '.{}'.format(output)
    if board is not '':
        board = '&boardId={}'.format(board)
    lst = [web_a, type_d, output, token, board]
    web = '{}{}{}?token={}{}'.format(*lst)
    r = get(web)
    return r.json()


def d_dict(lst, field='cardId'):
    ddict = defaultdict(list)
    for item in lst:
        ddict[item[field]].append(item)
    return ddict


def cards_leankit(boardid, token, field='cardId'):
    type_d = 'cards'
    args = [web_a, token, output, type_d, boardid]
    lst = data_leankit(*args)
    return {card[field]: card for card in lst}


def lanes_leankit(boardid, token, field='cardId'):
    type_d = 'lanes'
    args = [web_a, token, output, type_d, boardid]
    return data_leankit(*args)


def users_leankit(boardid, token, field='cardId'):
    type_d = 'userassignments/current'
    args = [web_a, token, output, type_d, boardid]
    lst = data_leankit(*args)
    return {card[field]: card for card in lst}


def positions_leankit(boardid, token, field='cardId'):
    type_d = 'cardpositions'
    args = [web_a, token, output, type_d, boardid]
    return d_dict(data_leankit(*args))


if __name__ == "__main__":
    
    boardid = '586372345'
    data = {
            'email': 'guillaume.thomas@isilon.com',
            'accountName' : 'isilon',
            'password' : 
            }

    token = leankit_token(web_auth, data)
    board = Leankit_Board(boardid, token.token)
   

