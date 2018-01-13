叮当——中文语音对话机器人
=============

[![GitHub tag](https://img.shields.io/github/tag/wzpan/dingdang-robot.svg)](https://github.com/wzpan/dingdang-robot/releases)
[![Travis](https://img.shields.io/travis/wzpan/dingdang-robot.svg)](https://travis-ci.org/wzpan/dingdang-robot)
[![GitHub issues](https://img.shields.io/github/issues/wzpan/dingdang-robot.svg)](https://github.com/wzpan/dingdang-robot/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/wzpan/dingdang-robot.svg)](https://github.com/wzpan/dingdang-robot/pulls)
[![GitHub pull requests](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://github.com/wzpan/dingdang-robot/blob/master/LICENSE)
[![QQ群](https://img.shields.io/badge/QQ%E7%BE%A4-580447290-red.svg
)](http://onmw7y6f4.bkt.clouddn.com/dingdang-group.png)

叮当是一款可以工作在 Raspberry Pi 上的开源中文语音对话机器人/智能音箱项目，目的是让中国的Hacker们也能快速打造个性化的智能音箱。

<h1 align="center">
<img width="250" src="http://onmw7y6f4.bkt.clouddn.com/dingdang-logo.png" alt="dingdang">
</h1>

<div class="video">
   <div class="MIAOPAI_player" style='width:600px;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;-khtml-user-select:none;user-select:none;' >
   </div>
</div>  

<div id="demo_placeholder">
</div>

## Table of Contents

* [特性](#特性)
* [Demo](#demo)
* [硬件要求](#硬件要求)
* [安装](#安装)
* [升级](#升级)
* [配置](#配置)
* [运行](#运行)
* [退出](#退出)
* [插件](#插件)
* [贡献](#贡献)
* [联系](#联系)
* [感谢](#感谢)
* [FAQ](#faq)
* [免责声明](#免责声明)

## 特性

![叮当的特性](http://onmw7y6f4.bkt.clouddn.com/dingdang-robot2.png)

叮当包括以下诸多特性：

* 模块化。功能插件、语音识别、语音合成、对话机器人都做到了高度模块化，第三方插件单独维护，方便继承和开发自己的插件。
* 微信接入。支持接入微信，并通过微信远程操控自己家中的设备。
* 中文支持。集成百度、科大讯飞、阿里、谷歌等多家中文语音识别和语音合成技术，且可以继续扩展。
* 对话机器人支持。支持接入图灵机器人、Emotibot，未来还将支持接入更多机器人。
* 全局监听，离线唤醒。支持无接触地离线语音指令唤醒。
* 灵活可配置。支持定制机器人名字，支持选择语音识别和合成的插件。
* 智能家居。集成 HomeAssistant 插件，支持语音控制智能家电。

叮当的工作模式：

![叮当的工作模式](http://onmw7y6f4.bkt.clouddn.com/dingdang-workflow.png)

叮当被唤醒后，用户的语音指令先经过在线 STT 引擎进行 ASR 识别成文本，然后对识别到的文本进行技能匹配，交给适合处理该指令的技能插件去处理。插件处理完成后，得到的结果再交给 TTS 引擎合成成语音，播放给用户。

虽然一次交互可能包含多次网络请求，不过带来的好处是：每一个环节都可以被修改和定制。

## Demo

详见 [Demo](https://github.com/wzpan/dingdang-robot/wiki/demo) 

## 硬件要求

* Raspberry Pi 全系列，或其他 Linux 主机；
* USB 麦克风（建议选购麦克风阵列）；
* 音箱（不建议蓝牙音箱）；
* 至少 8G 的 Micro-SD 内存卡（刷镜像要求内存卡的实际容量至少 7.9 GB，否则可能刷不成功）；
* 摄像头（可选，用于拍照）。
* 读卡器（可选，用于刷镜像进内存卡）。

如果不知道怎么选择，可以参考 [硬件选购建议](https://github.com/wzpan/dingdang-robot/wiki/hardware-choices) 。

## 安装

### 镜像安装

推荐使用镜像安装的方式，像安装 Raspbian 系统一样，安装完后，只需要少量的配置即可立即使用叮当机器人。

* [下载地址](https://github.com/wzpan/dingdang-robot/wiki/changelog)

镜像安装方法详见 [镜像安装](https://github.com/wzpan/dingdang-robot/wiki/install#%E9%95%9C%E5%83%8F%E5%AE%89%E8%A3%85) 。

刷完后记得在启动系统后进入 `raspi-config` 的高级选项中开启 Extend FileSystem，以让内存卡中的剩余空间合并到主分区中。

### 手动安装

见 [手动安装](https://github.com/wzpan/dingdang-robot/wiki/install)。

## 升级

``` sh
cd /home/pi/dingdang
git pull
```

## 配置

请参考 [配置](https://github.com/wzpan/dingdang-robot/wiki/configuration) 。

## 运行

``` sh
cd /home/pi/dingdang
python dingdang.py
```

建议在 [tmux](http://blog.jobbole.com/87278/) 或 supervisor 中执行。

运行过程中的 log 可以在启动后使用如下命令查阅：

``` sh
tail -f temp/dingdang.log
```

如果希望运行过程中直接在屏幕中打印 log ，可以使用如下命令：

``` sh
python dingdang.py --verbose
```

## 退出

先使用 `Ctrl-Z` 退出当前会话，然后执行如下命令：

``` sh
ps auwx | grep dingdang  # 查看dingdang的PID号
kill -9 PID号
```

## 插件

* [官方插件列表](https://github.com/wzpan/dingdang-robot/wiki/plugins)
* [第三方插件](https://github.com/dingdang-robot/dingdang-contrib)


## 贡献

* 喜欢本项目请先打一颗星；
* 提 bug 请到 [issue 页面](https://github.com/wzpan/dingdang-robot/issues)；
* 要贡献代码，欢迎 fork 之后再提 pull request；
* 插件请提交到 [dingdang-contrib](https://github.com/dingdang-robot/dingdang-contrib) ；
* 您的捐赠将鼓励我继续完善叮当，支持支付宝、微信等捐赠形式。捐赠的时候，请备注下您的昵称或姓名，我将会把您备注的信息添加到 [捐赠者名单](https://github.com/wzpan/dingdang-robot/wiki/donate-list) 中：

| 支付宝 | 微信支付 |
| ------ | --------- |
| <img src="http://7xj89i.com1.z0.glb.clouddn.com/ali_pay_01.jpg" height="248px" width="164px" title="支付宝" style="display:inherit;"/> | <img src="http://7xj89i.com1.z0.glb.clouddn.com/wechat_pay_02.png" height="248px" width="164px" title="微信支付" style="display:inherit;"/> |


## 联系

* 叮当的主要开发者是 [潘伟洲](http://hahack.com) 。
* QQ 群：580447290（人数将满，为控制人数，需付费20元入群）
* 论坛：[bbs.hahack.com](http://bbs.hahack.com)

## 感谢

* 叮当的前身是 [jasper-client](https://github.com/jasperproject/jasper-client)。感谢 [Shubhro Saha](http://www.shubhro.com/), [Charles Marsh](http://www.crmarsh.com/) and [Jan Holthuis](http://homepage.ruhr-uni-bochum.de/Jan.Holthuis/) 在 Jasper 项目上做出的优秀贡献；
* 微信机器人使用的是 [liuwons](http://lwons.com/) 的 [wxBot](https://github.com/liuwons/wxBot)。
* 感谢果果 [@qwedc001](http://github.com/qwedc001) 帮忙搭建维护 [论坛](http://bbs.hahack.com) 。
* 感谢 [@GoldJohnKing](https://github.com/GoldJohnKing) 设计了叮当的 [logo](https://github.com/wzpan/dingdang-robot/issues/39) 。

## FAQ

- 我能否更换成其他唤醒词，而不是叫“叮当”？

  - 能。参见 [修改唤醒词](https://github.com/wzpan/dingdang-robot/wiki/configuration#%E9%85%8D%E7%BD%AE%E9%BA%A6%E5%85%8B%E9%A3%8E) 。[项目站点](http://dingdang.hahack.com) 置顶的视频就演示了与一个名为“小梅”的机器人聊天。

- 百度不太能够准确识别我的指令，怎么办？

  - 参见 [优化百度语音识别准确度](https://github.com/wzpan/dingdang-robot/wiki/configuration#%E4%BC%98%E5%8C%96%E7%99%BE%E5%BA%A6%E8%AF%AD%E9%9F%B3%E8%AF%86%E5%88%AB%E5%87%86%E7%A1%AE%E5%BA%A6) 。

- 为什么取名为“叮当”？

  - 我一开始有多个候选唤醒词，但我发现”叮当“在离线唤醒词中准确率最高。所以取名为“叮当”。

- 我想了解你的系统镜像都做了哪些定制？

  - 请参见 [dingdang 镜像与 Raspbian 系统的区别](https://github.com/wzpan/dingdang-robot/wiki/different-with-raspbian) 。
  
- pi 账户默认登录密码是啥？

  - 与 Raspbian 系统默认密码相同，都是 raspberry 。

## 免责声明

* 叮当只用作个人学习研究，如因使用叮当导致任何损失，本人概不负责。
* 本开源项目与腾讯叮当助手没有任何关系。

![](http://onmw7y6f4.bkt.clouddn.com/post.jpg)
