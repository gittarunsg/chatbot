import streamlit as st
from openai import OpenAI

# Show title and description, updated for AI Pipe.
st.title("💬 AI Pipe Chatbot")
st.write(
    "This is a simple chatbot that uses AI Pipe to proxy requests to an OpenAI model. "
    "To use this app, you need to provide your AI Pipe token."
)

# Ask user for their AI Pipe token instead of an OpenAI key.
aipipe_token = st.text_input("AI Pipe Token", type="password")

# Check if the token has been provided.
if not aipipe_token:
    st.info("Please add your AI Pipe token to continue.", icon="🗝️")
else:
    # Create an OpenAI client, configuring it for AI Pipe.
    # 1. Pass the AI Pipe token to the `api_key` parameter.
    # 2. Set the `base_url` to the AI Pipe endpoint.
    client = OpenAI(
        api_key=aipipe_token,
        base_url="https://aipipe.org/openai/v1"
    )

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the client, which now points to AI Pipe.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
