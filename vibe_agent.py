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
        max_tokens=1500,
        messages=[
            {
                "role": "user",
                "content": f"""
あなたは優秀なPythonエンジニアです。
以下の指示に従って、完成したPythonコードのみを出力してください。
説明は不要です。コードだけ出力してください。

指示:
{user_instruction}
"""
            }
        ],
    )

    return response.content[0].text


def fix_code(original_code, error_message):
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        messages=[
            {
                "role": "user",
                "content": f"""
以下のPythonコードにエラーがあります。
エラーメッセージを参考に修正してください。
修正版の完全なコードのみを出力してください。

エラー:
{error_message}

コード:
{original_code}
"""
            }
        ],
    )

    return response.content[0].text


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
    user_input = input("何を作りますか？: ")

    code = generate_code(user_input)
    save_code(code)

    for attempt in range(5):
        print(f"\n--- 実行試行 {attempt+1} ---")
        returncode, stdout, stderr = run_code()

        if returncode == 0:
            print("実行成功！")
            print(stdout)
            git_commit(f"Auto commit: {user_input}")
            break
        else:
            print("エラー発生。解析中...")

            if install_missing_package(stderr):
                continue

            print("コード修正中...")
            code = fix_code(code, stderr)
            save_code(code)

    else:
        print("修正できませんでした。")