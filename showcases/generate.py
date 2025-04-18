import sys
import os
import json
abs_path = os.getcwd()
sys.path.append(abs_path) # Adds higher directory to python modules path.

import streamlit as st
from modules.get_modules import get_modules
from modules.background import gen_background
from modules.command import gen_command
from modules.constraints import gen_constraints
from modules.goal import gen_goal
from modules.initialization import gen_initialization
from modules.output_format import gen_output_format
from modules.skills import gen_skills
from modules.suggestion import gen_suggestion
from modules.workflow import gen_workflow

module_name_dict = {
    "background": "背景",
    "command": "命令",
    "suggesstion": "提案",
    "goal": "目標",
    "examples": "タスクのサンプル",
    "constraints": "制約",
    "workflow": "ワークフロー",
    "output_format": "出力形式",
    "skills": "スキル",
    "style": "スタイル",
    "initialization": "初期化"
}

module_func_dict = {
    "background": gen_background,
    "command": gen_command,
    "suggesstion": gen_suggestion,
    "goal": gen_goal,
    "examples": None,
    "constraints": gen_constraints,
    "workflow": gen_workflow,
    "output_format": gen_output_format,
    "skills": gen_skills,
    "style": None,
    "initialization": gen_initialization
}

## LangGPTプロンプトを生成するページ
def generate():
    state = st.session_state
    ## ユーザーがタスクの基本的な説明を入力するためのテキストフィールド
    col1, col2 = st.columns([8, 2])
    with col1:
        task = st.text_input("タスクの説明","",label_visibility="collapsed")
        state.input = task ## 入力した文章をstateのinputに保存
        pass
    ## タスクを分析してモジュールを設定するボタン
    with col2:
        if st.button("1．タスク分析でモジュールを設定",type="primary"):
            ## get_modules.pyでどのモジュールをオンにするかを設定する
            state.module_messages = [{"role": "user", "content": f"私がLLMに実行してほしいタスクは：{task}"}]
            state.modules = get_modules(state.generator, state.module_messages)
            pass
    with st.sidebar: ## サイドバー
        st.subheader("基本情報")
        state.role_name = st.text_input("役割","",help="例: 専門家、アシスタントなど")
        state.author = st.text_input("作成者","Minstrel_Jpn")
        state.version = st.number_input("バージョン",min_value=0.1,value=0.1,step=0.1)
        state.description = st.text_area("概要","",height=100)
        st.subheader("モジュール制御")
        if "modules" not in state:
            state.modules = {
                "background": False,
                "command": False,
                "suggesstion": False,
                "goal": False,
                "examples": False,
                "constraints": False,
                "workflow": False,
                "output_format": False,
                "skills": False,
                "style": False,
                "initialization": False
            }
        ## 設定したモジュールのオンオフを表示するトグルボタンを作成（ページ左下のボタン）
        if "on_modules" not in state:
            state.on_modules = {} ## 各モジュールの選択状態を保存する辞書を作る
            pass
        for key in state.modules.keys():
            if key in module_name_dict:
                state.on_modules[key] = st.toggle(module_name_dict[key],state.modules[key]) ## トグルボタンオンオフ設定
                pass
            pass
        pass
    if "modules" in state:
        if state.on_modules["examples"]: ## 「タスクのサンプル」モジュールがオンになったとき
            st.subheader("タスクのサンプルを提供してください：")
            input_area, output_area = st.columns(2)
            with input_area:
                input_example = st.text_area("サンプル入力","")
                pass
            with output_area:
                output_example = st.text_area("サンプル出力","")
                pass
            state.examples = {
                "input": input_example,
                "output": output_example
            }
            pass
        if state.on_modules["style"]: ## 「スタイル」モジュールがオンになったとき
            st.subheader("返信のスタイルを指定してください：")
            style = st.text_input("スタイル","",help="例: 公式、ユーモア、真面目など",label_visibility="collapsed")
            state.style = style
            pass
        ## 生成されたモジュールの表示と編集（既にモジュールが生成されてる）
        for key in state.modules.keys():
            if key in state: ## state[key]に指定されたモジュールの内容が格納されている
                if state.on_modules[key]:
                    with st.expander(module_name_dict[key]):
                        st.text_area(module_name_dict[key],state[key],label_visibility="collapsed")
                        pass
            pass
        ## モジュール生成とプロンプト合成ボタン
        g,c = st.columns([1,1])
        with g:
            generate_button = st.button("2．モジュール内容を生成")
            pass
        with c:
            compose_button = st.button("3．モジュールを合成してプロンプト作成")
            pass
        ## モジュールを生成ボタンが押されたとき
        if generate_button:
            for key in state.modules.keys():
                if key == "examples" or key == "style": ## exampleとstyleはスキップ
                    continue
                else:
                    if state.on_modules[key]: ## onになってるモジュールのみ
                        if key not in state:
                            state[key] = module_func_dict[key](state.generator,state.module_messages) ## ここでモジュールの内容を作成してる
                    pass
                pass
            st.rerun()
            pass
        ## プロンプト合成ボタンが押されたとき
        if compose_button:
            if "prompt" not in state:
                state.prompt = "" ## プロンプト初期化
                pass
            ## 入力された基本情報（役割、作成者、バージョン、説明）をプロンプトに追加
            if state.role_name:
                state.prompt += f"# 役割: {state.role_name}\n"
                pass
            state.prompt += f"## プロフィール\n"
            if state.author:
                state.prompt += f"- 作成者: {state.author}\n"
                pass
            if state.version:
                state.prompt += f"- バージョン: {state.version}\n"
                pass
            if state.description:
                state.prompt += f"- 説明: {state.description}\n"
                pass
            ## チェックしたモジュールがすべて生成されているかチェックする
            for key in state.modules.keys():
                if state.on_modules[key]:
                    if key not in state:
                        st.error(f"先に{module_name_dict[key]}を生成してください")
                        return
                    else:
                        ## 生成されたモジュールをプロンプトに追加
                        if key == "examples":
                            state.prompt += f"## {module_name_dict[key]}\n"
                            state.prompt += f"### 入力\n"
                            state.prompt += state.examples["input"]
                            state.prompt += "\n"
                            state.prompt += f"### 出力\n"
                            state.prompt += state.examples["output"]
                            state.prompt += "\n\n"
                        state.prompt += f"## {key}\n"
                        state.prompt += json.dumps(state[key], ensure_ascii=False, indent=2)
                        # state.prompt += state[key]
                        state.prompt += "\n\n"
                        state.page = "test"
                pass
            st.rerun()
