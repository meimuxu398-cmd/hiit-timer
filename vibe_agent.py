import os
import re
import subprocess
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def generate_code(user_instruction):
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[
            {
                "role": "user",
                "content": f"""
あなたは優秀なWebエンジニアです。
以下の指示に従って、完成したコードのみを出力してください。
説明やMarkdown記法は禁止です。
コードだけをそのまま出力してください。

指示:
{user_instruction}
"""
            }
        ],
    )

    full_text = ""
    for block in response.content:
        if block.type == "text":
            full_text += block.text

    return full_text.strip()


def fix_code(original_code, error_message):
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[
            {
                "role": "user",
                "content": f"""
以下のコードにエラーがあります。
エラーメッセージを参考に修正してください。
修正版の完全なコードのみを出力してください。
説明やMarkdownは禁止です。

エラー:
{error_message}

コード:
{original_code}
"""
            }
        ],
    )

    full_text = ""
    for block in response.content:
        if block.type == "text":
            full_text += block.text

    full_text = full_text.strip()
    full_text = full_text.replace("```python", "").replace("```", "")

    return full_text


def save_code(code_text, filename="generated_app.py"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(code_text)


def run_code(filename="generated_app.py"):
    process = subprocess.Popen(
        ["python", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        # 3秒待ってエラーが出るか確認
        stdout, stderr = process.communicate(timeout=3)
        return process.returncode, stdout, stderr
    except subprocess.TimeoutExpired:
        # タイムアウト = サーバー起動成功とみなす
        print("サーバー起動を検知しました（タイムアウト扱い成功）")
        return 0, "Server started", ""

def read_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

def git_commit(message):
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", message])

def install_missing_package(error_message):
    match = re.search(r"No module named '(.+?)'", error_message)
    if match:
        package_name = match.group(1)
        print(f"パッケージ {package_name} をインストールします...")
        subprocess.run(["uv", "pip", "install", package_name])
        return True
    return False

if __name__ == "__main__":
    mode = input("モードを選択してください (1: 新規生成, 2: 既存修正): ")

    if mode == "1":
        user_input = input("何を作りますか？: ")
        code = generate_code(user_input)
        save_code(code, "index.html")
        print("index.html に保存しました")

    elif mode == "2":
        instruction = input("何を修正しますか？: ")
        current_code = read_file("index.html")

        prompt = f"""
以下は現在のindex.htmlです。

{current_code}

これを次の要件に従って修正してください。

{instruction}

修正版の完全なindex.htmlのみ出力してください。
"""

        code = generate_code(prompt)
        save_code(code, "index.html")
        print("index.html を更新しました")