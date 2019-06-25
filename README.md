# NodeDepolyTool
## How to use it

### git description

```shell
echo "# NodeDeploy" >> README.md
git init
git add README.md
git commit -m "first commit"
git remote add origin https://github.com/bigdot123456/NodeDeploy.git
git push -u origin master
```

## Deploy command

* First, setup QT environment
* Second, run cmd
```linux
 python ./MATRIXCmd.py
```
Normal Node start:
```
cd work
./gman --datadir ./chaindata  init MANGenesis.json 
```

First command  
```
./gman --datadir ./chaindata --syncmode "full" --manAddress "MAN.CrsnQSJJfGxpb2taGhChLuyZwZJo" --testmode Yeying1021!@# --entrust ./entrust.json   
```

ipc connect
```
./gman attach ./chaindata/gman.ipc
```
rpc start
```
./gman --datadir ./chaindata --rpc --rpcaddr 0.0.0.0 --rpccorsdomain '*' --networkid 1 --debug --verbosity 5 --gcmode archive --outputinfo 0 --syncmode full    
```

wallet account generation
```
  personal.newAccount('password')
  
  echo "personal.newAccount('xxx')" | ./gman attach ./chaindata/gman.ipc | grep ^\"MAN
 ls chaindata/keystore
UTC--2019-06-14T09-29-19.066727000Z--MAN.UJX8DvDrjautigK8A2jGm9eojMwH	UTC--2019-06-14T09-29-52.551644000Z--MAN.D8bTbv4JNqTx1BXKzX8Vcejd68tG

net.peerCount

```

加密keystore  

./gman  --datadir ./chaindata aes --aesin Signature.json --aesout ./entrust.json  


 --manAddress MAN.2UMgrmoFTq2urw1xKBgx5XfpFnhR3 --entrust /home/matrix/entrust.json

1.--manAddress "MAN.CrsnQSJJfGxpb2taGhChLuyZwZJo" 地址更改为本机A1账户  
2.--entrust ./entrust.json 将"./entrust.json" 改为自己的entrust文件路径  
3.--testmode Yeying1021!@#  将"Yeying1021!@#"改为自己的entrust文件密码  

4. kill -9  `ps -ef | grep  -v grep  | grep  gman | grep 'networkid'  | awk '{print $2}'`   杀死gman  

5. /home/matrix/gman --datadir /home/matrix/chaindata  init /home/matrix/MANGenesis.json  初始化GMAN  

6. /home/matrix/gman --datadir /home/matrix/chaindata --rpc --rpcaddr 0.0.0.0 --rpccorsdomain '*' --networkid 666 --debug --verbosity 5 --manAddress MAN.2UMgrmoFTq2urw1xKBgx5XfpFnhR3 --entrust /home/matrix/entrust.json --gcmode archive --outputinfo 1 --syncmode 'full'  启动GMAN  

7. /home/matrix/gman  --datadir /home/matrix/chaindata aes --aesin Signature.json --aesout /home/matrix/entrust.json  加密keystore  
