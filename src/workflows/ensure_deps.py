#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
requirements.txt を読み、現在の環境と比較して不足/不一致のみを導入するユーティリティ。

想定:
- requirements.txt はピン留め形式（package==version）を基本とする
- Windows / Python 3.8+

使い方:
    python src/workflows/ensure_deps.py

挙動:
- 既に同バージョンが入っているパッケージはスキップ
- 未導入 or バージョン不一致のみを pip install する
"""

from __future__ import annotations

import os
import sys
import subprocess
from dataclasses import dataclass
from typing import List, Tuple

try:
    # Python 3.8+
    from importlib import metadata as importlib_metadata
except Exception:  # pragma: no cover
    import importlib_metadata  # type: ignore


@dataclass
class RequirementPin:
    name: str
    version: str

    @property
    def spec(self) -> str:
        return f"{self.name}=={self.version}"


def parse_requirements(requirements_path: str) -> List[RequirementPin]:
    pins: List[RequirementPin] = []
    if not os.path.exists(requirements_path):
        print(f"[WARN] requirements.txt が見つかりません: {requirements_path}")
        return pins

    with open(requirements_path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            # 最低限の対応: name==version のみを扱う
            if "==" in line and not line.startswith("-r "):
                name, version = line.split("==", 1)
                name = name.strip()
                version = version.strip()
                if name and version:
                    pins.append(RequirementPin(name=name, version=version))
            # それ以外の書式はスキップ（必要なら拡張）
    return pins


def get_installed_version(distribution_name: str) -> str | None:
    try:
        return importlib_metadata.version(distribution_name)
    except importlib_metadata.PackageNotFoundError:
        return None
    except Exception:
        return None


def diff_requirements(pins: List[RequirementPin]) -> Tuple[List[RequirementPin], List[RequirementPin]]:
    """(to_install, up_to_date) を返す"""
    to_install: List[RequirementPin] = []
    up_to_date: List[RequirementPin] = []

    for pin in pins:
        installed = get_installed_version(pin.name)
        if installed is None:
            to_install.append(pin)
        elif installed != pin.version:
            to_install.append(pin)
        else:
            up_to_date.append(pin)

    return to_install, up_to_date


def install_requirements(pins: List[RequirementPin]) -> int:
    if not pins:
        print("[OK] 依存関係は最新です。インストールは不要でした。")
        return 0

    specs = [p.spec for p in pins]
    print("[INFO] 次のパッケージを導入/更新します:")
    for s in specs:
        print(f"  - {s}")

    cmd = [sys.executable, "-m", "pip", "install", "--break-system-packages"] + specs
    try:
        return subprocess.call(cmd)
    except Exception as e:
        print(f"[ERROR] pip の実行に失敗しました: {e}")
        return 1


def main() -> int:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    requirements_path = os.path.join(project_root, "requirements.txt")

    print(f"[INFO] 要求仕様: {requirements_path}")
    pins = parse_requirements(requirements_path)
    if not pins:
        print("[WARN] インストール対象が見つかりませんでした（ピン留め行なし）")
        return 0

    to_install, up_to_date = diff_requirements(pins)

    if up_to_date:
        print("[OK] 最新の依存関係:")
        for p in up_to_date:
            print(f"  - {p.spec}")
    else:
        print("[INFO] 最新の依存関係はありませんでした。")

    code = install_requirements(to_install)
    if code == 0 and to_install:
        print("[OK] 依存関係の導入/更新が完了しました。")
    return code


if __name__ == "__main__":
    sys.exit(main())


