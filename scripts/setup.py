#!/usr/bin/env python3
"""One command: initialize workspace, install project skills and run checks."""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEPS = [
    ("初始化工作区", "scripts/init_workspace.py"),
    ("安装项目 Codex Skills", "scripts/install_codex_skills.py"),
    ("验证项目", "scripts/validate.py"),
    ("测试目的识别与召回", "scripts/test_purpose_recall.py"),
]

def main() -> int:
    if sys.version_info < (3, 10):
        print("需要 Python 3.10 或更高版本", file=sys.stderr)
        return 2
    for label, file in STEPS:
        print(f"\n[ZLYang] {label}…", flush=True)
        try:
            args = [sys.executable, str(ROOT / file)]
            if file.endswith("/validate.py"):
                args += ["--records", "--runs"]
            subprocess.run(args, cwd=ROOT, check=True)
        except subprocess.CalledProcessError as exc:
            print(f"[ZLYang] {label}失败，退出码 {exc.returncode}", file=sys.stderr)
            return exc.returncode
        except OSError as exc:
            print(f"[ZLYang] {label}失败：{exc}", file=sys.stderr)
            return 1
    print("\n[ZLYang] 安装与检查完成。请用 Codex 打开 ZLYang 文件夹。")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
