[TOC]

## Hive表相关介绍



### 存储格式

Hive会为每个创建的数据库在HDFS上创建一个目录，该数据库的表会以子目录形式存储，表中的数据会以表目录下的文件形式存储。对于default数据库，默认的缺省数据库没有自己的目录，default数据库下的表默认存放在/user/hive/warehouse目录下。

**（1）textfile** 

textfile为默认格式，存储方式为行存储。数据不做压缩，磁盘开销大，数据解析开销大。 

（2）SequenceFile 

SequenceFile是Hadoop API提供的一种二进制文件支持，其具有使用方便、可分割、可压缩的特点。 

SequenceFile支持三种压缩选择：NONE, RECORD, BLOCK。 Record压缩率低，一般建议使用BLOCK压缩。 

（3）RCFile 

一种行列存储相结合的存储方式。 

（4）ORCFile 

数据按照行分块，每个块按照列存储，其中每个块都存储有一个索引。hive给出的新格式，属于RCFILE的升级版,性能有大幅度提升,而且数据可以压缩存储,压缩快 快速列存取。 

**（5）Parquet** 

Parquet也是一种行式存储，同时具有很好的压缩性能；同时可以减少大量的表扫描和反序列化的时间。

## DDL操作

### *创建表

#### 创建内部表

```
CREATE TABLE page_view(
     viewTime INT, 
     userid BIGINT,
     page_url STRING, 
     referrer_url STRING,
     ip STRING COMMENT 'IP Address of the User')
 COMMENT 'This is the page view table'
 PARTITIONED BY(dt STRING, country STRING)
 ROW FORMAT DELIMITED
   FIELDS TERMINATED BY '\001'
   COLLECTION ITEMS TERMINATED BY '\002'
   MAP KEYS TERMINATED BY '\003'
 STORED AS TEXTFILE;
```



#### 创建外部表

```
CREATE EXTERNAL TABLE page_view(
     viewTime INT, 
     userid BIGINT,
     page_url STRING, 
     referrer_url STRING,
     ip STRING COMMENT 'IP Address of the User',
     country STRING COMMENT 'country of origination')
 COMMENT 'This is the staging page view table'
 ROW FORMAT DELIMITED FIELDS TERMINATED BY '\054'
 STORED AS TEXTFILE
 LOCATION '/user/hadoop/warehouse/page_view';
```



#### 创建分区表

```sql
create external table student_ptn(
		id int, 
		name string, 
		sex string, 
		age int,
		department string)
partitioned by (city string)
row format delimited fields terminated by ","
location "/hive/student_ptn";
```

分区

分为静态分区、动态分区，主要区别在于静态分区需要手动指定，而动态分区是基于查询参数的位置去推断分区的名称，从而建立分区。总的来说就是，静态分区的列是在编译时期通过用户传递来决定的；动态分区只有在SQL执行时才能确定。

#### 使用CTAS创建表

作用： 就是从一个查询select创建表结构，包括只复制表结构和复制表结构+数据。

```
//复制表结构
create table student_copy like student_ptn;
//复制表结构和数据
create table student_ctas as select * from student where id < 95012;

```

注意：

如果在table的前面没有加external关键字，那么复制出来的新表。无论如何都是内部表
如果在table的前面有加external关键字，那么复制出来的新表。无论如何都是外部表

### 修改表

#### 修改表名

```
alter table student rename to new_student;
```

#### 修改表分区

修改分区，一般来说，都是指修改分区的数据存储目录。

在添加分区的时候，直接指定当前分区的数据存储目录。

```
alter table student_ptn add if not exists partition(city='beijing') location '/student_ptn_beijing';
```

修改已经指定好的分区的数据存储目录

```
alter table student_ptn partition (city='beijing') set location '/student_ptn_beijing';
```

先的分区文件夹仍存在，但是在往分区添加数据时，只会添加到新的分区目录

#### 修改表列

```
//增加表字段	
alter table new_student add columns (score int);
//修改表字段定义
alter table new_student change name new_name string;
```

### *删除表

删除表会移除表的元数据和数据，而HDFS上的数据，如果配置了Trash，会移到.Trash/Current目录下。

删除外部表时，表中的数据不会被删除

```
DROP TABLE table_name;
DROP TABLE IF EXISTS table_name;
```

从表或者表分区删除所有行，不指定分区，将截断表中的所有分区，也可以一次指定多个分区，截断多个分区。

```
TRUNCATE TABLE table_name;
TRUNCATE TABLE table_name PARTITION (dt='20080808');
```

## DML操作

### 数据加载

#### *Load方式

Hive Load语句不会在加载数据的时候做任何转换工作，而是纯粹的把数据文件复制/移动到Hive表对应的地址。

```sql
LOAD DATA [LOCAL] INPATH 'filepath' [OVERWRITE] INTO TABLE tablename [PARTITION (partcol1=val1,partcol2=val2 ...)]
```

- 如果命令中带有LOCAL，说明从本地文件系统加载数据，文件路径可以是相对路径，也可以是绝对路径。在这种情况下，首先将文件从本地复制到hdfs相应的位置，然后移动到hive表格中，这个时候原始数据文件是存在于hive表之下的路径下。这一点我会专门写一篇关于hive外部表的相应博文。
- 如果命令中没有LOCAL，代表我们的数据是从hdfs中读取文件，这个时候如果我们使用的是内部表，相应的hdfs的原始文件会消失，进入到相应的表格中。
- filepath 可以是一个相对路径，也可以是一个绝对路径。可以是一个文件，也可以是一个文件夹目录（这个时候文件夹下的所有文件都会被加载），
  -命令中如果带有overwirte，代表加载数据之前会清空目标表格，否则就是追加的方式。

#### *INSERT方式

##### 简单结构插入

```sql
INSERT [OVERWRITE] INTO TABLE tablename [PARTITION(partcol1 = col1,partcol2 =col2…)] SELECT _statement FROM  _statement
```

动态分区插入

```sql
INSERT [OVERWRITE] INTO TABLE tablename [PARTITION(partcol1 = col1,partcol2 ='${col}'…)] SELECT _statement FROM  _statement
```



### 数据查询

#### SELECT

提供了丰富的SQL查询方式来分析存储在Hadoop 分布式文件系统中的数据，可以将结构化的数据文件映射为一张数据库表，并提供完整的SQL查询功能，可以将SQL语句转换为MapReduce任务进行运行，通过自己的SQL 去查询分析需要的内容，这套SQL 简称Hive SQL，使不熟悉mapreduce 的用户很方便的利用SQL 语言查询，汇总，分析数据。

#### 字符函数

说明：对字符进行拼接、截取、去空格

枚举：concat、concat_ws、substring、trim、lpad、rpad、split、find_in_set

##### concat

说明：拼接函数

```sql
```

##### concat_ws



##### substring

##### trim

##### Ipad

##### rpad





#### 聚合函数

#### 数学函数

#### 时间函数

#### 窗口函数

#### 条件函数

JOIN

### 数据导出

