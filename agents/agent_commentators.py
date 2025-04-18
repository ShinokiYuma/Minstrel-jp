from models.openai import Generator
import streamlit as st
state = st.session_state ##stateをインポート

## Genaratorクラスの初期設定
# generator = Generator( ## openai.pyの初期値を定義してる
#     api_key = "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",
#     base_url = "https://api.openai.com/v1"
# )
# generator.set_model("gpt-4o")

## commmentatorsエージェント
class Commentators:
    def __init__(self, requirement, prompt, answer):
        self.user_requirement = requirement
        self.current_prompt = prompt
        self.generated_answer = answer

    ## 批判的エージェント1
    def com_agent_criticize_1(self):
        role = [{"role": "system", "content": f"""
あなたは、コメンテーターエージェント（批判的）です。
「ユーザーの要求」と、「プロンプト」と、「AIモデルからの返答」が与えられるので、それらを総合的に確認して、批判的な意見を述べてください。
具体的には、以下の点において意見してください。
- プロンプトの内容に矛盾は生じていないか
- プロンプトは、返答を貰うのに十分な指示をしているか
- 返答は、要求に対して適切な内容を回答しているか
- 返答は、要求に対して望まれた出力の形式であるか
----------------------------------------------
以下は、「ユーザーの要求」と「プロンプト」と「AIモデルからの返答」です。
ユーザーの要求：
{self.user_requirement}
プロンプト：
{self.current_prompt}
AIモデルからの返答：
{self.generated_answer}
"""}]
        response = state.generator.generate_response(role)
        return response

    ## 批判的エージェント2
    def com_agent_criticize_2(self):
        role = [{"role": "system", "content": f"""
あなたは、コメンテーターエージェント（批判的）です。
「ユーザーの要求」と、「プロンプト」と、「AIモデルからの返答」が与えられるので、それらを総合的に確認して、批判的な意見を述べてください。
具体的には、以下の点において意見してください。
- プロンプトの内容に矛盾は生じていないか
- プロンプトは、返答を貰うのに十分な指示をしているか
- 返答は、要求に対して適切な内容を回答しているか
- 返答は、要求に対して望まれた出力の形式であるか
----------------------------------------------
以下は、「ユーザーの要求」と「プロンプト」と「AIモデルからの返答」です。
ユーザーの要求：
{self.user_requirement}
プロンプト：
{self.current_prompt}
AIモデルからの返答：
{self.generated_answer}
        """}]
        response = state.generator.generate_response(role)
        return response

    ## 好意的エージェント1
    def com_agent_favor_1(self):
        role = [{"role": "system", "content": f"""
あなたは、コメンテーターエージェント（好意的）です。
「ユーザーの要求」と、「プロンプト」と、「AIモデルからの返答」が与えられるので、それらを総合的に確認して、好意的な意見を述べてください。
具体的には、以下の点において意見してください。
- プロンプトの内容に矛盾は生じていないか
- プロンプトは、返答を貰うのに十分な指示をしているか
- 返答は、要求に対して適切な内容を回答しているか
- 返答は、要求に対して望まれた出力の形式であるか
----------------------------------------------
以下は、「ユーザーの要求」と「プロンプト」と「AIモデルからの返答」です。
ユーザーの要求：
{self.user_requirement}
プロンプト：
{self.current_prompt}
AIモデルからの返答：
{self.generated_answer}
        """}]
        response = state.generator.generate_response(role)
        return response
    
    ## 好意的エージェント2
    def com_agent_favor_2(self):
        role = [{"role": "system", "content": f"""
あなたは、コメンテーターエージェント（好意的）です。
「ユーザーの要求」と、「プロンプト」と、「AIモデルからの返答」が与えられるので、それらを総合的に確認して、好意的な意見を述べてください。
具体的には、以下の点において意見してください。
- プロンプトの内容に矛盾は生じていないか
- プロンプトは、返答を貰うのに十分な指示をしているか
- 返答は、要求に対して適切な内容を回答しているか
- 返答は、要求に対して望まれた出力の形式であるか
----------------------------------------------
以下は、「ユーザーの要求」と「プロンプト」と「AIモデルからの返答」です。
ユーザーの要求：
{self.user_requirement}
プロンプト：
"{self.current_prompt}
AIモデルからの返答：
{self.generated_answer}
               """}]
        response = state.generator.generate_response(role)
        return response
    
    ## 中立的エージェント
    def com_agent_natural(self):
        role = [{"role": "system", "content": f"""
あなたは、コメンテーターエージェント（中立的）です。
「ユーザーの要求」と、「プロンプト」と、「AIモデルからの返答」が与えられるので、それらを総合的に確認して、中立的な意見を述べてください。
具体的には、以下の点において意見してください。
- プロンプトの内容に矛盾は生じていないか
- プロンプトは、返答を貰うのに十分な指示をしているか
- 返答は、要求に対して適切な内容を回答しているか
- 返答は、要求に対して望まれた出力の形式であるか
----------------------------------------------
以下は、「ユーザーの要求」と「プロンプト」と「AIモデルからの返答」です。
ユーザーの要求：
{self.user_requirement}
プロンプト：
{self.current_prompt}
AIモデルからの返答：
{self.generated_answer}
               """}]
        response = state.generator.generate_response(role)
        return response