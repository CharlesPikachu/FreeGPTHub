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


# 🧪 Playground

Here are some projects built on top of FreeGPTHub,

...


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

FreeGPTHub provides a unified Python interface to call multiple LLM / MLLM endpoints via provider-specific `*Endpoints` clients.
You create a `ChatRequest`, pick an endpoint client, and call `send()`.

> **Notes:**
> *For security reasons, all free API keys collected by this project have been encrypted.*
> *Therefore, if you’d like to use this project, please first follow the WeChat Official Account “Charles的皮卡丘”, then send the message “FreeGPTHub” via private chat in the backend to obtain the key.*

### Supported Endpoint Clients (What you can import)

The repository currently lists these endpoint clients:

- `IFLYTEKSparkEndpoints`
- `BaiduQianfanEndpoints`
- `OpenAIGPTEndpoints`
- `ZhipuGLMEndpoints`
- `DeepSeekEndpoints`
- `DoubaoEndpoints`
- `AlibabaQwenEndpoints`
- `MiniMaxEndpoints`
- `ModelScopeEndpoints`

You can switch providers by swapping the client class, while keeping the same `ChatRequest`.

### Your First Call (iFLYTEK Spark)

This is the simplest “works-first” example from the repository.

```python
from freegpthub import ChatRequest, IFLYTEKSparkEndpoints

# 1) prepare your request
req = ChatRequest(text="10 * 10 = ?")
# 2) create a client
spark_client = IFLYTEKSparkEndpoints(aes_gem_key=xxx)
# 3) call an endpoint version (provider-specific)
resp = spark_client.send(req=req, version="lite")
print(resp.text)
# 4) try another version
resp = spark_client.send(req=req, version="4.0Ultra")
print(resp.text)
```

If you get errors about `aes_gem_key`, please first follow the WeChat Official Account “Charles的皮卡丘”, then send the message “FreeGPTHub” via private chat in the backend to obtain the `aes_gem_key`.

Some paid models use the free credits from the accounts we created on the corresponding platforms. 
If you see an error, it means those free credits have been exhausted. 
You can switch to your own API key to continue using it.

### Switch Providers (Same Pattern)

Example: ModelScope DeepSeek. The calling pattern is the same: create `ChatRequest`, create client, call `send()`.

```python
from freegpthub import ChatRequest, ModelScopeEndpoints

req = ChatRequest(text="Explain gradient descent in 3 sentences.")
client = ModelScopeEndpoints()
resp = client.send(req=req, version="deepseek-ai/DeepSeek-R1-0528")
print(resp.text)
```

### Arguments & Data Structures (What they mean)

This section explains the core objects used by FreeGPTHub, based on the actual implementation.

#### `ChatRequest`

`ChatRequest` is the unified input object you pass into `endpoint.send(...)`. 

Fields:

- `text` (`str`): The user prompt (default `""`).
- `images` (`Tuple[Any, ...]`): Optional image inputs for vision-capable endpoints (default `()`).
- `openai` (`Dict[str, Any]`): Configuration for OpenAI SDK–style endpoints. You may pass `model` or `messages` here; if not provided, the library uses `version` as the model name and uses a default `messages=[{"role":"user","content": req.text}]`.
- `websocket` (`Dict[str, Any]`): Reserved for websocket-style endpoints (default `{"client": {}}`).
- `extra_payload` (`Dict[str, Any]`): Provider-specific extra payload (default `{}`).
- `meta` (`Dict[str, Any]`): Any metadata you want to carry for logging/debugging (default `{}`).  

Minimal text-only request:  

```python
from freegpthub import ChatRequest

req = ChatRequest(text="10 * 10 = ?")
```

Vision request example (bytes / url / (bytes,mime) are all accepted):

```python
from freegpthub import ChatRequest

req = ChatRequest(
    text="Describe this image.",
    images=(
        "https://example.com/demo.png",
        # open("demo.png", "rb").read(),
        # (open("demo.jpg", "rb").read(), "image/jpeg"),
    ),
)
```

#### `ChatResponse`

`ChatResponse` is the unified output returned by `endpoint.send(...)`.

Fields:

- `text` (`str`): The final generated text.
- `raw` (`Any`): The original provider response object (useful for debugging).
- `api_used` (`str`): Which API route was selected/used inside the endpoint (may be empty if not set).
- `variant_used` (`str`): The fully-qualified variant id used (format: `provider:model:version`).

Example:

```python
resp = endpoint.send(req=req, version="lite")
print(resp.text)
print(resp.api_used, resp.variant_used)
```

#### `ModelIOType` and `Modality`

FreeGPTHub routes requests by I/O modality using `ModelIOType`.

- `Modality` is an enum with: `TEXT`, `IMAGE`, `AUDIO`, `VIDEO`.
- `ModelIOType` defines:
  - `inputs`: a set of input modalities.
  - `outputs`: a set of output modalities.

Common tags:

- `T2T`: text → text
- `TI2T`: text+image → text (vision)

Utilities you may see:

- `ModelIOType.create(inputs=[...], outputs=[...])` to build an IO type.
- `ModelIOType.fromtag("T2T")` to parse a tag.
- `detailedtag()` returns explicit tags like `TI2T`.
- `tag` may return canonical tags like `MM2T` when multiple inputs exist.

In the current `BaseEndpoint.inferio(...)`, only `ChatRequest` is supported:

- if `req.images` is empty: inferred IO is `T2T`
- if `req.images` is non-empty: inferred IO is `TI2T`

#### `BaseEndpoint.send(req, api=None, version=None, request_overrides=None)`

`send()` is the core entry point for all endpoint clients.

Arguments:

- `req` (Any): In practice, a `ChatRequest`. The library infers its IO type via `inferio(req)`.
- `version` (Optional[str]): Which *variant* to use.  
  If omitted, it falls back to `self.default_version`.  
  Must be registered in `self.variants`, otherwise `ValueError`.
- `api` (Optional[str]): Force a specific API route (by name) within the chosen variant.  
  If not provided, the endpoint automatically selects the highest-priority compatible API.
- `request_overrides` (dict): Extra request options passed into the handler (implementation-specific).  

#### `EndpointRegistry` (Discoverability)

`EndpointRegistry` collects all endpoints and can:

- `listall()`: return `describe()` for every registered endpoint
- `findvariantsbyio(io)`: find endpoints/versions supporting a given IO type (string tag like `"T2T"` or a `ModelIOType`)
- `get(provider, model)`: filter endpoints by provider/model

In the project, `REGISTERED_ENDPOINTS` is pre-populated by registering multiple endpoint classes.

```
from freegpthub import REGISTERED_ENDPOINTS

print(REGISTERED_ENDPOINTS.listall())
```

More examples can be found in [scripts/clients](https://github.com/CharlesPikachu/FreeGPTHub/tree/main/scripts/clients).


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
