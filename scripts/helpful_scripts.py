from brownie import (accounts, network, config, Contract, MockV3Aggregator, LinkToken)
from brownie import VRFCoordinatorMock

LOCAL_DEVELOPMENT_NETWORK= ["development", "ganache-local"]
MAINNET_FORK_NETWORK= ["mainnet-fork-dev"]

def get_account(id= None, index= None):
    if id:
        return accounts.load(id)
    if index:
        return accounts[index]
    if (network.show_active() in LOCAL_DEVELOPMENT_NETWORK 
    or network.show_active() in MAINNET_FORK_NETWORK):
     return accounts[0]
    else:
        # below2
        return accounts.add(config["wallets"]["from_key"])

def get_contractAddress(contract_name):
    contract_type= {
        # below 4 import these contracts
        "ethTo_usd_PriceFeed": MockV3Aggregator,
        "_vrfCoordinator": VRFCoordinatorMock,
        "_link": LinkToken,
    }
    helping_contract= contract_type[contract_name]
    
    if (network.show_active() in LOCAL_DEVELOPMENT_NETWORK
    or network.show_active() in MAINNET_FORK_NETWORK):
        # helping_contract= contract_type[contract_name]
        if len(helping_contract)<= 0:
            deploy_mocks(helping_contract)
        contract= helping_contract[-1]
    else:
        helping_contractsAddress= config["networks"][network.show_active()][contract_name]
        # below 3
        contract= Contract.from_abi(helping_contract._name, helping_contractsAddress, helping_contract.abi)

    return contract

def deploy_mocks(helping_contract):
    DECIMALS= 8
    INITIAL_VALUE= 200000000000
    if helping_contract== MockV3Aggregator:
        tx= helping_contract.deploy(DECIMALS, INITIAL_VALUE, {"from": get_account()})
    if helping_contract== LinkToken:
        tx_link= helping_contract.deploy({"from": get_account()})
    if helping_contract== VRFCoordinatorMock:
        tx= helping_contract.deploy(tx_link.address, {"from": get_account()})
    print("helping contracts have been deployed successfully on local network..")
