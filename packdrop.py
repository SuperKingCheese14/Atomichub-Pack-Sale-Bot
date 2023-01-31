import requests
import eospy.keys
import eospy.cleos

#Asks user to input their wallet address.
account = input("What is your wallet address? ")

#Asks the user to input the ID of the pack drop.
drop_id = input("Enter the drop id: ")

#Asks the user to input the amount of packs they wish to buy.
amount_packs = input("How many packs would you like to buy? ")

#Asks the user to input the amount of WAX for the deposit, must be followed by 8 decimals and WAX.
amount = input("Enter the amount of WAX required for the purchase with 8 decimals, EX: 200.00000000 WAX ")

#Get the delphi median.
def get_delphi_median():
    
    url = 'https://wax-testnet.eosphere.io/v1/chain/get_table_rows'
    scope = "waxpusd"
    jsonobj = {
        "json": True,
        "code": "delphioracle",
        "scope": scope,
        "table": "datapoints",
        "lower_bound": None,
        "upper_bound": None,
        "index_position": 1,
        "key_type": "",
        "limit": "1",
        "reverse": False,
        "show_payer": False
    }
    
    data = requests.post(url, json=jsonobj).json()
    
    median = data['rows'][0]['median']
    
    return median

median = get_delphi_median()

print("Retreived Delphi median "+str(median))

#Transfers the funds to atomicdropsx
def send_deposit():
    
    #Endpoint for testnet, change to main net if you need to.
    ce = eospy.cleos.Cleos(url='https://wax-testnet.eosphere.io')
    
    #The private key used to sign the transaction, replace with your own.
    key1 = eospy.keys.EOSKey('5JWHFhRwra2UNaZr1x9CyR9tkmq4obrCzuA2pnju9gSpMMFvNiR')
    
    #The payload, this contains all the data we need to provide to the blockchain.
    payload = [
            
            # The following are the arguments needed by the eosio.token contract.
            {
                'args': {
                    "from": account,  # Senders wallet address.
                    "to": 'atomicdropsx',  # Destination wallet address.
                    "quantity": amount,  # The amount of WAX to transfer.
                    "memo": 'deposit', # Memo, must be "deposit" or atomicdropsx won't accept.
                },
                "account": "eosio.token", # The smart contract of the WAX token.
                "name": "transfer",       # The name of the Smart contract action.
                "authorization": [{
                    "actor": account, #The address of the person sending the transaction.
                    "permission": "active",
                }],
            }
        ]
    
    # Here we convert the transaction data to binary.
    data=ce.abi_json_to_bin(payload[0]['account'],payload[0]['name'],payload[0]['args'])
    
    payload[0]['data']=data['binargs']
    
    payload[0].pop('args')
    
    trx = {"actions":[payload[0]]}
    
    try:
    
        # Now we send the transaction to the blockchain
        tx1 = ce.push_transaction(trx, [key1])
    
        # If the transaction was successful the script will show you the transacion ID.
        print(tx1)
    
    #Notify of any errors.
    except Exception as e:
        
        print(e)

#Claim the pack drop.
def push_action():

    #The api endpoint used for pushing the transaction. Test net in this case.
    ce = eospy.cleos.Cleos(url='https://wax-testnet.eosphere.io:443')

    #The private key used to sign the transaction, replace with your own.
    key1 = eospy.keys.EOSKey('5JWHFhRwra2UNaZr1x9CyR9tkmq4obrCzuA2pnju9gSpMMFvNiR')

    #The payload, this contains all the data we need to provide to the blockchain.
    payload = [
        
        # The following are the arguments needed by the eosio.token contract.
        {
            'args': {
                "claimer": account,  # Claimers wallet address.
                "drop_id": drop_id,  # Drop ID.
                "claim_amount": amount_packs,  # The amount of packs.
                "intended_delphi_median": median, # Delphi median.
                "referrer": "",
                "country": "",
            },
            "account": "atomicdropsx", # The smart contract address.
            "name": "claimdrop",       # The name of the Smart contract action.
            "authorization": [{
                "actor": account, #Claimers wallet address.
                "permission": "active",
            }],
        }
    ]

    # Here we convert the transaction data to binary.
    data=ce.abi_json_to_bin(payload[0]['account'],payload[0]['name'],payload[0]['args'])

    payload[0]['data']=data['binargs']

    payload[0].pop('args')

    trx = {"actions":[payload[0]]}
    
    try:

        # Now we send the transaction to the blockchain
        tx1 = ce.push_transaction(trx, [key1])

        # If the transaction was successful the script will show you the transacion ID.
        print(tx1)
    
    except Exception as e:
        
        print(e)
    
send = send_deposit()

push = push_action()

        
    