# codex_smoke.py
import os, sys, platform, json, time
print("=== Codex smoke test ===")
print("Python:", sys.version.split()[0])
print("Platform:", platform.platform())
print("CWD:", os.getcwd())

# 列出当前仓库文件
print("\nFiles:", sorted(os.listdir("."))[:30])

# 尝试读取一个密钥（若你在环境里加了 DEMO_SECRET，会被读到）
secret = os.getenv("DEMO_SECRET")
print("\nSecret available?:", bool(secret))
if secret:
    print("Secret (masked):", secret[:3] + "***")

# 依赖可选：如果你稍后在环境里安装了 pandas，会有更多输出
try:
    import pandas as pd
    print("\nPandas version:", pd.__version__)
    print(pd.DataFrame({"x":[1,2,3], "y":[9,8,7]}).describe())
except Exception as e:
    print("\nPandas not installed (this is OK).", repr(e))

# 可选联网测试（若环境未开网络会抛异常，也OK）
try:
    import urllib.request
    with urllib.request.urlopen("https://example.com", timeout=5) as r:
        print("\nHTTP:", r.status, r.reason)
except Exception as e:
    print("\nNetwork check skipped/failed:", repr(e))

print("\nDone at", time.strftime("%Y-%m-%d %H:%M:%S"))
