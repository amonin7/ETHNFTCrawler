from web3 import Web3, HTTPProvider
import requests

CRYPTO_KITTIES_SC = '0x06012c8cf97BEaD5deAe237070F9587f8E7A266d'

CRYPTO_PUNKS_SC = '0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB'


class CollectionCreationCrawler:
    """
    A class used to crawl NFT collections creation events from Alchemy node

    Attributes
    ----------
    base_url : str
        an Alchemy API base url
    web3 : Web3
        a Web3 api provider (not to make all requests via http)

    Methods
    -------
    get_logs(from_block: int, to_block: int)
        :returns all logs from Alchemy api, where topic0 == "OwnershipTranfer" event and topic1 == 0x0,
        meaning, that the smart contract was just created
    get_latest_block_number()
        :returns the latest block number in the chain
    get_contract_type(contract: str) -> str
        :returns the type of the smart contract provided
    run(from_block: int) -> None
        particularly performs the main (run) action of the class, saying that
        1. it gets all the logs, which contain OwnershipTransfer events from 0x0 address
        2. gets the smart contract address form each of them
        3. checks, whether the smart contract has ERC721 or ERC1155 standard,
            or it is just a CryptoKitties / CryptoPunks smart contract
    """


    def __init__(self, apikey: str):
        """
        Parameters
        ----------
        apikey : str
            The apikey to interact with Alchemy API
        """
        self.base_url = f'https://eth-mainnet.g.alchemy.com/v2/{apikey}'
        self.web3 = Web3(HTTPProvider(self.base_url))
        if self.web3.isConnected():
            print('Successfully connected to Alchemy node')
        else:
            raise ConnectionError('Failed to connect to Alchemy node')

    def get_logs(self, from_block: int, to_block: int):
        """Provides all logs from Alchemy api, where topic0 == "OwnershipTranfer" event and topic1 == 0x0,
        meaning, that the smart contract was just created

        Parameters
        ----------
        from_block : int
            The number of the block to start listening logs from
        to_block : int
            The final number of the block we are listening logs from

        Returns
        -------
        list
            a list of logs got from Alchemy API with the described filters
        """
        logs = self.web3.eth.get_logs({
            'fromBlock': from_block,
            'toBlock': to_block,
            'topics': [
                '0x8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e0',
                '0x0000000000000000000000000000000000000000000000000000000000000000'
            ]
        })
        return logs

    def get_latest_block_number(self) -> int:
        """
        Returns
        -------
        int
            The latest block number in the chain
        """
        return int(self.web3.eth.get_block_number())

    def get_contract_type(self, contract: str) -> str:
        get_metadata_url = f'{self.base_url}/getContractMetadata?contractAddress={contract}'
        headers = {"Accept": "application/json"}
        r = requests.get(get_metadata_url, headers=headers)
        return r.json()['contractMetadata']['tokenType']

    def run(self, from_block: int) -> None:
        latest = self.get_latest_block_number()
        for i in range(from_block, latest + 1, 200):
            latest_block_number = 0
            cur_block_number = 0
            cur_contracts_list = []
            logs = self.get_logs(i, i + 199)
            for log in logs:
                cur_block_number = log['blockNumber']
                if cur_block_number != latest_block_number:
                    if len(cur_contracts_list) != 0:
                        print(f'{latest_block_number}: {cur_contracts_list}')
                    cur_contracts_list = []
                    latest_block_number = cur_block_number
                contract = log['address']
                contract_type = self.get_contract_type(contract)
                if contract_type == 'ERC721' or contract_type == 'ERC1155'\
                        or contract == CRYPTO_PUNKS_SC or contract == CRYPTO_KITTIES_SC:
                    cur_contracts_list.append(contract)
            if len(cur_contracts_list) != 0:
                print(f'{cur_block_number}: {cur_contracts_list}')
        return
