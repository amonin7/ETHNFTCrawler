# ETHNFTCrawler

## Installation guide

1. Install & run Docker on your machine
2. run commands in your terminal
```shell
docker-compose build --build-arg API_KEY="<YOUR_ALCHEMY_API_KEY>" --build-arg START_BLOCK="<BLOCK_NUMBER_TO_START_WITH>"
docker-compose up
```
**Note:** remember to change `<YOUR_ALCHEMY_API_KEY>` with your particular API key gotten from Alchemy.
Also remember to replace `<BLOCK_NUMBER_TO_START_WITH>` with block, from which you want to start listening to smart contract addresses.

3. To ensure, that everything works correctly, please check, that your logs contain something like next:
```shell
crawler_1  | Successfully connected to Alchemy node
crawler_1  | 13821429: ['0xD16bdCCAe06DFD701a59103446A17e22e9ca0eF0']
crawler_1  | 13821531: ['0x0406dB8351aA6839169bb363f63c2c808FeE8f99']
crawler_1  | 13821564: ['0x6CA044FB1cD505c1dB4eF7332e73a236aD6cb71C']
```