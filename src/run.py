#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
シンプル実行ラッパー

使い方:
    python src/run.py --quick --outdir output

必要に応じて --company / --company-file / --date / --config を渡してください。
 --config を省略すると input/project-config.yaml を探索し、
 --company-file を省略すると input/company-name.txt を探索します。
"""

import os
import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = PROJECT_ROOT / "src" / "workflows" / "setup-project.py"


def main():
    if not WORKFLOW.exists():
        print("❌ src/workflows/setup-project.py が見つかりません。")
        sys.exit(1)

    # 既定で outdir=output を付与
    args = [sys.executable, str(WORKFLOW), "--outdir", "output"] + sys.argv[1:]

    # プロジェクトルートで実行
    subprocess.check_call(args, cwd=str(PROJECT_ROOT))


if __name__ == "__main__":
    main()


