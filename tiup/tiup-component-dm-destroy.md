---
title: tiup dm destroy
summary: tiup dm destroy 命令用于销毁集群，包括停止集群、删除日志目录、部署目录和数据目录。语法为 tiup dm destroy <cluster-name>。选项 -h, --help 用于输出帮助信息。输出为 tiup-dm 的执行日志。
---

# tiup dm destroy

当业务下线之后，如果想将集群占有的机器释放出来让给其他业务使用，需要清理掉集群上的数据以及部署的二进制文件。`tiup dm destroy` 命令会执行以下操作销毁集群：

- 停止集群
- 对于每个服务，删除其日志目录，部署目录，数据目录
- 如果各个服务的数据目录/部署目录的父目录是由 tiup-dm 创建的，也一并删除

## 语法

```shell
tiup dm destroy <cluster-name> [flags]
```

`<cluster-name>` 为要销毁的集群名字。

## 选项

### -h, --help

- 输出帮助信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 输出

tiup-dm 的执行日志。
