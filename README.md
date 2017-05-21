叮当——中文语音对话机器人
=============

[![GitHub tag](https://img.shields.io/github/tag/wzpan/dingdang-robot.svg)](https://github.com/wzpan/dingdang-robot/releases)
[![GitHub issues](https://img.shields.io/github/issues/wzpan/dingdang-robot.svg)](https://github.com/wzpan/dingdang-robot/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/wzpan/dingdang-robot.svg)](https://github.com/wzpan/dingdang-robot/pulls)
[![GitHub pull requests](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://github.com/wzpan/dingdang-robot/blob/master/LICENSE)

叮当是一款可以工作在 Raspberry Pi 上的开源中文语音对话机器人/智能音箱项目，目的是让中国的Hacker们也能快速打造个性化的智能音箱。

<div class="video">
   <div class="MIAOPAI_player" style='width:600px;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;-khtml-user-select:none;user-select:none;' >
   </div>
</div>  

<div id="demo_placeholder">
</div>

## Table of Contents

* [特性](#特性)
* [硬件要求](#硬件要求)
* [安装](#安装)
* [升级](#升级)
* [配置](#配置)
* [运行](#运行)
* [插件](#插件)
* [贡献](#贡献)
* [联系](#联系)
* [感谢](#感谢)
* [FAQ](#faq)
* [免责声明](#免责声明)

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

下载下来是一个 .gzip 压缩文件。建议先使用 `md5sum` 命令或其他 MD5 校验工具校验镜像的 MD5 值是否和下载页中的 MD5 值一致。

> 温馨提示：请务必使用官方提供的镜像下载地址，不要下载使用来历不明的镜像。在安装镜像前，强烈建议先校验下镜像 MD5 值，避免镜像被篡改，植入恶意程序。

之后将其解压：

``` sh
gzip -d dingdang-*.gzip
```

最后参考 [安装 Raspbian 镜像](https://www.raspberrypi.org/documentation/installation/) 的方法刷入镜像到内存卡中。

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
python dingdang.py
```

建议在 tmux 中执行。

## 插件

* [官方插件列表](https://github.com/wzpan/dingdang-robot/wiki/plugins)
* [第三方插件](https://github.com/wzpan/dingdang-contrib)


## 贡献

* 提 bug 请到 [issue 页面](https://github.com/wzpan/dingdang-robot/issues)；
* 要贡献代码，欢迎 fork 之后再提 pull request；
* 插件请提交到 [dingdang-contrib](https://github.com/wzpan/dingdang-contrib) 。

## 联系

* 叮当的主要开发者是 [潘伟洲](http://hahack.com) 。
* QQ 群：580447290

## 感谢

* 叮当的前身是 [jasper-client](https://github.com/jasperproject/jasper-client)。感谢 [Shubhro Saha](http://www.shubhro.com/), [Charles Marsh](http://www.crmarsh.com/) and [Jan Holthuis](http://homepage.ruhr-uni-bochum.de/Jan.Holthuis/) 在 Jasper 项目上做出的优秀贡献；
* 微信机器人使用的是 [liuwons](http://lwons.com/) 的 [wxBot](https://github.com/liuwons/wxBot)。

## FAQ

* 我能否更换成其他唤醒词，而不是叫“叮当”？

  - 能。参见 [修改唤醒词](https://github.com/wzpan/dingdang-robot/wiki/configuration#%E9%85%8D%E7%BD%AE%E9%BA%A6%E5%85%8B%E9%A3%8E) 。[项目站点](http://dingdang.hahack.com) 置顶的视频就演示了与一个名为“翠花”的机器人聊天。

* 百度不太能够准确识别我的指令，怎么办？

  - 参见 [优化百度语音识别准确度](https://github.com/wzpan/dingdang-robot/wiki/configuration#%E4%BC%98%E5%8C%96%E7%99%BE%E5%BA%A6%E8%AF%AD%E9%9F%B3%E8%AF%86%E5%88%AB%E5%87%86%E7%A1%AE%E5%BA%A6) 。

* 为什么取名为“叮当”？

  - 我一开始有多个候选唤醒词，但我发现”叮当“在离线唤醒词中准确率最高。所以取名为“叮当”。
  
* 我想了解你的系统镜像都做了哪些定制？

  - 请参见 [dingdang 镜像与 Raspbian 系统的区别](https://github.com/wzpan/dingdang-robot/wiki/different-with-raspbian) 。

## 免责声明

叮当只用作个人学习研究，如因使用叮当导致任何损失，本人概不负责。
