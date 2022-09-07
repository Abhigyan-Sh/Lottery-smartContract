from scripts.helpful_scripts import get_account, get_contractAddress
from brownie import Lottery, network, config, LinkToken
import time

def deployer():
    account= get_account()
    lottery_smart_contract= Lottery.deploy(
        get_contractAddress("ethTo_usd_PriceFeed"),
        get_contractAddress("_vrfCoordinator"),
        get_contractAddress("_link"),
        config["networks"][network.show_active()]["_keyHash"],
        config["networks"][network.show_active()]["_fee"],
        {"from": account},
        publish_source= config["networks"][network.show_active()].get("verify", False)
    )
    print("deployed! smart contract..")

def start_forLottery():
    account= get_account()
    lottery_smart_contract= Lottery[-1]
    start_txn= lottery_smart_contract.startLottery({"from":account})
    start_txn.wait(1)
    print('lottery has started!')

def end_forLottery():
    account= get_account()
    lottery_smart_contract= Lottery[-1]
    # funding contract with link token
    link_token= LinkToken.deploy({"from":account})
    txn_link= link_token.transfer(lottery_smart_contract.address, 1000000000000000000) # sending 0.1 link token will be sufficient
    txn_link.wait(1)
    # calling endLottery function of Lottery sm.contr.
    end_txn= lottery_smart_contract.endLottery({"from":account})
    end_txn.wait(1)
    print('Lottery has ended!!')
    time.sleep(60)
    print(f"{lottery_smart_contract.recentWinner} is the winner of this season.")

def enter_inLottery():
    account= get_account()
    lottery_smart_contract= Lottery[-1]
    enter_txn= lottery_smart_contract.enter({"from":account, "value":entranceFee_ofLottery()})
    enter_txn.wait(1)
    print('entered in lottery and you have been registered as a participant!')

def entranceFee_ofLottery():
    lottery_smart_contract= Lottery[-1]
    enter_txn= lottery_smart_contract.entranceFee() + 100000000
    return enter_txn

# deployment has not to wait(1) only the interactions have to wait(1) block
def main():
    deployer()
    start_forLottery()
    enter_inLottery()
    end_forLottery()

# deployment has no wait...
