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

### 加密keystore  
```linux
./gman  --datadir ./chaindata aes --aesin Signature.json --aesout ./entrust.json  


 --manAddress MAN.2UMgrmoFTq2urw1xKBgx5XfpFnhR3 --entrust /home/matrix/entrust.json

1.--manAddress "MAN.CrsnQSJJfGxpb2taGhChLuyZwZJo" 地址更改为本机A1账户  
2.--entrust ./entrust.json 将"./entrust.json" 改为自己的entrust文件路径  
3.--testmode Yeying1021!@#  将"Yeying1021!@#"改为自己的entrust文件密码  

4. kill -9  `ps -ef | grep  -v grep  | grep  gman | grep 'networkid'  | awk '{print $2}'`   杀死gman  

5. /home/matrix/gman --datadir /home/matrix/chaindata  init /home/matrix/MANGenesis.json  初始化GMAN  

6. /home/matrix/gman --datadir /home/matrix/chaindata --rpc --rpcaddr 0.0.0.0 --rpccorsdomain '*' --networkid 666 --debug --verbosity 5 --manAddress MAN.2UMgrmoFTq2urw1xKBgx5XfpFnhR3 --entrust /home/matrix/entrust.json --gcmode archive --outputinfo 1 --syncmode 'full'  启动GMAN  

7. /home/matrix/gman  --datadir /home/matrix/chaindata aes --aesin Signature.json --aesout /home/matrix/entrust.json  加密keystore  
```
** command from hyk

```shell

1.生成随机账户的命令:
echo "personal.newAccount(\"testPassword\")" | ./gman attach ./chaindata/gman.ipc | grep "MAN."

参数说明:
    	testPassword为账户的密码

返回值: 
	账户的地址 如：MAN.2jZbK6yTkKiimnPyDCh1Sbv49XkWo
	账户的私钥文件在 ./chaindata/keystore中


2、生成sig.json
格式内容为：

[
	{
		"Address":"MAN.427Suh4uPVqdBzrSbn2u6FrNz9rYj",
		"Password":"testPassword"
	}
]


[
	{
		"Address":"MAN.427Suh4uPVqdBzrSbn2u6FrNz9rYj",
		"Password":"testPassword"
	},
	{
		"Address":"MAN.7nk8CuT9ZCBfSfYpfiXaomHvk4Nn",
		"Password":"xxx"
	},
	{
		"Address":"MAN.49nECVaeeHYQ2H8t91r33yrfCMhXA",
		"Password":"xxx"
	},
	{
		"Address":"MAN.2SaM3sU8K6bAEG4eA15g6ZtwA5UuZ",
		"Password":"xxx"
	},
	{
		"Address":"MAN.4GoTEXV33PEaRrHL1rA46UtZsDtaz",
		"Password":"xxx"
	},
	{
		"Address":"MAN.3keXfyBY2HRkRNYvhaynkGD6ezmNh",
		"Password":"xxx"
	}
]


1.生成entrust文件命令：

./gman --datadir ./chaindata aes --aesin ./key.json --aesout ./entrust.json --testmode aAc@1234



说明: 
	--aesin ./sig.json 	为entrust加密前的文件
	--aesout ./entrust.json 为加密后的文件
	--testmode abc@123 	为加密后的文件的密码 
	(注：密码规则：Your password's length must be between 8 and 16 characters, and should contain numbers, uppercase letters (A-Z), lowercase letters (a-z) and special characters)

3.签名功能的命令
echo "personal.sign('0x1234', 'MAN.2jZbK6yTkKiimnPyDCh1Sbv49XkWo', 'testPassword')" | ./gman attach ./chaindata/gman.ipc | grep "\"0x"

参数说明:
	'0x1234'为需要签名的数据，必须是16进制格式
	'MAN.2jZbK6yTkKiimnPyDCh1Sbv49XkWo' 为签名使用的账户
	'testPassword' 为签名账户的密码
返回值:
	签名结果(如: "0xcbd8989d8497d444cc66aa09a4ac19b58955f82d3f031aacea92aa8d133dc0074a8073594207980b00a357e20e872cfd42a161f51a83ae79bc54bf38cc926b491b")
	
```
### control message
```shell

时间同步： 
       依赖：yum -y install ntpdate
       命令：ntpdate ntp1.aliyun.com（时间服务器）
当前区块高度： echo 'man.blockNumber' |./gman attach ./chaindata/gman.ipc | grep  ^[0-9]
当前peer连接数： echo 'net.peerCount' |./gman attach ./chaindata/gman.ipc |grep  ^[0-9]


```