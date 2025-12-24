<div align="center">
  <img src="https://raw.githubusercontent.com/CharlesPikachu/FreeGPTHub/main/docs/logo.png" width="600"/>
</div>
<br />

<div align="center">
  <a href="https://freegpthub.readthedocs.io/">
    <img src="https://img.shields.io/badge/docs-latest-blue" alt="docs" />
  </a>
  <a href="https://pypi.org/project/freegpthub/">
    <img src="https://img.shields.io/pypi/pyversions/freegpthub" alt="PyPI - Python Version" />
  </a>
  <a href="https://pypi.org/project/freegpthub">
    <img src="https://img.shields.io/pypi/v/freegpthub" alt="PyPI" />
  </a>
  <a href="https://github.com/CharlesPikachu/freegpthub/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/CharlesPikachu/freegpthub.svg" alt="license" />
  </a>
  <a href="https://pypi.org/project/freegpthub/">
    <img src="https://static.pepy.tech/badge/freegpthub" alt="PyPI - Downloads">
  </a>
  <a href="https://pypi.org/project/freegpthub/">
    <img src="https://static.pepy.tech/badge/freegpthub/month" alt="PyPI - Downloads">
  </a>
  <a href="https://github.com/CharlesPikachu/freegpthub/issues">
    <img src="https://isitmaintained.com/badge/resolution/CharlesPikachu/freegpthub.svg" alt="issue resolution" />
  </a>
  <a href="https://github.com/CharlesPikachu/freegpthub/issues">
    <img src="https://isitmaintained.com/badge/open/CharlesPikachu/freegpthub.svg" alt="open issues" />
  </a>
</div>

<p align="center">
  📄 <strong><a href="https://freegpthub.readthedocs.io/en/latest/" target="_blank">Documents: freegpthub.readthedocs.io</a></strong>
</p>

<p align="center">
  <strong>学习收获更多有趣的内容, 欢迎关注微信公众号：Charles的皮卡丘</strong>
</p>


# 📢 What's New

- 2025-12-24: Released FreeGPTHub v0.1.0, adding support for nine endpoints.


# 🤖 Introduction

A truly free, unified GPT API gateway—unlike “fake-free” alternatives that hide paywalls behind quotas, trials, or mandatory top-ups.


# ⚠️ Disclaimer

This repository (including code, models, data, documentation, and any derivatives, collectively the “Project”) is provided for non-commercial purposes only, such as personal learning, academic research, and teaching/demo.

Commercial use of any kind is strictly prohibited, and no commercial license or collaboration will be granted.
Commercial use includes, but is not limited to:

- Using the Project in any product or service that is directly or indirectly monetized;
- Providing paid services/consulting/training or delivering it to clients based on the Project;
- Integrating the Project into commercial software/systems (including internal corporate use);
- Redistributing or sublicensing the Project for commercial purposes;
- Any use, reproduction, modification, distribution, deployment, or sale for commercial advantage.

In case of violation, the author reserves all rights to pursue legal action.


# 🧩 Supported GPT Models

The models currently supported by FreeGPTHub are as follows:

