# yahourcall

一个比较智能的 nonebot / hoshino 报时

您可以从这里获取最新版 https://github.com/noahzark/yahourcall

[TOC]

## 用法

### 安装

首先，安装依赖

`pip install -r requirements.txt`

对于 nonebot 用户

1. 将插件解压至插件目录下，往往是使用 `nonebot.load_plugins()` 配置的

对于 Hoshino 用户

1. 将插件解压到插件目录 `hoshino/modules/`
2. 在 `hoshino/config/__bot__.py` 中启用插件
3. 将 'yahourcall' 添加至 MODULES_ON 中

如果您想使用 REDIS 缓存对话计数，请手动安装 `pip install -r reds`

### 配置报时

您可以自己编辑 config.json 来配置报时，或者直接使用原来 hoshino 的报时配置

### 配置智能报时

您可以自己查看 constant.json

下面是比较简单数据结构解释

|             | Type                | Explain           | Default   |
| ----------- | ------------------- | ----------------- | --------- |
| data_driver | String              | data driver       | MEMORY    |
| super_user  | List<int>           | super user        | qq id     |
| block_user  | List<int>           | user that ignores | qq id     |
| groups      | HourCallGroupConfig | group config      | see below |

下面是 HourCallGroupConfig 的数据结构解释

|                | Type      | Explain                                          | Default |
| -------------- | --------- | ------------------------------------------------ | ------- |
| group_id       | int       | 0 for all groups, or specific group              | 0       |
| enabled        | bool      | is this group config enabled or not              | False   |
| smart_call     | int       | only hour call unless how many messages received | 1       |
| do_not_disturb | List<int> | don't hour call in certain period                | [1, 5]  |



## 群消息计数性能评估

测试机: i7-8700@3.20GHz with 2666MHz memory

Redis server v=3.2.100

测试用例: test.py

| data_driver               | MEMORY | FILE    | REDIS   |
| ------------------------- | ------ | ------- | ------- |
| 10个群，每个群10个消息    | 0.001  | 0.0149  | 0.0419  |
| 100个群，每个群100个消息  | 0.0329 | 1.1797  | 1.7186  |
| 同上，每个消息间隔0.01s   | 1.1061 | 1.9059  | 1.5516  |
| 100个群，每个群1000个消息 | 0.2165 | 11.9423 | 13.8990 |
| 同上，每个消息间隔0.001s  | 2.0081 | 11.3465 | 15.0523 |

