---
title: 开发者手册概览
summary: 整体叙述了开发者手册，罗列了开发者手册的大致脉络。
---

# 开发者手册概览

本文是为应用程序开发者所编写的，如果你对 TiDB 的内部原理感兴趣，或希望参与到 TiDB 的开发中来，那么可前往阅读 [TiDB Kernel Development Guide](https://pingcap.github.io/tidb-dev-guide/) 来获取更多 TiDB 的相关信息。

本手册将展示如何使用 TiDB 来快速构建一个应用，并且阐述使用 TiDB 期间可能出现的场景以及可能会遇到的问题。因此，在阅读此页面之前，建议你先行阅读 TiDB 数据库快速上手指南。

此外，你还可以通过视频的形式学习免费的 [TiDB SQL 开发在线课程](https://pingcap.com/zh/courses-catalog/back-end-developer/?utm_source=docs-cn-dev-guide)。

## TiDB 基础

在你开始使用 TiDB 之前，你需要了解一些关于 TiDB 数据库的一些重要工作机制：

- 阅读 TiDB 事务概览来了解 TiDB 的事务运作方式或查看[为应用开发程序员准备的事务说明](#事务概览)查看应用开发程序员需要了解的事务部分。
- 学习免费在线课程 [TiDB 架构与特点](https://learn.pingcap.com/learner/course/600003/?utm_source=docs-cn-dev-guide)，了解构建 TiDB 分布式数据库集群的核心组件及其概念。
- 了解[应用程序与 TiDB 交互的方式](#应用程序与-tidb-交互的方式)。

## TiDB 事务机制

TiDB 支持分布式事务，而且提供乐观事务与悲观事务两种事务模式。TiDB 当前版本中默认采用 **悲观事务** 模式，这让你在 TiDB 事务时可以像使用传统的单体数据库 (如: MySQL) 事务一样。

你可以使用 BEGIN 开启一个事务，或者使用 `BEGIN PESSIMISTIC` 显式的指定开启一个**悲观事务**，使用 `BEGIN OPTIMISTIC` 显式的指定开启一个**乐观事务**。随后，使用 COMMIT 提交事务，或使用 ROLLBACK 回滚事务。

TiDB 会为你保证 `BEGIN` 开始到 `COMMIT` 或 `ROLLBACK` 结束间的所有语句的原子性，即在这期间的所有语句全部成功，或者全部失败。用以保证你在应用开发时所需的数据一致性。

若你不清楚**乐观事务**是什么，请暂时不要使用它。因为使用**乐观事务**的前提是需要应用程序可以正确的处理 `COMMIT` 语句所返回的所有错误。如果不确定应用程序如何处理，请直接使用**悲观事务**。

## 应用程序与 TiDB 交互的方式

TiDB 高度兼容 MySQL 协议，TiDB 支持大多数 MySQL 的语法及特性，因此大部分的 MySQL 的连接库都与 TiDB 兼容。如果你的应用程序框架或语言无 PingCAP 的官方适配，那么建议你使用 MySQL 的客户端库。同时，也有越来越多的三方数据库主动支持 TiDB 的差异特性。

因为 TiDB 兼容 MySQL 协议，且兼容 MySQL 语法，因此大多数支持 MySQL 的 ORM 也兼容 TiDB 。

## 扩展阅读

- [快速开始](#使用-tidb-cloud-(serverless-tier)-构建-tidb-集群)
- [选择驱动或 ORM 框架](#选择驱动或-orm-框架)
- [连接到 TiDB](#连接到-tidb)
- [数据库模式设计](#概述)
- [数据写入](#插入数据)
- [数据读取](#单表查询)
- [事务](#事务概览)
- [优化 SQL 性能](#概览)
- [示例程序](#使用-spring-boot-构建-tidb-应用程序)



# 快速开始

---
title: 使用 TiDB Cloud (Serverless Tier) 构建 TiDB 集群
summary: 使用 TiDB Cloud (Serverless Tier) 构建 TiDB 集群，并连接 TiDB Cloud 集群。
---

<!-- markdownlint-disable MD029 -->

## 使用 TiDB Cloud (Serverless Tier) 构建 TiDB 集群

本章节将介绍如何以最快的方式开始使用 TiDB。你将使用 [TiDB Cloud](https://en.pingcap.com/tidb-cloud) 创建并启动一个 Serverless Tier 集群，使用 TiDB SQL 客户端，插入数据。随后将从示例程序读取出数据。

若你需要在本地计算机上启动 TiDB，请参阅本地启动 TiDB。

### 第 1 步：创建 Serverless Tier 集群

1. 如果你还未拥有 TiDB Cloud 帐号，请先在此[注册](https://tidbcloud.com/free-trial)。
2. 使用你的 TiDB Cloud 帐号[登录](https://tidbcloud.com/)。
3. 在 [**Clusters**](https://tidbcloud.com/console/clusters) 页面中点击 **Create Cluster** 按钮。
4. **Create Cluster** 页面默认选择 **Serverless Tier**。你可以根据需要修改集群名称并选择可用区。
5. 点击 **Create** 创建 Serverless Tier 集群。

    你的 TiDB Cloud 集群将于 30 秒后创建完毕。

6. 集群创建完毕后，点击右上角的 **...** 按钮，在下拉框中选择 **Security Settings**。在对话框中设置连接集群的 root 密码，完成后点击 **Apply**。如果没有设置 root 密码，你将无法连接集群。
7. 点击 **Connect** 按钮，在连接对话框中选择你需要的连接方式和操作系统并保存对应的连接字符串。下面连接到集群的步骤将以 MySQL 客户端为例。

    > **注意：**
    >
    > 需要特别说明的是，在你使用 [Serverless Tier](https://docs.pingcap.com/tidbcloud/select-cluster-tier#serverless-tier) 集群时，你需要给你设置的用户名加上前缀（如 `2aEp24QWEDLqRFs.root` 中的 `2aEp24QWEDLqRFs`），若使用命令行连接，还需使用单引号包裹用户名。你可以在 [TiDB Cloud 用户名前缀](https://docs.pingcap.com/tidbcloud/select-cluster-tier#user-name-prefix) 中获得更多信息。

### 第 2 步：连接到集群

1. 若未安装 MySQL 客户端，请选择自己的操作系统，按以下步骤安装。

    <SimpleTab>

    <div label="macOS">

    对于 macOS 操作系统，如果你没有安装 Homebrew，请参考 [Homebrew 官网](https://brew.sh/index_zh-cn)进行安装。

    

    ```shell
    brew install mysql-client
    ```

    在安装完成的命令行输出中，得到以下信息：

    ```
    mysql-client is keg-only, which means it was not symlinked into /opt/homebrew,
    because it conflicts with mysql (which contains client libraries).

    If you need to have mysql-client first in your PATH, run:
    echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc

    For compilers to find mysql-client you may need to set:
    export LDFLAGS="-L/opt/homebrew/opt/mysql-client/lib"
    export CPPFLAGS="-I/opt/homebrew/opt/mysql-client/include"
    ```

    请运行其中的此行（命令行输出若与此处文档不一致，请以命令行输出为准）：

    

    ```shell
    echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc
    ```

    完成后，生效该配置文件（例如 `~/.zshrc`），并验证 MySQL 客户端是否安装成功：

    

    ```shell
    source ~/.zshrc
    mysql --version
    ```

    预期会得到形如以下的输出：

    ```
    mysql  Ver 8.0.28 for macos12.0 on arm64 (Homebrew)
    ```

    </div>

    <div label="Linux">

    对于 Linux 操作系统，下面以 CentOS 7 为例：

    

    ```shell
    yum install mysql
    ```

    完成后，请验证 MySQL 客户端是否安装成功：

    

    ```shell
    mysql --version
    ```

    预期会得到形如以下的输出：

    ```
    mysql  Ver 15.1 Distrib 5.5.68-MariaDB, for Linux (x86_64) using readline 5.1
    ```

    </div>

    </SimpleTab>

2. 运行第 1 步中得到的连接字符串。

    

    ```shell
    mysql --connect-timeout 15 -u '<prefix>.root' -h <host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=/etc/ssl/cert.pem -p
    ```

> **注意：**
>
> - 在连接 Serverless Tier 集群时，[必须使用 TLS 连接](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-tier-clusters)。
> - 如果你在连接时遇到问题，可阅读 [TiDB Cloud Serverless Tier 集群安全连接](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-tier-clusters) 来获得更多信息。

3. 填写密码，完成登录。

### 第 3 步：运行 SQL

尝试运行一下你在 TiDB Cloud 上的的第一个 SQL 吧：

```sql
SELECT 'Hello TiDB Cloud!';
```

你将看到这样的输出：

```sql
+-------------------+
| Hello TiDB Cloud! |
+-------------------+
| Hello TiDB Cloud! |
+-------------------+
```

如果你的实际输出与预期输出一致，表示你已经在 TiDB Cloud 上成功地运行了 SQL 语句。

---
title: 使用 TiDB 的增删改查 SQL
summary: 简单介绍 TiDB 的增删改查 SQL。
---

## 使用 TiDB 的增删改查 SQL

本章将简单介绍 TiDB 的增删改查 SQL 的使用方法。

### 在开始之前

请确保你已经连接到 TiDB 集群，若未连接，请参考[使用 TiDB Cloud (Serverless Tier) 构建 TiDB 集群](#第-1-步创建-serverless-tier-集群)来创建一个 Serverless Tier 集群。

### 基本 SQL 操作

> **注意：**
>
> 此处文档引用并简化自 TiDB 文档中的 SQL 基本操作，你可直接前往此文档获取更全面、深入的 SQL 基本操作信息。

成功部署 TiDB 集群之后，便可以在 TiDB 中执行 SQL 语句了。因为 TiDB 兼容 MySQL，你可以使用 MySQL 客户端连接 TiDB，并且大多数情况下可以直接执行 MySQL 语句。

SQL 是一门声明性语言，它是数据库用户与数据库交互的方式。它更像是一种自然语言，好像在用英语与数据库进行对话。本文档介绍基本的 SQL 操作。完整的 SQL 语句列表，参见 [TiDB SQL 语法详解](https://pingcap.github.io/sqlgram/)。

### 分类

SQL 语言通常按照功能划分成以下的 4 个部分：

- **DDL (Data Definition Language)**：数据定义语言，用来定义数据库对象，包括库、表、视图和索引等。
- **DML (Data Manipulation Language)**：数据操作语言，用来操作和业务相关的记录。
- **DQL (Data Query Language)**：数据查询语言，用来查询经过条件筛选的记录。
- **DCL (Data Control Language)**：数据控制语言，用来定义访问权限和安全级别。

此文档中，主要介绍 DML 和 DQL，即数据操作语言和数据查询语言。其余部分可查看 SQL 基本操作或 [TiDB SQL 语法详解](https://pingcap.github.io/sqlgram/)获得更多信息。

### DML 数据操作语言

数据操作语言可完成数据的增删改。

使用 `INSERT` 语句向表内插入表记录。例如：



```sql
INSERT INTO person VALUES(1,'tom','20170912');
```

使用 `INSERT` 语句向表内插入包含部分字段数据的表记录。例如：



```sql
INSERT INTO person(id,name) VALUES('2','bob');
```

使用 `UPDATE` 语句向表内修改表记录的部分字段数据。例如：



```sql
UPDATE person SET birthday='20180808' WHERE id=2;
```

使用 `DELETE` 语句向表内删除部分表记录。例如：



```sql
DELETE FROM person WHERE id=2;
```

> **注意：**
>
> `UPDATE` 和 `DELETE` 操作如果不带 `WHERE` 过滤条件是对全表进行操作。

### DQL 数据查询语言

数据查询语言是从一个表或多个表中检索出想要的数据行，通常是业务开发的核心内容。

使用 `SELECT` 语句检索单表内数据。例如：



```sql
SELECT * FROM person;
```

在 `SELECT` 后面加上要查询的列名。例如：



```sql
SELECT name FROM person;
```

运行结果为：

```
+------+
| name |
+------+
| tom  |
+------+
1 rows in set (0.00 sec)
```

使用 `WHERE` 子句，对所有记录进行是否符合条件的筛选后再返回。例如：



```sql
SELECT * FROM person WHERE id < 5;
```



# 示例程序

---
title: TiDB 和 Java 的简单 CRUD 应用程序
summary: 给出一个 TiDB 和 Java 的简单 CRUD 应用程序示例。
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD029 -->

## TiDB 和 Java 的简单 CRUD 应用程序

本文档将展示如何使用 TiDB 和 Java 来构造一个简单的 CRUD 应用程序。

> **注意：**
>
> 推荐使用 Java 8 及以上版本进行 TiDB 的应用程序的编写。

### 拓展学习视频

- [使用 Connector/J - TiDB v6](https://learn.pingcap.com/learner/course/840002/?utm_source=docs-cn-dev-guide)
- [在 TiDB 上开发应用的最佳实践 - TiDB v6](https://learn.pingcap.com/learner/course/780002/?utm_source=docs-cn-dev-guide)

> **建议：**
>
> 如果你希望使用 Spring Boot 进行 TiDB 应用程序的编写，可以查看 [Build the TiDB Application using Spring Boot](#使用-spring-boot-构建-tidb-应用程序)。

### 第 1 步：启动你的 TiDB 集群

本节将介绍 TiDB 集群的启动方法。

#### 使用 TiDB Cloud Serverless Tier 集群

[创建 Serverless Tier 集群](#第-1-步创建-serverless-tier-集群)。

#### 使用本地集群

此处将简要叙述启动一个测试集群的过程，若需查看正式环境集群部署，或查看更详细的部署内容，请查阅本地启动 TiDB。

**部署本地测试集群**

适用场景：利用本地 macOS 或者单机 Linux 环境快速部署 TiDB 测试集群，体验 TiDB 集群的基本架构，以及 TiDB、TiKV、PD、监控等基础组件的运行

1. 下载并安装 TiUP。

    

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. 声明全局环境变量。

    > **注意：**
    >
    > TiUP 安装完成后会提示对应 profile 文件的绝对路径。在执行以下 source 命令前，需要根据 profile 文件的实际位置修改命令。

    

    ```shell
    source .bash_profile
    ```

3. 在当前 session 执行以下命令启动集群。

    - 直接执行 `tiup playground` 命令会运行最新版本的 TiDB 集群，其中 TiDB、TiKV、PD 和 TiFlash 实例各 1 个：

        

        ```shell
        tiup playground
        ```

    - 也可以指定 TiDB 版本以及各组件实例个数，命令类似于：

        

        ```shell
        tiup playground v5.4.0 --db 2 --pd 3 --kv 3
        ```

        上述命令会在本地下载并启动某个版本的集群（例如 v5.4.0）。最新版本可以通过执行`tiup list tidb` 来查看。运行结果将显示集群的访问方式：

        ```
        CLUSTER START SUCCESSFULLY, Enjoy it ^-^
        To connect TiDB: mysql --comments --host 127.0.0.1 --port 4001 -u root -p (no password)
        To connect TiDB: mysql --comments --host 127.0.0.1 --port 4000 -u root -p (no password)
        To view the dashboard: http://127.0.0.1:2379/dashboard
        PD client endpoints: [127.0.0.1:2379 127.0.0.1:2382 127.0.0.1:2384]
        To view the Prometheus: http://127.0.0.1:9090
        To view the Grafana: http://127.0.0.1:3000
        ```

> **注意：**
>
> - 支持 v5.2.0 及以上版本的 TiDB 在 Apple M1 芯片的机器上运行 `tiup playground`。
> - 以这种方式执行的 playground，在结束部署测试后 TiUP 会清理掉原集群数据，重新执行该命令后会得到一个全新的集群。
> - 若希望持久化数据，可以执行 TiUP 的 `--tag` 参数：`tiup --tag <your-tag> playground ...`，详情参考 TiUP 参考手册。

#### 使用云原生开发环境

基于 Git 的预配置的开发环境：[现在就试试](#gitpod)。

该环境会自动克隆代码，并通过 TiUP 部署测试集群。

### 第 2 步：获取代码



```shell
git clone https://github.com/pingcap-inc/tidb-example-java.git
```

<SimpleTab groupId="language">

<div label="使用 Mybatis（推荐）" value="mybatis">

[Mybatis](https://mybatis.org/mybatis-3/index.html) 是当前比较流行的开源 Java 应用持久层框架，本文将以 Maven 插件的方式使用 [MyBatis Generator](https://mybatis.org/generator/quickstart.html) 生成部分持久层代码。

进入目录 `plain-java-mybatis`：



```shell
cd plain-java-mybatis
```

目录结构如下所示：

```
.
├── Makefile
├── pom.xml
└── src
    └── main
        ├── java
        │   └── com
        │       └── pingcap
        │           ├── MybatisExample.java
        │           ├── dao
        │           │   └── PlayerDAO.java
        │           └── model
        │               ├── Player.java
        │               ├── PlayerMapper.java
        │               └── PlayerMapperEx.java
        └── resources
            ├── dbinit.sql
            ├── log4j.properties
            ├── mapper
            │   ├── PlayerMapper.xml
            │   └── PlayerMapperEx.xml
            ├── mybatis-config.xml
            └── mybatis-generator.xml
```

其中，自动生成的文件有：

- `src/main/java/com/pingcap/model/Player.java`：Player 实体类文件
- `src/main/java/com/pingcap/model/PlayerMapper.java`：Player Mapper 的接口文件
- `src/main/resources/mapper/PlayerMapper.xml`：Player Mapper 的 XML 映射，它是 Mybatis 用于生成 Player Mapper 接口的实现类的配置

这些文件的生成策略被写在了 `mybatis-generator.xml` 配置文件内，它是 [Mybatis Generator](https://mybatis.org/generator/quickstart.html) 的配置文件，下面配置文件中添加了使用方法的说明：



```xml
<!DOCTYPE generatorConfiguration PUBLIC
 "-//mybatis.org//DTD MyBatis Generator Configuration 1.0//EN"
 "http://mybatis.org/dtd/mybatis-generator-config_1_0.dtd">

<generatorConfiguration>
    <!--
        <context/> entire document: https://mybatis.org/generator/configreference/context.html

        context.id: A unique identifier you like
        context.targetRuntime: Used to specify the runtime target for generated code.
            It has MyBatis3DynamicSql / MyBatis3Kotlin / MyBatis3 / MyBatis3Simple 4 selection to choice.
    -->
    <context id="simple" targetRuntime="MyBatis3">
        <!--
            <commentGenerator/> entire document: https://mybatis.org/generator/configreference/commentGenerator.html

            commentGenerator:
                - property(suppressDate): remove timestamp in comments
                - property(suppressAllComments): remove all comments
        -->
        <commentGenerator>
            <property name="suppressDate" value="true"/>
            <property name="suppressAllComments" value="true" />
        </commentGenerator>

        <!--
            <jdbcConnection/> entire document: https://mybatis.org/generator/configreference/jdbcConnection.html

            jdbcConnection.driverClass: The fully qualified class name for the JDBC driver used to access the database.
                Used mysql-connector-java:5.1.49, should specify JDBC is com.mysql.jdbc.Driver
            jdbcConnection.connectionURL: The JDBC connection URL used to access the database.
        -->
        <jdbcConnection driverClass="com.mysql.jdbc.Driver"
            connectionURL="jdbc:mysql://localhost:4000/test?user=root" />

        <!--
            <javaModelGenerator/> entire document: https://mybatis.org/generator/configreference/javaModelGenerator.html
            Model code file will be generated at ${targetProject}/${targetPackage}

            javaModelGenerator:
                - property(constructorBased): If it's true, generator will create constructor function in model
        -->
        <javaModelGenerator targetPackage="com.pingcap.model" targetProject="src/main/java">
            <property name="constructorBased" value="true"/>
        </javaModelGenerator>

        <!--
            <sqlMapGenerator/> entire document: https://mybatis.org/generator/configreference/sqlMapGenerator.html
            XML SQL mapper file will be generated at ${targetProject}/${targetPackage}
        -->
        <sqlMapGenerator targetPackage="." targetProject="src/main/resources/mapper"/>

        <!--
            <javaClientGenerator/> entire document: https://mybatis.org/generator/configreference/javaClientGenerator.html
            Java code mapper interface file will be generated at ${targetProject}/${targetPackage}

            javaClientGenerator.type (context.targetRuntime is MyBatis3):
                This attribute indicated Mybatis how to implement interface.
                It has ANNOTATEDMAPPER / MIXEDMAPPER / XMLMAPPER 3 selection to choice.
        -->
        <javaClientGenerator type="XMLMAPPER" targetPackage="com.pingcap.model" targetProject="src/main/java"/>

        <!--
            <table/> entire document: https://mybatis.org/generator/configreference/table.html

            table.tableName: The name of the database table.
            table.domainObjectName: The base name from which generated object names will be generated. If not specified, MBG will generate a name automatically based on the tableName.
            table.enableCountByExample: Signifies whether a count by example statement should be generated.
            table.enableUpdateByExample: Signifies whether an update by example statement should be generated.
            table.enableDeleteByExample: Signifies whether a delete by example statement should be generated.
            table.enableSelectByExample: Signifies whether a select by example statement should be generated.
            table.selectByExampleQueryId: This value will be added to the select list of the select by example statement in this form: "'<value>' as QUERYID".
        -->
        <table tableName="player" domainObjectName="Player"
               enableCountByExample="false" enableUpdateByExample="false"
               enableDeleteByExample="false" enableSelectByExample="false"
               selectByExampleQueryId="false"/>
    </context>
</generatorConfiguration>
```

`mybatis-generator.xml` 在 `pom.xml` 中，以 `mybatis-generator-maven-plugin` 插件配置的方式被引入：

```xml
<plugin>
    <groupId>org.mybatis.generator</groupId>
    <artifactId>mybatis-generator-maven-plugin</artifactId>
    <version>1.4.1</version>
    <configuration>
        <configurationFile>src/main/resources/mybatis-generator.xml</configurationFile>
        <verbose>true</verbose>
        <overwrite>true</overwrite>
    </configuration>

    <dependencies>
        <!-- https://mvnrepository.com/artifact/mysql/mysql-connector-java -->
        <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-java</artifactId>
        <version>5.1.49</version>
        </dependency>
    </dependencies>
</plugin>
```

在 Maven 插件内引入后，可删除旧的生成文件后，通过命令 `mvn mybatis-generate` 生成新的文件。或者你也可以使用已经编写好的 `make` 命令，通过 `make gen` 来同时删除旧文件，并生成新文件。

> **注意：**
>
> `mybatis-generator.xml` 中的属性 `configuration.overwrite` 仅可控制新生成的 Java 代码文件使用覆盖方式被写入，但 XML 映射文件仍会以追加方式写入。因此，推荐在 Mybaits Generator 生成新的文件前，先删除掉旧的文件。

`Player.java` 是使用 Mybatis Generator 生成出的数据实体类文件，为数据库表在程序内的映射。`Player` 类的每个属性都对应着 `player` 表的一个字段。



```java
package com.pingcap.model;

public class Player {
    private String id;

    private Integer coins;

    private Integer goods;

    public Player(String id, Integer coins, Integer goods) {
        this.id = id;
        this.coins = coins;
        this.goods = goods;
    }

    public Player() {
        super();
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public Integer getCoins() {
        return coins;
    }

    public void setCoins(Integer coins) {
        this.coins = coins;
    }

    public Integer getGoods() {
        return goods;
    }

    public void setGoods(Integer goods) {
        this.goods = goods;
    }
}
```

`PlayerMapper.java` 是使用 Mybatis Generator 生成出的映射接口文件，它仅规定了接口，接口的实现类是由 Mybatis 来通过 XML 或注解自动生成的：



```java
package com.pingcap.model;

import com.pingcap.model.Player;

public interface PlayerMapper {
    int deleteByPrimaryKey(String id);

    int insert(Player row);

    int insertSelective(Player row);

    Player selectByPrimaryKey(String id);

    int updateByPrimaryKeySelective(Player row);

    int updateByPrimaryKey(Player row);
}
```

`PlayerMapper.xml` 是使用 Mybatis Generator 生成出的映射 XML 文件，Mybatis 将使用这个文件自动生成 `PlayerMapper` 接口的实现类：



```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.pingcap.model.PlayerMapper">
  <resultMap id="BaseResultMap" type="com.pingcap.model.Player">
    <constructor>
      <idArg column="id" javaType="java.lang.String" jdbcType="VARCHAR" />
      <arg column="coins" javaType="java.lang.Integer" jdbcType="INTEGER" />
      <arg column="goods" javaType="java.lang.Integer" jdbcType="INTEGER" />
    </constructor>
  </resultMap>
  <sql id="Base_Column_List">
    id, coins, goods
  </sql>
  <select id="selectByPrimaryKey" parameterType="java.lang.String" resultMap="BaseResultMap">
    select 
    <include refid="Base_Column_List" />
    from player
    where id = #{id,jdbcType=VARCHAR}
  </select>
  <delete id="deleteByPrimaryKey" parameterType="java.lang.String">
    delete from player
    where id = #{id,jdbcType=VARCHAR}
  </delete>
  <insert id="insert" parameterType="com.pingcap.model.Player">
    insert into player (id, coins, goods
      )
    values (#{id,jdbcType=VARCHAR}, #{coins,jdbcType=INTEGER}, #{goods,jdbcType=INTEGER}
      )
  </insert>
  <insert id="insertSelective" parameterType="com.pingcap.model.Player">
    insert into player
    <trim prefix="(" suffix=")" suffixOverrides=",">
      <if test="id != null">
        id,
      </if>
      <if test="coins != null">
        coins,
      </if>
      <if test="goods != null">
        goods,
      </if>
    </trim>
    <trim prefix="values (" suffix=")" suffixOverrides=",">
      <if test="id != null">
        #{id,jdbcType=VARCHAR},
      </if>
      <if test="coins != null">
        #{coins,jdbcType=INTEGER},
      </if>
      <if test="goods != null">
        #{goods,jdbcType=INTEGER},
      </if>
    </trim>
  </insert>
  <update id="updateByPrimaryKeySelective" parameterType="com.pingcap.model.Player">
    update player
    <set>
      <if test="coins != null">
        coins = #{coins,jdbcType=INTEGER},
      </if>
      <if test="goods != null">
        goods = #{goods,jdbcType=INTEGER},
      </if>
    </set>
    where id = #{id,jdbcType=VARCHAR}
  </update>
  <update id="updateByPrimaryKey" parameterType="com.pingcap.model.Player">
    update player
    set coins = #{coins,jdbcType=INTEGER},
      goods = #{goods,jdbcType=INTEGER}
    where id = #{id,jdbcType=VARCHAR}
  </update>
</mapper>
```

由于 Mybatis Generator 需要逆向生成源码，因此，数据库中需先行有此表结构，可使用 `dbinit.sql` 生成表结构：



```sql
USE test;
DROP TABLE IF EXISTS player;

CREATE TABLE player (
    `id` VARCHAR(36),
    `coins` INTEGER,
    `goods` INTEGER,
    PRIMARY KEY (`id`)
);
```

额外拆分接口 `PlayerMapperEx` 继承 `PlayerMapper`，并且编写与之匹配的 `PlayerMapperEx.xml`。避免直接更改 `PlayerMapper.java` 和 `PlayerMapper.xml`。这是为了规避 Mybatis Generator 的反复生成，影响到自行编写的代码。

在 `PlayerMapperEx.java` 中定义自行增加的接口：



```java
package com.pingcap.model;

import java.util.List;

public interface PlayerMapperEx extends PlayerMapper {
    Player selectByPrimaryKeyWithLock(String id);

    List<Player> selectByLimit(Integer limit);

    Integer count();
}
```

在 `PlayerMapperEx.xml` 中定义映射规则：



```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.pingcap.model.PlayerMapperEx">
  <resultMap id="BaseResultMap" type="com.pingcap.model.Player">
    <constructor>
      <idArg column="id" javaType="java.lang.String" jdbcType="VARCHAR" />
      <arg column="coins" javaType="java.lang.Integer" jdbcType="INTEGER" />
      <arg column="goods" javaType="java.lang.Integer" jdbcType="INTEGER" />
    </constructor>
  </resultMap>
  <sql id="Base_Column_List">
    id, coins, goods
  </sql>

  <select id="selectByPrimaryKeyWithLock" parameterType="java.lang.String" resultMap="BaseResultMap">
    select 
    <include refid="Base_Column_List" />
    from player
    where `id` = #{id,jdbcType=VARCHAR}
    for update
  </select>

  <select id="selectByLimit" parameterType="java.lang.Integer" resultMap="BaseResultMap">
    select
    <include refid="Base_Column_List" />
    from player
    limit #{id,jdbcType=INTEGER}
  </select>

  <select id="count" resultType="java.lang.Integer">
    select count(*) from player
  </select>

</mapper>
```

`PlayerDAO.java` 是程序用来管理数据对象的类。其中 `DAO` 是 [Data Access Object](https://en.wikipedia.org/wiki/Data_access_object) 的缩写。在其中定义了一系列数据的操作方法，用于数据的写入。



```java
package com.pingcap.dao;

import com.pingcap.model.Player;
import com.pingcap.model.PlayerMapperEx;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;

import java.util.List;
import java.util.function.Function;

public class PlayerDAO {
    public static class NotEnoughException extends RuntimeException {
        public NotEnoughException(String message) {
            super(message);
        }
    }

    // Run SQL code in a way that automatically handles the
    // transaction retry logic, so we don't have to duplicate it in
    // various places.
    public Object runTransaction(SqlSessionFactory sessionFactory, Function<PlayerMapperEx, Object> fn) {
        Object resultObject = null;
        SqlSession session = null;

        try {
            // open a session with autoCommit is false
            session = sessionFactory.openSession(false);

            // get player mapper
            PlayerMapperEx playerMapperEx = session.getMapper(PlayerMapperEx.class);

            resultObject = fn.apply(playerMapperEx);
            session.commit();
            System.out.println("APP: COMMIT;");
        } catch (Exception e) {
            if (e instanceof NotEnoughException) {
                System.out.printf("APP: ROLLBACK BY LOGIC; \n%s\n", e.getMessage());
            } else {
                System.out.printf("APP: ROLLBACK BY ERROR; \n%s\n", e.getMessage());
            }

            if (session != null) {
                session.rollback();
            }
        } finally {
            if (session != null) {
                session.close();
            }
        }

        return resultObject;
    }

    public Function<PlayerMapperEx, Object> createPlayers(List<Player> players) {
        return playerMapperEx -> {
            Integer addedPlayerAmount = 0;
            for (Player player: players) {
                playerMapperEx.insert(player);
                addedPlayerAmount ++;
            }
            System.out.printf("APP: createPlayers() --> %d\n", addedPlayerAmount);
            return addedPlayerAmount;
        };
    }

    public Function<PlayerMapperEx, Object> buyGoods(String sellId, String buyId, Integer amount, Integer price) {
        return playerMapperEx -> {
            Player sellPlayer = playerMapperEx.selectByPrimaryKeyWithLock(sellId);
            Player buyPlayer = playerMapperEx.selectByPrimaryKeyWithLock(buyId);

            if (buyPlayer == null || sellPlayer == null) {
                throw new NotEnoughException("sell or buy player not exist");
            }

            if (buyPlayer.getCoins() < price || sellPlayer.getGoods() < amount) {
                throw new NotEnoughException("coins or goods not enough, rollback");
            }

            int affectRows = 0;
            buyPlayer.setGoods(buyPlayer.getGoods() + amount);
            buyPlayer.setCoins(buyPlayer.getCoins() - price);
            affectRows += playerMapperEx.updateByPrimaryKey(buyPlayer);

            sellPlayer.setGoods(sellPlayer.getGoods() - amount);
            sellPlayer.setCoins(sellPlayer.getCoins() + price);
            affectRows += playerMapperEx.updateByPrimaryKey(sellPlayer);

            System.out.printf("APP: buyGoods --> sell: %s, buy: %s, amount: %d, price: %d\n", sellId, buyId, amount, price);
            return affectRows;
        };
    }

    public Function<PlayerMapperEx, Object> getPlayerByID(String id) {
        return playerMapperEx -> playerMapperEx.selectByPrimaryKey(id);
    }

    public Function<PlayerMapperEx, Object> printPlayers(Integer limit) {
        return playerMapperEx -> {
            List<Player> players = playerMapperEx.selectByLimit(limit);

            for (Player player: players) {
                System.out.println("\n[printPlayers]:\n" + player);
            }
            return 0;
        };
    }

    public Function<PlayerMapperEx, Object> countPlayers() {
        return PlayerMapperEx::count;
    }
}
```

`MybatisExample` 是 `plain-java-mybatis` 这个示例程序的主类。其中定义了入口函数：

```java
package com.pingcap;

import com.pingcap.dao.PlayerDAO;
import com.pingcap.model.Player;
import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;

import java.io.IOException;
import java.io.InputStream;
import java.util.Arrays;
import java.util.Collections;

public class MybatisExample {
    public static void main( String[] args ) throws IOException {
        // 1. Create a SqlSessionFactory based on our mybatis-config.xml configuration
        // file, which defines how to connect to the database.
        InputStream inputStream = Resources.getResourceAsStream("mybatis-config.xml");
        SqlSessionFactory sessionFactory = new SqlSessionFactoryBuilder().build(inputStream);

        // 2. And then, create DAO to manager your data
        PlayerDAO playerDAO = new PlayerDAO();

        // 3. Run some simple examples.

        // Create a player who has 1 coin and 1 goods.
        playerDAO.runTransaction(sessionFactory, playerDAO.createPlayers(
                Collections.singletonList(new Player("test", 1, 1))));

        // Get a player.
        Player testPlayer = (Player)playerDAO.runTransaction(sessionFactory, playerDAO.getPlayerByID("test"));
        System.out.printf("PlayerDAO.getPlayer:\n    => id: %s\n    => coins: %s\n    => goods: %s\n",
                testPlayer.getId(), testPlayer.getCoins(), testPlayer.getGoods());

        // Count players amount.
        Integer count = (Integer)playerDAO.runTransaction(sessionFactory, playerDAO.countPlayers());
        System.out.printf("PlayerDAO.countPlayers:\n    => %d total players\n", count);

        // Print 3 players.
        playerDAO.runTransaction(sessionFactory, playerDAO.printPlayers(3));

        // 4. Getting further.

        // Player 1: id is "1", has only 100 coins.
        // Player 2: id is "2", has 114514 coins, and 20 goods.
        Player player1 = new Player("1", 100, 0);
        Player player2 = new Player("2", 114514, 20);

        // Create two players "by hand", using the INSERT statement on the backend.
        int addedCount = (Integer)playerDAO.runTransaction(sessionFactory,
                playerDAO.createPlayers(Arrays.asList(player1, player2)));
        System.out.printf("PlayerDAO.createPlayers:\n    => %d total inserted players\n", addedCount);

        // Player 1 wants to buy 10 goods from player 2.
        // It will cost 500 coins, but player 1 cannot afford it.
        System.out.println("\nPlayerDAO.buyGoods:\n    => this trade will fail");
        Integer updatedCount = (Integer)playerDAO.runTransaction(sessionFactory,
                playerDAO.buyGoods(player2.getId(), player1.getId(), 10, 500));
        System.out.printf("PlayerDAO.buyGoods:\n    => %d total update players\n", updatedCount);

        // So player 1 has to reduce the incoming quantity to two.
        System.out.println("\nPlayerDAO.buyGoods:\n    => this trade will success");
        updatedCount = (Integer)playerDAO.runTransaction(sessionFactory,
                playerDAO.buyGoods(player2.getId(), player1.getId(), 2, 100));
        System.out.printf("PlayerDAO.buyGoods:\n    => %d total update players\n", updatedCount);
    }
}
```

</div>

<div label="使用 Hibernate（推荐）" value="hibernate">

当前开源比较流行的 Java ORM 为 Hibernate，且 Hibernate 在版本 `6.0.0.Beta2` 及以后支持了 TiDB 方言。完美适配了 TiDB 的特性。因此，此处将以 6.0.0.Beta2 + 版本进行说明。

进入目录 `plain-java-hibernate` ：



```shell
cd plain-java-hibernate
```

目录结构如下所示：

```
.
├── Makefile
├── plain-java-hibernate.iml
├── pom.xml
└── src
    └── main
        ├── java
        │   └── com
        │       └── pingcap
        │           └── HibernateExample.java
        └── resources
            └── hibernate.cfg.xml
```

其中，`hibernate.cfg.xml` 为 Hibernate 配置文件，定义了：



```xml
<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE hibernate-configuration PUBLIC
        "-//Hibernate/Hibernate Configuration DTD 3.0//EN"
        "http://www.hibernate.org/dtd/hibernate-configuration-3.0.dtd">
<hibernate-configuration>
    <session-factory>

        <!-- Database connection settings -->
        <property name="hibernate.connection.driver_class">com.mysql.cj.jdbc.Driver</property>
        <property name="hibernate.dialect">org.hibernate.dialect.TiDBDialect</property>
        <property name="hibernate.connection.url">jdbc:mysql://localhost:4000/test</property>
        <property name="hibernate.connection.username">root</property>
        <property name="hibernate.connection.password"></property>
        <property name="hibernate.connection.autocommit">false</property>

        <!-- Required so a table can be created from the 'PlayerDAO' class -->
        <property name="hibernate.hbm2ddl.auto">create-drop</property>

        <!-- Optional: Show SQL output for debugging -->
        <property name="hibernate.show_sql">true</property>
        <property name="hibernate.format_sql">true</property>
    </session-factory>
</hibernate-configuration>
```

`HibernateExample.java` 是 `plain-java-hibernate` 这个示例程序的主体。使用 Hibernate 时，相较于 JDBC，这里仅需写入配置文件地址，Hibernate 屏蔽了创建数据库连接时，不同数据库差异的细节。

`PlayerDAO` 是程序用来管理数据对象的类。其中 `DAO` 是 [Data Access Object](https://en.wikipedia.org/wiki/Data_access_object) 的缩写。其中定义了一系列数据的操作方法，用来提供数据的写入能力。相较于 JDBC， Hibernate 封装了大量的操作，如对象映射、基本对象的 CRUD 等，极大的简化了代码量。

`PlayerBean` 是数据实体类，为数据库表在程序内的映射。`PlayerBean` 的每个属性都对应着 `player` 表的一个字段。相较于 JDBC，Hibernate 的 `PlayerBean` 实体类为了给 Hibernate 提供更多的信息，加入了注解，用来指示映射关系。



```java
package com.pingcap;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import org.hibernate.JDBCException;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.Transaction;
import org.hibernate.cfg.Configuration;
import org.hibernate.query.NativeQuery;
import org.hibernate.query.Query;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.function.Function;

@Entity
@Table(name = "player_hibernate")
class PlayerBean {
    @Id
    private String id;
    @Column(name = "coins")
    private Integer coins;
    @Column(name = "goods")
    private Integer goods;

    public PlayerBean() {
    }

    public PlayerBean(String id, Integer coins, Integer goods) {
        this.id = id;
        this.coins = coins;
        this.goods = goods;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public Integer getCoins() {
        return coins;
    }

    public void setCoins(Integer coins) {
        this.coins = coins;
    }

    public Integer getGoods() {
        return goods;
    }

    public void setGoods(Integer goods) {
        this.goods = goods;
    }

    @Override
    public String toString() {
        return String.format("    %-8s => %10s\n    %-8s => %10s\n    %-8s => %10s\n",
                "id", this.id, "coins", this.coins, "goods", this.goods);
    }
}

/**
 * Main class for the basic Hibernate example.
 **/
public class HibernateExample
{
    public static class PlayerDAO {
        public static class NotEnoughException extends RuntimeException {
            public NotEnoughException(String message) {
                super(message);
            }
        }

        // Run SQL code in a way that automatically handles the
        // transaction retry logic so we don't have to duplicate it in
        // various places.
        public Object runTransaction(Session session, Function<Session, Object> fn) {
            Object resultObject = null;

            Transaction txn = session.beginTransaction();
            try {
                resultObject = fn.apply(session);
                txn.commit();
                System.out.println("APP: COMMIT;");
            } catch (JDBCException e) {
                System.out.println("APP: ROLLBACK BY JDBC ERROR;");
                txn.rollback();
            } catch (NotEnoughException e) {
                System.out.printf("APP: ROLLBACK BY LOGIC; %s", e.getMessage());
                txn.rollback();
            }
            return resultObject;
        }

        public Function<Session, Object> createPlayers(List<PlayerBean> players) throws JDBCException {
            return session -> {
                Integer addedPlayerAmount = 0;
                for (PlayerBean player: players) {
                    session.persist(player);
                    addedPlayerAmount ++;
                }
                System.out.printf("APP: createPlayers() --> %d\n", addedPlayerAmount);
                return addedPlayerAmount;
            };
        }

        public Function<Session, Object> buyGoods(String sellId, String buyId, Integer amount, Integer price) throws JDBCException {
            return session -> {
                PlayerBean sellPlayer = session.get(PlayerBean.class, sellId);
                PlayerBean buyPlayer = session.get(PlayerBean.class, buyId);

                if (buyPlayer == null || sellPlayer == null) {
                    throw new NotEnoughException("sell or buy player not exist");
                }

                if (buyPlayer.getCoins() < price || sellPlayer.getGoods() < amount) {
                    throw new NotEnoughException("coins or goods not enough, rollback");
                }

                buyPlayer.setGoods(buyPlayer.getGoods() + amount);
                buyPlayer.setCoins(buyPlayer.getCoins() - price);
                session.persist(buyPlayer);

                sellPlayer.setGoods(sellPlayer.getGoods() - amount);
                sellPlayer.setCoins(sellPlayer.getCoins() + price);
                session.persist(sellPlayer);

                System.out.printf("APP: buyGoods --> sell: %s, buy: %s, amount: %d, price: %d\n", sellId, buyId, amount, price);
                return 0;
            };
        }

        public Function<Session, Object> getPlayerByID(String id) throws JDBCException {
            return session -> session.get(PlayerBean.class, id);
        }

        public Function<Session, Object> printPlayers(Integer limit) throws JDBCException {
            return session -> {
                NativeQuery<PlayerBean> limitQuery = session.createNativeQuery("SELECT * FROM player_hibernate LIMIT :limit", PlayerBean.class);
                limitQuery.setParameter("limit", limit);
                List<PlayerBean> players = limitQuery.getResultList();

                for (PlayerBean player: players) {
                    System.out.println("\n[printPlayers]:\n" + player);
                }
                return 0;
            };
        }

        public Function<Session, Object> countPlayers() throws JDBCException {
            return session -> {
                Query<Long> countQuery = session.createQuery("SELECT count(player_hibernate) FROM PlayerBean player_hibernate", Long.class);
                return countQuery.getSingleResult();
            };
        }
    }

    public static void main(String[] args) {
        // 1. Create a SessionFactory based on our hibernate.cfg.xml configuration
        // file, which defines how to connect to the database.
        SessionFactory sessionFactory
                = new Configuration()
                .configure("hibernate.cfg.xml")
                .addAnnotatedClass(PlayerBean.class)
                .buildSessionFactory();

        try (Session session = sessionFactory.openSession()) {
            // 2. And then, create DAO to manager your data.
            PlayerDAO playerDAO = new PlayerDAO();

            // 3. Run some simple examples.

            // Create a player who has 1 coin and 1 goods.
            playerDAO.runTransaction(session, playerDAO.createPlayers(Collections.singletonList(
                    new PlayerBean("test", 1, 1))));

            // Get a player.
            PlayerBean testPlayer = (PlayerBean)playerDAO.runTransaction(session, playerDAO.getPlayerByID("test"));
            System.out.printf("PlayerDAO.getPlayer:\n    => id: %s\n    => coins: %s\n    => goods: %s\n",
                    testPlayer.getId(), testPlayer.getCoins(), testPlayer.getGoods());

            // Count players amount.
            Long count = (Long)playerDAO.runTransaction(session, playerDAO.countPlayers());
            System.out.printf("PlayerDAO.countPlayers:\n    => %d total players\n", count);

            // Print 3 players.
            playerDAO.runTransaction(session, playerDAO.printPlayers(3));

            // 4. Explore more.

            // Player 1: id is "1", has only 100 coins.
            // Player 2: id is "2", has 114514 coins, and 20 goods.
            PlayerBean player1 = new PlayerBean("1", 100, 0);
            PlayerBean player2 = new PlayerBean("2", 114514, 20);

            // Create two players "by hand", using the INSERT statement on the backend.
            int addedCount = (Integer)playerDAO.runTransaction(session,
                    playerDAO.createPlayers(Arrays.asList(player1, player2)));
            System.out.printf("PlayerDAO.createPlayers:\n    => %d total inserted players\n", addedCount);

            // Player 1 wants to buy 10 goods from player 2.
            // It will cost 500 coins, but player 1 cannot afford it.
            System.out.println("\nPlayerDAO.buyGoods:\n    => this trade will fail");
            Integer updatedCount = (Integer)playerDAO.runTransaction(session,
                    playerDAO.buyGoods(player2.getId(), player1.getId(), 10, 500));
            System.out.printf("PlayerDAO.buyGoods:\n    => %d total update players\n", updatedCount);

            // So player 1 has to reduce the incoming quantity to two.
            System.out.println("\nPlayerDAO.buyGoods:\n    => this trade will success");
            updatedCount = (Integer)playerDAO.runTransaction(session,
                    playerDAO.buyGoods(player2.getId(), player1.getId(), 2, 100));
            System.out.printf("PlayerDAO.buyGoods:\n    => %d total update players\n", updatedCount);
        } finally {
            sessionFactory.close();
        }
    }
}
```

</div>

<div label="使用 JDBC" value="jdbc">

进入目录 `plain-java-jdbc`：



```shell
cd plain-java-jdbc
```

目录结构如下所示：

```
.
├── Makefile
├── plain-java-jdbc.iml
├── pom.xml
└── src
    └── main
        ├── java
        │   └── com
        │       └── pingcap
        │            └── JDBCExample.java
        └── resources
            └── dbinit.sql
```

其中，`dbinit.sql` 为数据表初始化语句：



```sql
USE test;
DROP TABLE IF EXISTS player;

CREATE TABLE player (
    `id` VARCHAR(36),
    `coins` INTEGER,
    `goods` INTEGER,
   PRIMARY KEY (`id`)
);
```

`JDBCExample.java` 是 `plain-java-jdbc` 这个示例程序的主体。因为 TiDB 与 MySQL 协议兼容，因此，需要初始化一个 MySQL 协议的数据源 `MysqlDataSource`，以此连接到 TiDB。并在其后，初始化 `PlayerDAO`，用来管理数据对象，进行增删改查等操作。

`PlayerDAO` 是程序用来管理数据对象的类。其中 `DAO` 是 [Data Access Object](https://en.wikipedia.org/wiki/Data_access_object) 的缩写。在其中定义了一系列数据的操作方法，用来对提供数据的写入能力。

`PlayerBean` 是数据实体类，为数据库表在程序内的映射。`PlayerBean` 的每个属性都对应着 `player` 表的一个字段。



```java
package com.pingcap;

import com.mysql.cj.jdbc.MysqlDataSource;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.*;

/**
 * Main class for the basic JDBC example.
 **/
public class JDBCExample
{
    public static class PlayerBean {
        private String id;
        private Integer coins;
        private Integer goods;

        public PlayerBean() {
        }

        public PlayerBean(String id, Integer coins, Integer goods) {
            this.id = id;
            this.coins = coins;
            this.goods = goods;
        }

        public String getId() {
            return id;
        }

        public void setId(String id) {
            this.id = id;
        }

        public Integer getCoins() {
            return coins;
        }

        public void setCoins(Integer coins) {
            this.coins = coins;
        }

        public Integer getGoods() {
            return goods;
        }

        public void setGoods(Integer goods) {
            this.goods = goods;
        }

        @Override
        public String toString() {
            return String.format("    %-8s => %10s\n    %-8s => %10s\n    %-8s => %10s\n",
                    "id", this.id, "coins", this.coins, "goods", this.goods);
        }
    }

    /**
     * Data access object used by 'ExampleDataSource'.
     * Example for CURD and bulk insert.
     */
    public static class PlayerDAO {
        private final MysqlDataSource ds;
        private final Random rand = new Random();

        PlayerDAO(MysqlDataSource ds) {
            this.ds = ds;
        }

        /**
         * Create players by passing in a List of PlayerBean.
         *
         * @param players Will create players list
         * @return The number of create accounts
         */
        public int createPlayers(List<PlayerBean> players){
            int rows = 0;

            Connection connection = null;
            PreparedStatement preparedStatement = null;
            try {
                connection = ds.getConnection();
                preparedStatement = connection.prepareStatement("INSERT INTO player (id, coins, goods) VALUES (?, ?, ?)");
            } catch (SQLException e) {
                System.out.printf("[createPlayers] ERROR: { state => %s, cause => %s, message => %s }\n",
                        e.getSQLState(), e.getCause(), e.getMessage());
                e.printStackTrace();

                return -1;
            }

            try {
                for (PlayerBean player : players) {
                    preparedStatement.setString(1, player.getId());
                    preparedStatement.setInt(2, player.getCoins());
                    preparedStatement.setInt(3, player.getGoods());

                    preparedStatement.execute();
                    rows += preparedStatement.getUpdateCount();
                }
            } catch (SQLException e) {
                System.out.printf("[createPlayers] ERROR: { state => %s, cause => %s, message => %s }\n",
                        e.getSQLState(), e.getCause(), e.getMessage());
                e.printStackTrace();
            } finally {
                try {
                    connection.close();
                } catch (SQLException e) {
                    e.printStackTrace();
                }
            }

            System.out.printf("\n[createPlayers]:\n    '%s'\n", preparedStatement);
            return rows;
        }

        /**
         * Buy goods and transfer funds between one player and another in one transaction.
         * @param sellId Sell player id.
         * @param buyId Buy player id.
         * @param amount Goods amount, if sell player has not enough goods, the trade will break.
         * @param price Price should pay, if buy player has not enough coins, the trade will break.
         *
         * @return The number of effected players.
         */
        public int buyGoods(String sellId, String buyId, Integer amount, Integer price) {
            int effectPlayers = 0;

            Connection connection = null;
            try {
                connection = ds.getConnection();
            } catch (SQLException e) {
                System.out.printf("[buyGoods] ERROR: { state => %s, cause => %s, message => %s }\n",
                        e.getSQLState(), e.getCause(), e.getMessage());
                e.printStackTrace();
                return effectPlayers;
            }

            try {
                connection.setAutoCommit(false);

                PreparedStatement playerQuery = connection.prepareStatement("SELECT * FROM player WHERE id=? OR id=? FOR UPDATE");
                playerQuery.setString(1, sellId);
                playerQuery.setString(2, buyId);
                playerQuery.execute();

                PlayerBean sellPlayer = null;
                PlayerBean buyPlayer = null;

                ResultSet playerQueryResultSet = playerQuery.getResultSet();
                while (playerQueryResultSet.next()) {
                    PlayerBean player =  new PlayerBean(
                            playerQueryResultSet.getString("id"),
                            playerQueryResultSet.getInt("coins"),
                            playerQueryResultSet.getInt("goods")
                    );

                    System.out.println("\n[buyGoods]:\n    'check goods and coins enough'");
                    System.out.println(player);

                    if (sellId.equals(player.getId())) {
                        sellPlayer = player;
                    } else {
                        buyPlayer = player;
                    }
                }

                if (sellPlayer == null || buyPlayer == null) {
                    throw new SQLException("player not exist.");
                }

                if (sellPlayer.getGoods().compareTo(amount) < 0) {
                    throw new SQLException(String.format("sell player %s goods not enough.", sellId));
                }

                if (buyPlayer.getCoins().compareTo(price) < 0) {
                    throw new SQLException(String.format("buy player %s coins not enough.", buyId));
                }

                PreparedStatement transfer = connection.prepareStatement("UPDATE player set goods = goods + ?, coins = coins + ? WHERE id=?");
                transfer.setInt(1, -amount);
                transfer.setInt(2, price);
                transfer.setString(3, sellId);
                transfer.execute();
                effectPlayers += transfer.getUpdateCount();

                transfer.setInt(1, amount);
                transfer.setInt(2, -price);
                transfer.setString(3, buyId);
                transfer.execute();
                effectPlayers += transfer.getUpdateCount();

                connection.commit();

                System.out.println("\n[buyGoods]:\n    'trade success'");
            } catch (SQLException e) {
                System.out.printf("[buyGoods] ERROR: { state => %s, cause => %s, message => %s }\n",
                        e.getSQLState(), e.getCause(), e.getMessage());

                try {
                    System.out.println("[buyGoods] Rollback");

                    connection.rollback();
                } catch (SQLException ex) {
                    // do nothing
                }
            } finally {
                try {
                    connection.close();
                } catch (SQLException e) {
                    // do nothing
                }
            }

            return effectPlayers;
        }

        /**
         * Get the player info by id.
         *
         * @param id Player id.
         * @return The player of this id.
         */
        public PlayerBean getPlayer(String id) {
            PlayerBean player = null;

            try (Connection connection = ds.getConnection()) {
                PreparedStatement preparedStatement = connection.prepareStatement("SELECT * FROM player WHERE id = ?");
                preparedStatement.setString(1, id);
                preparedStatement.execute();

                ResultSet res = preparedStatement.executeQuery();
                if(!res.next()) {
                    System.out.printf("No players in the table with id %s", id);
                } else {
                    player = new PlayerBean(res.getString("id"), res.getInt("coins"), res.getInt("goods"));
                }
            } catch (SQLException e) {
                System.out.printf("PlayerDAO.getPlayer ERROR: { state => %s, cause => %s, message => %s }\n",
                        e.getSQLState(), e.getCause(), e.getMessage());
            }

            return player;
        }

        /**
         * Insert randomized account data (id, coins, goods) using the JDBC fast path for
         * bulk inserts.  The fastest way to get data into TiDB is using the
         * TiDB Lightning(https://docs.pingcap.com/tidb/stable/tidb-lightning-overview).
         * However, if you must bulk insert from the application using INSERT SQL, the best
         * option is the method shown here. It will require the following:
         *
         *    Add `rewriteBatchedStatements=true` to your JDBC connection settings.
         *    Setting rewriteBatchedStatements to true now causes CallableStatements
         *    with batched arguments to be re-written in the form "CALL (...); CALL (...); ..."
         *    to send the batch in as few client/server round trips as possible.
         *    https://dev.mysql.com/doc/relnotes/connector-j/5.1/en/news-5-1-3.html
         *
         *    You can see the `rewriteBatchedStatements` param effect logic at
         *    implement function: `com.mysql.cj.jdbc.StatementImpl.executeBatchUsingMultiQueries`
         *
         * @param total Add players amount.
         * @param batchSize Bulk insert size for per batch.
         *
         * @return The number of new accounts inserted.
         */
        public int bulkInsertRandomPlayers(Integer total, Integer batchSize) {
            int totalNewPlayers = 0;

            try (Connection connection = ds.getConnection()) {
                // We're managing the commit lifecycle ourselves, so we can
                // control the size of our batch inserts.
                connection.setAutoCommit(false);

                // In this example we are adding 500 rows to the database,
                // but it could be any number.  What's important is that
                // the batch size is 128.
                try (PreparedStatement pstmt = connection.prepareStatement("INSERT INTO player (id, coins, goods) VALUES (?, ?, ?)")) {
                    for (int i=0; i<=(total/batchSize);i++) {
                        for (int j=0; j<batchSize; j++) {
                            String id = UUID.randomUUID().toString();
                            pstmt.setString(1, id);
                            pstmt.setInt(2, rand.nextInt(10000));
                            pstmt.setInt(3, rand.nextInt(10000));
                            pstmt.addBatch();
                        }

                        int[] count = pstmt.executeBatch();
                        totalNewPlayers += count.length;
                        System.out.printf("\nPlayerDAO.bulkInsertRandomPlayers:\n    '%s'\n", pstmt);
                        System.out.printf("    => %s row(s) updated in this batch\n", count.length);
                    }
                    connection.commit();
                } catch (SQLException e) {
                    System.out.printf("PlayerDAO.bulkInsertRandomPlayers ERROR: { state => %s, cause => %s, message => %s }\n",
                            e.getSQLState(), e.getCause(), e.getMessage());
                }
            } catch (SQLException e) {
                System.out.printf("PlayerDAO.bulkInsertRandomPlayers ERROR: { state => %s, cause => %s, message => %s }\n",
                        e.getSQLState(), e.getCause(), e.getMessage());
            }
            return totalNewPlayers;
        }


        /**
         * Print a subset of players from the data store by limit.
         *
         * @param limit Print max size.
         */
        public void printPlayers(Integer limit) {
            try (Connection connection = ds.getConnection()) {
                PreparedStatement preparedStatement = connection.prepareStatement("SELECT * FROM player LIMIT ?");
                preparedStatement.setInt(1, limit);
                preparedStatement.execute();

                ResultSet res = preparedStatement.executeQuery();
                while (!res.next()) {
                    PlayerBean player = new PlayerBean(res.getString("id"),
                            res.getInt("coins"), res.getInt("goods"));
                    System.out.println("\n[printPlayers]:\n" + player);
                }
            } catch (SQLException e) {
                System.out.printf("PlayerDAO.printPlayers ERROR: { state => %s, cause => %s, message => %s }\n",
                        e.getSQLState(), e.getCause(), e.getMessage());
            }
        }


        /**
         * Count players from the data store.
         *
         * @return All players count
         */
        public int countPlayers() {
            int count = 0;

            try (Connection connection = ds.getConnection()) {
                PreparedStatement preparedStatement = connection.prepareStatement("SELECT count(*) FROM player");
                preparedStatement.execute();

                ResultSet res = preparedStatement.executeQuery();
                if(res.next()) {
                    count = res.getInt(1);
                }
            } catch (SQLException e) {
                System.out.printf("PlayerDAO.countPlayers ERROR: { state => %s, cause => %s, message => %s }\n",
                        e.getSQLState(), e.getCause(), e.getMessage());
            }

            return count;
        }
    }

    public static void main(String[] args) {
        // 1. Configure the example database connection.

        // 1.1 Create a mysql data source instance.
        MysqlDataSource mysqlDataSource = new MysqlDataSource();

        // 1.2 Set server name, port, database name, username and password.
        mysqlDataSource.setServerName("localhost");
        mysqlDataSource.setPortNumber(4000);
        mysqlDataSource.setDatabaseName("test");
        mysqlDataSource.setUser("root");
        mysqlDataSource.setPassword("");

        // Or you can use jdbc string instead.
        // mysqlDataSource.setURL("jdbc:mysql://{host}:{port}/test?user={user}&password={password}");

        // 2. And then, create DAO to manager your data.
        PlayerDAO dao = new PlayerDAO(mysqlDataSource);

        // 3. Run some simple examples.

        // Create a player, who has a coin and a goods..
        dao.createPlayers(Collections.singletonList(new PlayerBean("test", 1, 1)));

        // Get a player.
        PlayerBean testPlayer = dao.getPlayer("test");
        System.out.printf("PlayerDAO.getPlayer:\n    => id: %s\n    => coins: %s\n    => goods: %s\n",
                testPlayer.getId(), testPlayer.getCoins(), testPlayer.getGoods());

        // Create players with bulk inserts. Insert 1919 players totally, with 114 players per batch.
        int addedCount = dao.bulkInsertRandomPlayers(1919, 114);
        System.out.printf("PlayerDAO.bulkInsertRandomPlayers:\n    => %d total inserted players\n", addedCount);

        // Count players amount.
        int count = dao.countPlayers();
        System.out.printf("PlayerDAO.countPlayers:\n    => %d total players\n", count);

        // Print 3 players.
        dao.printPlayers(3);

        // 4. Explore more.

        // Player 1: id is "1", has only 100 coins.
        // Player 2: id is "2", has 114514 coins, and 20 goods.
        PlayerBean player1 = new PlayerBean("1", 100, 0);
        PlayerBean player2 = new PlayerBean("2", 114514, 20);

        // Create two players "by hand", using the INSERT statement on the backend.
        addedCount = dao.createPlayers(Arrays.asList(player1, player2));
        System.out.printf("PlayerDAO.createPlayers:\n    => %d total inserted players\n", addedCount);

        // Player 1 wants to buy 10 goods from player 2.
        // It will cost 500 coins, but player 1 cannot afford it.
        System.out.println("\nPlayerDAO.buyGoods:\n    => this trade will fail");
        int updatedCount = dao.buyGoods(player2.getId(), player1.getId(), 10, 500);
        System.out.printf("PlayerDAO.buyGoods:\n    => %d total update players\n", updatedCount);

        // So player 1 has to reduce the incoming quantity to two.
        System.out.println("\nPlayerDAO.buyGoods:\n    => this trade will success");
        updatedCount = dao.buyGoods(player2.getId(), player1.getId(), 2, 100);
        System.out.printf("PlayerDAO.buyGoods:\n    => %d total update players\n", updatedCount);
    }
}
```

</div>

</SimpleTab>

### 第 3 步：运行代码

本节将逐步介绍代码的运行方法。

#### 第 3 步第 1 部分：JDBC 表初始化

<SimpleTab groupId="language">

<div label="使用 Mybatis（推荐）" value="mybatis">

> **建议：**
>
> 在 Gitpod Playground 中尝试 Mybatis：[现在就试试](https://gitpod.io/#targetMode=plain-java-mybatis/https://github.com/pingcap-inc/tidb-example-java)

使用 Mybatis 时，需手动初始化数据库表。若你本地已经安装了 `mysql-client`，且使用本地集群，可直接在 `plain-java-mybatis` 目录下通过 `make prepare` 运行：



```shell
make prepare
```

或直接执行：



```shell
mysql --host 127.0.0.1 --port 4000 -u root < src/main/resources/dbinit.sql
```

若你不使用本地集群，或未安装 `mysql-client`，请直接登录你的集群，并运行 `src/main/resources/dbinit.sql` 文件内的 SQL 语句。

</div>

<div label="使用 Hibernate（推荐）" value="hibernate">

> **建议：**
>
> 在 Gitpod Playground 中尝试 Hibernate：[现在就试试](https://gitpod.io/#targetMode=plain-java-jdbc/https://github.com/pingcap-inc/tidb-example-java)

无需手动初始化表。

</div>

<div label="使用 JDBC" value="jdbc">

> **建议：**
>
> 在 Gitpod Playground 中尝试 JDBC：[现在就试试](https://gitpod.io/#targetMode=plain-java-jdbc/https://github.com/pingcap-inc/tidb-example-java)

使用 JDBC 时，需手动初始化数据库表，若你本地已经安装了 `mysql-client`，且使用本地集群，可直接在 `plain-java-jdbc` 目录下运行：



```shell
make mysql
```

或直接执行：



```shell
mysql --host 127.0.0.1 --port 4000 -u root<src/main/resources/dbinit.sql
```

若你不使用本地集群，或未安装 **mysql-client**，请直接登录你的集群，并运行 `src/main/resources/dbinit.sql` 文件内的 SQL 语句。

</div>

</SimpleTab>

#### 第 3 步第 2 部分：TiDB Cloud 更改参数

<SimpleTab groupId="language">

<div label="使用 Mybatis（推荐）" value="mybatis">

若你使用 TiDB Cloud Serverless Tier 集群，更改 `mybatis-config.xml` 内关于 `dataSource.url`、`dataSource.username`、`dataSource.password` 的参数：



```xml
<?xml version="1.0" encoding="UTF-8" ?>

<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">

<configuration>
    <settings>
        <setting name="cacheEnabled" value="true"/>
        <setting name="lazyLoadingEnabled" value="false"/>
        <setting name="aggressiveLazyLoading" value="true"/>
        <setting name="logImpl" value="LOG4J"/>
    </settings>

    <typeAliases>
        <package name="com.pingcap.dao"/>
    </typeAliases>

    <environments default="development">
        <environment id="development">
            <!-- JDBC transaction manager -->
            <transactionManager type="JDBC"/>
            <!-- Database pool -->
            <dataSource type="POOLED">
                <property name="driver" value="com.mysql.jdbc.Driver"/>
                <property name="url" value="jdbc:mysql://127.0.0.1:4000/test"/>
                <property name="username" value="root"/>
                <property name="password" value=""/>
            </dataSource>
        </environment>
    </environments>

    <mappers>
        <mapper resource="mapper/PlayerMapper.xml"/>
        <mapper resource="mapper/PlayerMapperEx.xml"/>
    </mappers>

</configuration>
```

若你设定的密码为 `123456`，而且从 TiDB Cloud Serverless Tier 集群面板中得到的连接信息为：

- Endpoint: `xxx.tidbcloud.com`
- Port: `4000`
- User: `2aEp24QWEDLqRFs.root`

那么此处应将配置文件中 `dataSource` 节点内更改为：



```xml
<?xml version="1.0" encoding="UTF-8" ?>

<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">

        ...
            <!-- Database pool -->
            <dataSource type="POOLED">
                <property name="driver" value="com.mysql.jdbc.Driver"/>
                <property name="url" value="jdbc:mysql://xxx.tidbcloud.com:4000/test?sslMode=VERIFY_IDENTITY&amp;enabledTLSProtocols=TLSv1.2,TLSv1.3"/>
                <property name="username" value="2aEp24QWEDLqRFs.root"/>
                <property name="password" value="123456"/>
            </dataSource>
        ...

</configuration>
```

</div>

<div label="使用 Hibernate（推荐）" value="hibernate">

若你使用 TiDB Cloud Serverless Tier 集群，更改 `hibernate.cfg.xml` 内关于 `hibernate.connection.url`、`hibernate.connection.username`、`hibernate.connection.password` 的参数：



```xml
<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE hibernate-configuration PUBLIC
        "-//Hibernate/Hibernate Configuration DTD 3.0//EN"
        "http://www.hibernate.org/dtd/hibernate-configuration-3.0.dtd">
<hibernate-configuration>
    <session-factory>

        <!-- Database connection settings -->
        <property name="hibernate.connection.driver_class">com.mysql.cj.jdbc.Driver</property>
        <property name="hibernate.dialect">org.hibernate.dialect.TiDBDialect</property>
        <property name="hibernate.connection.url">jdbc:mysql://localhost:4000/test</property>
        <property name="hibernate.connection.username">root</property>
        <property name="hibernate.connection.password"></property>
        <property name="hibernate.connection.autocommit">false</property>

        <!-- Required so a table can be created from the 'PlayerDAO' class -->
        <property name="hibernate.hbm2ddl.auto">create-drop</property>

        <!-- Optional: Show SQL output for debugging -->
        <property name="hibernate.show_sql">true</property>
        <property name="hibernate.format_sql">true</property>
    </session-factory>
</hibernate-configuration>
```

若你设定的密码为 `123456`，而且从 TiDB Cloud Serverless Tier 集群面板中得到的连接信息为：

- Endpoint: `xxx.tidbcloud.com`
- Port: `4000`
- User: `2aEp24QWEDLqRFs.root`

那么此处应将配置文件更改为：



```xml
<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE hibernate-configuration PUBLIC
        "-//Hibernate/Hibernate Configuration DTD 3.0//EN"
        "http://www.hibernate.org/dtd/hibernate-configuration-3.0.dtd">
<hibernate-configuration>
    <session-factory>

        <!-- Database connection settings -->
        <property name="hibernate.connection.driver_class">com.mysql.cj.jdbc.Driver</property>
        <property name="hibernate.dialect">org.hibernate.dialect.TiDBDialect</property>
        <property name="hibernate.connection.url">jdbc:mysql://xxx.tidbcloud.com:4000/test?sslMode=VERIFY_IDENTITY&amp;enabledTLSProtocols=TLSv1.2,TLSv1.3</property>
        <property name="hibernate.connection.username">2aEp24QWEDLqRFs.root</property>
        <property name="hibernate.connection.password">123456</property>
        <property name="hibernate.connection.autocommit">false</property>

        <!-- Required so a table can be created from the 'PlayerDAO' class -->
        <property name="hibernate.hbm2ddl.auto">create-drop</property>

        <!-- Optional: Show SQL output for debugging -->
        <property name="hibernate.show_sql">true</property>
        <property name="hibernate.format_sql">true</property>
    </session-factory>
</hibernate-configuration>
```

</div>

<div label="使用 JDBC" value="jdbc">

若你使用 TiDB Cloud Serverless Tier 集群，更改 `JDBCExample.java` 内关于 Host、Port、User、Password 的参数：



```java
mysqlDataSource.setServerName("localhost");
mysqlDataSource.setPortNumber(4000);
mysqlDataSource.setDatabaseName("test");
mysqlDataSource.setUser("root");
mysqlDataSource.setPassword("");
```

若你设定的密码为 `123456`，而且从 TiDB Cloud Serverless Tier 集群面板中得到的连接信息为：

- Endpoint: `xxx.tidbcloud.com`
- Port: `4000`
- User: `2aEp24QWEDLqRFs.root`

那么此处应将参数更改为：



```java
mysqlDataSource.setServerName("xxx.tidbcloud.com");
mysqlDataSource.setPortNumber(4000);
mysqlDataSource.setDatabaseName("test");
mysqlDataSource.setUser("2aEp24QWEDLqRFs.root");
mysqlDataSource.setPassword("123456");
mysqlDataSource.setSslMode(PropertyDefinitions.SslMode.VERIFY_IDENTITY.name());
mysqlDataSource.setEnabledTLSProtocols("TLSv1.2,TLSv1.3");
```

</div>

</SimpleTab>

#### 第 3 步第 3 部分：运行

<SimpleTab groupId="language">

<div label="使用 Mybatis（推荐）" value="mybatis">

运行 `make`，这是以下四个操作的组合：

- 创建表 (`make prepare`)：

    

    ```shell
    mysql --host 127.0.0.1 --port 4000 -u root < src/main/resources/dbinit.sql
    mysql --host 127.0.0.1 --port 4000 -u root -e "TRUNCATE test.player"
    ```

- 清理并构建 (`make gen`)：

    

    ```shell
    rm -f src/main/java/com/pingcap/model/Player.java
    rm -f src/main/java/com/pingcap/model/PlayerMapper.java
    rm -f src/main/resources/mapper/PlayerMapper.xml
    mvn mybatis-generator:generate
    ```

- 清理并构建 (`make build`)：`mvn clean package`
- 运行 (`make run`)：`java -jar target/plain-java-mybatis-0.0.1-jar-with-dependencies.jar`

你也可以单独运行这四个 `make` 命令或原生命令。

</div>

<div label="使用 Hibernate（推荐）" value="hibernate">

运行 `make`，这是以下两个操作的组合：

- 清理并构建 (make build)：`mvn clean package`
- 运行 (make run)：`java -jar target/plain-java-hibernate-0.0.1-jar-with-dependencies.jar`

你也可以单独运行这两个 make 命令或原生命令。

</div>

<div label="使用 JDBC" value="jdbc">

运行 `make`，这是以下两个操作的组合：

- 清理并构建 (make build)： `mvn clean package`
- 运行 (make run)： `java -jar target/plain-java-jdbc-0.0.1-jar-with-dependencies.jar`

你也可以单独运行这两个 make 命令或原生命令。

</div>

</SimpleTab>

### 第 4 步：预期输出

<SimpleTab groupId="language">

<div label="使用 Mybatis（推荐）" value="mybatis">

[Mybatis 预期输出](https://github.com/pingcap-inc/tidb-example-java/blob/main/Expected-Output.md#plain-java-mybatis)

</div>

<div label="使用 Hibernate（推荐）" value="hibernate">

[Hibernate 预期输出](https://github.com/pingcap-inc/tidb-example-java/blob/main/Expected-Output.md#plain-java-hibernate)

</div>

<div label="使用 JDBC" value="jdbc">

[JDBC 预期输出](https://github.com/pingcap-inc/tidb-example-java/blob/main/Expected-Output.md#plain-java-jdbc)

</div>

</SimpleTab>

---
title: 使用 Spring Boot 构建 TiDB 应用程序
summary: 给出一个 Spring Boot 构建 TiDB 应用程序示例。
---

<!-- markdownlint-disable MD029 -->

## 使用 Spring Boot 构建 TiDB 应用程序

本教程向你展示如何使用 TiDB 构建 [Spring Boot](https://spring.io/projects/spring-boot) Web 应用程序。使用 [Spring Data JPA](https://spring.io/projects/spring-data-jpa) 模块作为数据访问能力的框架。此示例应用程序的代码仓库可在 [Github](https://github.com/pingcap-inc/tidb-example-java) 下载。

这是一个较为完整的构建 Restful API 的示例应用程序，展示了一个使用 **TiDB** 作为数据库的通用 **Spring Boot** 后端服务。设计了以下过程，用于还原一个现实场景：

这是一个关于游戏的例子，每个玩家有两个属性：金币数 `coins` 和货物数 `goods`。且每个玩家都拥有一个字段 `id`，作为玩家的唯一标识。玩家在金币数和货物数充足的情况下，可以自由的交易。

你可以以此示例为基础，构建自己的应用程序。

> **建议：**
>
> 在[云原生开发环境](#gitpod)中尝试 Spring Boot 构建 TiDB 应用程序。
> 预配置完成的环境，自动启动 TiDB 集群，获取和运行代码，只需要一个链接。
>
> [现在就试试](https://gitpod.io/#targetFile=spring-jpa-hibernate_Makefile,targetMode=spring-jpa-hibernate/https://github.com/pingcap-inc/tidb-example-java)

### 第 1 步：启动你的 TiDB 集群

本节将介绍 TiDB 集群的启动方法。

#### 使用 TiDB Cloud Serverless Tier 集群

[创建 Serverless Tier 集群](#第-1-步创建-serverless-tier-集群)

#### 使用本地集群

此处将简要叙述启动一个测试集群的过程，若需查看正式环境集群部署，或查看更详细的部署内容，请查阅本地启动 TiDB。

**部署本地测试集群**

适用场景：利用本地 macOS 或者单机 Linux 环境快速部署 TiDB 测试集群，体验 TiDB 集群的基本架构，以及 TiDB、TiKV、PD、监控等基础组件的运行

1. 下载并安装 TiUP。

    

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. 声明全局环境变量。

    > **注意：**
    >
    > TiUP 安装完成后会提示对应 profile 文件的绝对路径。在执行以下 source 命令前，需要根据 profile 文件的实际位置修改命令。

    

    ```shell
    source .bash_profile
    ```

3. 在当前 session 执行以下命令启动集群。

    - 直接执行`tiup playground` 命令会运行最新版本的 TiDB 集群，其中 TiDB、TiKV、PD 和 TiFlash 实例各 1 个：

        

        ```shell
        tiup playground
        ```

    - 也可以指定 TiDB 版本以及各组件实例个数，命令类似于：

        

        ```shell
        tiup playground v5.4.0 --db 2 --pd 3 --kv 3
        ```

    上述命令会在本地下载并启动某个版本的集群（例如 v5.4.0）。最新版本可以通过执行`tiup list tidb` 来查看。运行结果将显示集群的访问方式：

    ```
    CLUSTER START SUCCESSFULLY, Enjoy it ^-^
    To connect TiDB: mysql --comments --host 127.0.0.1 --port 4001 -u root -p (no password)
    To connect TiDB: mysql --comments --host 127.0.0.1 --port 4000 -u root -p (no password)
    To view the dashboard: http://127.0.0.1:2379/dashboard
    PD client endpoints: [127.0.0.1:2379 127.0.0.1:2382 127.0.0.1:2384]
    To view the Prometheus: http://127.0.0.1:9090
    To view the Grafana: http://127.0.0.1:3000
    ```

> **注意：**
>
> - 支持 v5.2.0 及以上版本的 TiDB 在 Apple M1 芯片的机器上运行 `tiup playground`。
> - 以这种方式执行的 playground，在结束部署测试后 TiUP 会清理掉原集群数据，重新执行该命令后会得到一个全新的集群。
> - 若希望持久化数据，可以执行 TiUP 的 `--tag` 参数：`tiup --tag <your-tag> playground ...`，详情参考 TiUP 参考手册。

### 第 2 步：安装 JDK

请在你的计算机上下载并安装 **Java Development Kit** (JDK)，这是 Java 开发的必备工具。**Spring Boot** 支持 Java 版本 8 以上的 JDK，由于 **Hibernate** 版本的缘故，推荐使用 Java 版本 11 以上的 JDK 。

示例应用程序同时支持 **Oracle JDK** 和 **OpenJDK**，请自行选择，本教程将使用 版本 17 的 **OpenJDK** 。

### 第 3 步：安装 Maven

此示例应用程序使用 **Maven** 来管理应用程序的依赖项。Spring 支持的 **Maven** 版本为 3.2 以上，作为依赖管理软件，推荐使用当前最新稳定版本的 **Maven**。

这里给出命令行安装 **Maven** 的办法：

- macOS 安装：

    

    ```
    brew install maven
    ```

- 基于 Debian 的 Linux 发行版上安装(如 Ubuntu 等)：

    

    ```
    apt-get install maven
    ```

- 基于 Red Hat 的 Linux 发行版上安装(如 Fedora、CentOS 等)：

- dnf 包管理器

    

    ```
    dnf install maven
    ```

- yum 包管理器

    

    ```
    yum install maven
    ```

其他安装方法，请参考 [Maven 官方文档](https://maven.apache.org/install.html)。

### 第 4 步：获取应用程序代码

请下载或克隆[示例代码库](https://github.com/pingcap-inc/tidb-example-java)，并进入到目录`spring-jpa-hibernate`中。

#### 创建相同依赖空白程序（可选）

本程序使用 [Spring Initializr](https://start.spring.io/) 构建。你可以在这个网页上通过点选以下选项并更改少量配置，来快速得到一个与本示例程序相同依赖的空白应用程序，配置项如下：

**Project**

- Maven Project

**Language**

- Java

**Spring Boot**

- 3.0.0-M2

**Project Metadata**

- Group: com.pingcap
- Artifact: spring-jpa-hibernate
- Name: spring-jpa-hibernate
- Package name: com.pingcap
- Packaging: Jar
- Java: 17

**Dependencies**

- Spring Web
- Spring Data JPA
- MySQL Driver

配置完毕后如图所示：

![Spring Initializr Config](./media/develop/IMG_20220401-234316020.png)

> **注意：**
>
> 尽管 SQL 相对标准化，但每个数据库供应商都使用 ANSI SQL 定义语法的子集和超集。这被称为数据库的方言。 Hibernate 通过其 org.hibernate.dialect.Dialect 类和每个数据库供应商的各种子类来处理这些方言的变化。
>
> 在大多数情况下，Hibernate 将能够通过在启动期间通过 JDBC 连接的一些返回值来确定要使用的正确方言。有关 Hibernate 确定要使用的正确方言的能力（以及你影响该解析的能力）的信息，请参阅[方言解析](https://docs.jboss.org/hibernate/orm/6.0/userguide/html_single/Hibernate_User_Guide.html#portability-dialectresolver)。
>
> 如果由于某种原因无法确定正确的方言，或者你想使用自定义方言，则需要设置 hibernate.dialect 配置项。
>
> _—— 节选自 Hibernate 官方文档： [Database Dialect](https://docs.jboss.org/hibernate/orm/6.0/userguide/html_single/Hibernate_User_Guide.html#database-dialect)_

随后，此项目即可正常使用，但仅可使用 TiDB 与 MySQL 相同的能力部分，即使用 MySQL 方言。这是由于 Hibernate 支持 TiDB 方言的版本为 6.0.0.Beta2 以上，而 Spring Data JPA 对 Hibernate 的默认依赖版本为 5.6.4.Final。所以，推荐对 pom.xml 作出以下修改：

1. 如此[依赖文件](https://github.com/pingcap-inc/tidb-example-java/blob/main/spring-jpa-hibernate/pom.xml#L26)中所示，将 **Spring Data JPA** 内引入的 `jakarta` 包进行排除，即将：

    

    ```xml
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    ```

    更改为：

    

    ```xml
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
        <exclusions>
            <exclusion>
                <groupId>org.hibernate</groupId>
                <artifactId>hibernate-core-jakarta</artifactId>
            </exclusion>
        </exclusions>
    </dependency>
    ```

2. 随后如此[依赖文件](https://github.com/pingcap-inc/tidb-example-java/blob/main/spring-jpa-hibernate/pom.xml#L53)中所示，引入 `6.0.0.Beta2` 版本以上的 **Hibernate** 依赖，此处以 `6.0.0.CR2` 版本为例：

    

    ```xml
    <dependency>
        <groupId>org.hibernate.orm</groupId>
        <artifactId>hibernate-core</artifactId>
        <version>6.0.0.CR2</version>
    </dependency>
    ```

    更改完毕后即可获取一个空白的，拥有与示例程序相同依赖的 **Spring Boot** 应用程序。

### 第 5 步：运行应用程序

此处对应用程序代码进行编译和运行，将产生一个 Web 应用程序。Hibernate 将创建一个 在数据库 `test` 内的表 `player_jpa`，如果你想应用程序的 Restful API 进行请求，这些请求将会在 TiDB 集群上运行[数据库事务](#事务概览)。

如果你想了解有关此应用程序的代码的详细信息，可参阅本教程下方的[实现细节](#实现细节)。

#### 第 5 步第 1 部分：TiDB Cloud 更改参数

若你使用 TiDB Cloud Serverless Tier 集群，更改 `application.yml`（位于 `src/main/resources` 内）关于 `spring.datasource.url`、`spring.datasource.username`、`spring.datasource.password` 的参数：

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:4000/test
    username: root
    #    password: xxx
    driver-class-name: com.mysql.cj.jdbc.Driver
  jpa:
    show-sql: true
    database-platform: org.hibernate.dialect.TiDBDialect
    hibernate:
      ddl-auto: create-drop
```

若你设定的密码为 `123456`，而且从 TiDB Cloud Serverless Tier 集群面板中得到的连接信息为：

- Endpoint: `xxx.tidbcloud.com`
- Port: `4000`
- User: `2aEp24QWEDLqRFs.root`

那么此处应将参数更改为：

```yaml
spring:
  datasource:
    url: jdbc:mysql://xxx.tidbcloud.com:4000/test?sslMode=VERIFY_IDENTITY&enabledTLSProtocols=TLSv1.2,TLSv1.3
    username: 2aEp24QWEDLqRFs.root
    password: 123456
    driver-class-name: com.mysql.cj.jdbc.Driver
  jpa:
    show-sql: true
    database-platform: org.hibernate.dialect.TiDBDialect
    hibernate:
      ddl-auto: create-drop
```

#### 第 5 步第 2 部分：运行

打开终端，确保你已经进入 spring-jpa-hibernate 目录，若还未在此目录，请使用命令进入：



```shell
cd <path>/tidb-example-java/spring-jpa-hibernate
```

##### 使用 Make 构建并运行(推荐)



```shell
make
```

##### 手动构建并运行

推荐你使用 Make 方式进行构建并运行，当然，若你希望手动进行构建，请依照以下步骤逐步运行，可以得到相同的结果：

清除缓存并打包：



```shell
mvn clean package
```

运行应用程序的 JAR 文件：



```shell
java -jar target/spring-jpa-hibernate-0.0.1.jar
```

#### 第 5 步第 3 部分：输出

输出的最后部分应如下所示：

```
  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::             (v3.0.0-M1)

2022-03-28 18:46:01.429  INFO 14923 --- [           main] com.pingcap.App                          : Starting App v0.0.1 using Java 17.0.2 on CheesedeMacBook-Pro.local with PID 14923 (/path/code/tidb-example-java/spring-jpa-hibernate/target/spring-jpa-hibernate-0.0.1.jar started by cheese in /path/code/tidb-example-java/spring-jpa-hibernate)
2022-03-28 18:46:01.430  INFO 14923 --- [           main] com.pingcap.App                          : No active profile set, falling back to default profiles: default
2022-03-28 18:46:01.709  INFO 14923 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
2022-03-28 18:46:01.733  INFO 14923 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 20 ms. Found 1 JPA repository interfaces.
2022-03-28 18:46:02.010  INFO 14923 --- [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat initialized with port(s): 8080 (http)
2022-03-28 18:46:02.016  INFO 14923 --- [           main] o.apache.catalina.core.StandardService   : Starting service [Tomcat]
2022-03-28 18:46:02.016  INFO 14923 --- [           main] org.apache.catalina.core.StandardEngine  : Starting Servlet engine: [Apache Tomcat/10.0.16]
2022-03-28 18:46:02.050  INFO 14923 --- [           main] o.a.c.c.C.[Tomcat].[localhost].[/]       : Initializing Spring embedded WebApplicationContext
2022-03-28 18:46:02.051  INFO 14923 --- [           main] w.s.c.ServletWebServerApplicationContext : Root WebApplicationContext: initialization completed in 598 ms
2022-03-28 18:46:02.143  INFO 14923 --- [           main] o.hibernate.jpa.internal.util.LogHelper  : HHH000204: Processing PersistenceUnitInfo [name: default]
2022-03-28 18:46:02.173  INFO 14923 --- [           main] org.hibernate.Version                    : HHH000412: Hibernate ORM core version 6.0.0.CR2
2022-03-28 18:46:02.262  WARN 14923 --- [           main] org.hibernate.orm.deprecation            : HHH90000021: Encountered deprecated setting [javax.persistence.sharedCache.mode], use [jakarta.persistence.sharedCache.mode] instead
2022-03-28 18:46:02.324  INFO 14923 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Starting...
2022-03-28 18:46:02.415  INFO 14923 --- [           main] com.zaxxer.hikari.pool.HikariPool        : HikariPool-1 - Added connection com.mysql.cj.jdbc.ConnectionImpl@2575f671
2022-03-28 18:46:02.416  INFO 14923 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Start completed.
2022-03-28 18:46:02.443  INFO 14923 --- [           main] SQL dialect                              : HHH000400: Using dialect: org.hibernate.dialect.TiDBDialect
Hibernate: drop table if exists player_jpa
Hibernate: drop sequence player_jpa_id_seq
Hibernate: create sequence player_jpa_id_seq start with 1 increment by 1
Hibernate: create table player_jpa (id bigint not null, coins integer, goods integer, primary key (id)) engine=InnoDB
2022-03-28 18:46:02.883  INFO 14923 --- [           main] o.h.e.t.j.p.i.JtaPlatformInitiator       : HHH000490: Using JtaPlatform implementation: [org.hibernate.engine.transaction.jta.platform.internal.NoJtaPlatform]
2022-03-28 18:46:02.888  INFO 14923 --- [           main] j.LocalContainerEntityManagerFactoryBean : Initialized JPA EntityManagerFactory for persistence unit 'default'
2022-03-28 18:46:03.125  WARN 14923 --- [           main] org.hibernate.orm.deprecation            : HHH90000021: Encountered deprecated setting [javax.persistence.lock.timeout], use [jakarta.persistence.lock.timeout] instead
2022-03-28 18:46:03.132  WARN 14923 --- [           main] org.hibernate.orm.deprecation            : HHH90000021: Encountered deprecated setting [javax.persistence.lock.timeout], use [jakarta.persistence.lock.timeout] instead
2022-03-28 18:46:03.168  WARN 14923 --- [           main] JpaBaseConfiguration$JpaWebConfiguration : spring.jpa.open-in-view is enabled by default. Therefore, database queries may be performed during view rendering. Explicitly configure spring.jpa.open-in-view to disable this warning
2022-03-28 18:46:03.307  INFO 14923 --- [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat started on port(s): 8080 (http) with context path ''
2022-03-28 18:46:03.311  INFO 14923 --- [           main] com.pingcap.App                          : Started App in 2.072 seconds (JVM running for 2.272)
```

输出日志中，提示应用程序在启动过程中做了什么，这里显示应用程序使用 [Tomcat](https://tomcat.apache.org/) 启动了一个 **Servlet**，使用 Hibernate 作为 ORM ，[HikariCP](https://github.com/brettwooldridge/HikariCP) 作为数据库连接池的实现，使用了 `org.hibernate.dialect.TiDBDialect` 作为数据库方言。启动后，Hibernate 删除并重新创建了表 `player_jpa`，及序列 `player_jpa_id_seq`。在启动的最后，监听了 8080 端口，对外提供 HTTP 服务。

如果你想了解有关此应用程序的代码的详细信息，可参阅本教程下方的[实现细节](#实现细节)。

### 第 6 步：HTTP 请求

服务完成运行后，即可使用 HTTP 接口请求后端程序。`http://localhost:8080` 是服务提供根地址。此处使用一系列的 HTTP 请求来演示如何使用该服务。

#### 第 6 步第 1 部分：使用 Postman 请求(推荐)

你可下载[此配置文件](https://raw.githubusercontent.com/pingcap-inc/tidb-example-java/main/spring-jpa-hibernate/Player.postman_collection.json)到本地，并导入 [Postman](https://www.postman.com/)，导入后如图所示：

![postman import](./media/develop/IMG_20220402-003303222.png)

##### 增加玩家

点击 **Create** 标签，点击 **Send** 按钮，发送 Post 形式的 `http://localhost:8080/player/` 请求。返回值为增加的玩家个数，预期为 1。

![Postman-Create](./media/develop/IMG_20220402-003350731.png)

##### 使用 ID 获取玩家信息

点击 **GetByID** 标签，点击 **Send** 按钮，发送 Get 形式的 `http://localhost:8080/player/1` 请求。返回值为 ID 为 1 的玩家信息。

![Postman-GetByID](./media/develop/IMG_20220402-003416079.png)

##### 使用 Limit 批量获取玩家信息

点击 **GetByLimit** 标签，点击 **Send** 按钮，发送 Get 形式的 `http://localhost:8080/player/limit/3` 请求。返回值为最多 3 个玩家的信息列表。

![Postman-GetByLimit](./media/develop/IMG_20220402-003505846.png)

##### 分页获取玩家信息

点击 **GetByPage** 标签，点击 **Send** 按钮，发送 Get 形式的 `http://localhost:8080/player/page?index=0&size=2` 请求。返回值为 index 为 0 的页，每页有 2 个玩家信息列表。此外，还包含了分页信息，如偏移量、总页数、是否排序等。

![Postman-GetByPage](./media/develop/IMG_20220402-003528474.png)

##### 获取玩家个数

点击 **Count** 标签，点击 **Send** 按钮，发送 Get 形式的 `http://localhost:8080/player/count` 请求。返回值为玩家个数。

![Postman-Count](./media/develop/IMG_20220402-003549966.png)

##### 玩家交易

点击 **Trade** 标签，点击 **Send** 按钮，发送 Put 形式的 `http://localhost:8080/player/trade` 请求，请求参数为售卖玩家 ID `sellID`、购买玩家 ID `buyID`、购买货物数量 `amount`、购买消耗金币数 `price`。返回值为交易是否成功。当出现售卖玩家货物不足、购买玩家金币不足或数据库错误时，交易将不成功，且由于[数据库事务](#事务概览)保证，不会有玩家的金币或货物丢失的情况。

![Postman-Trade](./media/develop/IMG_20220402-003659102.png)

#### 第 6 步第 2 部分：使用 curl 请求

当然，你也可以直接使用 curl 进行请求。

##### 增加玩家

使用 **Post** 方法请求 `/player` 端点请求来增加玩家，即：



```shell
curl --location --request POST 'http://localhost:8080/player/' --header 'Content-Type: application/json' --data-raw '[{"coins":100,"goods":20}]'
```

这里使用 JSON 作为信息的载荷。表示需要创建一个金币数 `coins` 为 100，货物数 `goods` 为 20 的玩家。返回值为创建的玩家个数。

```json
1
```

##### 使用 ID 获取玩家信息

使用 **Get** 方法请求 `/player` 端点请求来获取玩家信息，额外的需要在路径上给出玩家的 `id` 参数，即 `/player/{id}` ，例如在请求 `id` 为 1 的玩家时：



```shell
curl --location --request GET 'http://localhost:8080/player/1'
```

返回值为玩家的信息：

```json
{
  "coins": 200,
  "goods": 10,
  "id": 1
}
```

##### 使用 Limit 批量获取玩家信息

使用 **Get** 方法请求 `/player/limit` 端点请求来获取玩家信息，额外的需要在路径上给出限制查询的玩家信息的总数，即 `/player/limit/{limit}` ，例如在请求最多 3 个玩家的信息时：



```shell
curl --location --request GET 'http://localhost:8080/player/limit/3'
```

返回值为玩家信息的列表：

```json
[
  {
    "coins": 200,
    "goods": 10,
    "id": 1
  },
  {
    "coins": 0,
    "goods": 30,
    "id": 2
  },
  {
    "coins": 100,
    "goods": 20,
    "id": 3
  }
]
```

##### 分页获取玩家信息

使用 **Get** 方法请求 `/player/page` 端点请求来分页获取玩家信息，额外的需要使用 URL 参数 ，例如在请求页面序号 `index` 为 0，每页最大请求量 `size` 为 2 时：



```shell
curl --location --request GET 'http://localhost:8080/player/page?index=0&size=2'
```

返回值为 `index` 为 0 的页，每页有 2 个玩家信息列表。此外，还包含了分页信息，如偏移量、总页数、是否排序等。

```json
{
  "content": [
    {
      "coins": 200,
      "goods": 10,
      "id": 1
    },
    {
      "coins": 0,
      "goods": 30,
      "id": 2
    }
  ],
  "empty": false,
  "first": true,
  "last": false,
  "number": 0,
  "numberOfElements": 2,
  "pageable": {
    "offset": 0,
    "pageNumber": 0,
    "pageSize": 2,
    "paged": true,
    "sort": {
      "empty": true,
      "sorted": false,
      "unsorted": true
    },
    "unpaged": false
  },
  "size": 2,
  "sort": {
    "empty": true,
    "sorted": false,
    "unsorted": true
  },
  "totalElements": 4,
  "totalPages": 2
}
```

##### 获取玩家个数

使用 **Get** 方法请求 `/player/count` 端点请求来获取玩家个数：



```shell
curl --location --request GET 'http://localhost:8080/player/count'
```

返回值为玩家个数

```json
4
```

##### 玩家交易

使用 **Put** 方法请求 `/player/trade` 端点请求来发起玩家间的交易，即：



```shell
curl --location --request PUT 'http://localhost:8080/player/trade' \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'sellID=1' \
  --data-urlencode 'buyID=2' \
  --data-urlencode 'amount=10' \
  --data-urlencode 'price=100'
```

这里使用 **Form Data** 作为信息的载荷。表示售卖玩家 ID `sellID` 为 1、购买玩家 ID `buyID` 为 2、购买货物数量 `amount` 为 10、购买消耗金币数 `price` 为 100。返回值为交易是否成功。当出现售卖玩家货物不足、购买玩家金币不足或数据库错误时，交易将不成功，且由于[数据库事务](#事务概览)保证，不会有玩家的金币或货物丢失的情况。

```json
true
```

#### 第 6 步第 3 部分：使用 Shell 脚本请求

这里已经将请求过程编写为 [Shell](https://github.com/pingcap-inc/tidb-example-java/blob/main/spring-jpa-hibernate/request.sh) 脚本，以方便大家的测试，脚本将会做以下操作：

1. 循环创建 10 名玩家
2. 获取 `id` 为 1 的玩家信息
3. 获取至多 3 名玩家信息列表
4. 获取 `index` 为 0 ，`size` 为 2 的一页玩家信息
5. 获取玩家总数
6. `id` 为 1 的玩家作为售出方，id 为 2 的玩家作为购买方，购买 10 个货物，耗费 100 金币

你可以使用 `make request` 或 `./request.sh` 命令运行此脚本，结果应如下所示：

```
> make request
./request.sh
loop to create 10 players:
1111111111

get player 1:
{"id":1,"coins":200,"goods":10}

get players by limit 3:
[{"id":1,"coins":200,"goods":10},{"id":2,"coins":0,"goods":30},{"id":3,"coins":100,"goods":20}]

get first players:
{"content":[{"id":1,"coins":200,"goods":10},{"id":2,"coins":0,"goods":30}],"pageable":{"sort":{"empty":true,"unsorted":true,"sorted":false},"offset":0,"pageNumber":0,"pageSize":2,"paged":true,"unpaged":false},"last":false,"totalPages":7,"totalElements":14,"first":true,"size":2,"number":0,"sort":{"empty":true,"unsorted":true,"sorted":false},"numberOfElements":2,"empty":false}

get players count:
14

trade by two players:
false
```

### 实现细节

本小节介绍示例应用程序项目中的组件。

#### 总览

本示例项目的大致目录树如下所示（删除了有碍理解的部分）：

```
.
├── pom.xml
└── src
    └── main
        ├── java
        │   └── com
        │       └── pingcap
        │           ├── App.java
        │           ├── controller
        │           │   └── PlayerController.java
        │           ├── dao
        │           │   ├── PlayerBean.java
        │           │   └── PlayerRepository.java
        │           └── service
        │               ├── PlayerService.java
        │               └── impl
        │                   └── PlayerServiceImpl.java
        └── resources
            └── application.yml
```

其中：

- `pom.xml` 内声明了项目的 Maven 配置，如依赖，打包等
- `application.yml` 内声明了项目的用户配置，如数据库地址、密码、使用的数据库方言等
- `App.java` 是项目的入口
- `controller` 是项目对外暴露 HTTP 接口的包
- `service` 是项目实现接口与逻辑的包
- `dao` 是项目实现与数据库连接并完成数据持久化的包

#### 配置

本节将简要介绍 `pom.xml` 文件中的 Maven 配置，及 `application.yml` 文件中的用户配置。

##### Maven 配置

`pom.xml` 文件为 Maven 配置，在文件内声明了项目的 Maven 依赖，打包方法，打包信息等，你可以通过[创建相同依赖空白程序](#创建相同依赖空白程序可选) 这一节来复刻此配置文件的生成流程，当然，也可直接复制至你的项目来使用。



```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
   <modelVersion>4.0.0</modelVersion>
   <parent>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-parent</artifactId>
      <version>3.0.0-M1</version>
      <relativePath/> <!-- lookup parent from repository -->
   </parent>

   <groupId>com.pingcap</groupId>
   <artifactId>spring-jpa-hibernate</artifactId>
   <version>0.0.1</version>
   <name>spring-jpa-hibernate</name>
   <description>an example for spring boot, jpa, hibernate and TiDB</description>

   <properties>
      <java.version>17</java.version>
      <maven.compiler.source>17</maven.compiler.source>
      <maven.compiler.target>17</maven.compiler.target>
   </properties>

   <dependencies>
      <dependency>
         <groupId>org.springframework.boot</groupId>
         <artifactId>spring-boot-starter-data-jpa</artifactId>
         <exclusions>
            <exclusion>
               <groupId>org.hibernate</groupId>
               <artifactId>hibernate-core-jakarta</artifactId>
            </exclusion>
         </exclusions>
      </dependency>

      <dependency>
         <groupId>org.springframework.boot</groupId>
         <artifactId>spring-boot-starter-web</artifactId>
      </dependency>

      <dependency>
         <groupId>mysql</groupId>
         <artifactId>mysql-connector-java</artifactId>
         <scope>runtime</scope>
      </dependency>

      <dependency>
         <groupId>org.springframework.boot</groupId>
         <artifactId>spring-boot-starter-test</artifactId>
         <scope>test</scope>
      </dependency>

      <dependency>
         <groupId>org.hibernate.orm</groupId>
         <artifactId>hibernate-core</artifactId>
         <version>6.0.0.CR2</version>
      </dependency>
   </dependencies>

   <build>
      <plugins>
         <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
         </plugin>
      </plugins>
   </build>

   <repositories>
      <repository>
         <id>spring-milestones</id>
         <name>Spring Milestones</name>
         <url>https://repo.spring.io/milestone</url>
         <snapshots>
            <enabled>false</enabled>
         </snapshots>
      </repository>
   </repositories>
   <pluginRepositories>
      <pluginRepository>
         <id>spring-milestones</id>
         <name>Spring Milestones</name>
         <url>https://repo.spring.io/milestone</url>
         <snapshots>
            <enabled>false</enabled>
         </snapshots>
      </pluginRepository>
   </pluginRepositories>
</project>
```

##### 用户配置

`application.yml` 此配置文件声明了用户配置，如数据库地址、密码、使用的数据库方言等。

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:4000/test
    username: root
    #    password: xxx
    driver-class-name: com.mysql.cj.jdbc.Driver
  jpa:
    show-sql: true
    database-platform: org.hibernate.dialect.TiDBDialect
    hibernate:
      ddl-auto: create-drop
```

此配置格式为 [YAML](https://yaml.org/) 格式。其中：

- `spring.datasource.url` : 数据库连接的 URL。
- `spring.datasource.url` : 数据库用户名。
- `spring.datasource.password` : 数据库密码，此项为空，需注释或删除。
- `spring.datasource.driver-class-name` : 数据库驱动，因为 TiDB 与 MySQL 兼容，则此处使用与 mysql-connector-java 适配的驱动类 `com.mysql.cj.jdbc.Driver`。
- `jpa.show-sql` : 为 true 时将打印 JPA 运行的 SQL。
- `jpa.database-platform` : 选用的数据库方言，此处连接了 TiDB，自然选择 TiDB 方言，注意，此方言在 6.0.0.Beta2 版本后的 Hibernate 中才可选择，请注意依赖版本。
- `jpa.hibernate.ddl-auto` : 此处选择的 create-drop 将会在程序开始时创建表，退出时删除表。请勿在正式环境使用，但此处为示例程序，希望尽量不影响数据库数据，因此选择了此选项。

#### 入口文件

入口文件 `App.java`：



```java
package com.pingcap;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.ApplicationPidFileWriter;

@SpringBootApplication
public class App {
   public static void main(String[] args) {
      SpringApplication springApplication = new SpringApplication(App.class);
      springApplication.addListeners(new ApplicationPidFileWriter("spring-jpa-hibernate.pid"));
      springApplication.run(args);
   }
}
```

入口类比较简单，首先，有一个 Spring Boot 应用程序的标准配置注解 [@SpringBootApplication](https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/autoconfigure/SpringBootApplication.html)。有关详细信息，请参阅 Spring Boot 官方文档中的 [Using the @SpringBootApplication Annotation](https://docs.spring.io/spring-boot/docs/current/reference/html/using-spring-boot.html#using-boot-using-springbootapplication-annotation) 。随后，使用 `ApplicationPidFileWriter` 在程序启动过程中，写下一个名为 `spring-jpa-hibernate.pid` 的 PID (process identification number) 文件，可从外部使用此 PID 文件关闭此应用程序。

#### 数据库持久层

数据库持久层，即 `dao` 包内，实现了数据对象的持久化。

##### 实体对象

`PlayerBean.java` 文件为实体对象，这个对象对应了数据库的一张表。



```java
package com.pingcap.dao;

import jakarta.persistence.*;

/**
 * it's core entity in hibernate
 * @Table appoint to table name
 */
@Entity
@Table(name = "player_jpa")
public class PlayerBean {
    /**
     * @ID primary key
     * @GeneratedValue generated way. this field will use generator named "player_id"
     * @SequenceGenerator using `sequence` feature to create a generator,
     *    and it named "player_jpa_id_seq" in database, initial form 1 (by `initialValue`
     *    parameter default), and every operator will increase 1 (by `allocationSize`)
     */
    @Id
    @GeneratedValue(generator="player_id")
    @SequenceGenerator(name="player_id", sequenceName="player_jpa_id_seq", allocationSize=1)
    private Long id;

    /**
     * @Column field
     */
    @Column(name = "coins")
    private Integer coins;
    @Column(name = "goods")
    private Integer goods;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Integer getCoins() {
        return coins;
    }

    public void setCoins(Integer coins) {
        this.coins = coins;
    }

    public Integer getGoods() {
        return goods;
    }

    public void setGoods(Integer goods) {
        this.goods = goods;
    }
}
```

这里可以看到，实体类中有很多注解，这些注解给了 Hibernate 额外的信息，用以绑定实体类和表：

- `@Entity` 声明 `PlayerBean` 是一个实体类。
- `@Table` 使用注解属性 `name` 将此实体类和表 `player_jpa` 关联。
- `@Id` 声明此属性关联表的主键列。
- `@GeneratedValue` 表示自动生成该列的值，而不应手动设置，使用属性 `generator` 指定生成器的名称为 `player_id`。
- `@SequenceGenerator` 声明一个使用序列的生成器，使用注解属性 `name` 声明生成器的名称为 `player_id` （与 `@GeneratedValue` 中指定的名称需保持一致）。随后使用注解属性 `sequenceName` 指定数据库中序列的名称。最后，使用注解属性 `allocationSize` 声明序列的步长为 1。
- `@Column` 将每个私有属性声明为表 `player_jpa` 的一列，使用注解属性 `name` 确定属性对应的列名。

##### 存储库

为了抽象数据库层，Spring 应用程序使用 [Repository](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#repositories) 接口，或者 Repository 的子接口。 这个接口映射到一个数据库对象，常见的，比如会映射到一个表上。JPA 会实现一些预制的方法，比如 INSERT ，或使用主键的 SELECT 等。



```java
package com.pingcap.dao;

import jakarta.persistence.LockModeType;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Lock;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface PlayerRepository extends JpaRepository<PlayerBean, Long> {
    /**
     * use HQL to query by page
     * @param pageable a pageable parameter required by hibernate
     * @return player list package by page message
     */
    @Query(value = "SELECT player_jpa FROM PlayerBean player_jpa")
    Page<PlayerBean> getPlayersByPage(Pageable pageable);

    /**
     * use SQL to query by limit, using named parameter
     * @param limit sql parameter
     * @return player list (max size by limit)
     */
    @Query(value = "SELECT * FROM player_jpa LIMIT :limit", nativeQuery = true)
    List<PlayerBean> getPlayersByLimit(@Param("limit") Integer limit);

    /**
     * query player and add a lock for update
     * @param id player id
     * @return player
     */
    @Lock(value = LockModeType.PESSIMISTIC_WRITE)
    @Query(value = "SELECT player FROM PlayerBean player WHERE player.id = :id")
    // @Query(value = "SELECT * FROM player_jpa WHERE id = :id FOR UPDATE", nativeQuery = true)
    PlayerBean getPlayerAndLock(@Param("id") Long id);
}
```

`PlayerRepository` 拓展了 Spring 用于 JPA 数据访问所使用的接口 `JpaRepository`。使用 `@Query` 注解，告诉 Hibernate 此接口如何实现查询。在此处使用了两种查询语句的语法，其中，在接口 `getPlayersByPage` 中的查询语句使用的是一种被 Hibernate 称为 [HQL](https://docs.jboss.org/hibernate/orm/6.0/userguide/html_single/Hibernate_User_Guide.html#hql) (Hibernate Query Language) 的语法。而接口 `getPlayersByLimit` 中使用的是普通的 SQL，在使用 SQL 语法时，需要将 `@Query` 的注解参数 `nativeQuery` 设置为 true。

在 `getPlayersByLimit` 注解的 SQL 中，`:limit` 在 Hibernate 中被称为[命名参数](https://docs.jboss.org/hibernate/orm/6.0/userguide/html_single/Hibernate_User_Guide.html#jpql-query-parameters)，Hibernate 将按名称自动寻找并拼接注解所在接口内的参数。你也可以使用 `@Param` 来指定与参数不同的名称用于注入。

在 `getPlayerAndLock` 中，使用了一个注解 [@Lock](https://docs.spring.io/spring-data/jpa/docs/current/api/org/springframework/data/jpa/repository/Lock.html)，此注解声明此处使用悲观锁进行锁定，如需了解更多其他锁定方式，可查看[实体锁定](https://openjpa.apache.org/builds/2.2.2/apache-openjpa/docs/jpa_overview_em_locking.html)文档。此处的 `@Lock` 仅可与 HQL 搭配使用，否则将会产生错误。当然，如果你希望直接使用 SQL 进行锁定，可直接使用注释部分的注解：



```java
@Query(value = "SELECT * FROM player_jpa WHERE id = :id FOR UPDATE", nativeQuery = true)
```

直接使用 SQL 的 `FOR UPDATE` 来增加锁。你也可通过 TiDB SELECT 文档 进行更深层次的原理学习。

#### 逻辑实现

逻辑实现层，即 `service` 包，内含了项目实现的接口与逻辑

##### 接口

`PlayerService.java` 文件内定义了逻辑接口，实现接口，而不是直接编写一个类的原因，是尽量使例子贴近实际使用，体现设计的开闭原则。你也可以省略掉此接口，在依赖类中直接注入实现类，但并不推荐这样做。



```java
package com.pingcap.service;

import com.pingcap.dao.PlayerBean;
import org.springframework.data.domain.Page;

import java.util.List;

public interface PlayerService {
    /**
     * create players by passing in a List of PlayerBean
     *
     * @param players will create players list
     * @return The number of create accounts
     */
    Integer createPlayers(List<PlayerBean> players);

    /**
     * buy goods and transfer funds between one player and another in one transaction
     * @param sellId sell player id
     * @param buyId buy player id
     * @param amount goods amount, if sell player has not enough goods, the trade will break
     * @param price price should pay, if buy player has not enough coins, the trade will break
     */
    void buyGoods(Long sellId, Long buyId, Integer amount, Integer price) throws RuntimeException;

    /**
     * get the player info by id.
     *
     * @param id player id
     * @return the player of this id
     */
    PlayerBean getPlayerByID(Long id);

    /**
     * get a subset of players from the data store by limit.
     *
     * @param limit return max size
     * @return player list
     */
    List<PlayerBean> getPlayers(Integer limit);

    /**
     * get a page of players from the data store.
     *
     * @param index page index
     * @param size page size
     * @return player list
     */
    Page<PlayerBean> getPlayersByPage(Integer index, Integer size);

    /**
     * count players from the data store.
     *
     * @return all players count
     */
    Long countPlayers();
}
```

##### 实现 (重要)

`PlayerService.java` 文件内实现了 `PlayerService` 接口，所有数据操作逻辑都编写在这里。



```java
package com.pingcap.service.impl;

import com.pingcap.dao.PlayerBean;
import com.pingcap.dao.PlayerRepository;
import com.pingcap.service.PlayerService;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * PlayerServiceImpl implements PlayerService interface
 * @Transactional it means every method in this class, will package by a pair of
 *     transaction.begin() and transaction.commit(). and it will be call
 *     transaction.rollback() when method throw an exception
 */
@Service
@Transactional
public class PlayerServiceImpl implements PlayerService {
    @Autowired
    private PlayerRepository playerRepository;

    @Override
    public Integer createPlayers(List<PlayerBean> players) {
        return playerRepository.saveAll(players).size();
    }

    @Override
    public void buyGoods(Long sellId, Long buyId, Integer amount, Integer price) throws RuntimeException {
        PlayerBean buyPlayer = playerRepository.getPlayerAndLock(buyId);
        PlayerBean sellPlayer = playerRepository.getPlayerAndLock(sellId);
        if (buyPlayer == null || sellPlayer == null) {
            throw new RuntimeException("sell or buy player not exist");
        }

        if (buyPlayer.getCoins() < price || sellPlayer.getGoods() < amount) {
            throw new RuntimeException("coins or goods not enough, rollback");
        }

        buyPlayer.setGoods(buyPlayer.getGoods() + amount);
        buyPlayer.setCoins(buyPlayer.getCoins() - price);
        playerRepository.save(buyPlayer);

        sellPlayer.setGoods(sellPlayer.getGoods() - amount);
        sellPlayer.setCoins(sellPlayer.getCoins() + price);
        playerRepository.save(sellPlayer);
    }

    @Override
    public PlayerBean getPlayerByID(Long id) {
        return playerRepository.findById(id).orElse(null);
    }

    @Override
    public List<PlayerBean> getPlayers(Integer limit) {
        return playerRepository.getPlayersByLimit(limit);
    }

    @Override
    public Page<PlayerBean> getPlayersByPage(Integer index, Integer size) {
        return playerRepository.getPlayersByPage(PageRequest.of(index, size));
    }

    @Override
    public Long countPlayers() {
        return playerRepository.count();
    }
}
```

这里使用了 `@Service` 这个注解，声明此对象的生命周期交由 Spring 管理。

注意，除了有 `@Service` 注解之外，PlayerServiceImpl 实现类还有一个 [@Transactional](https://docs.spring.io/spring-framework/docs/current/reference/html/data-access.html#transaction-declarative-annotations) 注解。当在应用程序中启用事务管理时 (可使用 [@EnableTransactionManagement](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/transaction/annotation/EnableTransactionManagement.html) 打开，但 Spring Boot 默认开启，无需再次手动配置)，Spring 会自动将所有带有 `@Transactional` 注释的对象包装在一个代理中，使用该代理对对象的调用进行处理。

你可以简单的认为，代理在带有 `@Transactional` 注释的对象内的函数调用时：在函数顶部将使用 `transaction.begin()` 开启事务，函数返回后，调用 `transaction.commit()` 进行事务提交，而出现任何运行时错误时，代理将会调用 `transaction.rollback()` 来回滚。

你可参阅[数据库事务](#事务概览)来获取更多有关事务的信息，或者阅读 Spring 官网中的文章 [理解 Spring 框架的声明式事务实现](https://docs.spring.io/spring-framework/docs/current/reference/html/data-access.html#tx-decl-explained)。

整个实现类中，`buyGoods` 函数需重点关注，其在不符合逻辑时将抛出异常，引导 Hibernate 进行事务回滚，防止出现错误数据。

#### 外部接口

`controller` 包对外暴露 HTTP 接口，可以通过 [REST API](https://www.redhat.com/en/topics/api/what-is-a-rest-api#) 来访问服务。



```java
package com.pingcap.controller;

import com.pingcap.dao.PlayerBean;
import com.pingcap.service.PlayerService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.lang.NonNull;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/player")
public class PlayerController {
    @Autowired
    private PlayerService playerService;

    @PostMapping
    public Integer createPlayer(@RequestBody @NonNull List<PlayerBean> playerList) {
        return playerService.createPlayers(playerList);
    }

    @GetMapping("/{id}")
    public PlayerBean getPlayerByID(@PathVariable Long id) {
        return playerService.getPlayerByID(id);
    }

    @GetMapping("/limit/{limit_size}")
    public List<PlayerBean> getPlayerByLimit(@PathVariable("limit_size") Integer limit) {
        return playerService.getPlayers(limit);
    }

    @GetMapping("/page")
    public Page<PlayerBean> getPlayerByPage(@RequestParam Integer index, @RequestParam("size") Integer size) {
        return playerService.getPlayersByPage(index, size);
    }

    @GetMapping("/count")
    public Long getPlayersCount() {
        return playerService.countPlayers();
    }

    @PutMapping("/trade")
    public Boolean trade(@RequestParam Long sellID, @RequestParam Long buyID, @RequestParam Integer amount, @RequestParam Integer price) {
        try {
            playerService.buyGoods(sellID, buyID, amount, price);
        } catch (RuntimeException e) {
            return false;
        }

        return true;
    }
}
```

`PlayerController` 中使用了尽可能多的注解方式来作为示例展示功能，在实际项目中，请尽量保持风格的统一，同时遵循你公司或团体的规则。`PlayerController` 有许多注解，下方将进行逐一解释：

- [@RestController](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/RestController.html) 将 `PlayerController` 声明为一个 [Web Controller](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller)，且将返回值序列化为 JSON 输出。
- [@RequestMapping](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/RequestMapping.html) 映射 URL 端点为 `/player` ，即此 `Web Controller` 仅监听 `/player` URL 下的请求。
- `@Autowired` 用于 Spring 的自动装配，可以看到，此处声明需要一个 `PlayerService` 对象，此对象为接口，并未指定使用哪一个实现类，这是由 Spring 自动装配的，有关此装配规则，可查看 Spirng 官网中的 [The IoC container](https://docs.spring.io/spring-framework/docs/3.2.x/spring-framework-reference/html/beans.html) 一文。
- [@PostMapping](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/PostMapping.html) 声明此函数将响应 HTTP 中的 [POST](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST) 类型请求。
    - `@RequestBody` 声明此处将 HTTP 的整个载荷解析到参数 `playerList` 中。
    - `@NonNull` 声明参数不可为空，否则将校验并返回错误。
- [@GetMapping](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/GetMapping.html) 声明此函数将响应 HTTP 中的 [GET](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET) 类型请求。
    - [@PathVariable](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/PathVariable.html) 可以看到注解中有形如 `{id}` 、`{limit_size}` 这样的占位符，这种占位符将被绑定到 `@PathVariable` 注释的变量中，绑定的依据是注解中的注解属性 `name` （变量名可省略，即 `@PathVariable(name="limit_size")` 可写成 `@PathVariable("limit_size")` ），不特殊指定时，与变量名名称相同。
- [@PutMapping](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/PutMapping.html) 声明此函数将响应 HTTP 中的 [PUT](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT) 类型请求。
- [@RequestParam](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/RequestParam.html) 此声明将解析请求中的 URL 参数、表单参数等参数，绑定至注解的变量中。


---
title: TiDB 和 Golang 的简单 CRUD 应用程序
summary: 给出一个 TiDB 和 Golang 的简单 CRUD 应用程序示例。
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD029 -->

## TiDB 和 Golang 的简单 CRUD 应用程序

本文档将展示如何使用 TiDB 和 Golang 来构造一个简单的 CRUD 应用程序。

> **注意：**
>
> 推荐使用 Golang 1.16 以上版本进行 TiDB 的应用程序的编写。

### 第 1 步：启动你的 TiDB 集群

本节将介绍 TiDB 集群的启动方法。

#### 使用 TiDB Cloud Serverless Tier 集群

[创建 Serverless Tier 集群](#第-1-步创建-serverless-tier-集群)。

#### 使用本地集群

你可以部署一个本地测试的 TiDB 集群或正式的 TiDB 集群。详细步骤，请参考：

- 部署本地测试 TiDB 集群
- 部署正式 TiDB 集群。

#### 使用云原生开发环境

基于 Git 的预配置的开发环境：[现在就试试](#gitpod)

该环境会自动克隆代码，并通过 TiUP 部署测试集群。

### 第 2 步：获取代码



```shell
git clone https://github.com/pingcap-inc/tidb-example-golang.git
```

<SimpleTab groupId="language">

<div label="使用 GORM（推荐）" value="gorm">

当前开源比较流行的 Golang ORM 为 GORM，此处将以 v1.23.5 版本进行说明。

封装一个用于适配 TiDB 事务的工具包 [util](https://github.com/pingcap-inc/tidb-example-golang/tree/main/util)，编写以下代码备用：



```go
package util

import (
    "gorm.io/gorm"
)

// TiDBGormBegin start a TiDB and Gorm transaction as a block. If no error is returned, the transaction will be committed. Otherwise, the transaction will be rolled back.
func TiDBGormBegin(db *gorm.DB, pessimistic bool, fc func(tx *gorm.DB) error) (err error) {
    session := db.Session(&gorm.Session{})
    if session.Error != nil {
        return session.Error
    }

    if pessimistic {
        session = session.Exec("set @@tidb_txn_mode=pessimistic")
    } else {
        session = session.Exec("set @@tidb_txn_mode=optimistic")
    }

    if session.Error != nil {
        return session.Error
    }
    return session.Transaction(fc)
}
```

进入目录 `gorm` ：



```shell
cd gorm
```

目录结构如下所示：

```
.
├── Makefile
├── go.mod
├── go.sum
└── gorm.go
```

其中，`gorm.go` 是 `gorm` 这个示例程序的主体。使用 gorm 时，相较于 go-sql-driver/mysql，gorm 屏蔽了创建数据库连接时，不同数据库差异的细节，其还封装了大量的操作，如 AutoMigrate、基本对象的 CRUD 等，极大的简化了代码量。

`Player` 是数据结构体，为数据库表在程序内的映射。`Player` 的每个属性都对应着 `player` 表的一个字段。相较于 go-sql-driver/mysql，gorm 的 `Player` 数据结构体为了给 gorm 提供更多的信息，加入了形如 `` `gorm:"primaryKey;type:VARCHAR(36);column:id"` `` 的注解，用来指示映射关系。



```go

package main

import (
    "fmt"
    "math/rand"

    "github.com/google/uuid"
    "github.com/pingcap-inc/tidb-example-golang/util"

    "gorm.io/driver/mysql"
    "gorm.io/gorm"
    "gorm.io/gorm/clause"
    "gorm.io/gorm/logger"
)

type Player struct {
    ID    string `gorm:"primaryKey;type:VARCHAR(36);column:id"`
    Coins int    `gorm:"column:coins"`
    Goods int    `gorm:"column:goods"`
}

func (*Player) TableName() string {
    return "player"
}

func main() {
    // 1. Configure the example database connection.
    db := createDB()

    // AutoMigrate for player table
    db.AutoMigrate(&Player{})

    // 2. Run some simple examples.
    simpleExample(db)

    // 3. Explore more.
    tradeExample(db)
}

func tradeExample(db *gorm.DB) {
    // Player 1: id is "1", has only 100 coins.
    // Player 2: id is "2", has 114514 coins, and 20 goods.
    player1 := &Player{ID: "1", Coins: 100}
    player2 := &Player{ID: "2", Coins: 114514, Goods: 20}

    // Create two players "by hand", using the INSERT statement on the backend.
    db.Clauses(clause.OnConflict{UpdateAll: true}).Create(player1)
    db.Clauses(clause.OnConflict{UpdateAll: true}).Create(player2)

    // Player 1 wants to buy 10 goods from player 2.
    // It will cost 500 coins, but player 1 cannot afford it.
    fmt.Println("\nbuyGoods:\n    => this trade will fail")
    if err := buyGoods(db, player2.ID, player1.ID, 10, 500); err == nil {
        panic("there shouldn't be success")
    }

    // So player 1 has to reduce the incoming quantity to two.
    fmt.Println("\nbuyGoods:\n    => this trade will success")
    if err := buyGoods(db, player2.ID, player1.ID, 2, 100); err != nil {
        panic(err)
    }
}

func simpleExample(db *gorm.DB) {
    // Create a player, who has a coin and a goods..
    if err := db.Clauses(clause.OnConflict{UpdateAll: true}).
        Create(&Player{ID: "test", Coins: 1, Goods: 1}).Error; err != nil {
        panic(err)
    }

    // Get a player.
    var testPlayer Player
    db.Find(&testPlayer, "id = ?", "test")
    fmt.Printf("getPlayer: %+v\n", testPlayer)

    // Create players with bulk inserts. Insert 1919 players totally, with 114 players per batch.
    bulkInsertPlayers := make([]Player, 1919, 1919)
    total, batch := 1919, 114
    for i := 0; i < total; i++ {
        bulkInsertPlayers[i] = Player{
            ID:    uuid.New().String(),
            Coins: rand.Intn(10000),
            Goods: rand.Intn(10000),
        }
    }

    if err := db.Session(&gorm.Session{Logger: db.Logger.LogMode(logger.Error)}).
        CreateInBatches(bulkInsertPlayers, batch).Error; err != nil {
        panic(err)
    }

    // Count players amount.
    playersCount := int64(0)
    db.Model(&Player{}).Count(&playersCount)
    fmt.Printf("countPlayers: %d\n", playersCount)

    // Print 3 players.
    threePlayers := make([]Player, 3, 3)
    db.Limit(3).Find(&threePlayers)
    for index, player := range threePlayers {
        fmt.Printf("print %d player: %+v\n", index+1, player)
    }
}

func createDB() *gorm.DB {
    dsn := "root:@tcp(127.0.0.1:4000)/test?charset=utf8mb4"
    db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{
        Logger: logger.Default.LogMode(logger.Info),
    })
    if err != nil {
        panic(err)
    }

    return db
}

func buyGoods(db *gorm.DB, sellID, buyID string, amount, price int) error {
    return util.TiDBGormBegin(db, true, func(tx *gorm.DB) error {
        var sellPlayer, buyPlayer Player
        if err := tx.Clauses(clause.Locking{Strength: "UPDATE"}).
            Find(&sellPlayer, "id = ?", sellID).Error; err != nil {
            return err
        }

        if sellPlayer.ID != sellID || sellPlayer.Goods < amount {
            return fmt.Errorf("sell player %s goods not enough", sellID)
        }

        if err := tx.Clauses(clause.Locking{Strength: "UPDATE"}).
            Find(&buyPlayer, "id = ?", buyID).Error; err != nil {
            return err
        }

        if buyPlayer.ID != buyID || buyPlayer.Coins < price {
            return fmt.Errorf("buy player %s coins not enough", buyID)
        }

        updateSQL := "UPDATE player set goods = goods + ?, coins = coins + ? WHERE id = ?"
        if err := tx.Exec(updateSQL, -amount, price, sellID).Error; err != nil {
            return err
        }

        if err := tx.Exec(updateSQL, amount, -price, buyID).Error; err != nil {
            return err
        }

        fmt.Println("\n[buyGoods]:\n    'trade success'")
        return nil
    })
}
```

</div>

<div label="使用 go-sql-driver/mysql" value="sqldriver">

使用 go-sql-driver/mysql 时，首先进入目录 `sqldriver`：



```shell
cd sqldriver
```

目录结构如下所示：

```
.
├── Makefile
├── dao.go
├── go.mod
├── go.sum
├── sql
│   └── dbinit.sql
├── sql.go
└── sqldriver.go
```

其中，`dbinit.sql` 为数据表初始化语句：



```sql
USE test;
DROP TABLE IF EXISTS player;

CREATE TABLE player (
    `id` VARCHAR(36),
    `coins` INTEGER,
    `goods` INTEGER,
   PRIMARY KEY (`id`)
);
```

`sqldriver.go` 是 `sqldriver` 这个示例程序的主体。因为 TiDB 与 MySQL 协议兼容，因此，需要初始化一个 MySQL 协议的数据源 `db, err := sql.Open("mysql", dsn)`，以此连接到 TiDB。并在其后，调用 `dao.go` 中的一系列方法，用来管理数据对象，进行增删改查等操作。



```go
package main

import (
    "database/sql"
    "fmt"

    _ "github.com/go-sql-driver/mysql"
)

func main() {
    // 1. Configure the example database connection.
    dsn := "root:@tcp(127.0.0.1:4000)/test?charset=utf8mb4"
    openDB("mysql", dsn, func(db *sql.DB) {
        // 2. Run some simple examples.
        simpleExample(db)

        // 3. Explore more.
        tradeExample(db)
    })
}

func simpleExample(db *sql.DB) {
    // Create a player, who has a coin and a goods.
    err := createPlayer(db, Player{ID: "test", Coins: 1, Goods: 1})
    if err != nil {
        panic(err)
    }

    // Get a player.
    testPlayer, err := getPlayer(db, "test")
    if err != nil {
        panic(err)
    }
    fmt.Printf("getPlayer: %+v\n", testPlayer)

    // Create players with bulk inserts. Insert 1919 players totally, with 114 players per batch.

    err = bulkInsertPlayers(db, randomPlayers(1919), 114)
    if err != nil {
        panic(err)
    }

    // Count players amount.
    playersCount, err := getCount(db)
    if err != nil {
        panic(err)
    }
    fmt.Printf("countPlayers: %d\n", playersCount)

    // Print 3 players.
    threePlayers, err := getPlayerByLimit(db, 3)
    if err != nil {
        panic(err)
    }
    for index, player := range threePlayers {
        fmt.Printf("print %d player: %+v\n", index+1, player)
    }
}

func tradeExample(db *sql.DB) {
    // Player 1: id is "1", has only 100 coins.
    // Player 2: id is "2", has 114514 coins, and 20 goods.
    player1 := Player{ID: "1", Coins: 100}
    player2 := Player{ID: "2", Coins: 114514, Goods: 20}

    // Create two players "by hand", using the INSERT statement on the backend.
    if err := createPlayer(db, player1); err != nil {
        panic(err)
    }
    if err := createPlayer(db, player2); err != nil {
        panic(err)
    }

    // Player 1 wants to buy 10 goods from player 2.
    // It will cost 500 coins, but player 1 cannot afford it.
    fmt.Println("\nbuyGoods:\n    => this trade will fail")
    if err := buyGoods(db, player2.ID, player1.ID, 10, 500); err == nil {
        panic("there shouldn't be success")
    }

    // So player 1 has to reduce the incoming quantity to two.
    fmt.Println("\nbuyGoods:\n    => this trade will success")
    if err := buyGoods(db, player2.ID, player1.ID, 2, 100); err != nil {
        panic(err)
    }
}

func openDB(driverName, dataSourceName string, runnable func(db *sql.DB)) {
    db, err := sql.Open(driverName, dataSourceName)
    if err != nil {
        panic(err)
    }
    defer db.Close()

    runnable(db)
}
```

随后，封装一个用于适配 TiDB 事务的工具包 [util](https://github.com/pingcap-inc/tidb-example-golang/tree/main/util)，编写以下代码备用：



```go
package util

import (
    "context"
    "database/sql"
)

type TiDBSqlTx struct {
    *sql.Tx
    conn        *sql.Conn
    pessimistic bool
}

func TiDBSqlBegin(db *sql.DB, pessimistic bool) (*TiDBSqlTx, error) {
    ctx := context.Background()
    conn, err := db.Conn(ctx)
    if err != nil {
        return nil, err
    }
    if pessimistic {
        _, err = conn.ExecContext(ctx, "set @@tidb_txn_mode=?", "pessimistic")
    } else {
        _, err = conn.ExecContext(ctx, "set @@tidb_txn_mode=?", "optimistic")
    }
    if err != nil {
        return nil, err
    }
    tx, err := conn.BeginTx(ctx, nil)
    if err != nil {
        return nil, err
    }
    return &TiDBSqlTx{
        conn:        conn,
        Tx:          tx,
        pessimistic: pessimistic,
    }, nil
}

func (tx *TiDBSqlTx) Commit() error {
    defer tx.conn.Close()
    return tx.Tx.Commit()
}

func (tx *TiDBSqlTx) Rollback() error {
    defer tx.conn.Close()
    return tx.Tx.Rollback()
}
```

在 `dao.go` 中定义一系列数据的操作方法，用来对提供数据的写入能力。这也是本例子中和核心部分。



```go
package main

import (
    "database/sql"
    "fmt"
    "math/rand"
    "strings"

    "github.com/google/uuid"
    "github.com/pingcap-inc/tidb-example-golang/util"
)

type Player struct {
    ID    string
    Coins int
    Goods int
}

// createPlayer create a player
func createPlayer(db *sql.DB, player Player) error {
    _, err := db.Exec(CreatePlayerSQL, player.ID, player.Coins, player.Goods)
    return err
}

// getPlayer get a player
func getPlayer(db *sql.DB, id string) (Player, error) {
    var player Player

    rows, err := db.Query(GetPlayerSQL, id)
    if err != nil {
        return player, err
    }
    defer rows.Close()

    if rows.Next() {
        err = rows.Scan(&player.ID, &player.Coins, &player.Goods)
        if err == nil {
            return player, nil
        } else {
            return player, err
        }
    }

    return player, fmt.Errorf("can not found player")
}

// getPlayerByLimit get players by limit
func getPlayerByLimit(db *sql.DB, limit int) ([]Player, error) {
    var players []Player

    rows, err := db.Query(GetPlayerByLimitSQL, limit)
    if err != nil {
        return players, err
    }
    defer rows.Close()

    for rows.Next() {
        player := Player{}
        err = rows.Scan(&player.ID, &player.Coins, &player.Goods)
        if err == nil {
            players = append(players, player)
        } else {
            return players, err
        }
    }

    return players, nil
}

// bulk-insert players
func bulkInsertPlayers(db *sql.DB, players []Player, batchSize int) error {
    tx, err := util.TiDBSqlBegin(db, true)
    if err != nil {
        return err
    }

    stmt, err := tx.Prepare(buildBulkInsertSQL(batchSize))
    if err != nil {
        return err
    }

    defer stmt.Close()

    for len(players) > batchSize {
        if _, err := stmt.Exec(playerToArgs(players[:batchSize])...); err != nil {
            tx.Rollback()
            return err
        }

        players = players[batchSize:]
    }

    if len(players) != 0 {
        if _, err := tx.Exec(buildBulkInsertSQL(len(players)), playerToArgs(players)...); err != nil {
            tx.Rollback()
            return err
        }
    }

    if err := tx.Commit(); err != nil {
        tx.Rollback()
        return err
    }

    return nil
}

func getCount(db *sql.DB) (int, error) {
    count := 0

    rows, err := db.Query(GetCountSQL)
    if err != nil {
        return count, err
    }

    defer rows.Close()

    if rows.Next() {
        if err := rows.Scan(&count); err != nil {
            return count, err
        }
    }

    return count, nil
}

func buyGoods(db *sql.DB, sellID, buyID string, amount, price int) error {
    var sellPlayer, buyPlayer Player

    tx, err := util.TiDBSqlBegin(db, true)
    if err != nil {
        return err
    }

    buyExec := func() error {
        stmt, err := tx.Prepare(GetPlayerWithLockSQL)
        if err != nil {
            return err
        }
        defer stmt.Close()

        sellRows, err := stmt.Query(sellID)
        if err != nil {
            return err
        }
        defer sellRows.Close()

        if sellRows.Next() {
            if err := sellRows.Scan(&sellPlayer.ID, &sellPlayer.Coins, &sellPlayer.Goods); err != nil {
                return err
            }
        }
        sellRows.Close()

        if sellPlayer.ID != sellID || sellPlayer.Goods < amount {
            return fmt.Errorf("sell player %s goods not enough", sellID)
        }

        buyRows, err := stmt.Query(buyID)
        if err != nil {
            return err
        }
        defer buyRows.Close()

        if buyRows.Next() {
            if err := buyRows.Scan(&buyPlayer.ID, &buyPlayer.Coins, &buyPlayer.Goods); err != nil {
                return err
            }
        }
        buyRows.Close()

        if buyPlayer.ID != buyID || buyPlayer.Coins < price {
            return fmt.Errorf("buy player %s coins not enough", buyID)
        }

        updateStmt, err := tx.Prepare(UpdatePlayerSQL)
        if err != nil {
            return err
        }
        defer updateStmt.Close()

        if _, err := updateStmt.Exec(-amount, price, sellID); err != nil {
            return err
        }

        if _, err := updateStmt.Exec(amount, -price, buyID); err != nil {
            return err
        }

        return nil
    }

    err = buyExec()
    if err == nil {
        fmt.Println("\n[buyGoods]:\n    'trade success'")
        tx.Commit()
    } else {
        tx.Rollback()
    }

    return err
}

func playerToArgs(players []Player) []interface{} {
    var args []interface{}
    for _, player := range players {
        args = append(args, player.ID, player.Coins, player.Goods)
    }
    return args
}

func buildBulkInsertSQL(amount int) string {
    return CreatePlayerSQL + strings.Repeat(",(?,?,?)", amount-1)
}

func randomPlayers(amount int) []Player {
    players := make([]Player, amount, amount)
    for i := 0; i < amount; i++ {
        players[i] = Player{
            ID:    uuid.New().String(),
            Coins: rand.Intn(10000),
            Goods: rand.Intn(10000),
        }
    }

    return players
}
```

`sql.go` 中存放了 SQL 语句的常量。



```go
package main

const (
    CreatePlayerSQL      = "INSERT INTO player (id, coins, goods) VALUES (?, ?, ?)"
    GetPlayerSQL         = "SELECT id, coins, goods FROM player WHERE id = ?"
    GetCountSQL          = "SELECT count(*) FROM player"
    GetPlayerWithLockSQL = GetPlayerSQL + " FOR UPDATE"
    UpdatePlayerSQL      = "UPDATE player set goods = goods + ?, coins = coins + ? WHERE id = ?"
    GetPlayerByLimitSQL  = "SELECT id, coins, goods FROM player LIMIT ?"
)
```

</div>

</SimpleTab>

### 第 3 步：运行代码

本节将逐步介绍代码的运行方法。

#### 第 3 步第 1 部分：go-sql-driver/mysql 表初始化

<SimpleTab groupId="language">

<div label="使用 GORM（推荐）" value="gorm">

> **注意：**
>
> 在 Gitpod Playground 中尝试 GORM: [现在就试试](https://gitpod.io/#targetMode=gorm/https://github.com/pingcap-inc/tidb-example-golang)

无需手动初始化表。

</div>

<div label="使用 go-sql-driver/mysql" value="sqldriver">

> **注意：**
>
> 在 Gitpod Playground 中尝试 go-sql-driver/mysql: [现在就试试](https://gitpod.io/#targetMode=sqldriver/https://github.com/pingcap-inc/tidb-example-golang)

使用 go-sql-driver/mysql 时，需手动初始化数据库表，若你本地已经安装了 `mysql-client`，且使用本地集群，可直接在 `sqldriver` 目录下运行：



```shell
make mysql
```

或直接执行：



```shell
mysql --host 127.0.0.1 --port 4000 -u root<sql/dbinit.sql
```

若你不使用本地集群，或未安装 **mysql-client**，请直接登录你的集群，并运行 `sql/dbinit.sql` 文件内的 SQL 语句。

</div>

</SimpleTab>

#### 第 3 步第 2 部分：TiDB Cloud 更改参数

<SimpleTab groupId="language">

<div label="使用 GORM（推荐）" value="gorm">

若你使用 TiDB Cloud Serverless Tier 集群，更改 `gorm.go` 内 `dsn` 参数值：



```go
dsn := "root:@tcp(127.0.0.1:4000)/test?charset=utf8mb4"
```

若你设定的密码为 `123456`，而且从 TiDB Cloud Serverless Tier 集群面板中得到的连接信息为：

- Endpoint: `xxx.tidbcloud.com`
- Port: `4000`
- User: `2aEp24QWEDLqRFs.root`

那么此处应将 `mysql.RegisterTLSConfig` 和 `dsn` 更改为：

```go
mysql.RegisterTLSConfig("register-tidb-tls", &tls.Config {
    MinVersion: tls.VersionTLS12,
    ServerName: "xxx.tidbcloud.com",
})

dsn := "2aEp24QWEDLqRFs.root:123456@tcp(xxx.tidbcloud.com:4000)/test?charset=utf8mb4&tls=register-tidb-tls"
```

</div>

<div label="使用 go-sql-driver/mysql" value="sqldriver">

若你使用 TiDB Cloud Serverless Tier 集群，更改 `sqldriver.go` 内 `dsn` 参数的值：



```go
dsn := "root:@tcp(127.0.0.1:4000)/test?charset=utf8mb4"
```

若你设定的密码为 `123456`，而且从 TiDB Cloud Serverless Tier 集群面板中得到的连接信息为：

- Endpoint: `xxx.tidbcloud.com`
- Port: `4000`
- User: `2aEp24QWEDLqRFs.root`

那么此处应将 `mysql.RegisterTLSConfig` 和 `dsn` 更改为：



```go
mysql.RegisterTLSConfig("register-tidb-tls", &tls.Config {
    MinVersion: tls.VersionTLS12,
    ServerName: "xxx.tidbcloud.com",
})

dsn := "2aEp24QWEDLqRFs.root:123456@tcp(xxx.tidbcloud.com:4000)/test?charset=utf8mb4&tls=register-tidb-tls"
```

</div>

</SimpleTab>

#### 第 3 步第 3 部分：运行

<SimpleTab groupId="language">

<div label="使用 GORM（推荐）" value="gorm">

运行 `make all`，这是以下两个操作的组合：

- 构建二进制 (make build)：`go build -o bin/gorm-example`
- 运行 (make run)：`./bin/gorm-example`

你也可以单独运行这两个 make 命令或原生命令。

</div>

<div label="使用 go-sql-driver/mysql" value="sqldriver">

运行 `make all`，这是以下三个操作的组合：

- 创建表 (make mysql)：`mysql --host 127.0.0.1 --port 4000 -u root<sql/dbinit.sql`
- 构建二进制 (make build)： `go build -o bin/sql-driver-example`
- 运行 (make run)： `./bin/sql-driver-example`

你也可以单独运行这三个 make 命令或原生命令。

</div>

</SimpleTab>

### 第 4 步：预期输出

<SimpleTab groupId="language">

<div label="使用 GORM（推荐）" value="gorm">

[GORM 预期输出](https://github.com/pingcap-inc/tidb-example-golang/blob/main/Expected-Output.md#gorm)

</div>

<div label="使用 go-sql-driver/mysql" value="sqldriver">

[go-sql-driver/mysql 预期输出](https://github.com/pingcap-inc/tidb-example-golang/blob/main/Expected-Output.md#sqldriver)

</div>

</SimpleTab>


---
title: TiDB 和 Python 的简单 CRUD 应用程序
summary: 给出一个 TiDB 和 Python 的简单 CRUD 应用程序示例。
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD029 -->

## TiDB 和 Python 的简单 CRUD 应用程序

本文档将展示如何使用 TiDB 和 Python 来构造一个简单的 CRUD 应用程序。

> **注意：**
>
> 推荐使用 Python 3.10 及以上版本进行 TiDB 的应用程序的编写。

### 第 1 步：启动你的 TiDB 集群

本节将介绍 TiDB 集群的启动方法。

#### 使用 TiDB Cloud Serverless Tier 集群

[创建 Serverless Tier 集群](#第-1-步创建-serverless-tier-集群)

#### 使用本地集群

你可以部署一个本地测试的 TiDB 集群或正式的 TiDB 集群。详细步骤，请参考：

- 部署本地测试 TiDB 集群
- 部署正式 TiDB 集群。

#### 使用云原生开发环境

基于 Git 的预配置的开发环境：[现在就试试](#gitpod)

该环境会自动克隆代码，并通过 TiUP 部署测试集群。

### 第 2 步：获取代码



```shell
git clone https://github.com/pingcap-inc/tidb-example-python.git
```

<SimpleTab groupId="language">

<div label="使用 SQLAlchemy（推荐）" value="SQLAlchemy">

[SQLAlchemy](https://www.sqlalchemy.org/) 为当前比较流行的开源 Python ORM 之一。此处将以 SQLAlchemy **1.4.44** 版本进行说明。

```python
import uuid
from typing import List

from sqlalchemy import create_engine, String, Column, Integer, select, func
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('mysql://root:@127.0.0.1:4000/test')
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


class Player(Base):
    __tablename__ = "player"

    id = Column(String(36), primary_key=True)
    coins = Column(Integer)
    goods = Column(Integer)

    def __repr__(self):
        return f'Player(id={self.id!r}, coins={self.coins!r}, goods={self.goods!r})'


def random_player(amount: int) -> List[Player]:
    players = []
    for _ in range(amount):
        players.append(Player(id=uuid.uuid4(), coins=10000, goods=10000))

    return players


def simple_example() -> None:
    with Session() as session:
        # create a player, who has a coin and a goods.
        session.add(Player(id="test", coins=1, goods=1))

        # get this player, and print it.
        get_test_stmt = select(Player).where(Player.id == "test")
        for player in session.scalars(get_test_stmt):
            print(player)

        # create players with bulk inserts.
        # insert 1919 players totally, with 114 players per batch.
        # each player has a random UUID
        player_list = random_player(1919)
        for idx in range(0, len(player_list), 114):
            session.bulk_save_objects(player_list[idx:idx + 114])

        # print the number of players
        count = session.query(func.count(Player.id)).scalar()
        print(f'number of players: {count}')

        # print 3 players.
        three_players = session.query(Player).limit(3).all()
        for player in three_players:
            print(player)

        session.commit()


def trade_check(session: Session, sell_id: str, buy_id: str, amount: int, price: int) -> bool:
    # sell player goods check
    sell_player = session.query(Player.goods).filter(Player.id == sell_id).with_for_update().one()
    if sell_player.goods < amount:
        print(f'sell player {sell_id} goods not enough')
        return False

    # buy player coins check
    buy_player = session.query(Player.coins).filter(Player.id == buy_id).with_for_update().one()
    if buy_player.coins < price:
        print(f'buy player {buy_id} coins not enough')
        return False


def trade(sell_id: str, buy_id: str, amount: int, price: int) -> None:
    with Session() as session:
        if trade_check(session, sell_id, buy_id, amount, price) is False:
            return

        # deduct the goods of seller, and raise his/her the coins
        session.query(Player).filter(Player.id == sell_id). \
            update({'goods': Player.goods - amount, 'coins': Player.coins + price})
        # deduct the coins of buyer, and raise his/her the goods
        session.query(Player).filter(Player.id == buy_id). \
            update({'goods': Player.goods + amount, 'coins': Player.coins - price})

        session.commit()
        print("trade success")


def trade_example() -> None:
    with Session() as session:
        # create two players
        # player 1: id is "1", has only 100 coins.
        # player 2: id is "2", has 114514 coins, and 20 goods.
        session.add(Player(id="1", coins=100, goods=0))
        session.add(Player(id="2", coins=114514, goods=20))
        session.commit()

    # player 1 wants to buy 10 goods from player 2.
    # it will cost 500 coins, but player 1 cannot afford it.
    # so this trade will fail, and nobody will lose their coins or goods
    trade(sell_id="2", buy_id="1", amount=10, price=500)

    # then player 1 has to reduce the incoming quantity to 2.
    # this trade will be successful
    trade(sell_id="2", buy_id="1", amount=2, price=100)

    with Session() as session:
        traders = session.query(Player).filter(Player.id.in_(("1", "2"))).all()
        for player in traders:
            print(player)
        session.commit()


simple_example()
trade_example()
```

相较于直接使用 Driver，SQLAlchemy 屏蔽了创建数据库连接时，不同数据库差异的细节。SQLAlchemy 还封装了大量的操作，如会话管理、基本对象的 CRUD 等，极大地简化了代码量。

`Player` 类为数据库表在程序内的映射。`Player` 的每个属性都对应着 `player` 表的一个字段。SQLAlchemy 使用 `Player` 类为了给 SQLAlchemy 提供更多的信息，使用了形如以上示例中的 `id = Column(String(36), primary_key=True)` 的类型定义，用来指示字段类型和其附加属性。`id = Column(String(36), primary_key=True)` 表示 `id` 字段为 `String` 类型，对应数据库类型为 `VARCHAR`，长度为 `36`，且为主键。

关于 SQLAlchemy 的更多使用方法，你可以参考 [SQLAlchemy 官网](https://www.sqlalchemy.org/)。

</div>

<div label="使用 peewee（推荐）" value="peewee">

[peewee](http://docs.peewee-orm.com/en/latest/) 为当前比较流行的开源 Python ORM 之一。此处将以 peewee **3.15.4** 版本进行说明。

```python
import os
import uuid
from typing import List

from peewee import *

from playhouse.db_url import connect

db = connect('mysql://root:@127.0.0.1:4000/test')


class Player(Model):
    id = CharField(max_length=36, primary_key=True)
    coins = IntegerField()
    goods = IntegerField()

    class Meta:
        database = db
        table_name = "player"


def random_player(amount: int) -> List[Player]:
    players = []
    for _ in range(amount):
        players.append(Player(id=uuid.uuid4(), coins=10000, goods=10000))

    return players


def simple_example() -> None:
    # create a player, who has a coin and a goods.
    Player.create(id="test", coins=1, goods=1)

    # get this player, and print it.
    test_player = Player.select().where(Player.id == "test").get()
    print(f'id:{test_player.id}, coins:{test_player.coins}, goods:{test_player.goods}')

    # create players with bulk inserts.
    # insert 1919 players totally, with 114 players per batch.
    # each player has a random UUID
    player_list = random_player(1919)
    Player.bulk_create(player_list, 114)

    # print the number of players
    count = Player.select().count()
    print(f'number of players: {count}')
    
    # print 3 players.
    three_players = Player.select().limit(3)
    for player in three_players:
        print(f'id:{player.id}, coins:{player.coins}, goods:{player.goods}')


def trade_check(sell_id: str, buy_id: str, amount: int, price: int) -> bool:
    sell_goods = Player.select(Player.goods).where(Player.id == sell_id).get().goods
    if sell_goods < amount:
        print(f'sell player {sell_id} goods not enough')
        return False

    buy_coins = Player.select(Player.coins).where(Player.id == buy_id).get().coins
    if buy_coins < price:
        print(f'buy player {buy_id} coins not enough')
        return False

    return True


def trade(sell_id: str, buy_id: str, amount: int, price: int) -> None:
    with db.atomic() as txn:
        try:
            if trade_check(sell_id, buy_id, amount, price) is False:
                txn.rollback()
                return

            # deduct the goods of seller, and raise his/her the coins
            Player.update(goods=Player.goods - amount, coins=Player.coins + price).where(Player.id == sell_id).execute()
            # deduct the coins of buyer, and raise his/her the goods
            Player.update(goods=Player.goods + amount, coins=Player.coins - price).where(Player.id == buy_id).execute()

        except Exception as err:
            txn.rollback()
            print(f'something went wrong: {err}')
        else:
            txn.commit()
            print("trade success")


def trade_example() -> None:
    # create two players
    # player 1: id is "1", has only 100 coins.
    # player 2: id is "2", has 114514 coins, and 20 goods.
    Player.create(id="1", coins=100, goods=0)
    Player.create(id="2", coins=114514, goods=20)

    # player 1 wants to buy 10 goods from player 2.
    # it will cost 500 coins, but player 1 cannot afford it.
    # so this trade will fail, and nobody will lose their coins or goods
    trade(sell_id="2", buy_id="1", amount=10, price=500)

    # then player 1 has to reduce the incoming quantity to 2.
    # this trade will be successful
    trade(sell_id="2", buy_id="1", amount=2, price=100)

    # let's take a look for player 1 and player 2 currently
    after_trade_players = Player.select().where(Player.id.in_(["1", "2"]))
    for player in after_trade_players:
        print(f'id:{player.id}, coins:{player.coins}, goods:{player.goods}')


db.connect()

## recreate the player table
db.drop_tables([Player])
db.create_tables([Player])

simple_example()
trade_example()
```

相较于直接使用 Driver，peewee 屏蔽了创建数据库连接时，不同数据库差异的细节。peewee 还封装了大量的操作，如会话管理、基本对象的 CRUD 等，极大地简化了代码量。

`Player` 类为数据库表在程序内的映射。`Player` 的每个属性都对应着 `player` 表的一个字段。SQLAlchemy 使用 `Player` 类为了给 SQLAlchemy 提供更多的信息，使用了形如以上示例中的 `id = CharField(max_length=36, primary_key=True)` 的类型定义，用来指示字段类型和其附加属性。`id = CharField(max_length=36, primary_key=True)` 表示 `id` 字段为 `CharField` 类型，对应数据库类型为 `VARCHAR`, 长度为 `36`，且为主键。

关于 peewee 的更多使用方法，你可以参考 [peewee 官网](http://docs.peewee-orm.com/en/latest/)。

</div>

<div label="使用 mysqlclient" value="mysqlclient">

[mysqlclient](https://pypi.org/project/mysqlclient/) 为当前比较流行的开源 Python Driver 之一。此处将以 mysqlclient **2.1.1** 版本进行说明。虽然 Python 的 Driver 相较其他语言，使用也极其方便。但因其不可屏蔽底层实现，需手动管控事务的特性，如果没有大量必须使用 SQL 的场景，仍然推荐使用 ORM 进行程序编写。这可以降低程序的耦合性。

```python
import uuid
from typing import List

import MySQLdb
from MySQLdb import Connection
from MySQLdb.cursors import Cursor

def get_connection(autocommit: bool = True) -> MySQLdb.Connection:
    return MySQLdb.connect(
        host="127.0.0.1",
        port=4000,
        user="root",
        password="",
        database="test",
        autocommit=autocommit
    )


def create_player(cursor: Cursor, player: tuple) -> None:
    cursor.execute("INSERT INTO player (id, coins, goods) VALUES (%s, %s, %s)", player)


def get_player(cursor: Cursor, player_id: str) -> tuple:
    cursor.execute("SELECT id, coins, goods FROM player WHERE id = %s", (player_id,))
    return cursor.fetchone()


def get_players_with_limit(cursor: Cursor, limit: int) -> List[tuple]:
    cursor.execute("SELECT id, coins, goods FROM player LIMIT %s", (limit,))
    return cursor.fetchall()


def random_player(amount: int) -> List[tuple]:
    players = []
    for _ in range(amount):
        players.append((uuid.uuid4(), 10000, 10000))

    return players


def bulk_create_player(cursor: Cursor, players: List[tuple]) -> None:
    cursor.executemany("INSERT INTO player (id, coins, goods) VALUES (%s, %s, %s)", players)


def get_count(cursor: Cursor) -> None:
    cursor.execute("SELECT count(*) FROM player")
    return cursor.fetchone()[0]


def trade_check(cursor: Cursor, sell_id: str, buy_id: str, amount: int, price: int) -> bool:
    get_player_with_lock_sql = "SELECT coins, goods FROM player WHERE id = %s FOR UPDATE"

    # sell player goods check
    cursor.execute(get_player_with_lock_sql, (sell_id,))
    _, sell_goods = cursor.fetchone()
    if sell_goods < amount:
        print(f'sell player {sell_id} goods not enough')
        return False

    # buy player coins check
    cursor.execute(get_player_with_lock_sql, (buy_id,))
    buy_coins, _ = cursor.fetchone()
    if buy_coins < price:
        print(f'buy player {buy_id} coins not enough')
        return False


def trade_update(cursor: Cursor, sell_id: str, buy_id: str, amount: int, price: int) -> None:
    update_player_sql = "UPDATE player set goods = goods + %s, coins = coins + %s WHERE id = %s"

    # deduct the goods of seller, and raise his/her the coins
    cursor.execute(update_player_sql, (-amount, price, sell_id))
    # deduct the coins of buyer, and raise his/her the goods
    cursor.execute(update_player_sql, (amount, -price, buy_id))


def trade(connection: Connection, sell_id: str, buy_id: str, amount: int, price: int) -> None:
    with connection.cursor() as cursor:
        if trade_check(cursor, sell_id, buy_id, amount, price) is False:
            connection.rollback()
            return

        try:
            trade_update(cursor, sell_id, buy_id, amount, price)
        except Exception as err:
            connection.rollback()
            print(f'something went wrong: {err}')
        else:
            connection.commit()
            print("trade success")


def simple_example() -> None:
    with get_connection(autocommit=True) as conn:
        with conn.cursor() as cur:
            # create a player, who has a coin and a goods.
            create_player(cur, ("test", 1, 1))

            # get this player, and print it.
            test_player = get_player(cur, "test")
            print(f'id:{test_player[0]}, coins:{test_player[1]}, goods:{test_player[2]}')

            # create players with bulk inserts.
            # insert 1919 players totally, with 114 players per batch.
            # each player has a random UUID
            player_list = random_player(1919)
            for idx in range(0, len(player_list), 114):
                bulk_create_player(cur, player_list[idx:idx + 114])

            # print the number of players
            count = get_count(cur)
            print(f'number of players: {count}')

            # print 3 players.
            three_players = get_players_with_limit(cur, 3)
            for player in three_players:
                print(f'id:{player[0]}, coins:{player[1]}, goods:{player[2]}')


def trade_example() -> None:
    with get_connection(autocommit=False) as conn:
        with conn.cursor() as cur:
            # create two players
            # player 1: id is "1", has only 100 coins.
            # player 2: id is "2", has 114514 coins, and 20 goods.
            create_player(cur, ("1", 100, 0))
            create_player(cur, ("2", 114514, 20))
            conn.commit()

        # player 1 wants to buy 10 goods from player 2.
        # it will cost 500 coins, but player 1 cannot afford it.
        # so this trade will fail, and nobody will lose their coins or goods
        trade(conn, sell_id="2", buy_id="1", amount=10, price=500)

        # then player 1 has to reduce the incoming quantity to 2.
        # this trade will be successful
        trade(conn, sell_id="2", buy_id="1", amount=2, price=100)

        # let's take a look for player 1 and player 2 currently
        with conn.cursor() as cur:
            _, player1_coin, player1_goods = get_player(cur, "1")
            print(f'id:1, coins:{player1_coin}, goods:{player1_goods}')
            _, player2_coin, player2_goods = get_player(cur, "2")
            print(f'id:2, coins:{player2_coin}, goods:{player2_goods}')


simple_example()
trade_example()
```

Driver 有着更低的封装程度，因此我们可以在程序内见到大量的 SQL。程序内查询到的 `Player`，与 ORM 不同，因为没有数据对象的存在，`Player` 将以元组 (tuple) 进行表示。

关于 mysqlclient 的更多使用方法，你可以参考 [mysqlclient 官方文档](https://mysqlclient.readthedocs.io/)。

</div>

<div label="使用 PyMySQL" value="PyMySQL">

[PyMySQL](https://pypi.org/project/PyMySQL/) 为当前比较流行的开源 Python Driver 之一。此处将以 PyMySQL **1.0.2** 版本进行说明。虽然 Python 的 Driver 相较其他语言，使用也极其方便。但因其不可屏蔽底层实现，需手动管控事务的特性，如果没有大量必须使用 SQL 的场景，仍然推荐使用 ORM 进行程序编写。这可以降低程序的耦合性。

```python
import uuid
from typing import List

import pymysql.cursors
from pymysql import Connection
from pymysql.cursors import DictCursor


def get_connection(autocommit: bool = False) -> Connection:
    return pymysql.connect(host='127.0.0.1',
                           port=4000,
                           user='root',
                           password='',
                           database='test',
                           cursorclass=DictCursor,
                           autocommit=autocommit)


def create_player(cursor: DictCursor, player: tuple) -> None:
    cursor.execute("INSERT INTO player (id, coins, goods) VALUES (%s, %s, %s)", player)


def get_player(cursor: DictCursor, player_id: str) -> dict:
    cursor.execute("SELECT id, coins, goods FROM player WHERE id = %s", (player_id,))
    return cursor.fetchone()


def get_players_with_limit(cursor: DictCursor, limit: int) -> tuple:
    cursor.execute("SELECT id, coins, goods FROM player LIMIT %s", (limit,))
    return cursor.fetchall()


def random_player(amount: int) -> List[tuple]:
    players = []
    for _ in range(amount):
        players.append((uuid.uuid4(), 10000, 10000))

    return players


def bulk_create_player(cursor: DictCursor, players: List[tuple]) -> None:
    cursor.executemany("INSERT INTO player (id, coins, goods) VALUES (%s, %s, %s)", players)


def get_count(cursor: DictCursor) -> int:
    cursor.execute("SELECT count(*) as count FROM player")
    return cursor.fetchone()['count']


def trade_check(cursor: DictCursor, sell_id: str, buy_id: str, amount: int, price: int) -> bool:
    get_player_with_lock_sql = "SELECT coins, goods FROM player WHERE id = %s FOR UPDATE"

    # sell player goods check
    cursor.execute(get_player_with_lock_sql, (sell_id,))
    seller = cursor.fetchone()
    if seller['goods'] < amount:
        print(f'sell player {sell_id} goods not enough')
        return False

    # buy player coins check
    cursor.execute(get_player_with_lock_sql, (buy_id,))
    buyer = cursor.fetchone()
    if buyer['coins'] < price:
        print(f'buy player {buy_id} coins not enough')
        return False


def trade_update(cursor: DictCursor, sell_id: str, buy_id: str, amount: int, price: int) -> None:
    update_player_sql = "UPDATE player set goods = goods + %s, coins = coins + %s WHERE id = %s"

    # deduct the goods of seller, and raise his/her the coins
    cursor.execute(update_player_sql, (-amount, price, sell_id))
    # deduct the coins of buyer, and raise his/her the goods
    cursor.execute(update_player_sql, (amount, -price, buy_id))


def trade(connection: Connection, sell_id: str, buy_id: str, amount: int, price: int) -> None:
    with connection.cursor() as cursor:
        if trade_check(cursor, sell_id, buy_id, amount, price) is False:
            connection.rollback()
            return

        try:
            trade_update(cursor, sell_id, buy_id, amount, price)
        except Exception as err:
            connection.rollback()
            print(f'something went wrong: {err}')
        else:
            connection.commit()
            print("trade success")


def simple_example() -> None:
    with get_connection(autocommit=True) as connection:
        with connection.cursor() as cur:
            # create a player, who has a coin and a goods.
            create_player(cur, ("test", 1, 1))

            # get this player, and print it.
            test_player = get_player(cur, "test")
            print(test_player)

            # create players with bulk inserts.
            # insert 1919 players totally, with 114 players per batch.
            # each player has a random UUID
            player_list = random_player(1919)
            for idx in range(0, len(player_list), 114):
                bulk_create_player(cur, player_list[idx:idx + 114])

            # print the number of players
            count = get_count(cur)
            print(f'number of players: {count}')

            # print 3 players.
            three_players = get_players_with_limit(cur, 3)
            for player in three_players:
                print(player)


def trade_example() -> None:
    with get_connection(autocommit=False) as connection:
        with connection.cursor() as cur:
            # create two players
            # player 1: id is "1", has only 100 coins.
            # player 2: id is "2", has 114514 coins, and 20 goods.
            create_player(cur, ("1", 100, 0))
            create_player(cur, ("2", 114514, 20))
            connection.commit()

        # player 1 wants to buy 10 goods from player 2.
        # it will cost 500 coins, but player 1 cannot afford it.
        # so this trade will fail, and nobody will lose their coins or goods
        trade(connection, sell_id="2", buy_id="1", amount=10, price=500)

        # then player 1 has to reduce the incoming quantity to 2.
        # this trade will be successful
        trade(connection, sell_id="2", buy_id="1", amount=2, price=100)

        # let's take a look for player 1 and player 2 currently
        with connection.cursor() as cur:
            print(get_player(cur, "1"))
            print(get_player(cur, "2"))


simple_example()
trade_example()
```

Driver 有着更低的封装程度，因此我们可以在程序内见到大量的 SQL。程序内查询到的 `Player`，与 ORM 不同，因为没有数据对象的存在，`Player` 将以 dict 进行表示。

关于 PyMySQL 的更多使用方法，你可以参考 [PyMySQL 官方文档](https://pymysql.readthedocs.io/en/latest/)。

</div>

<div label="使用 mysql-connector-python" value="mysql-connector-python">

[mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/) 为当前比较流行的开源 Python Driver 之一。此处将以 mysql-connector-python **8.0.31** 版本进行说明。虽然 Python 的 Driver 相较其他语言，使用也极其方便。但因其不可屏蔽底层实现，需手动管控事务的特性，如果没有大量必须使用 SQL 的场景，仍然推荐使用 ORM 进行程序编写。这可以降低程序的耦合性。

```python
import uuid
from typing import List

from mysql.connector import connect, MySQLConnection
from mysql.connector.cursor import MySQLCursor


def get_connection(autocommit: bool = True) -> MySQLConnection:
    connection = connect(host='127.0.0.1',
                         port=4000,
                         user='root',
                         password='',
                         database='test')
    connection.autocommit = autocommit
    return connection


def create_player(cursor: MySQLCursor, player: tuple) -> None:
    cursor.execute("INSERT INTO player (id, coins, goods) VALUES (%s, %s, %s)", player)


def get_player(cursor: MySQLCursor, player_id: str) -> tuple:
    cursor.execute("SELECT id, coins, goods FROM player WHERE id = %s", (player_id,))
    return cursor.fetchone()


def get_players_with_limit(cursor: MySQLCursor, limit: int) -> List[tuple]:
    cursor.execute("SELECT id, coins, goods FROM player LIMIT %s", (limit,))
    return cursor.fetchall()


def random_player(amount: int) -> List[tuple]:
    players = []
    for _ in range(amount):
        players.append((str(uuid.uuid4()), 10000, 10000))

    return players


def bulk_create_player(cursor: MySQLCursor, players: List[tuple]) -> None:
    cursor.executemany("INSERT INTO player (id, coins, goods) VALUES (%s, %s, %s)", players)


def get_count(cursor: MySQLCursor) -> int:
    cursor.execute("SELECT count(*) FROM player")
    return cursor.fetchone()[0]


def trade_check(cursor: MySQLCursor, sell_id: str, buy_id: str, amount: int, price: int) -> bool:
    get_player_with_lock_sql = "SELECT coins, goods FROM player WHERE id = %s FOR UPDATE"

    # sell player goods check
    cursor.execute(get_player_with_lock_sql, (sell_id,))
    _, sell_goods = cursor.fetchone()
    if sell_goods < amount:
        print(f'sell player {sell_id} goods not enough')
        return False

    # buy player coins check
    cursor.execute(get_player_with_lock_sql, (buy_id,))
    buy_coins, _ = cursor.fetchone()
    if buy_coins < price:
        print(f'buy player {buy_id} coins not enough')
        return False


def trade_update(cursor: MySQLCursor, sell_id: str, buy_id: str, amount: int, price: int) -> None:
    update_player_sql = "UPDATE player set goods = goods + %s, coins = coins + %s WHERE id = %s"

    # deduct the goods of seller, and raise his/her the coins
    cursor.execute(update_player_sql, (-amount, price, sell_id))
    # deduct the coins of buyer, and raise his/her the goods
    cursor.execute(update_player_sql, (amount, -price, buy_id))


def trade(connection: MySQLConnection, sell_id: str, buy_id: str, amount: int, price: int) -> None:
    with connection.cursor() as cursor:
        if trade_check(cursor, sell_id, buy_id, amount, price) is False:
            connection.rollback()
            return

        try:
            trade_update(cursor, sell_id, buy_id, amount, price)
        except Exception as err:
            connection.rollback()
            print(f'something went wrong: {err}')
        else:
            connection.commit()
            print("trade success")


def simple_example() -> None:
    with get_connection(autocommit=True) as connection:
        with connection.cursor() as cur:
            # create a player, who has a coin and a goods.
            create_player(cur, ("test", 1, 1))

            # get this player, and print it.
            test_player = get_player(cur, "test")
            print(f'id:{test_player[0]}, coins:{test_player[1]}, goods:{test_player[2]}')

            # create players with bulk inserts.
            # insert 1919 players totally, with 114 players per batch.
            # each player has a random UUID
            player_list = random_player(1919)
            for idx in range(0, len(player_list), 114):
                bulk_create_player(cur, player_list[idx:idx + 114])

            # print the number of players
            count = get_count(cur)
            print(f'number of players: {count}')

            # print 3 players.
            three_players = get_players_with_limit(cur, 3)
            for player in three_players:
                print(f'id:{player[0]}, coins:{player[1]}, goods:{player[2]}')


def trade_example() -> None:
    with get_connection(autocommit=False) as conn:
        with conn.cursor() as cur:
            # create two players
            # player 1: id is "1", has only 100 coins.
            # player 2: id is "2", has 114514 coins, and 20 goods.
            create_player(cur, ("1", 100, 0))
            create_player(cur, ("2", 114514, 20))
            conn.commit()

        # player 1 wants to buy 10 goods from player 2.
        # it will cost 500 coins, but player 1 cannot afford it.
        # so this trade will fail, and nobody will lose their coins or goods
        trade(conn, sell_id="2", buy_id="1", amount=10, price=500)

        # then player 1 has to reduce the incoming quantity to 2.
        # this trade will be successful
        trade(conn, sell_id="2", buy_id="1", amount=2, price=100)

        # let's take a look for player 1 and player 2 currently
        with conn.cursor() as cur:
            _, player1_coin, player1_goods = get_player(cur, "1")
            print(f'id:1, coins:{player1_coin}, goods:{player1_goods}')
            _, player2_coin, player2_goods = get_player(cur, "2")
            print(f'id:2, coins:{player2_coin}, goods:{player2_goods}')


simple_example()
trade_example()
```

Driver 有着更低的封装程度，因此我们可以在程序内见到大量的 SQL。程序内查询到的 `Player`，与 ORM 不同，因为没有数据对象的存在，`Player` 将以 tuple 进行表示。

关于 mysql-connector-python 的更多使用方法，你可以参考 [mysql-connector-python 官方文档](https://dev.mysql.com/doc/connector-python/en/)。

</div>

</SimpleTab>

### 第 3 步：运行代码

本节将逐步介绍代码的运行方法。

#### 第 3 步第 1 部分：表初始化

> **建议：**
>
> 在 Gitpod Playground 中尝试 Python 与 TiDB 的连接：[现在就试试](https://gitpod.io/#https://github.com/pingcap-inc/tidb-example-python)

本示例需手动初始化表，若你使用本地集群，可直接运行：

<SimpleTab groupId="cli">

<div label="MySQL CLI" value="mysql-client">

```shell
mysql --host 127.0.0.1 --port 4000 -u root < player_init.sql
```

</div>

<div label="MyCLI" value="mycli">

```shell
mycli --host 127.0.0.1 --port 4000 -u root --no-warn < player_init.sql
```

</div>

</SimpleTab>

若不使用本地集群，或未安装命令行客户端，请用喜欢的方式（如 Navicat、DBeaver 等 GUI 工具）直接登录集群，并运行 `player_init.sql` 文件内的 SQL 语句。

#### 第 3 步第 2 部分：TiDB Cloud 更改参数

若你使用了 TiDB Cloud Serverless Tier 集群，此处需使用系统本地的 CA 证书，并将证书路径记为 `<ca_path>` 以供后续指代。请参考以下系统相关的证书路径地址：

<SimpleTab groupId="ca">

<div label="MacOS / Alpine" value="MacOS / Alpine">

`/etc/ssl/cert.pem`

</div>

<div label="Debian / Ubuntu / Arch" value="Debian / Ubuntu / Arch">

`/etc/ssl/certs/ca-certificates.crt`

</div>

<div label="RedHat / Fedora / CentOS / Mageia" value="RedHat / Fedora / CentOS / Mageia">

`/etc/pki/tls/certs/ca-bundle.crt`

</div>

<div label="OpenSUSE" value="OpenSUSE">

`/etc/ssl/ca-bundle.pem`

</div>

</SimpleTab>

若设置后仍有证书错误，请查阅 [TiDB Cloud Serverless Tier 安全连接文档](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-tier-clusters)。

<SimpleTab groupId="language">

<div label="使用 SQLAlchemy（推荐）" value="SQLAlchemy">

若你使用 TiDB Cloud Serverless Tier 集群，更改 `sqlalchemy_example.py` 内 `create_engine` 函数的入参：

```python
engine = create_engine('mysql://root:@127.0.0.1:4000/test')
```

若你设定的密码为 `123456`，而且从 TiDB Cloud Serverless Tier 集群面板中得到的连接信息为：

- Endpoint: `xxx.tidbcloud.com`
- Port: `4000`
- User: `2aEp24QWEDLqRFs.root`

那么此处应将 `create_engine` 更改为：

```python
engine = create_engine('mysql://2aEp24QWEDLqRFs.root:123456@xxx.tidbcloud.com:4000/test', connect_args={
    "ssl_mode": "VERIFY_IDENTITY",
    "ssl": {
        "ca": "<ca_path>"
    }
})
```

</div>

<div label="使用 peewee（推荐）" value="peewee">

若你使用 TiDB Cloud Serverless Tier 集群，更改 `peewee_example.py` 内 `connect` 函数的入参：

```python
db = connect('mysql://root:@127.0.0.1:4000/test')
```

若你设定的密码为 `123456`，而且从 TiDB Cloud Serverless Tier 集群面板中得到的连接信息为：

- Endpoint: `xxx.tidbcloud.com`
- Port: `4000`
- User: `2aEp24QWEDLqRFs.root`

那么此处应将 `connect` 更改为：

- peewee 将 PyMySQL 作为 Driver 时：

    ```python
    db = connect('mysql://2aEp24QWEDLqRFs.root:123456@xxx.tidbcloud.com:4000/test', 
        ssl_verify_cert=True, ssl_ca="<ca_path>")
    ```

- peewee 将 mysqlclient 作为 Driver 时：

    ```python
    db = connect('mysql://2aEp24QWEDLqRFs.root:123456@xxx.tidbcloud.com:4000/test',
        ssl_mode="VERIFY_IDENTITY", ssl={"ca": "<ca_path>"}
    ```

由于 peewee 会将参数透传至 Driver 中，使用 peewee 时请注意 Driver 的使用类型。

</div>

<div label="使用 mysqlclient" value="mysqlclient">

若你使用 TiDB Cloud Serverless Tier 集群，更改 `mysqlclient_example.py` 内 `get_connection` 函数：

```python
def get_connection(autocommit: bool = True) -> MySQLdb.Connection:
    return MySQLdb.connect(
        host="127.0.0.1",
        port=4000,
        user="root",
        password="",
        database="test",
        autocommit=autocommit
    )
```

若你设定的密码为 `123456`，而且从 TiDB Cloud Serverless Tier 集群面板中得到的连接信息为：

- Endpoint: `xxx.tidbcloud.com`
- Port: `4000`
- User: `2aEp24QWEDLqRFs.root`

那么此处应将 `get_connection` 更改为：

```python
def get_connection(autocommit: bool = True) -> MySQLdb.Connection:
    return MySQLdb.connect(
        host="xxx.tidbcloud.com",
        port=4000,
        user="2aEp24QWEDLqRFs.root",
        password="123456",
        database="test",
        autocommit=autocommit,
        ssl_mode="VERIFY_IDENTITY",
        ssl={
            "ca": "<ca_path>"
        }
    )
```

</div>

<div label="使用 PyMySQL" value="PyMySQL">

若你使用 TiDB Cloud Serverless Tier 集群，更改 `pymysql_example.py` 内 `get_connection` 函数：

```python
def get_connection(autocommit: bool = False) -> Connection:
    return pymysql.connect(host='127.0.0.1',
                           port=4000,
                           user='root',
                           password='',
                           database='test',
                           cursorclass=DictCursor,
                           autocommit=autocommit)
```

若你设定的密码为 `123456`，而且从 TiDB Cloud Serverless Tier 集群面板中得到的连接信息为：

- Endpoint: `xxx.tidbcloud.com`
- Port: `4000`
- User: `2aEp24QWEDLqRFs.root`

那么此处应将 `get_connection` 更改为：

```python
def get_connection(autocommit: bool = False) -> Connection:
    return pymysql.connect(host='xxx.tidbcloud.com',
                           port=4000,
                           user='2aEp24QWEDLqRFs.root',
                           password='123546',
                           database='test',
                           cursorclass=DictCursor,
                           autocommit=autocommit,
                           ssl_ca='<ca_path>',
                           ssl_verify_cert=True,
                           ssl_verify_identity=True)
```

</div>

<div label="使用 mysql-connector-python" value="mysql-connector-python">

若你使用 TiDB Cloud Serverless Tier 集群，更改 `mysql_connector_python_example.py` 内 `get_connection` 函数：

```python
def get_connection(autocommit: bool = True) -> MySQLConnection:
    connection = connect(host='127.0.0.1',
                         port=4000,
                         user='root',
                         password='',
                         database='test')
    connection.autocommit = autocommit
    return connection
```

若你设定的密码为 `123456`，而且从 TiDB Cloud Serverless Tier 集群面板中得到的连接信息为：

- Endpoint: `xxx.tidbcloud.com`
- Port: `4000`
- User: `2aEp24QWEDLqRFs.root`

那么此处应将 `get_connection` 更改为：

```python
def get_connection(autocommit: bool = True) -> MySQLConnection:
    connection = connect(
        host="xxx.tidbcloud.com",
        port=4000,
        user="2aEp24QWEDLqRFs.root",
        password="123456",
        database="test",
        autocommit=autocommit,
        ssl_ca='<ca_path>',
        ssl_verify_identity=True
    )
    connection.autocommit = autocommit
    return connection
```

</div>

</SimpleTab>

#### 第 3 步第 3 部分：运行

运行前请先安装依赖：

```bash
pip3 install -r requirement.txt
```

当以后需要多次运行脚本时，请在每次运行前先依照[表初始化](#第-3-步第-1-部分表初始化)一节再次进行表初始化。

<SimpleTab groupId="language">

<div label="使用 SQLAlchemy（推荐）" value="SQLAlchemy">

```bash
python3 sqlalchemy_example.py
```

</div>

<div label="使用 peewee（推荐）" value="peewee">

```bash
python3 peewee_example.py
```

</div>

<div label="使用 mysqlclient" value="mysqlclient">

```bash
python3 mysqlclient_example.py
```

</div>

<div label="使用 PyMySQL" value="PyMySQL">

```bash
python3 pymysql_example.py
```

</div>

<div label="使用 mysql-connector-python" value="mysql-connector-python">

```bash
python3 mysql_connector_python_example.py
```

</div>

</SimpleTab>

### 第 4 步：预期输出

<SimpleTab groupId="language">

<div label="使用 SQLAlchemy（推荐）" value="SQLAlchemy">

[SQLAlchemy 预期输出](https://github.com/pingcap-inc/tidb-example-python/blob/main/Expected-Output.md#SQLAlchemy)

</div>

<div label="使用 peewee（推荐）" value="peewee">

[peewee 预期输出](https://github.com/pingcap-inc/tidb-example-python/blob/main/Expected-Output.md#peewee)

</div>

<div label="使用 mysqlclient" value="mysqlclient">

[mysqlclient 预期输出](https://github.com/pingcap-inc/tidb-example-python/blob/main/Expected-Output.md#mysqlclient)

</div>

<div label="使用 PyMySQL" value="PyMySQL">

[PyMySQL 预期输出](https://github.com/pingcap-inc/tidb-example-python/blob/main/Expected-Output.md#PyMySQL)

</div>

<div label="使用 mysql-connector-python" value="mysql-connector-python">

[mysql-connector-python 预期输出](https://github.com/pingcap-inc/tidb-example-python/blob/main/Expected-Output.md#mysql-connector-python)

</div>

</SimpleTab>



# 连接到 TiDB

---
title: 选择驱动或 ORM 框架
summary: 选择驱动或 ORM 框架连接 TiDB。
---

## 选择驱动或 ORM 框架

> **注意：**
>
> TiDB 支持等级说明：
>
> - **Full**：表明 TiDB 已经兼容该工具的绝大多数功能，并且在该工具的新版本中对其保持兼容。PingCAP 将定期地对 [TiDB 支持的第三方工具](#tidb-支持的第三方工具)中的新版本进行兼容性测试。
> - **Compatible**：表明由于该工具已适配 MySQL，而 TiDB 高度兼容 MySQL 协议，因此 TiDB 可以兼容该工具的大部分功能。但 PingCAP 并未对该工具作出完整的兼容性验证，有可能出现一些意外的行为。
>
> 关于更多 TiDB 支持的第三方工具，你可以查看 [TiDB 支持的第三方工具](#tidb-支持的第三方工具)。

TiDB 兼容 MySQL 的协议，但存在部分与 MySQL 不兼容的特性，例如：

TiDB 不支持：

- 存储过程与函数
- 触发器
- 外键约束

TiDB 与 MySQL 有差异：

- 自增 ID：可保证全局唯一，或单 TiDB 节点的自增，但无法保证全局自增。

全部兼容性差异可查看与 MySQL 兼容性对比

### Java

本节介绍 Java 语言的 Driver 及 ORM 的使用方式。

#### Java Drivers

<SimpleTab>
<div label="MySQL-JDBC">

支持等级：**Full**

按照 [MySQL 文档](https://dev.mysql.com/doc/connector-j/8.0/en/)中的说明下载并配置 Java JDBC 驱动程序即可使用。对于 TiDB v6.3.0 及以上版本，建议使用 MySQL Connector/J 8.0.29 及以上版本。

> **建议：**
>
> 因为当前 8.0.30 版本有未合并的 [Bug 修复](https://bugs.mysql.com/bug.php?id=106252)，在与 TiDB v6.3.0 以前版本共同使用时，可能会导致线程卡死。因此，对于 v6.3.0 以前的 TiDB 版本，在 MySQL Connector/J 8.0 合并此修复之前，建议不要升级至 8.0 版本。此外，你也可以使用 TiDB 版本的 MySQL Connector/J，它是一个 fork 版本，修复了此 Bug。（详情见 *TiDB-JDBC* 标签）

有关一个完整的实例应用程序，可参阅使用 [TiDB 和 JDBC 构建一个 Java 应用](#第-2-步获取代码)。

</div>
<div label="TiDB-JDBC">

支持等级：**Full**

[TiDB-JDBC](https://github.com/pingcap/mysql-connector-j) 是基于 MySQL 8.0.29 的定制版本。TiDB-JDBC 基于 MySQL 官方 8.0.29 版本编译，修复了原 JDBC 在 prepare 模式下多参数、多字段 EOF 的错误，并新增 TiCDC snapshot 自动维护和 SM3 认证插件等功能。

基于 SM3 的认证仅在 TiDB 版本的 MySQL Connector/J 中支持。

如果你使用的是 **Maven**，请将以下内容添加到你的 `<dependencies></dependencies>`：

```xml
<dependency>
  <groupId>io.github.lastincisor</groupId>
  <artifactId>mysql-connector-java</artifactId>
  <version>8.0.29-tidb-1.0.0</version>
</dependency>
```

如果你需要使用 SM3 认证，请将以下内容添加到你的 `<dependencies></dependencies>`：

```xml
<dependency>
  <groupId>io.github.lastincisor</groupId>
  <artifactId>mysql-connector-java</artifactId>
  <version>8.0.29-tidb-1.0.0</version>
</dependency>
<dependency>
    <groupId>org.bouncycastle</groupId>
    <artifactId>bcprov-jdk15on</artifactId>
    <version>1.67</version>
</dependency>
<dependency>
    <groupId>org.bouncycastle</groupId>
    <artifactId>bcpkix-jdk15on</artifactId>
    <version>1.67</version>
</dependency>
```

如果你使用的是 Gradle，请将以下内容添加到你的 `dependencies`：

```gradle
implementation group: 'io.github.lastincisor', name: 'mysql-connector-java', version: '8.0.29-tidb-1.0.0'
implementation group: 'org.bouncycastle', name: 'bcprov-jdk15on', version: '1.67'
implementation group: 'org.bouncycastle', name: 'bcpkix-jdk15on', version: '1.67'
```

</div>
</SimpleTab>

#### Java ORM 框架

> **注意：**
>
> - Hibernate 当前[不支持嵌套事务](https://stackoverflow.com/questions/37927208/nested-transaction-in-spring-app-with-jpa-postgres)。
> - TiDB 从 v6.2.0 版本开始支持 Savepoint。如需在 `@Transactional` 中使用 `Propagation.NESTED` 事务传播选项，即 `@Transactional(propagation = Propagation.NESTED)`，请确认你的 TiDB 版本为 v6.2.0 或以上。

<SimpleTab>
<div label="Hibernate">

支持等级：**Full**

你可以使用 [Gradle](https://gradle.org/install) 或 [Maven](https://maven.apache.org/install.html) 获取你的应用程序的所有依赖项，且会帮你下载依赖项的间接依赖，而无需你手动管理复杂的依赖关系。注意，只有 Hibernate `6.0.0.Beta2` 及以上版本才支持 TiDB 方言。

如果你使用的是 **Maven**，请将以下内容添加到你的 `<dependencies></dependencies>`：

```xml
<dependency>
    <groupId>org.hibernate.orm</groupId>
    <artifactId>hibernate-core</artifactId>
    <version>6.0.0.CR2</version>
</dependency>

<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>5.1.49</version>
</dependency>
```

如果你使用的是 `Gradle`，请将以下内容添加到你的 `dependencies`：

```gradle
implementation 'org.hibernate:hibernate-core:6.0.0.CR2'
implementation 'mysql:mysql-connector-java:5.1.49'
```

- 有关原生 Java 使用 Hibernate 进行 TiDB 应用程序构建的例子，可参阅 [TiDB 和 Java 的简单 CRUD 应用程序 - 使用 Hibernate](#第-2-步获取代码)。
- 有关 Spring 使用 Spring Data JPA、Hibernate 进行 TiDB 应用程序构建的例子，可参阅[使用 Spring Boot 构建 TiDB 应用程序](#使用-spring-boot-构建-tidb-应用程序)。

额外的，你需要在 [Hibernate 配置文件](https://www.tutorialspoint.com/hibernate/hibernate_configuration.htm)中指定 TiDB 方言： `org.hibernate.dialect.TiDBDialect`，此方言在 Hibernate `6.0.0.Beta2` 以上才可支持。若你无法升级 Hibernate 版本，那么请你直接使用 MySQL 5.7 的方言 `org.hibernate.dialect.MySQL57Dialect`。但这可能造成不可预料的使用结果，及部分 TiDB 特有特性的缺失，如：序列等。

</div>

<div label="MyBatis">

支持等级：**Full**

你可以使用 [Gradle](https://gradle.org/install) 或 [Maven](https://maven.apache.org/install.html) 获取应用程序的所有依赖项包括间接依赖，无需手动管理复杂的依赖关系。

如果你使用的是 Maven，请将以下内容添加到你的 `<dependencies></dependencies>`：

```xml
<dependency>
    <groupId>org.mybatis</groupId>
    <artifactId>mybatis</artifactId>
    <version>3.5.9</version>
</dependency>

<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>5.1.49</version>
</dependency>
```

如果你使用的是 Gradle，请将以下内容添加到你的 `dependencies`：

```gradle
implementation 'org.mybatis:mybatis:3.5.9'
implementation 'mysql:mysql-connector-java:5.1.49'
```

使用 MyBatis 进行 TiDB 应用程序构建的例子，可参阅 [TiDB 和 Java 的简单 CRUD 应用程序 - 使用 Mybatis](#第-2-步获取代码)。

</div>

</SimpleTab>

#### Java 客户端负载均衡

**tidb-loadbalance**

支持等级：**Full**

[tidb-loadbalance](https://github.com/pingcap/tidb-loadbalance) 是应用端的负载均衡组件。通过 tidb-loadbalance，你可以实现自动维护 TiDB server 的节点信息，根据节点信息使用 tidb-loadbalance 策略在客户端分发 JDBC 连接。客户端应用与 TiDB server 之间使用 JDBC 直连，性能高于使用负载均衡组件。

目前 tidb-loadbalance 已实现轮询、随机、权重等负载均衡策略。

> **注意：**
>
> tidb-loadbalance 需配合 mysql-connector-j 一起使用。

如果你使用的是 **Maven**，请将以下内容添加到你的 `<dependencies></dependencies>`：

```xml
<dependency>
  <groupId>io.github.lastincisor</groupId>
  <artifactId>mysql-connector-java</artifactId>
  <version>8.0.29-tidb-1.0.0</version>
</dependency>
<dependency>
  <groupId>io.github.lastincisor</groupId>
  <artifactId>tidb-loadbalance</artifactId>
  <version>0.0.5</version>
</dependency>
```

如果你使用的是 Gradle，请将以下内容添加到你的 `dependencies`：

```gradle
implementation group: 'io.github.lastincisor', name: 'mysql-connector-java', version: '8.0.29-tidb-1.0.0'
implementation group: 'io.github.lastincisor', name: 'tidb-loadbalance', version: '0.0.5'
```

### Golang

本节介绍 Golang 语言的 Driver 及 ORM 的使用方式。

#### Golang Drivers

**go-sql-driver/mysql**

支持等级：**Full**

按照 [go-sql-driver/mysql 文档](https://github.com/go-sql-driver/mysql)中的说明获取并配置 Golang 驱动程序即可使用。

有关一个完整的实例应用程序，可参阅使用 [TiDB 和 go-sql-driver/mysql 构建一个 Golang 应用](#第-2-步获取代码)。

#### Golang ORM 框架

**GORM**

支持等级：**Full**

GORM 是一个流行的 Golang 的 ORM 框架，你可以使用 `go get` 获取你的应用程序的所有依赖项。

```shell
go get -u gorm.io/gorm
go get -u gorm.io/driver/mysql
```

使用 GORM 进行 TiDB 应用程序构建的例子，可参阅 [TiDB 和 Golang 的简单 CRUD 应用程序 - 使用 GORM](#第-2-步获取代码)。

### Python

本节介绍 Python 语言的 Driver 及 ORM 的使用方式。

#### Python Drivers

<SimpleTab>
<div label="PyMySQL">

支持等级：**Compatible**

按照 [PyMySQL 文档](https://pypi.org/project/PyMySQL/)中的说明下载并配置驱动程序即可使用。建议使用 **1.0.2** 及以上版本。

使用 PyMySQL 构建 TiDB 应用程序的例子，可参阅 [TiDB 和 Python 的简单 CRUD 应用程序 - 使用 PyMySQL](#第-2-步获取代码)。

</div>
<div label="mysqlclient">

支持等级：**Compatible**

按照 [mysqlclient 文档](https://pypi.org/project/mysqlclient/)中的说明下载并配置驱动程序即可使用。建议使用 **2.1.1** 及以上版本。

使用 mysqlclient 构建 TiDB 应用程序的例子，可参阅 [TiDB 和 Python 的简单 CRUD 应用程序 - 使用 mysqlclient](#第-2-步获取代码)。

</div>
<div label="mysql-connector-python">

支持等级：**Compatible**

按照 [mysql-connector-python 文档](https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html)中的说明下载并配置驱动程序即可使用。建议使用 **8.0.31** 及以上版本。

使用 mysql-connector-python 构建 TiDB 应用程序的例子，可参阅 [TiDB 和 Python 的简单 CRUD 应用程序 - 使用 mysql-connector-python](#第-2-步获取代码)。

</div>
</SimpleTab>

#### Python ORM 框架

<SimpleTab>
<div label="SQLAlchemy">

支持等级：**Compatible**

[SQLAlchemy](https://www.sqlalchemy.org/) 是一个流行的 Python 的 ORM 框架，你可以使用 `pip install SQLAlchemy==1.4.44` 获取你的应用程序的所有依赖项。建议使用 **1.4.44** 及以上版本。

使用 SQLAlchemy 构建 TiDB 应用程序的例子，可参阅 [TiDB 和 Python 的简单 CRUD 应用程序 - 使用 SQLAlchemy](#第-2-步获取代码)。

</div>
<div label="peewee">

支持等级：**Compatible**

[peewee](http://docs.peewee-orm.com/en/latest/) 是一个流行的 Python 的 ORM 框架，你可以使用 `pip install peewee==3.15.4` 获取你的应用程序的所有依赖项。建议使用 **3.15.4** 及以上版本。

使用 peewee 构建 TiDB 应用程序的例子，可参阅 [TiDB 和 Python 的简单 CRUD 应用程序 - 使用 peewee](#第-2-步获取代码)。

</div>
</SimpleTab>


---
title: 连接到 TiDB
summary: 介绍连接到 TiDB 的方法。
---

## 连接到 TiDB

**TiDB** 高度兼容 **MySQL** 协议，全量的客户端连接参数列表，请参阅 [MySQL Client Options](https://dev.mysql.com/doc/refman/5.7/en/mysql-command-options.html)。

TiDB 支持 [MySQL 客户端/服务器协议](https://dev.mysql.com/doc/internals/en/client-server-protocol.html)。这使得大多数客户端驱动程序和 ORM 框架可以像连接到 MySQL 一样地连接到 TiDB。

### MySQL Client

你可以使用 MySQL Client 作为 TiDB 的命令行工具。在 [MySQL Shell 官方文档](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install.html) 你可以找到不同操作系统的安装方式。在安装完后你可以使用如下命令行连接到 TiDB：



```shell
mysql --host <tidb_server_host> --port 4000 -u root -p --comments
```

注意：MySQL 命令行客户端在 5.7.7 版本之前默认清除了 Optimizer Hints。如果需要在这些早期版本的客户端中使用 Hint 语法，需要在启动客户端时加上 `--comments` 选项。

### JDBC

你可以使用 [JDBC](https://dev.mysql.com/doc/connector-j/8.0/en/) 驱动连接到 TiDB，这需要创建一个 `MysqlDataSource` 或 `MysqlConnectionPoolDataSource` 对象（它们都实现了 `DataSource` 接口），并使用 `setURL` 函数设置连接字符串。

例如：



```java
MysqlDataSource mysqlDataSource = new MysqlDataSource();
mysqlDataSource.setURL("jdbc:mysql://{host}:{port}/{database}?user={username}&password={password}");
```

有关 JDBC 连接的更多信息，可参考 [JDBC 官方文档](https://dev.mysql.com/doc/connector-j/8.0/en/)。

**连接参数**

|    参数名    |                                                描述                                                |
| :----------: | :------------------------------------------------------------------------------------------------: |
| `{username}` | 需要连接到 TiDB 集群的 SQL 用户 |
| `{password}` |                               需要连接到 TiDB 集群的 SQL 用户的密码                                |
|   `{host}`   |               TiDB 节点运行的 [Host](<https://en.wikipedia.org/wiki/Host_(network)>)               |
|   `{port}`   |                                      TiDB 节点正在监听的端口                                       |
| `{database}` |                                      (已经存在的)数据库的名称                                      |

### Hibernate

你可以使用 [Hibernate ORM](https://hibernate.org/orm/) 连接到 TiDB，请将 Hibernate 的配置中的 `hibernate.connection.url` 设置为合法的 TiDB 连接字符串。

例如，你的配置被写在 `hibernate.cfg.xml` 文件中，那么你的配置文件应该为：



```xml
<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE hibernate-configuration PUBLIC
        "-//Hibernate/Hibernate Configuration DTD 3.0//EN"
        "http://www.hibernate.org/dtd/hibernate-configuration-3.0.dtd">
<hibernate-configuration>
    <session-factory>
        <property name="hibernate.connection.driver_class">com.mysql.cj.jdbc.Driver</property>
        <property name="hibernate.dialect">org.hibernate.dialect.TiDBDialect</property>
        <property name="hibernate.connection.url">jdbc:mysql://{host}:{port}/{database}?user={user}&amp;password={password}</property>
    </session-factory>
</hibernate-configuration>
```

随后，使用代码读取配置文件，从而获得 `SessionFactory` 对象：



```java
SessionFactory sessionFactory = new Configuration().configure("hibernate.cfg.xml").buildSessionFactory();
```

这里有几个需要注意的点：

1. 因为使用的配置文件 `hibernate.cfg.xml` 为 XML 格式，而 `&` 字符，在 XML 中属于特殊字符，因此，需将 `&` 更改为 `&amp;`。即，连接字符串 `hibernate.connection.url` 由 `jdbc:mysql://{host}:{port}/{database}?user={user}&password={password}` 改为了 `jdbc:mysql://{host}:{port}/{database}?user={user}&amp;password={password}`。
2. 在你使用 Hibernate 时，建议使用 TiDB 方言，即 `hibernate.dialect` 设置为 `org.hibernate.dialect.TiDBDialect`。
3. Hibernate 在版本 `6.0.0.Beta2` 及以上可支持 TiDB 方言，因此推荐使用 `6.0.0.Beta2` 及以上版本的 Hibernate。

更多有关 Hibernate 连接参数的信息，请参阅 [Hibernate 官方文档](https://hibernate.org/orm/documentation)。

**连接参数**

|    参数名    |                                                描述                                                |
| :----------: | :------------------------------------------------------------------------------------------------: |
| `{username}` | 需要连接到 TiDB 集群的 SQL 用户 |
| `{password}` |                               需要连接到 TiDB 集群的 SQL 用户的密码                                |
|   `{host}`   |               TiDB 节点运行的 [Host](<https://en.wikipedia.org/wiki/Host_(network)>)               |
|   `{port}`   |                                      TiDB 节点正在监听的端口                                       |
| `{database}` |                                      (已经存在的)数据库的名称                                      |


---
title: 连接池与连接参数
summary: 针对开发者的 TiDB 连接池与连接参数的说明。
---

## 连接池与连接参数

> - 连接池参数 - 连接数配置、探活配置两节摘自 [开发 Java 应用使用 TiDB 的最佳实践 - 连接池](#连接池)。
> - 连接参数摘自 [开发 Java 应用使用 TiDB 的最佳实践 - JDBC](#jdbc)。

### 连接池参数

TiDB (MySQL) 连接建立是比较昂贵的操作（至少对于 OLTP 来讲），除了建立 TCP 连接外还需要进行连接鉴权操作，所以客户端通常会把 TiDB (MySQL) 连接保存到连接池中进行复用。

Java 的连接池实现很多 ([HikariCP](https://github.com/brettwooldridge/HikariCP), [tomcat-jdbc](https://tomcat.apache.org/tomcat-7.0-doc/jdbc-pool.html), [durid](https://github.com/alibaba/druid), [c3p0](https://www.mchange.com/projects/c3p0/), [dbcp](https://commons.apache.org/proper/commons-dbcp/))，TiDB 不会限定使用的连接池，应用可以根据业务特点自行选择连接池实现。

#### 连接数配置

比较常见的是应用需要根据自身情况配置合适的连接池大小，以 HikariCP 为例：

**maximumPoolSize**：连接池最大连接数，配置过大会导致 TiDB 消耗资源维护无用连接，配置过小则会导致应用获取连接变慢，所以需根据应用自身特点配置合适的值，可参考[这篇文章](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing)。

**minimumIdle**：连接池最小空闲连接数，主要用于在应用空闲时存留一些连接以应对突发请求，同样是需要根据业务情况进行配置。

应用在使用连接池时，需要注意连接使用完成后归还连接，推荐应用使用对应的连接池相关监控（如 **metricRegistry**），通过监控能及时定位连接池问题。

#### 探活配置

连接池维护到 TiDB 的长连接，TiDB 默认不会主动关闭客户端连接（除非报错），但一般客户端到 TiDB 之间还会有 [LVS](https://en.wikipedia.org/wiki/Linux_Virtual_Server) 或 [HAProxy](https://en.wikipedia.org/wiki/HAProxy) 之类的网络代理，它们通常会在连接空闲一定时间后主动清理连接。除了注意代理的 idle 配置外，连接池还需要进行保活或探测连接。

如果常在 Java 应用中看到以下错误：

```
The last packet sent successfully to the server was 3600000 milliseconds ago. The driver has not received any packets from the server. com.mysql.jdbc.exceptions.jdbc4.CommunicationsException: Communications link failure
```

如果 `n milliseconds ago` 中的 n 如果是 0 或很小的值，则通常是执行的 SQL 导致 TiDB 异常退出引起的报错，推荐查看 TiDB stderr 日志；如果 n 是一个非常大的值（比如这里的 3600000），很可能是因为这个连接空闲太久然后被中间 proxy 关闭了，通常解决方式除了调大 proxy 的 idle 配置，还可以让连接池执行以下操作：

- 每次使用连接前检查连接是否可用。
- 使用单独线程定期检查连接是否可用。
- 定期发送 test query 保活连接。

不同的连接池实现可能会支持其中一种或多种方式，可以查看所使用的连接池文档来寻找对应配置。

#### 经验公式

在 HikariCP 的 [About Pool Sizing](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing) 一文中可以了解到，在完全不知道如何设置数据库连接池大小的时候，可以考虑以以下[经验公式](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing#connections--core_count--2--effective_spindle_count)为起点，在此基础上，围绕该结果进行尝试，以得到最高性能的连接池大小。

该经验公式描述如下：

```
connections = ((core_count * 2) + effective_spindle_count)
```

解释一下参数含义：

- **connections**: 得出的连接数大小。
- **core_count**: CPU 核心数。
- **effective_spindle_count**: 直译为**有效主轴数**，实际上是说你有多少个硬盘（非 [SSD](https://en.wikipedia.org/wiki/Solid-state_drive)），因为每个旋转的硬盘可以被称为是一个旋转轴。例如，你使用的是一个有 16 个磁盘组成的 [RAID](https://en.wikipedia.org/wiki/RAID) 阵列的服务器，那么 **effective_spindle_count** 应为 16。此处经验公式，实际上是衡量你的服务器可以管理多少 I/O 并发请求，因为 **HDD** 通常只能串行请求。

要特别说明的是，在这个经验公式的的下方，也看到了一处说明：

> ```
> A formula which has held up pretty well across a lot of benchmarks for years is
> that for optimal throughput the number of active connections should be somewhere
> near ((core_count * 2) + effective_spindle_count). Core count should not include
> HT threads, even if hyperthreading is enabled. Effective spindle count is zero if
> the active data set is fully cached, and approaches the actual number of spindles
> as the cache hit rate falls. ... There hasn't been any analysis so far regarding
> how well the formula works with SSDs.
> ```

这个说明指出：

1. **core_count** 就是 _物理核心数_ ，与你是否开启[超线程](https://en.wikipedia.org/wiki/Hyper-threading)无关。
2. 数据被全量缓存时，**effective_spindle_count** 应被设置为 0，随着命中率的下降，会更加接近实际的 HDD 个数。
3. **这里没有任何基于 _SSD_ 的经验公式。**

这里的说明让你在使用 SSD 时，需探求其他的经验公式。

可以参考 CockroachDB 对[数据库连接池](https://www.cockroachlabs.com/docs/stable/connection-pooling.html?#sizing-connection-pools)中的描述，推荐的连接数大小公式为：

```
connections = (number of cores * 4)
```

因此，你在使用 SSD 的情况下可以将连接数设置为 `CPU 核心数 * 4`。以此来达到初始的连接池最大连接数大小，并以此数据周围进行进一步的调整。

#### 调整方向

可以看到，在上方的[经验公式](#经验公式)中得到的，是一个推荐的初始值，若需得到某台具体机器上的最佳值，需在推荐值周围，通过尝试，得到最佳值。

此最佳值的获取，会有一些基本规律，此处罗列如下：

1. 如果你的网络或存储延迟较大，请增大你的最大连接数，可以进行等待，从而让线程在被阻塞时，其他的线程可继续进行处理。
2. 如果你的服务器上部署了多个服务，并且每个服务拥有独立的连接池时，请关注它们的连接池的最大连接数总和。

### 连接参数

Java 应用尽管可以选择在不同的框架中封装，但在最底层一般会通过调用 JDBC 来与数据库服务器进行交互。对于 JDBC，需要关注的主要有：API 的使用选择和 API Implementer 的参数配置。

#### JDBC API

对于基本的 JDBC API 使用可以参考 [JDBC 官方教程](https://docs.oracle.com/javase/tutorial/jdbc/)，本文主要强调几个比较重要的 API 选择。

#### 使用 Prepare API

对于 OLTP 场景，程序发送给数据库的 SQL 语句在去除参数变化后都是可穷举的某几类，因此建议使用[预处理语句 (Prepared Statements)](https://docs.oracle.com/javase/tutorial/jdbc/basics/prepared.html) 代替普通的[文本执行](https://docs.oracle.com/javase/tutorial/jdbc/basics/processingsqlstatements.html#executing_queries)，并复用预处理语句来直接执行，从而避免 TiDB 重复解析和生成 SQL 执行计划的开销。

目前多数上层框架都会调用 Prepare API 进行 SQL 执行，如果直接使用 JDBC API 进行开发，注意选择使用 Prepare API。

另外需要注意 MySQL Connector/J 实现中默认只会做客户端的语句预处理，会将 `?` 在客户端替换后以文本形式发送到服务端，所以除了要使用 Prepare API，还需要在 JDBC 连接参数中配置 `useServerPrepStmts = true`，才能在 TiDB 服务器端进行语句预处理（下面参数配置章节有详细介绍）。

#### 使用 Batch 批量插入更新

对于批量插入更新，如果插入记录较多，可以选择使用 [addBatch/executeBatch API](https://www.tutorialspoint.com/jdbc/jdbc-batch-processing)。通过 addBatch 的方式将多条 SQL 的插入更新记录先缓存在客户端，然后在 executeBatch 时一起发送到数据库服务器。

> **注意：**
>
> 对于 MySQL Connector/J 实现，默认 Batch 只是将多次 addBatch 的 SQL 发送时机延迟到调用 executeBatch 的时候，但实际网络发送还是会一条条的发送，通常不会降低与数据库服务器的网络交互次数。
>
> 如果希望 Batch 网络发送，需要在 JDBC 连接参数中配置 `rewriteBatchedStatements = true`（下面参数配置章节有详细介绍）。

#### 使用 StreamingResult 流式获取执行结果

一般情况下，为提升执行效率，JDBC 会默认提前获取查询结果并将其保存在客户端内存中。但在查询返回超大结果集的场景中，客户端会希望数据库服务器减少向客户端一次返回的记录数，等客户端在有限内存处理完一部分后再去向服务器要下一批。

在 JDBC 中通常有以下两种处理方式：

- 设置 [**FetchSize** 为 `Integer.MIN_VALUE`](https://dev.mysql.com/doc/connector-j/5.1/en/connector-j-reference-implementation-notes.html#ResultSet) 让客户端不缓存，客户端通过 StreamingResult 的方式从网络连接上流式读取执行结果。
- 使用 Cursor Fetch，首先需[设置 **FetchSize**](http://makejavafaster.blogspot.com/2015/06/jdbc-fetch-size-performance.html) 为正整数，且在 JDBC URL 中配置 `useCursorFetch = true`。

TiDB 中同时支持两种方式，但更推荐使用第一种将 **FetchSize** 设置为 `Integer.MIN_VALUE` 的方式，比第二种功能实现更简单且执行效率更高。

#### MySQL JDBC 参数

JDBC 实现通常通过 JDBC URL 参数的形式来提供实现相关的配置。这里以 MySQL 官方的 Connector/J 来介绍[参数配置](https://dev.mysql.com/doc/connector-j/5.1/en/connector-j-reference-configuration-properties.html)（如果使用的是 MariaDB，可以参考 [MariaDB 的类似配置](https://mariadb.com/kb/en/library/about-mariadb-connector-j/#optional-url-parameters)）。因为配置项较多，这里主要关注几个可能影响到性能的参数。

##### Prepare 相关参数

- **useServerPrepStmts**

    默认情况下，**useServerPrepStmts** 的值为 `false`，即尽管使用了 Prepare API，也只会在客户端做 “prepare”。因此为了避免服务器重复解析的开销，如果同一条 SQL 语句需要多次使用 Prepare API，则建议设置该选项为 `true`。

    在 TiDB 监控中可以通过 **Query Summary > CPS By Instance** 查看请求命令类型，如果请求中 `COM_QUERY` 被 `COM_STMT_EXECUTE` 或 `COM_STMT_PREPARE` 代替即生效。

- **cachePrepStmts**

    虽然 `useServerPrepStmts = true` 能让服务端执行预处理语句，但默认情况下客户端每次执行完后会 close 预处理语句，并不会复用，这样预处理的效率甚至不如文本执行。所以建议开启 `useServerPrepStmts = true` 后同时配置 `cachePrepStmts = true`，这会让客户端缓存预处理语句。

    在 TiDB 监控中可以通过 **Query Summary > CPS By Instance** 查看请求命令类型，如果请求中 `COM_STMT_EXECUTE` 数目远远多于 `COM_STMT_PREPARE` 即生效。

    另外，通过 `useConfigs = maxPerformance` 配置会同时配置多个参数，其中也包括 `cachePrepStmts = true`。

- **prepStmtCacheSqlLimit**

    在配置 **cachePrepStmts** 后还需要注意 **prepStmtCacheSqlLimit** 配置（默认为 `256`），该配置控制客户端缓存预处理语句的最大长度，超过该长度将不会被缓存。

    在一些场景 SQL 的长度可能超过该配置，导致预处理 SQL 不能复用，建议根据应用 SQL 长度情况决定是否需要调大该值。

    在 TiDB 监控中通过 **Query Summary > CPS By Instance** 查看请求命令类型，如果已经配置了 `cachePrepStmts = true`，但 `COM_STMT_PREPARE` 还是和 `COM_STMT_EXECUTE` 基本相等且有 `COM_STMT_CLOSE`，需要检查这个配置项是否设置得太小。

- **prepStmtCacheSize**

    控制缓存的预处理语句数目（默认为 `25`），如果应用需要预处理的 SQL 种类很多且希望复用预处理语句，可以调大该值。

    和上一条类似，在监控中通过 **Query Summary > CPS By Instance** 查看请求中 `COM_STMT_EXECUTE` 数目是否远远多于 `COM_STMT_PREPARE` 来确认是否正常。

##### Batch 相关参数

在进行 batch 写入处理时推荐配置 `rewriteBatchedStatements = true`，在已经使用 `addBatch` 或 `executeBatch` 后默认 JDBC 还是会一条条 SQL 发送，例如：



```java
pstmt = prepare("INSERT INTO `t` (`a`) VALUES(?)");
pstmt.setInt(1, 10);
pstmt.addBatch();
pstmt.setInt(1, 11);
pstmt.addBatch();
pstmt.setInt(1, 12);
pstmt.executeBatch();
```

虽然使用了 batch 但发送到 TiDB 语句还是单独的多条 insert：



```sql
INSERT INTO `t` (`a`) VALUES(10);
INSERT INTO `t` (`a`) VALUES(11);
INSERT INTO `t` (`a`) VALUES(12);
```

如果设置 `rewriteBatchedStatements = true`，发送到 TiDB 的 SQL 将是：



```sql
INSERT INTO `t` (`a`) VALUES(10),(11),(12);
```

需要注意的是，insert 语句的改写，只能将多个 values 后的值拼接成一整条 SQL, insert 语句如果有其他差异将无法被改写。例如：



```sql
INSERT INTO `t` (`a`) VALUES (10) ON DUPLICATE KEY UPDATE `a` = 10;
INSERT INTO `t` (`a`) VALUES (11) ON DUPLICATE KEY UPDATE `a` = 11;
INSERT INTO `t` (`a`) VALUES (12) ON DUPLICATE KEY UPDATE `a` = 12;
```

上述 insert 语句将无法被改写成一条语句。该例子中，如果将 SQL 改写成如下形式：



```sql
INSERT INTO `t` (`a`) VALUES (10) ON DUPLICATE KEY UPDATE `a` = values(`a`);
INSERT INTO `t` (`a`) VALUES (11) ON DUPLICATE KEY UPDATE `a` = values(`a`);
INSERT INTO `t` (`a`) VALUES (12) ON DUPLICATE KEY UPDATE `a` = values(`a`);
```

即可满足改写条件，最终被改写成：



```sql
INSERT INTO `t` (`a`) VALUES (10), (11), (12) ON DUPLICATE KEY UPDATE `a` = values(`a`);
```

批量更新时如果有 3 处或 3 处以上更新，则 SQL 语句会改写为 multiple-queries 的形式并发送，这样可以有效减少客户端到服务器的请求开销，但副作用是会产生较大的 SQL 语句，例如这样：



```sql
UPDATE `t` SET `a` = 10 WHERE `id` = 1;
UPDATE `t` SET `a` = 11 WHERE `id` = 2;
UPDATE `t` SET `a` = 12 WHERE `id` = 3;
```

另外，因为一个[客户端 bug](https://bugs.mysql.com/bug.php?id=96623)，批量更新时如果要配置 `rewriteBatchedStatements = true` 和 `useServerPrepStmts = true`，推荐同时配置 `allowMultiQueries = true` 参数来避免这个 bug。

##### 集成参数

通过监控可能会发现，虽然业务只向集群进行 insert 操作，却看到有很多多余的 select 语句。通常这是因为 JDBC 发送了一些查询设置类的 SQL 语句（例如 `select @@session.transaction_read_only`）。这些 SQL 对 TiDB 无用，推荐配置 `useConfigs = maxPerformance` 来避免额外开销。

`useConfigs = maxPerformance` 会包含一组配置，可查看 mysql-connector-j [8.0 版本](https://github.com/mysql/mysql-connector-j/blob/release/8.0/src/main/resources/com/mysql/cj/configurations/maxPerformance.properties) 或 [5.1 版本](https://github.com/mysql/mysql-connector-j/blob/release/5.1/src/com/mysql/jdbc/configs/maxPerformance.properties) 来确认当前 MySQL JDBC 中 `maxPerformance` 包含的具体配置。

配置后查看监控，可以看到多余语句减少。

##### 超时参数

TiDB 提供两个与 MySQL 兼容的超时控制参数，[`wait_timeout`](#wait_timeout) 和 [`max_execution_time`](#max_execution_time)。这两个参数分别控制与 Java 应用连接的空闲超时时间和连接中 SQL 执行的超时时间，即控制 TiDB 与 Java 应用的连接最长闲多久和最长忙多久。在 TiDB v5.4 及以上版本中，`wait_timeout` 参数默认值为 `28800` 秒，即空闲超时为 8 小时。在 v5.4 之前，`wait_timeout` 参数的默认值为 `0`，即没有时间限制。 `max_execution_time` 参数的默认值为 `0`，即不限制一条 SQL 语句的执行时间。

但在实际生产环境中，空闲连接和一直无限执行的 SQL 对数据库和应用都有不好的影响。你可以通过在应用的连接字符串中配置这两个参数来避免空闲连接和执行时间过长的 SQL 语句。例如，设置 `sessionVariables=wait_timeout=3600`（1 小时）和 `sessionVariables=max_execution_time=300000`（5 分钟）。



# 数据库模式设计

---
title: 概述
summary: TiDB 数据库模式设计的概述。
---

## 概述

本页概述了 TiDB 中的数据库模式。将从本页开始围绕 [Bookshop](#bookshop-应用) 这个应用程序来对 TiDB 的设计数据库部分展开介绍。并使用此数据库做后续数据的写入、读取示例。

### 术语歧义

此处术语会有歧义，为消除歧义，在此作出数据库模式设计文档部分中的术语简要约定：

为避免和通用术语[数据库 (Database)](https://en.wikipedia.org/wiki/Database) 混淆，因此将逻辑对象称为**数据库 (Database)**，TiDB 仍使用原名称，并将 TiDB 的部署实例称为**集群 (Cluster)**。

因为 TiDB 使用与 MySQL 兼容的语法，在此语法下，**模式 (Schema)** 仅代表[通用术语定义](https://en.wiktionary.org/wiki/schema)，并无逻辑对象定义，可参考此[官方文档](https://dev.mysql.com/doc/refman/8.0/en/create-database.html)。若你从其他拥有 **Schema** 逻辑对象的数据库（如：[PostgreSQL](https://www.postgresql.org/docs/current/ddl-schemas.html)、[Oracle](https://docs.oracle.com/en/database/oracle/oracle-database/21/tdddg/creating-managing-schema-objects.html)、[Microsoft SQL Server](https://docs.microsoft.com/en-us/sql/relational-databases/security/authentication-access/create-a-database-schema?view=sql-server-ver15) 等）迁移而来，请注意此区别。

### 数据库 Database

TiDB 语境中的 Database 或者说数据库，可以认为是表和索引等对象的集合。

TiDB 集群包含一个名为 `test` 的数据库。但建议你自行创建数据库，而不是使用 `test` 数据库。

### 表 Table

TiDB 语境中的 Table 或者说表，从属于某个[数据库](#数据库-database)。

表包含数据**行**。每行数据中的每个值都属于一个特定的**列**。每列都只允许单一数据类型的数据值。列可添加约束来进一步限定。你还可以添加[生成列（实验特性）](None)用于计算。

### 索引 Index

索引是单个表中行的副本，按列或列集排序。TiDB 查询使用索引来更有效的查找表内的数据，同时可以给出特定列的值。每个索引都是从属于某个[表](#表-table)的。

索引有两种常见的类型，分别为：

- **Primary Key**: 即主键索引，即标识在主键列上的索引。
- **Secondary Index**: 即二级索引，即在非主键上标识的索引。

> **注意：**
>
> TiDB 中，关于 **Primary Key** 的默认定义与 MySQL 常用存储引擎 [InnoDB](https://mariadb.com/kb/en/innodb/) 不一致。**InnoDB** 中，**Primary Key** 的语义为：唯一，不为空，**且为聚簇索引**。
>
> 而在 TiDB 中，**Primary Key** 的定义为：唯一，不为空。但主键不保证为**聚簇索引**。而是由另一组关键字 `CLUSTERED`、`NONCLUSTERED` 额外控制 **Primary Key** 是否为聚簇索引，若不指定，则由系统变量 `@@global.tidb_enable_clustered_index` 影响，具体说明请看聚簇索引。

#### 专用索引

TiDB 支持一些特殊场景专用的索引，用以提高特定用例中的查询性能。有关这些专用索引的介绍，请参阅以下页面：

|                                                           索引和约束                                                           |   5.4    |   5.3    |   5.2    |   5.1    |   5.0    |   4.0    |
| :----------------------------------------------------------------------------------------------------------------------------: | :------: | :------: | :------: | :------: | :------: | :------: |
| 表达式索引 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 | 实验特性 |
|                         [列式存储 (TiFlash)](None)                         |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |
|                            RocksDB 引擎                            |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |
|                              Titan 插件                              |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |
|                         不可见索引                          |    Y     |    Y     |    Y     |    Y     |    Y     |    N     |
|              复合主键              |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |
|              唯一约束              |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |
|                          整型主键上的聚簇索引                           |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |
|                      复合或非整型主键上的聚簇索引                       |    Y     |    Y     |    Y     |    Y     |    Y     |    N     |

### 其他对象

TiDB 支持一些和**表**同级的对象：

- 视图: 视图是一张虚拟表，该虚拟表的结构由创建视图时的 `SELECT` 语句定义，TiDB 目前不支持物化视图。
- 序列: 创建和存储顺序数据。
- 临时表: 临时表是数据不持久化的表。

### 访问控制

TiDB 支持基于用户或角色的访问控制。你可以通过角色或直接指向用户，从而授予**用户**查看、修改或删除 数据对象和数据模式的权限。

### 执行数据库模式更改

不推荐使用客户端的 Driver 或 ORM 来执行数据库模式的更改。以经验来看，作为最佳实践，建议使用 [MySQL 客户端](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)或使用任意你喜欢的 GUI 客户端来进行数据库模式的更改。本文档中，将在大多数场景下，使用 **MySQL 客户端** 传入 SQL 文件来执行数据库模式的更改。

### 对象大小限制

此处摘录一些常见的对象大小限制，详细使用限制请查阅此文档。

#### 标识符长度限制

|    对象    |  限制   |
| :--------: | :-----: |
| 数据库名称 | 64 字符 |
|   表名称   | 64 字符 |
|   列名称   | 64 字符 |
|  索引名称  | 64 字符 |
|  视图名称  | 64 字符 |
|  序列名称  | 64 字符 |

#### 单个表内限制

|      对象      |                                                                                                                   限制                                                                                                                    |
| :------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|      列数      |                                                                                                       默认为 1017，最大可调至 4096                                                                                                        |
|     索引数     |                                                                                                         默认为 64，最大可调至 512                                                                                                         |
|     分区数     |                                                                                                                   8192                                                                                                                    |
|    单行大小    | 默认为 6MB，可通过 [txn-entry-size-limit](#txn-entry-size-limit-从-v50-版本开始引入) 配置项调整 |
| 单行内单列大小 |                                                                                                                    6MB                                                                                                                    |

#### 字符串类型限制

|   对象    |    限制    |
| :-------: | :--------: |
|   CHAR    |  256 字符  |
|  BINARY   |  256 字节  |
| VARBINARY | 65535 字节 |
|  VARCHAR  | 16383 字符 |
|   TEXT    |    6MB     |
|   BLOB    |    6MB     |

#### 行数

TiDB 可通过增加集群的节点数来支持任意数量的行，原理可阅读 TiDB 最佳实践


---
title: 创建数据库
summary: 创建数据库的方法、规范及例子。
---

## 创建数据库

在这个章节当中，将开始介绍如何使用 SQL 来创建数据库，及创建数据库时应遵守的规则。将在这个章节中围绕 [Bookshop](#bookshop-应用) 这个应用程序来对 TiDB 的创建数据库部分展开介绍。

> **注意：**
>
> 此处仅对 `CREATE DATABASE` 语句进行简单描述，详细参考文档（包含其他示例），可参阅 CREATE DATABASE 文档。

### 在开始之前

在阅读本页面之前，你需要准备以下事项：

- [使用 TiDB Cloud (Serverless Tier) 构建 TiDB 集群](#使用-tidb-cloud-(serverless-tier)-构建-tidb-集群)。
- 阅读[数据库模式概览](#概述)。

### 什么是数据库

在 TiDB 中[数据库](#数据库-database)对象可以包含**表**、**视图**、**序列**等对象。

### 创建数据库过程

可使用 `CREATE DATABASE` 语句来创建数据库。



```sql
CREATE DATABASE IF NOT EXISTS `bookshop`;
```

此语句会创建一个名为 `bookshop` 的数据库（如果尚不存在）。请以 `root` 用户身份执行文件中的建库语句，运行以下命令：



```shell
mysql
    -u root \
    -h {host} \
    -P {port} \
    -p {password} \
    -e "CREATE DATABASE IF NOT EXISTS bookshop;"
```

要查看集群中的数据库，可在命令行执行一条 `SHOW DATABASES` 语句：



```shell
mysql
    -u root \
    -h {host} \
    -P {port} \
    -p {password} \
    -e "SHOW DATABASES;"
```

运行结果为：

```
+--------------------+
| Database           |
+--------------------+
| INFORMATION_SCHEMA |
| PERFORMANCE_SCHEMA |
| bookshop           |
| mysql              |
| test               |
+--------------------+
```

### 数据库创建时应遵守的规则

- 遵循[数据库命名规范](#数据库命名规范)，给你的数据库起一个有意义的名字。
- `test` 数据库是 TiDB 提供的一个默认数据库。如果没有必要，尽量不要在生产环境使用它。你可以自行使用 `CREATE DATABASE` 语句来创建数据库，并且在 SQL 会话中使用 `USE {databasename};` 语句来更改当前数据库。
- 使用 root 用户创建数据库、角色、用户等，并只赋予必要的权限。
- 作为通用的规则，不推荐使用 Driver、ORM 进行数据库模式的定义与更改。相反，请使用 **MySQL 命令行客户端**或其他你喜欢的 **MySQL GUI 客户端**来进行操作。

### 更进一步

至此，你已经准备完毕 `bookshop` 数据库，可以将**表**添加到该数据库中。

你可继续阅读[创建表](#创建表)文档获得相关指引。


---
title: 创建表
summary: 创建表的方法、规范及例子。
---

## 创建表

本文档介绍如何使用 SQL 语句来创建表以及创建表的最佳实践。本文档提供了一个基于 TiDB 的 [bookshop](#bookshop-应用) 数据库的示例加以说明。

> **注意：**
>
> 此处仅对 `CREATE TABLE` 语句进行简单描述，详细参考文档（包含其他示例），可参阅 CREATE TABLE 文档。

### 在开始之前

在阅读本页面之前，你需要准备以下事项：

- [使用 TiDB Cloud (Serverless Tier) 构建 TiDB 集群](#使用-tidb-cloud-(serverless-tier)-构建-tidb-集群)。
- 阅读[数据库模式概览](#概述)。
- [创建一个数据库](#创建数据库)。

### 什么是表

[表](#表-table)是集群中的一种逻辑对象，它从属于[数据库](#数据库-database)，用于保存从 SQL 中发送的数据。表以行和列的形式组织数据记录,一张表至少有一列。若在表中定义了 n 个列，那么每一行数据都将拥有与这 n 个列中完全一致的字段。

### 命名表

创建表的第一步，就是给你的表起个名字。请不要使用无意义的表名，将给未来的你或者你的同事带来极大的困扰。推荐你遵循公司或组织的表命名规范。

`CREATE TABLE` 语句通常采用以下形式：



```sql
CREATE TABLE {table_name} ( {elements} );
```

**参数描述**

- `{table_name}`: 表名。
- `{elements}`: 以逗号分隔的表元素列表，比如列定义，主键定义等。

假设你需要创建一个表来存储 `bookshop` 库中的用户信息。

注意，此时因为一个列都没被添加，所以下方这条 SQL 暂时还不能被运行：



```sql
CREATE TABLE `bookshop`.`users` (
);
```

### 定义列

**列**从属于表，每张表都至少有一**列**。**列**通过将每行中的值分成一个个单一数据类型的小单元来为表提供结构。

列定义通常使用以下形式：

```
{column_name} {data_type} {column_qualification}
```

**参数描述**

- `{column_name}`: 列名。
- `{data_type}`: 列的数据类型。
- `{column_qualification}`: 列的限定条件，如**列级约束**或[生成列（实验功能）](None)子句。

可以为 `users` 表添加一些列，如他们的唯一标识 `id`，余额 `balance` 及昵称 `nickname`。



```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint,
  `nickname` varchar(100),
  `balance` decimal(15,2)
);
```

其中，定义了一个字段名为 `id`，类型为 bigint 的字段。用以表示用户唯一标识。这意味着，所有的用户标识都应该是 `bigint` 类型的。

而在其后，又定义了一个字段名为 `nickname`，类型为 varchar，且长度不得超过 100 字符的字段。用以表示用户的昵称。这意味着，所用用户的昵称都是 `varchar` 类型，且不超过 100 字符的。

最后，又加入了一个字段名为 `balance` 用以表示用户的余额，类型为 decimal，且其精度为 15，比例为 2。简单的说明一下精度和比例代表的含义，精度代表字段数值的总位数，而比例代表小数点后有多少位。例如: `decimal(5,2)`，即精度为 5，比例为 2 时，其取值范围为 `-999.99` 到 `999.99`。`decimal(6,1)` ，即精度为 6，比例为 1 时，其取值范围为 `-99999.9` 到 `99999.9`。`decimal` 类型为定点数，可精确保存数字，在需要精确数字的场景（如用户财产相关）中，请确保使用定点数类型。

TiDB 支持许多其他的列数据类型，包含 整数、浮点数、定点数、时间、枚举 等，可参考支持的列的数据类型，并使用与你准备保存在数据库内的数据匹配的**数据类型**。

稍微提升一下复杂度，例如选择定义一张 `books` 表，这张表将是 `bookshop` 数据的核心。它包含书的 唯一标识、名称、书籍类型（如：杂志、动漫、教辅 等）、库存、价格、出版时间 字段。



```sql
CREATE TABLE `bookshop`.`books` (
  `id` bigint NOT NULL,
  `title` varchar(100),
  `type` enum('Magazine', 'Novel', 'Life', 'Arts', 'Comics', 'Education & Reference', 'Humanities & Social Sciences', 'Science & Technology', 'Kids', 'Sports'),
  `published_at` datetime,
  `stock` int,
  `price` decimal(15,2)
);
```

这张表比 `users` 表包含更多的数据类型：

- int: 推荐使用合适大小的类型，防止使用过量的硬盘甚至影响性能(类型范围过大)或数据溢出(类型范围过小)。
- datetime: 可以使用 **datetime** 类型保存时间值。
- enum: 可以使用 **enum** 类型的枚举来保存有限选择的值。

### 选择主键

主键是一个或一组列，这个由所有主键列组合起来的值是数据行的唯一标识。

> **注意：**
>
> TiDB 中，关于 **Primary Key** 的默认定义与 MySQL 常用存储引擎 [InnoDB](https://mariadb.com/kb/en/innodb/) 不一致。**InnoDB** 中，**Primary Key** 的语义为：唯一，不为空，**且为聚簇索引**。
>
> 而在 TiDB 中，**Primary Key** 的定义为：唯一，不为空。但主键不保证为**聚簇索引**。而是由另一组关键字 `CLUSTERED`、`NONCLUSTERED` 额外控制 **Primary Key** 是否为聚簇索引，若不指定，则由系统变量 `@@global.tidb_enable_clustered_index` 影响，具体说明请看此文档。

主键在 `CREATE TABLE` 语句中定义。主键约束要求所有受约束的列仅包含非 `NULL` 值。

一个表可以没有主键，主键也可以是非整数类型。但此时 TiDB 就会创建一个 `_tidb_rowid` 作为隐式主键。隐式主键 `_tidb_rowid` 因为其单调递增的特性，可能在大批量写入场景下会导致写入热点，如果你写入量密集，可考虑通过 SHARD_ROW_ID_BITS 和 PRE_SPLIT_REGIONS 两参数控制打散。但这可能导致读放大，请自行取舍。

表的主键为 整数类型 且使用了 `AUTO_INCREMENT` 时，无法使用 `SHARD_ROW_ID_BITS` 消除热点。需解决此热点问题，且无需使用主键的连续和递增时，可使用 AUTO_RANDOM 替换 `AUTO_INCREMENT` 属性来消除行 ID 的连续性。

更多有关热点问题的处理办法，请参考TiDB 热点问题处理。

需遵循[选择主键时应遵守的规则](#选择主键时应遵守的规则)，举一个 `users` 表中定义 `AUTO_RANDOM` 主键的例子：



```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100),
  PRIMARY KEY (`id`)
);
```

### 选择聚簇索引

聚簇索引 (clustered index) 是 TiDB 从 v5.0 开始支持的特性，用于控制含有主键的表数据的存储方式。通过使用聚簇索引，TiDB 可以更好地组织数据表，从而提高某些查询的性能。有些数据库管理系统也将聚簇索引称为“索引组织表” (index-organized tables)。

目前 TiDB 中 **_含有主键_** 的表分为以下两类：

- `NONCLUSTERED`，表示该表的主键为非聚簇索引。在非聚簇索引表中，行数据的键由 TiDB 内部隐式分配的 `_tidb_rowid` 构成，而主键本质上是唯一索引，因此非聚簇索引表存储一行至少需要两个键值对，分别为：
    - `_tidb_rowid`（键）- 行数据（值）
    - 主键列数据（键） - `_tidb_rowid`（值）
- `CLUSTERED`，表示该表的主键为聚簇索引。在聚簇索引表中，行数据的键由用户给定的主键列数据构成，因此聚簇索引表存储一行至少只要一个键值对，即：
    - 主键列数据（键） - 行数据（值）

如[主键](#选择主键)中所述，聚簇索引在 TiDB 中，使用关键字 `CLUSTERED`、`NONCLUSTERED` 进行控制。

> **注意：**
>
> TiDB 仅支持根据表的主键来进行聚簇操作。聚簇索引启用时，“主键”和“聚簇索引”两个术语在一些情况下可互换使用。主键指的是约束（一种逻辑属性），而聚簇索引描述的是数据存储的物理实现。

需遵循[选择聚簇索引时应遵守的规则](#选择聚簇索引时应遵守的规则)，假设需要建立一张 `books` 和 `users` 之间关联的表，代表用户对某书籍的评分。使用表名 `ratings` 来创建该表，并使用 `book_id` 和 `user_id` 构建复合主键，并在该主键上建立聚簇索引：



```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime,
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```

### 添加列约束

除[主键约束](#选择主键)外，TiDB 还支持其他的列约束，如：[非空约束 `NOT NULL`](#非空约束)、[唯一约束 `UNIQUE KEY`](#唯一约束)、默认值 `DEFAULT` 等。完整约束，请查看 TiDB 约束文档。

#### 填充默认值

如需在列上设置默认值，请使用 `DEFAULT` 约束。默认值将可以使你无需指定每一列的值，就可以插入数据。

你可以将 `DEFAULT` 与支持的 SQL 函数结合使用，将默认值的计算移出应用层，从而节省应用层的资源（当然，计算所消耗的资源并不会凭空消失，只是被转移到了 TiDB 集群中）。常见的，希望实现数据插入时，可默认填充默认的时间。还是使用 `ratings` 作为示例，可使用以下语句：



```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime DEFAULT NOW(),
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```

额外的，如果需更新时也默认填入当前时间，可使用以下语句（但 `ON UPDATE` 后仅可填入[当前时间相关语句](https://pingcap.github.io/sqlgram/#NowSymOptionFraction)，`DEFAULT` 后支持[更多选择](https://pingcap.github.io/sqlgram/#DefaultValueExpr)）：



```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```

#### 防止重复

如果你需要防止列中出现重复值，那你可以使用 `UNIQUE` 约束。

例如，你需要确保用户的昵称唯一，可以这样改写 `users` 表的创建 SQL：



```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100) UNIQUE,
  PRIMARY KEY (`id`)
);
```

如果你在 `users` 表中尝试插入相同的 `nickname`，将返回错误。

#### 防止空值

如果你需要防止列中出现空值，那就可以使用 `NOT NULL` 约束。

还是使用用户昵称来举例子，除了昵称唯一，还希望昵称不可为空，于是此处可以这样改写 `users` 表的创建 SQL：



```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100) UNIQUE NOT NULL,
  PRIMARY KEY (`id`)
);
```

### 使用 HTAP 能力

> **注意：**
>
> 本指南中有关 HTAP 的步骤仅适用于快速上手体验，不适用于生产环境。如需探索 HTAP 更多功能，请参考深入探索 HTAP。

假设 `bookshop` 应用程序，有对用户评价的 `ratings` 表进行 OLAP 分析查询的需求，例如需查询: **书籍的评分，是否和评价的时间具有显著的相关性** 的需求，用以分析用户的书籍评分是否客观。那么会要求查询整个 `ratings` 表中的 `score` 和 `rated_at` 字段。这对普通仅支持的 OLTP 的数据库来说，是一个非常消耗资源的操作。或者使用一些 ETL 或其他数据同步工具，将 OLTP 数据库中的数据，导出到专用的 OLAP 数据库，再进行分析。

这种场景下，TiDB 就是一个比较理想的一站式数据库解决方案，TiDB 是一个 **HTAP (Hybrid Transactional and Analytical Processing)** 数据库，同时支持 OLTP 和 OLAP 场景。

#### 同步列存数据

当前，TiDB 支持两种数据分析引擎：**TiFlash** 和 **TiSpark**。大数据场景 (100 T) 下，推荐使用 TiFlash MPP 作为 HTAP 的主要方案，TiSpark 作为补充方案。希望了解更多关于 TiDB 的 HTAP 能力，可参考以下文章：快速上手 HTAP 和 深入探索 HTAP。

此处选用 TiFlash 为 `bookshop` 数据库的数据分析引擎。

TiFlash 部署完成后并不会自动同步数据，而需要手动指定需要同步的表，开启同步副本仅需一行 SQL，如下所示：



```sql
ALTER TABLE {table_name} SET TIFLASH REPLICA {count};
```

**参数描述**

- `{table_name}`: 表名。
- `{count}`: 同步副本数，若为 0，则表示删除同步副本。

随后，TiFlash 将同步该表，查询时，TiDB 将会自动基于成本优化，考虑使用 **TiKV (行存)** 或 **TiFlash (列存)** 进行数据查询。当然，除了自动的方法，你也可以直接指定查询是否使用 TiFlash 副本，使用方法可查看使用 TiDB 读取 TiFlash 文档。

#### 使用 HTAP 的示例

`ratings` 表开启 1 个 TiFlash 副本：



```sql
ALTER TABLE `bookshop`.`ratings` SET TIFLASH REPLICA 1;
```

> **注意：**
>
> 如果你的集群，不包含 TiFlash 节点，此 SQL 语句将会报错：`1105 - the tiflash replica count: 1 should be less than the total tiflash server count: 0` 你可以[使用 TiDB Cloud (Serverless Tier) 构建 TiDB 集群](#第-1-步创建-serverless-tier-集群) 来创建一个含有 TiFlash 的集群。

随后正常进行查询即可：



```sql
SELECT HOUR(`rated_at`), AVG(`score`) FROM `bookshop`.`ratings` GROUP BY HOUR(`rated_at`);
```

也可使用 EXPLAIN ANALYZE 语句查看此语句是否使用了 TiFlash 引擎：



```sql
EXPLAIN ANALYZE SELECT HOUR(`rated_at`), AVG(`score`) FROM `bookshop`.`ratings` GROUP BY HOUR(`rated_at`);
```

运行结果为：

```
+-----------------------------+-----------+---------+--------------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+----------+------+
| id                          | estRows   | actRows | task         | access object | execution info                                                                                                                                                                                                                                                                                                                                                       | operator info                                                                                                                                  | memory   | disk |
+-----------------------------+-----------+---------+--------------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+----------+------+
| Projection_4                | 299821.99 | 24      | root         |               | time:60.8ms, loops:6, Concurrency:5                                                                                                                                                                                                                                                                                                                                  | hour(cast(bookshop.ratings.rated_at, time))->Column#6, Column#5                                                                                | 17.7 KB  | N/A  |
| └─HashAgg_5                 | 299821.99 | 24      | root         |               | time:60.7ms, loops:6, partial_worker:{wall_time:60.660079ms, concurrency:5, task_num:293, tot_wait:262.536669ms, tot_exec:40.171833ms, tot_time:302.827753ms, max:60.636886ms, p95:60.636886ms}, final_worker:{wall_time:60.701437ms, concurrency:5, task_num:25, tot_wait:303.114278ms, tot_exec:176.564µs, tot_time:303.297475ms, max:60.69326ms, p95:60.69326ms}  | group by:Column#10, funcs:avg(Column#8)->Column#5, funcs:firstrow(Column#9)->bookshop.ratings.rated_at                                         | 714.0 KB | N/A  |
|   └─Projection_15           | 300000.00 | 300000  | root         |               | time:58.5ms, loops:294, Concurrency:5                                                                                                                                                                                                                                                                                                                                | cast(bookshop.ratings.score, decimal(8,4) BINARY)->Column#8, bookshop.ratings.rated_at, hour(cast(bookshop.ratings.rated_at, time))->Column#10 | 366.2 KB | N/A  |
|     └─TableReader_10        | 300000.00 | 300000  | root         |               | time:43.5ms, loops:294, cop_task: {num: 1, max: 43.1ms, proc_keys: 0, rpc_num: 1, rpc_time: 43ms, copr_cache_hit_ratio: 0.00}                                                                                                                                                                                                                                        | data:TableFullScan_9                                                                                                                           | 4.58 MB  | N/A  |
|       └─TableFullScan_9     | 300000.00 | 300000  | cop[tiflash] | table:ratings | tiflash_task:{time:5.98ms, loops:8, threads:1}, tiflash_scan:{dtfile:{total_scanned_packs:45, total_skipped_packs:1, total_scanned_rows:368640, total_skipped_rows:8192, total_rs_index_load_time: 1ms, total_read_time: 1ms},total_create_snapshot_time:1ms}                                                                                                        | keep order:false                                                                                                                               | N/A      | N/A  |
+-----------------------------+-----------+---------+--------------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+----------+------+
```

在出现 `cop[tiflash]` 字样时，表示该任务发送至 TiFlash 进行处理。

### 执行 `CREATE TABLE` 语句

按以上步骤创建所有表后，[数据库初始化](#数据库初始化-dbinitsql-脚本)脚本应该如此所示。若需查看表信息详解，请参阅[数据表详解](#数据表详解)。

如果将数据库初始化脚本命名为 `init.sql` 并保存，可使用以下语句来执行数据库初始化：



```shell
mysql
    -u root \
    -h {host} \
    -P {port} \
    -p {password} \
    < init.sql
```

需查看 `bookshop` 数据库下的所有表，可使用 SHOW TABLES 语句：



```sql
SHOW TABLES IN `bookshop`;
```

运行结果为：

```
+--------------------+
| Tables_in_bookshop |
+--------------------+
| authors            |
| book_authors       |
| books              |
| orders             |
| ratings            |
| users              |
+--------------------+
```

### 创建表时应遵守的规则

本小节给出了一些在创建表时应遵守的规则。

#### 命名表时应遵守的规则

- 使用**完全限定**的表名称（例如：`CREATE TABLE {database_name}.{table_name}`）。这是因为你在不指定数据库名称时，TiDB 将使用你 **SQL 会话**中的当前数据库。若你未在 SQL 会话中使用 `USE {databasename};` 来指定数据库，TiDB 将会返回错误。
- 请使用有意义的表名，例如，若你需要创建一个用户表，你可以使用名称：`user`, `t_user`, `users` 等，或遵循你公司或组织的命名规范。如果你的公司或组织没有相应的命名规范，可参考[表命名规范](#表命名规范)。请勿使用这样的表名，如：`t1`, `table1` 等。
- 多个单词以下划线分隔，不推荐超过 32 个字符。
- 不同业务模块的表单独建立 `DATABASE`，并增加相应注释。

#### 定义列时应遵守的规则

- 查看支持的列的数据类型，并按照数据类型的限制来组织你的数据。为你计划被存在列中的数据选择合适的类型。
- 查看[选择主键时应遵守的规则](#选择主键时应遵守的规则)，决定是否使用主键列。
- 查看[选择聚簇索引时应遵守的规则](#选择聚簇索引时应遵守的规则)，决定是否指定聚簇索引。
- 查看[添加列约束](#添加列约束)，决定是否添加约束到列中。
- 请使用有意义的列名，推荐你遵循公司或组织的表命名规范。如果你的公司或组织没有相应的命名规范，可参考[列命名规范](#字段命名规范)。

#### 选择主键时应遵守的规则

- 在表内定义一个主键或唯一索引。
- 尽量选择有意义的列作为主键。
- 出于为性能考虑，尽量避免存储超宽表，表字段数不建议超过 60 个，建议单行的总数据大小不要超过 64K，数据长度过大字段最好拆到另外的表。
- 不推荐使用复杂的数据类型。
- 需要 JOIN 的字段，数据类型保障绝对一致，避免隐式转换。
- 避免在单个单调数据列上定义主键。如果你使用单个单调数据列（例如：`AUTO_INCREMENT` 的列）来定义主键，有可能会对写性能产生负面影响。可能的话，使用 `AUTO_RANDOM` 替换 `AUTO_INCREMENT`（这会失去主键的连续和递增特性）。
- 如果你 **_必须_** 在单个单调数据列上创建索引，且有大量写入的话。请不要将这个单调数据列定义为主键，而是使用 `AUTO_RANDOM` 创建该表的主键，或使用 SHARD_ROW_ID_BITS 和 PRE_SPLIT_REGIONS 打散 `_tidb_rowid`。

#### 选择聚簇索引时应遵守的规则

- 遵循[选择主键时应遵守的规则](#选择主键时应遵守的规则)：

    聚簇索引将基于主键建立，请遵循选择主键时应遵守的规则，此为选择聚簇索引时应遵守规则的基础。

- 在以下场景中，尽量使用聚簇索引，将带来性能和吞吐量的优势：

    - 插入数据时会减少一次从网络写入索引数据。
    - 等值条件查询仅涉及主键时会减少一次从网络读取数据。
    - 范围条件查询仅涉及主键时会减少多次从网络读取数据。
    - 等值或范围条件查询仅涉及主键的前缀时会减少多次从网络读取数据。

- 在以下场景中，尽量避免使用聚簇索引，将带来性能劣势：

    - 批量插入大量取值相邻的主键时，可能会产生较大的写热点问题，请遵循[选择主键时应遵守的规则](#选择主键时应遵守的规则)。
    - 当使用大于 64 位的数据类型作为主键时，可能导致表数据需要占用更多的存储空间。该现象在存在多个二级索引时尤为明显。

- 显式指定是否使用聚簇索引，而非使用系统变量 `@@global.tidb_enable_clustered_index` 及配置项 `alter-primary-key` 控制是否使用聚簇索引的默认行为。

#### `CREATE TABLE` 执行时应遵守的规则

- 不推荐使用客户端的 Driver 或 ORM 来执行数据库模式的更改。基于过往经验，建议使用 [MySQL 客户端](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)或使用任意你喜欢的 GUI 客户端来进行数据库模式的更改。本文档中，将在大多数场景下，使用 **MySQL 客户端** 传入 SQL 文件来执行数据库模式的更改。
- 遵循 SQL 开发规范中的[建表删表规范](#建表删表规范)，建议业务应用内部封装建表删表语句增加判断逻辑。

### 更进一步

请注意，到目前为止，创建的所有表都不包含二级索引。添加二级索引的指南，请参考[创建二级索引](#创建二级索引)。


---
title: 创建二级索引
summary: 创建二级索引的方法、规范及例子。
---

## 创建二级索引

在这个章节当中，将开始介绍如何使用 SQL 来创建二级索引，及创建二级索引时应遵守的规则。将在这个章节中围绕 [Bookshop](#bookshop-应用) 这个应用程序来对 TiDB 的创建二级索引部分展开介绍。

### 在开始之前

在阅读本页面之前，你需要准备以下事项：

- [使用 TiDB Cloud (Serverless Tier) 构建 TiDB 集群](#使用-tidb-cloud-(serverless-tier)-构建-tidb-集群)。
- 阅读[数据库模式概览](#概述)。
- [创建一个数据库](#创建数据库)。
- [创建表](#创建表)。

### 什么是二级索引

二级索引是集群中的逻辑对象，你可以简单地认为它就是一种对数据的排序，TiDB 使用这种有序性来加速查询。TiDB 的创建二级索引的操作为在线操作，不会阻塞表中的数据读写。TiDB 会创建表中各行的引用，并按选择的列进行排序。而并非对表本身的数据进行排序。可在二级索引中查看更多信息。二级索引可[跟随表进行创建](#新建表的同时创建二级索引)，也可[在已有的表上进行添加](#在已有表中添加二级索引)。

### 在已有表中添加二级索引

如果需要对已有表中添加二级索引，可使用 CREATE INDEX 语句。在 TiDB 中，`CREATE INDEX` 为在线操作，不会阻塞表中的数据读写。二级索引创建一般如以下形式：



```sql
CREATE INDEX {index_name} ON {table_name} ({column_names});
```

**参数描述**

- `{index_name}`: 二级索引名。
- `{table_name}`: 表名。
- `{column_names}`: 将需要索引的列名列表，以半角逗号分隔。

### 新建表的同时创建二级索引

如果你希望在创建表的同时，同时创建二级索引，可在 CREATE TABLE 的末尾使用包含 `KEY` 关键字的子句来创建二级索引：



```sql
KEY `{index_name}` (`{column_names}`)
```

**参数描述**

- `{index_name}`: 二级索引名。
- `{column_names}`: 将需要索引的列名列表，以半角逗号分隔。

### 创建二级索引时应遵守的规则

见 [索引的最佳实践](#索引的最佳实践)。

### 例子

假设你希望 `bookshop` 应用程序有 **查询某个年份出版的所有书籍** 的功能。`books` 表如下所示:

|    字段名    |     类型      |                 含义                  |
| :----------: | :-----------: | :-----------------------------------: |
|      id      |  bigint(20)   |            书籍的唯一标识             |
|    title     | varchar(100)  |               书籍名称                |
|     type     |     enum      | 书籍类型（如：杂志、动漫、教辅 等） |
|    stock     |  bigint(20)   |                 库存                  |
|    price     | decimal(15,2) |                 价格                  |
| published_at |   datetime    |               出版时间                |



```sql
CREATE TABLE `bookshop`.`books` (
  `id` bigint(20) AUTO_RANDOM NOT NULL,
  `title` varchar(100) NOT NULL,
  `type` enum('Magazine', 'Novel', 'Life', 'Arts', 'Comics', 'Education & Reference', 'Humanities & Social Sciences', 'Science & Technology', 'Kids', 'Sports') NOT NULL,
  `published_at` datetime NOT NULL,
  `stock` int(11) DEFAULT '0',
  `price` decimal(15,2) DEFAULT '0.0',
  PRIMARY KEY (`id`) CLUSTERED
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
```

因此，就需要对 **查询某个年份出版的所有书籍** 的 SQL 进行编写， 以 2022 年为例，如下所示：



```sql
SELECT * FROM `bookshop`.`books` WHERE `published_at` >= '2022-01-01 00:00:00' AND `published_at` < '2023-01-01 00:00:00';
```

可以使用 EXPLAIN 进行 SQL 语句的执行计划检查：



```sql
EXPLAIN SELECT * FROM `bookshop`.`books` WHERE `published_at` >= '2022-01-01 00:00:00' AND `published_at` < '2023-01-01 00:00:00';
```

运行结果为：

```
+-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------+
| id                      | estRows  | task      | access object | operator info                                                                                                            |
+-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------+
| TableReader_7           | 346.32   | root      |               | data:Selection_6                                                                                                         |
| └─Selection_6           | 346.32   | cop[tikv] |               | ge(bookshop.books.published_at, 2022-01-01 00:00:00.000000), lt(bookshop.books.published_at, 2023-01-01 00:00:00.000000) |
|   └─TableFullScan_5     | 20000.00 | cop[tikv] | table:books   | keep order:false                                                                                                         |
+-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------+
3 rows in set (0.61 sec)
```

可以看到返回的计划中，出现了类似 **TableFullScan** 的字样，这代表 TiDB 准备在这个查询中对 `books` 表进行全表扫描，这在数据量较大的情况下，几乎是致命的。

在 `books` 表增加一个 `published_at` 列的索引：



```sql
CREATE INDEX `idx_book_published_at` ON `bookshop`.`books` (`bookshop`.`books`.`published_at`);
```

添加索引后，再次运行 `EXPLAIN` 语句检查执行计划：

```
+-------------------------------+---------+-----------+--------------------------------------------------------+-------------------------------------------------------------------+
| id                            | estRows | task      | access object                                          | operator info                                                     |
+-------------------------------+---------+-----------+--------------------------------------------------------+-------------------------------------------------------------------+
| IndexLookUp_10                | 146.01  | root      |                                                        |                                                                   |
| ├─IndexRangeScan_8(Build)     | 146.01  | cop[tikv] | table:books, index:idx_book_published_at(published_at) | range:[2022-01-01 00:00:00,2023-01-01 00:00:00), keep order:false |
| └─TableRowIDScan_9(Probe)     | 146.01  | cop[tikv] | table:books                                            | keep order:false                                                  |
+-------------------------------+---------+-----------+--------------------------------------------------------+-------------------------------------------------------------------+
3 rows in set (0.18 sec)
```

可以看到执行计划中没有了 **TableFullScan** 的字样，取而代之的是 **IndexRangeScan**，这代表已经 TiDB 在进行这个查询时准备使用索引。

> **注意：**
>
> 上方执行计划中的的 **TableFullScan**、**IndexRangeScan** 等在 TiDB 内被称为算子。这里对执行计划的解读及算子等不做进一步的展开，若你对此感兴趣，可前往 TiDB 执行计划概览文档查看更多关于执行计划与 TiDB 算子的相关知识。
>
> 执行计划并非每次返回使用的算子都相同，这是由于 TiDB 使用的优化方式为 **基于代价的优化方式 (CBO)**，执行计划不仅与规则相关，还和数据分布相关。你可以前往 SQL 性能调优文档查看更多 TiDB SQL 性能的描述。
>
> TiDB 在查询时，还支持显式地使用索引，你可以使用 Optimizer Hints 或 [执行计划管理 (SPM)](None) 来人为的控制索引的使用。但如果你不了解它内部发生了什么，请你**_暂时先不要使用它_**。

可以使用 SHOW INDEXES 语句查询表中的索引：



```sql
SHOW INDEXES FROM `bookshop`.`books`;
```

运行结果为：

```
+-------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| Table | Non_unique | Key_name              | Seq_in_index | Column_name  | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Visible | Expression | Clustered |
+-------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| books |          0 | PRIMARY               |            1 | id           | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       | YES       |
| books |          1 | idx_book_published_at |            1 | published_at | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       | NO        |
+-------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
2 rows in set (1.63 sec)
```

### 更进一步

至此，你已经完成数据库、表及二级索引的创建，接下来，数据库模式已经准备好给你的应用程序提供 [写入](#插入数据) 和 [读取](#单表查询) 读取的能力了。



# 数据写入

---
title: 插入数据
summary: 插入数据、批量导入数据的方法、最佳实践及例子。
---

<!-- markdownlint-disable MD029 -->

## 插入数据

此页面将展示使用 SQL 语言，配合各种编程语言将数据插入到 TiDB 中。

### 在开始之前

在阅读本页面之前，你需要准备以下事项：

- [使用 TiDB Cloud (Serverless Tier) 构建 TiDB 集群](#使用-tidb-cloud-(serverless-tier)-构建-tidb-集群)。
- 阅读[数据库模式概览](#概述)，并[创建数据库](#创建数据库)、[创建表](#创建表)、[创建二级索引](#创建二级索引)。

### 插入行

假设你需要插入多行数据，那么会有两种插入的办法，假设需要插入 3 个玩家数据：

- 一个**多行插入语句**：

    

    ```sql
    INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (1, 1000, 1), (2, 230, 2), (3, 300, 5);
    ```

- 多个**单行插入语句**：

    

    ```sql
    INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (1, 1000, 1);
    INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (2, 230, 2);
    INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (3, 300, 5);
    ```

一般来说使用一个`多行插入语句`，会比多个`单行插入语句`快。

<SimpleTab>
<div label="SQL">

在 SQL 中插入多行数据的示例：

```sql
CREATE TABLE `player` (`id` INT, `coins` INT, `goods` INT);
INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (1, 1000, 1), (2, 230, 2);
```

有关如何使用此 SQL，可查阅[连接到 TiDB 集群](#第-2-步连接到集群)文档部分，按文档步骤使用客户端连接到 TiDB 集群后，输入 SQL 语句即可。

</div>

<div label="Java">

在 Java 中插入多行数据的示例：

```java
// ds is an entity of com.mysql.cj.jdbc.MysqlDataSource
try (Connection connection = ds.getConnection()) {
    connection.setAutoCommit(false);

    PreparedStatement pstmt = connection.prepareStatement("INSERT INTO player (id, coins, goods) VALUES (?, ?, ?)"))

    // first player
    pstmt.setInt(1, 1);
    pstmt.setInt(2, 1000);
    pstmt.setInt(3, 1);
    pstmt.addBatch();

    // second player
    pstmt.setInt(1, 2);
    pstmt.setInt(2, 230);
    pstmt.setInt(3, 2);
    pstmt.addBatch();

    pstmt.executeBatch();
    connection.commit();
} catch (SQLException e) {
    e.printStackTrace();
}
```

另外，由于 MySQL JDBC Driver 默认设置问题，你需更改部分参数，以获得更好的批量插入性能：

|            参数            |                 作用                  |                                                                     推荐场景                                                                      |         推荐配置         |
| :------------------------: | :-----------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------------------: | :----------------------: |
|    `useServerPrepStmts`    |   是否使用服务端开启预处理语句支持    |                                                            在需要多次使用预处理语句时                                                             |          `true`          |
|      `cachePrepStmts`      |       客户端是否缓存预处理语句        |                                                           `useServerPrepStmts=true` 时                                                            |          `true`          |
|  `prepStmtCacheSqlLimit`   |  预处理语句最大大小（默认 256 字符）  |                                                             预处理语句大于 256 字符时                                                             | 按实际预处理语句大小配置 |
|    `prepStmtCacheSize`     | 预处理语句最大缓存数量 （默认 25 条） |                                                            预处理语句数量大于 25 条时                                                             | 按实际预处理语句数量配置 |
| `rewriteBatchedStatements` |          是否重写 Batch 语句          |                                                                  需要批量操作时                                                                   |          `true`          |
|    `allowMultiQueries`     |             开启批量操作              | 因为一个[客户端 Bug](https://bugs.mysql.com/bug.php?id=96623) 在 `rewriteBatchedStatements = true` 和 `useServerPrepStmts = true` 时，需设置此项 |          `true`          |

MySQL JDBC Driver 还提供了一个集成配置项：`useConfigs`。当它配置为 `maxPerformance` 时，相当于配置了一组配置，以 `mysql:mysql-connector-java:8.0.28` 为例，`useConfigs=maxPerformance` 包含：



```properties
cachePrepStmts=true
cacheCallableStmts=true
cacheServerConfiguration=true
useLocalSessionState=true
elideSetAutoCommits=true
alwaysSendSetIsolation=false
enableQueryTimeouts=false
connectionAttributes=none
useInformationSchema=true
```

你可以自行查看 `mysql-connector-java-{version}.jar!/com/mysql/cj/configurations/maxPerformance.properties` 来获得对应版本MySQL JDBC Driver 的 `useConfigs=maxPerformance` 包含配置。

在此处给出一个较为的通用场景的 JDBC 连接字符串配置，以 Host: `127.0.0.1`，Port: `4000`，用户名: `root`，密码: 空 ，默认数据库: `test`为例：



```
jdbc:mysql://127.0.0.1:4000/test?user=root&useConfigs=maxPerformance&useServerPrepStmts=true&prepStmtCacheSqlLimit=2048&prepStmtCacheSize=256&rewriteBatchedStatements=true&allowMultiQueries=true
```

有关 Java 的完整示例，可参阅：

- [TiDB 和 Java 的简单 CRUD 应用程序 - 使用 JDBC](#第-2-步获取代码)
- [TiDB 和 Java 的简单 CRUD 应用程序 - 使用 Hibernate](#第-2-步获取代码)
- [Build the TiDB Application using Spring Boot](#使用-spring-boot-构建-tidb-应用程序)

</div>

<div label="Golang">

在 Golang 中插入多行数据的示例：

```go
package main

import (
    "database/sql"
    "strings"

    _ "github.com/go-sql-driver/mysql"
)

type Player struct {
    ID    string
    Coins int
    Goods int
}

func bulkInsertPlayers(db *sql.DB, players []Player, batchSize int) error {
    tx, err := db.Begin()
    if err != nil {
        return err
    }

    stmt, err := tx.Prepare(buildBulkInsertSQL(batchSize))
    if err != nil {
        return err
    }

    defer stmt.Close()

    for len(players) > batchSize {
        if _, err := stmt.Exec(playerToArgs(players[:batchSize])...); err != nil {
            tx.Rollback()
            return err
        }

        players = players[batchSize:]
    }

    if len(players) != 0 {
        if _, err := tx.Exec(buildBulkInsertSQL(len(players)), playerToArgs(players)...); err != nil {
            tx.Rollback()
            return err
        }
    }

    if err := tx.Commit(); err != nil {
        tx.Rollback()
        return err
    }

    return nil
}

func playerToArgs(players []Player) []interface{} {
    var args []interface{}
    for _, player := range players {
        args = append(args, player.ID, player.Coins, player.Goods)
    }
    return args
}

func buildBulkInsertSQL(amount int) string {
    return "INSERT INTO player (id, coins, goods) VALUES (?, ?, ?)" + strings.Repeat(",(?,?,?)", amount-1)
}
```

有关 Golang 的完整示例，可参阅：

- [TiDB 和 Golang 的简单 CRUD 应用程序 - 使用 go-sql-driver/mysql](#第-2-步获取代码)
- [TiDB 和 Golang 的简单 CRUD 应用程序 - 使用 GORM](#第-2-步获取代码)

</div>

<div label="Python">

在 Python 中插入多行数据的示例：

```python
import MySQLdb

connection = MySQLdb.connect(
    host="127.0.0.1",
    port=4000,
    user="root",
    password="",
    database="bookshop",
    autocommit=True
)
with get_connection(autocommit=True) as connection:

    with connection.cursor() as cur:
        player_list = random_player(1919)
        for idx in range(0, len(player_list), 114):
            cur.executemany("INSERT INTO player (id, coins, goods) VALUES (%s, %s, %s)", player_list[idx:idx + 114])
```

有关 Python 的完整示例，可参阅：

- [TiDB 和 Python 的简单 CRUD 应用程序 - 使用 PyMySQL](#第-2-步获取代码)
- [TiDB 和 Python 的简单 CRUD 应用程序 - 使用 mysqlclient](#第-2-步获取代码)
- [TiDB 和 Python 的简单 CRUD 应用程序 - 使用 mysql-connector-python](#第-2-步获取代码)
- [TiDB 和 Python 的简单 CRUD 应用程序 - 使用 SQLAlchemy](#第-2-步获取代码)
- [TiDB 和 Python 的简单 CRUD 应用程序 - 使用 peewee](#第-2-步获取代码)

</div>

</SimpleTab>

### 批量插入

如果你需要快速地将大量数据导入 TiDB 集群，最好的方式并不是使用 `INSERT` 语句，这并不是最高效的方法，而且需要你自行处理异常等问题。推荐使用 PingCAP 提供的一系列工具进行数据迁移：

- 数据导出工具：Dumpling。可以导出 MySQL 或 TiDB 的数据到本地或 Amazon S3 中。
- 数据导入工具：TiDB Lightning。可以导入 `Dumpling` 导出的数据、CSV 文件，或者 Amazon Aurora 生成的 Apache Parquet 文件。同时支持在本地盘或 Amazon S3 云盘读取数据。
- 数据同步工具：TiDB Data Migration。可同步 MySQL、MariaDB、Amazon Aurora 数据库到 TiDB 中。且支持分库分表数据库的迁移。
- 数据备份恢复工具：[Backup & Restore (BR)](None)。相对于 `Dumpling`，BR 更适合**_大数据量_**的场景。

### 避免热点

在设计表时需要考虑是否存在大量插入行为，若有，需在表设计期间对热点进行规避。请查看[创建表 - 选择主键](#选择主键)部分，并遵从[选择主键时应遵守的规则](#选择主键时应遵守的规则)。

更多有关热点问题的处理办法，请参考 TiDB 热点问题处理文档。

### 主键为 `AUTO_RANDOM` 表插入数据

在插入的表主键为 `AUTO_RANDOM` 时，这时默认情况下，不能指定主键。例如 [bookshop](#bookshop-应用) 数据库中，可以看到 [users 表](#users-表) 的 `id` 字段含有 `AUTO_RANDOM` 属性。

此时，不可使用类似以下 SQL 进行插入：



```sql
INSERT INTO `bookshop`.`users` (`id`, `balance`, `nickname`) VALUES (1, 0.00, 'nicky');
```

将会产生错误：

```
ERROR 8216 (HY000): Invalid auto random: Explicit insertion on auto_random column is disabled. Try to set @@allow_auto_random_explicit_insert = true.
```

这是旨在提示你，不建议在插入时手动指定 `AUTO_RANDOM` 的列。这时，你有两种解决办法处理此错误：

- (推荐) 插入语句中去除此列，使用 TiDB 帮你初始化的 `AUTO_RANDOM` 值。这样符合 `AUTO_RANDOM` 的语义。

    

    ```sql
    INSERT INTO `bookshop`.`users` (`balance`, `nickname`) VALUES (0.00, 'nicky');
    ```

- 如果你确认一定需要指定此列，那么可以使用 SET 语句通过更改用户变量的方式，允许在插入时，指定 `AUTO_RANDOM` 的列。

    

    ```sql
    SET @@allow_auto_random_explicit_insert = true;
    INSERT INTO `bookshop`.`users` (`id`, `balance`, `nickname`) VALUES (1, 0.00, 'nicky');
    ```

### 使用 HTAP

在 TiDB 中，使用 HTAP 能力无需你在插入数据时进行额外操作。不会有任何额外的插入逻辑，由 TiDB 自动进行数据的一致性保证。你只需要在创建表后，[开启列存副本同步](#使用-htap-能力)，就可以直接使用列存副本来加速你的查询。


---
title: 更新数据
summary: 更新数据、批量更新数据的方法、最佳实践及例子。
---

## 更新数据

此页面将展示以下 SQL 语句，配合各种编程语言 TiDB 中的数据进行更新：

- UPDATE: 用于修改指定表中的数据。
- INSERT ON DUPLICATE KEY UPDATE: 用于插入数据，在有主键或唯一键冲突时，更新此数据。注意，**_不建议_**在有多个唯一键(包含主键)的情况下使用此语句。这是因为此语句在检测到任何唯一键(包括主键) 冲突时，将更新数据。在不止匹配到一行冲突时，将只会更新一行数据。

### 在开始之前

在阅读本页面之前，你需要准备以下事项：

- [使用 TiDB Cloud (Serverless Tier) 构建 TiDB 集群](#使用-tidb-cloud-(serverless-tier)-构建-tidb-集群)
- 阅读[数据库模式概览](#概述)，并[创建数据库](#创建数据库)、[创建表](#创建表)、[创建二级索引](#创建二级索引)
- 若需使用 `UPDATE` 语句更新数据，需先[插入数据](#插入数据)

### 使用 `UPDATE`

需更新表中的现有行，需要使用带有 WHERE 子句的 UPDATE 语句，即需要过滤列进行更新。

> **注意：**
>
> 如果您需要更新大量的行，比如数万甚至更多行，那么建议不要一次性进行完整的更新，而是每次迭代更新一部分，直到所有行全部更新。您可以编写脚本或程序，使用循环完成此操作。
> 您可参考[批量更新](#批量更新)获得指引。

#### SQL 语法

在 SQL 中，`UPDATE` 语句一般为以下形式：



```sql
UPDATE {table} SET {update_column} = {update_value} WHERE {filter_column} = {filter_value}
```

|       参数        |         描述         |
| :---------------: | :------------------: |
|     `{table}`     |         表名         |
| `{update_column}` |     需更新的列名     |
| `{update_value}`  |   需更新的此列的值   |
| `{filter_column}` | 匹配条件过滤器的列名 |
| `{filter_value}`  | 匹配条件过滤器的列值 |

此处仅展示 `UPDATE` 的简单用法，详细文档可参考 TiDB 的 UPDATE 语法页。

#### `UPDATE` 最佳实践

以下是更新行时需要遵循的一些最佳实践：

- 始终在更新语句中指定 `WHERE` 子句。如果 `UPDATE` 没有 `WHERE` 子句，TiDB 将更新这个表内的**_所有行_**。
- 需要更新大量行(数万或更多)的时候，使用[批量更新](#批量更新)，这是因为 TiDB 单个事务大小限制为 [txn-total-size-limit](#txn-total-size-limit)（默认为 100MB），且一次性过多的数据更新，将导致持有锁时间过长（悲观事务），或产生大量冲突（乐观事务）。

#### `UPDATE` 例子

假设某位作者改名为 Helen Haruki，需要更改 [authors](#authors-表) 表。假设他的唯一标识 `id` 为 1，即过滤器应为：`id = 1`。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在 SQL 中更改作者姓名的示例为：

```sql
UPDATE `authors` SET `name` = "Helen Haruki" WHERE `id` = 1;
```

</div>

<div label="Java" value="java">

在 Java 中更改作者姓名的示例为：

```java
// ds is an entity of com.mysql.cj.jdbc.MysqlDataSource
try (Connection connection = ds.getConnection()) {
    PreparedStatement pstmt = connection.prepareStatement("UPDATE `authors` SET `name` = ? WHERE `id` = ?");
    pstmt.setString(1, "Helen Haruki");
    pstmt.setInt(2, 1);
    pstmt.executeUpdate();
} catch (SQLException e) {
    e.printStackTrace();
}
```

</div>
</SimpleTab>

### 使用 `INSERT ON DUPLICATE KEY UPDATE`

如果你需要将新数据插入表中，但如果有任何唯一键（主键也是一种唯一键）发生冲突，则会更新第一条冲突数据，可使用 `INSERT ... ON DUPLICATE KEY UPDATE ...` 语句进行插入或更新。

#### SQL 语法

在 SQL 中，`INSERT ... ON DUPLICATE KEY UPDATE ...` 语句一般为以下形式：



```sql
INSERT INTO {table} ({columns}) VALUES ({values})
    ON DUPLICATE KEY UPDATE {update_column} = {update_value};
```

|       参数        |       描述       |
| :---------------: | :--------------: |
|     `{table}`     |       表名       |
|    `{columns}`    |   需插入的列名   |
|    `{values}`     | 需插入的此列的值 |
| `{update_column}` |   需更新的列名   |
| `{update_value}`  | 需更新的此列的值 |

#### `INSERT ON DUPLICATE KEY UPDATE` 最佳实践

- 在仅有一个唯一键的表上使用 `INSERT ON DUPLICATE KEY UPDATE`。此语句在检测到任何 **_唯一键_** (包括主键) 冲突时，将更新数据。在不止匹配到一行冲突时，将只会一行数据。因此，除非能保证仅有一行冲突，否则不建议在有多个唯一键的表中使用 `INSERT ON DUPLICATE KEY UPDATE` 语句。
- 在创建或更新的场景中使用此语句。

#### `INSERT ON DUPLICATE KEY UPDATE` 例子

例如，需要更新 [ratings](#ratings-表) 表来写入用户对书籍的评价，如果用户还未评价此书籍，将新建一条评价，如果用户已经评价过，那么将会更新他之前的评价。

此处主键为 `book_id` 和 `user_id` 的联合主键。`user_id` 为 1 的用户，给 `book_id` 为 1000 的书籍，打出的 5 分的评价。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在 SQL 中更新书籍评价的示例为：

```sql
INSERT INTO `ratings`
    (`book_id`, `user_id`, `score`, `rated_at`)
VALUES
    (1000, 1, 5, NOW())
ON DUPLICATE KEY UPDATE `score` = 5, `rated_at` = NOW();
```

</div>

<div label="Java" value="java">

在 Java 中更新书籍评价的示例为：

```java
// ds is an entity of com.mysql.cj.jdbc.MysqlDataSource

try (Connection connection = ds.getConnection()) {
    PreparedStatement p = connection.prepareStatement("INSERT INTO `ratings` (`book_id`, `user_id`, `score`, `rated_at`)
VALUES (?, ?, ?, NOW()) ON DUPLICATE KEY UPDATE `score` = ?, `rated_at` = NOW()");
    p.setInt(1, 1000);
    p.setInt(2, 1);
    p.setInt(3, 5);
    p.setInt(4, 5);
    p.executeUpdate();
} catch (SQLException e) {
    e.printStackTrace();
}
```

</div>
</SimpleTab>

### 批量更新

需要更新表中多行的数据，可选择 [使用 `UPDATE`](#使用-update)，并使用 `WHERE` 子句过滤需要更新的数据。

但如果你需要更新大量行(数万或更多)的时候，建议使用一个迭代，每次都只更新一部分数据，直到更新全部完成。这是因为 TiDB 单个事务大小限制为 [txn-total-size-limit](#txn-total-size-limit)（默认为 100MB），且一次性过多的数据更新，将导致持有锁时间过长（悲观事务），或产生大量冲突（乐观事务）。你可以在程序或脚本中使用循环来完成操作。

本页提供了编写脚本来处理循环更新的示例，该示例演示了应如何进行 `SELECT` 和 `UPDATE` 的组合，完成循环更新。

#### 编写批量更新循环

首先，你应在你的应用或脚本的循环中，编写一个 `SELECT` 查询。这个查询的返回值可以作为需要更新的行的主键。需要注意的是，定义这个 `SELECT` 查询时，需要注意使用 `WHERE` 子句过滤需要更新的行。

#### 例子

假设在过去的一年里，用户在 `bookshop` 网站进行了大量的书籍打分，但是原本设计为 5 分制的评分导致书籍评分的区分度不够，大量书籍评分集中在 3 分附近，因此，决定将 5 分制改为 10 分制。用来增大书籍评分的区分度。

这时需要对 `ratings` 表内之前 5 分制的数据进行乘 2 操作，同时需向 `ratings` 表内添加一个新列，以指示行是否已经被更新了。使用此列，可以在 `SELECT` 中过滤掉已经更新的行，这将防止脚本崩溃时对行进行多次更新，导致不合理的数据出现。

例如，你可以创建一个名为 `ten_point`，数据类型为 BOOL 的列作为是否为 10 分制的标识：



```sql
ALTER TABLE `bookshop`.`ratings` ADD COLUMN `ten_point` BOOL NOT NULL DEFAULT FALSE;
```

> **注意：**
>
> 此批量更新程序将使用 **DDL** 语句将进行数据表的模式更改。TiDB 的所有 DDL 变更操作全部都是在线进行的，可查看此处，了解此处使用的 ADD COLUMN 语句。

<SimpleTab groupId="language">
<div label="Golang" value="golang">

在 Golang 中，批量更新程序类似于以下内容：

```go
package main

import (
    "database/sql"
    "fmt"
    _ "github.com/go-sql-driver/mysql"
    "strings"
    "time"
)

func main() {
    db, err := sql.Open("mysql", "root:@tcp(127.0.0.1:4000)/bookshop")
    if err != nil {
        panic(err)
    }
    defer db.Close()

    bookID, userID := updateBatch(db, true, 0, 0)
    fmt.Println("first time batch update success")
    for {
        time.Sleep(time.Second)
        bookID, userID = updateBatch(db, false, bookID, userID)
        fmt.Printf("batch update success, [bookID] %d, [userID] %d\n", bookID, userID)
    }
}

// updateBatch select at most 1000 lines data to update score
func updateBatch(db *sql.DB, firstTime bool, lastBookID, lastUserID int64) (bookID, userID int64) {
    // select at most 1000 primary keys in five-point scale data
    var err error
    var rows *sql.Rows

    if firstTime {
        rows, err = db.Query("SELECT `book_id`, `user_id` FROM `bookshop`.`ratings` " +
            "WHERE `ten_point` != true ORDER BY `book_id`, `user_id` LIMIT 1000")
    } else {
        rows, err = db.Query("SELECT `book_id`, `user_id` FROM `bookshop`.`ratings` "+
            "WHERE `ten_point` != true AND `book_id` > ? AND `user_id` > ? "+
            "ORDER BY `book_id`, `user_id` LIMIT 1000", lastBookID, lastUserID)
    }

    if err != nil || rows == nil {
        panic(fmt.Errorf("error occurred or rows nil: %+v", err))
    }

    // joint all id with a list
    var idList []interface{}
    for rows.Next() {
        var tempBookID, tempUserID int64
        if err := rows.Scan(&tempBookID, &tempUserID); err != nil {
            panic(err)
        }
        idList = append(idList, tempBookID, tempUserID)
        bookID, userID = tempBookID, tempUserID
    }

    bulkUpdateSql := fmt.Sprintf("UPDATE `bookshop`.`ratings` SET `ten_point` = true, "+
        "`score` = `score` * 2 WHERE (`book_id`, `user_id`) IN (%s)", placeHolder(len(idList)))
    db.Exec(bulkUpdateSql, idList...)

    return bookID, userID
}

// placeHolder format SQL place holder
func placeHolder(n int) string {
    holderList := make([]string, n/2, n/2)
    for i := range holderList {
        holderList[i] = "(?,?)"
    }
    return strings.Join(holderList, ",")
}
```

每次迭代中，`SELECT` 按主键顺序进行查询，最多选择 1000 行未更新到 10 分制（`ten_point` 为 `false`）数据的主键值。每次 `SELECT` 都会选择比上一次 `SELECT` 结果的最大主键还要大的数据，防止重复。然后，使用批量更新的方式，对其 `score` 列乘 2，并且将 `ten_point` 设为 `true`，更新 `ten_point` 的意义是在于防止更新程序崩溃重启后，反复更新同一行数据，导致数据损坏。每次循环中的 `time.Sleep(time.Second)` 将使得更新程序暂停 1 秒，防止批量更新程序占用过多的硬件资源。

</div>

<div label="Java (JDBC)" value="java">

在 Java (JDBC) 中，批量更新程序类似于以下内容：

**Java 代码部分：**



```java
package com.pingcap.bulkUpdate;

import com.mysql.cj.jdbc.MysqlDataSource;

import java.sql.*;
import java.util.LinkedList;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class BatchUpdateExample {
    static class UpdateID {
        private Long bookID;
        private Long userID;

        public UpdateID(Long bookID, Long userID) {
            this.bookID = bookID;
            this.userID = userID;
        }

        public Long getBookID() {
            return bookID;
        }

        public void setBookID(Long bookID) {
            this.bookID = bookID;
        }

        public Long getUserID() {
            return userID;
        }

        public void setUserID(Long userID) {
            this.userID = userID;
        }

        @Override
        public String toString() {
            return "[bookID] " + bookID + ", [userID] " + userID ;
        }
    }

    public static void main(String[] args) throws InterruptedException {
        // Configure the example database connection.

        // Create a mysql data source instance.
        MysqlDataSource mysqlDataSource = new MysqlDataSource();

        // Set server name, port, database name, username and password.
        mysqlDataSource.setServerName("localhost");
        mysqlDataSource.setPortNumber(4000);
        mysqlDataSource.setDatabaseName("bookshop");
        mysqlDataSource.setUser("root");
        mysqlDataSource.setPassword("");

        UpdateID lastID = batchUpdate(mysqlDataSource, null);

        System.out.println("first time batch update success");
        while (true) {
            TimeUnit.SECONDS.sleep(1);
            lastID = batchUpdate(mysqlDataSource, lastID);
            System.out.println("batch update success, [lastID] " + lastID);
        }
    }

    public static UpdateID batchUpdate (MysqlDataSource ds, UpdateID lastID) {
        try (Connection connection = ds.getConnection()) {
            UpdateID updateID = null;

            PreparedStatement selectPs;

            if (lastID == null) {
                selectPs = connection.prepareStatement(
                        "SELECT `book_id`, `user_id` FROM `bookshop`.`ratings` " +
                        "WHERE `ten_point` != true ORDER BY `book_id`, `user_id` LIMIT 1000");
            } else {
                selectPs = connection.prepareStatement(
                        "SELECT `book_id`, `user_id` FROM `bookshop`.`ratings` "+
                            "WHERE `ten_point` != true AND `book_id` > ? AND `user_id` > ? "+
                            "ORDER BY `book_id`, `user_id` LIMIT 1000");

                selectPs.setLong(1, lastID.getBookID());
                selectPs.setLong(2, lastID.getUserID());
            }

            List<Long> idList = new LinkedList<>();
            ResultSet res = selectPs.executeQuery();
            while (res.next()) {
                updateID = new UpdateID(
                        res.getLong("book_id"),
                        res.getLong("user_id")
                );
                idList.add(updateID.getBookID());
                idList.add(updateID.getUserID());
            }

            if (idList.isEmpty()) {
                System.out.println("no data should update");
                return null;
            }

            String updateSQL = "UPDATE `bookshop`.`ratings` SET `ten_point` = true, "+
                    "`score` = `score` * 2 WHERE (`book_id`, `user_id`) IN (" +
                    placeHolder(idList.size() / 2) + ")";
            PreparedStatement updatePs = connection.prepareStatement(updateSQL);
            for (int i = 0; i < idList.size(); i++) {
                updatePs.setLong(i + 1, idList.get(i));
            }
            int count = updatePs.executeUpdate();
            System.out.println("update " + count + " data");

            return updateID;
        } catch (SQLException e) {
            e.printStackTrace();
        }

        return null;
    }

    public static String placeHolder(int n) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n ; i++) {
            sb.append(i == 0 ? "(?,?)" : ",(?,?)");
        }

        return sb.toString();
    }
}
```

**`hibernate.cfg.xml` 配置部分：**



```xml
<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE hibernate-configuration PUBLIC
        "-//Hibernate/Hibernate Configuration DTD 3.0//EN"
        "http://www.hibernate.org/dtd/hibernate-configuration-3.0.dtd">
<hibernate-configuration>
    <session-factory>

        <!-- Database connection settings -->
        <property name="hibernate.connection.driver_class">com.mysql.cj.jdbc.Driver</property>
        <property name="hibernate.dialect">org.hibernate.dialect.TiDBDialect</property>
        <property name="hibernate.connection.url">jdbc:mysql://localhost:4000/movie</property>
        <property name="hibernate.connection.username">root</property>
        <property name="hibernate.connection.password"></property>
        <property name="hibernate.connection.autocommit">false</property>
        <property name="hibernate.jdbc.batch_size">20</property>

        <!-- Optional: Show SQL output for debugging -->
        <property name="hibernate.show_sql">true</property>
        <property name="hibernate.format_sql">true</property>
    </session-factory>
</hibernate-configuration>
```

每次迭代中，`SELECT` 按主键顺序进行查询，最多选择 1000 行未更新到 10 分制（`ten_point` 为 `false`）数据的主键值。每次 `SELECT` 都会选择比上一次 `SELECT` 结果的最大主键还要大的数据，防止重复。然后，使用批量更新的方式，对其 `score` 列乘 2，并且将 `ten_point` 设为 `true`，更新 `ten_point` 的意义是在于防止更新程序崩溃重启后，反复更新同一行数据，导致数据损坏。每次循环中的 `TimeUnit.SECONDS.sleep(1);` 将使得更新程序暂停 1 秒，防止批量更新程序占用过多的硬件资源。

</div>

</SimpleTab>


---
title: 删除数据
summary: 删除数据、批量删除数据的方法、最佳实践及例子。
---

## 删除数据

此页面将使用 DELETE SQL 语句，对 TiDB 中的数据进行删除。如果需要周期性地删除过期数据，可以考虑使用 TiDB 的 [TTL 功能](#使用-ttl-(time-to-live)-定期删除过期数据)。

### 在开始之前

在阅读本页面之前，你需要准备以下事项：

- [使用 TiDB Cloud (Serverless Tier) 构建 TiDB 集群](#使用-tidb-cloud-(serverless-tier)-构建-tidb-集群)。
- 阅读[数据库模式概览](#概述)，并[创建数据库](#创建数据库)、[创建表](#创建表)、[创建二级索引](#创建二级索引)。
- 需先[插入数据](#插入数据)才可删除。

### SQL 语法

在 SQL 中，`DELETE` 语句一般为以下形式：



```sql
DELETE FROM {table} WHERE {filter}
```

|    参数    |      描述      |
| :--------: | :------------: |
| `{table}`  |      表名      |
| `{filter}` | 过滤器匹配条件 |

此处仅展示 `DELETE` 的简单用法，详细文档可参考 TiDB 的 DELETE 语法。

### 最佳实践

以下是删除行时需要遵循的一些最佳实践：

- 始终在删除语句中指定 `WHERE` 子句。如果 `DELETE` 没有 `WHERE` 子句，TiDB 将删除这个表内的**_所有行_**。
- 需要删除大量行(数万或更多)的时候，使用[批量删除](#批量删除)，这是因为 TiDB 单个事务大小限制为 [txn-total-size-limit](#txn-total-size-limit)（默认为 100MB）。
- 如果你需要删除表内的所有数据，请勿使用 `DELETE` 语句，而应该使用 TRUNCATE 语句。
- 查看 [性能注意事项](#性能注意事项)。
- 在需要大批量删除数据的场景下，[非事务批量删除](#非事务批量删除)对性能的提升十分明显。但与之相对的，这将丢失删除的事务性，因此**无法**进行回滚，请务必正确进行操作选择。

### 例子

假设在开发中发现在特定时间段内，发生了业务错误，需要删除这期间内的所有 [rating](#ratings-表) 的数据，例如，`2022-04-15 00:00:00` 至 `2022-04-15 00:15:00` 的数据。此时，可使用 `SELECT` 语句查看需删除的数据条数：



```sql
SELECT COUNT(*) FROM `ratings` WHERE `rated_at` >= "2022-04-15 00:00:00" AND  `rated_at` <= "2022-04-15 00:15:00";
```

- 若返回数量大于 1 万条，请参考[批量删除](#批量删除)。
- 若返回数量小于 1 万条，可参考下面的示例进行删除：

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在 SQL 中，删除数据的示例如下：

```sql
DELETE FROM `ratings` WHERE `rated_at` >= "2022-04-15 00:00:00" AND  `rated_at` <= "2022-04-15 00:15:00";
```

</div>

<div label="Java" value="java">

在 Java 中，删除数据的示例如下：

```java
// ds is an entity of com.mysql.cj.jdbc.MysqlDataSource

try (Connection connection = ds.getConnection()) {
    String sql = "DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= ? AND  `rated_at` <= ?";
    PreparedStatement preparedStatement = connection.prepareStatement(sql);
    Calendar calendar = Calendar.getInstance();
    calendar.set(Calendar.MILLISECOND, 0);

    calendar.set(2022, Calendar.APRIL, 15, 0, 0, 0);
    preparedStatement.setTimestamp(1, new Timestamp(calendar.getTimeInMillis()));

    calendar.set(2022, Calendar.APRIL, 15, 0, 15, 0);
    preparedStatement.setTimestamp(2, new Timestamp(calendar.getTimeInMillis()));

    preparedStatement.executeUpdate();
} catch (SQLException e) {
    e.printStackTrace();
}
```

</div>

<div label="Golang" value="golang">

在 Golang 中，删除数据的示例如下：

```go
package main

import (
    "database/sql"
    "fmt"
    "time"

    _ "github.com/go-sql-driver/mysql"
)

func main() {
    db, err := sql.Open("mysql", "root:@tcp(127.0.0.1:4000)/bookshop")
    if err != nil {
        panic(err)
    }
    defer db.Close()

    startTime := time.Date(2022, 04, 15, 0, 0, 0, 0, time.UTC)
    endTime := time.Date(2022, 04, 15, 0, 15, 0, 0, time.UTC)

    bulkUpdateSql := fmt.Sprintf("DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= ? AND  `rated_at` <= ?")
    result, err := db.Exec(bulkUpdateSql, startTime, endTime)
    if err != nil {
        panic(err)
    }
    _, err = result.RowsAffected()
    if err != nil {
        panic(err)
    }
}
```

</div>

<div label="Python" value="python">

在 Python 中，删除数据的示例如下：

```python
import MySQLdb
import datetime
import time

connection = MySQLdb.connect(
    host="127.0.0.1",
    port=4000,
    user="root",
    password="",
    database="bookshop",
    autocommit=True
)

with connection:
    with connection.cursor() as cursor:
        start_time = datetime.datetime(2022, 4, 15)
        end_time = datetime.datetime(2022, 4, 15, 0, 15)
        delete_sql = "DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= %s AND `rated_at` <= %s"
        affect_rows = cursor.execute(delete_sql, (start_time, end_time))
        print(f'delete {affect_rows} data')
```

</div>

</SimpleTab>

> **注意：**
>
> `rated_at` 字段为日期和时间类型 中的 `DATETIME` 类型，你可以认为它在 TiDB 保存时，存储为一个字面量，与时区无关。而 `TIMESTAMP` 类型，将会保存一个时间戳，从而在不同的时区配置时，展示不同的时间字符串。
>
> 另外，和 MySQL 一样，`TIMESTAMP` 数据类型受 [2038 年问题](https://zh.wikipedia.org/wiki/2038%E5%B9%B4%E9%97%AE%E9%A2%98)的影响。如果存储的值大于 2038，建议使用 `DATETIME` 类型。

### 性能注意事项

#### TiDB GC 机制

`DELETE` 语句运行之后 TiDB 并非立刻删除数据，而是将这些数据标记为可删除。然后等待 TiDB GC (Garbage Collection) 来清理不再需要的旧数据。因此，你的 `DELETE` 语句**_并不会_**立即减少磁盘用量。

GC 在默认配置中，为 10 分钟触发一次，每次 GC 都会计算出一个名为 **safe_point** 的时间点，这个时间点前的数据，都不会再被使用到，因此，TiDB 可以安全的对数据进行清除。

GC 的具体实现方案和细节此处不再展开，请参考 GC 机制简介 了解更详细的 GC 说明。

#### 更新统计信息

TiDB 使用统计信息来决定索引的选择，因此，在大批量的数据删除之后，很有可能会导致索引选择不准确的情况发生。你可以使用手动收集的办法，更新统计信息。用以给 TiDB 优化器以更准确的统计信息来提供 SQL 性能优化。

### 批量删除

需要删除表中多行的数据，可选择 [`DELETE` 示例](#例子)，并使用 `WHERE` 子句过滤需要删除的数据。

但如果你需要删除大量行（数万或更多）的时候，建议使用一个迭代，每次都只删除一部分数据，直到删除全部完成。这是因为 TiDB 单个事务大小限制为 [txn-total-size-limit](#txn-total-size-limit)（默认为 100MB）。你可以在程序或脚本中使用循环来完成操作。

本页提供了编写脚本来处理循环删除的示例，该示例演示了应如何进行 `SELECT` 和 `DELETE` 的组合，完成循环删除。

#### 编写批量删除循环

在你的应用或脚本的循环中，编写一个 `DELETE` 语句，使用 `WHERE` 子句过滤需要删除的行，并使用 `LIMIT` 限制单次删除的数据条数。

#### 批量删除例子

假设发现在特定时间段内，发生了业务错误，需要删除这期间内的所有 [rating](#ratings-表) 的数据，例如，`2022-04-15 00:00:00` 至 `2022-04-15 00:15:00` 的数据。并且在 15 分钟内，有大于 1 万条数据被写入，此时请使用循环删除的方式进行删除：

<SimpleTab groupId="language">
<div label="Java" value="java">

在 Java 中，批量删除程序类似于以下内容：



```java
package com.pingcap.bulkDelete;

import com.mysql.cj.jdbc.MysqlDataSource;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.util.Calendar;
import java.util.concurrent.TimeUnit;

public class BatchDeleteExample
{
    public static void main(String[] args) throws InterruptedException {
        // Configure the example database connection.

        // Create a mysql data source instance.
        MysqlDataSource mysqlDataSource = new MysqlDataSource();

        // Set server name, port, database name, username and password.
        mysqlDataSource.setServerName("localhost");
        mysqlDataSource.setPortNumber(4000);
        mysqlDataSource.setDatabaseName("bookshop");
        mysqlDataSource.setUser("root");
        mysqlDataSource.setPassword("");

        Integer updateCount = -1;
        while (updateCount != 0) {
            updateCount = batchDelete(mysqlDataSource);
        }
    }

    public static Integer batchDelete (MysqlDataSource ds) {
        try (Connection connection = ds.getConnection()) {
            String sql = "DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= ? AND  `rated_at` <= ? LIMIT 1000";
            PreparedStatement preparedStatement = connection.prepareStatement(sql);
            Calendar calendar = Calendar.getInstance();
            calendar.set(Calendar.MILLISECOND, 0);

            calendar.set(2022, Calendar.APRIL, 15, 0, 0, 0);
            preparedStatement.setTimestamp(1, new Timestamp(calendar.getTimeInMillis()));

            calendar.set(2022, Calendar.APRIL, 15, 0, 15, 0);
            preparedStatement.setTimestamp(2, new Timestamp(calendar.getTimeInMillis()));

            int count = preparedStatement.executeUpdate();
            System.out.println("delete " + count + " data");

            return count;
        } catch (SQLException e) {
            e.printStackTrace();
        }

        return -1;
    }
}
```

每次迭代中，`DELETE` 最多删除 1000 行时间段为 `2022-04-15 00:00:00` 至 `2022-04-15 00:15:00` 的数据。

</div>

<div label="Golang" value="golang">

在 Golang 中，批量删除程序类似于以下内容：



```go
package main

import (
    "database/sql"
    "fmt"
    "time"

    _ "github.com/go-sql-driver/mysql"
)

func main() {
    db, err := sql.Open("mysql", "root:@tcp(127.0.0.1:4000)/bookshop")
    if err != nil {
        panic(err)
    }
    defer db.Close()

    affectedRows := int64(-1)
    startTime := time.Date(2022, 04, 15, 0, 0, 0, 0, time.UTC)
    endTime := time.Date(2022, 04, 15, 0, 15, 0, 0, time.UTC)

    for affectedRows != 0 {
        affectedRows, err = deleteBatch(db, startTime, endTime)
        if err != nil {
            panic(err)
        }
    }
}

// deleteBatch delete at most 1000 lines per batch
func deleteBatch(db *sql.DB, startTime, endTime time.Time) (int64, error) {
    bulkUpdateSql := fmt.Sprintf("DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= ? AND  `rated_at` <= ? LIMIT 1000")
    result, err := db.Exec(bulkUpdateSql, startTime, endTime)
    if err != nil {
        return -1, err
    }
    affectedRows, err := result.RowsAffected()
    if err != nil {
        return -1, err
    }

    fmt.Printf("delete %d data\n", affectedRows)
    return affectedRows, nil
}
```

每次迭代中，`DELETE` 最多删除 1000 行时间段为 `2022-04-15 00:00:00` 至 `2022-04-15 00:15:00` 的数据。

</div>

<div label="Python" value="python">

在 Python 中，批量删除程序类似于以下内容：

```python
import MySQLdb
import datetime
import time

connection = MySQLdb.connect(
    host="127.0.0.1",
    port=4000,
    user="root",
    password="",
    database="bookshop",
    autocommit=True
)

with connection:
    with connection.cursor() as cursor:
        start_time = datetime.datetime(2022, 4, 15)
        end_time = datetime.datetime(2022, 4, 15, 0, 15)
        affect_rows = -1
        while affect_rows != 0:
            delete_sql = "DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= %s AND  `rated_at` <= %s LIMIT 1000"
            affect_rows = cursor.execute(delete_sql, (start_time, end_time))
            print(f'delete {affect_rows} data')
            time.sleep(1)
```

每次迭代中，`DELETE` 最多删除 1000 行时间段为 `2022-04-15 00:00:00` 至 `2022-04-15 00:15:00` 的数据。

</div>

</SimpleTab>

### 非事务批量删除

> **注意：**
>
> TiDB 从 v6.1.0 版本开始支持非事务 DML 语句特性。在 TiDB v6.1.0 以下版本中无法使用此特性。

#### 使用前提

在使用非事务批量删除前，请先**仔细**阅读非事务 DML 语句。非事务批量删除，本质是以牺牲事务的原子性、隔离性为代价，增强批量数据处理场景下的性能和易用性。

因此在使用过程中，需要极为小心，否则，因为操作的非事务特性，在误操作时会导致严重的后果（如数据丢失等）。

#### 非事务批量删除 SQL 语法

非事务批量删除的 SQL 语法如下：



```sql
BATCH ON {shard_column} LIMIT {batch_size} {delete_statement};
```

|    参数    |      描述      |
| :--------: | :------------: |
| `{shard_column}`  |      非事务批量删除的划分列      |
| `{batch_size}` | 非事务批量删除的每批大小 |
| `{delete_statement}` | 删除语句 |

此处仅展示非事务批量删除的简单用法，详细文档可参考 TiDB 的非事务 DML 语句。

#### 非事务批量删除使用示例

以上方[批量删除例子](#批量删除例子)场景为例，可使用以下 SQL 语句进行非事务批量删除：

```sql
BATCH ON `rated_at` LIMIT 1000 DELETE FROM `ratings` WHERE `rated_at` >= "2022-04-15 00:00:00" AND `rated_at` <= "2022-04-15 00:15:00";
```


---
title: 使用 TTL (Time to Live) 定期删除过期数据
summary: 介绍如何通过 SQL 来管理表数据的生命周期
---

## 使用 TTL (Time to Live) 定期删除过期数据

Time to Live (TTL) 提供了行级别的生命周期控制策略。通过为表设置 TTL 属性，TiDB 可以周期性地自动检查并清理表中的过期数据。此功能在一些场景可以有效节省存储空间、提升性能。

TTL 常见的使用场景：

* 定期删除验证码、短网址记录
* 定期删除不需要的历史订单
* 自动删除计算的中间结果

TTL 设计的目标是在不影响在线读写负载的前提下，帮助用户周期性且及时地清理不需要的数据。TTL 会以表为单位，并发地分发不同的任务到不同的 TiDB Server 节点上，进行并行删除处理。TTL 并不保证所有过期数据立即被删除，也就是说即使数据过期了，客户端仍然有可能在这之后的一段时间内读到过期的数据，直到其真正的被后台处理任务删除。

> **警告：**
>
> 当前该功能为实验特性，不建议在生产环境中使用。
> TTL 无法在 [Serverless Tier clusters](https://docs.pingcap.com/tidbcloud/select-cluster-tier#serverless-tier-beta) 上使用。

### 语法

你可以通过 [`CREATE TABLE`](None) 或 [`ALTER TABLE`](None) 语句来配置表的 TTL 功能。

#### 创建具有 TTL 属性的表

- 创建一个具有 TTL 属性的表：

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH;
    ```

    上面的例子创建了一张表 `t1`，并指定了 `created_at` 为 TTL 的时间列，表示数据的创建时间。同时，它还通过 `INTERVAL 3 MONTH` 设置了表中行的最长存活时间为 3 个月。超过了此时长的过期数据会在之后被删除。

- 设置 `TTL_ENABLE` 属性来开启或关闭清理过期数据的功能：

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH TTL_ENABLE = 'OFF';
    ```

    如果 `TTL_ENABLE` 被设置成了 `OFF`，则即使设置了其他 TTL 选项，当前表也不会自动清理过期数据。对于一个设置了 TTL 属性的表，`TTL_ENABLE` 在缺省条件下默认为 `ON`。

- 为了与 MySQL 兼容，你也可以使用注释语法来设置 TTL：

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP
    ) /*T![ttl] TTL = `created_at` + INTERVAL 3 MONTH TTL_ENABLE = 'OFF'*/;
    ```

    在 TiDB 环境中，使用表的 TTL 属性和注释语法来配置 TTL 是等价的。在 MySQL 环境中，会自动忽略注释中的内容，并创建普通的表。

#### 修改表的 TTL 属性

- 修改表的 TTL 属性：

    ```sql
    ALTER TABLE t1 TTL = `created_at` + INTERVAL 1 MONTH;
    ```

    上面的语句既支持修改已配置 TTL 属性的表，也支持为一张非 TTL 的表添加 TTL 属性。

- 单独修改 TTL 表的 `TTL_ENABLE` 值：

    ```sql
    ALTER TABLE t1 TTL_ENABLE = 'OFF';
    ```

- 清除一张表的所有 TTL 属性：

    ```sql
    ALTER TABLE t1 REMOVE TTL;
    ```

#### TTL 和数据类型的默认值

TTL 可以和数据类型的默认值一起使用。以下是两种常见的用法示例：

* 使用 `DEFAULT CURRENT_TIMESTAMP` 来指定某一列的默认值为该行的创建时间，并用这一列作为 TTL 的时间列，创建时间超过 3 个月的数据将被标记为过期：

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH;
    ```

* 指定某一列的默认值为该行的创建时间或更新时间，并用这一列作为 TTL 的时间列，创建时间或更新时间超过 3 个月的数据将被标记为过期：

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    ) TTL = `created_at` + INTERVAL 3 MONTH;
    ```

#### TTL 和生成列

TTL 可以和生成列（实验特性）一起使用，用来表达更加复杂的过期规则。例如：

```sql
CREATE TABLE message (
    id int PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    image bool,
    expire_at TIMESTAMP AS (IF(image,
            created_at + INTERVAL 5 DAY,
            created_at + INTERVAL 30 DAY
    ))
) TTL = `expire_at` + INTERVAL 0 DAY;
```

上述语句的消息以 `expire_at` 列来作为过期时间，并按照消息类型来设定。如果是图片，则 5 天后过期，不然就 30 天后过期。

TTL 还可以和 JSON 类型 一起使用。例如：

```sql
CREATE TABLE orders (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    order_info JSON,
    created_at DATE AS (JSON_EXTRACT(order_info, '$.created_at')) VIRTUAL
) TTL = `created_at` + INTERVAL 3 month;
```

### TTL 任务

对于每张设置了 TTL 属性的表，TiDB 内部会定期调度后台任务来清理过期的数据。你可以通过设置全局变量 [`tidb_ttl_job_run_interval`](#tidb_ttl_job_run_interval-从-v650-版本开始引入) 来自定义任务的执行周期，比如通过下面的语句将后台清理任务设置为每 24 小时执行一次：

```sql
SET @@global.tidb_ttl_job_run_interval = '24h';
```

如果想禁止 TTL 任务的执行，除了可以设置表属性 `TTL_ENABLE='OFF'` 外，也可以通过设置全局变量 `tidb_ttl_job_enable` 关闭整个集群的 TTL 任务的执行。

```sql
SET @@global.tidb_ttl_job_enable = OFF;
```

在某些场景下，你可能希望只允许在每天的某个时间段内调度后台的 TTL 任务，此时可以设置全局变量 [`tidb_ttl_job_schedule_window_start_time`](#tidb_ttl_job_schedule_window_start_time-从-v650-版本开始引入) 和 [`tidb_ttl_job_schedule_window_end_time`](#tidb_ttl_job_schedule_window_end_time-从-v650-版本开始引入) 来指定时间窗口，比如：

```sql
SET @@global.tidb_ttl_job_schedule_window_start_time = '01:00 +0000';
SET @@global.tidb_ttl_job_schedule_window_end_time = '05:00 +0000';
```

上述语句只允许在 UTC 时间的凌晨 1 点到 5 点调度 TTL 任务。默认情况下的时间窗口设置为 `00:00 +0000` 到 `23:59 +0000`，即允许所有时段的任务调度。

### 监控与图表

TiDB 会定时采集 TTL 的运行时信息，并在 Grafana 中提供了相关指标的可视化图表。你可以在 TiDB -> TTL 的面板下看到这些信息。指标详情见 TiDB 重要监控指标详解 中的 `TTL` 部分。

### 工具兼容性

作为实验特性，TTL 特性暂时不兼容包括 BR、TiDB Lightning、TiCDC 在内的数据导入导出以及同步工具。

### 使用限制

目前，TTL 特性具有以下限制:

* 不允许在临时表上设置 TTL 属性，包括本地临时表和全局临时表。
* 具有 TTL 属性的表不支持作为外键约束的主表被其他表引用。
* 不保证所有过期数据立即被删除，过期数据被删除的时间取决于后台清理任务的调度周期和调度窗口。
* 目前单个表的清理任务同时只能在同一个 TiDB Server 节点运行，这在某些场景下（比如表特别大的情况）可能会产生性能瓶颈。此问题会在后续版本中优化。


---
title: 预处理语句
summary: 介绍 TiDB 的预处理语句功能。
---

## 预处理语句

预处理语句是一种将多个仅有参数不同的 SQL 语句进行模板化的语句，它让 SQL 语句与参数进行了分离。可以用它提升 SQL 语句的：

- 安全性：因为参数和语句已经分离，所以避免了 [SQL 注入攻击](https://en.wikipedia.org/wiki/SQL_injection)的风险。
- 性能：因为语句在 TiDB 端被预先解析，后续执行只需要传递参数，节省了完整 SQL 解析、拼接 SQL 语句字符串以及网络传输的代价。

在大部分的应用程序中，SQL 语句是可以被枚举的，可以使用有限个 SQL 语句来完成整个应用程序的数据查询，所以使用预处理语句是最佳实践之一。

### SQL 语法

本节将介绍创建、使用及删除预处理语句的 SQL 语法。

#### 创建预处理语句



```sql
PREPARE {prepared_statement_name} FROM '{prepared_statement_sql}';
```

|            参数             |                  描述                  |
| :-------------------------: | :------------------------------------: |
| `{prepared_statement_name}` |             预处理语句名称             |
| `{prepared_statement_sql}`  | 预处理语句 SQL，以英文半角问号做占位符 |

你可查看 PREPARE 语句 获得更多信息。

#### 使用预处理语句

预处理语句仅可使用用户变量作为参数，因此，需先使用 SET 语句 设置变量后，供 EXECUTE 语句 调用预处理语句。



```sql
SET @{parameter_name} = {parameter_value};
EXECUTE {prepared_statement_name} USING @{parameter_name};
```

|            参数             |                                 描述                                  |
| :-------------------------: | :-------------------------------------------------------------------: |
|     `{parameter_name}`      |                              用户参数名                               |
|     `{parameter_value}`     |                              用户参数值                               |
| `{prepared_statement_name}` | 预处理语句名称，需和[创建预处理语句](#创建预处理语句)中定义的名称一致 |

你可查看 EXECUTE 语句 获得更多信息。

#### 删除预处理语句



```sql
DEALLOCATE PREPARE {prepared_statement_name};
```

|            参数             |                                 描述                                  |
| :-------------------------: | :-------------------------------------------------------------------: |
| `{prepared_statement_name}` | 预处理语句名称，需和[创建预处理语句](#创建预处理语句)中定义的名称一致 |

你可查看 DEALLOCATE 语句 获得更多信息。

### 例子

本节以使用预处理语句，完成查询数据和插入数据两个场景的示例。

#### 查询示例

例如，需要查询 [Bookshop 应用](#books-表) 中，`id` 为 1 的书籍信息。

<SimpleTab groupId="language">

<div label="SQL" value="sql">

使用 SQL 查询示例：

```sql
PREPARE `books_query` FROM 'SELECT * FROM `books` WHERE `id` = ?';
```

运行结果为：

```
Query OK, 0 rows affected (0.01 sec)
```



```sql
SET @id = 1;
```

运行结果为：

```
Query OK, 0 rows affected (0.04 sec)
```



```sql
EXECUTE `books_query` USING @id;
```

运行结果为：

```
+---------+---------------------------------+--------+---------------------+-------+--------+
| id      | title                           | type   | published_at        | stock | price  |
+---------+---------------------------------+--------+---------------------+-------+--------+
| 1       | The Adventures of Pierce Wehner | Comics | 1904-06-06 20:46:25 |   586 | 411.66 |
+---------+---------------------------------+--------+---------------------+-------+--------+
1 row in set (0.05 sec)
```

</div>

<div label="Java" value="java">

使用 Java 查询示例：

```java
// ds is an entity of com.mysql.cj.jdbc.MysqlDataSource
try (Connection connection = ds.getConnection()) {
    PreparedStatement preparedStatement = connection.prepareStatement("SELECT * FROM `books` WHERE `id` = ?");
    preparedStatement.setLong(1, 1);

    ResultSet res = preparedStatement.executeQuery();
    if(!res.next()) {
        System.out.println("No books in the table with id 1");
    } else {
        // got book's info, which id is 1
        System.out.println(res.getLong("id"));
        System.out.println(res.getString("title"));
        System.out.println(res.getString("type"));
    }
} catch (SQLException e) {
    e.printStackTrace();
}
```

</div>

</SimpleTab>

#### 插入示例

还是使用 [books 表](#books-表) 为例，需要插入一个 `title` 为 `TiDB Developer Guide`, `type` 为 `Science & Technology`, `stock` 为 `100`, `price` 为 `0.0`, `published_at` 为 `插入的当前时间` 的书籍信息。需要注意的是，`books` 表的主键包含 `AUTO_RANDOM` 属性，无需指定它。如果你对插入数据还不了解，可以在[插入数据](#插入数据)一节了解更多数据插入的相关信息。

<SimpleTab groupId="language">

<div label="SQL" value="sql">

使用 SQL 插入数据示例如下：

```sql
PREPARE `books_insert` FROM 'INSERT INTO `books` (`title`, `type`, `stock`, `price`, `published_at`) VALUES (?, ?, ?, ?, ?);';
```

运行结果为：

```
Query OK, 0 rows affected (0.03 sec)
```



```sql
SET @title = 'TiDB Developer Guide';
SET @type = 'Science & Technology';
SET @stock = 100;
SET @price = 0.0;
SET @published_at = NOW();
```

运行结果为：

```
Query OK, 0 rows affected (0.04 sec)
```



```sql
EXECUTE `books_insert` USING @title, @type, @stock, @price, @published_at;
```

运行结果为：

```
Query OK, 1 row affected (0.03 sec)
```

</div>

<div label="Java" value="java">

使用 Java 插入数据示例如下：

```java
try (Connection connection = ds.getConnection()) {
    String sql = "INSERT INTO `books` (`title`, `type`, `stock`, `price`, `published_at`) VALUES (?, ?, ?, ?, ?);";
    PreparedStatement preparedStatement = connection.prepareStatement(sql);

    preparedStatement.setString(1, "TiDB Developer Guide");
    preparedStatement.setString(2, "Science & Technology");
    preparedStatement.setInt(3, 100);
    preparedStatement.setBigDecimal(4, new BigDecimal("0.0"));
    preparedStatement.setTimestamp(5, new Timestamp(Calendar.getInstance().getTimeInMillis()));

    preparedStatement.executeUpdate();
} catch (SQLException e) {
    e.printStackTrace();
}
```

可以看到，JDBC 帮你管控了预处理语句的生命周期，而无需你在应用程序里手动使用预处理语句的创建、使用、删除等。但值得注意的是，因为 TiDB 兼容 MySQL 协议，在客户端使用 MySQL JDBC Driver 的过程中，其默认配置并非开启 **_服务端_** 的预处理语句选项，而是使用客户端的预处理语句。你需要关注以下配置项，来获得在 JDBC 下 TiDB 服务端预处理语句的支持，及在你的使用场景下的最佳配置：

|          参数           |                 作用                  |           推荐场景           |         推荐配置         |
| :---------------------: | :-----------------------------------: | :--------------------------: | :----------------------: |
|  `useServerPrepStmts`   |   是否使用服务端开启预处理语句支持    |  在需要多次使用预处理语句时  |          `true`          |
|    `cachePrepStmts`     |       客户端是否缓存预处理语句        | `useServerPrepStmts=true` 时 |          `true`          |
| `prepStmtCacheSqlLimit` |  预处理语句最大大小（默认 256 字符）  |  预处理语句大于 256 字符时   | 按实际预处理语句大小配置 |
|   `prepStmtCacheSize`   | 预处理语句最大缓存数量 （默认 25 条） |  预处理语句数量大于 25 条时  | 按实际预处理语句数量配置 |

在此处给出一个较为的通用场景的 JDBC 连接字符串配置，以 Host: `127.0.0.1`，Port: `4000`，用户: `root`，密码: 空 ，默认数据库: `test`为例：

```
jdbc:mysql://127.0.0.1:4000/test?user=root&useConfigs=maxPerformance&useServerPrepStmts=true&prepStmtCacheSqlLimit=2048&prepStmtCacheSize=256&rewriteBatchedStatements=true&allowMultiQueries=true
```

你也可以查看[插入行](#插入行)一章，来查看是否需要在插入数据场景下更改其他 JDBC 的参数。

有关 Java 的完整示例，可参阅：

- [TiDB 和 Java 的简单 CRUD 应用程序 - 使用 JDBC](#第-2-步获取代码)。
- [TiDB 和 Java 的简单 CRUD 应用程序 - 使用 Hibernate](#第-2-步获取代码)。
- [Build the TiDB Application using Spring Boot](#使用-spring-boot-构建-tidb-应用程序)。

</div>

</SimpleTab>



# 数据读取

---
title: 单表查询
summary: 介绍 TiDB 中的单表查询功能。
---

<!-- markdownlint-disable MD029 -->

## 单表查询

在这个章节当中，将开始介绍如何使用 SQL来对数据库中的数据进行查询。

### 开始之前

下面将围绕 [Bookshop](#bookshop-应用) 这个应用程序来对 TiDB 的数据查询部分展开介绍。

在阅读本章节之前，你需要做以下准备工作：

1. 构建 TiDB 集群（推荐使用 [TiDB Cloud](#使用-tidb-cloud-(serverless-tier)-构建-tidb-集群) 或 TiUP）。
2. [导入 Bookshop 应用程序的表结构和示例数据](#导入表结构和数据)。
3. [连接到 TiDB](#连接到-tidb)。

### 简单的查询

在 Bookshop 应用程序的数据库当中，`authors` 表存放了作家们的基础信息，可以通过 `SELECT ... FROM ...` 语句将数据从数据库当中调取出去。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在 MySQL Client 等客户端输入并执行如下 SQL 语句：

```sql
SELECT id, name FROM authors;
```

输出结果如下：

```
+------------+--------------------------+
| id         | name                     |
+------------+--------------------------+
|       6357 | Adelle Bosco             |
|     345397 | Chanelle Koepp           |
|     807584 | Clementina Ryan          |
|     839921 | Gage Huel                |
|     850070 | Ray Armstrong            |
|     850362 | Ford Waelchi             |
|     881210 | Jayme Gutkowski          |
|    1165261 | Allison Kuvalis          |
|    1282036 | Adela Funk               |
...
| 4294957408 | Lyla Nitzsche            |
+------------+--------------------------+
20000 rows in set (0.05 sec)
```

</div>
<div label="Java" value="java">

在 Java 语言当中，可以通过声明一个 `Author` 类来定义如何存放作者的基础信息，根据数据的类型和取值范围从 Java 语言当中选择合适的数据类型来存放对应的数据，例如：

- 使用 `Int` 类型变量存放 `int` 类型的数据。
- 使用 `Long` 类型变量存放 `bigint` 类型的数据。
- 使用 `Short` 类型变量存放 `tinyint` 类型的数据。
- 使用 `String` 类型变量存放 `varchar` 类型的数据。
- ...



```java
public class Author {
    private Long id;
    private String name;
    private Short gender;
    private Short birthYear;
    private Short deathYear;

    public Author() {}

     // Skip the getters and setters.
}
```



```java
public class AuthorDAO {

    // Omit initialization of instance variables.

    public List<Author> getAuthors() throws SQLException {
        List<Author> authors = new ArrayList<>();

        try (Connection conn = ds.getConnection()) {
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT id, name FROM authors");
            while (rs.next()) {
                Author author = new Author();
                author.setId(rs.getLong("id"));
                author.setName(rs.getString("name"));
                authors.add(author);
            }
        }
        return authors;
    }
}
```

- 在[获得数据库连接](#jdbc)之后，你可以通过 `conn.createStatement()` 语句创建一个 `Statement` 实例对象。
- 然后调用 `stmt.executeQuery("query_sql")` 方法向 TiDB 发起一个数据库查询请求。
- 数据库返回的查询结果将会存放到 `ResultSet` 当中，通过遍历 `ResultSet` 对象可以将返回结果映射到此前准备的 `Author` 类对象当中。

</div>
</SimpleTab>

### 对结果进行筛选

查询得到的结果非常多，但是并不都是你想要的？可以通过 `WHERE` 语句对查询的结果进行过滤，从而找到想要查询的部分。

例如，想要查找众多作家当中找出在 1998 年出生的作家：

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在 SQL 中，可以使用 `WHERE` 子句添加筛选的条件：

```sql
SELECT * FROM authors WHERE birth_year = 1998;
```

</div>
<div label="Java" value="java">

对于 Java 程序而言，可以通过同一个 SQL 来处理带有动态参数的数据查询请求。

将参数拼接到 SQL 语句当中也许是一种方法，但是这可能不是一个好的主意，因为这会给应用程序带来潜在的 [SQL 注入](https://zh.wikipedia.org/wiki/SQL%E6%B3%A8%E5%85%A5)风险。

在处理这类查询时，应该使用 [PreparedStatement](#预处理语句) 来替代普通的 Statement。

```java
public List<Author> getAuthorsByBirthYear(Short birthYear) throws SQLException {
    List<Author> authors = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        PreparedStatement stmt = conn.prepareStatement("""
        SELECT * FROM authors WHERE birth_year = ?;
        """);
        stmt.setShort(1, birthYear);
        ResultSet rs = stmt.executeQuery();
        while (rs.next()) {
            Author author = new Author();
            author.setId(rs.getLong("id"));
            author.setName(rs.getString("name"));
            authors.add(author);
        }
    }
    return authors;
}
```

</div>
</SimpleTab>

### 对结果进行排序

使用 `ORDER BY` 语句可以让查询结果按照期望的方式进行排序。

例如，可以通过下面的 SQL 语句对 `authors` 表的数据按照 `birth_year` 列进行降序 (`DESC`) 排序，从而得到最年轻的作家列表。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

```sql
SELECT id, name, birth_year
FROM authors
ORDER BY birth_year DESC;
```

</div>

<div label="Java" value="java">

```java
public List<Author> getAuthorsSortByBirthYear() throws SQLException {
    List<Author> authors = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery("""
            SELECT id, name, birth_year
            FROM authors
            ORDER BY birth_year DESC;
            """);

        while (rs.next()) {
            Author author = new Author();
            author.setId(rs.getLong("id"));
            author.setName(rs.getString("name"));
            author.setBirthYear(rs.getShort("birth_year"));
            authors.add(author);
        }
    }
    return authors;
}
```

</div>
</SimpleTab>

查询结果如下：

```
+-----------+------------------------+------------+
| id        | name                   | birth_year |
+-----------+------------------------+------------+
| 83420726  | Terrance Dach          | 2000       |
| 57938667  | Margarita Christiansen | 2000       |
| 77441404  | Otto Dibbert           | 2000       |
| 61338414  | Danial Cormier         | 2000       |
| 49680887  | Alivia Lemke           | 2000       |
| 45460101  | Itzel Cummings         | 2000       |
| 38009380  | Percy Hodkiewicz       | 2000       |
| 12943560  | Hulda Hackett          | 2000       |
| 1294029   | Stanford Herman        | 2000       |
| 111453184 | Jeffrey Brekke         | 2000       |
...
300000 rows in set (0.23 sec)
```

### 限制查询结果数量

如果希望 TiDB 只返回部分结果，可以使用 `LIMIT` 语句限制查询结果返回的记录数。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

```sql
SELECT id, name, birth_year
FROM authors
ORDER BY birth_year DESC
LIMIT 10;
```

</div>

<div label="Java" value="java">

```java
public List<Author> getAuthorsWithLimit(Integer limit) throws SQLException {
    List<Author> authors = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        PreparedStatement stmt = conn.prepareStatement("""
            SELECT id, name, birth_year
            FROM authors
            ORDER BY birth_year DESC
            LIMIT ?;
            """);
        stmt.setInt(1, limit);
        ResultSet rs = stmt.executeQuery();
        while (rs.next()) {
            Author author = new Author();
            author.setId(rs.getLong("id"));
            author.setName(rs.getString("name"));
            author.setBirthYear(rs.getShort("birth_year"));
            authors.add(author);
        }
    }
    return authors;
}
```

</div>
</SimpleTab>

查询结果如下：

```
+-----------+------------------------+------------+
| id        | name                   | birth_year |
+-----------+------------------------+------------+
| 83420726  | Terrance Dach          | 2000       |
| 57938667  | Margarita Christiansen | 2000       |
| 77441404  | Otto Dibbert           | 2000       |
| 61338414  | Danial Cormier         | 2000       |
| 49680887  | Alivia Lemke           | 2000       |
| 45460101  | Itzel Cummings         | 2000       |
| 38009380  | Percy Hodkiewicz       | 2000       |
| 12943560  | Hulda Hackett          | 2000       |
| 1294029   | Stanford Herman        | 2000       |
| 111453184 | Jeffrey Brekke         | 2000       |
+-----------+------------------------+------------+
10 rows in set (0.11 sec)
```

通过观察查询结果你会发现，在使用 `LIMIT` 语句之后，查询的时间明显缩短，这是 TiDB 对 `LIMIT` 子句进行优化后的结果，你可以通过 TopN 和 Limit 下推章节了解更多细节。

### 聚合查询

如果你想要关注数据整体的情况，而不是部分数据，你可以通过使用 `GROUP BY` 语句配合聚合函数，构建一个聚合查询来帮助你对数据的整体情况有一个更好的了解。

比如说，你希望知道哪些年出生的作家比较多，你可以将作家基本信息按照 `birth_year` 列进行分组，然后分别统计在当年出生的作家数量：

<SimpleTab groupId="language">
<div label="SQL" value="sql">

```sql
SELECT birth_year, COUNT(DISTINCT id) AS author_count
FROM authors
GROUP BY birth_year
ORDER BY author_count DESC;
```

</div>

<div label="Java" value="java">

```java
public class AuthorCount {
    private Short birthYear;
    private Integer authorCount;

    public AuthorCount() {}

     // Skip the getters and setters.
}

public List<AuthorCount> getAuthorCountsByBirthYear() throws SQLException {
    List<AuthorCount> authorCounts = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery("""
            SELECT birth_year, COUNT(DISTINCT id) AS author_count
            FROM authors
            GROUP BY birth_year
            ORDER BY author_count DESC;
            """);

        while (rs.next()) {
            AuthorCount authorCount = new AuthorCount();
            authorCount.setBirthYear(rs.getShort("birth_year"));
            authorCount.setAuthorCount(rs.getInt("author_count"));
            authorCounts.add(authorCount);
        }
    }
    return authorCount;
}
```

</div>
</SimpleTab>

查询结果如下：

```
+------------+--------------+
| birth_year | author_count |
+------------+--------------+
|       1932 |          317 |
|       1947 |          290 |
|       1939 |          282 |
|       1935 |          289 |
|       1968 |          291 |
|       1962 |          261 |
|       1961 |          283 |
|       1986 |          289 |
|       1994 |          280 |
...
|       1972 |          306 |
+------------+--------------+
71 rows in set (0.00 sec)
```

除了 `COUNT` 函数外，TiDB 还支持了其他聚合函数。详情请参考 GROUP BY 聚合函数。


---
title: 多表连接查询
summary: 介绍 TiDB 中的多表连接查询功能。
---

## 多表连接查询

很多时候，应用程序需要在一个查询当中使用到多张表的数据，这个时候可以通过 `JOIN` 语句将两张或多张表的数据组合在一起。

### Join 类型

此节将详细叙述 Join 的连接类型。

#### 内连接 INNER JOIN

内连接的连接结果只返回匹配连接条件的行。

例如，想要知道编写过最多书的作家是谁，需要将作家基础信息表 `authors` 与书籍作者表 `book_authors` 进行连接。

![Inner Join](./media/develop/inner-join.png)

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在下面的 SQL 语句当中，通过关键字 `JOIN` 声明要将左表 `authors` 和右表 `book_authors` 的数据行以内连接的方式进行连接，连接条件为 `a.id = ba.author_id`，那么连接的结果集当中将只会包含满足连接条件的行。假设有一个作家没有编写过任何书籍，那么他在 `authors` 表当中的记录将无法满足连接条件，因此也不会出现在结果集当中。



```sql
SELECT ANY_VALUE(a.id) AS author_id, ANY_VALUE(a.name) AS author_name, COUNT(ba.book_id) AS books
FROM authors a
JOIN book_authors ba ON a.id = ba.author_id
GROUP BY ba.author_id
ORDER BY books DESC
LIMIT 10;
```

查询结果如下：

```
+------------+----------------+-------+
| author_id  | author_name    | books |
+------------+----------------+-------+
|  431192671 | Emilie Cassin  |     7 |
|  865305676 | Nola Howell    |     7 |
|  572207928 | Lamar Koch     |     6 |
| 3894029860 | Elijah Howe    |     6 |
| 1150614082 | Cristal Stehr  |     6 |
| 4158341032 | Roslyn Rippin  |     6 |
| 2430691560 | Francisca Hahn |     6 |
| 3346415350 | Leta Weimann   |     6 |
| 1395124973 | Albin Cole     |     6 |
| 2768150724 | Caleb Wyman    |     6 |
+------------+----------------+-------+
10 rows in set (0.01 sec)
```

</div>
<div label="Java" value="java">

在 Java 中内连接的示例如下：

```java
public List<Author> getTop10AuthorsOrderByBooks() throws SQLException {
    List<Author> authors = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery("""
        SELECT ANY_VALUE(a.id) AS author_id, ANY_VALUE(a.name) AS author_name, COUNT(ba.book_id) AS books
        FROM authors a
        JOIN book_authors ba ON a.id = ba.author_id
        GROUP BY ba.author_id
        ORDER BY books DESC
        LIMIT 10;
        """);
        while (rs.next()) {
            Author author = new Author();
            author.setId(rs.getLong("author_id"));
            author.setName(rs.getString("author_name"));
            author.setBooks(rs.getInt("books"));
            authors.add(author);
        }
    }
    return authors;
}
```

</div>
</SimpleTab>

#### 左外连接 LEFT OUTER JOIN

左外连接会返回左表中的所有数据行，以及右表当中能够匹配连接条件的值，如果在右表当中没有找到能够匹配的行，则使用 `NULL` 填充。

![Left Outer Join](./media/develop/left-outer-join.png)

在一些情况下，希望使用多张表来完成数据的查询，但是并不希望因为不满足连接条件而导致数据集变小。

例如，在 Bookshop 应用的首页，希望展示一个带有平均评分的最新书籍列表。在这种情况下，最新的书籍可能是还没有经过任何人评分的，如果使用内连接就会导致这些无人评分的书籍信息被过滤掉，而这并不是期望的结果。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在下面的 SQL 语句当中，通过 `LEFT JOIN` 关键字声明左表 `books` 将以左外连接的方式与右表 `ratings` 进行连接，从而确保 `books` 表当中的所有记录都能得到返回。



```sql
SELECT b.id AS book_id, ANY_VALUE(b.title) AS book_title, AVG(r.score) AS average_score
FROM books b
LEFT JOIN ratings r ON b.id = r.book_id
GROUP BY b.id
ORDER BY b.published_at DESC
LIMIT 10;
```

查询结果如下：

```
+------------+---------------------------------+---------------+
| book_id    | book_title                      | average_score |
+------------+---------------------------------+---------------+
| 3438991610 | The Documentary of lion         |        2.7619 |
| 3897175886 | Torey Kuhn                      |        3.0000 |
| 1256171496 | Elmo Vandervort                 |        2.5500 |
| 1036915727 | The Story of Munchkin           |        2.0000 |
|  270254583 | Tate Kovacek                    |        2.5000 |
| 1280950719 | Carson Damore                   |        3.2105 |
| 1098041838 | The Documentary of grasshopper  |        2.8462 |
| 1476566306 | The Adventures of Vince Sanford |        2.3529 |
| 4036300890 | The Documentary of turtle       |        2.4545 |
| 1299849448 | Antwan Olson                    |        3.0000 |
+------------+---------------------------------+---------------+
10 rows in set (0.30 sec)
```

看起来最新出版的书籍已经有了很多评分，为了验证上面所说的，通过 SQL 语句把 **The Documentary of lion** 这本书的所有评分给删掉：



```sql
DELETE FROM ratings WHERE book_id = 3438991610;
```

再次查询，你会发现 **The Documentary of lion** 这本书依然出现在结果集当中，但是通过右表 `ratings` 的 `score` 列计算得到的 `average_score` 列被填上了 `NULL`。

```
+------------+---------------------------------+---------------+
| book_id    | book_title                      | average_score |
+------------+---------------------------------+---------------+
| 3438991610 | The Documentary of lion         |          NULL |
| 3897175886 | Torey Kuhn                      |        3.0000 |
| 1256171496 | Elmo Vandervort                 |        2.5500 |
| 1036915727 | The Story of Munchkin           |        2.0000 |
|  270254583 | Tate Kovacek                    |        2.5000 |
| 1280950719 | Carson Damore                   |        3.2105 |
| 1098041838 | The Documentary of grasshopper  |        2.8462 |
| 1476566306 | The Adventures of Vince Sanford |        2.3529 |
| 4036300890 | The Documentary of turtle       |        2.4545 |
| 1299849448 | Antwan Olson                    |        3.0000 |
+------------+---------------------------------+---------------+
10 rows in set (0.30 sec)
```

如果改成使用的是内连接 `JOIN` 结果会怎样？这就交给你来尝试了。

</div>
<div label="Java" value="java">

在 Java 中左外连接的示例如下：

```java
public List<Book> getLatestBooksWithAverageScore() throws SQLException {
    List<Book> books = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery("""
        SELECT b.id AS book_id, ANY_VALUE(b.title) AS book_title, AVG(r.score) AS average_score
        FROM books b
        LEFT JOIN ratings r ON b.id = r.book_id
        GROUP BY b.id
        ORDER BY b.published_at DESC
        LIMIT 10;
        """);
        while (rs.next()) {
            Book book = new Book();
            book.setId(rs.getLong("book_id"));
            book.setTitle(rs.getString("book_title"));
            book.setAverageScore(rs.getFloat("average_score"));
            books.add(book);
        }
    }
    return books;
}
```

</div>
</SimpleTab>

#### 右外连接 RIGHT OUTER JOIN

右外连接返回右表中的所有记录，以及左表当中能够匹配连接条件的值，没有匹配的值则使用 `NULL` 填充。

![Right Outer Join](./media/develop/right-outer-join.png)

#### 交叉连接 CROSS JOIN

当连接条件恒成立时，两表之间的内连接称为[交叉连接](https://zh.wikipedia.org/wiki/%E8%BF%9E%E6%8E%A5#%E4%BA%A4%E5%8F%89%E8%BF%9E%E6%8E%A5)（又被称为“笛卡尔连接”）。交叉连接会把左表的每一条记录和右表的所有记录相连接，如果左表的记录数为 m, 右表的记录数为 n，则结果集中会产生 m \* n 条记录。

#### 左半连接 LEFT SEMI JOIN

TiDB 在 SQL 语法层面上不支持 `LEFT SEMI JOIN table_name`，但是在执行计划层面，子查询相关的优化会将 `semi join` 作为改写后的等价 JOIN 查询默认的连接方式。

### 隐式连接

在显式声明连接的 `JOIN` 语句作为 SQL 标准出现之前，在 SQL 语句当中可以通过 `FROM t1, t2` 子句来连接两张或多张表，通过 `WHERE t1.id = t2.id` 子句来指定连接的条件。你可以将其理解为隐式声明的连接，隐式连接会使用内连接的方式进行连接。

### Join 相关算法

TiDB 支持下列三种常规的表连接算法，优化器会根据所连接表的数据量等因素来选择合适的 Join 算法去执行。你可以通过 `EXPLAIN` 语句来查看查询使用了何种算法进行 Join。

- Index Join
- Hash Join
- Merge Join

如果发现 TiDB 的优化器没有按照最佳的 Join 算法去执行。你也可以通过 Optimizer Hints 强制 TiDB 使用更好的 Join 算法去执行。

例如，假设上文当中的左连接查询的示例 SQL 使用 Hash Join 算法执行更快，而优化器并没有选择这种算法，你可以在 `SELECT` 关键字后面加上 Hint `/*+ HASH_JOIN(b, r) */`（注意：如果表名添加了别名，Hint 当中也应该使用表别名）。



```sql
EXPLAIN SELECT /*+ HASH_JOIN(b, r) */ b.id AS book_id, ANY_VALUE(b.title) AS book_title, AVG(r.score) AS average_score
FROM books b
LEFT JOIN ratings r ON b.id = r.book_id
GROUP BY b.id
ORDER BY b.published_at DESC
LIMIT 10;
```

Join 算法相关的 Hints：

- [MERGE_JOIN(t1_name [, tl_name ...])](#merge_joint1_name--tl_name-)
- [INL_JOIN(t1_name [, tl_name ...])](#inl_joint1_name--tl_name-)
- [INL_HASH_JOIN(t1_name [, tl_name ...])](#inl_hash_join)
- [HASH_JOIN(t1_name [, tl_name ...])](#hash_joint1_name--tl_name-)

### Join 顺序

在实际的业务场景中，多个表的 Join 语句是很常见的，而 Join 的执行效率和各个表参与 Join 的顺序有关。TiDB 使用 Join Reorder 算法来确定多个表进行 Join 的顺序。

当优化器选择的 Join 顺序并不够好时，你可以使用 `STRAIGHT_JOIN` 语法让 TiDB 强制按照 FROM 子句中所使用的表的顺序做联合查询。



```sql
EXPLAIN SELECT *
FROM authors a STRAIGHT_JOIN book_authors ba STRAIGHT_JOIN books b
WHERE b.id = ba.book_id AND ba.author_id = a.id;
```

关于该算法的实现细节和限制你可以通过查看Join Reorder 算法简介章节进行了解。

### 扩展阅读

- 用 EXPLAIN 查看 JOIN 查询的执行计划
- Join Reorder 算法简介


---
title: 子查询
summary: 介绍 TiDB 子查询功能。
---

## 子查询

本章将介绍 TiDB 中的子查询功能。

### 概述

子查询是嵌套在另一个查询中的 SQL 表达式，借助子查询，可以在一个查询当中使用另外一个查询的查询结果。

下面将以 [Bookshop](#bookshop-应用) 应用为例对子查询展开介绍：

### 子查询语句

通常情况下，子查询语句分为如下几种形式：

- 标量子查询（Scalar Subquery），如 `SELECT (SELECT s1 FROM t2) FROM t1`。
- 派生表（Derived Tables），如 `SELECT t1.s1 FROM (SELECT s1 FROM t2) t1`。
- 存在性测试（Existential Test），如 `WHERE NOT EXISTS(SELECT ... FROM t2)`，`WHERE t1.a IN (SELECT ... FROM t2)`。
- 集合比较（Quantified Comparison），如 `WHERE t1.a = ANY(SELECT ... FROM t2)`。
- 作为比较运算符操作数的子查询, 如 `WHERE t1.a > (SELECT ... FROM t2)`。

### 子查询的分类

一般来说，可以将子查询分为关联子查询（[Correlated Subquery](https://en.wikipedia.org/wiki/Correlated_subquery)）和无关联子查询 (Self-contained Subquery) 两大类，TiDB 对于这两类子查询的处理方式是不一样的。

判断是否为关联子查询的依据在于子查询当中是否引用了外层查询的列。

#### 无关联子查询

对于将子查询作为比较运算符 (`>` / `>=`/ `<` / `<=` / `=` / `!=`) 操作数的这类无关联子查询而言，内层子查询只需要进行一次查询，TiDB 在生成执行计划阶段会将内层子查询改写为常量。

例如，想要查找 `authors` 表当中年龄大于总体平均年龄的作家，可以通过将子查询作为比较操作符的操作数来实现：



```sql
SELECT * FROM authors a1 WHERE (IFNULL(a1.death_year, YEAR(NOW())) - a1.birth_year) > (
    SELECT
        AVG(IFNULL(a2.death_year, YEAR(NOW())) - a2.birth_year) AS average_age
    FROM
        authors a2
)
```

在 TiDB 执行上述查询的时候会先执行一次内层子查询：



```sql
SELECT AVG(IFNULL(a2.death_year, YEAR(NOW())) - a2.birth_year) AS average_age FROM authors a2;
```

假设查询得到的结果为 34，即总体平均年龄为 34，34 将作为常量替换掉原来的子查询。



```sql
SELECT * FROM authors a1
WHERE (IFNULL(a1.death_year, YEAR(NOW())) - a1.birth_year) > 34;
```

运行结果为：

```
+--------+-------------------+--------+------------+------------+
| id     | name              | gender | birth_year | death_year |
+--------+-------------------+--------+------------+------------+
| 13514  | Kennith Kautzer   | 1      | 1956       | 2018       |
| 13748  | Dillon Langosh    | 1      | 1985       | NULL       |
| 99184  | Giovanny Emmerich | 1      | 1954       | 2012       |
| 180191 | Myrtie Robel      | 1      | 1958       | 2009       |
| 200969 | Iva Renner        | 0      | 1977       | NULL       |
| 209671 | Abraham Ortiz     | 0      | 1943       | 2016       |
| 229908 | Wellington Wiza   | 1      | 1932       | 1969       |
| 306642 | Markus Crona      | 0      | 1969       | NULL       |
| 317018 | Ellis McCullough  | 0      | 1969       | 2014       |
| 322369 | Mozelle Hand      | 0      | 1942       | 1977       |
| 325946 | Elta Flatley      | 0      | 1933       | 1986       |
| 361692 | Otho Langosh      | 1      | 1931       | 1997       |
| 421294 | Karelle VonRueden | 0      | 1977       | NULL       |
...
```

对于存在性测试和集合比较两种情况下的无关联列子查询，TiDB 会将其进行改写和等价替换以获得更好的执行性能，你可以通过阅读子查询相关的优化章节来了解更多的实现细节。

### 关联子查询

对于关联子查询而言，由于内层的子查询引用外层查询的列，子查询需要对外层查询得到的每一行都执行一遍，也就是说假设外层查询得到一千万的结果，那么子查询也会被执行一千万次，这会导致查询需要消耗更多的时间和资源。

因此在处理过程中，TiDB 会尝试对关联子查询去关联，以从执行计划层面上提高查询效率。

例如，假设想要查找那些大于其它相同性别作家的平均年龄的的作家，SQL 语句可以这样写：



```sql
SELECT * FROM authors a1 WHERE (IFNULL(a1.death_year, YEAR(NOW())) - a1.birth_year) > (
    SELECT
        AVG(
            IFNULL(a2.death_year, YEAR(NOW())) - IFNULL(a2.birth_year, YEAR(NOW()))
        ) AS average_age
    FROM
        authors a2
    WHERE a1.gender = a2.gender
);
```

TiDB 在处理该 SQL 语句是会将其改写为等价的 Join 查询：



```sql
SELECT *
FROM
    authors a1,
    (
        SELECT
            gender, AVG(
                IFNULL(a2.death_year, YEAR(NOW())) - IFNULL(a2.birth_year, YEAR(NOW()))
            ) AS average_age
        FROM
            authors a2
        GROUP BY gender
    ) a2
WHERE
    a1.gender = a2.gender
    AND (IFNULL(a1.death_year, YEAR(NOW())) - a1.birth_year) > a2.average_age;
```

作为最佳实践，在实际开发当中，建议在明确知道有更好的等价写法时，尽量避免通过关联子查询来进行查询。

### 扩展阅读

- 子查询相关的优化
- 关联子查询去关联
- [TiDB 中的子查询优化技术](https://pingcap.com/zh/blog/tidb-optimization-for-subquery)


---
title: 分页查询
summary: 介绍 TiDB 的分页查询功能。
---

## 分页查询

当查询结果数据量较大时，往往希望以“分页”的方式返回所需要的部分。

### 对查询结果进行分页

在 TiDB 当中，可以利用 `LIMIT` 语句来实现分页功能，常规的分页语句写法如下所示：



```sql
SELECT * FROM table_a t ORDER BY gmt_modified DESC LIMIT offset, row_count;
```

`offset` 表示起始记录数，`row_count` 表示每页记录数。除此之外，TiDB 也支持 `LIMIT row_count OFFSET offset` 语法。

除非明确要求不要使用任何排序来随机展示数据，使用分页查询语句时都应该通过 `ORDER BY` 语句指定查询结果的排序方式。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

例如，在 [Bookshop](#bookshop-应用) 应用当中，希望将最新书籍列表以分页的形式返回给用户。通过 `LIMIT 0, 10` 语句，便可以得到列表第 1 页的书籍信息，每页中最多有 10 条记录。获取第 2 页信息，则改成可以改成 `LIMIT 10, 10`，如此类推。



```sql
SELECT *
FROM books
ORDER BY published_at DESC
LIMIT 0, 10;
```

</div>
<div label="Java" value="java">

在使用 Java 开发应用程序时，后端程序从前端接收到的参数页码 `page_number` 和每页的数据条数 `page_size`，而不是起始记录数 `offset`，因此在进行数据库查询前需要对其进行一些转换。



```java
public List<Book> getLatestBooksPage(Long pageNumber, Long pageSize) throws SQLException {
    pageNumber = pageNumber < 1L ? 1L : pageNumber;
    pageSize = pageSize < 10L ? 10L : pageSize;
    Long offset = (pageNumber - 1) * pageSize;
    Long limit = pageSize;
    List<Book> books = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        PreparedStatement stmt = conn.prepareStatement("""
        SELECT id, title, published_at
        FROM books
        ORDER BY published_at DESC
        LIMIT ?, ?;
        """);
        stmt.setLong(1, offset);
        stmt.setLong(2, limit);
        ResultSet rs = stmt.executeQuery();
        while (rs.next()) {
            Book book = new Book();
            book.setId(rs.getLong("id"));
            book.setTitle(rs.getString("title"));
            book.setPublishedAt(rs.getDate("published_at"));
            books.add(book);
        }
    }
    return books;
}
```

</div>
</SimpleTab>

### 单字段主键表的分页批处理

常规的分页更新 SQL 一般使用主键或者唯一索引进行排序，再配合 LIMIT 语法中的 `offset`，按固定行数拆分页面。然后把页面包装进独立的事务中，从而实现灵活的分页更新。但是，劣势也很明显：由于需要对主键或者唯一索引进行排序，越靠后的页面参与排序的行数就会越多，尤其当批量处理涉及的数据体量较大时，可能会占用过多计算资源。

下面将介绍一种更为高效的分页批处理方案：

<SimpleTab groupId="language">
<div label="SQL" value="sql">

使用 SQL 实现分页批处理，可以按照如下步骤进行：

首先将数据按照主键排序，然后调用窗口函数 `row_number()` 为每一行数据生成行号，接着调用聚合函数按照设置好的页面大小对行号进行分组，最终计算出每页的最小值和最大值。



```sql
SELECT
    floor((t.row_num - 1) / 1000) + 1 AS page_num,
    min(t.id) AS start_key,
    max(t.id) AS end_key,
    count(*) AS page_size
FROM (
    SELECT id, row_number() OVER (ORDER BY id) AS row_num
    FROM books
) t
GROUP BY page_num
ORDER BY page_num;
```

查询结果如下：

```
+----------+------------+------------+-----------+
| page_num | start_key  | end_key    | page_size |
+----------+------------+------------+-----------+
|        1 |     268996 |  213168525 |      1000 |
|        2 |  213210359 |  430012226 |      1000 |
|        3 |  430137681 |  647846033 |      1000 |
|        4 |  647998334 |  848878952 |      1000 |
|        5 |  848899254 | 1040978080 |      1000 |
...
|       20 | 4077418867 | 4294004213 |      1000 |
+----------+------------+------------+-----------+
20 rows in set (0.01 sec)
```

接下来，只需要使用 `WHERE id BETWEEN start_key AND end_key` 语句查询每个分片的数据即可。修改数据时，也可以借助上面计算好的分片信息，实现高效的数据更新。

例如，假如想要删除第 1 页上的所有书籍的基本信息，可以将上表第 1 页所对应的 `start_key` 和 `end_key` 填入 SQL 语句当中。



```sql
DELETE FROM books
WHERE
    id BETWEEN 268996 AND 213168525
ORDER BY id;
```

</div>
<div label="Java" value="java">

在 Java 语言当中，可以定义一个 `PageMeta` 类来存储分页元信息。



```java
public class PageMeta<K> {
    private Long pageNum;
    private K startKey;
    private K endKey;
    private Long pageSize;

    // Skip the getters and setters.

}
```

定义一个 `getPageMetaList()` 方法获取到分页元信息列表，然后定义一个可以根据页面元信息批量删除数据的方法 `deleteBooksByPageMeta()`。



```java
public class BookDAO {
    public List<PageMeta<Long>> getPageMetaList() throws SQLException {
        List<PageMeta<Long>> pageMetaList = new ArrayList<>();
        try (Connection conn = ds.getConnection()) {
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("""
            SELECT
                floor((t.row_num - 1) / 1000) + 1 AS page_num,
                min(t.id) AS start_key,
                max(t.id) AS end_key,
                count(*) AS page_size
            FROM (
                SELECT id, row_number() OVER (ORDER BY id) AS row_num
                FROM books
            ) t
            GROUP BY page_num
            ORDER BY page_num;
            """);
            while (rs.next()) {
                PageMeta<Long> pageMeta = new PageMeta<>();
                pageMeta.setPageNum(rs.getLong("page_num"));
                pageMeta.setStartKey(rs.getLong("start_key"));
                pageMeta.setEndKey(rs.getLong("end_key"));
                pageMeta.setPageSize(rs.getLong("page_size"));
                pageMetaList.add(pageMeta);
            }
        }
        return pageMetaList;
    }

    public void deleteBooksByPageMeta(PageMeta<Long> pageMeta) throws SQLException {
        try (Connection conn = ds.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement("DELETE FROM books WHERE id >= ? AND id <= ?");
            stmt.setLong(1, pageMeta.getStartKey());
            stmt.setLong(2, pageMeta.getEndKey());
            stmt.executeUpdate();
        }
    }
}
```

如果想要删除第 1 页的数据，可以这样写：



```java
List<PageMeta<Long>> pageMetaList = bookDAO.getPageMetaList();
if (pageMetaList.size() > 0) {
    bookDAO.deleteBooksByPageMeta(pageMetaList.get(0));
}
```

如果希望通过分页分批地删除所有书籍数据，可以这样写：



```java
List<PageMeta<Long>> pageMetaList = bookDAO.getPageMetaList();
pageMetaList.forEach((pageMeta) -> {
    try {
        bookDAO.deleteBooksByPageMeta(pageMeta);
    } catch (SQLException e) {
        e.printStackTrace();
    }
});
```

</div>
</SimpleTab>

改进方案由于规避了频繁的数据排序操作造成的性能损耗，显著改善了批量处理的效率。

### 复合主键表的分页批处理

#### 非聚簇索引表

对于非聚簇索引表（又被称为“非索引组织表”）而言，可以使用隐藏字段 `_tidb_rowid` 作为分页的 key，分页的方法与单列主键表中所介绍的方法相同。

> **建议：**
>
> 你可以通过 `SHOW CREATE TABLE users;` 语句查看表主键是否使用了聚簇索引。

例如：



```sql
SELECT
    floor((t.row_num - 1) / 1000) + 1 AS page_num,
    min(t._tidb_rowid) AS start_key,
    max(t._tidb_rowid) AS end_key,
    count(*) AS page_size
FROM (
    SELECT _tidb_rowid, row_number() OVER (ORDER BY _tidb_rowid) AS row_num
    FROM users
) t
GROUP BY page_num
ORDER BY page_num;
```

查询结果如下：

```
+----------+-----------+---------+-----------+
| page_num | start_key | end_key | page_size |
+----------+-----------+---------+-----------+
|        1 |         1 |    1000 |      1000 |
|        2 |      1001 |    2000 |      1000 |
|        3 |      2001 |    3000 |      1000 |
|        4 |      3001 |    4000 |      1000 |
|        5 |      4001 |    5000 |      1000 |
|        6 |      5001 |    6000 |      1000 |
|        7 |      6001 |    7000 |      1000 |
|        8 |      7001 |    8000 |      1000 |
|        9 |      8001 |    9000 |      1000 |
|       10 |      9001 |    9990 |       990 |
+----------+-----------+---------+-----------+
10 rows in set (0.00 sec)
```

#### 聚簇索引表

对于聚簇索引表（又被称为“索引组织表”），可以利用 `concat` 函数将多个列的值连接起来作为一个 key，然后使用窗口函数获取分页信息。

需要注意的是，这时候 key 是一个字符串，你必须确保这个字符串长度总是相等的，才能够通过 `min` 和 `max` 聚合函数得到分页内正确的 `start_key` 和 `end_key`。如果进行字符串连接的字段长度不固定，你可以通过 `LPAD` 函数进行补全。

例如，想要对 `ratings` 表里的数据进行分页批处理。

先可以通过下面的 SQL 语句来在制造元信息表。因为组成 key 的 `book_id` 列和 `user_id` 列都是 `bigint` 类型，转换为字符串是并不是等宽的，因此需要根据 `bigint` 类型的最大位数 19，使用 `LPAD` 函数在长度不够时用 `0` 补齐。



```sql
SELECT
    floor((t1.row_num - 1) / 10000) + 1 AS page_num,
    min(mvalue) AS start_key,
    max(mvalue) AS end_key,
    count(*) AS page_size
FROM (
    SELECT
        concat('(', LPAD(book_id, 19, 0), ',', LPAD(user_id, 19, 0), ')') AS mvalue,
        row_number() OVER (ORDER BY book_id, user_id) AS row_num
    FROM ratings
) t1
GROUP BY page_num
ORDER BY page_num;
```

查询结果如下：

```
+----------+-------------------------------------------+-------------------------------------------+-----------+
| page_num | start_key                                 | end_key                                   | page_size |
+----------+-------------------------------------------+-------------------------------------------+-----------+
|        1 | (0000000000000268996,0000000000092104804) | (0000000000140982742,0000000000374645100) |     10000 |
|        2 | (0000000000140982742,0000000000456757551) | (0000000000287195082,0000000004053200550) |     10000 |
|        3 | (0000000000287196791,0000000000191962769) | (0000000000434010216,0000000000237646714) |     10000 |
|        4 | (0000000000434010216,0000000000375066168) | (0000000000578893327,0000000002167504460) |     10000 |
|        5 | (0000000000578893327,0000000002457322286) | (0000000000718287668,0000000001502744628) |     10000 |
...
|       29 | (0000000004002523918,0000000000902930986) | (0000000004147203315,0000000004090920746) |     10000 |
|       30 | (0000000004147421329,0000000000319181561) | (0000000004294004213,0000000003586311166) |      9972 |
+----------+-------------------------------------------+-------------------------------------------+-----------+
30 rows in set (0.28 sec)
```

假如想要删除第 1 页上的所有评分记录，可以将上表第 1 页所对应的 `start_key` 和 `end_key` 填入 SQL 语句当中。



```sql
SELECT * FROM ratings
WHERE
    (book_id, user_id) >= (268996, 92104804)
    AND (book_id, user_id) <= (140982742, 374645100)
ORDER BY book_id, user_id;
```


---
title: 视图
summary: 介绍 TiDB 中的视图功能。
---

## 视图

本章将介绍 TiDB 中的视图功能。

### 概述

TiDB 支持视图，视图是一张虚拟表，该虚拟表的结构由创建视图时的 `SELECT` 语句定义。

- 通过视图可以对用户只暴露安全的字段及数据，进而保证底层表的敏感字段及数据的安全。
- 将频繁出现的复杂查询定义为视图，可以使复杂查询更加简单便捷。

### 创建视图

在 TiDB 当中，可以通过 `CREATE VIEW` 语句来将某个较为复杂的查询定义为视图，其语法如下：



```sql
CREATE VIEW view_name AS query;
```

请注意，创建的视图名称不能与已有的视图或表重名。

例如，在[多表连接查询](#多表连接查询) 章节当中，通过 `JOIN` 语句连接 `books` 表和 `ratings` 表查询到了带有平均评分的书籍列表。为了方便后续查询，可以将该查询语句定义为一个视图，SQL 语句如下所示：



```sql
CREATE VIEW book_with_ratings AS
SELECT b.id AS book_id, ANY_VALUE(b.title) AS book_title, AVG(r.score) AS average_score
FROM books b
LEFT JOIN ratings r ON b.id = r.book_id
GROUP BY b.id;
```

### 查询视图

视图创建完成后，便可以使用 `SELECT` 语句像查询一般数据表一样查询视图。



```sql
SELECT * FROM book_with_ratings LIMIT 10;
```

TiDB 在执行查询视图语句时，会将视图展开成创建视图时定义的 `SELECT` 语句，进而执行展开后的查询语句。

### 更新视图

目前 TiDB 中的视图不支持 `ALTER VIEW view_name AS query;` 语法，你可以通过以下两种方式实现视图的 “更新”：

- 先 `DROP VIEW view_name;` 语句删除旧视图，再通过 `CREATE VIEW view_name AS query;` 语句创建新视图的方式来更新视图。
- 使用 `CREATE OR REPLACE VIEW view_name AS query;` 语句覆盖已存在的同名视图。



```sql
CREATE OR REPLACE VIEW book_with_ratings AS
SELECT b.id AS book_id, ANY_VALUE(b.title), ANY_VALUE(b.published_at) AS book_title, AVG(r.score) AS average_score
FROM books b
LEFT JOIN ratings r ON b.id = r.book_id
GROUP BY b.id;
```

### 获取视图相关信息

#### 使用 `SHOW CREATE TABLE|VIEW view_name` 语句



```sql
SHOW CREATE VIEW book_with_ratings\G
```

运行结果为：

```
*************************** 1. row ***************************
                View: book_with_ratings
         Create View: CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `book_with_ratings` (`book_id`, `ANY_VALUE(b.title)`, `book_title`, `average_score`) AS SELECT `b`.`id` AS `book_id`,ANY_VALUE(`b`.`title`) AS `ANY_VALUE(b.title)`,ANY_VALUE(`b`.`published_at`) AS `book_title`,AVG(`r`.`score`) AS `average_score` FROM `bookshop`.`books` AS `b` LEFT JOIN `bookshop`.`ratings` AS `r` ON `b`.`id`=`r`.`book_id` GROUP BY `b`.`id`
character_set_client: utf8mb4
collation_connection: utf8mb4_general_ci
1 row in set (0.00 sec)
```

#### 查询 `INFORMATION_SCHEMA.VIEWS` 表



```sql
SELECT * FROM information_schema.views WHERE TABLE_NAME = 'book_with_ratings'\G
```

运行结果为：

```
*************************** 1. row ***************************
       TABLE_CATALOG: def
        TABLE_SCHEMA: bookshop
          TABLE_NAME: book_with_ratings
     VIEW_DEFINITION: SELECT `b`.`id` AS `book_id`,ANY_VALUE(`b`.`title`) AS `ANY_VALUE(b.title)`,ANY_VALUE(`b`.`published_at`) AS `book_title`,AVG(`r`.`score`) AS `average_score` FROM `bookshop`.`books` AS `b` LEFT JOIN `bookshop`.`ratings` AS `r` ON `b`.`id`=`r`.`book_id` GROUP BY `b`.`id`
        CHECK_OPTION: CASCADED
        IS_UPDATABLE: NO
             DEFINER: root@%
       SECURITY_TYPE: DEFINER
CHARACTER_SET_CLIENT: utf8mb4
COLLATION_CONNECTION: utf8mb4_general_ci
1 row in set (0.00 sec)
```

### 删除视图

通过 `DROP VIEW view_name;` 语句可以删除已经创建的视图。



```sql
DROP VIEW book_with_ratings;
```

### 局限性

关于局限性，你可以通过阅读参考文档当中的视图章节进行了解。

### 扩展阅读

- 视图
- CREATE VIEW 语句
- DROP VIEW 语句
- 用 EXPLAIN 查看带视图的 SQL 执行计划
- [TiFlink: 使用 TiKV 和 Flink 实现强一致的物化视图](https://github.com/tiflink/tiflink)


---
title: 临时表
summary: 介绍 TiDB 临时表创建、删除、限制。
---

## 临时表

临时表可以被认为是一种复用查询结果的技术。

假设希望知道 [Bookshop](#bookshop-应用) 应用当中最年长的作家们的一些情况，可能需要编写多个查询，而这些查询都需要使用到这个最年长作家列表。可以通过下面的 SQL 语句从 `authors` 表当中找出最年长的前 50 位作家作为研究对象。



```sql
SELECT a.id, a.name, (IFNULL(a.death_year, YEAR(NOW())) - a.birth_year) AS age
FROM authors a
ORDER BY age DESC
LIMIT 50;
```

查询结果如下：

```
+------------+---------------------+------+
| id         | name                | age  |
+------------+---------------------+------+
| 4053452056 | Dessie Thompson     |   80 |
| 2773958689 | Pedro Hansen        |   80 |
| 4005636688 | Wyatt Keeling       |   80 |
| 3621155838 | Colby Parker        |   80 |
| 2738876051 | Friedrich Hagenes   |   80 |
| 2299112019 | Ray Macejkovic      |   80 |
| 3953661843 | Brandi Williamson   |   80 |
...
| 4100546410 | Maida Walsh         |   80 |
+------------+---------------------+------+
50 rows in set (0.01 sec)
```

在找到这 50 位最年长的作家后，希望缓存这个查询结果，以便后续的查询能够方便地使用到这组数据。如果使用一般的数据库表进行存储的话，在创建这些表时，需要考虑如何避免不同会话之间的表重名问题，而且可能在一批查询结束之后就不再需要这些表了，还需要及时地对这些中间结果表进行清理。

### 创建临时表

为了满足这类缓存中间结果的需求，TiDB 在 v5.3.0 版本中引入了临时表功能，对于临时表当中的本地临时表而言，TiDB 将会在会话结束的一段时间后自动清理这些已经没用的临时表，用户无需担心中间结果表的增多会带来管理上的麻烦。

#### 临时表类型

TiDB 的临时表分为本地临时表和全局临时表：

- 本地临时表的表定义和表内数据只对当前会话可见，适用于暂存会话内的中间数据。
- 全局临时表的表定义对整个 TiDB 集群可见，表内数据只对当前事务可见，适用于暂存事务内的中间数据。

#### 创建本地临时表

在创建本地临时表前，你需要给当前数据库用户添加上 `CREATE TEMPORARY TABLES` 权限。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在 SQL 中，通过 `CREATE TEMPORARY TABLE <table_name>` 语句创建临时表，默认临时表的类型为本地临时表，它只能被当前会话所访问。



```sql
CREATE TEMPORARY TABLE top_50_eldest_authors (
    id BIGINT,
    name VARCHAR(255),
    age INT,
    PRIMARY KEY(id)
);
```

在创建完临时表后，你可以通过 `INSERT INTO table_name SELECT ...` 语句，将上述查询得到的结果导入到刚刚创建的临时表当中。



```sql
INSERT INTO top_50_eldest_authors
SELECT a.id, a.name, (IFNULL(a.death_year, YEAR(NOW())) - a.birth_year) AS age
FROM authors a
ORDER BY age DESC
LIMIT 50;
```

运行结果为：

```
Query OK, 50 rows affected (0.03 sec)
Records: 50  Duplicates: 0  Warnings: 0
```

</div>
<div label="Java" value="java">

在 Java 中创建本地临时表的示例如下：

```java
public List<Author> getTop50EldestAuthorInfo() throws SQLException {
    List<Author> authors = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        Statement stmt = conn.createStatement();
        stmt.executeUpdate("""
            CREATE TEMPORARY TABLE top_50_eldest_authors (
                id BIGINT,
                name VARCHAR(255),
                age INT,
                PRIMARY KEY(id)
            );
        """);

        stmt.executeUpdate("""
            INSERT INTO top_50_eldest_authors
            SELECT a.id, a.name, (IFNULL(a.death_year, YEAR(NOW())) - a.birth_year) AS age
            FROM authors a
            ORDER BY age DESC
            LIMIT 50;
        """);

        ResultSet rs = stmt.executeQuery("""
            SELECT id, name FROM top_50_eldest_authors;
        """);

        while (rs.next()) {
            Author author = new Author();
            author.setId(rs.getLong("id"));
            author.setName(rs.getString("name"));
            authors.add(author);
        }
    }
    return authors;
}
```

</div>
</SimpleTab>

#### 创建全局临时表

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在 SQL 中，你可以通过加上 `GLOBAL` 关键字来声明你所创建的是全局临时表。创建全局临时表时必须在末尾 `ON COMMIT DELETE ROWS` 修饰，这表明该全局数据表的所有数据行将在事务结束后被删除。



```sql
CREATE GLOBAL TEMPORARY TABLE IF NOT EXISTS top_50_eldest_authors_global (
    id BIGINT,
    name VARCHAR(255),
    age INT,
    PRIMARY KEY(id)
) ON COMMIT DELETE ROWS;
```

在对全局临时表导入数据时，你需要特别注意，你必须通过 `BEGIN` 显式声明事务的开始。否则导入的数据在 `INSERT INTO` 语句执行后就清除掉，因为 Auto Commit 模式下，`INSERT INTO` 语句的执行结束，事务会自动被提交，事务结束，全局临时表的数据便被清空了。

</div>
<div label="Java" value="java">

在 Java 中使用全局临时表时，你需要将 Auto Commit 模式先关闭。在 Java 语言当中，你可以通过 `conn.setAutoCommit(false);` 语句来实现，当你使用完成后，可以通过 `conn.commit();` 显式地提交事务。事务在提交或取消后，在事务过程中对全局临时表添加的数据将会被清除。



```java
public List<Author> getTop50EldestAuthorInfo() throws SQLException {
    List<Author> authors = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        conn.setAutoCommit(false);

        Statement stmt = conn.createStatement();
        stmt.executeUpdate("""
            CREATE GLOBAL TEMPORARY TABLE IF NOT EXISTS top_50_eldest_authors (
                id BIGINT,
                name VARCHAR(255),
                age INT,
                PRIMARY KEY(id)
            ) ON COMMIT DELETE ROWS;
        """);

        stmt.executeUpdate("""
            INSERT INTO top_50_eldest_authors
            SELECT a.id, a.name, (IFNULL(a.death_year, YEAR(NOW())) - a.birth_year) AS age
            FROM authors a
            ORDER BY age DESC
            LIMIT 50;
        """);

        ResultSet rs = stmt.executeQuery("""
            SELECT id, name FROM top_50_eldest_authors;
        """);

        conn.commit();
        while (rs.next()) {
            Author author = new Author();
            author.setId(rs.getLong("id"));
            author.setName(rs.getString("name"));
            authors.add(author);
        }
    }
    return authors;
}
```

</div>
</SimpleTab>

### 查看临时表信息

通过 `SHOW [FULL] TABLES` 语句可以查看到已经创建的全局临时表，但是无法看到本地临时表的信息，TiDB 暂时也没有类似的 `information_schema.INNODB_TEMP_TABLE_INFO` 系统表存放临时表的信息。

例如，你可以在 table 列表当中查看到全局临时表 `top_50_eldest_authors_global`，但是无法查看到 `top_50_eldest_authors` 表。

```
+-------------------------------+------------+
| Tables_in_bookshop            | Table_type |
+-------------------------------+------------+
| authors                       | BASE TABLE |
| book_authors                  | BASE TABLE |
| books                         | BASE TABLE |
| orders                        | BASE TABLE |
| ratings                       | BASE TABLE |
| top_50_eldest_authors_global  | BASE TABLE |
| users                         | BASE TABLE |
+-------------------------------+------------+
9 rows in set (0.00 sec)
```

### 查询临时表

在临时表准备就绪之后，你便可以像对一般数据表一样对临时表进行查询：



```sql
SELECT * FROM top_50_eldest_authors;
```

你可以通过[表连接](#多表连接查询)将临时表中的数据引用到你的查询当中：



```sql
EXPLAIN SELECT ANY_VALUE(ta.id) AS author_id, ANY_VALUE(ta.age), ANY_VALUE(ta.name), COUNT(*) AS books
FROM top_50_eldest_authors ta
LEFT JOIN book_authors ba ON ta.id = ba.author_id
GROUP BY ta.id;
```

与[视图](#视图)有所不同，在对临时表进行查询时，不会再执行导入数据时所使用的原始查询，而是直接从临时表中获取数据。在一些情况下，这会帮助你提高查询的效率。

### 删除临时表

本地临时表会在**会话**结束后连同数据和表结构都进行自动清理。全局临时表在**事务**结束后会自动清除数据，但是表结构依然保留，需要手动删除。

你可以通过 `DROP TABLE` 或 `DROP TEMPORARY TABLE` 语句手动删除**本地临时表**。例如：



```sql
DROP TEMPORARY TABLE top_50_eldest_authors;
```

你还可以通过 `DROP TABLE` 或 `DROP GLOBAL TEMPORARY TABLE` 语句手动删除**全局临时表**。例如：



```sql
DROP GLOBAL TEMPORARY TABLE top_50_eldest_authors_global;
```

### 限制

关于 TiDB 在临时表功能上的一些限制，你可以通过阅读参考文档中的临时表与其他 TiDB 功能的兼容性限制小节进行了解。

### 扩展阅读

- 临时表

---
title: 公共表表达式 (CTE)
summary: 介绍 TiDB 公共表表达式能力，用以简化 SQL。
---

## 公共表表达式 (CTE)

由于业务的客观复杂性，有时候会写出长达 2000 行的单条 SQL 语句，其中包含大量的聚合和多层子查询嵌套，维护此类 SQL 堪称开发人员的噩梦。

在前面的小节当中已经介绍了如何使用[视图](#视图)简化查询，也介绍了如何使用[临时表](#临时表)来缓存中间查询结果。

在这一小节当中，将介绍 TiDB 当中的公共表表达式（CTE）语法，它是一种更加便捷的复用查询结果的方法。

TiDB 从 5.1 版本开始支持 ANSI SQL 99 标准的 CTE 及其递归的写法，极大提升开发人员和 DBA 编写复杂业务逻辑 SQL 的效率，增强代码的可维护性。

### 基本使用

公共表表达式 (CTE) 是一个临时的中间结果集，能够在 SQL 语句中引用多次，提高 SQL 语句的可读性与执行效率。在 TiDB 中可以通过 `WITH` 语句使用公共表表达式。

公共表表达式可以分为非递归和递归两种类型。

#### 非递归的 CTE

非递归的 CTE 使用如下语法进行定义：



```sql
WITH <query_name> AS (
    <query_definition>
)
SELECT ... FROM <query_name>;
```

例如，假设还想知道最年长的 50 位作家分别编写过多少书籍。

<SimpleTab>
<div label="SQL">

在 SQL 中，可以将[临时表](#临时表)小节当中的例子改为以下 SQL 语句：



```sql
WITH top_50_eldest_authors_cte AS (
    SELECT a.id, a.name, (IFNULL(a.death_year, YEAR(NOW())) - a.birth_year) AS age
    FROM authors a
    ORDER BY age DESC
    LIMIT 50
)
SELECT
    ANY_VALUE(ta.id) AS author_id,
    ANY_VALUE(ta.age) AS author_age,
    ANY_VALUE(ta.name) AS author_name,
    COUNT(*) AS books
FROM top_50_eldest_authors_cte ta
LEFT JOIN book_authors ba ON ta.id = ba.author_id
GROUP BY ta.id;
```

查询结果如下：

```
+------------+------------+---------------------+-------+
| author_id  | author_age | author_name         | books |
+------------+------------+---------------------+-------+
| 1238393239 |         80 | Araceli Purdy       |     1 |
|  817764631 |         80 | Ivory Davis         |     3 |
| 3093759193 |         80 | Lysanne Harris      |     1 |
| 2299112019 |         80 | Ray Macejkovic      |     4 |
...
+------------+------------+---------------------+-------+
50 rows in set (0.01 sec)
```

</div>
<div label="Java">

在 Java 中的示例如下：

```java
public List<Author> getTop50EldestAuthorInfoByCTE() throws SQLException {
    List<Author> authors = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery("""
            WITH top_50_eldest_authors_cte AS (
                SELECT a.id, a.name, (IFNULL(a.death_year, YEAR(NOW())) - a.birth_year) AS age
                FROM authors a
                ORDER BY age DESC
                LIMIT 50
            )
            SELECT
                ANY_VALUE(ta.id) AS author_id,
                ANY_VALUE(ta.name) AS author_name,
                ANY_VALUE(ta.age) AS author_age,
                COUNT(*) AS books
            FROM top_50_eldest_authors_cte ta
            LEFT JOIN book_authors ba ON ta.id = ba.author_id
            GROUP BY ta.id;
        """);
        while (rs.next()) {
            Author author = new Author();
            author.setId(rs.getLong("author_id"));
            author.setName(rs.getString("author_name"));
            author.setAge(rs.getShort("author_age"));
            author.setBooks(rs.getInt("books"));
            authors.add(author);
        }
    }
    return authors;
}
```

</div>
</SimpleTab>

这时，可以发现名为 “Ray Macejkovic” 的作者写了 4 本书，继续通过 CTE 查询来了解这 4 本书的销量和评分：



```sql
WITH books_authored_by_rm AS (
    SELECT *
    FROM books b
    LEFT JOIN book_authors ba ON b.id = ba.book_id
    WHERE author_id = 2299112019
), books_with_average_ratings AS (
    SELECT
        b.id AS book_id,
        AVG(r.score) AS average_rating
    FROM books_authored_by_rm b
    LEFT JOIN ratings r ON b.id = r.book_id
    GROUP BY b.id
), books_with_orders AS (
    SELECT
        b.id AS book_id,
        COUNT(*) AS orders
    FROM books_authored_by_rm b
    LEFT JOIN orders o ON b.id = o.book_id
    GROUP BY b.id
)
SELECT
    b.id AS `book_id`,
    b.title AS `book_title`,
    br.average_rating AS `average_rating`,
    bo.orders AS `orders`
FROM
    books_authored_by_rm b
    LEFT JOIN books_with_average_ratings br ON b.id = br.book_id
    LEFT JOIN books_with_orders bo ON b.id = bo.book_id
;
```

查询结果如下：

```
+------------+-------------------------+----------------+--------+
| book_id    | book_title              | average_rating | orders |
+------------+-------------------------+----------------+--------+
|  481008467 | The Documentary of goat |         2.0000 |     16 |
| 2224531102 | Brandt Skiles           |         2.7143 |     17 |
| 2641301356 | Sheridan Bashirian      |         2.4211 |     12 |
| 4154439164 | Karson Streich          |         2.5833 |     19 |
+------------+-------------------------+----------------+--------+
4 rows in set (0.06 sec)
```

在这个 SQL 语句，定义了三个 CTE 块，CTE 块之间使用 `,` 进行分隔。

先在 CTE 块 `books_authored_by_rm` 当中将该作者（作者 ID 为 `2299112019`）所编写的书查出来，然后在 `books_with_average_ratings` 和 `books_with_orders` 中分别查出这些书的平均评分和订单数，最后通过 `JOIN` 语句进行汇总。

值得注意的是，`books_authored_by_rm` 中的查询只会执行一次，TiDB 会开辟一块临时空间对查询的结果进行缓存，当 `books_with_average_ratings` 和 `books_with_orders` 引用时会直接从该临时空间当中获取数据。

> **建议：**
>
> 当默认的 CTE 查询执行效率不高时，你可以使用 [`MERGE()`](#merge) hint，将 CTE 子查询拓展到外部查询，以此提高执行效率。

#### 递归的 CTE

递归的公共表表达式可以使用如下语法进行定义：



```sql
WITH RECURSIVE <query_name> AS (
    <query_definition>
)
SELECT ... FROM <query_name>;
```

比较经典的例子是通过递归的 CTE 生成一组[斐波那契数](https://zh.wikipedia.org/wiki/%E6%96%90%E6%B3%A2%E9%82%A3%E5%A5%91%E6%95%B0)：



```sql
WITH RECURSIVE fibonacci (n, fib_n, next_fib_n) AS
(
  SELECT 1, 0, 1
  UNION ALL
  SELECT n + 1, next_fib_n, fib_n + next_fib_n FROM fibonacci WHERE n < 10
)
SELECT * FROM fibonacci;
```

查询结果如下：

```
+------+-------+------------+
| n    | fib_n | next_fib_n |
+------+-------+------------+
|    1 |     0 |          1 |
|    2 |     1 |          1 |
|    3 |     1 |          2 |
|    4 |     2 |          3 |
|    5 |     3 |          5 |
|    6 |     5 |          8 |
|    7 |     8 |         13 |
|    8 |    13 |         21 |
|    9 |    21 |         34 |
|   10 |    34 |         55 |
+------+-------+------------+
10 rows in set (0.00 sec)
```

### 扩展阅读

- WITH



## 读取副本数据

---
title: Follower Read
summary: 使用 Follower Read 在特定情况下加速查询。
---

### Follower Read

本章将介绍使用 Follower Read 在特定情况下加速查询的方法。

#### 简介

在 TiDB 当中，数据是以 Region 为单位，分散在集群中所有的节点上进行存储的。一个 Region 可以存在多个副本，副本又分为一个 leader 和多个 follower。当 leader 上的数据发生变化时，TiDB 会将数据同步更新到 follower。

默认情况下，TiDB 只会在同一个 Region 的 leader 上读写数据。当系统中存在读取热点 Region 导致 leader 资源紧张成为整个系统读取瓶颈时，启用 Follower Read 功能可明显降低 leader 的负担，并且通过在多个 follower 之间均衡负载，显著地提升整体系统的吞吐能力。

#### 何时使用

##### 优化读热点

你可以在 TiDB Dashboard 流量可视化页面当中通过可视化的方法分析你的应用程序是否存在热点 Region。你可以通过将「指标选择框」选择到 `Read (bytes)` 或 `Read (keys)` 查看是否存在读取热点 Region。

如果发现确实存在热点问题，你可以通过阅读 TiDB 热点问题处理章节进行逐一排查，以便从应用程序层面上避免热点的产生。

如果读取热点的确无法避免或者改动的成本很大，你可以尝试通过 Follower Read 功能将读取请求更好的负载均衡到 follower region。

##### 优化跨数据中心部署的延迟

如果 TiDB 集群是跨地区或跨数据中心部署的，一个 Region 的不同副本分布在不同的地区或数据中心，此时可以通过配置 Follower Read 为 `closest-adaptive` 或 `closest-replicas` 让 TiDB 优先从当前的数据中心执行读操作，这样可以大幅降低读操作的延迟和流量开销。具体原理可参考 Follower Read。

#### 开启 Follower Read

<SimpleTab>
<div label="SQL">

在 SQL 中，你可以将变量 `tidb_replica_read` 的值（默认为 `leader`）设置为 `follower`、 `leader-and-follower`、 `closest-replicas` 或 `closest-adaptive` 开启 TiDB 的 Follower Read 功能：



```sql
SET [GLOBAL] tidb_replica_read = 'follower';
```

你可以通过 Follower Read 使用方式 了解该变量的更多细节。

</div>
<div label="Java">

在 Java 语言当中，可以定义一个 `FollowerReadHelper` 类用于开启 Follower Read 功能：



```java
public enum FollowReadMode {
    LEADER("leader"),
    FOLLOWER("follower"),
    LEADER_AND_FOLLOWER("leader-and-follower"),
    CLOSEST_REPLICA("closest-replica"),
    CLOSEST_ADAPTIVE("closest-adaptive");

    private final String mode;

    FollowReadMode(String mode) {
        this.mode = mode;
    }

    public String getMode() {
        return mode;
    }
}

public class FollowerReadHelper {

    public static void setSessionReplicaRead(Connection conn, FollowReadMode mode) throws SQLException {
        if (mode == null) mode = FollowReadMode.LEADER;
        PreparedStatement stmt = conn.prepareStatement(
            "SET @@tidb_replica_read = ?;"
        );
        stmt.setString(1, mode.getMode());
        stmt.execute();
    }

    public static void setGlobalReplicaRead(Connection conn, FollowReadMode mode) throws SQLException {
        if (mode == null) mode = FollowReadMode.LEADER;
        PreparedStatement stmt = conn.prepareStatement(
            "SET GLOBAL @@tidb_replica_read = ?;"
        );
        stmt.setString(1, mode.getMode());
        stmt.execute();
    }

}
```

在需要使用从 Follower 节点读取数据时，通过 `setSessionReplicaRead(conn, FollowReadMode.LEADER_AND_FOLLOWER)` 方法在当前 Session 开启能够在 Leader 节点和 Follower 节点进行负载均衡的 Follower Read 功能，当连接断开时，会恢复到原来的模式。



```java
public static class AuthorDAO {

    // Omit initialization of instance variables...

    public void getAuthorsByFollowerRead() throws SQLException {
        try (Connection conn = ds.getConnection()) {
            // Enable the follower read feature.
            FollowerReadHelper.setSessionReplicaRead(conn, FollowReadMode.LEADER_AND_FOLLOWER);

            // Read the authors list for 100000 times.
            Random random = new Random();
            for (int i = 0; i < 100000; i++) {
                Integer birthYear = 1920 + random.nextInt(100);
                List<Author> authors = this.getAuthorsByBirthYear(birthYear);
                System.out.println(authors.size());
            }
        }
    }

    public List<Author> getAuthorsByBirthYear(Integer birthYear) throws SQLException {
        List<Author> authors = new ArrayList<>();
        try (Connection conn = ds.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement("SELECT id, name FROM authors WHERE birth_year = ?");
            stmt.setInt(1, birthYear);
            ResultSet rs = stmt.executeQuery();
            while (rs.next()) {
                Author author = new Author();
                author.setId( rs.getLong("id"));
                author.setName(rs.getString("name"));
                authors.add(author);
            }
        }
        return authors;
    }
}
```

</div>
</SimpleTab>

#### 扩展阅读

- Follower Read
- TiDB 热点问题处理
- TiDB Dashboard 流量可视化页面


---
title: Stale Read
summary: 使用 Stale Read 在特定情况下加速查询。
---

### Stale Read

Stale Read 是一种读取历史数据版本的机制，通过 Stale Read 功能，你能从指定时间点或时间范围内读取对应的历史数据，从而在数据强一致需求没那么高的场景降低读取数据的延迟。当使用 Stale Read 时，TiDB 默认会随机选择一个副本来读取数据，因此能利用所有保存有副本的节点的处理能力。

在实际的使用当中，请根据具体的场景判断是否适合在 TiDB 当中开启 Stale Read 功能。如果你的应用程序不能容忍读到非实时的数据，请勿使用 Stale Read，否则读到的数据可能不是最新成功写入的数据。

TiDB 提供了语句级别、事务级别、会话级别三种级别的 Stale Read 功能，接下来将逐一进行介绍：

#### 引入

在 [Bookshop](#bookshop-应用) 应用程序当中，你可以通过下面的 SQL 语句查询出最新出版的书籍以及它们的价格：



```sql
SELECT id, title, type, price FROM books ORDER BY published_at DESC LIMIT 5;
```

运行结果为：

```
+------------+------------------------------+-----------------------+--------+
| id         | title                        | type                  | price  |
+------------+------------------------------+-----------------------+--------+
| 3181093216 | The Story of Droolius Caesar | Novel                 | 100.00 |
| 1064253862 | Collin Rolfson               | Education & Reference |  92.85 |
| 1748583991 | The Documentary of cat       | Magazine              | 159.75 |
|  893930596 | Myrl Hills                   | Education & Reference | 356.85 |
| 3062833277 | Keven Wyman                  | Life                  | 477.91 |
+------------+------------------------------+-----------------------+--------+
5 rows in set (0.02 sec)
```

看到此时（2022-04-20 15:20:00）的列表中，**The Story of Droolius Caesar** 这本小说的价格为 100.0 元。

于此同时，卖家发现这本书很受欢迎，于是他通过下面的 SQL 语句将这本书的价格高到了 150.0 元。



```sql
UPDATE books SET price = 150 WHERE id = 3181093216;
```

运行结果为：

```
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0
```

当再次查询最新书籍列表时，发现这本书确实涨价了。

```
+------------+------------------------------+-----------------------+--------+
| id         | title                        | type                  | price  |
+------------+------------------------------+-----------------------+--------+
| 3181093216 | The Story of Droolius Caesar | Novel                 | 150.00 |
| 1064253862 | Collin Rolfson               | Education & Reference |  92.85 |
| 1748583991 | The Documentary of cat       | Magazine              | 159.75 |
|  893930596 | Myrl Hills                   | Education & Reference | 356.85 |
| 3062833277 | Keven Wyman                  | Life                  | 477.91 |
+------------+------------------------------+-----------------------+--------+
5 rows in set (0.01 sec)
```

如果不要求必须使用最新的数据，可以让 TiDB 通过 Stale Read 功能直接返回可能已经过期的历史数据，避免使用强一致性读时数据同步带来的延迟。

假设在 Bookshop 应用程序当中，在用户浏览书籍列表页时，不对书籍价格的实时性进行要求，只有用户在点击查看书籍详情页或下单时才去获取实时的价格信息，可以借助 Stale Read 能力来进一步提升应用的吞吐量。

#### 语句级别

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在 SQL 中，你可以在上述价格的查询语句当中添加上 `AS OF TIMESTAMP <datetime>` 语句查看到固定时间点之前这本书的价格。



```sql
SELECT id, title, type, price FROM books AS OF TIMESTAMP '2022-04-20 15:20:00' ORDER BY published_at DESC LIMIT 5;
```

运行结果为：

```
+------------+------------------------------+-----------------------+--------+
| id         | title                        | type                  | price  |
+------------+------------------------------+-----------------------+--------+
| 3181093216 | The Story of Droolius Caesar | Novel                 | 100.00 |
| 1064253862 | Collin Rolfson               | Education & Reference |  92.85 |
| 1748583991 | The Documentary of cat       | Magazine              | 159.75 |
|  893930596 | Myrl Hills                   | Education & Reference | 356.85 |
| 3062833277 | Keven Wyman                  | Life                  | 477.91 |
+------------+------------------------------+-----------------------+--------+
5 rows in set (0.01 sec)
```

除了指定精确的时间点外，你还可以通过：

- `AS OF TIMESTAMP NOW() - INTERVAL 10 SECOND` 表示读取 10 秒前最新的数据。
- `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS('2016-10-08 16:45:26', '2016-10-08 16:45:29')` 表示读取在 2016 年 10 月 8 日 16 点 45 分 26 秒到 29 秒的时间范围内尽可能新的数据。
- `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS(NOW() - INTERVAL 20 SECOND, NOW())` 表示读取 20 秒前到现在的时间范围内尽可能新的数据。

需要注意的是，设定的时间戳或时间戳的范围不能过早或晚于当前时间。

过期的数据在 TiDB 当中会由垃圾回收器进行回收，数据在被清除之前会被保留一小段时间，这段时间被称为 [GC Life Time (默认 10 分钟)](#tidb_gc_life_time-从-v50-版本开始引入)。每次进行 GC 时，将以当前时间减去该时间周期的值作为 **GC Safe Point**。如果尝试读取 GC Safe Point 之前数据，TiDB 会报如下错误：

```
ERROR 9006 (HY000): GC life time is shorter than transaction duration...
```

如果给出的时间戳是一个未来的时间节点，TiDB 会报如下错误：

```
ERROR 9006 (HY000): cannot set read timestamp to a future time.
```

</div>
<div label="Java" value="java">

在 Java 中的示例如下：

```java
public class BookDAO {

    // Omit some code...

    public List<Book> getTop5LatestBooks() throws SQLException {
        List<Book> books = new ArrayList<>();
        try (Connection conn = ds.getConnection()) {
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("""
            SELECT id, title, type, price FROM books ORDER BY published_at DESC LIMIT 5;
            """);
            while (rs.next()) {
                Book book = new Book();
                book.setId(rs.getLong("id"));
                book.setTitle(rs.getString("title"));
                book.setType(rs.getString("type"));
                book.setPrice(rs.getDouble("price"));
                books.add(book);
            }
        }
        return books;
    }

    public void updateBookPriceByID(Long id, Double price) throws SQLException {
        try (Connection conn = ds.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement("""
            UPDATE books SET price = ? WHERE id = ?;
            """);
            stmt.setDouble(1, price);
            stmt.setLong(2, id);
            int affects = stmt.executeUpdate();
            if (affects == 0) {
                throw new SQLException("Failed to update the book with id: " + id);
            }
        }
    }

    public List<Book> getTop5LatestBooksWithStaleRead(Integer seconds) throws SQLException {
        List<Book> books = new ArrayList<>();
        try (Connection conn = ds.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement("""
            SELECT id, title, type, price FROM books AS OF TIMESTAMP NOW() - INTERVAL ? SECOND ORDER BY published_at DESC LIMIT 5;
            """);
            stmt.setInt(1, seconds);
            ResultSet rs = stmt.executeQuery();
            while (rs.next()) {
                Book book = new Book();
                book.setId(rs.getLong("id"));
                book.setTitle(rs.getString("title"));
                book.setType(rs.getString("type"));
                book.setPrice(rs.getDouble("price"));
                books.add(book);
            }
        } catch (SQLException e) {
            if ("HY000".equals(e.getSQLState()) && e.getErrorCode() == 1105) {
                System.out.println("WARN: cannot set read timestamp to a future time.");
            } else if ("HY000".equals(e.getSQLState()) && e.getErrorCode() == 9006) {
                System.out.println("WARN: GC life time is shorter than transaction duration.");
            } else {
                throw e;
            }
        }
        return books;
    }
}
```



```java
List<Book> top5LatestBooks = bookDAO.getTop5LatestBooks();

if (top5LatestBooks.size() > 0) {
    System.out.println("The latest book price (before update): " + top5LatestBooks.get(0).getPrice());

    Book book = top5LatestBooks.get(0);
    bookDAO.updateBookPriceByID(book.getId(), book.price + 10);

    top5LatestBooks = bookDAO.getTop5LatestBooks();
    System.out.println("The latest book price (after update): " + top5LatestBooks.get(0).getPrice());

    // Use the stale read.
    top5LatestBooks = bookDAO.getTop5LatestBooksWithStaleRead(5);
    System.out.println("The latest book price (maybe stale): " + top5LatestBooks.get(0).getPrice());

    // Try to stale read the data at the future time.
    bookDAO.getTop5LatestBooksWithStaleRead(-5);

    // Try to stale read the data before 20 minutes.
    bookDAO.getTop5LatestBooksWithStaleRead(20 * 60);
}
```

通过结果可以看到通过 Stale Read 读取到了更新之前的价格 100.00 元。

```
The latest book price (before update): 100.00
The latest book price (after update): 150.00
The latest book price (maybe stale): 100.00
WARN: cannot set read timestamp to a future time.
WARN: GC life time is shorter than transaction duration.
```

</div>
</SimpleTab>

#### 事务级别

通过 `START TRANSACTION READ ONLY AS OF TIMESTAMP` 语句，你可以开启一个基于历史时间的只读事务，该事务基于所提供的历史时间来读取历史数据。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在 SQL 中的示例如下：



```sql
START TRANSACTION READ ONLY AS OF TIMESTAMP NOW() - INTERVAL 5 SECOND;
```

尝试通过 SQL 查询最新书籍的价格，发现 **The Story of Droolius Caesar** 这本书的价格还是更新之前的价格 100.0 元。



```sql
SELECT id, title, type, price FROM books ORDER BY published_at DESC LIMIT 5;
```

运行结果为：

```
+------------+------------------------------+-----------------------+--------+
| id         | title                        | type                  | price  |
+------------+------------------------------+-----------------------+--------+
| 3181093216 | The Story of Droolius Caesar | Novel                 | 100.00 |
| 1064253862 | Collin Rolfson               | Education & Reference |  92.85 |
| 1748583991 | The Documentary of cat       | Magazine              | 159.75 |
|  893930596 | Myrl Hills                   | Education & Reference | 356.85 |
| 3062833277 | Keven Wyman                  | Life                  | 477.91 |
+------------+------------------------------+-----------------------+--------+
5 rows in set (0.01 sec)
```

随后通过 `COMMIT;` 语句提交事务，当事务结束后，又可以重新读取到最新数据：

```
+------------+------------------------------+-----------------------+--------+
| id         | title                        | type                  | price  |
+------------+------------------------------+-----------------------+--------+
| 3181093216 | The Story of Droolius Caesar | Novel                 | 150.00 |
| 1064253862 | Collin Rolfson               | Education & Reference |  92.85 |
| 1748583991 | The Documentary of cat       | Magazine              | 159.75 |
|  893930596 | Myrl Hills                   | Education & Reference | 356.85 |
| 3062833277 | Keven Wyman                  | Life                  | 477.91 |
+------------+------------------------------+-----------------------+--------+
5 rows in set (0.01 sec)
```

</div>
<div label="Java" value="java">

在 Java 中，可以先定义一个事务的工具类，将开启事务级别 Stale Read 的命令封装成工具方法。



```java
public static class StaleReadHelper {

    public static void startTxnWithStaleRead(Connection conn, Integer seconds) throws SQLException {
        conn.setAutoCommit(false);
        PreparedStatement stmt = conn.prepareStatement(
            "START TRANSACTION READ ONLY AS OF TIMESTAMP NOW() - INTERVAL ? SECOND;"
        );
        stmt.setInt(1, seconds);
        stmt.execute();
    }

}
```

然后在 `BookDAO` 类当中定义一个通过事务开启 Stale Read 功能的方法，在方法内查询最新的书籍列表，但是不再在查询语句中添加 `AS OF TIMESTAMP`。



```java
public class BookDAO {

    // Omit some code...

    public List<Book> getTop5LatestBooksWithTxnStaleRead(Integer seconds) throws SQLException {
        List<Book> books = new ArrayList<>();
        try (Connection conn = ds.getConnection()) {
            // Start a read only transaction.
            TxnHelper.startTxnWithStaleRead(conn, seconds);

            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("""
            SELECT id, title, type, price FROM books ORDER BY published_at DESC LIMIT 5;
            """);
            while (rs.next()) {
                Book book = new Book();
                book.setId(rs.getLong("id"));
                book.setTitle(rs.getString("title"));
                book.setType(rs.getString("type"));
                book.setPrice(rs.getDouble("price"));
                books.add(book);
            }

            // Commit transaction.
            conn.commit();
        } catch (SQLException e) {
            if ("HY000".equals(e.getSQLState()) && e.getErrorCode() == 1105) {
                System.out.println("WARN: cannot set read timestamp to a future time.");
            } else if ("HY000".equals(e.getSQLState()) && e.getErrorCode() == 9006) {
                System.out.println("WARN: GC life time is shorter than transaction duration.");
            } else {
                throw e;
            }
        }
        return books;
    }
}
```



```java
List<Book> top5LatestBooks = bookDAO.getTop5LatestBooks();

if (top5LatestBooks.size() > 0) {
    System.out.println("The latest book price (before update): " + top5LatestBooks.get(0).getPrice());

    Book book = top5LatestBooks.get(0);
    bookDAO.updateBookPriceByID(book.getId(), book.price + 10);

    top5LatestBooks = bookDAO.getTop5LatestBooks();
    System.out.println("The latest book price (after update): " + top5LatestBooks.get(0).getPrice());

    // Use the stale read.
    top5LatestBooks = bookDAO.getTop5LatestBooksWithTxnStaleRead(5);
    System.out.println("The latest book price (maybe stale): " + top5LatestBooks.get(0).getPrice());

    // After the stale read transaction is committed.
    top5LatestBooks = bookDAO.getTop5LatestBooks();
    System.out.println("The latest book price (after the transaction commit): " + top5LatestBooks.get(0).getPrice());
}
```

输出结果：

```
The latest book price (before update): 100.00
The latest book price (after update): 150.00
The latest book price (maybe stale): 100.00
The latest book price (after the transaction commit): 150
```

</div>
</SimpleTab>

通过 `SET TRANSACTION READ ONLY AS OF TIMESTAMP` 语句，你可以将当前事务或下一个事务设置为基于指定历史时间的只读事务。该事务将会基于所提供的历史时间来读取历史数据。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

例如，可以通过下面这个 SQL 将已开启的事务切换到只读模式，通过 `AS OF TIMESTAMP` 语句开启能够读取 5 秒前的历史数据 Stale Read 功能。



```sql
SET TRANSACTION READ ONLY AS OF TIMESTAMP NOW() - INTERVAL 5 SECOND;
```

</div>
<div label="Java" value="java">

可以先定义一个事务的工具类，将开启事务级别 Stale Read 的命令封装成工具方法。



```java
public static class TxnHelper {

    public static void setTxnWithStaleRead(Connection conn, Integer seconds) throws SQLException {
        PreparedStatement stmt = conn.prepareStatement(
            "SET TRANSACTION READ ONLY AS OF TIMESTAMP NOW() - INTERVAL ? SECOND;"
        );
        stmt.setInt(1, seconds);
        stmt.execute();
    }

}
```

然后在 `BookDAO` 类当中定义一个通过事务开启 Stale Read 功能的方法，在方法内查询最新的书籍列表，但是不再在查询语句中添加 `AS OF TIMESTAMP`。



```java
public class BookDAO {

    // Omit some code...

    public List<Book> getTop5LatestBooksWithTxnStaleRead2(Integer seconds) throws SQLException {
        List<Book> books = new ArrayList<>();
        try (Connection conn = ds.getConnection()) {
            // Start a read only transaction.
            conn.setAutoCommit(false);
            StaleReadHelper.setTxnWithStaleRead(conn, seconds);

            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("""
            SELECT id, title, type, price FROM books ORDER BY published_at DESC LIMIT 5;
            """);
            while (rs.next()) {
                Book book = new Book();
                book.setId(rs.getLong("id"));
                book.setTitle(rs.getString("title"));
                book.setType(rs.getString("type"));
                book.setPrice(rs.getDouble("price"));
                books.add(book);
            }

            // Commit transaction.
            conn.commit();
        } catch (SQLException e) {
            if ("HY000".equals(e.getSQLState()) && e.getErrorCode() == 1105) {
                System.out.println("WARN: cannot set read timestamp to a future time.");
            } else if ("HY000".equals(e.getSQLState()) && e.getErrorCode() == 9006) {
                System.out.println("WARN: GC life time is shorter than transaction duration.");
            } else {
                throw e;
            }
        }
        return books;
    }
}
```

</div>
</SimpleTab>

#### 会话级别

为支持读取历史版本数据，TiDB 从 5.4 版本起引入了一个新的系统变量 `tidb_read_staleness`。系统变量 `tidb_read_staleness` 用于设置当前会话允许读取的历史数据范围，其数据类型为 int，作用域为 SESSION。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在会话中开启 Stale Read：



```sql
SET @@tidb_read_staleness="-5";
```

比如，如果该变量的值设置为 -5，TiDB 会在 5 秒时间范围内，保证 TiKV 拥有对应历史版本数据的情况下，选择尽可能新的一个时间戳。

关闭会话当中的 Stale Read：



```sql
set @@tidb_read_staleness="";
```

</div>
<div label="Java" value="java">

在 Java 中示例如下：

```java
public static class StaleReadHelper{

    public static void enableStaleReadOnSession(Connection conn, Integer seconds) throws SQLException {
        PreparedStatement stmt = conn.prepareStatement(
            "SET @@tidb_read_staleness= ?;"
        );
        stmt.setString(1, String.format("-%d", seconds));
        stmt.execute();
    }

    public static void disableStaleReadOnSession(Connection conn) throws SQLException {
        PreparedStatement stmt = conn.prepareStatement(
            "SET @@tidb_read_staleness=\"\";"
        );
        stmt.execute();
    }

}
```

</div>
</SimpleTab>

#### 扩展阅读

- Stale Read 功能的使用场景
- 使用 AS OF TIMESTAMP 语法读取历史数据
- 通过系统变量 tidb_read_staleness 读取历史数据


---
title: HTAP 查询
summary: 介绍 TiDB 中的 HTAP 查询功能。
---

## HTAP 查询

HTAP 是 Hybrid Transactional / Analytical Processing 的缩写。传统意义上，数据库往往专为交易或者分析场景设计，因而数据平台往往需要被切分为 Transactional Processing 和 Analytical Processing 两个部分，而数据需要从交易库复制到分析型数据库以便快速响应分析查询。而 TiDB 数据库则可以同时承担交易和分析两种职能，这大大简化了数据平台的建设，也能让用户使用更新鲜的数据进行分析。

在 TiDB 当中，同时拥有面向在线事务处理的行存储引擎 TiKV 与面向实时分析场景的列存储引擎 TiFlash 两套存储引擎。数据在行存 (Row-Store) 与列存 (Columnar-Store) 同时存在，自动同步，保持强一致性。行存为在线事务处理 OLTP 提供优化，列存则为在线分析处理 OLAP 提供性能优化。

在[创建数据库](#使用-htap-能力)章节当中，已经介绍了如何开启 TiDB 的 HTAP 能力。下面将进一步介绍如何使用 HTAP 能力更快地分析数据。

### 数据准备

在开始之前，你可以[通过 `tiup demo` 命令导入](#方法一通过-tiup-demo-命令行)更加大量的示例数据，例如：



```shell
tiup demo bookshop prepare --users=200000 --books=500000 --authors=100000 --ratings=1000000 --orders=1000000 --host 127.0.0.1 --port 4000 --drop-tables
```

或[使用 TiDB Cloud 的 Import 功能导入](#方法二通过-tidb-cloud-import-功能)预先准备好的示例数据。

### 窗口函数

在使用数据库时，除了希望它能够存储想要记录的数据，能够实现诸如下单买书、给书籍评分等业务功能外，可能还需要对已有的数据进行分析，以便根据数据作出进一步的运营和决策。

在[单表读取](#单表查询)章节当中，已经介绍了如何使用聚合查询来分析数据的整体情况，在更为复杂的使用场景下，你可能希望多个聚合查询的结果汇总在一个查询当中。例如：你想要对某一本书的订单量的历史趋势有所了解，就需要在每个月都对所有订单数据进行一次聚合求 `sum`，然后将 `sum` 结果汇总在一起才能够得到历史的趋势变化数据。

为了方便用户进行此类分析，TiDB 从 3.0 版本开始便支持了窗口函数功能，窗口函数为每一行数据提供了跨行数据访问的能力，不同于常规的聚合查询，窗口函数在对数据行进行聚合时不会导致结果集被合并成单行数据。

与聚合函数类似，窗口函数在使用时也需要搭配一套固定的语法：



```sql
SELECT
    window_function() OVER ([partition_clause] [order_clause] [frame_clause]) AS alias
FROM
    table_name
```

#### `ORDER BY` 子句

例如：可以利用聚合窗口函数 `sum()` 函数的累加效果来实现对某一本书的订单量的历史趋势的分析:



```sql
WITH orders_group_by_month AS (
  SELECT DATE_FORMAT(ordered_at, '%Y-%c') AS month, COUNT(*) AS orders
  FROM orders
  WHERE book_id = 3461722937
  GROUP BY 1
)
SELECT
month,
SUM(orders) OVER(ORDER BY month ASC) as acc
FROM orders_group_by_month
ORDER BY month ASC;
```

`sum()` 函数会在 `OVER` 子句当中通过 `ORDER BY` 子句指定的排序方式按顺序对数据进行累加，累加的结果如下：

```
+---------+-------+
| month   | acc   |
+---------+-------+
| 2011-5  |     1 |
| 2011-8  |     2 |
| 2012-1  |     3 |
| 2012-2  |     4 |
| 2013-1  |     5 |
| 2013-3  |     6 |
| 2015-11 |     7 |
| 2015-4  |     8 |
| 2015-8  |     9 |
| 2017-11 |    10 |
| 2017-5  |    11 |
| 2019-5  |    13 |
| 2020-2  |    14 |
+---------+-------+
13 rows in set (0.01 sec)
```

将得到的数据通过一个横轴为时间，纵轴为累计订单量的折线图进行可视化，便可以轻松地通过折线图的斜率变化宏观地了解到这本书的历史订单的增长趋势。

#### `PARTITION BY` 子句

把需求变得更复杂一点，假设想要分析不同类型书的历史订单增长趋势，并且希望将这些数据通过同一个多系列折线图进行呈现。

可以利用 `PARTITION BY` 子句根据书的类型进行分组，对不同类型的书籍分别统计它们的订单历史订单累计量。



```sql
WITH orders_group_by_month AS (
    SELECT
        b.type AS book_type,
        DATE_FORMAT(ordered_at, '%Y-%c') AS month,
        COUNT(*) AS orders
    FROM orders o
    LEFT JOIN books b ON o.book_id = b.id
    WHERE b.type IS NOT NULL
    GROUP BY book_type, month
), acc AS (
    SELECT
        book_type,
        month,
        SUM(orders) OVER(PARTITION BY book_type ORDER BY book_type, month ASC) as acc
    FROM orders_group_by_month
    ORDER BY book_type, month ASC
)
SELECT * FROM acc;
```

查询结果如下：

```
+------------------------------+---------+------+
| book_type                    | month   | acc  |
+------------------------------+---------+------+
| Magazine                     | 2011-10 |    1 |
| Magazine                     | 2011-8  |    2 |
| Magazine                     | 2012-5  |    3 |
| Magazine                     | 2013-1  |    4 |
| Magazine                     | 2013-6  |    5 |
...
| Novel                        | 2011-3  |   13 |
| Novel                        | 2011-4  |   14 |
| Novel                        | 2011-6  |   15 |
| Novel                        | 2011-8  |   17 |
| Novel                        | 2012-1  |   18 |
| Novel                        | 2012-2  |   20 |
...
| Sports                       | 2021-4  |   49 |
| Sports                       | 2021-7  |   50 |
| Sports                       | 2022-4  |   51 |
+------------------------------+---------+------+
1500 rows in set (1.70 sec)
```

#### 非聚合窗口函数

除此之外，TiDB 还提供了一些非聚合的窗口函数，可以借助这些函数实现更加丰富分析查询。

例如，在前面的[分页查询](#分页查询)章节当中，已经介绍了如何巧妙地利用 `row_number()` 函数实现高效的分页批处理能力。

### 混合负载

当将 TiDB 应用于在线实时分析处理的混合负载场景时，开发人员只需要提供一个入口，TiDB 将自动根据业务类型选择不同的处理引擎。

#### 开启列存副本

TiDB 默认使用的存储引擎 TiKV 是行存的，你可以通过阅读[开启 HTAP 能力](#使用-htap-能力)章节，在进行后续步骤前，先通过如下 SQL 对 `books` 与 `orders` 表添加 TiFlash 列存副本：



```sql
ALTER TABLE books SET TIFLASH REPLICA 1;
ALTER TABLE orders SET TIFLASH REPLICA 1;
```

通过执行下面的 SQL 语句可以查看到 TiDB 创建列存副本的进度：



```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'bookshop' and TABLE_NAME = 'books';
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'bookshop' and TABLE_NAME = 'orders';
```

当 `PROGRESS` 列为 1 时表示同步进度完成度达到 100%，`AVAILABLE` 列为 1 表示副本当前可用。

```
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| TABLE_SCHEMA | TABLE_NAME | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| bookshop     | books      |      143 |             1 |                 |         1 |        1 |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
1 row in set (0.07 sec)
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| TABLE_SCHEMA | TABLE_NAME | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| bookshop     | orders     |      147 |             1 |                 |         1 |        1 |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
1 row in set (0.07 sec)
```

副本添加完成之后，你可以通过使用 `EXPLAIN` 语句查看上面窗口函数[示例 SQL](#partition-by-子句) 的执行计划。你会发现执行计划当中已经出现了 `cop[tiflash]` 字样，说明 TiFlash 引擎已经开始发挥作用了。

再次执行[示例 SQL](#partition-by-子句)，查询结果如下：

```
+------------------------------+---------+------+
| book_type                    | month   | acc  |
+------------------------------+---------+------+
| Magazine                     | 2011-10 |    1 |
| Magazine                     | 2011-8  |    2 |
| Magazine                     | 2012-5  |    3 |
| Magazine                     | 2013-1  |    4 |
| Magazine                     | 2013-6  |    5 |
...
| Novel                        | 2011-3  |   13 |
| Novel                        | 2011-4  |   14 |
| Novel                        | 2011-6  |   15 |
| Novel                        | 2011-8  |   17 |
| Novel                        | 2012-1  |   18 |
| Novel                        | 2012-2  |   20 |
...
| Sports                       | 2021-4  |   49 |
| Sports                       | 2021-7  |   50 |
| Sports                       | 2022-4  |   51 |
+------------------------------+---------+------+
1500 rows in set (0.79 sec)
```

通过对比前后两次的执行结果，你会发现使用 TiFlash 处理有查询速度有了较为明显的提升（当数据量更大时，提升会更为显著）。这是因为在使用窗口函数时往往需要对某些列的数据进行全表扫描，相比行存的 TiKV，列存的 TiFlash 更加适合来处理这类分析型任务的负载。而对于 TiKV 来说，如果能够通过主键或索引快速地将所要查询的行数减少，往往查询速度也会非常快，而且所消耗的资源一般相对 TiFlash 而言会更少。

#### 指定查询引擎

尽管 TiDB 会使用基于成本的优化器（CBO）自动地根据代价估算选择是否使用 TiFlash 副本。但是在实际使用当中，如果你非常确定查询的类型，推荐你使用 Optimizer Hints 明确的指定查询所使用的执行引擎，避免因为优化器的优化结果不同，导致应用程序性能出现波动。

你可以像下面的 SQL 一样在 SELECT 语句中通过 Hint `/*+ read_from_storage(engine_name[table_name]) */` 指定查询时需要使用的查询引擎。

> **注意：**
>
> 1. 如果你的表使用了别名，你应该将 Hints 当中的 table_name 替代为 alias_name, 否则 Hints 会失效。
> 2. 另外，对[公共表表达式](#公共表表达式-(cte))设置 read_from_storage Hint 是不起作用的。



```sql
WITH orders_group_by_month AS (
    SELECT
        /*+ read_from_storage(tikv[o]) */
        b.type AS book_type,
        DATE_FORMAT(ordered_at, '%Y-%c') AS month,
        COUNT(*) AS orders
    FROM orders o
    LEFT JOIN books b ON o.book_id = b.id
    WHERE b.type IS NOT NULL
    GROUP BY book_type, month
), acc AS (
    SELECT
        book_type,
        month,
        SUM(orders) OVER(PARTITION BY book_type ORDER BY book_type, month ASC) as acc
    FROM orders_group_by_month mo
    ORDER BY book_type, month ASC
)
SELECT * FROM acc;
```

如果你通过 `EXPLAIN` 语句查看上面 SQL 的执行计划，你会发现 task 列中会同时出现 `cop[tiflash]` 和 `cop[tikv]` ，这意味着 TiDB 在处理这个查询的时候会同时调度行存查询引擎和列存查询引擎来完成查询任务。需要指出的是，因为 tiflash 和 tikv 存储引擎通常属于不同的计算节点，所以两种查询类型互相之间不受影响。

你可以通过阅读使用 TiDB 读取 TiFlash 小节进一步了解 TiDB 如何选择使用 TiFlash 作为查询引擎。

### 扩展阅读

- HTAP 快速上手指南
- HTAP 深入探索指南
- 窗口函数
- 使用 TiFlash


---
title: FastScan
summary: 介绍通过使用 FastScan 来加速 OLAP 场景的查询的方法。
---

## FastScan

> **警告：**
>
> 该功能目前是实验性功能，其形式和使用方法可能会在未来版本中发生变化。

本文档介绍通过使用 FastScan 来加速 Online Analytical Processing (OLAP) 场景中查询的方法。

默认情况下，TiFlash 能够保证查询结果精度以及数据一致性。如果使用 FastScan，TiFlash 可以实现更高效的查询性能，但不保证查询结果精度和数据一致性。

某些 OLAP 对查询结果精度可以容忍一定误差。如果对查询性能有更高要求，可以在 session 级别或 global 级别开启 FastScan 功能，你可以通过修改变量 `tiflash_fastscan` 的值来选择是否启用 FastScan 功能。

### 启用和禁用 FastScan

默认情况下，session 和 global 级别的变量 `tiflash_fastscan=OFF`，即没有开启 FastScan 功能。你可以通过以下语句来查看对应的变量信息。

```
show variables like 'tiflash_fastscan';
```

```
+------------------+-------+
| Variable_name    | Value |
+------------------+-------+
| tiflash_fastscan | OFF   |
+------------------+-------+
```

```
show global variables like 'tiflash_fastscan';
```

```
+------------------+-------+
| Variable_name    | Value |
+------------------+-------+
| tiflash_fastscan | OFF   |
+------------------+-------+
```

变量 `tiflash_fastscan` 支持 session 级别和 global 级别的修改。如果需要在当前 session 中启用 FastScan 功能，可以通过以下语句设置:

```
set session tiflash_fastscan=ON;
```

如果对 global 级别的 `tiflash_fastscan` 进行设置，设置后新建的会话中默认 session 和 global 变量 `tiflash_fastscan` 启用新值。设置方式如下：

```
set global tiflash_fastscan=ON;
```

可以用下面语句禁用 FastScan：

```sql
set session tiflash_fastscan=OFF;
set global tiflash_fastscan=OFF;
```

### 实现机制

TiFlash 存储层的数据主要存放在 Delta 层和 Stable 层。

在默认状态下（即未开启 FastScan 功能），TableScan 算子过程整体包括了以下步骤：

1. Read data：在 Delta 层 和 Stable 层分别建立数据流，进行各自数据的读取。
2. Sort Merge：将步骤 1 中建立的数据流进行合并，并且将数据按照 (handle, version) 顺序排列返回。
3. Range Filter：根据读取范围限制，对步骤 2 中的数据进行过滤筛选并返回。
4. MVCC + Column Filter：对步骤 3 中的数据进行 MVCC 过滤，同时过滤掉不需要的列并返回。

FastScan 通过损失一定的数据一致性来获取更快的查询性能。FastScan 中的 TableScan 流程省略了上述过程中的第 2 步和第 4 步中 MVCC 的部分，从而提高查询性能。


# 事务

---
title: 事务概览
summary: 简单介绍 TiDB 中的事务。
---

## 事务概览

TiDB 支持完整的分布式事务，提供乐观事务与悲观事务（TiDB 3.0 中引入）两种事务模型。本文主要介绍涉及到事务的语句、乐观事务和悲观事务、事务的隔离级别，以及乐观事务应用端重试和错误处理。

### 拓展学习视频

[TiDB 特有功能与事务控制 - TiDB v6](https://learn.pingcap.com/learner/course/750002/?utm_source=docs-cn-dev-guide)：了解可用于应用程序的 TiDB 独特功能，如 `AUTO_RANDOM` 及 `AUTO_INCREMENT` 特别注意事项、全局临时表、如何使用 TiFlash 启用 HTAP 以及放置策略等。

### 通用语句

本章介绍在 TiDB 中如何使用事务。 将使用下面的示例来演示一个简单事务的控制流程：

Bob 要给 Alice 转账 20 元钱，当中至少包括两个操作：

- Bob 账户减少 20 元。
- Alice 账户增加 20 元。

事务可以确保以上两个操作要么都执行成功，要么都执行失败，不会出现钱平白消失或出现的情况。

使用 [bookshop](#bookshop-应用) 数据库中的 `users` 表，在表中插入一些示例数据：



```sql
INSERT INTO users (id, nickname, balance)
  VALUES (2, 'Bob', 200);
INSERT INTO users (id, nickname, balance)
  VALUES (1, 'Alice', 100);
```

现在，运行以下事务并解释每个语句的含义：



```sql
BEGIN;
  UPDATE users SET balance = balance - 20 WHERE nickname = 'Bob';
  UPDATE users SET balance = balance + 20 WHERE nickname= 'Alice';
COMMIT;
```

上述事务成功后，表应如下所示：

```
+----+--------------+---------+
| id | account_name | balance |
+----+--------------+---------+
|  1 | Alice        |  120.00 |
|  2 | Bob          |  180.00 |
+----+--------------+---------+

```

#### 开启事务

要显式地开启一个新事务，既可以使用 `BEGIN` 语句，也可以使用 `START TRANSACTION` 语句，两者效果相同。语法：



```sql
BEGIN;
```



```sql
START TRANSACTION;
```

TiDB 的默认事务模式是悲观事务，你也可以明确指定开启[乐观事务](#乐观事务和悲观事务)：



```sql
BEGIN OPTIMISTIC;
```

开启[悲观事务](#乐观事务和悲观事务)：



```sql
BEGIN PESSIMISTIC;
```

如果执行以上语句时，当前 Session 正处于一个事务的中间过程，那么系统会先自动提交当前事务，再开启一个新的事务。

#### 提交事务

`COMMIT` 语句用于提交 TiDB 在当前事务中进行的所有修改。语法：



```sql
COMMIT;
```

启用乐观事务前，请确保应用程序可正确处理 `COMMIT` 语句可能返回的错误。如果不确定应用程序将会如何处理，建议改为使用悲观事务。

#### 回滚事务

`ROLLBACK` 语句用于回滚并撤销当前事务的所有修改。语法：



```sql
ROLLBACK;
```

回到之前转账示例，使用 `ROLLBACK` 回滚整个事务之后，Alice 和 Bob 的余额都未发生改变，当前事务的所有修改一起被取消。



```sql
TRUNCATE TABLE `users`;

INSERT INTO `users` (`id`, `nickname`, `balance`) VALUES (1, 'Alice', 100), (2, 'Bob', 200);

SELECT * FROM `users`;
+----+--------------+---------+
| id | nickname     | balance |
+----+--------------+---------+
|  1 | Alice        |  100.00 |
|  2 | Bob          |  200.00 |
+----+--------------+---------+

BEGIN;
  UPDATE `users` SET `balance` = `balance` - 20 WHERE `nickname`='Bob';
  UPDATE `users` SET `balance` = `balance` + 20 WHERE `nickname`='Alice';
ROLLBACK;

SELECT * FROM `users`;
+----+--------------+---------+
| id | nickname     | balance |
+----+--------------+---------+
|  1 | Alice        |  100.00 |
|  2 | Bob          |  200.00 |
+----+--------------+---------+
```

如果客户端连接中止或关闭，也会自动回滚该事务。

### 事务隔离级别

事务隔离级别是数据库事务处理的基础，**ACID** 中的 **“I”**，即 Isolation，指的就是事务的隔离性。

SQL-92 标准定义了 4 种隔离级别：读未提交 (`READ UNCOMMITTED`)、读已提交 (`READ COMMITTED`)、可重复读 (`REPEATABLE READ`)、串行化 (`SERIALIZABLE`)。详见下表：

| Isolation Level  | Dirty Write  | Dirty Read   | Fuzzy Read   | Phantom      |
| ---------------- | ------------ | ------------ | ------------ | ------------ |
| READ UNCOMMITTED | Not Possible | Possible     | Possible     | Possible     |
| READ COMMITTED   | Not Possible | Not possible | Possible     | Possible     |
| REPEATABLE READ  | Not Possible | Not possible | Not possible | Possible     |
| SERIALIZABLE     | Not Possible | Not possible | Not possible | Not possible |

TiDB 语法上支持设置 `READ COMMITTED` 和 `REPEATABLE READ` 两种隔离级别：



```sql
mysql> SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
ERROR 8048 (HY000): The isolation level 'READ-UNCOMMITTED' is not supported. Set tidb_skip_isolation_level_check=1 to skip this error
mysql> SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
Query OK, 0 rows affected (0.00 sec)

mysql> SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
Query OK, 0 rows affected (0.00 sec)

mysql> SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
ERROR 8048 (HY000): The isolation level 'SERIALIZABLE' is not supported. Set tidb_skip_isolation_level_check=1 to skip this error
```

TiDB 实现了快照隔离 (Snapshot Isolation, SI) 级别的一致性。为与 MySQL 保持一致，又称其为“可重复读”。该隔离级别不同于 ANSI 可重复读隔离级别 和 MySQL 可重复读隔离级别。更多细节请阅读 TiDB 事务隔离级别。


---
title: 乐观事务和悲观事务
summary: 介绍 TiDB 中的乐观事务和悲观事务，乐观事务的重试等。
---

## 乐观事务和悲观事务

简单的讲，乐观事务模型就是直接提交，遇到冲突就回滚，悲观事务模型就是在真正提交事务前，先尝试对需要修改的资源上锁，只有在确保事务一定能够执行成功后，才开始提交。

对于乐观事务模型来说，比较适合冲突率不高的场景，因为直接提交大概率会成功，冲突是小概率事件，但是一旦遇到事务冲突，回滚的代价会比较大。

悲观事务的好处是对于冲突率高的场景，提前上锁的代价小于事后回滚的代价，而且还能以比较低的代价解决多个并发事务互相冲突导致谁也成功不了的场景。不过悲观事务在冲突率不高的场景并没有乐观事务处理高效。

从应用端实现的复杂度而言，悲观事务更直观，更容易实现。而乐观事务需要复杂的应用端重试机制来保证。

下面用 [bookshop](#bookshop-应用) 数据库中的表实现一个购书的例子来演示乐观事务和悲观事务的区别以及优缺点。购书流程主要包括：

1. 更新库存数量
2. 创建订单
3. 付款

这三个操作需要保证全部成功或者全部失败，并且在并发情况下要保证不超卖。

### 悲观事务

下面代码以悲观事务的方式，用两个线程模拟了两个用户并发买同一本书的过程，书店剩余 10 本，Bob 购买了 6 本，Alice 购买了 4 本。两个人几乎同一时间完成订单，最终，这本书的剩余库存为零。

<SimpleTab groupId="language">

<div label="Java" value="java">

当使用多个线程模拟多用户同时插入的情况时，需要使用一个线程安全的连接对象，这里使用 Java 当前较流行的连接池 [HikariCP](https://github.com/brettwooldridge/HikariCP) 。

</div>

<div label="Golang" value="golang">

Golang 的 `sql.DB` 是并发安全的，无需引入外部包。

封装一个用于适配 TiDB 事务的工具包 [util](https://github.com/pingcap-inc/tidb-example-golang/tree/main/util)，编写以下代码备用：



```go
package util

import (
    "context"
    "database/sql"
)

type TiDBSqlTx struct {
    *sql.Tx
    conn        *sql.Conn
    pessimistic bool
}

func TiDBSqlBegin(db *sql.DB, pessimistic bool) (*TiDBSqlTx, error) {
    ctx := context.Background()
    conn, err := db.Conn(ctx)
    if err != nil {
        return nil, err
    }
    if pessimistic {
        _, err = conn.ExecContext(ctx, "set @@tidb_txn_mode=?", "pessimistic")
    } else {
        _, err = conn.ExecContext(ctx, "set @@tidb_txn_mode=?", "optimistic")
    }
    if err != nil {
        return nil, err
    }
    tx, err := conn.BeginTx(ctx, nil)
    if err != nil {
        return nil, err
    }
    return &TiDBSqlTx{
        conn:        conn,
        Tx:          tx,
        pessimistic: pessimistic,
    }, nil
}

func (tx *TiDBSqlTx) Commit() error {
    defer tx.conn.Close()
    return tx.Tx.Commit()
}

func (tx *TiDBSqlTx) Rollback() error {
    defer tx.conn.Close()
    return tx.Tx.Rollback()
}
```

</div>

<div label="Python" value="python">

使用 Python 的 mysqlclient Driver 开启多个连接对象进行交互，线程之间不共享连接，以保证其线程安全。

</div>
</SimpleTab>

#### 1. 编写悲观事务示例

<SimpleTab groupId="language">

<div label="Java" value="java">

**配置文件**

在 Java 中，如果你使用 Maven 作为包管理，在 `pom.xml` 中的 `<dependencies>` 节点中，加入以下依赖来引入 `HikariCP`，同时设定打包目标，及 JAR 包启动的主类，完整的 `pom.xml` 如下所示:



```xml
<?xml version="1.0" encoding="UTF-8"?>

<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>com.pingcap</groupId>
  <artifactId>plain-java-txn</artifactId>
  <version>0.0.1</version>

  <name>plain-java-jdbc</name>

  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.source>17</maven.compiler.source>
    <maven.compiler.target>17</maven.compiler.target>
  </properties>

  <dependencies>
    <dependency>
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <version>4.13.2</version>
      <scope>test</scope>
    </dependency>

    <!-- https://mvnrepository.com/artifact/mysql/mysql-connector-java -->
    <dependency>
      <groupId>mysql</groupId>
      <artifactId>mysql-connector-java</artifactId>
      <version>8.0.28</version>
    </dependency>

    <dependency>
      <groupId>com.zaxxer</groupId>
      <artifactId>HikariCP</artifactId>
      <version>5.0.1</version>
    </dependency>
  </dependencies>

  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-assembly-plugin</artifactId>
        <version>3.3.0</version>
        <configuration>
          <descriptorRefs>
            <descriptorRef>jar-with-dependencies</descriptorRef>
          </descriptorRefs>
          <archive>
            <manifest>
              <mainClass>com.pingcap.txn.TxnExample</mainClass>
            </manifest>
          </archive>

        </configuration>
        <executions>
          <execution>
            <id>make-assembly</id>
            <phase>package</phase>
            <goals>
              <goal>single</goal>
            </goals>
          </execution>
        </executions>
      </plugin>
    </plugins>
  </build>

</project>
```

**代码**

随后编写代码：



```java
package com.pingcap.txn;

import com.zaxxer.hikari.HikariDataSource;

import java.math.BigDecimal;
import java.sql.*;
import java.util.Arrays;
import java.util.concurrent.*;

public class TxnExample {
    public static void main(String[] args) throws SQLException, InterruptedException {
        System.out.println(Arrays.toString(args));
        int aliceQuantity = 0;
        int bobQuantity = 0;

        for (String arg: args) {
            if (arg.startsWith("ALICE_NUM")) {
                aliceQuantity = Integer.parseInt(arg.replace("ALICE_NUM=", ""));
            }

            if (arg.startsWith("BOB_NUM")) {
                bobQuantity = Integer.parseInt(arg.replace("BOB_NUM=", ""));
            }
        }

        HikariDataSource ds = new HikariDataSource();
        ds.setJdbcUrl("jdbc:mysql://localhost:4000/bookshop?useServerPrepStmts=true&cachePrepStmts=true");
        ds.setUsername("root");
        ds.setPassword("");

        // prepare data
        Connection connection = ds.getConnection();
        createBook(connection, 1L, "Designing Data-Intensive Application", "Science & Technology",
                Timestamp.valueOf("2018-09-01 00:00:00"), new BigDecimal(100), 10);
        createUser(connection, 1L, "Bob", new BigDecimal(10000));
        createUser(connection, 2L, "Alice", new BigDecimal(10000));

        CountDownLatch countDownLatch = new CountDownLatch(2);
        ExecutorService threadPool = Executors.newFixedThreadPool(2);

        final int finalBobQuantity = bobQuantity;
        threadPool.execute(() -> {
            buy(ds, 1, 1000L, 1L, 1L, finalBobQuantity);
            countDownLatch.countDown();
        });
        final int finalAliceQuantity = aliceQuantity;
        threadPool.execute(() -> {
            buy(ds, 2, 1001L, 1L, 2L, finalAliceQuantity);
            countDownLatch.countDown();
        });

        countDownLatch.await(5, TimeUnit.SECONDS);
    }

    public static void createUser(Connection connection, Long id, String nickname, BigDecimal balance) throws SQLException  {
        PreparedStatement insert = connection.prepareStatement(
                "INSERT INTO `users` (`id`, `nickname`, `balance`) VALUES (?, ?, ?)");
        insert.setLong(1, id);
        insert.setString(2, nickname);
        insert.setBigDecimal(3, balance);
        insert.executeUpdate();
    }

    public static void createBook(Connection connection, Long id, String title, String type, Timestamp publishedAt, BigDecimal price, Integer stock) throws SQLException {
        PreparedStatement insert = connection.prepareStatement(
                "INSERT INTO `books` (`id`, `title`, `type`, `published_at`, `price`, `stock`) values (?, ?, ?, ?, ?, ?)");
        insert.setLong(1, id);
        insert.setString(2, title);
        insert.setString(3, type);
        insert.setTimestamp(4, publishedAt);
        insert.setBigDecimal(5, price);
        insert.setInt(6, stock);

        insert.executeUpdate();
    }

    public static void buy (HikariDataSource ds, Integer threadID,
                            Long orderID, Long bookID, Long userID, Integer quantity) {
        String txnComment = "/* txn " + threadID + " */ ";

        try (Connection connection = ds.getConnection()) {
            try {
                connection.setAutoCommit(false);
                connection.createStatement().executeUpdate(txnComment + "begin pessimistic");

                // waiting for other thread ran the 'begin pessimistic' statement
                TimeUnit.SECONDS.sleep(1);

                BigDecimal price = null;

                // read price of book
                PreparedStatement selectBook = connection.prepareStatement(txnComment + "select price from books where id = ? for update");
                selectBook.setLong(1, bookID);
                ResultSet res = selectBook.executeQuery();
                if (!res.next()) {
                    throw new RuntimeException("book not exist");
                } else {
                    price = res.getBigDecimal("price");
                }

                // update book
                String updateBookSQL = "update `books` set stock = stock - ? where id = ? and stock - ? >= 0";
                PreparedStatement updateBook = connection.prepareStatement(txnComment + updateBookSQL);
                updateBook.setInt(1, quantity);
                updateBook.setLong(2, bookID);
                updateBook.setInt(3, quantity);
                int affectedRows = updateBook.executeUpdate();

                if (affectedRows == 0) {
                    // stock not enough, rollback
                    connection.createStatement().executeUpdate(txnComment + "rollback");
                    return;
                }

                // insert order
                String insertOrderSQL = "insert into `orders` (`id`, `book_id`, `user_id`, `quality`) values (?, ?, ?, ?)";
                PreparedStatement insertOrder = connection.prepareStatement(txnComment + insertOrderSQL);
                insertOrder.setLong(1, orderID);
                insertOrder.setLong(2, bookID);
                insertOrder.setLong(3, userID);
                insertOrder.setInt(4, quantity);
                insertOrder.executeUpdate();

                // update user
                String updateUserSQL = "update `users` set `balance` = `balance` - ? where id = ?";
                PreparedStatement updateUser = connection.prepareStatement(txnComment + updateUserSQL);
                updateUser.setBigDecimal(1, price.multiply(new BigDecimal(quantity)));
                updateUser.setLong(2, userID);
                updateUser.executeUpdate();

                connection.createStatement().executeUpdate(txnComment + "commit");
            } catch (Exception e) {
                connection.createStatement().executeUpdate(txnComment + "rollback");
                e.printStackTrace();
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

</div>

<div label="Golang" value="golang">

首先编写一个封装了所需的数据库操作的 `helper.go` 文件：



```go
package main

import (
    "context"
    "database/sql"
    "fmt"
    "time"

    "github.com/go-sql-driver/mysql"
    "github.com/pingcap-inc/tidb-example-golang/util"
    "github.com/shopspring/decimal"
)

type TxnFunc func(txn *util.TiDBSqlTx) error

const (
    ErrWriteConflict      = 9007 // Transactions in TiKV encounter write conflicts.
    ErrInfoSchemaChanged  = 8028 // table schema changes
    ErrForUpdateCantRetry = 8002 // "SELECT FOR UPDATE" commit conflict
    ErrTxnRetryable       = 8022 // The transaction commit fails and has been rolled back
)

const retryTimes = 5

var retryErrorCodeSet = map[uint16]interface{}{
    ErrWriteConflict:      nil,
    ErrInfoSchemaChanged:  nil,
    ErrForUpdateCantRetry: nil,
    ErrTxnRetryable:       nil,
}

func runTxn(db *sql.DB, optimistic bool, optimisticRetryTimes int, txnFunc TxnFunc) {
    txn, err := util.TiDBSqlBegin(db, !optimistic)
    if err != nil {
        panic(err)
    }

    err = txnFunc(txn)
    if err != nil {
        txn.Rollback()
        if mysqlErr, ok := err.(*mysql.MySQLError); ok && optimistic && optimisticRetryTimes != 0 {
            if _, retryableError := retryErrorCodeSet[mysqlErr.Number]; retryableError {
                fmt.Printf("[runTxn] got a retryable error, rest time: %d\n", optimisticRetryTimes-1)
                runTxn(db, optimistic, optimisticRetryTimes-1, txnFunc)
                return
            }
        }

        fmt.Printf("[runTxn] got an error, rollback: %+v\n", err)
    } else {
        err = txn.Commit()
        if mysqlErr, ok := err.(*mysql.MySQLError); ok && optimistic && optimisticRetryTimes != 0 {
            if _, retryableError := retryErrorCodeSet[mysqlErr.Number]; retryableError {
                fmt.Printf("[runTxn] got a retryable error, rest time: %d\n", optimisticRetryTimes-1)
                runTxn(db, optimistic, optimisticRetryTimes-1, txnFunc)
                return
            }
        }

        if err == nil {
            fmt.Println("[runTxn] commit success")
        }
    }
}

func prepareData(db *sql.DB, optimistic bool) {
    runTxn(db, optimistic, retryTimes, func(txn *util.TiDBSqlTx) error {
        publishedAt, err := time.Parse("2006-01-02 15:04:05", "2018-09-01 00:00:00")
        if err != nil {
            return err
        }

        if err = createBook(txn, 1, "Designing Data-Intensive Application",
            "Science & Technology", publishedAt, decimal.NewFromInt(100), 10); err != nil {
            return err
        }

        if err = createUser(txn, 1, "Bob", decimal.NewFromInt(10000)); err != nil {
            return err
        }

        if err = createUser(txn, 2, "Alice", decimal.NewFromInt(10000)); err != nil {
            return err
        }

        return nil
    })
}

func buyPessimistic(db *sql.DB, goroutineID, orderID, bookID, userID, amount int) {
    txnComment := fmt.Sprintf("/* txn %d */ ", goroutineID)
    if goroutineID != 1 {
        txnComment = "\t" + txnComment
    }

    fmt.Printf("\nuser %d try to buy %d books(id: %d)\n", userID, amount, bookID)

    runTxn(db, false, retryTimes, func(txn *util.TiDBSqlTx) error {
        time.Sleep(time.Second)

        // read the price of book
        selectBookForUpdate := "select `price` from books where id = ? for update"
        bookRows, err := txn.Query(selectBookForUpdate, bookID)
        if err != nil {
            return err
        }
        fmt.Println(txnComment + selectBookForUpdate + " successful")
        defer bookRows.Close()

        price := decimal.NewFromInt(0)
        if bookRows.Next() {
            err = bookRows.Scan(&price)
            if err != nil {
                return err
            }
        } else {
            return fmt.Errorf("book ID not exist")
        }
        bookRows.Close()

        // update book
        updateStock := "update `books` set stock = stock - ? where id = ? and stock - ? >= 0"
        result, err := txn.Exec(updateStock, amount, bookID, amount)
        if err != nil {
            return err
        }
        fmt.Println(txnComment + updateStock + " successful")

        affected, err := result.RowsAffected()
        if err != nil {
            return err
        }

        if affected == 0 {
            return fmt.Errorf("stock not enough, rollback")
        }

        // insert order
        insertOrder := "insert into `orders` (`id`, `book_id`, `user_id`, `quality`) values (?, ?, ?, ?)"
        if _, err := txn.Exec(insertOrder,
            orderID, bookID, userID, amount); err != nil {
            return err
        }
        fmt.Println(txnComment + insertOrder + " successful")

        // update user
        updateUser := "update `users` set `balance` = `balance` - ? where id = ?"
        if _, err := txn.Exec(updateUser,
            price.Mul(decimal.NewFromInt(int64(amount))), userID); err != nil {
            return err
        }
        fmt.Println(txnComment + updateUser + " successful")

        return nil
    })
}

func buyOptimistic(db *sql.DB, goroutineID, orderID, bookID, userID, amount int) {
    txnComment := fmt.Sprintf("/* txn %d */ ", goroutineID)
    if goroutineID != 1 {
        txnComment = "\t" + txnComment
    }

    fmt.Printf("\nuser %d try to buy %d books(id: %d)\n", userID, amount, bookID)

    runTxn(db, true, retryTimes, func(txn *util.TiDBSqlTx) error {
        time.Sleep(time.Second)

        // read the price and stock of book
        selectBookForUpdate := "select `price`, `stock` from books where id = ? for update"
        bookRows, err := txn.Query(selectBookForUpdate, bookID)
        if err != nil {
            return err
        }
        fmt.Println(txnComment + selectBookForUpdate + " successful")
        defer bookRows.Close()

        price, stock := decimal.NewFromInt(0), 0
        if bookRows.Next() {
            err = bookRows.Scan(&price, &stock)
            if err != nil {
                return err
            }
        } else {
            return fmt.Errorf("book ID not exist")
        }
        bookRows.Close()

        if stock < amount {
            return fmt.Errorf("book not enough")
        }

        // update book
        updateStock := "update `books` set stock = stock - ? where id = ? and stock - ? >= 0"
        result, err := txn.Exec(updateStock, amount, bookID, amount)
        if err != nil {
            return err
        }
        fmt.Println(txnComment + updateStock + " successful")

        affected, err := result.RowsAffected()
        if err != nil {
            return err
        }

        if affected == 0 {
            return fmt.Errorf("stock not enough, rollback")
        }

        // insert order
        insertOrder := "insert into `orders` (`id`, `book_id`, `user_id`, `quality`) values (?, ?, ?, ?)"
        if _, err := txn.Exec(insertOrder,
            orderID, bookID, userID, amount); err != nil {
            return err
        }
        fmt.Println(txnComment + insertOrder + " successful")

        // update user
        updateUser := "update `users` set `balance` = `balance` - ? where id = ?"
        if _, err := txn.Exec(updateUser,
            price.Mul(decimal.NewFromInt(int64(amount))), userID); err != nil {
            return err
        }
        fmt.Println(txnComment + updateUser + " successful")

        return nil
    })
}

func createBook(txn *util.TiDBSqlTx, id int, title, bookType string,
    publishedAt time.Time, price decimal.Decimal, stock int) error {
    _, err := txn.ExecContext(context.Background(),
        "INSERT INTO `books` (`id`, `title`, `type`, `published_at`, `price`, `stock`) values (?, ?, ?, ?, ?, ?)",
        id, title, bookType, publishedAt, price, stock)
    return err
}

func createUser(txn *util.TiDBSqlTx, id int, nickname string, balance decimal.Decimal) error {
    _, err := txn.ExecContext(context.Background(),
        "INSERT INTO `users` (`id`, `nickname`, `balance`) VALUES (?, ?, ?)",
        id, nickname, balance)
    return err
}
```

再编写一个包含 `main` 函数的 `txn.go` 来调用 `helper.go`，同时处理传入的命令行参数：



```go
package main

import (
    "database/sql"
    "flag"
    "fmt"
    "sync"
)

func main() {
    optimistic, alice, bob := parseParams()

    openDB("mysql", "root:@tcp(127.0.0.1:4000)/bookshop?charset=utf8mb4", func(db *sql.DB) {
        prepareData(db, optimistic)
        buy(db, optimistic, alice, bob)
    })
}

func buy(db *sql.DB, optimistic bool, alice, bob int) {
    buyFunc := buyOptimistic
    if !optimistic {
        buyFunc = buyPessimistic
    }

    wg := sync.WaitGroup{}
    wg.Add(1)
    go func() {
        defer wg.Done()
        buyFunc(db, 1, 1000, 1, 1, bob)
    }()

    wg.Add(1)
    go func() {
        defer wg.Done()
        buyFunc(db, 2, 1001, 1, 2, alice)
    }()

    wg.Wait()
}

func openDB(driverName, dataSourceName string, runnable func(db *sql.DB)) {
    db, err := sql.Open(driverName, dataSourceName)
    if err != nil {
        panic(err)
    }
    defer db.Close()

    runnable(db)
}

func parseParams() (optimistic bool, alice, bob int) {
    flag.BoolVar(&optimistic, "o", false, "transaction is optimistic")
    flag.IntVar(&alice, "a", 4, "Alice bought num")
    flag.IntVar(&bob, "b", 6, "Bob bought num")

    flag.Parse()

    fmt.Println(optimistic, alice, bob)

    return optimistic, alice, bob
}
```

Golang 的例子中，已经包含乐观事务。

</div>

<div label="Python" value="python">

```python
import time

import MySQLdb
import os
import datetime
from threading import Thread

REPEATABLE_ERROR_CODE_SET = {
    9007,  # Transactions in TiKV encounter write conflicts.
    8028,  # table schema changes
    8002,  # "SELECT FOR UPDATE" commit conflict
    8022   # The transaction commit fails and has been rolled back
}


def create_connection():
    return MySQLdb.connect(
        host="127.0.0.1",
        port=4000,
        user="root",
        password="",
        database="bookshop",
        autocommit=False
    )


def prepare_data() -> None:
    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO `books` (`id`, `title`, `type`, `published_at`, `price`, `stock`) "
                           "values (%s, %s, %s, %s, %s, %s)",
                           (1, "Designing Data-Intensive Application", "Science & Technology",
                            datetime.datetime(2018, 9, 1), 100, 10))

            cursor.executemany("INSERT INTO `users` (`id`, `nickname`, `balance`) VALUES (%s, %s, %s)",
                               [(1, "Bob", 10000), (2, "ALICE", 10000)])
            connection.commit()


def buy_optimistic(thread_id: int, order_id: int, book_id: int, user_id: int, amount: int,
                   optimistic_retry_times: int = 5) -> None:
    connection = create_connection()

    txn_log_header = f"/* txn {thread_id} */"
    if thread_id != 1:
        txn_log_header = "\t" + txn_log_header

    with connection:
        with connection.cursor() as cursor:
            cursor.execute("BEGIN OPTIMISTIC")
            print(f'{txn_log_header} BEGIN OPTIMISTIC')
            time.sleep(1)

            try:
                # read the price of book
                select_book_for_update = "SELECT `price`, `stock` FROM books WHERE id = %s FOR UPDATE"
                cursor.execute(select_book_for_update, (book_id,))
                book = cursor.fetchone()
                if book is None:
                    raise Exception("book_id not exist")
                price, stock = book
                print(f'{txn_log_header} {select_book_for_update} successful')

                if stock < amount:
                    raise Exception("book not enough, rollback")

                # update book
                update_stock = "update `books` set stock = stock - %s where id = %s and stock - %s >= 0"
                rows_affected = cursor.execute(update_stock, (amount, book_id, amount))
                print(f'{txn_log_header} {update_stock} successful')

                if rows_affected == 0:
                    raise Exception("stock not enough, rollback")

                # insert order
                insert_order = "insert into `orders` (`id`, `book_id`, `user_id`, `quality`) values (%s, %s, %s, %s)"
                cursor.execute(insert_order, (order_id, book_id, user_id, amount))
                print(f'{txn_log_header} {insert_order} successful')

                # update user
                update_user = "update `users` set `balance` = `balance` - %s where id = %s"
                cursor.execute(update_user, (amount * price, user_id))
                print(f'{txn_log_header} {update_user} successful')

            except Exception as err:
                connection.rollback()

                print(f'something went wrong: {err}')
            else:
                # important here! you need deal the Exception from the TiDB
                try:
                    connection.commit()
                except MySQLdb.MySQLError as db_err:
                    code, desc = db_err.args
                    if code in REPEATABLE_ERROR_CODE_SET and optimistic_retry_times > 0:
                        print(f'retry, rest {optimistic_retry_times - 1} times, for {code} {desc}')
                        buy_optimistic(thread_id, order_id, book_id, user_id, amount, optimistic_retry_times - 1)


def buy_pessimistic(thread_id: int, order_id: int, book_id: int, user_id: int, amount: int) -> None:
    connection = create_connection()

    txn_log_header = f"/* txn {thread_id} */"
    if thread_id != 1:
        txn_log_header = "\t" + txn_log_header

    with connection:
        with connection.cursor() as cursor:
            cursor.execute("BEGIN PESSIMISTIC")
            print(f'{txn_log_header} BEGIN PESSIMISTIC')
            time.sleep(1)

            try:
                # read the price of book
                select_book_for_update = "SELECT `price` FROM books WHERE id = %s FOR UPDATE"
                cursor.execute(select_book_for_update, (book_id,))
                book = cursor.fetchone()
                if book is None:
                    raise Exception("book_id not exist")
                price = book[0]
                print(f'{txn_log_header} {select_book_for_update} successful')

                # update book
                update_stock = "update `books` set stock = stock - %s where id = %s and stock - %s >= 0"
                rows_affected = cursor.execute(update_stock, (amount, book_id, amount))
                print(f'{txn_log_header} {update_stock} successful')

                if rows_affected == 0:
                    raise Exception("stock not enough, rollback")

                # insert order
                insert_order = "insert into `orders` (`id`, `book_id`, `user_id`, `quality`) values (%s, %s, %s, %s)"
                cursor.execute(insert_order, (order_id, book_id, user_id, amount))
                print(f'{txn_log_header} {insert_order} successful')

                # update user
                update_user = "update `users` set `balance` = `balance` - %s where id = %s"
                cursor.execute(update_user, (amount * price, user_id))
                print(f'{txn_log_header} {update_user} successful')

            except Exception as err:
                connection.rollback()
                print(f'something went wrong: {err}')
            else:
                connection.commit()


optimistic = os.environ.get('OPTIMISTIC')
alice = os.environ.get('ALICE')
bob = os.environ.get('BOB')

if not (optimistic and alice and bob):
    raise Exception("please use \"OPTIMISTIC=<is_optimistic> ALICE=<alice_num> "
                    "BOB=<bob_num> python3 txn_example.py\" to start this script")

prepare_data()

if bool(optimistic) is True:
    buy_func = buy_optimistic
else:
    buy_func = buy_pessimistic

bob_thread = Thread(target=buy_func, kwargs={
    "thread_id": 1, "order_id": 1000, "book_id": 1, "user_id": 1, "amount": int(bob)})
alice_thread = Thread(target=buy_func, kwargs={
    "thread_id": 2, "order_id": 1001, "book_id": 1, "user_id": 2, "amount": int(alice)})

bob_thread.start()
alice_thread.start()
bob_thread.join(timeout=10)
alice_thread.join(timeout=10)
```

Python 的例子中，已经包含乐观事务。

</div>

</SimpleTab>

#### 2. 运行不涉及超卖的例子

运行示例程序：

<SimpleTab groupId="language">

<div label="Java" value="java">

在 Java 中运行示例程序：

```shell
mvn clean package
java -jar target/plain-java-txn-0.0.1-jar-with-dependencies.jar ALICE_NUM=4 BOB_NUM=6
```

</div>

<div label="Golang" value="golang">

在 Golang 中运行示例程序：

```shell
go build -o bin/txn
./bin/txn -a 4 -b 6
```

</div>

<div label="Python" value="python">

在 Python 中运行示例程序：

```shell
OPTIMISTIC=False ALICE=4 BOB=6 python3 txn_example.py
```

</div>

</SimpleTab>

SQL 日志：



```sql
/* txn 1 */ BEGIN PESSIMISTIC
    /* txn 2 */ BEGIN PESSIMISTIC
    /* txn 2 */ SELECT * FROM `books` WHERE `id` = 1 FOR UPDATE
    /* txn 2 */ UPDATE `books` SET `stock` = `stock` - 4 WHERE `id` = 1 AND `stock` - 4 >= 0
    /* txn 2 */ INSERT INTO `orders` (`id`, `book_id`, `user_id`, `quality`) VALUES (1001, 1, 1, 4)
    /* txn 2 */ UPDATE `users` SET `balance` = `balance` - 400.0 WHERE `id` = 2
    /* txn 2 */ COMMIT
/* txn 1 */ SELECT * FROM `books` WHERE `id` = 1 FOR UPDATE
/* txn 1 */ UPDATE `books` SET `stock` = `stock` - 6 WHERE `id` = 1 AND `stock` - 6 >= 0
/* txn 1 */ INSERT INTO `orders` (`id`, `book_id`, `user_id`, `quality`) VALUES (1000, 1, 1, 6)
/* txn 1 */ UPDATE `users` SET `balance` = `balance` - 600.0 WHERE `id` = 1
/* txn 1 */ COMMIT
```

最后，检验一下订单创建、用户余额扣减、图书库存扣减情况，都符合预期。

```sql
mysql> SELECT * FROM `books`;
+----+--------------------------------------+----------------------+---------------------+-------+--------+
| id | title                                | type                 | published_at        | stock | price  |
+----+--------------------------------------+----------------------+---------------------+-------+--------+
|  1 | Designing Data-Intensive Application | Science & Technology | 2018-09-01 00:00:00 |     0 | 100.00 |
+----+--------------------------------------+----------------------+---------------------+-------+--------+
1 row in set (0.00 sec)

mysql> SELECT * FROM orders;
+------+---------+---------+---------+---------------------+
| id   | book_id | user_id | quality | ordered_at          |
+------+---------+---------+---------+---------------------+
| 1000 |       1 |       1 |       6 | 2022-04-19 10:58:12 |
| 1001 |       1 |       1 |       4 | 2022-04-19 10:58:11 |
+------+---------+---------+---------+---------------------+
2 rows in set (0.01 sec)

mysql> SELECT * FROM users;
+----+---------+----------+
| id | balance | nickname |
+----+---------+----------+
|  1 | 9400.00 | Bob      |
|  2 | 9600.00 | Alice    |
+----+---------+----------+
2 rows in set (0.00 sec)
```

#### 3. 运行防止超卖的例子

可以再把难度加大，如果图书的库存剩余 10 本，Bob 购买 7 本， Alice 购买 4 本，两人几乎同时下单，结果会是怎样？继续复用上个例子里的代码来解决这个需求，只不过把 Bob 购买数量从 6 改成 7：

运行示例程序：

<SimpleTab groupId="language">

<div label="Java" value="java">

在 Java 中运行示例程序：

```shell
mvn clean package
java -jar target/plain-java-txn-0.0.1-jar-with-dependencies.jar ALICE_NUM=4 BOB_NUM=7
```

</div>

<div label="Golang" value="golang">

在 Golang 中运行示例程序：

```shell
go build -o bin/txn
./bin/txn -a 4 -b 7
```

</div>

<div label="Python" value="python">

在 Python 中运行示例程序：

```shell
OPTIMISTIC=False ALICE=4 BOB=7 python3 txn_example.py
```

</div>

</SimpleTab>



```sql
/* txn 1 */ BEGIN PESSIMISTIC
    /* txn 2 */ BEGIN PESSIMISTIC
    /* txn 2 */ SELECT * FROM `books` WHERE `id` = 1 FOR UPDATE
    /* txn 2 */ UPDATE `books` SET `stock` = `stock` - 4 WHERE `id` = 1 AND `stock` - 4 >= 0
    /* txn 2 */ INSERT INTO `orders` (`id`, `book_id`, `user_id`, `quality`) values (1001, 1, 1, 4)
    /* txn 2 */ UPDATE `users` SET `balance` = `balance` - 400.0 WHERE `id` = 2
    /* txn 2 */ COMMIT
/* txn 1 */ SELECT * FROM `books` WHERE `id` = 1 FOR UPDATE
/* txn 1 */ UPDATE `books` SET `stock` = `stock` - 7 WHERE `id` = 1 AND `stock` - 7 >= 0
/* txn 1 */ ROLLBACK
```

由于 `txn 2` 抢先获得锁资源，更新了 stock，`txn 1` 里面 `affected_rows` 返回值为 0，进入了 `rollback` 流程。

再检验一下订单创建、用户余额扣减、图书库存扣减情况。Alice 下单 4 本书成功，Bob 下单 7 本书失败，库存剩余 6 本符合预期。

```sql
mysql> SELECT * FROM books;
+----+--------------------------------------+----------------------+---------------------+-------+--------+
| id | title                                | type                 | published_at        | stock | price  |
+----+--------------------------------------+----------------------+---------------------+-------+--------+
|  1 | Designing Data-Intensive Application | Science & Technology | 2018-09-01 00:00:00 |     6 | 100.00 |
+----+--------------------------------------+----------------------+---------------------+-------+--------+
1 row in set (0.00 sec)

mysql> SELECT * FROM orders;
+------+---------+---------+---------+---------------------+
| id   | book_id | user_id | quality | ordered_at          |
+------+---------+---------+---------+---------------------+
| 1001 |       1 |       1 |       4 | 2022-04-19 11:03:03 |
+------+---------+---------+---------+---------------------+
1 row in set (0.00 sec)

mysql> SELECT * FROM users;
+----+----------+----------+
| id | balance  | nickname |
+----+----------+----------+
|  1 | 10000.00 | Bob      |
|  2 |  9600.00 | Alice    |
+----+----------+----------+
2 rows in set (0.01 sec)
```

### 乐观事务

下面代码以乐观事务的方式，用两个线程模拟了两个用户并发买同一本书的过程，和悲观事务的示例一样。书店剩余 10 本，Bob 购买了 6 本，Alice 购买了 4 本。两个人几乎同一时间完成订单，最终，这本书的剩余库存为零。

#### 1. 编写乐观事务示例

<SimpleTab groupId="language">

<div label="Java" value="java">

使用 Java 编写乐观事务示例：

**代码编写**



```java
package com.pingcap.txn.optimistic;

import com.zaxxer.hikari.HikariDataSource;

import java.math.BigDecimal;
import java.sql.*;
import java.util.Arrays;
import java.util.concurrent.*;

public class TxnExample {
    public static void main(String[] args) throws SQLException, InterruptedException {
        System.out.println(Arrays.toString(args));
        int aliceQuantity = 0;
        int bobQuantity = 0;

        for (String arg: args) {
            if (arg.startsWith("ALICE_NUM")) {
                aliceQuantity = Integer.parseInt(arg.replace("ALICE_NUM=", ""));
            }

            if (arg.startsWith("BOB_NUM")) {
                bobQuantity = Integer.parseInt(arg.replace("BOB_NUM=", ""));
            }
        }

        HikariDataSource ds = new HikariDataSource();
        ds.setJdbcUrl("jdbc:mysql://localhost:4000/bookshop?useServerPrepStmts=true&cachePrepStmts=true");
        ds.setUsername("root");
        ds.setPassword("");

        // prepare data
        Connection connection = ds.getConnection();
        createBook(connection, 1L, "Designing Data-Intensive Application", "Science & Technology",
                Timestamp.valueOf("2018-09-01 00:00:00"), new BigDecimal(100), 10);
        createUser(connection, 1L, "Bob", new BigDecimal(10000));
        createUser(connection, 2L, "Alice", new BigDecimal(10000));

        CountDownLatch countDownLatch = new CountDownLatch(2);
        ExecutorService threadPool = Executors.newFixedThreadPool(2);

        final int finalBobQuantity = bobQuantity;
        threadPool.execute(() -> {
            buy(ds, 1, 1000L, 1L, 1L, finalBobQuantity, 5);
            countDownLatch.countDown();
        });
        final int finalAliceQuantity = aliceQuantity;
        threadPool.execute(() -> {
            buy(ds, 2, 1001L, 1L, 2L, finalAliceQuantity, 5);
            countDownLatch.countDown();
        });

        countDownLatch.await(5, TimeUnit.SECONDS);
    }

    public static void createUser(Connection connection, Long id, String nickname, BigDecimal balance) throws SQLException  {
        PreparedStatement insert = connection.prepareStatement(
                "INSERT INTO `users` (`id`, `nickname`, `balance`) VALUES (?, ?, ?)");
        insert.setLong(1, id);
        insert.setString(2, nickname);
        insert.setBigDecimal(3, balance);
        insert.executeUpdate();
    }

    public static void createBook(Connection connection, Long id, String title, String type, Timestamp publishedAt, BigDecimal price, Integer stock) throws SQLException {
        PreparedStatement insert = connection.prepareStatement(
                "INSERT INTO `books` (`id`, `title`, `type`, `published_at`, `price`, `stock`) values (?, ?, ?, ?, ?, ?)");
        insert.setLong(1, id);
        insert.setString(2, title);
        insert.setString(3, type);
        insert.setTimestamp(4, publishedAt);
        insert.setBigDecimal(5, price);
        insert.setInt(6, stock);

        insert.executeUpdate();
    }

    public static void buy (HikariDataSource ds, Integer threadID, Long orderID, Long bookID,
                            Long userID, Integer quantity, Integer retryTimes) {
        String txnComment = "/* txn " + threadID + " */ ";

        try (Connection connection = ds.getConnection()) {
            try {

                connection.setAutoCommit(false);
                connection.createStatement().executeUpdate(txnComment + "begin optimistic");

                // waiting for other thread ran the 'begin optimistic' statement
                TimeUnit.SECONDS.sleep(1);

                BigDecimal price = null;

                // read price of book
                PreparedStatement selectBook = connection.prepareStatement(txnComment + "SELECT * FROM books where id = ? for update");
                selectBook.setLong(1, bookID);
                ResultSet res = selectBook.executeQuery();
                if (!res.next()) {
                    throw new RuntimeException("book not exist");
                } else {
                    price = res.getBigDecimal("price");
                    int stock = res.getInt("stock");
                    if (stock < quantity) {
                        throw new RuntimeException("book not enough");
                    }
                }

                // update book
                String updateBookSQL = "update `books` set stock = stock - ? where id = ? and stock - ? >= 0";
                PreparedStatement updateBook = connection.prepareStatement(txnComment + updateBookSQL);
                updateBook.setInt(1, quantity);
                updateBook.setLong(2, bookID);
                updateBook.setInt(3, quantity);
                updateBook.executeUpdate();

                // insert order
                String insertOrderSQL = "insert into `orders` (`id`, `book_id`, `user_id`, `quality`) values (?, ?, ?, ?)";
                PreparedStatement insertOrder = connection.prepareStatement(txnComment + insertOrderSQL);
                insertOrder.setLong(1, orderID);
                insertOrder.setLong(2, bookID);
                insertOrder.setLong(3, userID);
                insertOrder.setInt(4, quantity);
                insertOrder.executeUpdate();

                // update user
                String updateUserSQL = "update `users` set `balance` = `balance` - ? where id = ?";
                PreparedStatement updateUser = connection.prepareStatement(txnComment + updateUserSQL);
                updateUser.setBigDecimal(1, price.multiply(new BigDecimal(quantity)));
                updateUser.setLong(2, userID);
                updateUser.executeUpdate();

                connection.createStatement().executeUpdate(txnComment + "commit");
            } catch (Exception e) {
                connection.createStatement().executeUpdate(txnComment + "rollback");
                System.out.println("error occurred: " + e.getMessage());

                if (e instanceof SQLException sqlException) {
                    switch (sqlException.getErrorCode()) {
                        // You can get all error codes at https://docs.pingcap.com/tidb/stable/error-codes
                        case 9007: // Transactions in TiKV encounter write conflicts.
                        case 8028: // table schema changes
                        case 8002: // "SELECT FOR UPDATE" commit conflict
                        case 8022: // The transaction commit fails and has been rolled back
                            if (retryTimes != 0) {
                                System.out.println("rest " + retryTimes + " times. retry for " + e.getMessage());
                                buy(ds, threadID, orderID, bookID, userID, quantity, retryTimes - 1);
                            }
                    }
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

**配置更改**

此处，需将 `pom.xml` 中启动类：



```xml
<mainClass>com.pingcap.txn.TxnExample</mainClass>
```

更改为：



```xml
<mainClass>com.pingcap.txn.optimistic.TxnExample</mainClass>
```

来指向乐观事务的例子。

</div>

<div label="Golang" value="golang">

Golang 在[编写悲观事务示例](#1-编写悲观事务示例)章节中的例子已经支持了乐观事务，无需更改，可直接使用。

</div>

<div label="Python" value="python">

Python 在[编写悲观事务示例](#1-编写悲观事务示例)章节中的例子已经支持了乐观事务，无需更改，可直接使用。

</div>

</SimpleTab>

#### 2. 运行不涉及超卖的例子

运行示例程序：

<SimpleTab groupId="language">

<div label="Java" value="java">

在 Java 中运行示例程序：

```shell
mvn clean package
java -jar target/plain-java-txn-0.0.1-jar-with-dependencies.jar ALICE_NUM=4 BOB_NUM=6
```

</div>

<div label="Golang" value="golang">

在 Golang 中运行示例程序：

```shell
go build -o bin/txn
./bin/txn -a 4 -b 6 -o true
```

</div>

<div label="Python" value="python">

在 Python 中运行示例程序：

```shell
OPTIMISTIC=True ALICE=4 BOB=6 python3 txn_example.py
```

</div>

</SimpleTab>

SQL 语句执行过程：



```sql
    /* txn 2 */ BEGIN OPTIMISTIC
/* txn 1 */ BEGIN OPTIMISTIC
    /* txn 2 */ SELECT * FROM `books` WHERE `id` = 1 FOR UPDATE
    /* txn 2 */ UPDATE `books` SET `stock` = `stock` - 4 WHERE `id` = 1 AND `stock` - 4 >= 0
    /* txn 2 */ INSERT INTO `orders` (`id`, `book_id`, `user_id`, `quality`) VALUES (1001, 1, 1, 4)
    /* txn 2 */ UPDATE `users` SET `balance` = `balance` - 400.0 WHERE `id` = 2
    /* txn 2 */ COMMIT
/* txn 1 */ SELECT * FROM `books` WHERE `id` = 1 for UPDATE
/* txn 1 */ UPDATE `books` SET `stock` = `stock` - 6 WHERE `id` = 1 AND `stock` - 6 >= 0
/* txn 1 */ INSERT INTO `orders` (`id`, `book_id`, `user_id`, `quality`) VALUES (1000, 1, 1, 6)
/* txn 1 */ UPDATE `users` SET `balance` = `balance` - 600.0 WHERE `id` = 1
retry 1 times for 9007 Write conflict, txnStartTS=432618733006225412, conflictStartTS=432618733006225411, conflictCommitTS=432618733006225414, key={tableID=126, handle=1} primary={tableID=114, indexID=1, indexValues={1, 1000, }} [try again later]
/* txn 1 */ BEGIN OPTIMISTIC
/* txn 1 */ SELECT * FROM `books` WHERE `id` = 1 FOR UPDATE
/* txn 1 */ UPDATE `books` SET `stock` = `stock` - 6 WHERE `id` = 1 AND `stock` - 6 >= 0
/* txn 1 */ INSERT INTO `orders` (`id`, `book_id`, `user_id`, `quality`) VALUES (1000, 1, 1, 6)
/* txn 1 */ UPDATE `users` SET `balance` = `balance` - 600.0 WHERE `id` = 1
/* txn 1 */ COMMIT
```

在乐观事务模式下，由于中间状态不一定正确，不能像悲观事务模式一样，通过 `affected_rows` 来判断某个语句是否执行成功。需要把事务看做一个整体，通过最终的 COMMIT 语句是否返回异常来判断当前事务是否发生写冲突。

从上面 SQL 日志可以看出，由于两个事务并发执行，并且对同一条记录做了修改，`txn 1` COMMIT 之后抛出了 `9007 Write conflict` 异常。对于乐观事务写冲突，在应用端可以进行安全的重试，重试一次之后提交成功，最终执行结果符合预期：

```sql
mysql> SELECT * FROM books;
+----+--------------------------------------+----------------------+---------------------+-------+--------+
| id | title                                | type                 | published_at        | stock | price  |
+----+--------------------------------------+----------------------+---------------------+-------+--------+
|  1 | Designing Data-Intensive Application | Science & Technology | 2018-09-01 00:00:00 |     0 | 100.00 |
+----+--------------------------------------+----------------------+---------------------+-------+--------+
1 row in set (0.01 sec)

mysql> SELECT * FROM orders;
+------+---------+---------+---------+---------------------+
| id   | book_id | user_id | quality | ordered_at          |
+------+---------+---------+---------+---------------------+
| 1000 |       1 |       1 |       6 | 2022-04-19 03:18:19 |
| 1001 |       1 |       1 |       4 | 2022-04-19 03:18:17 |
+------+---------+---------+---------+---------------------+
2 rows in set (0.01 sec)

mysql> SELECT * FROM users;
+----+---------+----------+
| id | balance | nickname |
+----+---------+----------+
|  1 | 9400.00 | Bob      |
|  2 | 9600.00 | Alice    |
+----+---------+----------+
2 rows in set (0.00 sec)
```

#### 3. 运行防止超卖的例子

再来看一下用乐观事务防止超卖的例子，如果图书的库存剩余 10 本，Bob 购买 7 本， Alice 购买 4 本，两人几乎同时下单，结果会是怎样？继续复用乐观事务例子里的代码来解决这个需求，只不过把 Bob 购买数量从 6 改成 7：

运行示例程序：

<SimpleTab groupId="language">

<div label="Java" value="java">

在 Java 中运行示例程序：

```shell
mvn clean package
java -jar target/plain-java-txn-0.0.1-jar-with-dependencies.jar ALICE_NUM=4 BOB_NUM=7
```

</div>

<div label="Golang" value="golang">

在 Golang 中运行示例程序：

```shell
go build -o bin/txn
./bin/txn -a 4 -b 7 -o true
```

</div>

<div label="Python" value="python">

在 Python 中运行示例程序：

```shell
OPTIMISTIC=True ALICE=4 BOB=7 python3 txn_example.py
```

</div>

</SimpleTab>



```sql
/* txn 1 */ BEGIN OPTIMISTIC
    /* txn 2 */ BEGIN OPTIMISTIC
    /* txn 2 */ SELECT * FROM `books` WHERE `id` = 1 FOR UPDATE
    /* txn 2 */ UPDATE `books` SET `stock` = `stock` - 4 WHERE `id` = 1 AND `stock` - 4 >= 0
    /* txn 2 */ INSERT INTO `orders` (`id`, `book_id`, `user_id`, `quality`) VALUES (1001, 1, 1, 4)
    /* txn 2 */ UPDATE `users` SET `balance` = `balance` - 400.0 WHERE `id` = 2
    /* txn 2 */ COMMIT
/* txn 1 */ SELECT * FROM `books` WHERE `id` = 1 FOR UPDATE
/* txn 1 */ UPDATE `books` SET `stock` = `stock` - 7 WHERE `id` = 1 AND `stock` - 7 >= 0
/* txn 1 */ INSERT INTO `orders` (`id`, `book_id`, `user_id`, `quality`) VALUES (1000, 1, 1, 7)
/* txn 1 */ UPDATE `users` SET `balance` = `balance` - 700.0 WHERE `id` = 1
retry 1 times for 9007 Write conflict, txnStartTS=432619094333980675, conflictStartTS=432619094333980676, conflictCommitTS=432619094333980678, key={tableID=126, handle=1} primary={tableID=114, indexID=1, indexValues={1, 1000, }} [try again later]
/* txn 1 */ BEGIN OPTIMISTIC
/* txn 1 */ SELECT * FROM `books` WHERE `id` = 1 FOR UPDATE
Fail -> out of stock
/* txn 1 */ ROLLBACK
```

从上面的 SQL 日志可以看出，第一次执行由于写冲突，`txn 1` 在应用端进行了重试，从获取到的最新快照对比发现，剩余库存不够，应用端抛出 `out of stock` 异常结束。

```sql
mysql> SELECT * FROM books;
+----+--------------------------------------+----------------------+---------------------+-------+--------+
| id | title                                | type                 | published_at        | stock | price  |
+----+--------------------------------------+----------------------+---------------------+-------+--------+
|  1 | Designing Data-Intensive Application | Science & Technology | 2018-09-01 00:00:00 |     6 | 100.00 |
+----+--------------------------------------+----------------------+---------------------+-------+--------+
1 row in set (0.00 sec)

mysql> SELECT * FROM orders;
+------+---------+---------+---------+---------------------+
| id   | book_id | user_id | quality | ordered_at          |
+------+---------+---------+---------+---------------------+
| 1001 |       1 |       1 |       4 | 2022-04-19 03:41:16 |
+------+---------+---------+---------+---------------------+
1 row in set (0.00 sec)

mysql> SELECT * FROM users;
+----+----------+----------+
| id | balance  | nickname |
+----+----------+----------+
|  1 | 10000.00 | Bob      |
|  2 |  9600.00 | Alice    |
+----+----------+----------+
2 rows in set (0.00 sec)
```


---
title: 事务限制
summary: 介绍 TiDB 中的事务限制。
---

## 事务限制

本章将简单介绍 TiDB 中的事务限制。

### 隔离级别

TiDB 支持的隔离级别是 RC（Read Committed）与 SI（Snapshot Isolation），其中 SI 与 RR（Repeatable Read）隔离级别基本等价。

![隔离级别](./media/develop/transaction_isolation_level.png)

### SI 可以克服幻读

TiDB 的 SI 隔离级别可以克服幻读异常 (Phantom Reads)，但 ANSI/ISO SQL 标准 中的 RR 不能。

所谓幻读是指：事务 A 首先根据条件查询得到 n 条记录，然后事务 B 改变了这 n 条记录之外的 m 条记录或者增添了 m 条符合事务 A 查询条件的记录，导致事务 A 再次发起请求时发现有 n+m 条符合条件记录，就产生了幻读。

例如：系统管理员 A 将数据库中所有学生的成绩从具体分数改为 ABCDE 等级，但是系统管理员 B 就在这个时候插入了一条具体分数的记录，当系统管理员 A 改结束后发现还有一条记录没有改过来，就好像发生了幻觉一样，这就叫幻读。

### SI 不能克服写偏斜

TiDB 的 SI 隔离级别不能克服写偏斜异常（Write Skew），需要使用 Select for update 语法来克服写偏斜异常。

写偏斜异常是指两个并发的事务读取了不同但相关的记录，接着这两个事务各自更新了自己读到的数据，并最终都提交了事务，如果这些相关的记录之间存在着不能被多个事务并发修改的约束，那么最终结果将是违反约束的。

举个例子，假设你正在为医院写一个医生轮班管理程序。医院通常会同时要求几位医生待命，但底线是至少有一位医生在待命。医生可以放弃他们的班次（例如，如果他们自己生病了），只要至少有一个同事在这一班中继续工作。

现在出现这样一种情况，Alice 和 Bob 是两位值班医生。两人都感到不适，所以他们都决定请假。不幸的是，他们恰好在同一时间点击按钮下班。下面用程序来模拟一下这个过程。

<SimpleTab groupId="language">

<div label="Java" value="java">

Java 程序示例如下：

```java
package com.pingcap.txn.write.skew;

import com.zaxxer.hikari.HikariDataSource;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Semaphore;

public class EffectWriteSkew {
    public static void main(String[] args) throws SQLException, InterruptedException {
        HikariDataSource ds = new HikariDataSource();
        ds.setJdbcUrl("jdbc:mysql://localhost:4000/test?useServerPrepStmts=true&cachePrepStmts=true");
        ds.setUsername("root");

        // prepare data
        Connection connection = ds.getConnection();
        createDoctorTable(connection);
        createDoctor(connection, 1, "Alice", true, 123);
        createDoctor(connection, 2, "Bob", true, 123);
        createDoctor(connection, 3, "Carol", false, 123);

        Semaphore txn1Pass = new Semaphore(0);
        CountDownLatch countDownLatch = new CountDownLatch(2);
        ExecutorService threadPool = Executors.newFixedThreadPool(2);

        threadPool.execute(() -> {
            askForLeave(ds, txn1Pass, 1, 1);
            countDownLatch.countDown();
        });

        threadPool.execute(() -> {
            askForLeave(ds, txn1Pass, 2, 2);
            countDownLatch.countDown();
        });

        countDownLatch.await();
    }

    public static void createDoctorTable(Connection connection) throws SQLException {
        connection.createStatement().executeUpdate("CREATE TABLE `doctors` (" +
                "    `id` int(11) NOT NULL," +
                "    `name` varchar(255) DEFAULT NULL," +
                "    `on_call` tinyint(1) DEFAULT NULL," +
                "    `shift_id` int(11) DEFAULT NULL," +
                "    PRIMARY KEY (`id`)," +
                "    KEY `idx_shift_id` (`shift_id`)" +
                "  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin");
    }

    public static void createDoctor(Connection connection, Integer id, String name, Boolean onCall, Integer shiftID) throws SQLException {
        PreparedStatement insert = connection.prepareStatement(
                "INSERT INTO `doctors` (`id`, `name`, `on_call`, `shift_id`) VALUES (?, ?, ?, ?)");
        insert.setInt(1, id);
        insert.setString(2, name);
        insert.setBoolean(3, onCall);
        insert.setInt(4, shiftID);
        insert.executeUpdate();
    }

    public static void askForLeave(HikariDataSource ds, Semaphore txn1Pass, Integer txnID, Integer doctorID) {
        try(Connection connection = ds.getConnection()) {
            try {
                connection.setAutoCommit(false);

                String comment = txnID == 2 ? "    " : "" + "/* txn #{txn_id} */ ";
                connection.createStatement().executeUpdate(comment + "BEGIN");

                // Txn 1 should be waiting until txn 2 is done.
                if (txnID == 1) {
                    txn1Pass.acquire();
                }

                PreparedStatement currentOnCallQuery = connection.prepareStatement(comment +
                        "SELECT COUNT(*) AS `count` FROM `doctors` WHERE `on_call` = ? AND `shift_id` = ?");
                currentOnCallQuery.setBoolean(1, true);
                currentOnCallQuery.setInt(2, 123);
                ResultSet res = currentOnCallQuery.executeQuery();

                if (!res.next()) {
                    throw new RuntimeException("error query");
                } else {
                    int count = res.getInt("count");
                    if (count >= 2) {
                        // If current on-call doctor has 2 or more, this doctor can leave
                        PreparedStatement insert = connection.prepareStatement( comment +
                                "UPDATE `doctors` SET `on_call` = ? WHERE `id` = ? AND `shift_id` = ?");
                        insert.setBoolean(1, false);
                        insert.setInt(2, doctorID);
                        insert.setInt(3, 123);
                        insert.executeUpdate();

                        connection.commit();
                    } else {
                        throw new RuntimeException("At least one doctor is on call");
                    }
                }

                // Txn 2 is done. Let txn 1 run again.
                if (txnID == 2) {
                    txn1Pass.release();
                }
            } catch (Exception e) {
                // If got any error, you should roll back, data is priceless
                connection.rollback();
                e.printStackTrace();
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

</div>

<div label="Golang" value="golang">

在 Golang 中，首先，封装一个用于适配 TiDB 事务的工具包 [util](https://github.com/pingcap-inc/tidb-example-golang/tree/main/util)，随后编写以下代码：



```go
package main

import (
    "database/sql"
    "fmt"
    "sync"

    "github.com/pingcap-inc/tidb-example-golang/util"

    _ "github.com/go-sql-driver/mysql"
)

func main() {
    openDB("mysql", "root:@tcp(127.0.0.1:4000)/test", func(db *sql.DB) {
        writeSkew(db)
    })
}

func openDB(driverName, dataSourceName string, runnable func(db *sql.DB)) {
    db, err := sql.Open(driverName, dataSourceName)
    if err != nil {
        panic(err)
    }
    defer db.Close()

    runnable(db)
}

func writeSkew(db *sql.DB) {
    err := prepareData(db)
    if err != nil {
        panic(err)
    }

    waitingChan, waitGroup := make(chan bool), sync.WaitGroup{}

    waitGroup.Add(1)
    go func() {
        defer waitGroup.Done()
        err = askForLeave(db, waitingChan, 1, 1)
        if err != nil {
            panic(err)
        }
    }()

    waitGroup.Add(1)
    go func() {
        defer waitGroup.Done()
        err = askForLeave(db, waitingChan, 2, 2)
        if err != nil {
            panic(err)
        }
    }()

    waitGroup.Wait()
}

func askForLeave(db *sql.DB, waitingChan chan bool, goroutineID, doctorID int) error {
    txnComment := fmt.Sprintf("/* txn %d */ ", goroutineID)
    if goroutineID != 1 {
        txnComment = "\t" + txnComment
    }

    txn, err := util.TiDBSqlBegin(db, true)
    if err != nil {
        return err
    }
    fmt.Println(txnComment + "start txn")

    // Txn 1 should be waiting until txn 2 is done.
    if goroutineID == 1 {
        <-waitingChan
    }

    txnFunc := func() error {
        queryCurrentOnCall := "SELECT COUNT(*) AS `count` FROM `doctors` WHERE `on_call` = ? AND `shift_id` = ?"
        rows, err := txn.Query(queryCurrentOnCall, true, 123)
        if err != nil {
            return err
        }
        defer rows.Close()
        fmt.Println(txnComment + queryCurrentOnCall + " successful")

        count := 0
        if rows.Next() {
            err = rows.Scan(&count)
            if err != nil {
                return err
            }
        }
        rows.Close()

        if count < 2 {
            return fmt.Errorf("at least one doctor is on call")
        }

        shift := "UPDATE `doctors` SET `on_call` = ? WHERE `id` = ? AND `shift_id` = ?"
        _, err = txn.Exec(shift, false, doctorID, 123)
        if err == nil {
            fmt.Println(txnComment + shift + " successful")
        }
        return err
    }

    err = txnFunc()
    if err == nil {
        txn.Commit()
        fmt.Println("[runTxn] commit success")
    } else {
        txn.Rollback()
        fmt.Printf("[runTxn] got an error, rollback: %+v\n", err)
    }

    // Txn 2 is done. Let txn 1 run again.
    if goroutineID == 2 {
        waitingChan <- true
    }

    return nil
}

func prepareData(db *sql.DB) error {
    err := createDoctorTable(db)
    if err != nil {
        return err
    }

    err = createDoctor(db, 1, "Alice", true, 123)
    if err != nil {
        return err
    }
    err = createDoctor(db, 2, "Bob", true, 123)
    if err != nil {
        return err
    }
    err = createDoctor(db, 3, "Carol", false, 123)
    if err != nil {
        return err
    }
    return nil
}

func createDoctorTable(db *sql.DB) error {
    _, err := db.Exec("CREATE TABLE IF NOT EXISTS `doctors` (" +
        "    `id` int(11) NOT NULL," +
        "    `name` varchar(255) DEFAULT NULL," +
        "    `on_call` tinyint(1) DEFAULT NULL," +
        "    `shift_id` int(11) DEFAULT NULL," +
        "    PRIMARY KEY (`id`)," +
        "    KEY `idx_shift_id` (`shift_id`)" +
        "  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin")
    return err
}

func createDoctor(db *sql.DB, id int, name string, onCall bool, shiftID int) error {
    _, err := db.Exec("INSERT INTO `doctors` (`id`, `name`, `on_call`, `shift_id`) VALUES (?, ?, ?, ?)",
        id, name, onCall, shiftID)
    return err
}
```

</div>

</SimpleTab>

SQL 日志：



```sql
/* txn 1 */ BEGIN
    /* txn 2 */ BEGIN
    /* txn 2 */ SELECT COUNT(*) as `count` FROM `doctors` WHERE `on_call` = 1 AND `shift_id` = 123
    /* txn 2 */ UPDATE `doctors` SET `on_call` = 0 WHERE `id` = 2 AND `shift_id` = 123
    /* txn 2 */ COMMIT
/* txn 1 */ SELECT COUNT(*) AS `count` FROM `doctors` WHERE `on_call` = 1 and `shift_id` = 123
/* txn 1 */ UPDATE `doctors` SET `on_call` = 0 WHERE `id` = 1 AND `shift_id` = 123
/* txn 1 */ COMMIT
```

执行结果：



```sql
mysql> SELECT * FROM doctors;
+----+-------+---------+----------+
| id | name  | on_call | shift_id |
+----+-------+---------+----------+
|  1 | Alice |       0 |      123 |
|  2 | Bob   |       0 |      123 |
|  3 | Carol |       0 |      123 |
+----+-------+---------+----------+
```

在两个事务中，应用首先检查是否有两个或以上的医生正在值班；如果是的话，它就假定一名医生可以安全地休班。由于数据库使用快照隔离，两次检查都返回 2 ，所以两个事务都进入下一个阶段。Alice 更新自己的记录休班了，而 Bob 也做了一样的事情。两个事务都成功提交了，现在没有医生值班了。违反了至少有一名医生在值班的要求。下图(引用自《Designing Data-Intensive Application》)说明了实际发生的情况：

![Write Skew](./media/develop/write-skew.png)

现在更改示例程序，使用 `SELECT FOR UPDATE` 来克服写偏斜问题：

<SimpleTab groupId="language">

<div label="Java" value="java">

Java 中使用 `SELECT FOR UPDATE` 来克服写偏斜问题的示例如下：

```java
package com.pingcap.txn.write.skew;

import com.zaxxer.hikari.HikariDataSource;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Semaphore;

public class EffectWriteSkew {
    public static void main(String[] args) throws SQLException, InterruptedException {
        HikariDataSource ds = new HikariDataSource();
        ds.setJdbcUrl("jdbc:mysql://localhost:4000/test?useServerPrepStmts=true&cachePrepStmts=true");
        ds.setUsername("root");

        // prepare data
        Connection connection = ds.getConnection();
        createDoctorTable(connection);
        createDoctor(connection, 1, "Alice", true, 123);
        createDoctor(connection, 2, "Bob", true, 123);
        createDoctor(connection, 3, "Carol", false, 123);

        Semaphore txn1Pass = new Semaphore(0);
        CountDownLatch countDownLatch = new CountDownLatch(2);
        ExecutorService threadPool = Executors.newFixedThreadPool(2);

        threadPool.execute(() -> {
            askForLeave(ds, txn1Pass, 1, 1);
            countDownLatch.countDown();
        });

        threadPool.execute(() -> {
            askForLeave(ds, txn1Pass, 2, 2);
            countDownLatch.countDown();
        });

        countDownLatch.await();
    }

    public static void createDoctorTable(Connection connection) throws SQLException {
        connection.createStatement().executeUpdate("CREATE TABLE `doctors` (" +
                "    `id` int(11) NOT NULL," +
                "    `name` varchar(255) DEFAULT NULL," +
                "    `on_call` tinyint(1) DEFAULT NULL," +
                "    `shift_id` int(11) DEFAULT NULL," +
                "    PRIMARY KEY (`id`)," +
                "    KEY `idx_shift_id` (`shift_id`)" +
                "  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin");
    }

    public static void createDoctor(Connection connection, Integer id, String name, Boolean onCall, Integer shiftID) throws SQLException {
        PreparedStatement insert = connection.prepareStatement(
                "INSERT INTO `doctors` (`id`, `name`, `on_call`, `shift_id`) VALUES (?, ?, ?, ?)");
        insert.setInt(1, id);
        insert.setString(2, name);
        insert.setBoolean(3, onCall);
        insert.setInt(4, shiftID);
        insert.executeUpdate();
    }

    public static void askForLeave(HikariDataSource ds, Semaphore txn1Pass, Integer txnID, Integer doctorID) {
        try(Connection connection = ds.getConnection()) {
            try {
                connection.setAutoCommit(false);

                String comment = txnID == 2 ? "    " : "" + "/* txn #{txn_id} */ ";
                connection.createStatement().executeUpdate(comment + "BEGIN");

                // Txn 1 should be waiting until txn 2 is done.
                if (txnID == 1) {
                    txn1Pass.acquire();
                }

                PreparedStatement currentOnCallQuery = connection.prepareStatement(comment +
                        "SELECT COUNT(*) AS `count` FROM `doctors` WHERE `on_call` = ? AND `shift_id` = ? FOR UPDATE");
                currentOnCallQuery.setBoolean(1, true);
                currentOnCallQuery.setInt(2, 123);
                ResultSet res = currentOnCallQuery.executeQuery();

                if (!res.next()) {
                    throw new RuntimeException("error query");
                } else {
                    int count = res.getInt("count");
                    if (count >= 2) {
                        // If current on-call doctor has 2 or more, this doctor can leave
                        PreparedStatement insert = connection.prepareStatement( comment +
                                "UPDATE `doctors` SET `on_call` = ? WHERE `id` = ? AND `shift_id` = ?");
                        insert.setBoolean(1, false);
                        insert.setInt(2, doctorID);
                        insert.setInt(3, 123);
                        insert.executeUpdate();

                        connection.commit();
                    } else {
                        throw new RuntimeException("At least one doctor is on call");
                    }
                }

                // Txn 2 is done. Let txn 1 run again.
                if (txnID == 2) {
                    txn1Pass.release();
                }
            } catch (Exception e) {
                // If got any error, you should roll back, data is priceless
                connection.rollback();
                e.printStackTrace();
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

</div>

<div label="Golang" value="golang">

Golang 中使用 `SELECT FOR UPDATE` 来克服写偏斜问题的示例如下：

```go
package main

import (
    "database/sql"
    "fmt"
    "sync"

    "github.com/pingcap-inc/tidb-example-golang/util"

    _ "github.com/go-sql-driver/mysql"
)

func main() {
    openDB("mysql", "root:@tcp(127.0.0.1:4000)/test", func(db *sql.DB) {
        writeSkew(db)
    })
}

func openDB(driverName, dataSourceName string, runnable func(db *sql.DB)) {
    db, err := sql.Open(driverName, dataSourceName)
    if err != nil {
        panic(err)
    }
    defer db.Close()

    runnable(db)
}

func writeSkew(db *sql.DB) {
    err := prepareData(db)
    if err != nil {
        panic(err)
    }

    waitingChan, waitGroup := make(chan bool), sync.WaitGroup{}

    waitGroup.Add(1)
    go func() {
        defer waitGroup.Done()
        err = askForLeave(db, waitingChan, 1, 1)
        if err != nil {
            panic(err)
        }
    }()

    waitGroup.Add(1)
    go func() {
        defer waitGroup.Done()
        err = askForLeave(db, waitingChan, 2, 2)
        if err != nil {
            panic(err)
        }
    }()

    waitGroup.Wait()
}

func askForLeave(db *sql.DB, waitingChan chan bool, goroutineID, doctorID int) error {
    txnComment := fmt.Sprintf("/* txn %d */ ", goroutineID)
    if goroutineID != 1 {
        txnComment = "\t" + txnComment
    }

    txn, err := util.TiDBSqlBegin(db, true)
    if err != nil {
        return err
    }
    fmt.Println(txnComment + "start txn")

    // Txn 1 should be waiting until txn 2 is done.
    if goroutineID == 1 {
        <-waitingChan
    }

    txnFunc := func() error {
        queryCurrentOnCall := "SELECT COUNT(*) AS `count` FROM `doctors` WHERE `on_call` = ? AND `shift_id` = ?"
        rows, err := txn.Query(queryCurrentOnCall, true, 123)
        if err != nil {
            return err
        }
        defer rows.Close()
        fmt.Println(txnComment + queryCurrentOnCall + " successful")

        count := 0
        if rows.Next() {
            err = rows.Scan(&count)
            if err != nil {
                return err
            }
        }
        rows.Close()

        if count < 2 {
            return fmt.Errorf("at least one doctor is on call")
        }

        shift := "UPDATE `doctors` SET `on_call` = ? WHERE `id` = ? AND `shift_id` = ?"
        _, err = txn.Exec(shift, false, doctorID, 123)
        if err == nil {
            fmt.Println(txnComment + shift + " successful")
        }
        return err
    }

    err = txnFunc()
    if err == nil {
        txn.Commit()
        fmt.Println("[runTxn] commit success")
    } else {
        txn.Rollback()
        fmt.Printf("[runTxn] got an error, rollback: %+v\n", err)
    }

    // Txn 2 is done. Let txn 1 run again.
    if goroutineID == 2 {
        waitingChan <- true
    }

    return nil
}

func prepareData(db *sql.DB) error {
    err := createDoctorTable(db)
    if err != nil {
        return err
    }

    err = createDoctor(db, 1, "Alice", true, 123)
    if err != nil {
        return err
    }
    err = createDoctor(db, 2, "Bob", true, 123)
    if err != nil {
        return err
    }
    err = createDoctor(db, 3, "Carol", false, 123)
    if err != nil {
        return err
    }
    return nil
}

func createDoctorTable(db *sql.DB) error {
    _, err := db.Exec("CREATE TABLE IF NOT EXISTS `doctors` (" +
        "    `id` int(11) NOT NULL," +
        "    `name` varchar(255) DEFAULT NULL," +
        "    `on_call` tinyint(1) DEFAULT NULL," +
        "    `shift_id` int(11) DEFAULT NULL," +
        "    PRIMARY KEY (`id`)," +
        "    KEY `idx_shift_id` (`shift_id`)" +
        "  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin")
    return err
}

func createDoctor(db *sql.DB, id int, name string, onCall bool, shiftID int) error {
    _, err := db.Exec("INSERT INTO `doctors` (`id`, `name`, `on_call`, `shift_id`) VALUES (?, ?, ?, ?)",
        id, name, onCall, shiftID)
    return err
}
```

</div>

</SimpleTab>

SQL 日志：



```sql
/* txn 1 */ BEGIN
    /* txn 2 */ BEGIN
    /* txn 2 */ SELECT COUNT(*) AS `count` FROM `doctors` WHERE on_call = 1 AND `shift_id` = 123 FOR UPDATE
    /* txn 2 */ UPDATE `doctors` SET on_call = 0 WHERE `id` = 2 AND `shift_id` = 123
    /* txn 2 */ COMMIT
/* txn 1 */ SELECT COUNT(*) AS `count` FROM `doctors` WHERE `on_call` = 1 FOR UPDATE
At least one doctor is on call
/* txn 1 */ ROLLBACK
```

执行结果：



```sql
mysql> SELECT * FROM doctors;
+----+-------+---------+----------+
| id | name  | on_call | shift_id |
+----+-------+---------+----------+
|  1 | Alice |       1 |      123 |
|  2 | Bob   |       0 |      123 |
|  3 | Carol |       0 |      123 |
+----+-------+---------+----------+
```

### 对 savepoint 和嵌套事务的支持

Spring 支持的 PROPAGATION_NESTED 传播行为会启动一个嵌套的事务，它是当前事务之上独立启动的一个子事务。嵌套事务开始时会记录一个 savepoint ，如果嵌套事务执行失败，事务将会回滚到 savepoint 的状态。嵌套事务是外层事务的一部分，它将会在外层事务提交时一起被提交。下面案例展示了 savepoint 机制：



```sql
mysql> BEGIN;
mysql> INSERT INTO T2 VALUES(100);
mysql> SAVEPOINT svp1;
mysql> INSERT INTO T2 VALUES(200);
mysql> ROLLBACK TO SAVEPOINT svp1;
mysql> RELEASE SAVEPOINT svp1;
mysql> COMMIT;
mysql> SELECT * FROM T2;
+------+
|  ID   |
+------+
|  100 |
+------+
```

> **注意：**
>
> TiDB 从 v6.2.0 版本开始支持 savepoint 特性。因此低于 v6.2.0 版本的 TiDB 不支持 `PROPAGATION_NESTED` 传播行为。基于 Java Spring 框架的应用如果使用了 `PROPAGATION_NESTED` 传播行为，需要在应用端做出调整，将嵌套事务的逻辑移除。

### 大事务限制

基本原则是要限制事务的大小。TiDB 对单个事务的大小有限制，这层限制是在 KV 层面。反映在 SQL 层面的话，简单来说一行数据会映射为一个 KV entry，每多一个索引，也会增加一个 KV entry。所以这个限制反映在 SQL 层面是：

- 最大单行记录容量为 120MB（TiDB v5.0 及更高的版本可通过 tidb-server 配置项 `performance.txn-entry-size-limit` 调整，低于 TiDB v5.0 的版本支持的单行容量为 6MB）。
- 支持的最大单个事务容量为 10GB（TiDB v4.0 及更高版本可通过 tidb-server 配置项 `performance.txn-total-size-limit` 调整，低于 TiDB v4.0 的版本支持的最大单个事务容量为 100MB）。

另外注意，无论是大小限制还是行数限制，还要考虑事务执行过程中，TiDB 做编码以及事务额外 Key 的开销。在使用的时候，为了使性能达到最优，建议每 100 ～ 500 行写入一个事务。

### 自动提交的 SELECT FOR UPDATE 语句不会等锁

自动提交下的 SELECT FOR UPDATE 目前不会加锁。效果如下图所示：

![TiDB中的情况](./media/develop/autocommit_selectforupdate_nowaitlock.png)

这是已知的与 MySQL 不兼容的地方。

可以通过使用显式的 `BEGIN;COMMIT;` 解决该问题。


---
title: 事务错误处理
summary: 介绍 TiDB 中的事务错误处理办法。
---

## 事务错误处理

本章介绍使用事务时可能会遇到的错误和处理办法。

### 死锁

如果应用程序遇到下面错误时，说明遇到了死锁问题：



```sql
ERROR 1213: Deadlock found when trying to get lock; try restarting transaction
```

当两个及以上的事务，双方都在等待对方释放已经持有的锁或因为加锁顺序不一致，造成循环等待锁资源，就会出现“死锁”。这里以 [bookshop](#bookshop-应用) 数据库中的 `books` 表为示例演示死锁：

先给 `books` 表中写入 2 条数据：



```sql
INSERT INTO books (id, title, stock, published_at) VALUES (1, 'book-1', 10, now()), (2, 'book-2', 10, now());
```

在 TiDB 悲观事务模式下，用 2 个客户端分别执行以下语句，就会遇到死锁：

| 客户端-A                                                   | 客户端-B                                                         |
| ---------------------------------------------------------- | ---------------------------------------------------------------- |
| BEGIN;                                                     |                                                                  |
|                                                            | BEGIN;                                                           |
| UPDATE books SET stock=stock-1 WHERE id=1;                 |                                                                  |
|                                                            | UPDATE books SET stock=stock-1 WHERE id=2;                       |
| UPDATE books SET stock=stock-1 WHERE id=2; -- 执行会被阻塞 |                                                                  |
|                                                            | UPDATE books SET stock=stock-1 WHERE id=1; -- 遇到 Deadlock 错误 |

在客户端-B 遇到死锁错误后，TiDB 会自动 `ROLLBACK` 客户端-B 中的事务，然后客户端-A 中购买 `id=2` 的操作就会执行成功，再执行 `COMMIT` 即可完成购买的事务流程。

#### 解决方案 1：避免死锁

为了应用程序有更好的性能，可以通过调整业务逻辑或者 Schema 设计，尽量从应用层面避免死锁。例如上面示例中，如果客户端-B 也和客户端-A 用同样的购买顺序，即都先买 `id=1` 的书，再买 `id=2` 的书，就可以避免死锁了：

| 客户端-A                                   | 客户端-B                                                                              |
| ------------------------------------------ | ------------------------------------------------------------------------------------- |
| BEGIN;                                     |                                                                                       |
|                                            | BEGIN;                                                                                |
| UPDATE books SET stock=stock-1 WHERE id=1; |                                                                                       |
|                                            | UPDATE books SET stock=stock-1 WHERE id=1; -- 执行会被阻塞，当事务 A 完成后再继续执行 |
| UPDATE books SET stock=stock-1 WHERE id=2; |                                                                                       |
|                                            | UPDATE books SET stock=stock-1 WHERE id=2;                                            |
| COMMIT;                                    |                                                                                       |
|                                            | COMMIT;                                                                               |

或者直接用 1 条 SQL 购买 2 本书，也能避免死锁，而且执行效率更高：



```sql
UPDATE books SET stock=stock-1 WHERE id IN (1, 2);
```

#### 解决方案 2：减小事务粒度

如果每次购书都是一个单独的事务，也能避免死锁。但需要权衡的是，事务粒度太小不符合性能上的最佳实践。

#### 解决方案 3：使用乐观事务

乐观事务模型下，并不会有死锁问题，但应用端需要加上乐观事务在失败后的重试逻辑，具体重试逻辑见 [应用端重试和错误处理](#应用端重试和错误处理)。

#### 解决方案 4：重试

正如错误信息中提示的那样，在应用代码中加入重试逻辑即可。具体重试逻辑见 [应用端重试和错误处理](#应用端重试和错误处理)。

### 应用端重试和错误处理

尽管 TiDB 尽可能地与 MySQL 兼容，但其分布式系统的性质导致了某些差异，其中之一就是事务模型。

开发者用来与数据库通信的 Adapter 和 ORM 都是为 MySQL 和 Oracle 等传统数据库量身定制的，在这些数据库中，提交很少在默认隔离级别失败，因此不需要重试机制。对于这些客户端，当提交失败时，它们会因错误而中止，因为这在这些数据库中被呈现为罕见的异常。

与 MySQL 等传统数据库不同的是，在 TiDB 中，如果采用乐观事务模型，想要避免提交失败，需要在自己的应用程序的业务逻辑中添加机制来处理相关的异常。

下面的类似 Python 的伪代码展示了如何实现应用程序级的重试。 它不要求您的驱动程序或 ORM 来实现高级重试处理逻辑，因此可以在任何编程语言或环境中使用。

特别是，您的重试逻辑必须：

- 如果失败重试的次数达到 `max_retries` 限制，则抛出错误
- 使用 `try ... catch ...` 语句捕获 SQL 执行异常，当遇到下面这些错误时进行失败重试，遇到其它错误则进行回滚。详细信息请参考：[错误码与故障诊断](https://docs.pingcap.com/tidb/stable/error-codes)。
    - `Error 8002: can not retry select for update statement`：SELECT FOR UPDATE 写入冲突报错。
    - `Error 8022: Error: KV error safe to retry`：事务提交失败报错。
    - `Error 8028: Information schema is changed during the execution of the statement`：表的 Schema 结构因为完成了 DDL 变更，导致事务提交时报错。
    - `Error 9007: Write conflict`：写冲突报错，一般是采用乐观事务模式时，多个事务都对同一行数据进行修改时遇到的写冲突报错。
- 在 try 块结束时使用 COMMIT 提交事务：

```python
while True:
    n++
    if n == max_retries:
        raise("did not succeed within #{n} retries")
    try:
        connection.execute("your sql statement here")
        connection.exec('COMMIT')
        break
    catch error:
        if (error.code != "9007" && error.code != "8028" && error.code != "8002" && error.code != "8022"):
            raise error
        else:
            connection.exec('ROLLBACK')

            # Capture the error types that require application-side retry,
            # wait for a short period of time,
            # and exponentially increase the wait time for each transaction failure
            sleep_ms = int(((1.5 ** n) + rand) * 100)
            sleep(sleep_ms) # make sure your sleep() takes milliseconds
```

> **注意：**
>
> 如果你经常遇到 `Error 9007: Write conflict` 错误，你可能需要进一步评估你的 Schema 设计和数据存取模型，找到冲突的根源并从设计上避免冲突。
> 关于如何定位和解决事务冲突，请参考TiDB 锁冲突问题处理。

### 推荐阅读

- TiDB 锁冲突问题处理
- 乐观事务模型下写写冲突问题排查



# 优化 SQL 性能

---
title: 概览
summary: 介绍 TiDB 的 SQL 性能调优概览。
---

## 概览

本章内容描述了如何在 TiDB 中优化 SQL 语句的性能。为了获得更好的性能，你可以从以下方面入手：

- SQL 性能调优。
- Schema 设计：根据你的业务负载类型，为了避免事务冲突或者是热点，你可能需要对表的 Schema 做出一些调整。

### SQL 性能调优

为了让 SQL 语句的性能更好，可以遵循以下原则：

- 扫描的数据越少越好，最好能只扫描需要的数据，避免扫描多余的数据。
- 使用合适的索引，对于 SQL 中的 `WHERE` 子句中的 Column，需要保证有相应索引，否则这将是一个全表扫的语句，性能会很差。
- 使用合适的 Join 类型。根据查询中各个表的大小和关联性，选择合适的 Join 类型也会非常重要。一般情况下，TiDB 的 cost-based 优化器会自动选择最优的 Join 类型。但在少数情况下，用户手动指定 Join 类型可能会更好。
- 使用合适的存储引擎。对于 OLTP 和 OLAP 混合类型的负载，推荐使用 TiFlash 查询引擎，具体可以参考 [HTAP 查询](#htap-查询)。

### Schema 设计

如果根据[SQL 性能调优](#sql-性能调优)调优后任然无法获得较好的性能，你可能需要检查你的 Schema 设计和数据读取模型，来确保避免以下问题：

- 事务冲突。关于如何定位和解决事务冲突，请参考TiDB 锁冲突问题处理。
- 热点。关于如何定位和解决热点，请参考TiDB 热点问题处理。

### 推荐阅读

- SQL 性能调优。


---
title: SQL 性能调优
summary: 介绍 TiDB 的 SQL 性能调优方案和分析办法。
---

## SQL 性能调优

本章介绍常见的 SQL 性能调优，你将会了解导致 SQL 执行慢的常见的原因。

### 准备工作

在开始之前，你可以[通过 `tiup demo` 命令导入](#方法一通过-tiup-demo-命令行)示例数据：



```shell
tiup demo bookshop prepare --books 1000000 --host 127.0.0.1 --port 4000
```

或[使用 TiDB Cloud 的 Import 功能导入](#方法二通过-tidb-cloud-import-功能)预先准备好的示例数据。

### 问题：全表扫描

慢查询最常见的原因就是 `SELECT` 语句执行是全表扫描，或者是用了不合适的索引。

当基于不在主键或任何二级索引中的列从大表中检索少量行时，通常会获得较差的性能：



```sql
SELECT * FROM books WHERE title = 'Marian Yost';
```

```sql
+------------+-------------+-----------------------+---------------------+-------+--------+
| id         | title       | type                  | published_at        | stock | price  |
+------------+-------------+-----------------------+---------------------+-------+--------+
| 65670536   | Marian Yost | Arts                  | 1950-04-09 06:28:58 | 542   | 435.01 |
| 1164070689 | Marian Yost | Education & Reference | 1916-05-27 12:15:35 | 216   | 328.18 |
| 1414277591 | Marian Yost | Arts                  | 1932-06-15 09:18:14 | 303   | 496.52 |
| 2305318593 | Marian Yost | Arts                  | 2000-08-15 19:40:58 | 398   | 402.90 |
| 2638226326 | Marian Yost | Sports                | 1952-04-02 12:40:37 | 191   | 174.64 |
+------------+-------------+-----------------------+---------------------+-------+--------+
5 rows in set
Time: 0.582s
```

可以使用 `EXPLAIN` 来查看这个查询的执行计划，看看为什么查询这么慢：



```sql
EXPLAIN SELECT * FROM books WHERE title = 'Marian Yost';
```

```sql
+---------------------+------------+-----------+---------------+-----------------------------------------+
| id                  | estRows    | task      | access object | operator info                           |
+---------------------+------------+-----------+---------------+-----------------------------------------+
| TableReader_7       | 1.27       | root      |               | data:Selection_6                        |
| └─Selection_6       | 1.27       | cop[tikv] |               | eq(bookshop.books.title, "Marian Yost") |
|   └─TableFullScan_5 | 1000000.00 | cop[tikv] | table:books   | keep order:false                        |
+---------------------+------------+-----------+---------------+-----------------------------------------+
```

从执行计划中的 **TableFullScan_5** 可以看出，TiDB 将会对表 `books` 进行全表扫描，然后对每一行都判断 `title` 是否满足条件。**TableFullScan_5** 的 `estRows` 值为 `1000000.00`，说明优化器估计这个全表扫描会扫描 `1000000.00` 行数据。

更多关于 `EXPLAIN` 的使用介绍，可以阅读 使用 EXPLAIN 解读执行计划。

#### 解决方案：使用索引过滤数据

为了加速上面的查询，可以在 `books.title` 列创建一个索引：



```sql
CREATE INDEX title_idx ON books (title);
```

现在再执行这个查询将会快很多：



```sql
SELECT * FROM books WHERE title = 'Marian Yost';
```

```sql
+------------+-------------+-----------------------+---------------------+-------+--------+
| id         | title       | type                  | published_at        | stock | price  |
+------------+-------------+-----------------------+---------------------+-------+--------+
| 1164070689 | Marian Yost | Education & Reference | 1916-05-27 12:15:35 | 216   | 328.18 |
| 1414277591 | Marian Yost | Arts                  | 1932-06-15 09:18:14 | 303   | 496.52 |
| 2305318593 | Marian Yost | Arts                  | 2000-08-15 19:40:58 | 398   | 402.90 |
| 2638226326 | Marian Yost | Sports                | 1952-04-02 12:40:37 | 191   | 174.64 |
| 65670536   | Marian Yost | Arts                  | 1950-04-09 06:28:58 | 542   | 435.01 |
+------------+-------------+-----------------------+---------------------+-------+--------+
5 rows in set
Time: 0.007s
```

可以使用 `EXPLAIN` 来查看这个查询的执行计划，看看为什么查询变快了：



```sql
EXPLAIN SELECT * FROM books WHERE title = 'Marian Yost';
```

```sql
+---------------------------+---------+-----------+-------------------------------------+-------------------------------------------------------+
| id                        | estRows | task      | access object                       | operator info                                         |
+---------------------------+---------+-----------+-------------------------------------+-------------------------------------------------------+
| IndexLookUp_10            | 1.27    | root      |                                     |                                                       |
| ├─IndexRangeScan_8(Build) | 1.27    | cop[tikv] | table:books, index:title_idx(title) | range:["Marian Yost","Marian Yost"], keep order:false |
| └─TableRowIDScan_9(Probe) | 1.27    | cop[tikv] | table:books                         | keep order:false                                      |
+---------------------------+---------+-----------+-------------------------------------+-------------------------------------------------------+
```

从执行计划中的 **IndexLookUp_10** 可以看出，TiDB 将会通过索引 `title_idx` 来查询数据，其 `estRows` 值为 `1.27`，说明优化器估计只会扫描 `1.27` 行数据，远远小于之前全表扫的 `1000000.00` 行数据。

**IndexLookUp_10** 执行计划的执行流程是先用 **IndexRangeScan_8** 算子通过 `title_idx` 索引获取符合条件的索引数据，然后 **TableRowIDScan_9** 再更据索引数据里面的 Row ID 回表查询相应的行数据。

更多关于 TiDB 执行计划的内容，可以阅读TiDB 执行计划概览。

#### 解决方案：使用索引查询数据

上述解决方案中，需要先读取索引信息，再回表查询对应的行数据。但如果索引数据中包含了 SQL 查询所需的所有信息，就可以省去回表查询这个步骤。

例如下面查询中，仅需要根据 `title` 查询对应的 `price`：



```sql
SELECT title, price FROM books WHERE title = 'Marian Yost';
```

```sql
+-------------+--------+
| title       | price  |
+-------------+--------+
| Marian Yost | 435.01 |
| Marian Yost | 328.18 |
| Marian Yost | 496.52 |
| Marian Yost | 402.90 |
| Marian Yost | 174.64 |
+-------------+--------+
5 rows in set
Time: 0.007s
```

由于索引 `title_idx` 仅包含 `title` 列的信息，所以 TiDB 还是需要扫描索引数据，然后回表查询 `price` 数据：



```sql
EXPLAIN SELECT title, price FROM books WHERE title = 'Marian Yost';
```

```sql
+---------------------------+---------+-----------+-------------------------------------+-------------------------------------------------------+
| id                        | estRows | task      | access object                       | operator info                                         |
+---------------------------+---------+-----------+-------------------------------------+-------------------------------------------------------+
| IndexLookUp_10            | 1.27    | root      |                                     |                                                       |
| ├─IndexRangeScan_8(Build) | 1.27    | cop[tikv] | table:books, index:title_idx(title) | range:["Marian Yost","Marian Yost"], keep order:false |
| └─TableRowIDScan_9(Probe) | 1.27    | cop[tikv] | table:books                         | keep order:false                                      |
+---------------------------+---------+-----------+-------------------------------------+-------------------------------------------------------+
```

删除 `title_idx` 索引，并新建一个 `title_price_idx` 索引：



```sql
ALTER TABLE books DROP INDEX title_idx;
```



```sql
CREATE INDEX title_price_idx ON books (title, price);
```

现在，`price` 数据已经存储在索引 `title_price_idx` 中了，所以下面查询仅需扫描索引数据，无需回表查询了。这种索引通常被叫做覆盖索引：



```sql
EXPLAIN SELECT title, price FROM books WHERE title = 'Marian Yost';
```

```sql
--------------------+---------+-----------+--------------------------------------------------+-------------------------------------------------------+
| id                 | estRows | task      | access object                                    | operator info                                         |
+--------------------+---------+-----------+--------------------------------------------------+-------------------------------------------------------+
| IndexReader_6      | 1.27    | root      |                                                  | index:IndexRangeScan_5                                |
| └─IndexRangeScan_5 | 1.27    | cop[tikv] | table:books, index:title_price_idx(title, price) | range:["Marian Yost","Marian Yost"], keep order:false |
+--------------------+---------+-----------+--------------------------------------------------+-------------------------------------------------------+
```

现在这条查询的速度将会更快：



```sql
SELECT title, price FROM books WHERE title = 'Marian Yost';
```

```sql
+-------------+--------+
| title       | price  |
+-------------+--------+
| Marian Yost | 174.64 |
| Marian Yost | 328.18 |
| Marian Yost | 402.90 |
| Marian Yost | 435.01 |
| Marian Yost | 496.52 |
+-------------+--------+
5 rows in set
Time: 0.004s
```

由于后面的示例还会用到这个库，删除 `title_price_idx` 索引。



```sql
ALTER TABLE books DROP INDEX title_price_idx;
```

#### 解决方案：使用主键查询数据

如果查询中使用主键过滤数据，这条查询的执行速度会非常快，例如表 `books` 的主键是列 `id`, 使用列 `id` 来查询数据：



```sql
SELECT * FROM books WHERE id = 896;
```

```sql
+-----+----------------+----------------------+---------------------+-------+--------+
| id  | title          | type                 | published_at        | stock | price  |
+-----+----------------+----------------------+---------------------+-------+--------+
| 896 | Kathryne Doyle | Science & Technology | 1969-03-18 01:34:15 | 468   | 281.32 |
+-----+----------------+----------------------+---------------------+-------+--------+
1 row in set
Time: 0.004s
```

使用 `EXPLAIN` 查看执行计划:



```sql
EXPLAIN SELECT * FROM books WHERE id = 896;
```



```sql
+-------------+---------+------+---------------+---------------+
| id          | estRows | task | access object | operator info |
+-------------+---------+------+---------------+---------------+
| Point_Get_1 | 1.00    | root | table:books   | handle:896    |
+-------------+---------+------+---------------+---------------+
```

**Point_Get**，又名 “点查”，它的执行速度也非常快。

### 选择合适的 Join 执行计划

见 JOIN 查询的执行计划。

### 推荐阅读

- 使用 EXPLAIN 解读执行计划。
- 用 EXPLAIN 查看索引查询的执行计划。


---
title: 性能调优最佳实践
summary: 介绍使用 TiDB 的性能调优最佳实践。
---

## 性能调优最佳实践

本章将介绍在使用 TiDB 数据库的一些最佳实践。

### DML 最佳实践

以下将介绍使用 TiDB 的 DML 时所涉及到的最佳实践。

#### 使用单个语句多行数据操作

当需要修改多行数据时，推荐使用单个 SQL 多行数据的语句：



```sql
INSERT INTO t VALUES (1, 'a'), (2, 'b'), (3, 'c');

DELETE FROM t WHERE id IN (1, 2, 3);
```

不推荐使用多个 SQL 单行数据的语句：



```sql
INSERT INTO t VALUES (1, 'a');
INSERT INTO t VALUES (2, 'b');
INSERT INTO t VALUES (3, 'c');

DELETE FROM t WHERE id = 1;
DELETE FROM t WHERE id = 2;
DELETE FROM t WHERE id = 3;
```

#### 使用 PREPARE

当需要多次执行某个 SQL 语句时，推荐使用 `PREPARE` 语句，可以避免重复解析 SQL 语法的开销。

<SimpleTab>
<div label="Golang">

在 Golang 中使用 `PREPARE` 语句：

```go
func BatchInsert(db *sql.DB) error {
  stmt, err := db.Prepare("INSERT INTO t (id) VALUES (?), (?), (?), (?), (?)")
  if err != nil {
    return err
  }
  for i := 0; i < 1000; i += 5 {
    values := []interface{}{i, i + 1, i + 2, i + 3, i + 4}
    _, err = stmt.Exec(values...)
    if err != nil {
      return err
    }
  }
  return nil
}
```

</div>

<div label="Java">

在 Java 中使用 `PREPARE` 语句：

```java
public void batchInsert(Connection connection) throws SQLException {
  PreparedStatement statement = connection.prepareStatement(
      "INSERT INTO `t` (`id`) VALUES (?), (?), (?), (?), (?)");
  for (int i = 0; i < 1000; i ++) {
    statement.setInt(i % 5 + 1, i);

    if (i % 5 == 4) {
      statement.executeUpdate();
    }
  }
}
```

</div>

<div label="Python">

在 Python 中使用 `PREPARE` 语句时，并不需要显式指定。在你使用参数化查询时，mysqlclient 等 Driver 将自动转用执行计划。

</div>
</SimpleTab>

注意不要重复执行 `PREPARE` 语句，否则并不能提高执行效率。

#### 避免查询不必要的信息

如非必要，不要总是用 `SELECT *` 返回所以列的数据，下面查询是低效的：



```sql
SELECT * FROM books WHERE title = 'Marian Yost';
```

应该仅查询需要的列信息，例如：



```sql
SELECT title, price FROM books WHERE title = 'Marian Yost';
```

#### 使用批量删除

当需要删除大量的数据，推荐使用批量删除，见[批量删除](#批量删除)

#### 使用批量更新

当需要更新大量的数据时，推荐使用批量更新，见[批量更新](#批量更新)

#### 使用 TRUNCATE 语句代替 DELETE 全表数据

当需要删除一个表的所有数据时，推荐使用 `TRUNCATE` 语句：



```sql
TRUNCATE TABLE t;
```

不推荐使用 `DELETE` 全表数据：



```sql
DELETE FROM t;
```

### DDL 最佳实践

以下将介绍使用 TiDB 的 DDL 时所涉及到的最佳实践。

#### 主键选择的最佳实践

见[选择主键时应遵守的规则](#选择主键时应遵守的规则)。

### 索引的最佳实践

见[索引的最佳实践](#索引的最佳实践)。

#### 添加索引性能最佳实践

TiDB 支持在线添加索引操作，可通过 [`ADD INDEX`](None) 或 [`CREATE INDEX`](None) 完成索引添加操作。添加索引不会阻塞表中的数据读写。可以通过修改下面的系统变量来调整 DDL 操作 `re-organize` 阶段的并行度与回填索引的单批数量大小：

- tidb_ddl_reorg_worker_cnt
- tidb_ddl_reorg_batch_size

为了减少对在线业务的影响，添加索引的默认速度会比较保守。当添加索引的目标列仅涉及查询负载，或者与线上负载不直接相关时，可以适当调大上述变量来加速添加索引：



```sql
SET @@global.tidb_ddl_reorg_worker_cnt = 16;
SET @@global.tidb_ddl_reorg_batch_size = 4096;
```

当添加索引操作的目标列被频繁更新（包含 `UPDATE`、`INSERT` 和 `DELETE`）时，调大上述配置会造成较为频繁的写冲突，使得在线负载较大；同时添加索引操作也可能由于不断地重试，需要很长的时间才能完成。此时建议调小上述配置来避免和在线业务的写冲突：



```sql
SET @@global.tidb_ddl_reorg_worker_cnt = 4;
SET @@global.tidb_ddl_reorg_batch_size = 128;
```

### 事务冲突

关于如何定位和解决事务冲突，请参考TiDB 锁冲突问题处理。

### Java 数据库应用开发最佳实践

[TiDB 最佳实践系列（五）Java 数据库应用开发指南](https://pingcap.com/zh/blog/best-practice-java)。

#### 推荐阅读

- [TiDB 最佳实践系列（一）高并发写入常见热点问题及规避方法](https://pingcap.com/zh/blog/tidb-in-high-concurrency-scenarios)。


---
title: 索引的最佳实践
summary: 介绍 TiDB 中索引的最佳实践。
---

<!-- markdownlint-disable MD029 -->

## 索引的最佳实践

本章会介绍在 TiDB 中使用索引的一些最佳实践。

### 准备工作

本章内容将会用 [bookshop](#bookshop-应用) 数据库中的 `books` 表作为示例。



```sql
CREATE TABLE `books` (
  `id` bigint(20) AUTO_RANDOM NOT NULL,
  `title` varchar(100) NOT NULL,
  `type` enum('Magazine', 'Novel', 'Life', 'Arts', 'Comics', 'Education & Reference', 'Humanities & Social Sciences', 'Science & Technology', 'Kids', 'Sports') NOT NULL,
  `published_at` datetime NOT NULL,
  `stock` int(11) DEFAULT '0',
  `price` decimal(15,2) DEFAULT '0.0',
  PRIMARY KEY (`id`) CLUSTERED
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
```

### 创建索引的最佳实践

- 建立你需要使用的数据的所有列的组合索引，这种优化技巧被称为 [覆盖索引优化 (covering index optimization)](#indexreader)。**覆盖索引优化**将使得 TiDB 可以直接在索引上得到该查询所需的所有数据，可以大幅提升性能。
- 避免创建你不需要的二级索引，有用的二级索引能加速查询，但是要注意新增一个索引是有副作用的。每增加一个索引，在插入一条数据的时候，就要额外新增一个 Key-Value，所以索引越多，写入越慢，并且空间占用越大。另外过多的索引也会影响优化器运行时间，并且不合适的索引会误导优化器。所以索引并不是越多越好。
- 根据具体的业务特点创建合适的索引。原则上需要对查询中需要用到的列创建索引，目的是提高性能。下面几种情况适合创建索引：

    - 区分度比较大的列，通过索引能显著地减少过滤后的行数。例如推荐在人的身份证号码这一列上创建索引，但不推荐在人的性别这一列上创建索引。
    - 有多个查询条件时，可以选择组合索引，注意需要把等值条件的列放在组合索引的前面。这里举一个例子，假设常用的查询是 `SELECT * FROM t where c1 = 10 and c2 = 100 and c3 > 10`, 那么可以考虑建立组合索引 `Index cidx (c1, c2, c3)`，这样可以用查询条件构造出一个索引前缀进行 Scan。

- 请使用有意义的二级索引名，推荐你遵循公司或组织的表命名规范。如果你的公司或组织没有相应的命名规范，可参考[索引命名规范](#索引命名规范)。

### 使用索引的最佳实践

- 建立索引的目的是为了加速查询，所以请确保索引能在一些查询中被用上。如果一个索引不会被任何查询语句用到，那这个索引是没有意义的，请删除这个索引。
- 使用组合索引时，需要满足最左前缀原则。

    例如假设在列 `title, published_at` 上新建一个组合索引索引：

    

    ```sql
    CREATE INDEX title_published_at_idx ON books (title, published_at);
    ```

    下面这个查询依然能用上这个组合索引：

    

    ```sql
    SELECT * FROM books WHERE title = 'database';
    ```

    但下面这个查询由于未指定组合索引中最左边第一列的条件，所以无法使用组合索引：

    

    ```sql
    SELECT * FROM books WHERE published_at = '2018-08-18 21:42:08';
    ```

- 在查询条件中使用索引列作为条件时，不要在索引列上做计算，函数，或者类型转换的操作，会导致优化器无法使用该索引。

    例如假设在时间类型的列 `published_at` 上新建一个索引：

    

    ```sql
    CREATE INDEX published_at_idx ON books (published_at);
    ```

    但下面查询是无法使用 `published_at` 上的索引的：

    

    ```sql
    SELECT * FROM books WHERE YEAR(published_at)=2022;
    ```

    可以改写成下面查询，避免在索引列上做函数计算后，即可使用 `published_at` 上的索引:

    

    ```sql
    SELECT * FROM books WHERE published_at >= '2022-01-01' AND published_at < '2023-01-01';
    ```

    也可以使用表达式索引，例如对查询条件中的 `YEAR(published_at)` 创建一个表达式索引：

    

    ```sql
    CREATE INDEX published_year_idx ON books ((YEAR(published_at)));
    ```

    然后通过 `SELECT * FROM books WHERE YEAR(published_at)=2022;` 查询就能使用 `published_year_idx` 索引来加速查询了。

    > **注意：**
    >
    > 表达式索引目前是 TiDB 的实验特性，需要在 TiDB 配置文件中开启表达式索引特性，详情可以参考 表达式索引文档。

- 尽量使用覆盖索引，即索引列包含查询列，避免总是 `SELECT *` 查询所有列的语句。

    例如下面查询只需扫描索引 `title_published_at_idx` 数据即可获取查询列的数据：

    

    ```sql
    SELECT title, published_at FROM books WHERE title = 'database';
    ```

    但下面查询语句虽然能用上组合索引 `(title, published_at)`, 但会多一个回表查询非索引列数据的额外开销，回表查询是指根据索引数据中存储的引用（一般是主键信息），到表中查询相应行的数据。

    

    ```sql
    SELECT * FROM books WHERE title = 'database';
    ```

- 查询条件使用 `!=`，`NOT IN` 时，无法使用索引。例如下面查询无法使用任何索引：

    

    ```sql
    SELECT * FROM books WHERE title != 'database';
    ```

- 使用 `LIKE` 时如果条件是以通配符 `%` 开头，也无法使用索引。例如下面查询无法使用任何索引：

    

    ```sql
    SELECT * FROM books WHERE title LIKE '%database';
    ```

- 当查询条件有多个索引可供使用，但你知道用哪一个索引是最优的时，推荐使用 优化器 Hint 来强制优化器使用这个索引，这样可以避免优化器因为统计信息不准或其他问题时，选错索引。

    例如下面查询中，假设在列 `id` 和 列 `title` 上都各自有索引 `id_idx` 和 `title_idx`，你知道 `id_idx` 的过滤性更好，就可以在 SQL 中使用 `USE INDEX` Hint 来强制优化器使用 `id_idx` 索引。

    

    ```sql
    SELECT * FROM t USE INDEX(id_idx) WHERE id = 1 and title = 'database';
    ```

- 查询条件使用 `IN` 表达式时，后面匹配的条件数量建议不要超过 300 个，否则执行效率会较差。



## 其他优化

---
title: 避免隐式类型转换
summary: 介绍 TiDB 中隐式类型转换可能会带来的后果和避免方法。
---

### 避免隐式类型转换

本章内容将介绍 TiDB 中的隐式类型转换规则、可能带来的后果及避免方法。

#### 转换规则

当 SQL 中谓词两侧的数据类型不一致时，TiDB 将隐式地将一侧或两侧的数据类型进行转换，将其变为兼容的数据类型，以进行谓词运算。

TiDB 中隐式类型转换规则如下：

- 如果一个或两个参数都是 NULL，比较的结果是 NULL（NULL 安全的 `<=>` 相等比较运算符除外，对于 NULL `<=>` NULL，结果为 true，不需要转换）。
- 如果比较操作中的两个参数都是字符串，则将它们作为字符串进行比较。
- 如果两个参数都是整数，则将它们作为整数进行比较。
- 如果不与数字进行比较，则将十六进制值视为二进制字符串。
- 如果其中一个参数是十进制值，则比较取决于另一个参数。如果另一个参数是十进制或整数值，则将参数与十进制值进行比较，如果另一个参数是浮点值，则将参数与浮点值进行比较。
- 如果其中一个参数是 TIMESTAMP 或 DATETIME 列，另一个参数是常量，则在执行比较之前将常量转换为时间戳。
- 在所有其他情况下，参数都是作为浮点数（DOUBLE 类型）比较的。

#### 隐式类型转换引起的后果

隐式类型转换增强了人机交互的易用性，但在应用代码中，应尽量避免隐式类型转换出现，这是由于隐式类型转换会导致：

- 索引失效
- 精度丢失

##### 索引失效

如下案例，account_id 为主键，其数据类型为 `varchar`。通过执行计划可见，该 SQL 发生了隐式类型转换，无法使用索引。



```sql
DESC SELECT * FROM `account` WHERE `account_id`=6010000000009801;
+-------------------------+----------------+-----------+---------------+------------------------------------------------------------+
| id                      | estRows        | task      | access object | operator info                                              |
+-------------------------+----------------+-----------+---------------+------------------------------------------------------------+
| TableReader_7           | 8000628000.00  | root      |               | data:Selection_6                                           |
| └─Selection_6           | 8000628000.00  | cop[tikv] |               | eq(cast(findpt.account.account_id), 6.010000000009801e+15) |
|   └─TableFullScan_5     | 10000785000.00 | cop[tikv] | table:account | keep order:false                                           |
+-------------------------+----------------+-----------+---------------+------------------------------------------------------------+
3 rows in set (0.00 sec)
```

**运行结果简述**：从以上执行计划中，可见 Cast 算子。

##### 精度丢失

如下案例，字段 a 的数据类型为 `decimal(32,0)`，从执行计划可以得知，出现了隐式类型转换，decimal 字段和字符串常值都被转换为 double 类型，而 `double` 类型的精度没有 `decimal` 高，出现了精度丢失，在这个 case 中，造成了筛选出范围之外的结果集的错误。



```sql
DESC SELECT * FROM `t1` WHERE `a` BETWEEN '12123123' AND '1111222211111111200000';
+-------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------+
| id                      | estRows | task      | access object | operator info                                                                       |
+-------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------+
| TableReader_7           | 0.80    | root      |               | data:Selection_6                                                                    |
| └─Selection_6           | 0.80    | cop[tikv] |               | ge(cast(findpt.t1.a), 1.2123123e+07), le(cast(findpt.t1.a), 1.1112222111111112e+21) |
|   └─TableFullScan_5     | 1.00    | cop[tikv] | table:t1      | keep order:false, stats:pseudo                                                      |
+-------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------+
3 rows in set (0.00 sec)
```

**运行结果简述**：从以上执行计划中，可见 Cast 算子。



```sql
SELECT * FROM `t1` WHERE `a` BETWEEN '12123123' AND '1111222211111111200000';
+------------------------+
| a                      |
+------------------------+
| 1111222211111111222211 |
+------------------------+
1 row in set (0.01 sec)

```

**运行结果简述**：以上执行出现了错误结果。


---
title: 唯一序列号生成方案
summary: 唯一序列号生成方案，为自行生成唯一 ID 的开发者提供帮助。
---

### 唯一序列号生成方案

本章将介绍唯一序列号生成方案，为自行生成唯一 ID 的开发者提供帮助。

#### 自增列

自增（auto_increment）是大多数兼容 MySQL 协议的 RDBMS 上列的一种属性，通过配置该属性来使数据库为该列的值自动赋值，用户不需要为该列赋值，该列的值随着表内记录增加会自动增长，并确保唯一性。在大多数场景中，自增列并未拥有业务属性，仅仅代表了这一行数据，即被作为无业务含义的代理主键使用。自增列的局限性在于：自增列只能采用整型字段，所赋的值也只能为整型。假设业务所需要的序列号由字母、数字及其他字符拼接而成，用户将难以通过自增列来获取序列号中所需的数字自增值。

#### 序列（Sequence）

序列是一种数据库对象，应用程序通过调用某个序列可以产生递增的序列值，应用程序可以灵活的使用这个序列值为一张表或多张表赋值，也可以使用序列值进行更复杂的加工，来实现文本和数字的组合，来赋予代理键以一定的跟踪和分类的意义。从 TiDB v4.0 版本开始提供序列功能，详情请参考 CREATE SEQUENCE。

#### 类 Snowflake 方案

Snowflake 是 Twitter 提出的分布式 ID 生成方案。目前有多种实现，较流行的是百度的 uid-generator 和美团的 leaf。下面以 uid-generator 为例展开说明。

uid-generator 生成的 64 位 ID 结构如下：

```
| sign | delta seconds | worker node id | sequencs |
|------|---------------|----------------|----------|
| 1bit |     28bits    | 22bits         | 13bits   |
```

- sign：长度固定为 1 位。固定为 0，表示生成的 ID 始终为正数。
- delta seconds：默认 28 位。当前时间，表示为相对于某个预设时间基点 (默认"2016-05-20") 的增量值，单位为秒。28 位最多可支持约 8.7 年。
- worker node id：默认 22 位。表示机器 id，通常在应用程序进程启动时从一个集中式的 ID 生成器取得。常见的集中式 ID 生成器是数据库自增列或者 Zookeeper。默认分配策略为用后即弃，进程重启时会重新获取一个新的 worker node id，22 位最多可支持约 420 万次启动。
- sequence：默认 13 位。表示每秒的并发序列，13 位可支持每秒 8192 个并发。

#### 号段分配方案

号段分配方案可以理解为从数据库批量获取自增 ID。本方案需要一张序列号生成表，每行记录表示一个序列对象。表定义示例如下：

| 字段名   | 字段类型     | 字段说明                     |
| -------- | ------------ | ---------------------------- |
| SEQ_NAME | varchar(128) | 序列名称，用来区分不同业务   |
| MAX_ID   | bigint(20)   | 当前序列已被分配出去的最大值 |
| STEP     | int(11)      | 步长，表示每次分配的号段长度 |

应用程序每次按配置好的步长获取一段序列号，并同时更新数据库以持久化保存当前序列已被分配出去的最大值，然后在应用程序内存中即可完成序列号加工及分配动作。待一段号码耗尽之后，应用程序才会去获取新的号段，这样就有效降低了数据库写入压力。实际使用过程中，还可以适度调节步长以控制数据库记录的更新频度。

最后，需要注意的是，上述两种方案生成的 ID 都不够随机，不适合直接作为 TiDB 表的主键。实际使用过程中可以对生成的 ID 进行位反转（bit-reverse）后得到一个较为随机的新 ID。



# 故障诊断

---
title: SQL 或事务问题
summary: 学习诊断在应用开发过程中可能产生的 SQL 或事务问题的方法。
---

## SQL 或事务问题

本章介绍在开发应用过程中可能遇到的常见问题的诊断处理方法。

### SQL 操作常见问题

如果你想提高 SQL 的性能，可以阅读 [SQL 性能优化](#概览)来避免一些常见的性能问题。然后如果依然存在性能问题，推荐阅读：

- 分析慢查询
- 使用 Top SQL 定位系统资源消耗过多的查询

如果你遇到了一些关于 SQL 操作的问题，可以阅读 SQL 操作常见问题。

### 事务错误处理

见[事务错误处理](#事务错误处理)。

### 推荐阅读

- 不支持的功能特性
- 集群管理 FAQ
- TiDB 产品 FAQ


---
title: 结果集不稳定
summary: 结果集不稳定错误的处理办法。
---

## 结果集不稳定

本章将叙述结果集不稳定错误的处理办法。

### group by

出于便捷的考量，MySQL “扩展” 了 group by 语法，使 select 子句可以引用未在 group by 子句中声明的非聚集字段，也就是 non-full group by 语法。在其他数据库中，这被认为是一种语法错误，因为这会导致结果集不稳定。

在下例的 3 条 SQL 语句中，第一条 SQL 使用了 full group by 语法 ，所有在 select 子句中引用的字段，都在 group by 子句中有所声明，所以它的结果集是稳定的，可以看到 class 与 stuname 的全部组合共有三种；第二条与第三条是同一个 SQL，但它在两次执行时得到了不同的结果，这条 SQL 的 group by 子句中仅声明了一个 class 字段，因此结果集只会针对 class 进行聚集，class 的唯一值有两个，也就是说结果集中只会包含两行数据，而 class 与 stuname 的全部组合共有三种，班级 2018_CS_03 有两位同学，每次执行时返回哪位同学是没有语义上的限制的，都是符合语义的结果。



```sql
mysql> SELECT a.class, a.stuname, max(b.courscore) from stu_info a join stu_score b on a.stuno=b.stuno group by a.class, a.stuname order by a.class, a.stuname;
+------------+--------------+------------------+
| class      | stuname      | max(b.courscore) |
+------------+--------------+------------------+
| 2018_CS_01 | MonkeyDLuffy |             95.5 |
| 2018_CS_03 | PatrickStar  |             99.0 |
| 2018_CS_03 | SpongeBob    |             95.0 |
+------------+--------------+------------------+
3 rows in set (0.00 sec)

mysql> select a.class, a.stuname, max(b.courscore) from stu_info a join stu_score b on a.stuno=b.stuno group by a.class order by a.class, a.stuname;
+------------+--------------+------------------+
| class      | stuname      | max(b.courscore) |
+------------+--------------+------------------+
| 2018_CS_01 | MonkeyDLuffy |             95.5 |
| 2018_CS_03 | SpongeBob    |             99.0 |
+------------+--------------+------------------+
2 rows in set (0.01 sec)

mysql> select a.class, a.stuname, max(b.courscore) from stu_info a join stu_score b on a.stuno=b.stuno group by a.class order by a.class, a.stuname;
+------------+--------------+------------------+
| class      | stuname      | max(b.courscore) |
+------------+--------------+------------------+
| 2018_CS_01 | MonkeyDLuffy |             95.5 |
| 2018_CS_03 | PatrickStar  |             99.0 |
+------------+--------------+------------------+
2 rows in set (0.01 sec)

```

因此，想保障 group by 语句结果集的稳定，请使用 full group by 语法。

MySQL 提供了一个 SQL_MODE 开关 ONLY_FULL_GROUP_BY 来控制是否进行 full group by 语法的检查，TiDB 也兼容了这个 SQL_MODE 开关：



```sql
mysql> select a.class, a.stuname, max(b.courscore) from stu_info a join stu_score b on a.stuno=b.stuno group by a.class order by a.class, a.stuname;
+------------+--------------+------------------+
| class      | stuname      | max(b.courscore) |
+------------+--------------+------------------+
| 2018_CS_01 | MonkeyDLuffy |             95.5 |
| 2018_CS_03 | PatrickStar  |             99.0 |
+------------+--------------+------------------+
2 rows in set (0.01 sec)

mysql> set @@sql_mode='STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION,ONLY_FULL_GROUP_BY';
Query OK, 0 rows affected (0.01 sec)

mysql> select a.class, a.stuname, max(b.courscore) from stu_info a join stu_score b on a.stuno=b.stuno group by a.class order by a.class, a.stuname;
ERROR 1055 (42000): Expression #2 of ORDER BY is not in GROUP BY clause and contains nonaggregated column '' which is not functionally dependent on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by
```

**运行结果简述**：上例为 sql_mode 设置了 ONLY_FULL_GROUP_BY 的效果。

### order by

在 SQL 的语义中，只有使用了 order by 语法才会保障结果集的顺序输出。而单机数据库由于数据都存储在一台服务器上，在不进行数据重组时，多次执行的结果往往是稳定的，有些数据库(尤其是 MySQL InnoDB 存储引擎)还会按照主键或索引的顺序进行结果集的输出。TiDB 是分布式数据库，数据被存储在多台服务器上，另外 TiDB 层不缓存数据页，因此不含 order by 的 SQL 语句的结果集展现顺序容易被感知到不稳定。想要按顺序输出的结果集，需明确地把要排序的字段添加到 order by 子句中，这符合 SQL 的语义。

在下面的案例中，用户只在 order by 子句中添加了一个字段，TiDB 只会按照这一个字段进行排序。



```sql
mysql> select a.class, a.stuname, b.course, b.courscore from stu_info a join stu_score b on a.stuno=b.stuno order by a.class;
+------------+--------------+-------------------------+-----------+
| class      | stuname      | course                  | courscore |
+------------+--------------+-------------------------+-----------+
| 2018_CS_01 | MonkeyDLuffy | PrinciplesofDatabase    |      60.5 |
| 2018_CS_01 | MonkeyDLuffy | English                 |      43.0 |
| 2018_CS_01 | MonkeyDLuffy | OpSwimming              |      67.0 |
| 2018_CS_01 | MonkeyDLuffy | OpFencing               |      76.0 |
| 2018_CS_01 | MonkeyDLuffy | FundamentalsofCompiling |      88.0 |
| 2018_CS_01 | MonkeyDLuffy | OperatingSystem         |      90.5 |
| 2018_CS_01 | MonkeyDLuffy | PrincipleofStatistics   |      69.0 |
| 2018_CS_01 | MonkeyDLuffy | ProbabilityTheory       |      76.0 |
| 2018_CS_01 | MonkeyDLuffy | Physics                 |      63.5 |
| 2018_CS_01 | MonkeyDLuffy | AdvancedMathematics     |      95.5 |
| 2018_CS_01 | MonkeyDLuffy | LinearAlgebra           |      92.5 |
| 2018_CS_01 | MonkeyDLuffy | DiscreteMathematics     |      89.0 |
| 2018_CS_03 | SpongeBob    | PrinciplesofDatabase    |      88.0 |
| 2018_CS_03 | SpongeBob    | English                 |      79.0 |
| 2018_CS_03 | SpongeBob    | OpBasketball            |      92.0 |
| 2018_CS_03 | SpongeBob    | OpTennis                |      94.0 |
| 2018_CS_03 | PatrickStar  | LinearAlgebra           |       6.5 |
| 2018_CS_03 | PatrickStar  | AdvancedMathematics     |       5.0 |
| 2018_CS_03 | SpongeBob    | DiscreteMathematics     |      72.0 |
| 2018_CS_03 | PatrickStar  | ProbabilityTheory       |      12.0 |
| 2018_CS_03 | PatrickStar  | PrincipleofStatistics   |      20.0 |
| 2018_CS_03 | PatrickStar  | OperatingSystem         |      36.0 |
| 2018_CS_03 | PatrickStar  | FundamentalsofCompiling |       2.0 |
| 2018_CS_03 | PatrickStar  | DiscreteMathematics     |      14.0 |
| 2018_CS_03 | PatrickStar  | PrinciplesofDatabase    |       9.0 |
| 2018_CS_03 | PatrickStar  | English                 |      60.0 |
| 2018_CS_03 | PatrickStar  | OpTableTennis           |      12.0 |
| 2018_CS_03 | PatrickStar  | OpPiano                 |      99.0 |
| 2018_CS_03 | SpongeBob    | FundamentalsofCompiling |      43.0 |
| 2018_CS_03 | SpongeBob    | OperatingSystem         |      95.0 |
| 2018_CS_03 | SpongeBob    | PrincipleofStatistics   |      90.0 |
| 2018_CS_03 | SpongeBob    | ProbabilityTheory       |      87.0 |
| 2018_CS_03 | SpongeBob    | Physics                 |      65.0 |
| 2018_CS_03 | SpongeBob    | AdvancedMathematics     |      55.0 |
| 2018_CS_03 | SpongeBob    | LinearAlgebra           |      60.5 |
| 2018_CS_03 | PatrickStar  | Physics                 |       6.0 |
+------------+--------------+-------------------------+-----------+
36 rows in set (0.01 sec)

```

当遇到相同的 order by 值时，排序结果不稳定。为减少随机性，应当尽可能保持 order by 值的唯一性。不能保证唯一的继续加，保证 order by 的字段组合是唯一时，结果才能唯一。

### 由于 group_concat() 中没有使用 order by 导致结果集不稳定

结果集不稳定是因为 TiDB 是并行地从存储层读取数据，所以 `group_concat()` 在不加 order by 的情况下得到的结果集展现顺序容易被感知到不稳定。

`group_concat()` 要获取到按顺序输出的结果集，需要把用于排序的字段添加到 order by 子句中，这样才符合 SQL 的语义。在下面的案例中，使用 `group_concat()` 不加 order by 的情况下拼接 customer_id ，造成结果集不稳定：

1. 不加 order by

   第一次查询：

   

   ```sql
   mysql>  select GROUP_CONCAT( customer_id SEPARATOR ',' ) FROM customer where customer_id like '200002%';
   +-------------------------------------------------------------------------+
   | GROUP_CONCAT(customer_id  SEPARATOR ',')                                |
   +-------------------------------------------------------------------------+
   | 20000200992,20000200993,20000200994,20000200995,20000200996,20000200... |
   +-------------------------------------------------------------------------+
   ```

   第二次查询：

   

   ```sql
   mysql>  select GROUP_CONCAT( customer_id SEPARATOR ',' ) FROM customer where customer_id like '200002%';
   +-------------------------------------------------------------------------+
   | GROUP_CONCAT(customer_id  SEPARATOR ',')                                |
   +-------------------------------------------------------------------------+
   | 20000203040,20000203041,20000203042,20000203043,20000203044,20000203... |
   +-------------------------------------------------------------------------+
   ```

2. 加 order by

   第一次查询：

   

   ```sql
   mysql>  select GROUP_CONCAT( customer_id order by customer_id SEPARATOR ',' ) FROM customer where customer_id like '200002%';
   +-------------------------------------------------------------------------+
   | GROUP_CONCAT(customer_id  SEPARATOR ',')                                |
   +-------------------------------------------------------------------------+
   | 20000200000,20000200001,20000200002,20000200003,20000200004,20000200... |
   +-------------------------------------------------------------------------+
   ```

   第二次查询：

   

   ```sql
   mysql>  select GROUP_CONCAT( customer_id order by customer_id SEPARATOR ',' ) FROM customer where customer_id like '200002%';
   +-------------------------------------------------------------------------+
   | GROUP_CONCAT(customer_id  SEPARATOR ',')                                |
   +-------------------------------------------------------------------------+
   | 20000200000,20000200001,20000200002,20000200003,20000200004,20000200... |
   +-------------------------------------------------------------------------+
   ```

### select \* from t limit n 的结果不稳定

返回结果与数据在存储节点 (TiKV) 上的分布有关。如果进行了多次查询，存储节点 (TiKV) 不同存储单元 (Region) 返回结果的速度不同，会造成结果不稳定。


---
title: TiDB 中的各种超时
summary: 简单介绍 TiDB 中的各种超时，为排查错误提供依据。
---

## TiDB 中的各种超时

本章将介绍 TiDB 中的各种超时，为排查错误提供依据。

### GC 超时

TiDB 的事务的实现采用了 MVCC（多版本并发控制）机制，当新写入的数据覆盖旧的数据时，旧的数据不会被替换掉，而是与新写入的数据同时保留，并以时间戳来区分版本。TiDB 通过定期 GC 的机制来清理不再需要的旧数据。

默认配置下 TiDB 可以保障每个 MVCC 版本（一致性快照）保存 10 分钟，读取时间超过 10 分钟的事务，会收到报错 `GC life time is shorter than transaction duration`。

当用户确信自己需要更长的读取时间时，比如在使用了 Mydumper 做全量备份的场景中（Mydumper 备份的是一致性的快照），可以通过调整 TiDB 中`mysql.tidb` 表中的 `tikv_gc_life_time` 的值来调大 MVCC 版本保留时间，需要注意的是 tikv_gc_life_time 的配置是立刻影响全局的，调大它会为当前所有存在的快照增加生命时长，调小它会立即缩短所有快照的生命时长。过多的 MVCC 版本会拖慢 TiKV 的处理效率，在使用 Mydumper 做完全量备份后需要及时把 tikv_gc_life_time 调整回之前的设置。

更多关于 GC 的信息，请参考 [GC 机制简介](https://pingcap.com/docs-cn/stable/reference/garbage-collection/overview/)文档。

### 事务超时

垃圾回收 (GC) 不会影响到正在执行的事务。但悲观事务的运行仍有上限，有基于事务超时的限制（TiDB 配置文件 [performance] 类别下的 `max-txn-ttl` 修改，默认为 60 分钟）和 基于事务使用内存的限制。

形如 `INSERT INTO t10 SELECT * FROM t1` 的 SQL 语句，不会受到 GC 的影响，但超过了 `max-txn-ttl` 的时间后，会由于超时而回滚。

### SQL 执行时间超时

TiDB 还提供了一个系统变量来限制单条 SQL 语句的执行时间：max_execution_time，它的默认值为 0，表示无限制。`max_execution_time` 目前对所有类型的 statement 生效，并非只对 SELECT 语句生效。其单位为 ms，但实际精度在 100ms 级别，而非更准确的毫秒级别。

### JDBC 查询超时

MySQL jdbc 的查询超时设置 `setQueryTimeout()` 对 TiDB 不起作用。这是因为现实客户端感知超时时，向数据库发送一个 KILL 命令。但是由于 tidb-server 是负载均衡的， 为防止在错误的 tidb-server 上终止连接， tidb-server 不会执行这个 KILL。这时就要用 `MAX_EXECUTION_TIME` 实现查询超时的效果。

TiDB 提供了三个与 MySQL 兼容的超时控制参数：

- **wait_timeout**，控制与 Java 应用连接的非交互式空闲超时时间。在 TiDB v5.4 及以上版本中，默认值为 `28800` 秒，即空闲超时为 8 小时。在 v5.4 之前，默认值为 `0`，即没有时间限制。
- **interactive_timeout**，控制与 Java 应用连接的交互式空闲超时时间，默认值为 8 小时。
- **max_execution_time**，控制连接中 SQL 执行的超时时间，默认值是 0，即允许连接无限忙碌（一个 SQL 语句执行无限的长的时间）。

但在实际生产环境中，空闲连接和一直无限执行的 SQL 对数据库和应用都有不好的影响。你可以通过在应用的连接字符串中配置这两个 session 级的变量来避免空闲连接和执行时间过长的 SQL 语句。例如，设置 `sessionVariables=wait_timeout=3600（1 小时）`和 `sessionVariables=max_execution_time=300000（5 分钟）`。



# 引用文档

---
title: Bookshop 应用
summary: Bookshop 应用设计、数据导入、连接数据库等操作。
---

## Bookshop 应用

Bookshop 是一个虚拟的在线书店应用，你可以在 Bookshop 当中便捷地购买到各种类别的书，也可以对你看过的书进行点评。

为了方便你阅读应用开发指南中的内容，我们将以 Bookshop 应用的[数据表结构](#数据表详解)和数据为基础来编写示例 SQL。本章节将为你介绍如何导入该应用的表结构和数据，以及其数据表结构的定义。

### 导入表结构和数据

你可以[通过 TiUP](#方法一通过-tiup-demo-命令行) 或[通过 TiDB Cloud Import](#方法二通过-tidb-cloud-import-功能) 两种方式导入 Bookshop 应用的表结构和数据。

#### 方法一：通过 `tiup demo` 命令行

如果你使用 TiUP 部署 TiDB 集群或者你可以直接连接到你的 TiDB 服务器，你可以通过如下命令快速生成并导入 Bookshop 应用的示例数据：



```shell
tiup demo bookshop prepare
```

该命令默认会连接到 `127.0.0.1` 地址上的 `4000` 端口，使用 `root` 用户名进行无密码登录，默认在名为 `bookshop` 的数据库中创建[表结构](#数据表详解)。

##### 配置连接信息

你可以通过如下参数修改默认的连接信息：

| 参数         | 简写 | 默认值      | 解释           |
| ------------ | ---- | ----------- | -------------- |
| `--host`     | `-H` | `127.0.0.1` | 数据库地址     |
| `--port`     | `-P` | `4000`      | 数据库端口     |
| `--user`     | `-U` | `root`      | 数据库用户     |
| `--password` | `-p` | 无          | 数据库用户密码 |
| `--db`       | `-D` | `bookshop`  | 数据库名称     |

例如，你想要连接到 TiDB Cloud 上的数据库，你可以如下命令指定连接信息进行连接：



```shell
tiup demo bookshop prepare -U <username> -H <endpoint> -P 4000 -p <password>
```

##### 设置数据量

另外，你还可以通过如下参数指定各个数据库表生成的数据量：

| 参数        | 默认值   | 解释                              |
| ----------- | -------- | --------------------------------- |
| `--users`   | `10000`  | 指定在 `users` 表生成的数据行数   |
| `--authors` | `20000`  | 指定在 `authors` 表生成的数据行数 |
| `--books`   | `20000`  | 指定在 `books` 表生成的数据行数   |
| `--orders`  | `300000` | 指定在 `orders` 表生成的数据行数  |
| `--ratings` | `300000` | 指定在 `ratings` 表生成的数据行数 |

例如，以下命令通过 `--users` 参数指定生成 20 万行用户信息，通过 `--books` 参数指定生成 50 万行书籍的基本信息，通过 `--authors` 参数指定生成 10 万的作者信息，通过 `--ratings` 参数指定生成 100 万的评分记录，通过 `--orders` 参数指定生成 100 万的订单记录。

```shell
tiup demo bookshop prepare --users=200000 --books=500000 --authors=100000 --ratings=1000000 --orders=1000000 --drop-tables
```

通过 `--drop-tables` 参数你可以删除原有的表结构，更多的参数说明你可以通过命令 `tiup demo bookshop --help` 进行了解。

#### 方法二：通过 TiDB Cloud Import 功能

在 TiDB Cloud 的集群详情页面，你可以通过切换到 **Import** 标签页，点击 **Import Data** 按钮进入到 **Data Import** 页面。在该页面当中，按照以下步骤将 Bookshop 示例数据从 AWS S3 中导入到你的 TiDB Cloud 集群：

1. 选择 **Data Format** 为 **SQL File**。
2. 将以下 **Bucket URI** 和 **Role ARN** 复制到页面上对应的输入框当中：

    **Bucket URI**:

    ```
    s3://developer.pingcap.com/bookshop/
    ```

    **Role ARN**:

    ```
    arn:aws:iam::494090988690:role/s3-tidb-cloud-developer-access
    ```

3. 点击 **Next** 按钮切换到 **Choose the tables to be imported** 步骤确认将要导入的文件的信息。

4. 点击 **Next** 按钮切换到 **Preview** 步骤确认将要导入的示例数据是否正确。

    在这个示例数据当中，预先生成了 20 万的用户信息、50 万条书籍信息、10 万条作者信息、100 万条评分记录以及 100 万条订单信息。

5. 点击 **Start Import** 按钮开始导入数据，等待 TiDB Cloud 完成数据导入。

你可以通过 [TiDB Cloud Migration Overview](https://docs.pingcap.com/tidbcloud/tidb-cloud-migration-overview) 文档获取更多有关 TiDB Cloud 数据导入和迁移的信息。

#### 查看数据导入情况

导入完成后，你可以通过下面的 SQL 语句查看各个表的数据量信息：

```sql
SELECT
    CONCAT(table_schema,'.',table_name) AS 'Table Name',
    table_rows AS 'Number of Rows',
    CONCAT(ROUND(data_length/(1024*1024*1024),4),'G') AS 'Data Size',
    CONCAT(ROUND(index_length/(1024*1024*1024),4),'G') AS 'Index Size',
    CONCAT(ROUND((data_length+index_length)/(1024*1024*1024),4),'G') AS 'Total'
FROM
    information_schema.TABLES
WHERE table_schema LIKE 'bookshop';
```

运行结果为：

```
+-----------------------+----------------+-----------+------------+---------+
| Table Name            | Number of Rows | Data Size | Index Size | Total   |
+-----------------------+----------------+-----------+------------+---------+
| bookshop.orders       |        1000000 | 0.0373G   | 0.0075G    | 0.0447G |
| bookshop.book_authors |        1000000 | 0.0149G   | 0.0149G    | 0.0298G |
| bookshop.ratings      |        4000000 | 0.1192G   | 0.1192G    | 0.2384G |
| bookshop.authors      |         100000 | 0.0043G   | 0.0000G    | 0.0043G |
| bookshop.users        |         195348 | 0.0048G   | 0.0021G    | 0.0069G |
| bookshop.books        |        1000000 | 0.0546G   | 0.0000G    | 0.0546G |
+-----------------------+----------------+-----------+------------+---------+
6 rows in set (0.03 sec)
```

### 数据表详解

以下将详细介绍 Bookshop 应用程序的数据库表结构：

#### `books` 表

该表用于存储书籍的基本信息。

| 字段名        | 类型          | 含义                                  |
|--------------|---------------|---------------------------------------|
| id           | bigint(20)    | 书籍的唯一标识                        |
| title        | varchar(100)  | 书籍名称                              |
| type         | enum          | 书籍类型（如：杂志 / 动漫 / 教辅 等）    |
| stock        | bigint(20)    | 库存                                  |
| price        | decimal(15,2) | 价格                                  |
| published_at | datetime      | 出版时间                              |

#### `authors` 表

该表用于存储作者的基本信息。

| 字段名      | 类型         | 含义                                |
|------------|--------------|-------------------------------------|
| id         | bigint(20)   | 作者的唯一标识                       |
| name       | varchar(100) | 姓名                                |
| gender     | tinyint(1)   | 生理性别 (0: 女, 1: 男，NULL: 未知)   |
| birth_year | smallint(6)  | 生年                                |
| death_year | smallint(6)  | 卒年                                |

#### `users` 表

该表用于存储使用 Bookshop 应用程序的用户。

| 字段名    | 类型          | 含义            |
|----------|---------------|----------------|
| id       | bigint(20)    | 用户的唯一标识   |
| balance  | decimal(15,2) | 余额           |
| nickname | varchar(100)  | 昵称           |

#### `ratings` 表

该表用于存储用户对书籍的评分记录。

| 字段名    | 类型     | 含义                                        |
|----------|----------|---------------------------------------------|
| book_id  | bigint   | 书籍的唯一标识（关联至 [books](#books-表)）     |
| user_id  | bigint   | 用户的唯一标识（关联至 [users](#users-表)）    |
| score    | tinyint  | 用户评分 (1-5)                              |
| rated_at | datetime | 评分时间                                    |

#### `book_authors` 表

一个作者可能会编写多本书，一本书可能需要多个作者同时编写，该表用于存储书籍与作者之间的对应关系。

| 字段名     | 类型       | 含义                                        |
|-----------|------------|--------------------------------------------|
| book_id   | bigint(20) | 书籍的唯一标识（关联至 [books](#books-表)）     |
| author_id | bigint(20) | 作者的唯一标识（关联至 [authors](#authors-表)） |

#### `orders` 表

该表用于存储用户购买书籍的订单信息。

| 字段名      | 类型       | 含义                                        |
|------------|------------|--------------------------------------------|
| id         | bigint(20) | 订单的唯一标识                               |
| book_id    | bigint(20) | 书籍的唯一标识（关联至 [books](#books-表)）    |
| user_id    | bigint(20) | 用户唯一标识（关联至 [users](#users-表)）      |
| quantity   | tinyint(4) | 购买数量                                    |
| ordered_at | datetime   | 购买时间                                    |

### 数据库初始化 `dbinit.sql` 脚本

如果你希望手动创建 Bookshop 应用的数据库表结构，你可以运行以下 SQL 语句：

```sql
CREATE DATABASE IF NOT EXISTS `bookshop`;

DROP TABLE IF EXISTS `bookshop`.`books`;
CREATE TABLE `bookshop`.`books` (
  `id` bigint(20) AUTO_RANDOM NOT NULL,
  `title` varchar(100) NOT NULL,
  `type` enum('Magazine', 'Novel', 'Life', 'Arts', 'Comics', 'Education & Reference', 'Humanities & Social Sciences', 'Science & Technology', 'Kids', 'Sports') NOT NULL,
  `published_at` datetime NOT NULL,
  `stock` int(11) DEFAULT '0',
  `price` decimal(15,2) DEFAULT '0.0',
  PRIMARY KEY (`id`) CLUSTERED
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

DROP TABLE IF EXISTS `bookshop`.`authors`;
CREATE TABLE `bookshop`.`authors` (
  `id` bigint(20) AUTO_RANDOM NOT NULL,
  `name` varchar(100) NOT NULL,
  `gender` tinyint(1) DEFAULT NULL,
  `birth_year` smallint(6) DEFAULT NULL,
  `death_year` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`id`) CLUSTERED
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

DROP TABLE IF EXISTS `bookshop`.`book_authors`;
CREATE TABLE `bookshop`.`book_authors` (
  `book_id` bigint(20) NOT NULL,
  `author_id` bigint(20) NOT NULL,
  PRIMARY KEY (`book_id`,`author_id`) CLUSTERED
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

DROP TABLE IF EXISTS `bookshop`.`ratings`;
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `score` tinyint NOT NULL,
  `rated_at` datetime NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED,
  UNIQUE KEY `uniq_book_user_idx` (`book_id`,`user_id`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
ALTER TABLE `bookshop`.`ratings` SET TIFLASH REPLICA 1;

DROP TABLE IF EXISTS `bookshop`.`users`;
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM NOT NULL,
  `balance` decimal(15,2) DEFAULT '0.0',
  `nickname` varchar(100) UNIQUE NOT NULL,
  PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

DROP TABLE IF EXISTS `bookshop`.`orders`;
CREATE TABLE `bookshop`.`orders` (
  `id` bigint(20) AUTO_RANDOM NOT NULL,
  `book_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `quality` tinyint(4) NOT NULL,
  `ordered_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) CLUSTERED,
  KEY `orders_book_id_idx` (`book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
```



## 规范

---
title: 对象命名规范
summary: 介绍 TiDB 中的对象命名规范。
---

### 对象命名规范

用于规范数据库对象的命名，如数据库（DATABASE）、表（TABLE）、索引（INDEX）、用户（USER）等的命名约定。

#### 原则

- 命名建议使用具有意义的英文词汇，词汇中间以下划线分隔。
- 命名只能使用英文字母、数字、下划线。
- 避免用 TiDB 的保留字如：group，order 等作为单个字段名。
- 建议所有数据库对象使用小写字母。

#### 数据库命名规范

建议按照业务、产品线或者其它指标进行区分，一般不要超过 20 个字符。如：临时库 (tmp_crm)、测试库 (test_crm) 。

#### 表命名规范

- 同一业务或者模块的表尽可能使用相同的前缀，表名称尽可能表达含义。
- 多个单词以下划线分隔，不推荐超过 32 个字符。
- 建议对表的用途进行注释说明，以便于统一认识。如：
    - 临时表（tmp_t_crm_relation_0425）
    - 备份表（bak_t_crm_relation_20170425）
    - 业务运营临时统计表（`tmp_st_{business code}_{creator abbreviation}_{date}`）
    - 账期归档表（`t_crm_ec_record_YYYY{MM}{dd}`）
- 不同业务模块的表单独建立 DATABASE，并增加相应注释。

#### 字段命名规范

- 字段命名需要表示其实际含义的英文单词或简写。
- 建议各表之间相同意义的字段应同名。
- 字段也尽量添加注释，枚举型需指明主要值的含义，如”0 - 离线，1 - 在线”。
- 布尔值列命名为 `is_{description}`。如 member 表上表示为 enabled 的会员的列命名为 is_enabled。
- 字段名不建议超过 30 个字符，字段个数不建议大于 60。
- 尽量避免使用保留字，如 order、from、desc 等，请参考附录部分的官方保留字。

#### 索引命名规范

- 主键索引：`pk_{表名称简写}_{字段名简写}`
- 唯一索引：`uk_{表名称简写}_{字段名简写}`
- 普通索引：`idx_{表名称简写}_{字段名简写}`
- 多单词组成的 column_name，取尽可能代表意义的缩写。


---
title: SQL 开发规范
summary: TiDB 的 SQL 开发规范。
---

### SQL 开发规范

本章将介绍一些使用 SQL 的一般化开发规范。

#### 建表删表规范

- 基本原则：表的建立在遵循表命名规范前提下，建议业务应用内部封装建表删表语句增加判断逻辑，防止业务流程异常中断。
- 详细说明：`create table if not exists table_name` 或者 `drop table if exists table_name` 语句建议增加 if 判断，避免应用侧由于 SQL 命令运行异常造成的异常中断。

#### SELECT \* 使用规范

- 基本原则：避免使用 SELECT \* 进行查询。
- 详细说明：按需求选择合适的字段列，避免盲目地 SELECT \* 读取全部字段，因为其会消耗网络带宽。考虑将被查询的字段也加入到索引中，以有效利用覆盖索引功能。

#### 字段上使用函数规范

- 基本原则：在取出字段上可以使用相关函数,但是在 Where 条件中的过滤条件字段上避免使用任何函数,包括数据类型转换函数，以避免索引失效。或者可以考虑使用表达式索引功能。
- 详细说明：

    不推荐的写法：

    

    ```sql
    SELECT gmt_create
    FROM ...
    WHERE DATE_FORMAT(gmt_create, '%Y%m%d %H:%i:%s') = '20090101 00:00:00'
    ```

    推荐的写法：

    

    ```sql
    SELECT DATE_FORMAT(gmt_create，'%Y%m%d %H:%i:%s')
    FROM ...
    WHERE gmt_create = str_to_date('20090101 00:00:00', '%Y%m%d %H:%i:%s')
    ```

#### 其他规范

- WHERE 条件中不要在索引列上进行数学运算或函数运算。
- 用 in/union 替换 or，并注意 in 的个数小于 300。
- 避免使用 %前缀进行模糊前缀查询。
- 如应用使用 Multi Statements 执行 SQL，即将多个 SQL 使用分号连接，一次性地发给客户端执行，TiDB 只会返回第一个 SQL 的执行结果。
- 当使用表达式时，检查其是否支持计算下推到存储层的功能 (TiKV、TiFlash)，否则应有预期 在 TiDB 层需要消耗更多内存、甚至 OOM。计算下推到存储层的功能列表如下：
    - TiFlash 支持的计算下推清单。
    - 下推到 TiKV 的表达式列表。
    - 谓词下推。



# 云原生开发环境

---
title: Gitpod
---

<!-- markdownlint-disable MD029 -->

## Gitpod

使用 [Gitpod](https://www.gitpod.io/)，只需单击一个按钮或链接即可在浏览器中获得完整的开发环境，并且可以立即编写代码。

Gitpod 是一个开源 Kubernetes 应用程序（GitHub 仓库地址 <https://github.com/gitpod-io/gitpod>)，适用于可直接编写代码的开发环境，可为云中的每个任务提供全新的自动化开发环境，非常迅速。此外，Gitpod 能够将你的开发环境描述为代码，并直接从你的浏览器或桌面 IDE 启动即时、远程和基于云的开发环境。

### 快速开始

1. Fork 出 TiDB 应用开发的示例代码仓库 [pingcap-inc/tidb-example-java](https://github.com/pingcap-inc/tidb-example-java)。

2. 通过浏览器的地址栏，在示例代码仓库的 URL 前加上 `https://gitpod.io/#` 来启动你的 gitpod 工作区。

    - 例如，`https://gitpod.io/#https://github.com/pingcap-inc/tidb-example-java`。

    - 支持在 URL 中配置环境变量。例如，`https://gitpod.io/#targetFile=spring-jpa-hibernate_Makefile,targetMode=spring-jpa-hibernate/https://github.com/pingcap-inc/tidb-example-java`。

3. 使用列出的提供商之一登录并启动工作区，例如，`Github`。

### 使用默认的 Gitpod 配置和环境

完成[快速开始](#快速开始) 的步骤之后，Gitpod 会需要一段时间来设置你的工作区。

以 [Spring Boot Web](#使用-spring-boot-构建-tidb-应用程序) 应用程序为例，通过 URL `https://gitpod.io/#targetFile=spring-jpa-hibernate_Makefile,targetMode=spring-jpa-hibernate/https://github.com/pingcap-inc/tidb-example-java` 可以创建一个新工作区。

完成后，你将看到如下所示的页面。

![playground gitpod workspace init](./media/develop/playground-gitpod-workspace-init.png)

页面中的这个场景使用了 [TiUP](https://docs.pingcap.com/zh/tidb/stable/tiup-overview) 来搭建一个 TiDB Playground。你可以在终端的左侧查看进度。

一旦 TiDB Playground 准备就绪，另一个 `Spring JPA Hibernate` 任务将运行。 你可以在终端的右侧查看进度。

完成所有任务后，你可以看到如下所示的页面，并在左侧导航栏的 `REMOTE EXPLORER` 中找到你的端口 `8080` URL（Gitpod 支持基于 URL 的端口转发）。

![playground gitpod workspace ready](./media/develop/playground-gitpod-workspace-ready.png)

你可以按照[该指南](#第-6-步http-请求)测试 API。注意请将 URL `http://localhost:8080` 替换为你在 `REMOTE EXPLORER` 中找到的那个。

### 使用自定义的 Gitpod 配置和 Docker 镜像

#### 自定义 Gitpod 配置

在项目的根目录中，参考[示例 .gitpod.yml](https://github.com/pingcap-inc/tidb-example-java/blob/main/.gitpod.yml)，创建一个 `.gitpod.yml` 文件用于配置 Gitpod 工作空间。

```yml
## This configuration file was automatically generated by Gitpod.
## Please adjust to your needs (see https://www.gitpod.io/docs/config-gitpod-file)
## and commit this file to your remote git repository to share the goodness with others.

## image:
##   file: .gitpod.Dockerfile

tasks:
  - name: Open Target File
    command: |
      if [ -n "$targetFile" ]; then code ${targetFile//[_]//};  fi
  - name: TiUP init playground
    command: |
      $HOME/.tiup/bin/tiup playground
  - name: Test Case
    openMode: split-right
    init: echo "*** Waiting for TiUP Playground Ready! ***"
    command: |
      gp await-port 3930
      if [ "$targetMode" == "plain-java-jdbc" ]
      then
        cd plain-java-jdbc
        code src/main/resources/dbinit.sql
        code src/main/java/com/pingcap/JDBCExample.java
        make mysql
      elif [ "$targetMode" == "plain-java-hibernate" ]
      then
        cd plain-java-hibernate
        make
      elif [ "$targetMode" == "spring-jpa-hibernate" ]
      then
        cd spring-jpa-hibernate
        make
      fi
ports:
  - port: 8080
    visibility: public
  - port: 4000
    visibility: public
  - port: 2379-36663
    onOpen: ignore
```

#### 自定义 Gitpod Docker 镜像

默认情况下，Gitpod 使用名为 Workspace-Full 的标准 Docker 镜像作为工作空间的基础。 基于此默认镜像启动的工作区预装了 Docker、Go、Java、Node.js、C/C++、Python、Ruby、Rust、PHP 以及 Homebrew、Tailscale、Nginx 等工具。

你可以提供公共 Docker 镜像或 Dockerfile。 并为你的项目安装所需的任何依赖项。

这是一个 Dockerfile 示例：[示例 .gitpod.Dockerfile](https://github.com/pingcap-inc/tidb-example-java/blob/main/.gitpod.Dockerfile)

```dockerfile
FROM gitpod/workspace-java-17

RUN sudo apt install mysql-client -y
RUN curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
```

然后需要更新`.gitpod.yml`：

```yml
## This configuration file was automatically generated by Gitpod.
## Please adjust to your needs (see https://www.gitpod.io/docs/config-gitpod-file)
## and commit this file to your remote git repository to share the goodness with others.

image:
  # 在这里导入你的 Dockerfile
  file: .gitpod.Dockerfile

tasks:
  - name: Open Target File
    command: |
      if [ -n "$targetFile" ]; then code ${targetFile//[_]//};  fi
  - name: TiUP init playground
    command: |
      $HOME/.tiup/bin/tiup playground
  - name: Test Case
    openMode: split-right
    init: echo "*** Waiting for TiUP Playground Ready! ***"
    command: |
      gp await-port 3930
      if [ "$targetMode" == "plain-java-jdbc" ]
      then
        cd plain-java-jdbc
        code src/main/resources/dbinit.sql
        code src/main/java/com/pingcap/JDBCExample.java
        make mysql
      elif [ "$targetMode" == "plain-java-hibernate" ]
      then
        cd plain-java-hibernate
        make
      elif [ "$targetMode" == "spring-jpa-hibernate" ]
      then
        cd spring-jpa-hibernate
        make
      fi
ports:
  - port: 8080
    visibility: public
  - port: 4000
    visibility: public
  - port: 2379-36663
    onOpen: ignore
```

#### 应用更改

完成对 `.gitpod.yml` 文件配置后，请保证最新的代码已在你对应的 GitHub 代码仓库中可用。

访问 `https://gitpod.io/#<YOUR_REPO_URL>` 以建立新的 Gitpod 工作区，新工作区会应用最新的代码。

访问 `https://gitpod.io/workspaces` 以获取所有建立的工作区。

### 总结

Gitpod 提供了完整的、自动化的、预配置的云原生开发环境。无需本地配置，你可以直接在浏览器中开发、运行、测试代码。

![playground gitpod summary](./media/develop/playground-gitpod-summary.png)



# 第三方工具支持

---
title: TiDB 支持的第三方工具
---

## TiDB 支持的第三方工具

> **注意：**
>
> 本文档仅列举了常见的 TiDB 支持的第三方工具，未被列入其中的第三方工具并非代表不支持，但 PingCAP 无法了解其是否使用到 TiDB 不支持的特性，从而无法保证兼容性。

TiDB 高度兼容 MySQL 协议，使得大部分适配 MySQL 的 Driver、ORM 及其他工具与 TiDB 兼容。本文主要介绍这些工具和它们的支持等级。

### 支持等级

PingCAP 与开源社区合作，通过三方工具提供以下支持：

- Full：表明 PingCAP 已经支持该工具的绝大多数功能兼容性，并且在新版本中对其保持兼容，将定期地对下表中记录的新版本进行兼容性测试。
- Compatible：表明由于该工具已适配 MySQL，而 TiDB 高度兼容 MySQL 协议，因此可以使用此工具的大部分功能。但 PingCAP 并未对该工具作出完整的兼容性验证，有可能出现一些意外的行为。

> **注意：**
>
> 除非明确说明，否则对于支持的 Driver 或者 ORM 框架并不包括[应用端事务重试和错误处理](#应用端重试和错误处理)。

如果在使用本文列出的工具连接 TiDB 时出现问题，请在 GitHub 上提交包含详细信息的 [issue](https://github.com/pingcap/tidb/issues/new?assignees=&labels=type%2Fquestion&template=general-question.md)，以帮助在此工具的支持上得到进展。

### Driver

<table>
   <thead>
      <tr>
         <th>编程语言</th>
         <th>驱动</th>
         <th>最新已测试版本</th>
         <th>支持等级</th>
         <th>TiDB 适配器</th>
         <th>教程</th>
      </tr>
   </thead>
   <tbody>
      <tr>
         <td>C</td>
         <td><a href="https://dev.mysql.com/doc/c-api/8.0/en/c-api-introduction.html" target="_blank" referrerpolicy="no-referrer-when-downgrade">libmysqlclient</a></td>
         <td>8.0</td>
         <td>Compatible</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td>C#(.Net)</td>
         <td><a href="https://downloads.mysql.com/archives/c-net/" target="_blank" referrerpolicy="no-referrer-when-downgrade">MySQL Connector/NET</a></td>
         <td>8.0</td>
         <td>Compatible</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td>ODBC</td>
         <td><a href="https://downloads.mysql.com/archives/c-odbc/" target="_blank" referrerpolicy="no-referrer-when-downgrade">MySQL Connector/ODBC</a></td>
         <td>8.0</td>
         <td>Compatible</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td>Go</td>
         <td><a href="https://github.com/go-sql-driver/mysql" target="_blank" referrerpolicy="no-referrer-when-downgrade">go-sql-driver/mysql</a></td>
         <td>v1.6.0</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/zh/tidb/dev/dev-guide-sample-application-golang">TiDB 和 Golang 的简单 CRUD 应用程序</a></td>
      </tr>
      <tr>
         <td>Java</td>
         <td><a href="https://dev.mysql.com/downloads/connector/j/" target="_blank" referrerpolicy="no-referrer-when-downgrade">JDBC</a></td>
         <td>8.0</td>
         <td>Full</td>
         <td>
            <ul>
               <li><a href="/zh/tidb/dev/dev-guide-choose-driver-or-orm#java-drivers" data-href="/zh/tidb/dev/dev-guide-choose-driver-or-orm#java-drivers">pingcap/mysql-connector-j</a></li>
               <li><a href="/zh/tidb/dev/dev-guide-choose-driver-or-orm#tidb-loadbalance" data-href="/zh/tidb/dev/dev-guide-choose-driver-or-orm#tidb-loadbalance">pingcap/tidb-loadbalance</a></li>
            </ul>
         </td>
         <td><a href="/zh/tidb/dev/dev-guide-sample-application-java">TiDB 和 Java 的简单 CRUD 应用程序</a></td>
      </tr>
      <tr>
         <td>JavaScript</td>
         <td><a href="https://github.com/mysqljs/mysql" target="_blank" referrerpolicy="no-referrer-when-downgrade">mysql</a></td>
         <td>v2.18.1</td>
         <td>Compatible</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td>PHP</td>
         <td><a href="https://dev.mysql.com/downloads/connector/php-mysqlnd/" target="_blank" referrerpolicy="no-referrer-when-downgrade">mysqlnd</a></td>
         <td>PHP 5.4+</td>
         <td>Compatible</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td rowspan="3">Python</td>
         <td><a href="https://dev.mysql.com/doc/connector-python/en/" target="_blank" referrerpolicy="no-referrer-when-downgrade">mysql-connector-python</a></td>
         <td>8.0</td>
         <td>Compatible</td>
         <td>N/A</td>
         <td><a href="/zh/tidb/dev/dev-guide-sample-application-python">TiDB 和 Python 的简单 CRUD 应用程序</a></td>
      </tr>
      <tr>
         <td><a href="https://mysqlclient.readthedocs.io/" target="_blank" referrerpolicy="no-referrer-when-downgrade">mysqlclient</a></td>
         <td>2.1.1</td>
         <td>Compatible</td>
         <td>N/A</td>
         <td><a href="/zh/tidb/dev/dev-guide-sample-application-python">TiDB 和 Python 的简单 CRUD 应用程序</a></td>
      </tr>
      <tr>
         <td><a href="https://pypi.org/project/PyMySQL/" target="_blank" referrerpolicy="no-referrer-when-downgrade">PyMySQL</a></td>
         <td>1.0.2</td>
         <td>Compatible</td>
         <td>N/A</td>
         <td><a href="/zh/tidb/dev/dev-guide-sample-application-python">TiDB 和 Python 的简单 CRUD 应用程序</a></td>
      </tr>
   </tbody>
</table>

### ORM

<table>
   <thead>
      <tr>
         <th>编程语言</th>
         <th>ORM 框架</th>
         <th>最新已测试版本</th>
         <th>支持等级</th>
         <th>TiDB 适配器</th>
         <th>教程</th>
      </tr>
   </thead>
   <tbody>
      <tr>
         <td rowspan="5">Go</td>
         <td><a href="https://github.com/go-gorm/gorm" target="_blank" referrerpolicy="no-referrer-when-downgrade">gorm</a></td>
         <td>v1.23.5</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/zh/tidb/dev/dev-guide-sample-application-golang">TiDB 和 Golang 的简单 CRUD 应用程序</a></td>
      </tr>
      <tr>
         <td><a href="https://github.com/beego/beego" target="_blank" referrerpolicy="no-referrer-when-downgrade">beego</a></td>
         <td>v2.0.3</td>
         <td>Full</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td><a href="https://github.com/upper/db" target="_blank" referrerpolicy="no-referrer-when-downgrade">upper/db</a></td>
         <td>v4.5.2</td>
         <td>Full</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td><a href="https://gitea.com/xorm/xorm" target="_blank" referrerpolicy="no-referrer-when-downgrade">xorm</a></td>
         <td>v1.3.1</td>
         <td>Full</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td><a href="https://github.com/ent/ent" target="_blank" referrerpolicy="no-referrer-when-downgrade">ent</a></td>
         <td>v0.11.0</td>
         <td>Compatible</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td rowspan="4">Java</td>
         <td><a href="https://hibernate.org/orm/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Hibernate</a></td>
         <td>6.1.0.Final</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/zh/tidb/dev/dev-guide-sample-application-java">TiDB 和 Java 的简单 CRUD 应用程序</a></td>
      </tr>
      <tr>
         <td><a href="https://mybatis.org/mybatis-3/" target="_blank" referrerpolicy="no-referrer-when-downgrade">MyBatis</a></td>
         <td>v3.5.10</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/zh/tidb/dev/dev-guide-sample-application-java">TiDB 和 Java 的简单 CRUD 应用程序</a></td>
      </tr>
      <tr>
         <td><a href="https://spring.io/projects/spring-data-jpa/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Spring Data JPA</a></td>
         <td>2.7.2</td>
         <td>Full</td>
         <td>N/A</td>
         <td><a href="/zh/tidb/dev/dev-guide-sample-application-spring-boot">使用 Spring Boot 构建 TiDB 应用程序</a></td>
      </tr>
      <tr>
         <td><a href="https://github.com/jOOQ/jOOQ" target="_blank" referrerpolicy="no-referrer-when-downgrade">jOOQ</a></td>
         <td>v3.16.7 (Open Source)</td>
         <td>Full</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td>Ruby</td>
         <td><a href="https://guides.rubyonrails.org/active_record_basics.html" target="_blank" referrerpolicy="no-referrer-when-downgrade">Active Record</a></td>
         <td>v7.0</td>
         <td>Full</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td rowspan="4">JavaScript / TypeScript</td>
         <td><a href="https://www.npmjs.com/package/sequelize" target="_blank" referrerpolicy="no-referrer-when-downgrade">sequelize</a></td>
         <td>v6.20.1</td>
         <td>Compatible</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td><a href="https://knexjs.org/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Knex.js</a></td>
         <td>v1.0.7</td>
         <td>Compatible</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td><a href="https://www.prisma.io/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Prisma Client</a></td>
         <td>3.15.1</td>
         <td>Compatible</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td><a href="https://www.npmjs.com/package/typeorm" target="_blank" referrerpolicy="no-referrer-when-downgrade">TypeORM</a></td>
         <td>v0.3.6</td>
         <td>Compatible</td>
         <td>N/A</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td>PHP</td>
         <td><a href="https://laravel.com/" target="_blank" referrerpolicy="no-referrer-when-downgrade">laravel</a></td>
         <td>v9.1.10</td>
         <td>Compatible</td>
         <td><a href="https://github.com/colopl/laravel-tidb" target="_blank" referrerpolicy="no-referrer-when-downgrade">laravel-tidb</a></td>
         <td>N/A</td>
      </tr>
      <tr>
         <td rowspan="4">Python</td>
         <td><a href="https://pypi.org/project/Django/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Django</a></td>
         <td>v4.0.5</td>
         <td>Compatible</td>
         <td><a href="https://github.com/pingcap/django-tidb" target="_blank" referrerpolicy="no-referrer-when-downgrade">django-tidb</a></td>
         <td>N/A</td>
      </tr>
      <tr>
         <td><a href="https://github.com/coleifer/peewee/" target="_blank" referrerpolicy="no-referrer-when-downgrade">peewee</a></td>
         <td>v3.14.10</td>
         <td>Compatible</td>
         <td>N/A</td>
         <td><a href="/zh/tidb/dev/dev-guide-sample-application-python">TiDB 和 Python 的简单 CRUD 应用程序</a></td>
      </tr>
      <tr>
         <td><a href="https://www.sqlalchemy.org/" target="_blank" referrerpolicy="no-referrer-when-downgrade">SQLAlchemy</a></td>
         <td>v1.4.37</td>
         <td>Compatible</td>
         <td>N/A</td>
         <td><a href="/zh/tidb/dev/dev-guide-sample-application-python">TiDB 和 Python 的简单 CRUD 应用程序</a></td>
      </tr>
   </tbody>
</table>

### GUI

| GUI | 最新已测试版本 | 支持等级 | 教程 |
| - | - | - | - |
| [DBeaver](https://dbeaver.io/) | 22.1.0 | Compatible | N/A |
| [Navicat for MySQL](https://www.navicat.com/) | 16.0.14 | Compatible | N/A |
| [MySQL Workbench](https://www.mysql.com/products/workbench/) | 8.0 | Compatible | N/A |

<table>
   <thead>
      <tr>
         <th>IDE</th>
         <th>插件</th>
         <th>支持等级</th>
         <th>教程</th>
      </tr>
   </thead>
   <tbody>
      <tr>
         <td><a href="https://www.jetbrains.com/datagrip/" target="_blank" referrerpolicy="no-referrer-when-downgrade">DataGrip</a></td>
         <td>N/A</td>
         <td>Compatible</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td><a href="https://www.jetbrains.com/idea/" target="_blank" referrerpolicy="no-referrer-when-downgrade">IntelliJ IDEA</a></td>
         <td>N/A</td>
         <td>Compatible</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td rowspan="2"><a href="https://code.visualstudio.com/" target="_blank" referrerpolicy="no-referrer-when-downgrade">Visual Studio Code</a></td>
         <td><a href="https://marketplace.visualstudio.com/items?itemName=dragonly.ticode" target="_blank" referrerpolicy="no-referrer-when-downgrade">TiDE</a></td>
         <td>Compatible</td>
         <td>N/A</td>
      </tr>
      <tr>
         <td><a href="https://marketplace.visualstudio.com/items?itemName=formulahendry.vscode-mysql" target="_blank" referrerpolicy="no-referrer-when-downgrade">MySQL</a></td>
         <td>Compatible</td>
         <td>N/A</td>
      </tr>
   </tbody>
</table>


---
title: 已知的第三方工具兼容问题
summary: 介绍在测试中发现的 TiDB 与第三方工具的兼容性问题。
---

## 已知的第三方工具兼容问题

> **注意：**
>
> TiDB 已列举不支持的功能特性，典型的不支持特性有：
>
> - 存储过程与函数
> - 触发器
> - 事件
> - 自定义函数
> - 外键约束
> - 空间类型的函数、数据类型和索引
> - `XA` 语法
>
> 这些不支持的功能不兼容将被视为预期行为，不再重复叙述。关于更多 TiDB 与 MySQL 的兼容性对比，你可以查看与 MySQL 兼容性对比。

### 通用

#### TiDB 中 `SELECT CONNECTION_ID()` 返回结果类型为 64 位整型

**描述**

TiDB 中 `SELECT CONNECTION_ID()` 的返回值为 64 位，如 `2199023260887`。而 MySQL 中返回值为 32 位，如 `391650`。

**规避方法**

在 TiDB 应用程序中，请注意使用各语言的 64 位整型类型（或字符串类型）存储 `SELECT CONNECTION_ID()` 的结果，防止溢出。如 Java 应使用 `Long` 或 `String` 进行接收，JavaScript/TypeScript 应使用 `string` 类型进行接收。

#### TiDB 未设置 `Com_*` 计数器

**描述**

MySQL 维护了一系列 [`Com_` 开头的服务端变量](https://dev.mysql.com/doc/refman/8.0/en/server-status-variables.html#statvar_Com_xxx)来记录你对数据库的操作总数，如 `Com_select` 记录了 MySQL 数据库从上次启动开始，总共发起的 `SELECT` 语句数（即使语句并未成功执行）。而 TiDB 并未维护此变量。你可以使用语句 [<code>SHOW GLOBAL STATUS LIKE 'Com_%'</code>](None) 观察 TiDB 与 MySQL 的差异。

**规避方法**

请勿使用这样的变量。在 MySQL 中 `Com_*` 常见的使用场景之一是监控。TiDB 的可观测性较为完善，无需从服务端变量进行查询。如需定制监控工具，可阅读 TiDB 监控框架概述来获得更多信息。

#### TiDB 错误日志区分 `TIMESTAMP` 与 `DATETIME` 类型

**描述**

TiDB 错误日志区分 `TIMESTAMP` 与 `DATETIME`，而 MySQL 不区分，全部返回为 `DATETIME`。即 MySQL 会将 `TIMESTAMP` 类型的报错信息错误地写为 `DATETIME` 类型。

**规避方法**

请勿使用错误日志进行字符串匹配，要使用错误码进行故障诊断。

#### TiDB 不支持 `CHECK TABLE` 语句

**描述**

TiDB 不支持 `CHECK TABLE` 语句。

**规避方法**

在 TiDB 中使用 [`ADMIN CHECK [TABLE|INDEX]`](None) 语句进行表中数据和对应索引的一致性校验。

### 与 MySQL JDBC 的兼容性

测试版本为 MySQL Connector/J 8.0.29。

#### 默认排序规则不一致

**描述**

MySQL Connector/J 的排序规则保存在客户端内，通过获取的服务端版本进行判别。

下表列出了已知的客户端与服务端排序规则不一致的字符集：

| 字符集 | 客户端默认排序规则 | 服务端默认排序规则 |
| --------- | -------------------- | ------------- |
| `ascii`   | `ascii_general_ci`   | `ascii_bin`   |
| `latin1`  | `latin1_swedish_ci`  | `latin1_bin`  |
| `utf8mb4` | `utf8mb4_0900_ai_ci` | `utf8mb4_bin` |

**规避方法**

在 TiDB 中手动设置排序规则，不要依赖客户端默认排序规则。客户端默认排序规则由 MySQL Connector/J 配置文件保存。

#### 参数 `NO_BACKSLASH_ESCAPES` 不生效

**描述**

TiDB 中 无法使用 `NO_BACKSLASH_ESCAPES` 参数从而不进行 `\` 字符的转义。已提 [issue](https://github.com/pingcap/tidb/issues/35302)。

**规避方法**

在 TiDB 中不搭配使用 `NO_BACKSLASH_ESCAPES` 与 `\`，而是使用 `\\` 编写 SQL 语句。

#### 未设置索引使用情况参数

**描述**

TiDB 在通讯协议中未设置 `SERVER_QUERY_NO_GOOD_INDEX_USED` 与 `SERVER_QUERY_NO_INDEX_USED` 参数。这将导致以下参数返回与实际不一致：

- `com.mysql.cj.protocol.ServerSession.noIndexUsed()`
- `com.mysql.cj.protocol.ServerSession.noGoodIndexUsed()`

**规避方法**

不使用 `noIndexUsed()` 与 `noGoodIndexUsed()` 函数。

#### 不支持 `enablePacketDebug` 参数

**描述**

TiDB 不支持 [enablePacketDebug](https://dev.mysql.com/doc/connector-j/8.0/en/connector-j-connp-props-debugging-profiling.html) 参数，这是一个 MySQL Connector/J 用于调试的参数，将保留数据包的 Buffer。这将导致连接的**意外关闭**，**请勿**打开。

**规避方法**

不设置 `enablePacketDebug` 参数。

#### 不支持 UpdatableResultSet

**描述**

TiDB 暂不支持 `UpdatableResultSet`，即请勿指定 `ResultSet.CONCUR_UPDATABLE` 参数，也不要在 `ResultSet` 内部进行数据更新。

**规避方法**

使用 `UPDATE` 语句进行数据更新，可使用事务保证数据一致性。

### MySQL JDBC Bug

#### `useLocalTransactionState` 和 `rewriteBatchedStatements` 同时开启将导致事务无法提交或回滚

**描述**

`useLocalTransactionState` 和 `rewriteBatchedStatements` 两参数同时开启时，将导致事务无法提交。你可以使用[代码](https://github.com/Icemap/tidb-java-gitpod/tree/reproduction-local-transaction-state-txn-error)复现。

**规避方法**

> **注意：**
>
> 已向 MySQL JDBC 报告此 Bug，可关注此 [Bug Report](https://bugs.mysql.com/bug.php?id=108643) 进行最新消息的跟踪。

请勿开启 `useLocalTransactionState`，这有可能导致事务无法提交或回滚。

#### Connector 无法兼容 5.7.5 版本以下的服务端

**描述**

MySQL Connector/J 8.0.29 在与 5.7.5 版本以下的 MySQL 服务端，或使用 5.7.5 版本以下 MySQL 服务端协议的数据库（如 TiDB 6.3.0 版本以下）同时使用时，将在某些情况下导致数据库连接的挂起。关于更多细节信息，可查看此 [Bug Report](https://bugs.mysql.com/bug.php?id=106252)。

**规避方法**

这是一个已知的问题，截至 2022 年 10 月 12 日，MySQL Connector/J 未合并修复代码。

TiDB 对其进行了两个维度的修复：

- 客户端方面：**pingcap/mysql-connector-j** 中修复了该 Bug，你可以使用 [pingcap/mysql-connector-j](https://github.com/pingcap/mysql-connector-j) 替换官方的 MySQL Connector/J。
- 服务端方面：TiDB v6.3.0 修复了此兼容性问题，你可以升级服务端至 v6.3.0 或以上版本。

### 与 Sequelize 的兼容性

本小节描述的兼容性信息基于 [Sequelize v6.21.4](https://www.npmjs.com/package/sequelize/v/6.21.4) 测试。

根据测试结果，TiDB 支持绝大部分 Sequelize 功能（[使用 `MySQL` 作为方言](https://sequelize.org/docs/v6/other-topics/dialect-specific-things/#mysql)），不支持的功能有：

- 不支持与外键约束相关的功能（包括多对多关联）。
- [不支持 `GEOMETRY`](https://github.com/pingcap/tidb/issues/6347) 相关。
- 不支持修改整数主键。
- 不支持 `PROCEDURE` 相关。
- 不支持 `READ-UNCOMMITTED` 和 `SERIALIZABLE` 隔离级别。
- 默认不允许修改列的 `AUTO_INCREMENT` 属性。
- 不支持 `FULLTEXT`、`HASH` 和 `SPATIAL` 索引。

#### 不支持修改整数主键

**描述**

不支持修改整数类型的主键，这是由于当主键为整数类型时，TiDB 使用其作为数据组织的索引。你可以在此 [Issue](https://github.com/pingcap/tidb/issues/18090) 或聚簇索引一节中获取更多信息。

#### 不支持 `READ-UNCOMMITTED` 和 `SERIALIZABLE` 隔离级别

**描述**

TiDB 不支持 `READ-UNCOMMITTED` 和 `SERIALIZABLE` 隔离级别。设置事务隔离级别为 `READ-UNCOMMITTED` 或 `SERIALIZABLE` 时将报错。

**规避方法**

仅使用 TiDB 支持的 `REPEATABLE-READ` 或 `READ-COMMITTED` 隔离级别。

如果你的目的是兼容其他设置 `SERIALIZABLE` 隔离级别的应用，但不依赖于 `SERIALIZABLE`，你可以设置 [`tidb_skip_isolation_level_check`](#tidb_skip_isolation_level_check) 为 `1`，此后如果对 `tx_isolation`（[`transaction_isolation`](#transaction_isolation) 别名）赋值一个 TiDB 不支持的隔离级别（`READ-UNCOMMITTED` 和 `SERIALIZABLE`），不会报错。

#### 默认不允许修改列的 `AUTO_INCREMENT` 属性

**描述**

默认不允许通过 `ALTER TABLE MODIFY` 或 `ALTER TABLE CHANGE` 来增加或移除某个列的 `AUTO_INCREMENT` 属性。

**规避方法**

参考 [`AUTO_INCREMENT` 的使用限制](#使用限制)。

设置 `@@tidb_allow_remove_auto_inc` 为 `true`，即可允许移除 `AUTO_INCREMENT` 属性。

#### 不支持 `FULLTEXT`、`HASH` 和 `SPATIAL` 索引

**描述**

TiDB 不支持 `FULLTEXT`、`HASH` 和 `SPATIAL` 索引。


---
title: TiDB 与 ProxySQL 集成
summary: 介绍 TiDB 与 ProxySQL 集成的方法。
---

## TiDB 与 ProxySQL 集成

本文以 CentOS 7 为例，简单介绍 **TiDB** 与 **ProxySQL** 的集成方法。如果你有其他系统的集成需求，可参考[快速体验](#4-快速体验)使用 Docker 及 Docker Compose 部署测试集成环境。你也可以参考以下链接，以获得更多信息：

- TiDB 文档
- [TiDB 应用开发文档](#开发者手册概览)
- [ProxySQL 官方文档](https://proxysql.com/documentation/)
- [TiDB 与 ProxySQL 的集成测试](https://github.com/Icemap/tidb-proxysql-integration-test)

### 1. 启动 TiDB

#### 测试环境

<SimpleTab groupId="startup-tidb">

<div label="TiDB Cloud" value="tidb-cloud">

请参考[使用 TiDB Cloud (Serverless Tier) 构建 TiDB 集群](#使用-tidb-cloud-(serverless-tier)-构建-tidb-集群)。

</div>

<div label="编译源码" value="source-code">

1. 下载 [TiDB](https://github.com/pingcap/tidb) 源码，进入 `tidb-server` 目录后，使用 `go build` 进行编译。

    ```shell
    git clone git@github.com:pingcap/tidb.git
    cd tidb/tidb-server
    go build
    ```

2. 使用配置文件 [`tidb-config.toml`](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/tidb-config.toml) 来启动 TiDB，命令如下所示：

    ```shell
    ${TIDB_SERVER_PATH} -config ./tidb-config.toml -store unistore -path "" -lease 0s > ${LOCAL_TIDB_LOG} 2>&1 &
    ```

    > **注意：**
    >
    > - 此处使用 `unistore` 作为存储引擎，这是 TiDB 的测试存储引擎，请仅在测试时使用它。
    > - `TIDB_SERVER_PATH`：上一步中使用 `go build` 编译的二进制文件位置，如你在 `/usr/local` 下进行上一步操作，那么此处的 `TIDB_SERVER_PATH` 应为 `/usr/local/tidb/tidb-server/tidb-server`。
    > - `LOCAL_TIDB_LOG`：输出 TiDB 日志的位置。

</div>

<div label="TiUP" value="tiup">

TiUP 在 TiDB 中承担着包管理器的角色，管理着 TiDB 生态下众多的组件，如 TiDB、PD、TiKV 等。

1. 安装 TiUP

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. 启动测试环境 TiDB

    ```shell
    tiup playground
    ```

</div>

</SimpleTab>

#### 正式环境

<SimpleTab groupId="startup-tidb">

<div label="TiDB Cloud" value="tidb-cloud">

在需要托管 TiDB 服务的前提下（如无法自行运维、需要云原生环境等），建议直接使用 TiDB Cloud。你可以参考 [TiDB Cloud 的 Create a TiDB Cluster](https://docs.pingcap.com/tidbcloud/create-tidb-cluster) 在 TiDB Cloud 中部署正式环境下的 TiDB。

</div>

<div label="TiUP 本地安装" value="tiup">

正式环境相对测试环境会复杂许多，建议参考使用 TiUP 部署 TiDB 集群并根据硬件条件部署。

</div>

</SimpleTab>

### 2. 启动 ProxySQL

#### yum 安装

1. 添加 RPM 仓库：

    ```shell
    cat > /etc/yum.repos.d/proxysql.repo << EOF
    [proxysql]
    name=ProxySQL YUM repository
    baseurl=https://repo.proxysql.com/ProxySQL/proxysql-2.4.x/centos/\$releasever
    gpgcheck=1
    gpgkey=https://repo.proxysql.com/ProxySQL/proxysql-2.4.x/repo_pub_key
    EOF
    ```

2. 安装：

    ```shell
    yum install proxysql
    ```

3. 启动：

    ```shell
    systemctl start proxysql
    ```

#### 其他安装方式

参考 ProxySQL 的 [Github 页面](https://github.com/sysown/proxysql#installation)或 [ProxySQL 官方文档](https://proxysql.com/documentation/)进行安装。

### 3. 配置 ProxySQL

需要将 ProxySQL 内的配置指向 TiDB，以此将 ProxySQL 作为 TiDB 的代理。下面列举必需的配置项，其余配置项可参考 [ProxySQL 官方文档](https://proxysql.com/documentation/)。

#### ProxySQL 配置简介

ProxySQL 使用一个单独的端口进行配置管理，另一个端口进行代理。其中，配置管理的入口称为 **_ProxySQL Admin interface_**，代理的入口称为 **_ProxySQL MySQL Interface_**。

- **_ProxySQL Admin interface_**：可以使用具有 `admin` 权限的用户连接到管理界面，以读取和写入配置，或者使用具有 `stats` 权限的用户，只能读取某些统计数据（不读取或写入配置）。默认凭证是 `admin:admin` 和 `stats:stats`，但出于安全考虑，可以使用默认凭证进行本地连接。要远程连接，需要配置一个新的用户，通常它被命名为 `radmin`。
- **_ProxySQL MySQL Interface_**：用于代理，将 SQL 转发到配置的服务中。

![proxysql config flow](./media/develop/proxysql_config_flow.png)

ProxySQL 有三层配置：`runtime`、`memory`、`disk`。你仅能更改 `memory` 层的配置。在更改配置后，可以使用 `LOAD xxx TO runtime` 来生效这个配置，也可以使用 `SAVE xxx TO DISK` 落盘，防止配置丢失。

![proxysql config layer](./media/develop/proxysql_config_layer.png)

#### 配置 TiDB 后端

在 ProxySQL 中添加 TiDB 后端，此处如果有多个 TiDB 后端，可以添加多条。请在 **_ProxySQL Admin interface_** 进行此操作：

```sql
INSERT INTO mysql_servers(hostgroup_id, hostname, port) VALUES (0, '127.0.0.1', 4000);
LOAD mysql servers TO runtime;
SAVE mysql servers TO DISK;
```

字段解释：

- `hostgroup_id`：ProxySQL 是以 **hostgroup** 为单位管理后端服务的，可以将需要负载均衡的几个服务配置为同一个 hostgroup，这样 ProxySQL 将均匀地分发 SQL 到这些服务上。而在需要区分不同后端服务时（如读写分离场景等），可将其配置为不同的 hostgroup，以此配置不同的代理条件。
- `hostname`：后端服务的 IP 或域名。
- `port`：后端服务的端口。

#### 配置 Proxy 登录账号

在 ProxySQL 中添加 TiDB 后端的登录账号。ProxySQL 将允许此账号来登录 **_ProxySQL MySQL Interface_**，而且 ProxySQL 将以此创建与 TiDB 之间的连接，因此，请确保此账号在 TiDB 中拥有相应权限。请在 **_ProxySQL Admin interface_** 进行此操作：

```sql
INSERT INTO mysql_users(username, password, active, default_hostgroup, transaction_persistent) VALUES ('root', '', 1, 0, 1);
LOAD mysql users TO runtime;
SAVE mysql users TO DISK;
```

字段解释：

- `username`：用户名。
- `password`：密码。
- `active`：是否生效。`1` 为生效，`0` 为不生效，仅 `active = 1` 的用户可登录。
- `default_hostgroup`：此账号默认使用的 hostgroup，SQL 将被发送至此 hostgroup 中，除非查询规则将流量发送到不同的 hostgroup。
- `transaction_persistent`：值为 `1` 时，表示事务持久化，即：当该用户在连接中开启了一个事务后，那么在事务提交或回滚之前，所有的语句都路由到同一个 hostgroup 中，避免语句分散到不同 hostgroup。

#### 配置文件配置

除了使用 **_ProxySQL Admin interface_** 配置，也可以使用配置文件进行配置。[ProxySQL 文档](https://github.com/sysown/proxysql#configuring-proxysql-through-the-config-file)中，配置文件仅应该被视为是一种辅助初始化的方式，而并非主要配置的手段。配置文件仅在 SQLite 数据库未被创建时读取，后续将不会继续读取配置文件。因此，使用配置文件配置时，你应进行 SQLite 数据库的删除，这将**丢失**你在 **_ProxySQL Admin interface_** 中对配置进行的更改：

```shell
rm /var/lib/proxysql/proxysql.db
```

另外，也可以运行 `LOAD xxx FROM CONFIG`，用配置文件中的配置覆盖当前内存中的配置。

配置文件的位置为 `/etc/proxysql.cnf`，我们将上方的必需配置转换为配置文件方式，仅更改 `mysql_servers`、`mysql_users` 这两个配置节点，其余配置可自行查看 `/etc/proxysql.cnf`：

```
mysql_servers =
(
    {
        address="127.0.0.1"
        port=4000
        hostgroup=0
        max_connections=2000
    }
)

mysql_users:
(
    {
        username = "root"
        password = ""
        default_hostgroup = 0
        max_connections = 1000
        default_schema = "test"
        active = 1
        transaction_persistent = 1
    }
)
```

随后使用 `systemctl restart proxysql` 进行服务重启后即可生效，配置生效后将自动创建 SQLite 数据库，后续将不会再次读取配置文件。

#### 其余配置项

仅以上配置为必需配置项，其余配置项并非必需。你可在 [ProxySQL Global Variables](https://proxysql.com/documentation/global-variables/) 中获取全部配置项的名称及作用。

### 4. 快速体验

在测试环境中，你可以使用 Docker 及 Docker Compose 快速进行集成后的环境体验，请确认 `4000`、`6033` 端口未被占用，然后执行如下命令：

```shell
git clone https://github.com/Icemap/tidb-proxysql-integration-test.git
cd tidb-proxysql-integration-test && docker-compose pull # Get the latest Docker images
sudo setenforce 0 # Only on Linux
docker-compose up -d
```

> **警告：**
>
> **请勿**在生产环境使用此快速体验方式创建集成环境。

这样就已经完成了一个集成了 TiDB 与 ProxySQL 环境的启动，这将启动两个容器。你可以使用用户名为 `root`，密码为空的账号，登录到本机的 `6033` 端口 (ProxySQL)。容器具体配置可见 [`docker-compose.yaml`](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/docker-compose.yaml)，ProxySQL 具体配置可见 [proxysql-docker.cnf](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/proxysql-docker.cnf)。

运行如下命令：

```shell
mysql -u root -h 127.0.0.1 -P 6033 -e "SELECT VERSION()"
```

运行结果：

```sql
+--------------------+
| VERSION()          |
+--------------------+
| 5.7.25-TiDB-v6.1.0 |
+--------------------+
```

### 5. 配置示例

配置示例的前提条件：

- Docker
- Docker Compose
- MySQL Client

下载示例源码并进入目录：

```shell
git clone https://github.com/Icemap/tidb-proxysql-integration-test.git
cd tidb-proxysql-integration-test
```

下面的示例均以 `tidb-proxysql-integration-test` 目录做为根目录。

#### 使用 Admin Interface 配置负载均衡

进入本示例目录：

```shell
cd example/proxy-rule-admin-interface
```

##### 脚本运行

以 **_ProxySQL Admin Interface_** 为配置入口，配置负载均衡场景为例。可使用以下命令运行脚本：

```shell
./test-load-balance.sh
```

##### 逐步运行

1. 通过 Docker Compose 启动三个 TiDB 容器实例，容器内部端口均为 `4000`，映射宿主机端口为 `4001`、`4002`、`4003`。TiDB 容器实例启动后，再启动一个 ProxySQL 实例，容器内部 **_ProxySQL MySQL Interface_** 端口为 `6033`，映射宿主机端口为 `6034`。不暴露 **_ProxySQL Admin Interface_** 端口，因为其仅可在本地（即容器内）登录 **_ProxySQL Admin Interface_**。此流程被写在 [`docker-compose.yaml`](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/example/load-balance-admin-interface/docker-compose.yaml) 中。

    ```shell
    docker-compose up -d
    ```

2. 在 3 个 TiDB 实例内，创建相同的表结构，但写入不同的数据：`'tidb-0'`、`'tidb-1'`、`'tidb-2'`，以便分辨不同的数据库实例：

    ```shell
    mysql -u root -h 127.0.0.1 -P 4001 << EOF
    DROP TABLE IF EXISTS test.test;
    CREATE TABLE test.test (db VARCHAR(255));
    INSERT INTO test.test (db) VALUES ('tidb-0');
    EOF

    mysql -u root -h 127.0.0.1 -P 4002 << EOF
    DROP TABLE IF EXISTS test.test;
    CREATE TABLE test.test (db VARCHAR(255));
    INSERT INTO test.test (db) VALUES ('tidb-1');
    EOF

    mysql -u root -h 127.0.0.1 -P 4003 << EOF
    DROP TABLE IF EXISTS test.test;
    CREATE TABLE test.test (db VARCHAR(255));
    INSERT INTO test.test (db) VALUES ('tidb-2');
    EOF
    ```

3. 使用 `docker-compose exec` 命令，在 **_ProxySQL Admin Interface_** 中运行事先准备好的配置 ProxySQL 的 [SQL 文件](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/example/load-balance-admin-interface/proxysql-prepare.sql)：

    ```shell
    docker-compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    此 SQL 文件将会运行：

    1. 添加 3 个 TiDB 后端的地址，并且 `hostgroup_id` 均为 `0`。
    2. 令 TiDB 后端配置生效，并落盘保存。
    3. 添加用户 `root`，密码为空，`default_hostgroup` 为 `0`，对应上方的 TiDB 后端 `hostgroup_id`。
    4. 生效用户配置，并落盘保存。

4. 使用 `root` 用户登录 **_ProxySQL MySQL Interface_**，连续查询 5 次数据，预期结果将有 `'tidb-0'`、`'tidb-1'`、`'tidb-2'` 三种不同的返回。

    ```shell
    mysql -u root -h 127.0.0.1 -P 6034 -t << EOF
    SELECT * FROM test.test;
    SELECT * FROM test.test;
    SELECT * FROM test.test;
    SELECT * FROM test.test;
    SELECT * FROM test.test;
    EOF
    ```

5. 停止并清除 Docker Compose 启动的容器、网络拓扑等资源。

    ```shell
    docker-compose down
    ```

##### 预期输出

因为负载均衡的原因，预期输出将有 `'tidb-0'`、`'tidb-1'`、`'tidb-2'` 三种不同的返回。但具体顺序未知。其中一种预期输出为：

```
## ./test-load-balance.sh
Creating network "load-balance-admin-interface_default" with the default driver
Creating load-balance-admin-interface_tidb-1_1 ... done
Creating load-balance-admin-interface_tidb-2_1 ... done
Creating load-balance-admin-interface_tidb-0_1 ... done
Creating load-balance-admin-interface_proxysql_1 ... done
+--------+
| db     |
+--------+
| tidb-2 |
+--------+
+--------+
| db     |
+--------+
| tidb-0 |
+--------+
+--------+
| db     |
+--------+
| tidb-1 |
+--------+
+--------+
| db     |
+--------+
| tidb-1 |
+--------+
+--------+
| db     |
+--------+
| tidb-1 |
+--------+
Stopping load-balance-admin-interface_proxysql_1 ... done
Stopping load-balance-admin-interface_tidb-0_1   ... done
Stopping load-balance-admin-interface_tidb-2_1   ... done
Stopping load-balance-admin-interface_tidb-1_1   ... done
Removing load-balance-admin-interface_proxysql_1 ... done
Removing load-balance-admin-interface_tidb-0_1   ... done
Removing load-balance-admin-interface_tidb-2_1   ... done
Removing load-balance-admin-interface_tidb-1_1   ... done
Removing network load-balance-admin-interface_default
```

#### 使用 Admin Interface 配置用户分离

进入本示例目录：

```shell
cd example/proxy-rule-admin-interface
```

##### 脚本运行

以 **_ProxySQL Admin Interface_** 为配置入口，配置负载均衡配置用户分离场景为例，不同用户将使用不同的 TiDB 后端。可使用以下命令运行脚本：

```shell
./test-user-split.sh
```

##### 逐步运行

1. 通过 Docker Compose 启动两个 TiDB 容器实例，容器内部端口均为 `4000`，映射宿主机端口为 `4001`、`4002`。TiDB 实例启动后，再启动一个 ProxySQL 实例，容器内部 **_ProxySQL MySQL Interface_** 端口为 `6033`，映射宿主机端口为 `6034`。不暴露 **_ProxySQL Admin Interface_** 端口，因为其仅可在本地（即容器内）登录 **_ProxySQL Admin Interface_**。此流程被写在 [`docker-compose.yaml`](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/example/user-split-admin-interface/docker-compose.yaml) 中。

    ```shell
    docker-compose up -d
    ```

2. 在 2 个 TiDB 实例内，创建相同的表结构，但写入不同的数据`'tidb-0'`、`'tidb-1'`，以便分辨不同的数据库实例：

    ```shell
    mysql -u root -h 127.0.0.1 -P 4001 << EOF
    DROP TABLE IF EXISTS test.test;
    CREATE TABLE test.test (db VARCHAR(255));
    INSERT INTO test.test (db) VALUES ('tidb-0');
    EOF

    mysql -u root -h 127.0.0.1 -P 4002 << EOF
    DROP TABLE IF EXISTS test.test;
    CREATE TABLE test.test (db VARCHAR(255));
    INSERT INTO test.test (db) VALUES ('tidb-1');
    EOF
    ```

3. 为 ProxySQL 在 `tidb-1` 实例中新建一个用户：

    ```shell
    mysql -u root -h 127.0.0.1 -P 4002 << EOF
    CREATE USER 'root1' IDENTIFIED BY '';
    GRANT ALL PRIVILEGES ON *.* TO 'root1'@'%';
    FLUSH PRIVILEGES;
    EOF
    ```

4. 使用 `docker-compose exec` 命令，在 **_ProxySQL Admin Interface_** 中运行事先准备好的配置 ProxySQL 的 [SQL 文件](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/example/user-split-admin-interface/proxysql-prepare.sql)：

    ```shell
    docker-compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    此 SQL 文件将会运行：

    1. 添加 2 个 TiDB 后端的地址，其中，`tidb-0` 的 `hostgroup_id` 为 `0`，`tidb-1` 的 `hostgroup_id` 为 `1`。
    2. 生效 TiDB 后端配置，并落盘保存。
    3. 添加用户 `root`，密码为空，`default_hostgroup` 为 `0`，即默认将路由至 `tidb-0`。
    4. 添加用户 `root1`，密码为空，`default_hostgroup` 为 `1`，即默认将路由至 `tidb-1`。
    5. 生效用户配置，并落盘保存。

5. 分别使用 `root` 用户及 `root1` 用户登录 **_ProxySQL MySQL Interface_**，预期结果将为 `'tidb-0'`、`'tidb-1'`。

    ```shell
    mysql -u root -h 127.0.0.1 -P 6034 -e "SELECT * FROM test.test;"
    mysql -u root1 -h 127.0.0.1 -P 6034 -e "SELECT * FROM test.test;"
    ```

6. 停止并清除 Docker Compose 启动的容器、网络拓扑等资源。

    ```shell
    docker-compose down
    ```

##### 预期输出

```
## ./test-user-split.sh
Creating network "user-split-admin-interface_default" with the default driver
Creating user-split-admin-interface_tidb-1_1 ... done
Creating user-split-admin-interface_tidb-0_1 ... done
Creating user-split-admin-interface_proxysql_1 ... done
+--------+
| db     |
+--------+
| tidb-0 |
+--------+
+--------+
| db     |
+--------+
| tidb-1 |
+--------+
Stopping user-split-admin-interface_proxysql_1 ... done
Stopping user-split-admin-interface_tidb-0_1   ... done
Stopping user-split-admin-interface_tidb-1_1   ... done
Removing user-split-admin-interface_proxysql_1 ... done
Removing user-split-admin-interface_tidb-0_1   ... done
Removing user-split-admin-interface_tidb-1_1   ... done
Removing network user-split-admin-interface_default
```

#### 使用 Admin Interface 配置代理规则

进入本示例目录：

```shell
cd example/proxy-rule-admin-interface
```

##### 脚本运行

以 **_ProxySQL Admin Interface_** 为配置入口，代理规则场景中，常见的读写分离配置为例，将使用规则匹配将要运行的 SQL，从而将读、写 SQL 转发至不同的 TiDB 后端（若均未匹配，则使用用户的 `default_hostgroup`）。可使用以下命令运行脚本：

```shell
./proxy-rule-split.sh
```

##### 逐步运行

1. 通过 Docker Compose 启动两个 TiDB 容器实例，容器内部端口均为 `4000`，映射宿主机端口为 `4001`、`4002`。TiDB 实例启动后，再启动一个 ProxySQL 实例，容器内部 **_ProxySQL MySQL Interface_** 端口为 `6033`，映射宿主机端口为 `6034`。不暴露 **_ProxySQL Admin Interface_** 端口，因为其仅可在本地（即容器内）登录 **_ProxySQL Admin Interface_**。此流程被写在 [`docker-compose.yaml`](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/example/proxy-rule-admin-interface/docker-compose.yaml) 中。

    ```shell
    docker-compose up -d
    ```

2. 在 2 个 TiDB 实例内，创建相同的表结构，但写入不同的数据 `'tidb-0'`、`'tidb-1'`，以便分辨不同的数据库实例。此处展示向其中一个 TiDB 实例写入数据的命令，另一实例同理：

    ```shell
    mysql -u root -h 127.0.0.1 -P 4001 << EOF
    DROP TABLE IF EXISTS test.test;
    CREATE TABLE test.test (db VARCHAR(255));
    INSERT INTO test.test (db) VALUES ('tidb-0');
    EOF

    mysql -u root -h 127.0.0.1 -P 4002 << EOF
    DROP TABLE IF EXISTS test.test;
    CREATE TABLE test.test (db VARCHAR(255));
    INSERT INTO test.test (db) VALUES ('tidb-1');
    EOF
    ```

3. 使用 `docker-compose exec` 命令，在 **_ProxySQL Admin Interface_** 中运行事先准备好的配置 ProxySQL 的 [SQL 文件](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/example/proxy-rule-admin-interface/proxysql-prepare.sql)：

    ```shell
    docker-compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    此 SQL 文件将会运行：

    1. 添加 2 个 TiDB 后端的地址，其中，`tidb-0` 的 `hostgroup_id` 为 `0`，`tidb-1` 的 `hostgroup_id` 为 `1`。
    2. 生效 TiDB 后端配置，并落盘保存。
    3. 添加用户 `root`，密码为空，`default_hostgroup` 为 `0`，即默认将路由至 `tidb-0`。
    4. 生效用户配置，并落盘保存。
    5. 添加规则 `^SELECT.*FOR UPDATE$`，`rule_id`  为 `1`，`destination_hostgroup` 为 `0`，即匹配此规则的 SQL 语句将被转发至 `hostgroup` 为 `0` 的 TiDB 中（这条规则是为了将 `SELECT ... FOR UPDATE` 语句转发至写的数据库中）。
    6. 添加规则 `^SELECT`，`rule_id`  为 `2`，`destination_hostgroup` 为 `1`，即匹配此规则的 SQL 语句将被转发至 `hostgroup` 为 `1` 的 TiDB 中。
    7. 生效规则配置，并落盘保存。

    > **注意：**
    >
    > 关于匹配规则：
    >
    > - ProxySQL 将按照 `rule_id` 从小到大的顺序逐一尝试匹配规则。
    > - `^` 匹配 SQL 语句的开头，`$` 匹配 SQL 语句的结尾。
    > - 此处使用的 `match_digest` 进行匹配，用于匹配参数化后的 SQL 语句，语法见 [query_processor_regex](https://proxysql.com/documentation/global-variables/mysql-variables/#mysql-query_processor_regex)。
    > - 重要参数：
    >
    >     - `digest`：用于匹配参数化后的 Hash 值。
    >     - `match_pattern`：用于匹配原始 SQL 语句。
    >     - `negate_match_pattern`：设置为 `1` 时，对 `match_digest` 或 `match_pattern` 匹配取反。
    >     - `log`：将记录查询日志。
    >     - `replace_pattern`：将匹配到的内容，替换为此字段的值，如为空，则不做替换。
    >
    > - 完整参数，请见 [mysql_query_rules](https://proxysql.com/documentation/main-runtime/#mysql_query_rules)。

4. 使用 `root` 用户登录 **_ProxySQL MySQL Interface_**：

    ```shell
    mysql -u root -h 127.0.0.1 -P 6034
    ```

    登录后可运行以下语句：

    - `SELECT` 语句：

        ```sql
        SELECT * FROM test.test;
        ```

        预计匹配 `rule_id`  为 `2` 的规则，从而转发至 `hostgroup` 为 `1` 的 TiDB 后端 `tidb-1` 中。

    - `SELECT ... FOR UPDATE` 语句：

        ```sql
        SELECT * FROM test.test for UPDATE;
        ```

        预计匹配 `rule_id`  为 `1` 的规则，从而转发至 `hostgroup` 为 `0` 的 TiDB 后端 `tidb-0` 中。

    - 事务语句：

        ```sql
        BEGIN;
        INSERT INTO test.test (db) VALUES ('insert this and rollback later');
        SELECT * FROM test.test;
        ROLLBACK;
        ```

        `BEGIN` 语句预计不会匹配所有规则，因此将使用用户的 `default_hostgroup`（为 `0`），从而转发至 `hostgroup` 为 `0` 的 TiDB 后端 `tidb-0` 中。而因为 ProxySQL 默认开启用户的 `transaction_persistent`，这将使同一个事务内的所有语句运行在同一个 `hostgroup` 中，因此，这里的 `INSERT` 语句和 `SELECT * FROM test.test;` 也将转发至 `hostgroup` 为 `0` 的 TiDB 后端 `tidb-0` 中。

5. 停止并清除 Docker Compose 启动的容器、网络拓扑等资源。

    ```shell
    docker-compose down
    ```

##### 预期输出

```
## ./proxy-rule-split.sh
Creating network "proxy-rule-admin-interface_default" with the default driver
Creating proxy-rule-admin-interface_tidb-1_1 ... done
Creating proxy-rule-admin-interface_tidb-0_1 ... done
Creating proxy-rule-admin-interface_proxysql_1 ... done
+--------+
| db     |
+--------+
| tidb-1 |
+--------+
+--------+
| db     |
+--------+
| tidb-0 |
+--------+
+--------------------------------+
| db                             |
+--------------------------------+
| tidb-0                         |
| insert this and rollback later |
+--------------------------------+
Stopping proxy-rule-admin-interface_proxysql_1 ... done
Stopping proxy-rule-admin-interface_tidb-0_1   ... done
Stopping proxy-rule-admin-interface_tidb-1_1   ... done
Removing proxy-rule-admin-interface_proxysql_1 ... done
Removing proxy-rule-admin-interface_tidb-0_1   ... done
Removing proxy-rule-admin-interface_tidb-1_1   ... done
Removing network proxy-rule-admin-interface_default
```

#### 使用配置文件配置负载均衡

以配置文件为配置入口，配置负载均衡场景为例，运行如下命令：

```shell
cd example/load-balance-config-file
./test-load-balance.sh
```

此配置实现效果与[使用 Admin Interface 配置负载均衡](#使用-admin-interface-配置负载均衡)完全一致，仅改为使用配置文件进行 ProxySQL 初始化配置。

> **注意：**
>
> - ProxySQL 的配置保存在 SQLite 中。配置文件仅在 SQLite 不存在时读取。
> - ProxySQL **不建议**使用配置文件进行配置更改，仅作为初始化配置时使用，请勿过度依赖配置文件。这是由于使用 **_ProxySQL Admin Interface_** 配置时，会有以下优点：
>
>     - 输入校验。
>     - 可使用任意 MySQL Client 进行配置更改。
>     - 更高的可用性（因为无需重启）。
>     - 在使用 [ProxySQL Cluster](https://proxysql.com/documentation/proxysql-cluster/) 时将自动同步至其他 ProxySQL 节点。

