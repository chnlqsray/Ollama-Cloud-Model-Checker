# Ollama Cloud Model Checker
# Ollama 云端模型可用性检测工具

A script that tests all known Ollama Cloud models and reports which ones are free on your account.
一个测试所有已知 Ollama Cloud 模型的脚本，报告哪些模型在你的账户下可以免费使用。

---

## Requirements / 环境要求

- Python 3.9+
- An Ollama account and API key: https://ollama.com/settings/keys
- Ollama 账户及 API Key：https://ollama.com/settings/keys

---

## Usage / 使用方法

```bash
pip install -r requirements.txt
```

Set your API key as an environment variable:
将 API Key 设置为环境变量：

```bash
export OLLAMA_API_KEY=your_key_here       # macOS / Linux
set    OLLAMA_API_KEY=your_key_here       # Windows
```

Or paste it directly into the top of `test_ollama_cloud.py`.
或者直接填入 `test_ollama_cloud.py` 文件顶部的变量。

Then run:
然后运行：

```bash
python test_ollama_cloud.py
```

---

## Test Results / 实测结果

Tested on 2026-05-25 with a free account.
测试时间：2026年5月25日，使用免费账户。

After a full test run (41 models), Session usage was only 0.2% — the token consumption is negligible.
完整测试 41 个模型后，Session usage 仅消耗 0.2%，token 消耗可忽略不计。

### ✅ Free / 免费可用 (25 models)

```
gemma4:31b-cloud
nemotron-3-super:cloud
minimax-m2.5:cloud
glm-4.7:cloud
qwen3-coder-next:cloud
minimax-m2.1:cloud
ministral-3:3b-cloud
ministral-3:8b-cloud
ministral-3:14b-cloud
devstral-small-2:24b-cloud
qwen3-next:80b-cloud
nemotron-3-nano:30b-cloud
rnj-1:8b-cloud
devstral-2:123b-cloud
gpt-oss:20b-cloud
gpt-oss:120b-cloud
qwen3-vl:235b-cloud
qwen3-vl:235b-instruct-cloud
qwen3-coder:480b-cloud
minimax-m2:cloud
glm-4.6:cloud
cogito-2.1:671b-cloud
gemma3:4b-cloud
gemma3:12b-cloud
gemma3:27b-cloud
```

### ❌ Subscription required / 需要订阅 (16 models)

```
qwen3.5:cloud
qwen3.5:397b-cloud
glm-5.1:cloud
minimax-m2.7:cloud
glm-5:cloud
gemini-3-flash-preview:latest
gemini-3-flash-preview:cloud
kimi-k2.6:cloud
deepseek-v3.2:cloud
deepseek-v4-flash:cloud
deepseek-v4-pro:cloud
kimi-k2.5:cloud
mistral-large-3:675b-cloud
kimi-k2-thinking:cloud
deepseek-v3.1:671b-cloud
kimi-k2:1t-cloud
```

---

## Notes / 说明

Results may change as Ollama updates its free tier policy.
结果可能随 Ollama 免费政策调整而变化，建议定期重新运行脚本确认。
