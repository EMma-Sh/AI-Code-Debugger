import subprocess 
import os
import sys
import huggingface_hub as hf_hub
from huggingface_hub import InferenceClient
def check_code_errors(code):
    """
    Save the user's code into a temp file and run pylint to detect errors.
    Handles UTF-8 encoding issues on Windows.
    """
    temp_file = "temp_code.py"
    
    # Save code using UTF-8
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(code)

    # Run pylint safely with UTF-8
    result = subprocess.run(
        [sys.executable, "-m", "pylint", temp_file, "--disable=R,C"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"  # Replaces bad characters instead of crashing
    )

    output = result.stdout.strip()

    # Clean up temp file
    if os.path.exists(temp_file):
        os.remove(temp_file)

  
    if "syntax-error" in output.lower():
        return (
            "❌ Syntax Error Detected!\n"
            "Your code has a basic issue such as an unclosed string or missing parenthesis.\n\n"
            f"{output}"
        )

    return output


def get_ai_sugesstion(code, errors, api_key):
    """
    Generates AI suggestions for fixing the user's code errors using Hugging Face API.
    """
    try:
        client = InferenceClient(api_key=api_key)

        # Make a clear prompt for the AI model
        prompt = f"""
        The following code has some errors. Please suggest a corrected version.
        ---
        Code:
        {code}

        Errors:
        {errors}
        ---
        """
        response = client.text_generation(
            prompt,
            model="gpt2",  
            max_new_tokens=200,
            temperature=0.2
        )

        return response.strip()

    except StopIteration:
        return "❌ No model provider found. Please check your Hugging Face API key and model name."

    except Exception as e:
        return f"❌ An error occurred while generating suggestions: {str(e)}"
