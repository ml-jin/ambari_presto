#  Presto 集群HA 安装配置与操作指南

[TOC]

## 版本要求

- Ambari-server: 2.7.1 
- Apache PrestoSQL: 345

## 前期准备

### Nginx 依赖整理以及Nginx 安装  - pcre, zlib, openssl.tgz

存放pcre, zlib, openssl 压缩包，到HOME下的presto目录：

- *.tar.gz (PrestoSQL官网)

### 提供PRESTO安装包内网下载

- 安装httpd服务

```shell
sudo yum install httpd
```

- 复制presto安装包到目录

```
mkdir -p /var/www/html/InsightHD/hdp/presto/
cp /path/to/presto.tar.gz /var/www/html/InsightHD/hdp/presto/
```

- 启动httpd服务

```
systemctl start httpd.service
```

- 检查http server是否正常启动

浏览器打开http://server-ip/InsightHD/hdp/presto/。查看是否显示presto安装包。

- 修改每个节点配置, 并设置ulimit

```bash
vim /etc/security/limits.conf

## 添加如下两行
* soft nofile 131072
* hard nofile 131072
```



## 安装 Nginx Service

- 复制 PRESTO-345 到ambari目录，并修改项目根目录下的bin/launcher文件

```
cp -r /path/to/PRESTO-345/ /var/lib/ambari-server/resources/stacks/HDP/3.0/services/PRESTO/
```

修改launcher文件，在`exec "$(dirname "$0")/launcher.py" "$@"`加入两行, 修改java 环境

```bash
PATH=/usr/hdp/3.0.1.0-187/presto/presto-server-345/jdk11/jdk-11.0.9/bin/:$PATH
export PATH
```

- 重新启动ambari-server

```
sudo ambari-server restart
```

## 启动Nginx Service

创建mysql.properties，放入主节点/usr/hdp/3.0.1.0-187/presto/presto-server-345/etc/catalog/ 目录和worker节点/home/presto/worker/presto-server-345/etc/catalog目录下

```bash
connector.name=mysql

connection-url=jdbc:mysql://[ip]:3306

connection-user=[user]

connection-password=[password]
```

- 创建hive.properties

  ```bash
  connector.name=hive-hadoop2
  hive.metastore.uri=thrift://[IP]:9083
  hive.config.resources=/etc/hadoop/3.0.1.0-187/0/core-site.xml,/etc/hadoop/3.0.1.0-187/0/hdfs-site.xml
  hive.allow-drop-table=true
  hive.allow-rename-table=true
  ```

- Hive client 连接命令：

  ```bash
  /usr/hdp/3.0.1.0-187/presto/presto-server-345/presto-cli --server [ip]:30088 --catalog hive --schema [dbname]
  # 进入presto 客户端交互模式
  show schemas;
  show tables; ...
  ```

## 启动Presto Service - 两个Coordinator, 一个worker节点 

``` bash

```



## 测试Presto 主备Coordinator

进入到Presto的安装目录，执行如下命令,可以查询到当前数据库中的表（schema对应mysql数据库名）：

```shell
cd /usr/hdp/3.0.1.0-187/presto/presto-server-345/
./presto-cli --server ip:30088 --catalog mysql  --schema test
show schemas
use [schema]
show tables;

```

之后进入presto管理页面，输入coordinator 主节点http://ip:30088 查看Running Node。如果可以查看页面，并且显示具体worker数目，搜索查询可以即时显示，则启动成功。

# 作者信息

金昭

浪潮系统软件部研发六处 -  三组

