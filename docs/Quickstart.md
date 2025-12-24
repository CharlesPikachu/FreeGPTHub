# Quick Start

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

