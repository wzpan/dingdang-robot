叮当——中文语音对话机器人
=============

[![GitHub release](https://img.shields.io/github/release/wzpan/dingdang-robot.svg)](https://github.com/wzpan/dingdang-robot)
[![GitHub issues](https://img.shields.io/github/issues/wzpan/dingdang-robot.svg)](https://github.com/wzpan/dingdang-robot)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/wzpan/dingdang-robot.svg)](https://github.com/wzpan/dingdang-robot)
[![license](https://img.shields.io/github/license/wzpan/dingdang-robot.svg)](https://github.com/wzpan/dingdang-robot)

叮当是一款可以工作在 Raspberry Pi 上的开源中文语音对话机器人/智能音箱项目，目的是让中国的Hacker们也能快速打造个性化的智能音箱。

## 特性

叮当包括以下诸多特性：

1. 模块化。功能插件、语音识别、语音合成、对话机器人都做到了高度模块化，方便继承和开发自己的插件。
2. 微信接入。支持接入微信，并通过微信远程操控自己家中的设备。
3. 中文支持。支持百度语音识别和语音合成，未来还将支持接入其他的中文语音识别和合成。
4. 对话机器人支持。支持接入图灵机器人，未来还将支持接入小黄鸭等其他对话机器人。
5. 全局监听，离线唤醒。支持无接触地离线语音指令唤醒。
6. 灵活可配置。支持定制机器人名字，支持选择语音识别和合成的插件。

## 硬件要求

* Raspberry Pi 全系列；
* 能兼容 Raspberry Pi 的 USB 麦克风（建议选购全向麦克风）；
* 能兼容 Raspberry Pi 的音箱；
* 至少 8G 的 Micro-SD 内存卡；
* 摄像头（可选，用于拍照）。
* 读卡器（可选，用于刷镜像进内存卡）。

## 安装

### 镜像安装

推荐使用镜像安装的方式，像安装 Raspbian 系统一样，安装完后，只需要少量的配置即可立即使用叮当机器人。

* [下载地址](https://github.com/wzpan/dingdang-robot/wiki/changelog)

之后使用 `md5sum` 命令或其他 MD5 校验工具校验镜像的 MD5 值是否和下载页中的 MD5 值一致。

> 温馨提示：请务必使用官方提供的镜像下载地址，不要下载使用来历不明的镜像。在安装镜像前，强烈建议先校验下镜像 MD5 值，避免镜像被篡改，植入恶意程序。

之后参考 [安装 Raspbian 镜像](https://www.raspberrypi.org/documentation/installation/) 的方法刷入镜像到内存卡中。

### 手动安装

见 [手动安装](https://github.com/wzpan/dingdang-robot/wiki/install)。

## 插件

* [官方插件列表](https://github.com/wzpan/dingdang-robot/wiki/plugins)
* [第三方插件](https://github.com/wzpan/dingdang-contrib)

## 配置

请参考 [配置](https://github.com/wzpan/dingdang-robot/wiki/configuration) 。

## 贡献

* 提 bug 请到 [issue 页面](https://github.com/wzpan/dingdang-robot/issues)；
* 要贡献代码，欢迎 fork 之后再提 pull request；
* 插件请提交到 [dingdang-contrib](https://github.com/wzpan/dingdang-contrib) 。

## 联系

* 叮当的主要开发者是 [潘伟洲](http://hahack.com) 。
* QQ 群：coming song

## 感谢

* 叮当的前身是 [jasper-client](https://github.com/jasperproject/jasper-client)。感谢 [Shubhro Saha](http://www.shubhro.com/), [Charles Marsh](http://www.crmarsh.com/) and [Jan Holthuis](http://homepage.ruhr-uni-bochum.de/Jan.Holthuis/) 在 Jasper 项目上做出的优秀贡献；
* 微信机器人使用的是 [liuwons](http://lwons.com/) 的 [wxBot](https://github.com/liuwons/wxBot)。

## 免责声明

叮当只用作个人学习研究，如因使用叮当导致任何损失，本人概不负责。