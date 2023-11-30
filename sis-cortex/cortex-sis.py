# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Handle encoding -- THIS WOULD NEED WORK FOR PRODUCTION!
def clean_and_wrap(the_value):
    ret_val = the_value.replace("'", "\\'")
    return "\'" + ret_val + "\'"


st.session_state['query'] = ''


# Write directly to the app
st.title("Snowflake Cortex")

# Get the current credentials
session = get_active_session()

# default query
query = ""

tab_translate, tab_summarize, tab_sentiment, tab_complete = st.tabs(["Translate", "Summarize", "Sentiment", "Complete"])

################################################################
#### Translate
################################################################
with tab_translate:
    st.header("Cortex-powered Translation 🗼")
    
    # Beautify the dropdowns
    CHOICES = {"en": "English", "fr": "Francáis", "de": "Deutsch", "es": "Español"}
    def format_func(option):
        return CHOICES[option]
    
    # Layout
    col1, col2 = st.columns(2)
    
    # Get the input
    with col1:
        from_language = st.selectbox("From Language", options=list(CHOICES.keys()), format_func=format_func)
    
    with col2:
        to_language = st.selectbox("To Language", options=list(CHOICES.keys()), format_func=format_func)
    
    text_to_translate = st.text_input("Text to Translate")
    
    query = "select snowflake.ml.translate(" + clean_and_wrap(text_to_translate) + "," \
        + clean_and_wrap(from_language) + ", " \
        + clean_and_wrap(to_language) + ") as result"

    if text_to_translate:
        st.session_state['query'] = query

    
        # Do the translation!
        translation = session.sql(query).select(col("result")).collect()    
        st.text_area("Translation", str(translation[0][0]))


################################################################
#### Summarize
################################################################
with tab_summarize:
    st.header("Cortex-powered Summarization")

    text_to_summarize = st.text_area("Text to Summarize")
    
    query = "select snowflake.ml.summarize(" + clean_and_wrap(text_to_summarize) + ") as result"

    if text_to_summarize:
        st.session_state['query'] = query

        # Do the translation!
        summary = session.sql(query).select(col("result")).collect()    
        st.text_area("Summary", str(summary[0][0]))


################################################################
#### Sentiment
################################################################
with tab_sentiment:
    st.header("Cortex-powered Sentiment")

    text_for_analysis = st.text_area("Text to Determine Sentiment")
    
    query = "select snowflake.ml.sentiment(" + clean_and_wrap(text_for_analysis) + ") as result"

    if text_for_analysis:
        st.session_state['query'] = query

        # Do the sentiment!
        summary = session.sql(query).select(col("result")).collect()    
        st.text_input("Sentiment Score", str(summary[0][0]))

################################################################
#### Completion
################################################################
with tab_complete:
    st.header("Cortex-powered LLM Completion")

    llm = st.selectbox("LLM", ['llama2-7b-chat'])
    text_for_analysis = st.text_area("Prompt/Question")
    
    query = "select snowflake.ml.complete(" + clean_and_wrap(llm) + "," \
        + clean_and_wrap(text_for_analysis) + ") as result"

    if text_for_analysis:
        st.session_state['query'] = query

        # Do the sentiment!
        summary = session.sql(query).select(col("result")).collect()    
        st.text_area("Generation Result", str(summary[0][0]))


# Display the resulting query
st.text_area("Resulting Query", st.session_state['query'])



# INFO
# @author:  jeremy.lemmon@snowflake.com