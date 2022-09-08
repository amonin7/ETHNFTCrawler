from web3 import Web3, HTTPProvider
import requests


class CollectionCreationCrawler:

    def __init__(self, apikey: str):
        self.base_url = f'https://eth-mainnet.g.alchemy.com/v2/{apikey}'
        self.web3 = Web3(HTTPProvider(self.base_url))
        if self.web3.isConnected():
            print('Successfully connected to Alchemy node')
        else:
            raise ConnectionError('Failed to connect to Alchemy node')

    def get_logs(self, from_block: int, to_block: int):
        logs = self.web3.eth.get_logs({
            'fromBlock': from_block,
            'toBlock': to_block,
            'topics': [
                '0x8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e0',
                '0x0000000000000000000000000000000000000000000000000000000000000000'
            ]
        })
        return logs

    def get_latest_block_number(self):
        return int(self.web3.eth.get_block_number())

    def get_contract_type(self, contract: str) -> str:
        get_metadata_url = f'{self.base_url}/getContractMetadata?contractAddress={contract}'
        headers = {"Accept": "application/json"}
        r = requests.get(get_metadata_url, headers=headers)
        return r.json()['contractMetadata']['tokenType']

    def run(self, from_block: int) -> None:
        latest = self.get_latest_block_number()
        for i in range(from_block, latest + 1, 100):
            latest_block_number = 0
            cur_block_number = 0
            cur_contracts_list = []
            logs = self.get_logs(i, i + 99)
            for log in logs:
                cur_block_number = log['blockNumber']
                if cur_block_number != latest_block_number:
                    if len(cur_contracts_list) != 0:
                        print(f'{cur_block_number}: {cur_contracts_list}')
                    cur_contracts_list = []
                    latest_block_number = cur_block_number
                contract = log['address']
                contract_type = self.get_contract_type(contract)
                if contract_type == 'ERC721' or contract_type == 'ERC1155':
                    cur_contracts_list.append(contract)
            if len(cur_contracts_list) != 0:
                print(f'{cur_block_number}: {cur_contracts_list}')
        return
