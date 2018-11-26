class TradeInfo:
    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self.__parse(goods)


    def __parse(self, goods):
        self.total = len(goods)
        self.trades = [self.__map_to_trade(single) for single in goods]


    def __map_to_trade(self,single):
        if single.create_datatime:
            time = single.create_datatime.strftime('%Y-%m-%d')
        else:
            time = "unknown"
        return dict(
            user_name=single.user.nickname,
            time = time,
            id=single.id
        )

from .book import BookViewModel

class MyTrades:
    def __init__(self, trades_of_mine, wish_count_list):
        self.trades = []
        self.__trades_of_mine = trades_of_mine
        self.__trades_count_list = wish_count_list
        self.trades = self.parse()

    def parse(self):
        temp_trades = []
        for gift in self.__trades_of_mine:
            temp_trades.append(self.__matchine(gift))
        return temp_trades

    def __matchine(self, trades):
        count = 0
        for trades_count in self.__trades_count_list:
            if trades.isbn == trades_count['isbn']:
                count = trades_count['count']
        r = {
            'wishes_count': count,
            'book': BookViewModel(trades.book),
            'id': trades.id
        }
        return r
