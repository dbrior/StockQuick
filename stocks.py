from wallstreet import Stock, Call, Put
import kivy
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelHeader
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from MyStock import MyStock
import time
from kivy.clock import Clock
kivy.require('1.10.1')
from kivy.config import Config
from kivy.app import App
import requests


Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '700')
Window.clearcolor = (0.2,0.2,0.2,1)

class StockPage(GridLayout):



    def __init__(self, **kwargs):

        super(StockPage, self).__init__(**kwargs)
        # self.height = 500
        # self.size_hint_y = None
        # self.width  = 300
        self.rows = 2
        App.title = "StockQuick"

        #Top Bar

        #Heigth
        top_height = 30

        self.top_bar = BoxLayout(orientation='horizontal',spacing=10,height=top_height + 4,size_hint_y=(None))
        top_bar = self.top_bar

        top_bar.add_widget(Label(text='',size_hint_x=(.5),height=top_height,size_hint_y=(None)))

        top_bar.add_widget(Label(text='Enter Ticker(s):',size=(85,top_height),size_hint=(None,None)))
        self.ticker = TextInput(text='',multiline=False,size=(200,top_height),size_hint=(None,None))
        self.ticker.bind(on_text_validate=self.enter)
        top_bar.add_widget(self.ticker)
        self.submit = Button(text='Submit',size=(75,top_height),size_hint=(None,None))
        self.submit.bind(on_press=self.enter)
        top_bar.add_widget(self.submit)

        top_bar.add_widget(Label(text='',size_hint_x=(.5),height=top_height,size_hint_y=(None)))

        self.add_widget(top_bar)


        #Stock Section (Dot notation kept to show structure)

        self.tab_box = TabbedPanel()
        tab_box = self.tab_box
        tab_box.background_color = [1,1,1,1]
        tab_box.do_default_tab = False
        tab_box.tab_height = 30
        tab_box.tab_width = 60



        self.quotes_header = TabbedPanelHeader(text='Quotes')
        self.quotes_height = 30
        self.stock_list = []
        self.quotes_blank = Label(text='',size_hint_x=(0.5))

        self.quotes_grid = GridLayout(cols=7,row_default_height=self.quotes_height,row_force_default=True)
        self.live_button = ToggleButton(text='Live',state='normal',size_hint_x=(0.125))
        self.live_button.bind(on_press=self.update)
        self.quotes_grid.add_widget(self.live_button)
        # self.tab_box.quotes_th.quotes_grid.add_widget(self.quotes_blank)
        # self.tab_box.quotes_th.quotes_grid.add_widget(Label(text='Ticker',size_hint_x=(0.125)))
        self.quotes_grid.add_widget(Label(text='Current',size_hint_x=(0.125)))
        self.quotes_grid.add_widget(Label(text='Open',size_hint_x=(0.125)))
        self.quotes_grid.add_widget(Label(text='High',size_hint_x=(0.125)))
        self.quotes_grid.add_widget(Label(text='Low',size_hint_x=(0.125)))
        self.quotes_grid.add_widget(Label(text='Close',size_hint_x=(0.125)))

        self.remove_all = Button(text="Clear",size_hint_x=(0.125))
        self.remove_all.bind(on_press=self.clearStocks)
        self.quotes_grid.add_widget(self.remove_all)
        self.quotes_header.content = self.quotes_grid
        tab_box.add_widget(self.quotes_header)




        # self.options_header = TabbedPanelHeader(text='Options')
        # self.options_header.content = self.optionsTab()
        # tab_box.add_widget(self.options_header)



        self.add_widget(self.tab_box)

        # self.tab_box.switch_to(self.quotes_header)
        Clock.schedule_once(lambda *args: self.tab_box.switch_to(self.quotes_header))
        # Clock.schedule_once(partial(self.switch, tab1), 0)


    def update(self,event):
        if self.live_button.state == 'down':
            self.event = Clock.schedule_interval(self.live,0.5)




    def live(self,event):
        # for stock in self.stock_list:
        #     stock.updateLabel()
        symbols = '?symbols='
        i = 0
        for stock in self.stock_list:
            if i != 0:
                symbols += ',' + stock.getTick()
            else:
                symbols += stock.getTick()
                i += 1

        url = 'https://api.iextrading.com/1.0/stock/market/batch'
        url += symbols + "&types=price,ohlc"
        # url += symbols + "&filter=lastSalePrice"


        r = requests.get(url)
        output = r.json()
        print(output)
        for stock in self.stock_list:
            ticker = stock.getTick().upper()
            price = str(output.get(ticker).get('price'))
            open = str(output.get(ticker).get('ohlc').get('open').get('price'))
            close = str(output.get(ticker).get('ohlc').get('close').get('price'))
            high = str(output.get(ticker).get('ohlc').get('high'))
            low = str(output.get(ticker).get('ohlc').get('low'))
            stock.updateLabel(price)
            stock.open_label.text = open
            stock.high_label.text = high
            stock.low_label.text = low
            stock.close_label.text = close
        if self.live_button.state == 'normal':
            return False

    def findPrice(self,ticker):
        stock = Stock(ticker,source='yahoo')
        return(str(stock.price))

    def initStocks(self,event):
        self.clearStocks(event)

        tick_csv = self.ticker.text
        tick_list = tick_csv.split(",")
        for tick in tick_list:
            blank1 = Label(text='',size_hint_x=(0.125))
            tick_label = Label(text='',size_hint_x=(0.125))
            price_label = Label(text='',size_hint_x=(0.125))
            open_label = Label(text='',size_hint_x=(0.125))
            high_label = Label(text='',size_hint_x=(0.125))
            low_label = Label(text='',size_hint_x=(0.125))
            close_label = Label(text='',size_hint_x=(0.125))
            blank2 = Label(text='',size_hint_x=(0.125))
            type_label = Label(text='',size_hint_y=None)
            strike_label = Label(text='',size_hint_y=None)
            bid_label = Label(text='',size_hint_y=None)
            ask_label = Label(text='',size_hint_y=None)
            option_block = GridLayout(rows=2)
            new_Stock = MyStock(tick,blank1,tick_label,price_label,open_label,high_label,low_label,close_label,blank2,type_label,strike_label,bid_label,ask_label,option_block)

            self.stock_list.append(new_Stock)

            # self.tab_box.quotes_th.content.add_widget(new_Stock.getBlank1())
            self.quotes_grid.add_widget(new_Stock.getTickLabel())
            self.quotes_grid.add_widget(new_Stock.getPriceLabel())
            self.quotes_grid.add_widget(new_Stock.open_label)
            self.quotes_grid.add_widget(new_Stock.high_label)
            self.quotes_grid.add_widget(new_Stock.low_label)
            self.quotes_grid.add_widget(new_Stock.close_label)
            self.quotes_grid.add_widget(new_Stock.getBlank2())

            self.live(event)

    def enter(self,event):
        self.initStocks(event)


        # self.initOptions(event)

        # popup = Popup(title='Test popup',
        # content=Label(text='Hello world'),
        # size_hint=(None, None), size=(400, 400))
        #
        # popup.open()





    def clearStocks(self,event):
        trim = []
        for stock in self.stock_list:
            self.quotes_grid.clear_widgets(children=stock.getWidgets())

    # def optionsTab(self):
    #     self.options_main_box = BoxLayout(orientation='vertical',size_hint_y=None,height=590)
    #
    #     self.options_main_box.add_widget(Label(text='Filters'))
    #
    #     self.options_main_box.add_widget(self.optionsGrid())
    #     return self.options_main_box
    #
    #
    #
    # def optionsGrid(self):
    #     self.option_grid = GridLayout(cols=1,size_hint_y=None,height=560)
    #     grid = self.option_grid
    #     grid.bind(minimum_height=grid.setter('height'))
    #
    #
    #
    #     self.optionsScroll = ScrollView(size_hint=(1, None), size=(grid.width, grid.height))
    #     self.optionsScroll.add_widget(grid)
    #     self.optionsScroll.do_scroll_y =True
    #     return self.optionsScroll
    #
    # def optionsFilters(self):
    #     return None
    #     #CURRENTLY CONSTURCTING THE FILTERS SECTION OF THE OPTIONS TAB
    #
    # def clearOptions(self,event):
    #     self.option_grid.clear_widgets()
    #
    #
    #
    # def initOptions(self,event):
    #     self.clearOptions(event)
    #
    #     tick_csv = self.ticker.text
    #     tick_list = tick_csv.split(",")
    #     for stock in self.stock_list:
    #         r = requests.get('https://query1.finance.yahoo.com/v7/finance/options/' + stock.getTick())
    #         options = r.json().get('optionChain').get('result')[0].get('options')
    #         self.option_grid.add_widget(stock.option_block)
    #
    #         puts = []
    #         for option in options:
    #             put_list = option.get('puts')
    #             stock.put_grid.add_widget(Label(text='Option'))
    #             stock.put_grid.add_widget(Label(text='Ticker'))
    #             stock.put_grid.add_widget(Label(text='Strike'))
    #             stock.put_grid.add_widget(Label(text='Bid'))
    #             stock.put_grid.add_widget(Label(text='Ask'))
    #             for put in put_list:
    #                 print(put)
    #                 if not (put.get('bid') == 0.00 or put.get('ask') == 0.00):
    #                     puts.append(put)
    #                     strike = put.get('strike')
    #                     bid = put.get('bid')
    #                     ask = put.get('ask')
    #
    #                     put_label = Label(text='Put')
    #                     tick_label = Label(text=stock.getTick().upper())
    #                     strike_label = Label(text=str(strike))
    #                     bid_label = Label(text=str(bid))
    #                     ask_label = Label(text=str(ask))
    #
    #
    #
    #                     stock.put_grid.add_widget(put_label)
    #                     stock.put_grid.add_widget(tick_label)
    #                     stock.put_grid.add_widget(strike_label)
    #                     stock.put_grid.add_widget(bid_label)
    #                     stock.put_grid.add_widget(ask_label)
    #
    #
    #
    #
    #
    #
    #
    #     for stock in self.stock_list:
    #         if True:
    #             None
    #             # new_option = Option(tick.upper())
    #             #
    #             # self.option_grid.add_widget(Label(text=new_put.expiration))
    #
    #
    # def getOptions(self):
    #     return None
    #     # self.base_call = Call(self.ticker.upper(),source='yahoo')
    #     # self.base_put = Put(self.ticker.upper(),source='yahoo')









class MyApp(App):

    def build(self):
        return StockPage()


if __name__ == '__main__':
    MyApp().run()
