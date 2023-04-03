# hydra-forpoor

## <ins>How to setup project</ins>
The following commands must be executed on your host
### <ins>Clone the project</ins>
```bash
git clone git@github.com:Nemrode/hydra-forpoor.git
```
and
```bash
cd hydra-forpoor
```

### <ins>Virtual environment</ins>
```bash
python -m venv venv
```
and
```bash
source venv/bin/activate
```

### <ins>Install dependencies</ins>
```bash
pip install -r requirements.txt
```
If you have an error with <code>mysqlclient</code> you must install <code>libmysqlclient-dev</code> on your host
You can see this [link](https://askubuntu.com/questions/1321141/unable-to-install-mysqlclient-on-ubuntu-20-10) for more information

## <ins>SSH protocol</ins>
### <ins>Setup laboratory environment</ins>
#### <ins>Pull docker images for ssh server</ins>
```bash
docker pull linuxserver/openssh-server
```

#### <ins>Launch container</ins>
```bash
docker run -d --name openssh-server -e SUDO_ACCESS=true -e PASSWORD_ACCESS=true -e USER_PASSWORD="password" -e USER_NAME="test" -p 2222:2222 --restart unless-stopped lscr.io/linuxserver/openssh-server:latest
```

#### <ins>SSH connection</ins>
The following commands must be executed on your host
password : <code>password</code>
```bash
ssh -p 2222 test@localhost
```

### <ins>Test project on container</ins>
You must execute this command in your host at the root of the project
```bash
python main.py -p "ssh" -t "localhost" -u "test" -P 2222 -w passwords.txt
```

### <ins>Stop and remove container</ins>
When you are done with the container, you just have to close the shell opened in the container


## <ins>MySQL protocol</ins>
### <ins>Setup laboratory environment</ins>
#### <ins>Pull docker images for ssh server</ins>
```bash
docker pull mysql:latest
```

#### <ins>Launch container</ins>
```bash
docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=password -p 3306:3306 -d mysql
```

#### <ins>Setup container</ins>
```bash
docker exec -it mysql-container mysql -uroot -ppassword
```
and
```sql
ALTER USER 'root' IDENTIFIED WITH mysql_native_password BY 'password';
```
and
```sql
exit
```

#### <ins>Test connection</ins>
The following commands must be executed on your host
password : <code>password</code>
```bash
mysql -h 127.0.0.1 -P 3306 -u root -p
```


### <ins>Test project on container</ins>
You must execute this command in your host at the root of the project
```bash
python main.py -p "mysql" -t "127.0.0.1" -u "root" -P 3306 -w passwords.txt
```

### <ins>Stop and remove container</ins>
```bash
docker stop mysql-container
```
and
```bash
docker rm mysql-container
```