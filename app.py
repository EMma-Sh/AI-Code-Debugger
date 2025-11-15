import streamlit as st
from main import check_code_errors, get_ai_sugesstion

st.set_page_config(page_title="AI Code Debugger", page_icon="🛠")

st.title("🤖 AI Code Debugger")
st.write("Paste your Python code below, and I will find errors and suggest fixes!")

# API Key Input
api_key = st.text_input("Enter Your API Key ", type="password")

# Code input area
code_input = st.text_area("Paste your Python code here:", height=300)

if st.button("Check Code"):
    if not api_key:
        st.error("Please enter your API key!")
    elif not code_input.strip():
        st.warning("Please paste your Python code first.")
    else:
        with st.spinner("Analyzing code..."):
            # Check for errors
            errors = check_code_errors(code_input)
            
            if "Your code has been rated" in errors:
                st.success("No major issues found in your code ✅")
                st.write(errors)
            else:
                st.subheader("🛑 Errors Found:")
                st.code(errors, language="text")

                # Get AI suggestion
                suggestion = get_ai_sugesstion(code_input, errors, api_key)
                st.subheader("💡 Suggested Fix:")
                st.code(suggestion, language="python")
