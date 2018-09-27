from wallstreet import Stock, Call, Put
import kivy
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
import requests


class MyStock:

    def __init__(self,ticker,blank1,tick_label,price_label,open_label,high_label,low_label,close_label,blank2,type_label,strike_label,bid_label,ask_label,option_block):
        self.ticker = ticker
        self.click = False
        self.price = None
        self.updatePrice()
        self.blank1 = blank1
        self.tick_label = tick_label
        self.price_label = price_label
        self.open_label = open_label
        self.high_label = high_label
        self.low_label = low_label
        self.close_label = close_label
        self.blank2 = blank2
        self.tick_label.text = self.ticker.upper()
        self.price_label.text = self.getPrice()
        self.type_label = type_label
        self.strike_label = strike_label
        self.bid_label = bid_label
        self.ask_label = ask_label
        self.put = None
        self.call = None
        self.option_block = option_block
        self.option_block_grid = GridLayout(cols=2)

        self.option_block_head = GridLayout(cols=5,spacing=10,size_hint_y=None,height=30)
        self.option_block_head.add_widget(Label(text=self.ticker.upper(),size_hint_x=None,width=40))
        self.option_block_head.add_widget(Label(text='Current Price: ' + self.getPrice(),size_hint_x=None,width=200))
        self.put_button = ToggleButton(text='Puts',size_hint_x=None,width=40)
        self.put_button.bind(on_press=self.putPress)
        self.option_block_head.add_widget(self.put_button)
        self.option_block_head.add_widget(ToggleButton(text='Calls',size_hint_x=None,width=40))
        self.option_block.add_widget(self.option_block_head)
        self.option_block.add_widget(self.option_block_grid)
        self.put_grid = GridLayout(cols=5,row_default_height=30,row_force_default=True)
        self.option_block_grid.add_widget(Label(text="",size_hint_x=None,width=20))
        self.option_block_grid.add_widget(self.put_grid)


    def putPress(self,event):
        self.click = not self.click
        if self.click:
            return None;
            

    def updatePrice(self):
        try:
            self.price = Stock(self.getTick(),source='yahoo').price
        except:
            self.price = "Price Error"

    def getPrice(self):
        return str(self.price)

    def getOptionBlock(self):
        return self.option_block

    def getTick(self):
        return self.ticker

    def getBlank1(self):
        return self.blank1

    def getBlank2(self):
        return self.blank2

    def getTickLabel(self):
        return self.tick_label

    def getPriceLabel(self):
        return self.price_label

    def getWidgets(self):
        return [self.blank1,self.tick_label,self.price_label,self.blank2,self.open_label,self.high_label,self.low_label,self.close_label]

    def updateLabel(self,newValue):

        self.price_label.text = newValue