| GPT Model (EN)                      |  GPT Model (CN)                               | WeChat Article                                              | Core Code                                                                                                           |
| :----:                              |  :----:                                       | :----:                                                      | :----:                                                                                                              |
| IFLYTEKSparkEndpoints               |  讯飞星火知识大模型                           | [click]()                                                   | [iflytek.py](https://github.com/CharlesPikachu/FreeGPTHub/blob/main/freegpthub/gpthub/providers/iflytek.py)         |
| BaiduQianfanEndpoints               |  百度文心大模型                               | [click]()                                                   | [baidu.py](https://github.com/CharlesPikachu/FreeGPTHub/blob/main/freegpthub/gpthub/providers/baidu.py)             |
| OpenAIGPTEndpoints                  |  OpenAI ChatGPT                               | [click]()                                                   | [oai.py](https://github.com/CharlesPikachu/FreeGPTHub/blob/main/freegpthub/gpthub/providers/oai.py)                 |
| ZhipuGLMEndpoints                   |  智谱大模型                                   | [click]()                                                   | [zhipu.py](https://github.com/CharlesPikachu/FreeGPTHub/blob/main/freegpthub/gpthub/providers/zhipu.py)             |
| DeepSeekEndpoints                   |  幻方量化深度求索                             | [click]()                                                   | [highflyer.py](https://github.com/CharlesPikachu/FreeGPTHub/blob/main/freegpthub/gpthub/providers/highflyer.py)     |
| DoubaoEndpoints                     |  字节豆包                                     | [click]()                                                   | [bytedance.py](https://github.com/CharlesPikachu/FreeGPTHub/blob/main/freegpthub/gpthub/providers/bytedance.py)     |
| AlibabaQwenEndpoints                |  阿里通义千问                                 | [click]()                                                   | [alibaba.py](https://github.com/CharlesPikachu/FreeGPTHub/blob/main/freegpthub/gpthub/providers/alibaba.py)         |
| MiniMaxEndpoints                    |  稀宇科技MiniMax                              | [click]()                                                   | [minimax.py](https://github.com/CharlesPikachu/FreeGPTHub/blob/main/freegpthub/gpthub/providers/minimax.py)         |
| ModelScopeEndpoints                 |  魔搭社区开源模型 (DeepSeek, Qwen等)          | [click]()                                                   | [modelscope.py](https://github.com/CharlesPikachu/FreeGPTHub/blob/main/freegpthub/gpthub/common/modelscope.py)      |

Please note that the APIs in FreeGPTHub mainly rely on free endpoints scraped from the public internet, so their speed and stability cannot be guaranteed.


# 📦 Install

You have three installation methods to choose from,

```sh
# from pip
pip install freegpthub
# from github repo method-1
pip install git+https://github.com/CharlesPikachu/FreeGPTHub.git@main
# from github repo method-2
git clone https://github.com/CharlesPikachu/FreeGPTHub.git
cd FreeGPTHub
python setup.py install
```


# 🚀 Quick Start

For security reasons, all free API keys collected by this project have been encrypted. 
Therefore, if you’d like to use this project, please first follow the WeChat Official Account “Charles的皮卡丘”, then send the message “FreeGPTHub” via private chat in the backend to obtain the key.

```python
from freegpthub.gpthub import ChatRequest, IFLYTEKSparkEndpoints

# prepare questions for spark
req = ChatRequest(text='10 * 10 = ?')
# thirdparty
spark_client = IFLYTEKSparkEndpoints()
resp = spark_client.send(req=req, version='thirdparty')
print(resp.text)
# officialapiv1
spark_client = IFLYTEKSparkEndpoints()
resp = spark_client.send(req=req, version='lite')
print(resp.text)
```


# 🌟 Recommended Projects

| Project                                                    | ⭐ Stars                                                                                                                                               | 📦 Version                                                                                                 | ⏱ Last Update                                                                                                                                                                   | 🛠 Repository                                                        |
| -------------                                              | ---------                                                                                                                                             | -----------                                                                                                | ----------------                                                                                                                                                                 | --------                                                             |
| 🎵 **Musicdl**<br/>轻量级无损音乐下载器                    | [![Stars](https://img.shields.io/github/stars/CharlesPikachu/musicdl?style=flat-square)](https://github.com/CharlesPikachu/musicdl)                   | [![Version](https://img.shields.io/pypi/v/musicdl)](https://pypi.org/project/musicdl)                      | [![Last Commit](https://img.shields.io/github/last-commit/CharlesPikachu/musicdl?style=flat-square)](https://github.com/CharlesPikachu/musicdl/commits/master)                   | [🛠 Repository](https://github.com/CharlesPikachu/musicdl)           |
| 🎬 **Videodl**<br/>轻量级高清无水印视频下载器              | [![Stars](https://img.shields.io/github/stars/CharlesPikachu/videodl?style=flat-square)](https://github.com/CharlesPikachu/videodl)                   | [![Version](https://img.shields.io/pypi/v/videofetch)](https://pypi.org/project/videofetch)                | [![Last Commit](https://img.shields.io/github/last-commit/CharlesPikachu/videodl?style=flat-square)](https://github.com/CharlesPikachu/videodl/commits/master)                   | [🛠 Repository](https://github.com/CharlesPikachu/videodl)           |
| 🖼️ **Imagedl**<br/>轻量级海量图片搜索下载器                | [![Stars](https://img.shields.io/github/stars/CharlesPikachu/imagedl?style=flat-square)](https://github.com/CharlesPikachu/imagedl)                   | [![Version](https://img.shields.io/pypi/v/pyimagedl)](https://pypi.org/project/pyimagedl)                  | [![Last Commit](https://img.shields.io/github/last-commit/CharlesPikachu/imagedl?style=flat-square)](https://github.com/CharlesPikachu/imagedl/commits/main)                     | [🛠 Repository](https://github.com/CharlesPikachu/imagedl)           |
| 🌐 **FreeProxy**<br/>全球海量高质量免费代理采集器          | [![Stars](https://img.shields.io/github/stars/CharlesPikachu/freeproxy?style=flat-square)](https://github.com/CharlesPikachu/freeproxy)               | [![Version](https://img.shields.io/pypi/v/pyfreeproxy)](https://pypi.org/project/pyfreeproxy)              | [![Last Commit](https://img.shields.io/github/last-commit/CharlesPikachu/freeproxy?style=flat-square)](https://github.com/CharlesPikachu/freeproxy/commits/master)               | [🛠 Repository](https://github.com/CharlesPikachu/freeproxy)         |
| 🌐 **MusicSquare**<br/>简易音乐搜索下载和播放网页          | [![Stars](https://img.shields.io/github/stars/CharlesPikachu/musicsquare?style=flat-square)](https://github.com/CharlesPikachu/musicsquare)           | [![Version](https://img.shields.io/pypi/v/musicdl)](https://pypi.org/project/musicdl)                      | [![Last Commit](https://img.shields.io/github/last-commit/CharlesPikachu/musicsquare?style=flat-square)](https://github.com/CharlesPikachu/musicsquare/commits/main)             | [🛠 Repository](https://github.com/CharlesPikachu/musicsquare)       |
| 🌐 **FreeGPTHub**<br/>真正免费的GPT统一接口                | [![Stars](https://img.shields.io/github/stars/CharlesPikachu/FreeGPTHub?style=flat-square)](https://github.com/CharlesPikachu/FreeGPTHub)             | [![Version](https://img.shields.io/pypi/v/freegpthub)](https://pypi.org/project/freegpthub)                | [![Last Commit](https://img.shields.io/github/last-commit/CharlesPikachu/FreeGPTHub?style=flat-square)](https://github.com/CharlesPikachu/FreeGPTHub/commits/main)               | [🛠 Repository](https://github.com/CharlesPikachu/FreeGPTHub)        |


# 📚 Citation

If you use this project in your research, please cite the repository,

```
@misc{freegpthub,
    author = {Zhenchao Jin},
    title = {FreeGPTHub: A truly free, unified GPT API gateway—unlike “fake-free” alternatives that hide paywalls behind quotas, trials, or mandatory top-ups.},
    year = {2025},
    publisher = {GitHub},
    journal = {GitHub repository},
    howpublished = {\url{https://github.com/CharlesPikachu/FreeGPTHub}},
}
```


# ⭐️ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=CharlesPikachu/FreeGPTHub&type=date&legend=top-left)](https://www.star-history.com/#CharlesPikachu/FreeGPTHub&type=date&legend=top-left)


# 💖 Appreciation (赞赏 / 打赏)

| WeChat Appreciation QR Code (微信赞赏码)                                                                                       | Alipay Appreciation QR Code (支付宝赞赏码)                                                                                     |
| :--------:                                                                                                                     | :----------:                                                                                                                   |
| <img src="https://raw.githubusercontent.com/CharlesPikachu/FreeGPTHub/main/.github/pictures/wechat_reward.jpg" width="260" />  | <img src="https://raw.githubusercontent.com/CharlesPikachu/FreeGPTHub/main/.github/pictures/alipay_reward.png" width="260" />  |


# 💬 WeChat Official Account (微信公众号)

Charles的皮卡丘 (*Charles_pikachu*)  
![img](https://raw.githubusercontent.com/CharlesPikachu/FreeGPTHub/main/docs/pikachu.jpg)
