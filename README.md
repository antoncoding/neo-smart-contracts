# Neo Smart Contracts

![](https://themerkle.com/wp-content/uploads/2017/08/NEO-GAS-Ethereum-Gas.jpg)

### Test Smart Contracts:
use neo-python to test your smart contracts:
```
np-prompt -p
```


* Sample 1: Hello World
```
neo> build {path}/smart-contracts/sample1.py test '' 01 False False
```
* Sample 2: Basic Computation
```
neo> build {path}/smart-contracts/sample2.py test 070202 02 False False add 1 2
```


* Sample 3: Balance Checker
```
neo> build {path}/smart-contracts/sample3.py test 070502 02 True False add AG4GfwjnvydAZodm4xEDivguCtjCFzLcJy 3
```
