# DramaMoyu CLI

Your go-to terminal app for watching short dramas while "working".

[中文说明 → README.md](https://github.com/CharlesPikachu/FreeGPTHub/blob/main/playground/dramamoyu/README.md)

---

### Introduction

dramamoyu is a command-line tool for watching short dramas while slacking off. It supports:

- Multiple search engines (HongGuo by default)
- Multi-episode short dramas (one drama → multiple episodes)
- Play / resume / binge
- AI search suggestions & keyword rewriting (FreeGPTHub + MiniMax-M2)
- Save cache and watch progress using a pkl file
- Stable playback based on mpv (optional terminal rendering)

Great for slacking off during research / at work / over SSH on a server.

---

### Features

#### Core Features

- Multiple search engines
  - HongGuo Short Drama (default)
  - QiMao Short Drama
  - WeiGuan Short Drama
  - BaiDu Short Drama
  - HeMa Short Drama
- Multi-episode short drama support
  - Search returns “dramas”
  - Each drama contains multiple episodes
- Playback controls
  - Play a specified episode
  - Resume (auto-play the next episode)
  - Binge (play a specified episode range)
- Local state cache (pkl)
  - Recent search results
  - Episode list cache
  - Watch progress for each drama

#### AI Features (FreeGPTHub + MiniMax-M2)

- Search keyword suggestions (highlight-driven / “爽点” oriented)
- Rewrite colloquial requests into searchable keywords
- Hook-episode recommendation (which episode to start from)

---

### Installation

Install via python package:

```python
pip install freegpthub-dramamoyu
```

mpv installation reference: [https://mpv.io/installation/](https://mpv.io/installation/)

---

### Quick Start

```sh
usage: drama_moyu [-h] [--lang {zh,en,auto}]
                  [--engine {HeMaProvider,BaiDuProvider,QiMaoProvider,WeiGuanProvider,HongGuoProvider}]
                  [--state STATE] [--aesgemkey AESGEMKEY]
                  {search,eps,play,resume,binge,ai} ...

Slack off in terminal watching short dramas: multi-episode playback + optional search engines + AI search assistant

positional arguments:
  {search,eps,play,resume,binge,ai}
    search              Search short dramas (drama-level)
    eps                 Get the episode list of a drama (based on recent search result idx)
    play                Play a specific episode of a drama (based on recent search result idx)
    resume              Resume: play the next episode recorded last time
    binge               Binge: play an episode range
    ai                  AI features (FreeGPTHub + MiniMaxEndpoints)

options:
  -h, --help            show this help message and exit
  --lang {zh,en,auto}
  --engine {HeMaProvider,BaiDuProvider,QiMaoProvider,WeiGuanProvider,HongGuoProvider}
                        Search engine (default: HongGuoProvider)
  --state STATE         pkl state file path (default: ~/.drama_moyu_state.pkl)
  --aesgemkey AESGEMKEY
                        AES GEM KEY PATH, key file path required by FreeGPTHub when using AI features, e.g.: aes_gem_key.txt
```

Default search engine: HongGuo Short Drama (HongGuoProvider)

- Search short dramas (by “drama”):
  ```sh
  dramamoyu search "总裁复仇"
  ```

- View the episode list of the first search result:
  ```sh
  dramamoyu eps 1
  ```

- Play episode 3 of the first drama:
  ```sh
  dramamoyu play 1 --ep 3
  ```

- Resume (auto next episode):
  ```sh
  dramamoyu resume 1
  ```

- Binge (play episodes 1 to 10 of the first drama):
  ```sh
  dramamoyu binge 1 --from 1 --to 10
  ```

- Switch/specify another search engine:
  ```sh 
  # QiMao Short Drama 
  dramamoyu --engine QiMaoProvider search "霸道总裁"
  # BaiDu Short Drama
  dramamoyu --engine BaiDuProvider search "霸道总裁"
  # WeiGuan Short Drama
  dramamoyu --engine WeiGuanProvider search "霸道总裁"
  # HeMa Short Drama
  dramamoyu --engine HeMaProvider search "霸道总裁"
  ```

- Terminal-rendered playback (optional; on some systems mpv can render video in the terminal):
  ```sh
  dramamoyu play 1 --ep 1 --vo tct
  dramamoyu play 1 --ep 1 --vo caca
  ```

- AI feature: keyword suggestions (get the key by following the WeChat public account “Charles的皮卡丘”, reply “FreeGPTHub” to obtain it)
  ```sh
  dramamoyu --aesgemkey "aes_gem_key.txt" ai suggest --mood "爽" --avoid "虐" -n 10
  ```

- AI feature: rewrite colloquial request (get the key by following the WeChat public account “Charles的皮卡丘”, reply “FreeGPTHub” to obtain it)
  ```sh
  dramamoyu --aesgemkey "aes_gem_key.txt" ai rewrite "我想看节奏快、反转多、女主很强的短剧"
  ```

- AI feature: hook-episode recommendation (get the key by following the WeChat public account “Charles的皮卡丘”, reply “FreeGPTHub” to obtain it)
  ```sh
  dramamoyu --aesgemkey "aes_gem_key.txt" ai hook 1
  ```

- The default state file is saved at `~/.drama_moyu_state.pkl`. You can change it like this:
  ```sh
  dramamoyu --state ./my_state.pkl search "霸道总裁"
  ```