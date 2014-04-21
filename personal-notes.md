
01 - Criou uma wallet
02 - Adicionou um servidor a wallet
	Copiou o contrato do servidor em sample_data/localhost.xml
	opentxs addserver 
		Colou o contrato do servidor, ele fornece as formas de conexao
03 - Registrou o NYM no servidor
	opentxs register --mynym (dois digitos iniciais do pseudonym) --server (dois digitos do serverId)

Definindo defaults para a opentxs
~/.ot/command-line-ot.opt

Emitindo um novo Asset

opentxs newasset: serve para vc criar um novo asset contract
opentxs issueasset: emite um asset no servidor. Para emitir um asset no servidor, você deve usar 
o mesmo NYM que assinou o asset contract e também deve ser o NYM no qual a chave pública aparece
no contrato.

Ao fazer isso, você irá criar um nova Account para o NYM. Para verificar digite "opentxs stat", esse
comando mostra as informações da wallet. Você verá que existe uma Account sem um label. 
Digite o comando: opentxs editaccount --myacct (copie o account id) e de um nome apropriado, por ex:
"Silver Issuer", pois essa conta representa quem é o emissor da moeda/asset.


Agora vamos criar uma nova Asset Account para o mesmo NYM

Para o NYM e o servidor é usado o padrão da wallet. O que falta é definir para qual asset que você
irá criar a conta. 

Digite "opentxs stat" para facilitar a copia dos parametros.

Agora digite "opentxs newacct --mypurse (copie o asset type)"

Digit "opentxs stat" para verificar. De uma label apropiada com:
"opentxs editacct --myacct (copie a account id)"
Dando por exemplo: "FellowTraveler's silver account"


Transferindo fundos de uma conta para outra

Vamos tranferir fundos da Issuer Account para uma conta comum. Para isso digite:
opentxs stat (para facilitar a copia dos parametros)
opentxs transfer --myacct (copie o account id da Issuer Account) --hisacct (copie o account id da conta comum)

O programa irá perguntar a quantia e em seguida se deseja enviar uma mensagem.

Agora valor da transação deve estar na outbox do Issuer Account, para verificar, digite:
opentxs outbox --myacct (copie o account id do Issuer Account)
Você verá que há uma transação pendente na outbox dessa conta.

Se você verificar o inbox da conta do recepiente, verá que está vazia, pq quem fez a transação foi
a outra conta, então não faz sentido o recepiente ter que baixar algo. Veja:
opentxs inbox --myacct (copie o account id da conta comum)

UMA BOA WALLET FARIA COM QUE ELA FOSSE ATUALIZADA, MOSTRANDO A INBOX COM A TRANSAÇÃO PENDENTE

opentxs refresh --myacct (copie o account id da conta comum)

Agora digitando opentxs inbox --myacct (da conta comum), poderá ver que apareceu uma transação pendente.

Vamos aceitar todas as transações na inbox digitando:
opentxs acceptall --myacct (copie o account id da conta comum)

Poderá ver em opentxs inbox --myacct (conta comum) ficou vazia. Se formos ver o saldo:
opentxs balance --myacct (conta comum)
Verá que está com o saldo com o valor da transação


# Queremos transformar o saldo em cash

Nesse caso não podemos pq o mint file não foi gerado. O servidor deve emitir um mint file.
Para isso, chamamos um script server-side que gera o mint file:
createmint

Irá mostrar quais parametros que precisamos para rodar o script, são eles:
createmint server_id server_user_id asset_type_id

Conseguimos essas informações no seguinte arquivo:
cat ~/.ot/server_data/notaryServer.xml

Veremos que há um "ARMORED NOTARY". Copie o conteúdo (apenas o código em base-64) e use o 
decode do opentxs:
opentxs decode
E cole o conteúdo

Agora podemos ver o conteúdo do arquivo e pegar o server_id e server_user_id. Enquanto o 
asset_type_id podemos pegar com opentxs stat.

createmint (cole aqui o server_id) (cole aqui o server_user_id) (cole aqui o asset_type_id)

Pronto, agora ele irá gerar diversas chaves que será o cash no qual poderá ser colocado
em qualquer client que tentar sacar o cash. Esse processo irá demorar algum tempo..

Para retirar o cash o que ele irá fazer internamente é tentar carregar o mint file, para
gerar o cash. Porém ele não vai achar o mint file, pq ele ainda não baixou o arquivo do 
servidor, já que ele acabou de ser gerado. 

Então, O QUE UM BOM CLIENT FARIA SERIA: TENTAR CARREGAR O MINT FILE, SE NÃO ENCONTRA, ELE
AUTOMATICAMENTE BAIXA DO SERVIDOR E FAZ O SAQUE.

Rode o comando:
opentxs showmint --mypurse (cole o asset type)

Você vera o mint file.

Primeiramente, vamos verificar a purse. Qual purse vc quer ver a sua Silver purse, dolar
purse, token purse? 
opentxs showpurse --mypurse (cole o asset type)

>> "UNABLE TO LOAD PURSE"

Como nunca sacamos antes, não existe uma purse.

