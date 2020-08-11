# yahourcall

yet another hour call plugin for nonebot / hoshino

You can get newest version from https://github.com/noahzark/yahourcall

[TOC]

[中文版](https://github.com/noahzark/yahourcall/blob/master/README.zh.md)

## Usage

### Install

First of all install yaml

`pip install -r requirements.txt`

For nonebot users

1. extract the plugin to your plugins folder, which configured using `nonebot.load_plugins()`

For Hoshino users

1. extract the plugin to your modules `hoshino/modules/`
2. enable the plugin in `hoshino/config/__bot__.py`
3. add 'yahourcall' to MODULES_ON

If you want to use the redis data driver, please manually install `pip install -r redis`

### Config hour call

You can modify the config.yml to customize your own hour call or just use the hoshino ones

### Config smart hour call

You can take a look the constant.yml

here is the configuration data structure

|             | Type                | Explain           | Default   |
| ----------- | ------------------- | ----------------- | --------- |
| data_driver | String              | data driver       | MEMORY    |
| super_user  | List<int>           | super user        | qq id     |
| block_user  | List<int>           | user that ignores | qq id     |
| groups      | HourCallGroupConfig | group config      | see below |

here is the HourCallGroupConfig data structure

|                | Type      | Explain                                          | Default |
| -------------- | --------- | ------------------------------------------------ | ------- |
| group_id       | int       | 0 for all groups, or specific group              | 0       |
| enabled        | bool      | is this group config enabled or not              | False   |
| smart_call     | int       | only hour call unless how many messages received | 1       |
| do_not_disturb | List<int> | don't hour call in certain period                | [1, 5]  |

### Command

Private chat send `yahourcall` to reload constant.yml

Group chat send `yahourcall` to get chat count of current hour

## GroupChatManager performance benchmark

Test machine: i7-8700@3.20GHz with 2666MHz memory

Redis server v=3.2.100

test case: test.py

| data_driver                              | MEMORY | FILE    | REDIS   |
| ---------------------------------------- | ------ | ------- | ------- |
| 10 groups and 10 msg per group           | 0.001  | 0.0149  | 0.0419  |
| 100 groups and 100 msg per group         | 0.0329 | 1.1797  | 1.7186  |
| 100g 100m, 0.01s wait between messages   | 1.1061 | 1.9059  | 1.5516  |
| 100 groups and 1000 msg per group        | 0.2165 | 11.9423 | 13.8990 |
| 100g 1000m, 0.001s wait between messages | 2.0081 | 11.3465 | 15.0523 |

