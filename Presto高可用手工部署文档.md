#  Presto 集群HA 安装配置与操作指南

[TOC]

## 版本要求

- Ambari-server: 2.7.1 
- Apache PrestoSQL: 345
- Nginx ： 1.6.1
- PCRE：8.32.17
- zlib:  1.2.7
- openssl: 1.0.2

## 前期准备

### Nginx 依赖整理以及Nginx 安装  - pcre, zlib, openssl.tgz

```bash
yum install -y pcre pcre-devel
yum install -y zlib zlib-devel
yum install -y openssl
```



或者下载pcre, zlib, openssl 压缩包，到HOME下的presto目录并离线安装：

### 提供Nginx安装包内网下载

- 安装httpd服务

```shell
sudo yum install httpd
```

- 复制presto安装包到目录

```
mkdir -p /var/www/html/InsightHD/hdp/presto/
cp /path/to/nginx-1.16.1.tar.gz /var/www/html/InsightHD/hdp/presto/
```

- 启动httpd服务

```
systemctl start httpd.service
```

- 检查http server是否正常启动

浏览器打开http://server-ip/InsightHD/hdp/presto/。查看是否显示Nginx安装包。

- 下载Nginx 安装包

```bash
cd /home/presto
wget http://[ip]/InsightHD/hdp/presto/nginx-1.16.1.tar.gz
```

- 安装三节点presto server, 其中连个coordinator(coor1, coor2), 一个worker. 安装过程参考集成流程文档。

## 安装 Nginx Service

- 解压缩 NGINX 到presto目录，并修改项目/usr目录下的conf/nginx.conf文件

```
cd /home/presto
tar -zxvf nginx-1.16.1.tar.gz
```

编译Nginx(默认已安装gcc++环境). 若无报错，则说明编译成功

```bash
cd nginx-1.16.1/
./configure && make && make install
```

- 修改nginx配置

``` bash
vim /usr/local/nginx/conf/nginx.conf
```

修改配置项, 分别定义后端服务器及端口，以及前端服务器及接口。backserver 为服务代理名称，可使用任意变量。

``` bash
#gzip  on;
    upstream [backserver] {  
      #ip_hash; 
      server [ip_coor1]:30088;
      server [ip_coor2]:30088 backup;
    }
    
    server {
        listen       50022;
        server_name  localhost;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        location / {
            proxy_pass http://[backserver];
            #root   html;
            index  index.html index.htm;
            proxy_connect_timeout 1;
            proxy_send_timeout 1;
            proxy_read_timeout 1;
        }
```



- 启动nginx-server, 访问[nginx_ip]:50022, 若显示presto 监控页面，则说明配置成功。

```
/usr/local/nginx/sbin/nginx
```

## 重启Presto Service

- 创建coor1,coor2 server config.properties配置

```bash
coordinator=true
  node-scheduler.include-coordinator=true
  http-server.http.port=30088
  query.max-memory=5GB
  query.max-memory-per-node=1GB
  query.max-total-memory-per-node=2GB
  discovery-server.enabled=true
  discovery.uri=http://[填写coor1_ip/coor2_ip自身]:30088
```

- worker config.properties配置：

```bash
  coordinator=false
  http-server.http.port=50022
  query.max-memory=5GB
  query.max-memory-per-node=1GB
  query.max-total-memory-per-node=2GB
  discovery.uri=http://[nginx]:50022
```

## 启动Presto Service - 两个Coordinator, 一个worker节点 

- 进入presto安装根目录, 重启服务器. 

``` bash
cd /path/to/presto
./bin/launcher start
```



## 测试Presto 主备Coordinator切换

进入到chrome 浏览器， 输入http://[nginx_ip]:50022, 应显示为2个worker. 代表一个worker主机和一个主coor1 server1.

- 使用命令关闭第一个presto. 可以看到presto 稍过片刻，提示登录，登陆后依然可以看到两个worker, 为worker1, coor2.

``` )bash
kill -9 $(pgrep presto)
```

- 使用presto命令重启coor1, 可以看到监控页面登出，重新登陆后，稍等10s, 可以看到服务重新切回coor1 和worker1.

```bash
cd /path/to/presto
./bin/launcher start

```

- 集群节点信息查询方法。

```bash
cd /path/to/presto-dir
./presto-cli --server [server_ip]:30088 --catalog hive
SELECT * FROM system.runtime.nodes;
```

信息显示样例：

               node_id                |          http_uri          | node_version | coordinator
--------------------------------------+----------------------------+--------------+----------
 ffffffff-ffff-ffff-ffff-ffffffffff00 | http://[worker1]:50022 | 345          | false    
 ffffffff-ffff-ffff-ffff-ffffffffff01 | http://[coor1]:30088 | 345          | true   



若以上测试均通过，则说明部署Presto HA成功。

# 作者信息

金昭

浪潮系统软件部研发六处 -  三组

