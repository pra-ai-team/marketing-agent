#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
後方互換用ラッパー

READMEや旧プロンプトで参照される generic-setup-project.py から
現行の setup-project.py の main() を呼び出すための薄いスクリプト。
"""

import os
import sys
import importlib.util

# workflows ディレクトリ直下の setup-project.py を動的読み込み
SCRIPT_DIR = os.path.dirname(__file__)
TARGET_PATH = os.path.join(SCRIPT_DIR, "setup-project.py")

if not os.path.exists(TARGET_PATH):
    print("❌ setup-project.py が見つかりません。")
    sys.exit(1)

spec = importlib.util.spec_from_file_location("setup_project_module", TARGET_PATH)
module = importlib.util.module_from_spec(spec)  # type: ignore
assert spec and spec.loader
spec.loader.exec_module(module)  # type: ignore

if __name__ == "__main__":
    module.main()


