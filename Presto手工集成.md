#   Ambari Presto Service 安装配置与操作指南

[TOC]

## 版本要求

* Ambari-server: 2.7.1 
* Apache PrestoSQL: 345

## 前期准备

### Presto JDK 依赖整理 - JAVA 需要11+ 版本包

### 提供PRESTO安装包内网下载

* 复制presto安装包和JDK11+ 到目录

```
mkdir -p /var/www/html/InsightHD/hdp/presto/
cp jdk-11.0.9_linux-x64_bin.tar /var/www/html/InsightHD/hdp/presto/
cp presto-server-345.tar /var/www/html/InsightHD/hdp/presto/
```

* 检查http server是否正常启动

浏览器打开http://server-ip/InsightHD/hdp/presto/。查看是否显示presto安装包。

- 修改每个节点配置, 并设置ulimit

```bash
vim /etc/security/limits.conf

## 添加如下两行
* soft nofile 131072
* hard nofile 131072
```

## 安装 Ambari Presto Service

* 复制 PRESTO-345 到ambari目录

```
cp -r /PRESTO/ /var/lib/ambari-server/resources/stacks/HDP/3.0/services/
```

~~修改launcher文件，在/usr/hdp/3.0.1.0-187/presto/presto-server-345/bin/launcher.py 加入两行~~

* 重新启动ambari-server

```
sudo ambari-server restart
```

## Ambari 安装presto

1. 进入并登录ambari。点击左侧的`Actions`按钮，选择`Add service`。
2. 在打开的窗口中勾选PRESTO服务。
3. Assign Slaves and Clients界面选择Presto client  (目前指coordinator默认安装在ambari-server节点, client不可以勾选主节点) 需要安装到的服务器。
5. 根据业务需要，修改Presto的配置参数,注意一定修改master ip为安装主节点。
6. 检查配置是否正确。
7. 开始安装Presto client，等待ambari安装presto完成(client不可以勾选主节点)。
8. 出现Summary界面，Presto client已安装到目标服务器。

## 启动Presto Service

创建mysql.properties，放入主节点和worker节点对应/usr/hdp/3.0.1.0-187/presto/presto-server-345/etc/catalog/ 目录

``` bash
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

``` bash
  /usr/hdp/3.0.1.0-187/presto/presto-server-345/presto-cli --server [coor_ip]:30088 --catalog hive --schema [dbname]
  # 进入presto 客户端交互模式
  show schemas;
  show tables; 
```

再Ambari UI 界面重启Presto，进入到 Presto coordinator 的安装根目录，执行如下命令,可以到当前数据库中的表（schema对应mysql数据库名）：

```shell
cd /usr/hdp/3.0.1.0-187/presto/presto-server-345/
./presto-cli --server ip:30088 --catalog mysql  --schema test
show schemas;
use [schema];
show tables;
```

之后进入presto管理页面，输入coordinator 主节点http://ip:30088 查看Running Node。如果可以查看页面，并且显示具体worker数目（为coordinator 数目 + worker 数目），且搜索查询可以即时显示，则启动成功。

# 作者信息

金昭

云计算与大数据研发部 - 浪潮系统软件部研发六处 -  三组