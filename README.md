# Neo Smart Contracts Tutorials
![](my-neo-python-tour.png)

### Required Packages:
`neo-boa` : for compile
`neo-python`: to interact with the NEO blockchain, build and deploy your contracts.


Use this command to start `neo-python`
```
np-prompt -p
```


##### Official Sample 1: Hello World
```
neo> build {path}/smart-contracts/sample1.py test '' 01 False False
```
#### Official Sample 2: Basic Computation
```
neo> build {path}/smart-contracts/sample2.py test 070202 02 False False add 1 2
```

#### Official Sample 3: Balance Checker
```
neo> build {path}/smart-contracts/sample3.py test 070502 02 True False add AG4GfwjnvydAZodm4xEDivguCtjCFzLcJy 3
```
You can you any other address instead of `AG4GfwjnvydAZodm4xEDivguCtjCFzLcJy`, it's only working as a key for Storage

## My Simple Smart Contract Samples

#### Sample -  Storage
```
build {path}/smart-contracts/sample-storage.py test 02 02 True True
```
It's a good idea to use `concat()` to contruct specific keystring for storage.

#### Sample: List Operation
Currently working with a samll function `remove_from_list`. Since the remove() and pop() functions are not working properly.
```
build {path}/smart-contracts/sample-list.py test 02 02 True True 1
```


#### Sample: Timestamp
This is about how to get Current TimeStamp in a neo Smart Contract. the GetTime() function works as well.
```
build {path}/smart-contracts/sample-timestamp.py test 02 02 True True
return: Current Linux TimeStamp
```
