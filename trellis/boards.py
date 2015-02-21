from backend import Operator


class Board(object):
    """
    BOARD:  When initialized, a simple dict is saved to the database.
            board = {
                'name': <board_name>
                'lists': <list_of_boardlist>
                'archived': <true|false>
            }
    """
    def __init__(self, name, data=None):
        self._operator = Operator()
        if not self.in_database(name):
            self.board = {}
            self.board['name'] = name
            self.board['lists'] = None
            self.board['archived'] = False
            self._operator.save_board(self.board)
        elif not data:
            self.board = self._operator.get_board(name)
        elif data:
            self.board = data

    def archive(self):
        self.board['archived'] = True
        self._operator.update_board(self.board)

    def rename(self, new_name):
        old_name = self.board['name']
        self.board['name'] = new_name
        self._operator.update_board(self.board, old_name)

    def add_list(self, list_name):
        if not self.board['lists']:
            self.board['lists'] = []
        parent_board = self.board['name']
        new_list_item = BoardList(board=parent_board, name=list_name)
        self.board['lists'].append(new_list_item.lizt)
        self._operator.update_board(self.board)
        return new_list_item

    def get_list(self, list_name):
        for lizt in self.board['lists']:
            if lizt['name'] == list_name:
                list_from_dict = BoardList(from_dict=lizt)
                return list_from_dict

    def in_database(self, name):
        return self._operator.get_board(name)

    def update_board(self):
        self._operator.update_board(self.board)


class BoardList(object):
    """
    LIST:  A List class is represented as follows in the database:
            lists = [{
                'board': <board_name>
                'name': <list_name>
                'cards': <list_of_boardlistcard>
                'archived': <true|false>
            }]
    """

    def __init__(self, from_dict=None, *tuples, **dicts):
        if not from_dict:
            self.lizt = {}
            self.lizt['board'] = dicts.get('board')
            self.lizt['name'] = dicts.get('name')
            self.lizt['cards'] = None
            self.lizt['archived'] = False
        if from_dict:
            self.lizt = from_dict

    def archive(self):
        self.lizt['archived'] = True
        return self

    def rename(self, new_name):
        old_name = self.lizt['name']
        self.lizt['name'] = new_name
        return self

    def add_card(self, card):
        if not self.lizt['cards']:
            self.lizt['cards'] = []
        new_card = None
        if isinstance(card, BoardListCard):
            new_card = card
        elif isinstance(card, str):
            new_card = BoardListCard(card)
        self.lizt['cards'].append(new_card.card)
        return new_card

    def get_card(self, card_name):
        if self.lizt['cards']:
            for card in self.lizt['cards']:
                if card['name'] == card_name:
                    return BoardListCard(card_name, data=card)

    def save(self):
        board = self._operator.get_board(self.lizt['board'])
        for each in board['lists']:
            if each['name'] == self.lizt['name']:
                each = self.lizt


class BoardListCard(object):
    """
    CARD:   This is implemented as a simple dict.
            The property "name" must exist, as all
            cards must have a name.
    """
    def __init__(self, name, data=None):
        self.card = {}
        self.card['name'] = name
        self.card['archived'] = False
        if data:
            self.card = data

    def archive(self):
        self.card['archived'] = True

    def rename(self, new_name):
        self.card['name'] = new_name
        return self