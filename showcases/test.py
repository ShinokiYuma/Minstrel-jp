import sys
import os
abs_path = os.getcwd()
sys.path.append(abs_path) # Adds higher directory to python modules path.
from models.openai import Generator
import streamlit as st

## コメンテーターエージェント
from agents.agent_commentators import Commentators
## リフレクターエージェント
from agents.agent_reflector import Reflector


def test():
    state = st.session_state
    # col1, col2 = st.columns([1, 1])
    with st.sidebar: ##サイドバー
        st.subheader("ユーザーの要求")
        input = st.text_area("user_input",state.input,height=100,label_visibility="collapsed")
        st.subheader("Minstrelプロンプト")
        prompt_origin = st.text_area("langgpt_prompt",state.prompt,height=500,label_visibility="collapsed") ## 合成後のプロンプト表示（編集も可能）
        
        # if st.button("プロンプトを保存"):
        #     if "test_messages" not in state:
        #         state.test_messages = []
        #         pass
        #     state.test_messages = [{"role": "system", "content": prompt}]
        #     state.prompt = prompt
        #     st.rerun()
        #     pass
        
        
        ## モジュール内容分析&改善ボタン（元のコードでは未実装の機）
        ## 一度、現在のプロンプトを、テストチャットで試しておく必要あり
        if "test_messages" in state:
            if st.button("プロンプトを分析＆改善"):
                ## ここでコメンテーターエージェントに接続する！
                print("【メインシステム】プロンプトを受け付けました。コメンテーターエージェントに接続中．．．") # デバッグ
                commentators = Commentators( ## 初期値定義できる
                    requirement = state.input,
                    prompt = state.prompt,
                    answer = state.response
                )
                ## 5つのコメンテーターエージェントからコメントを取得
                comment_criticize_1 = commentators.com_agent_criticize_1()
                comment_criticize_2 = commentators.com_agent_criticize_2()
                comment_favor_1 = commentators.com_agent_favor_1()
                comment_favor_2 = commentators.com_agent_favor_2()
                comment_natural = commentators.com_agent_natural()
                ## 5つのコメントをまとめる
                comment_overall = f"""
------------------------------------------------------------------
コメント1（批判的）
{comment_criticize_1}
------------------------------------------------------------------
コメント2（批判的）
{comment_criticize_2}
------------------------------------------------------------------
コメント3（好意的）
{comment_favor_1}
------------------------------------------------------------------
コメント4（好意的）
{comment_favor_2}
------------------------------------------------------------------
コメント5（中立的）
{comment_natural}
------------------------------------------------------------------
                """
                print("【コメンテーターエージェント】：コメントを作成しました。リフレクターエージェントに接続中...") ## デバッグ

                ## まとめたコメントをリフレクターエージェントに接続する
                reflector = Reflector(
                    prompt = state.prompt,
                    comment = comment_overall
                )

                ## プロンプトを書き換えて表示
                state.prompt = reflector.ref_agent()
                print(f""" 
----------------------------------------------------------------------
{state.prompt}
----------------------------------------------------------------------
【リフレクターエージェント】：コメントを反映し、プロンプトを改善しました。
                """) ##デバッグ用
                
                ### 改善後のプロンプトを実行
                print("【メインシステム】新しいプロンプトを実行中．．．") ##デバッグ用
                state.test_messages.append({"role": "user", "content": state.prompt})
                response = state.generator.generate_response(state.test_messages)
                state.test_messages.append({"role": "assistant", "content": response})
                st.rerun()
                
                print("【メインシステム】新しいプロンプトでの回答が生成されました。") ##デバッグ用

                st.rerun() ## stateをと表示内容を同期

            pass


    ## ページのメイン

    ## メッセージを表示するチャット（一番最初に合成後のプロンプトを試してくれるやつ）
    ## ここの動作は一番はじめだけ
    if "test_messages" not in state:
        state.test_messages = [{"role": "system", "content": state.prompt}] 
        response = state.generator.generate_response(state.test_messages) ## 合成後プロンプトに対してGeneraterでモデルからの返事を作成
        state.response = response ## 分析&改善用にstateにresponseを追加して保存
        state.test_messages.append({"role": "assistant", "content": response})
        st.rerun()
        pass

    st.subheader("テストチャット")
    ## チャットの内容を順次表示
    for message in state.test_messages:
        if message["role"] == "system":
            continue
        st.chat_message(message["role"]).write(message["content"])
        pass
    
    ## 入力した会話から返事を生成
    if prompt := st.chat_input("会話を入力"):
        state.test_messages.append({"role": "user", "content": prompt})
        response = state.generator.generate_response(state.test_messages)
        state.test_messages.append({"role": "assistant", "content": response})
        st.rerun()
        pass
    pass
