'''
Function:
    Implementation of Player Related Functions
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from __future__ import annotations
import shutil
import subprocess
from typing import List, Optional


'''ensurempv'''
def ensurempv() -> str:
    mpv = shutil.which("mpv")
    if not mpv: raise RuntimeError("mpv not found: please install mpv and make sure it is available in your PATH.")
    return mpv


'''mpvplayurl'''
def mpvplayurl(url: str, vo: Optional[str] = None, extra_args: Optional[List[str]] = None) -> int:
    mpv = ensurempv()
    args = [mpv, "--force-window=no", "--really-quiet"]
    if vo: args += [f"--vo={vo}"]
    if extra_args: args += extra_args
    args += [url]
    return subprocess.call(args)


'''mpvplayplaylist'''
def mpvplayplaylist(urls: List[str], vo: Optional[str] = None, extra_args: Optional[List[str]] = None) -> int:
    mpv = ensurempv()
    args = [mpv, "--force-window=no", "--really-quiet"]
    if vo: args += [f"--vo={vo}"]
    if extra_args: args += extra_args
    args += urls
    return subprocess.call(args)