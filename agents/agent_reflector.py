from models.openai import Generator
import streamlit as st
state = st.session_state ##stateをインポート


## Reflectorエージェント
class Reflector:
    def __init__(self, prompt, comment):
        self.current_prompt = prompt
        self.improvement_comment = comment

    def ref_agent(self):
        role = [{"role": "system", "content": f"""
あなたは、Reflectorエージェントです。
あなたの役割は、プロンプトのモジュールの中身を改善することです。
コメンテーターは、5人います。2人は批判的、2人は好意的、1人は中立的です。
5人のコメンテーターからの意見を汲み取って、適切になるように現在のプロンプトのモジュールの内容を改善してください。
モジュールの内容は日本語にしてください。
プロンプトのバージョンは、"以前のバージョン+0.1"にしてください。
"## ○○"の○○がモジュール名となっていますが、モジュール存在自体はそのままで、モジュールの内容だけを確認してください。
改善後のプロンプトのみを出力として提示してください。
----------------------------------------------------------------
以下は、現在のプロンプトと、コメンテーターからの意見です。
現在のプロンプト：
{self.current_prompt}
コメンテーターからの意見：
{self.improvement_comment}
        """}]
        response = state.generator.generate_response(role)
        return response