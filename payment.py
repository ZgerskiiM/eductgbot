
from yoomoney import Authorize
from yoomoney import Client

Authorize(client_id="E1F13F1F0C639355A037D2757166898EA9FFF94BC6950A49AF6E70B5ADC0C400",
          redirect_uri='https://t.me/CollFriend_bot',
          scope=["account-info"
                 "operation history"
                 "operation details"
                 "incoming-transfers"
                 "payment-p2p"
                 "payment-shop"
                ]
        )
pay_token=''
client=Client(token)
user=client.account_info()

print('Account number', user.account)
print('Account balance', user.balance)
print('Account currency code in ISO 4217',user.currency)
print('Account status',user.account_status)
print('Account type', user.account_type)
print('extended balance iformation')
for pair in vars(user.balance_details):
    print(pair, "", vars(user.balance_details).get(pair))
print('about')
cards=user.cards_linked
if len(cards)!=0:
    for card in cards:
        print (card.pan_fragment, '',card.type)
    else:
        print('Zero card in account')