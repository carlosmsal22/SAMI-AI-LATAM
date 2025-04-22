import openai
import streamlit as st

# Initialize client with proper error handling
try:
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except KeyError:
    st.error("🔑 OpenAI API key not found in secrets! Please configure it in Streamlit Cloud settings.")
    st.stop()
except Exception as e:
    st.error(f"🚨 OpenAI initialization failed: {str(e)}")
    st.stop()

def run_gpt(prompt_config, user_input):
    """Enhanced GPT function with better error handling"""
    try:
        # Setup system instruction
        messages = [{"role": "system", "content": prompt_config.get("instructions", "")}]

        # Add memory from prior interaction if available
        history = st.session_state.get("gpt_memory", [])
        messages.extend(history)

        # Append user input
        messages.append({"role": "user", "content": user_input})

        # Run GPT call with timeout
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            timeout=10  # seconds
        )

        result = response.choices[0].message.content

        # Save message history for chaining
        messages.append({"role": "assistant", "content": result})
        st.session_state["gpt_memory"] = messages[-6:]  # limit memory

        return result
        
    except openai.APIConnectionError:
        st.error("🌐 Connection error - please check your internet connection")
        return None
    except openai.RateLimitError:
        st.error("🐇 API rate limit exceeded - please wait before trying again")
        return None
    except Exception as e:
        st.error(f"⚠️ Unexpected error: {str(e)}")
        return None
