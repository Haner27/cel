rm -rf /tmp/mysql
mkdir -p /tmp/mysql/data /tmp/mysql/conf
echo "[mysqld]
server-id = 1 #服务Id唯一
port = 3306
log-error    = /var/log/mysql/error.log
#只能用IP地址
skip_name_resolve
#数据库默认字符集
character-set-server = utf8mb4
#数据库字符集对应一些排序等规则
collation-server = utf8mb4_general_ci
#设置client连接mysql时的字符集,防止乱码
init_connect='SET NAMES utf8mb4'
#最大连接数
max_connections = 300
" > /data/mysql/conf/mysql.conf
docker run --name mysql -itd --rm -v /tmp/mysql/conf:/etc/mysql/conf.d -v /tmp/mysql/data:/var/lib/mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 mysql:5.6