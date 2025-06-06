# タスクに必要な制約モジュールを生成

import sys
import os
abs_path = os.getcwd()
sys.path.append(abs_path) # 上位ディレクトリをPythonモジュールのパスに追加

##「制約」モジュール内容を生成するエージェント
def gen_constraints(client, messages):
    messages = [
        {"role": "system", "content": "ユーザーがプロンプトを作成中です。あなたはユーザーがプロンプトの制約部分を完成させるのを手助けする必要があります。まず、ユーザーが与えたタスクを分析し、タスクの実行に必要な制約を特定します。次に、制約に関する具体的な詳細を直接指定します。例えば、長さの制約については「長さは20語以内にしてください」といった具体的な制約を示し、「想定される文字数の範囲」といった曖昧な表現は避けてください。もしユーザーが具体的な制約を示していない場合は、あなたの知識と経験に基づいて内容を補完してください。箇条書き形式で出力し、いかなるインタラクション情報も出力しないでください。例えば、ユーザーがLLMに論文のタイトルを考案してほしい場合、制約情報は次のようになります：\n- タイトルの長さは20文字以内にしてください\n- 侮辱的な言葉を使用しないでください\n- 専門用語を使用してください"},
    ] + messages
    response = client.generate_response(messages)
    return response