Agora vamos sacar, digite:
opentxs withdraw 
Em seguida, digite a quantidade.

Verifique o saldo para ver se de fato abaixou o saldo:
opentxs balance

Veja agora em sua purse:
opentxs showpurse --mypurse (asset type)

Você verá os tokens que estão na purse.

Você pode fazer um depósito. Digite:
opentxs deposit

Ele pede o parâmetro indices. Você pode depositar cash ou cheque. Digite o indice dos
tokens que você quer depositar. Após fazer o depósito, verifique sua purse e veja 
que os tokens foram retirados de lá.


Criando outro NYM

Para isso digite:
opentxs newnym

Pronto. Verifique com opentxs stat. Vamos editar o nome do NYM:
opentxs editnym --mynym (nym)
Digite, por ex: "Trader Bob"


Escrevendo um cheque

opentxs cheque --hisnym (nym do trader bob)

Digite o valor; uma mensagem; um período de validade (default 3 meses)

O cheque será impresso na tela, copie o cheque. Apenas Trader Bob pode depositar o
cheque. 

MAS, o que deve acontecer: Bob não tem um Account para receber o cheque. Precisamos
criar um conta para ele. UMA BOA WALLET FARIA ISSO AUTOMATICAMENTE:

opentxs register --mynym (nym do trader bob)
opentxs newacct --mynym (nym do trader bob)
opentxs editacct --myacct (acct id) --mynym (nym do trader bob)
Label: Bob's Silver

Agora sim, deposite o cheque na conta de Bob:

opentxs deposit --mynym (nym do trader bob) --myacct (account do bob)
Cole o cheque.

Verifique os novos saldos com opentxs stat


Mas e se o servidor fizer algo de errado com meus arquivos

O que você deve fazer é:
opentxs verifyreceipt

UM BOM CLIENT FARIA ISSO AUTOMATICAMENTE (é parte de uma transação)


Caso eu não tenha o contrato do Asset

opentxs getcontract --args "contract_id (asset id)"

Ele irá baixar o contrato.


Trocar uma mensagem encriptada

Para encriptar digite:
opentxs encrypt --hisnym (nym do Trader Bob)
digite uma mensagem qualquer

Copie o resultado do comando.

Para decriptar, use:
opentxs decrypt --mynym (nym do Trade Bob)
cole a mensagem

Leia o resultado. Esse processo consiste em usar a chave pública para
encriptar e usar a chave privada para decriptar.

Porém, há outra forma de fazer isso, que é passando um chave simétrica.

Primeiramente crie uma nova chave simétrica:
opentxs newkey

O programa irá pedir uma passphrase para a chave. Digite: test
Ele irá retornar a chave simétrica, copie-a.

OK, agora iremos encriptar usando um chave simétrica. Digite:
opentxs pass_encrypt
Cole a chave simétrica criada anteriormente
Agora digite a mensagem a ser encriptada
Digite a passphrase da chave simétrica (test)

Copie o resultado (cipher text)

Agora iremos decriptar:
opentxs pass_decrypt
cole a chave simétrica
cole o cipher text
digite a passphrase (test)

É isso!


Moneychanger
[21:52] <+pigeons> assuming your ot libs are in ~/.local/lib add this line adjusted for your username to ~/.profile and then type source ~/.profile
[21:52] <+pigeons> export LD_LIBRARY_PATH=$HOME/.local/lib:$LD_LIBRARY_PATH




###################################### How To
Setup a fresh OT Server:
## Create Nym:
opentxs newnym
## Create credentials folder and copy from client_data to server_data:
mkdir ~/.ot/server_data/credentials && cp -R ~/.ot/client_data/credentials/* ~/.ot/server_data/credentials
## Modify Server Contract .xml file (get a basis file from sample-data/sample-contracts/localhost.xml)
## Sign Server Contract:
opentxs newserver --mynym Cq1ALIuPTPuQJLwCRqab4njQJaijJogfXaH463CDwqm
(the nym you got from "opentxs newnym")
## Decode Cached Key from wallet.xml:
opentxs decode
## Setup the server, enter the generated data from previous steps:
otserver
## Delete client_data

### opentxs:
newasset (or addasset for already signed, existing assets)
issueasset (issue the asset on the server)

# create mint (on server, for anonym digital cash):
createmint  server_id  server_user_id(Nym_ID)  asset_type_id  
e.g.:
createmint KujoAS9CzZgtKoqv68vD6H10itVIKuFwxlh5qfLOGAi Cq1ALIuPTPuQJLwCRqab4njQJaijJogfXaH463CDwqm Vu8hw5hhtttbvemN4fdsO1BAhjR1NdlORsH06hMaz87

# Download Mint Pubkeys (on client):
showmint        show a mint file for specific asset ID. Download if necessary.
e.g.:
opentxs showmint  --server KujoAS9CzZgtKoqv68vD6H10itVIKuFwxlh5qfLOGAi --mynym HRgfdsHFf9QkYrNF0Zz95APjFhmcHoSY2coX7yiKkQV --mypurse Vu8hw5hhtttbvemN4fdsO1BAhjR1NdlORsH06hMaz87
(mypurse = asset type ID)
