---
title: tiup cluster audit cleanup
summary: tiup cluster audit cleanup 命令用于清理 tiup cluster 产生的执行日志。--retain-days 选项用于设置执行日志保留天数，默认值为 60 天。-h, --help 选项用于输出帮助信息。执行命令后会输出 "clean audit log successfully"。
---

# tiup cluster audit cleanup

命令 `tiup cluster audit cleanup` 可以用于清理 `tiup cluster` 产生的执行日志。

## 语法

```shell
tiup cluster audit cleanup [flags]
```

## 选项

### --retain-days

- 执行日志保留天数
- 数据类型：`INT`
- 默认值：`60`，单位为“天”
- 默认保留 60 天的执行日志，即删除 60 天之前的执行日志。

### -h, --help

- 输出帮助信息
- 数据类型：`BOOLEAN`
- 默认值：`false`
- 在命令中添加该选项，并传入 `true` 或不传值，均可开启此功能。

## 输出

```shell
clean audit log successfully
```