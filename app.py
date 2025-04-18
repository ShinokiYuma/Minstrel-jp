from showcases.generate import generate
from showcases.test import test
from models.openai import Generator
import streamlit as st

if __name__ == "__main__":
    state = st.session_state
    if "generator" not in state:
        state.generator = Generator(
            api_key = "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",
            base_url = "https://api.openai.com/v1"
        )
        state.generator.set_model("gpt-4o")
        pass
    if "page" not in state:
        state.page = "generate"
        pass
    if state.page == "generate":
        generate()
        pass
    elif state.page == "test":
        test()
        pass
