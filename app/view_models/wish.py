from .book import BookViewModel

class MyWishes:
    def __init__(self, gifts_of_mine, wish_count_list):
        self.gifts = []
        self.__gifts_of_mine = gifts_of_mine
        self.__wish_count_list = wish_count_list
        self.gifts = self.parse()

    def parse(self):
        temp_gifts = []
        for gift in self.__gifts_of_mine:
            temp_gifts.append(self.__matchine(gift))
        return temp_gifts

    def __matchine(self, gift):
        count = 0
        for wish_count in self.__wish_count_list:
            if gift.isbn == wish_count['isbn']:
                count = wish_count['count']
        r = {
            'wishes_count': count,
            'book': BookViewModel(gift.book),
            'id': gift.id
        }
        return r

