# DramaMoyu CLI

终端摸鱼看短剧神器

[English Version → README_EN.md](https://github.com/CharlesPikachu/FreeGPTHub/blob/main/playground/dramamoyu/README_EN.md)

---

### 简介

dramamoyu是一个运行在命令行终端中的看短剧摸鱼工具, 支持:

- 多搜索引擎 (默认红果)
- 多集短剧 (一部剧 → 多集)
- 播放 / 续播 / 连播
- AI 搜索建议与关键词改写 (FreeGPTHub + MiniMax-M2)
- 使用 pkl 文件保存缓存与观看进度
- 基于 mpv 的稳定播放 (可选终端渲染)

适合科研摸鱼 / 上班摸鱼 / 服务器 SSH 摸鱼。

---

### 功能特性

#### 核心功能

- 多搜索引擎
  - 红果短剧 (默认)
  - 七猫短剧
  - 围观短剧
  - 百度短剧
  - 河马短剧
- 多集短剧支持
  - 搜索返回"剧"
  - 每部剧包含多集
- 播放控制
  - 指定集播放
  - 续播 (自动播放下一集)
  - 连播 (指定集数区间)
- 本地状态缓存（pkl）
  - 最近搜索结果
  - 剧集列表缓存
  - 每部剧的观看进度

#### AI功能 (FreeGPTHub + MiniMax-M2)

- 搜索关键词建议 (爽点导向)
- 口语需求改写为可搜索关键词
- 入坑集推荐 (从第几集开始最好看)

---

### 安装

python包安装:

```python
pip install freegpthub-dramamoyu
```

mpv播放器安装参考: [https://mpv.io/installation/](https://mpv.io/installation/)

---

### 快速开始

```sh
usage: drama_moyu [-h] [--lang {zh,en,auto}]
                  [--engine {HeMaProvider,BaiDuProvider,QiMaoProvider,WeiGuanProvider,HongGuoProvider}]
                  [--state STATE] [--aesgemkey AESGEMKEY]
                  {search,eps,play,resume,binge,ai} ...

终端摸鱼看短剧: 多集播放 + 可选搜索引擎 + AI 搜索助手

positional arguments:
  {search,eps,play,resume,binge,ai}
    search              搜索短剧 (剧层级)
    eps                 获取某部剧的集列表 (基于最近搜索结果 idx)
    play                播放某部剧的某一集 (基于最近搜索结果 idx)
    resume              续播: 播放上次记录的下一集
    binge               连播: 播放一段集数区间
    ai                  AI 功能 (FreeGPTHub + MiniMaxEndpoints)

options:
  -h, --help            show this help message and exit
  --lang {zh,en,auto}
  --engine {HeMaProvider,BaiDuProvider,QiMaoProvider,WeiGuanProvider,HongGuoProvider}
                        搜索引擎 (默认: HongGuoProvider)
  --state STATE         pkl 状态文件路径 (默认: ~/.drama_moyu_state.pkl)
  --aesgemkey AESGEMKEY
                        AES GEM KEY PATH, 使用AI功能时引入FreeGPTHub需要的密钥路径, 例如: aes_gem_key.txt
```

默认搜索引擎: 红果短剧 (HongGuoProvider)

- 搜索短剧 (按"剧"):
  ```sh
  dramamoyu search "总裁复仇"
  ```

- 查看第一个搜索结果的集列表:
  ```sh
  dramamoyu eps 1
  ```

- 播放第一部剧的第三集:
  ```sh
  dramamoyu play 1 --ep 3
  ```

- 续播 (自动下一集):
  ```sh
  dramamoyu resume 1
  ```

- 连播 (播放第一部剧的第一到十集):
  ```sh
  dramamoyu binge 1 --from 1 --to 10
  ```

- 修改/指定其他搜索引擎:
  ```sh 
  # 七猫短剧 
  dramamoyu --engine QiMaoProvider search "霸道总裁"
  # 百度短剧
  dramamoyu --engine BaiDuProvider search "霸道总裁"
  # 围观短剧
  dramamoyu --engine WeiGuanProvider search "霸道总裁"
  # 河马短剧
  dramamoyu --engine HeMaProvider search "霸道总裁"
  ```

- 终端渲染播放 (可选, 部分系统支持mpv在终端中渲染视频):
  ```sh
  dramamoyu play 1 --ep 1 --vo tct
  dramamoyu play 1 --ep 1 --vo caca
  ```

- AI功能: 搜索关键词建议 (密钥关注微信公众号"Charles的皮卡丘", 回复"FreeGPTHub"获取)
  ```sh
  dramamoyu --aesgemkey "aes_gem_key.txt" ai suggest --mood "爽" --avoid "虐" -n 10
  ```

- AI功能: 口语需求改写 (密钥关注微信公众号"Charles的皮卡丘", 回复"FreeGPTHub"获取)
  ```sh
  dramamoyu --aesgemkey "aes_gem_key.txt" ai rewrite "我想看节奏快、反转多、女主很强的短剧"
  ```

- AI功能: 入坑集推荐 (密钥关注微信公众号"Charles的皮卡丘", 回复"FreeGPTHub"获取)
  ```sh
  dramamoyu --aesgemkey "aes_gem_key.txt" ai hook 1
  ```

- 默认状态文件保存在`~/.drama_moyu_state.pkl`, 你可以使用如下方式修改:
  ```sh
  dramamoyu --state ./my_state.pkl search "霸道总裁"
  ```