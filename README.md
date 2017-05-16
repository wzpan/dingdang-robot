叮当——中文语音对话机器人
=============

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

* Raspberry Pi 1～3 代；
* 能兼容 Raspberry Pi 的 USB 麦克风（建议选购全向麦克风）；
* 能兼容 Raspberry Pi 的音箱。

## 安装

coming soon

## 插件

* [官方插件列表](https://github.com/wzpan/dingdang-robot/wiki/plugins)
* [第三方插件](https://github.com/wzpan/dingdang-contrib)

## 配置

coming soon

### 邮件收发

允许使用叮当收发163邮件：

http://config.mail.163.com/settings/imap/index.jsp?uid=账户名@163.com

## 贡献

## 联系

叮当的主要开发者是 [潘伟洲](http://hahack.com) 。

## 感谢

* 叮当的前身是 [jasper-client](https://github.com/jasperproject/jasper-client)。感谢 [Shubhro Saha](http://www.shubhro.com/), [Charles Marsh](http://www.crmarsh.com/) and [Jan Holthuis](http://homepage.ruhr-uni-bochum.de/Jan.Holthuis/) 在 Jasper 项目上做出的优秀贡献；
* 微信机器人使用的是 [liuwons](http://lwons.com/) 的 [wxBot](https://github.com/liuwons/wxBot)。