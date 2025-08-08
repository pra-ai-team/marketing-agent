#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
user_input.md を解析し、input/project-config.yaml に反映するユーティリティ。

想定する入力は `marketing-agent/user_input.md` のフォーム形式。
本モジュールは保守的に動作し、空やプレースホルダ（"ここに入力"）は無視する。
"""

from __future__ import annotations

import os
import re
from typing import Dict, Any, List, Tuple

import yaml


def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _strip_example(text: str) -> str:
    # 日本語全角括弧の例示を削除（例：～）/ 半角も一応対応
    text = re.sub(r"[（(]例：.*?[）)]", "", text)
    return text.strip()


def _normalize_value(value: str) -> str:
    if value is None:
        return ""
    value = _strip_example(value)
    value = value.strip()
    # プレースホルダを無視
    if not value or "ここに入力" in value:
        return ""
    return value


def _ensure_dict_path(d: Dict[str, Any], path: List[str]) -> Dict[str, Any]:
    cur = d
    for key in path:
        if key not in cur or not isinstance(cur.get(key), dict):
            cur[key] = {}
        cur = cur[key]
    return cur


def _set_if_value(d: Dict[str, Any], path: List[str], value: Any, updated_keys: List[str]):
    if value is None:
        return
    if isinstance(value, str) and not value.strip():
        return
    parent = _ensure_dict_path(d, path[:-1]) if path[:-1] else d
    parent[path[-1]] = value
    updated_keys.append(".".join(path))


def _parse_user_input_markdown(md_text: str) -> Dict[str, Any]:
    """user_input.md の内容から設定断片を抽出して返す。
    返却は project-config.yaml の構造に合わせた dict。
    """
    lines = md_text.splitlines()

    # 状態管理
    section = ""

    # 一時格納
    company_name = ""
    location_full = ""
    prefecture = ""
    city = ""
    website = ""
    business_name = ""
    key_features: List[str] = []
    competitors: List[Dict[str, str]] = []
    special_offers = ""
    phone = ""
    email = ""
    lp_purpose = ""
    lp_action = ""
    design_pref = ""
    ng_note = ""
    target_note = ""

    # 競合の作業中バッファ
    current_comp: Dict[str, str] | None = None

    def flush_comp():
        nonlocal current_comp
        if current_comp:
            # 何かしら入力があれば採用
            if any(_normalize_value(v) for v in current_comp.values()):
                # 正規化
                normalized = {
                    "name": _normalize_value(current_comp.get("name", "")),
                    "website": _normalize_value(current_comp.get("website", "")),
                    "category": _normalize_value(current_comp.get("category", "")),
                }
                competitors.append(normalized)
        current_comp = None

    for raw in lines:
        line = raw.rstrip("\n")

        # セクション見出し検出
        if line.startswith("### "):
            # 新しいセクションに入る前に競合をフラッシュ
            if section.startswith("2-3."):
                flush_comp()

            # 現在セクションの更新
            section = line.replace("### ", "").strip()
            continue

        # 1-1. 企業名
        if section.startswith("1-1."):
            m = re.match(r"^\s*-\s*ここに入力:\s*(.*)$", line)
            if m:
                company_name = _normalize_value(m.group(1))
                continue

        # 1-2. 主な営業地域
        if section.startswith("1-2."):
            m_full = re.match(r"^\s*-\s*ここに入力:\s*(.*)$", line)
            if m_full:
                location_full = _normalize_value(m_full.group(1))
                continue
            m_pref = re.match(r"^\s*-\s*都道府県:\s*(.*)$", line)
            if m_pref:
                prefecture = _normalize_value(m_pref.group(1))
                continue
            m_city = re.match(r"^\s*-\s*市区町村:\s*(.*)$", line)
            if m_city:
                city = _normalize_value(m_city.group(1))
                continue

        # 1-3. 公式サイトURL
        if section.startswith("1-3."):
            m = re.match(r"^\s*-\s*ここに入力:\s*(.*)$", line)
            if m:
                website = _normalize_value(m.group(1))
                continue

        # 2-1. サービス/ブランド名
        if section.startswith("2-1."):
            m = re.match(r"^\s*-\s*ここに入力:\s*(.*)$", line)
            if m:
                business_name = _normalize_value(m.group(1))
                continue

        # 2-2. 強み・特徴
        if section.startswith("2-2."):
            m = re.match(r"^\s*-\s*ここに入力\d*:\s*(.*)$", line)
            if m:
                val = _normalize_value(m.group(1))
                if val:
                    key_features.append(val)
                continue

        # 2-3. 競合候補
        if section.startswith("2-3."):
            m_name = re.match(r"^\s*-\s*競合\d+\s*名前:\s*(.*)$", line)
            if m_name:
                # 直前のブロックをフラッシュ
                flush_comp()
                current_comp = {"name": _normalize_value(m_name.group(1)), "website": "", "category": ""}
                continue
            m_url = re.match(r"^\s*-\s*URL:\s*(.*)$", line) or re.match(r"^\s*\-\s*URL\s*:\s*(.*)$", line)
            if m_url:
                if current_comp is None:
                    current_comp = {"name": "", "website": "", "category": ""}
                current_comp["website"] = _normalize_value(m_url.group(1))
                continue
            m_cat = re.match(r"^\s*-\s*カテゴリ:\s*(.*)$", line)
            if m_cat:
                if current_comp is None:
                    current_comp = {"name": "", "website": "", "category": ""}
                current_comp["category"] = _normalize_value(m_cat.group(1))
                continue

        # 2-4. キャンペーン・特別オファー
        if section.startswith("2-4."):
            m = re.match(r"^\s*-\s*ここに入力:\s*(.*)$", line)
            if m:
                special_offers = _normalize_value(m.group(1))
                continue

        # 2-5. 連絡先
        if section.startswith("2-5."):
            m_phone = re.match(r"^\s*-\s*電話:\s*(.*)$", line)
            if m_phone:
                phone = _normalize_value(m_phone.group(1))
                continue
            m_mail = re.match(r"^\s*-\s*メール:\s*(.*)$", line)
            if m_mail:
                email = _normalize_value(m_mail.group(1))
                continue

        # 2-6. LPの目的 / 想定アクション
        if section.startswith("2-6."):
            m_p = re.match(r"^\s*-\s*目的:\s*(.*)$", line)
            if m_p:
                lp_purpose = _normalize_value(m_p.group(1))
                continue
            m_a = re.match(r"^\s*-\s*アクション:\s*(.*)$", line)
            if m_a:
                lp_action = _normalize_value(m_a.group(1))
                continue

        # 2-7. デザイン傾向
        if section.startswith("2-7."):
            m = re.match(r"^\s*-\s*ここに入力:\s*(.*)$", line)
            if m:
                design_pref = _normalize_value(m.group(1))
                continue

        # 2-8. 掲載NG
        if section.startswith("2-8."):
            m = re.match(r"^\s*-\s*ここに入力:\s*(.*)$", line)
            if m:
                ng_note = _normalize_value(m.group(1))
                continue

        # 2-9. ターゲット顧客メモ
        if section.startswith("2-9."):
            m = re.match(r"^\s*-\s*ここに入力:\s*(.*)$", line)
            if m:
                target_note = _normalize_value(m.group(1))
                continue

    # ファイル末尾で競合をフラッシュ
    if section.startswith("2-3."):
        flush_comp()

    # 設定断片の構築
    cfg: Dict[str, Any] = {}

    if company_name:
        _set_if_value(cfg, ["company", "name"], company_name, [])
    if location_full:
        _set_if_value(cfg, ["company", "location"], location_full, [])
    if prefecture:
        _set_if_value(cfg, ["company", "prefecture"], prefecture, [])
    if city:
        _set_if_value(cfg, ["company", "city"], city, [])
    if website:
        _ensure_dict_path(cfg, ["company", "contact"])  # ensure dict
        _set_if_value(cfg, ["company", "contact", "website"], website, [])
    if business_name:
        _set_if_value(cfg, ["company", "business_name"], business_name, [])
    if key_features:
        cfg.setdefault("company", {}).setdefault("key_features", key_features)
    if special_offers:
        _ensure_dict_path(cfg, ["company", "services"])
        _set_if_value(cfg, ["company", "services", "special_offers"], special_offers, [])
    if phone or email:
        _ensure_dict_path(cfg, ["company", "contact"])
        if phone:
            _set_if_value(cfg, ["company", "contact", "phone"], phone, [])
        if email:
            _set_if_value(cfg, ["company", "contact", "email"], email, [])
    if lp_purpose or lp_action or design_pref:
        if lp_purpose:
            _set_if_value(cfg, ["landing_page", "purpose"], lp_purpose, [])
        if lp_action:
            _set_if_value(cfg, ["landing_page", "target_action"], lp_action, [])
        if design_pref:
            _set_if_value(cfg, ["landing_page", "design_preference"], design_pref, [])
    if competitors:
        # 空要素を除去
        cleaned = []
        for comp in competitors:
            if any(comp.get(k) for k in ("name", "website", "category")):
                cleaned.append(comp)
        if cleaned:
            cfg.setdefault("competitors", {})["target_companies"] = cleaned
    if ng_note:
        # 既存の品質レビューに追記形式で残す
        cfg.setdefault("quality_control", {}).setdefault("mandatory_reviews", [])
        cfg["quality_control"]["mandatory_reviews"].append(f"掲載NG・避けたい表現: {ng_note}")
    if target_note:
        # 任意のメモとして保持（拡張フィールド）
        cfg.setdefault("target_customers", {}).setdefault("notes", target_note)

    return cfg


def _deep_merge(base: Dict[str, Any], updates: Dict[str, Any], updated_keys: List[str], path: List[str] | None = None):
    """辞書のディープマージ。更新されたキーを記録。"""
    if path is None:
        path = []
    for key, val in updates.items():
        cur_path = path + [key]
        if isinstance(val, dict):
            node = base.get(key)
            if not isinstance(node, dict):
                base[key] = {}
                node = base[key]
            _deep_merge(node, val, updated_keys, cur_path)
        else:
            base[key] = val
            updated_keys.append(".".join(cur_path))


def apply_user_input_to_config(user_input_md_path: str, config_yaml_path: str) -> Tuple[bool, List[str]]:
    """
    user_input.md を解析し、project-config.yaml にディープマージで反映する。

    Returns:
        (applied, updated_keys)
    """
    if not os.path.exists(user_input_md_path):
        return False, []

    md_text = _read_text(user_input_md_path)
    updates = _parse_user_input_markdown(md_text)

    if not updates:
        return False, []

    # 既存設定の読み込み
    base_cfg: Dict[str, Any] = {}
    if os.path.exists(config_yaml_path):
        try:
            with open(config_yaml_path, "r", encoding="utf-8") as f:
                loaded = yaml.safe_load(f) or {}
                if isinstance(loaded, dict):
                    base_cfg = loaded
        except Exception:
            # 壊れている場合は初期化
            base_cfg = {}

    updated_keys: List[str] = []
    _deep_merge(base_cfg, updates, updated_keys)

    # 保存
    os.makedirs(os.path.dirname(config_yaml_path), exist_ok=True)
    with open(config_yaml_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(base_cfg, f, allow_unicode=True, sort_keys=False)

    return True, updated_keys


