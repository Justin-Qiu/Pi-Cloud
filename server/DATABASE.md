#### 在Ubuntu服务器上安装MySQL
`sudo apt-get update
sudo apt-get upgrade
sudo apt-get -f install
sudo apt-get install mysql-server
sudo apt-get isntall mysql-client
sudo apt-get install libmysqlclient-dev`

#### 检查是否安装成功
`sudo netstat -tap | grep mysql`

#### 登录root用户
`mysql -u root -p`

#### 添加管理员用户
`GRANT ALL ON  *.* TO admin@localhost IDENTIFIED BY '123456';`

#### 登录数据库
`mysql -u admin -p`

#### 建立数据库
`CREATE DATABASE pi;`

#### 使用数据库
`use pi`
或命令行直接输入
`mysql -u admin -p pi`

#### 建立一个名为users的用户表
`create table users(
   id int(11) not null auto_increment,
   username varchar(50) not null,
   token varchar(50) not null,
   primary key(id)
)ENGINE=InnoDB DEFAULT
CHARSET=utf8;`

#### 添加用户注册信息
`insert into users(username, token) values('1615123150', '123456');`

#### 查看用户表内容
`select * from users;`
