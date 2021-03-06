!pip install bitkub
!pip install songline

from bitkub import Bitkub
from songline import Sendline
import time

API_KEY = '' #เอาจากในเว็บมาใส่
API_SECRET = '' #เอาจากในเว็บมาใส่

# initial obj only non-secure
bitkub = Bitkub()

# initial obj non-secure and secure
bitkub = Bitkub(api_key=API_KEY, api_secret=API_SECRET)
bitkub.set_api_key(API_KEY)
bitkub.set_api_secret(API_SECRET)

token = '' #ใส่Token line
messenger = Sendline(token)

def rebalance():

  pair = 'THB_KUB' #เหรียญ
  token_name = 'KUB' #เหรียญ

  balance_coin=bitkub.balances()
  balance_coin=balance_coin['result'][token_name]['available'] + balance_coin['result'][token_name]['reserved']
  #print('จำนวนเหรียญในบัญชี' , balance_coin , 'เหรียญ')

  balance_thb=bitkub.balances()
  balance_thb=balance_thb['result']['THB']['available'] + balance_thb['result']['THB']['reserved']
  #print('จำนวนเงินในบัญชี' , balance_thb , 'บาท')

  last_price = bitkub.ticker(sym = pair)
  last_price = last_price[pair]['last']
  #print('ราคาเหรียญล่าสุด' , last_price , 'บาท')

  balance_value = balance_coin*last_price
  #print('มูลค่าเหรียญ' ,  balance_value , 'บาท')

  portfolio = balance_thb + balance_value
  #print('มูลค่าพอร์ต' , portfolio , 'บาท')

  fix_value = 5000 #ใส่จำนวนเงินที่ต้องการrebalance

  if balance_value > fix_value:
      amount = balance_value - fix_value
      if amount > 10: #มูลค่าเพิ่มมากกว่าเท่าไหร่ถึงจะแจ้งเตือน
        #print('ขายออก' , amount , 'บาท')
        #print(type(amount))
        #messenger.sendtext('Sell ' + str(float(amount)) +' Baht')
        messenger.sendtext('Sell {:,.2f} baht @ {:,.2f} '.format(amount,last_price))
      else:
        print('Rebalance : Waiting')
       # messenger.sendtext('Rebalance : Waiting')
  elif balance_value < fix_value:
      amount = fix_value - balance_value
      if amount > 10: #มูลค่าลดมากกว่าเท่าไหร่ถึงจะแจ้งเตือน
        print('ซื้อเข้า' , amount , 'บาท')
        messenger.sendtext('Buy {:,.2f} baht @ {:,.2f} '.format(amount,last_price))
      else:
        print('Rebalance : Waiting')
        #messenger.sendtext('Rebalance : Waiting')
  else:
      print('Not yet')

  #print('-----------------------------------------------')

while True:
  rebalance()
  time.sleep(10)
