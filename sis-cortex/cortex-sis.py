# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Handle encoding -- THIS WOULD NEED WORK FOR PRODUCTION!
def clean_and_wrap(the_value):
    ret_val = the_value.replace("'", "\\'")
    return "\'" + ret_val + "\'"

# Write directly to the app
st.title("Snowflake Cortex")

# Get the current credentials
session = get_active_session()

# default query
query = ""

tab_translate, tab_summarize, tab_sentiment, tab_complete, tab_answer = st.tabs(["Translate", "Summarize", "Sentiment", "Complete", "Extract Answer"])

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
        + clean_and_wrap(to_language) + ")"

    
    if text_to_translate:

        # Display the resulting query
        with st.expander("Cortex Query", expanded=True):
            st.code(query, "sql")
    
        # Do the translation!
        translation = session.sql(query).collect()    
        with st.expander("Translation", expanded=True):
            st.write(str(translation[0][0]))


################################################################
#### Summarize
################################################################
with tab_summarize:
    st.header("Cortex-powered Summarization")

    text_to_summarize = st.text_area("Text to Summarize")
    
    query = "select snowflake.ml.summarize(" + clean_and_wrap(text_to_summarize) + ")"


    if text_to_summarize:

        # Display the resulting query
        with st.expander("Cortex Query", expanded=True):
            st.code(query, "sql")

        # Do the translation!
        summary = session.sql(query).collect()    
        with st.expander("Summary", expanded=True):
            st.write(str(summary[0][0]))


################################################################
#### Sentiment
################################################################
with tab_sentiment:
    st.header("Cortex-powered Sentiment")

    text_for_analysis = st.text_area("Text to Determine Sentiment")
    
    query = "select snowflake.ml.sentiment(" + clean_and_wrap(text_for_analysis) + ")"

    if text_for_analysis:
        # Display the resulting query
        with st.expander("Cortex Query", expanded=True):
            st.code(query, "sql")


        # Do the sentiment!
        summary = session.sql(query).collect()    
        with st.expander("Sentiment Score", expanded=True):
            st.metric("Sentiment Score", "", delta=summary[0][0], label_visibility="hidden")

################################################################
#### Completion
################################################################
with tab_complete:
    st.header("Cortex-powered LLM Completion")

    llm = st.selectbox("LLM", ['llama2-7b-chat', 'llama2-70b-chat'])
    text_for_analysis = st.text_area("Prompt/Question")
    
    query = "select snowflake.ml.complete(" + clean_and_wrap(llm) + "," \
        + clean_and_wrap(text_for_analysis) + ")"

    if text_for_analysis:

        # Display the resulting query
        with st.expander("Cortex Query", expanded=True):
            st.code(query, "sql")

        # Do the sentiment!
        summary = session.sql(query).collect()    
        with st.expander("Generation Result", expanded=True):
            st.write(str(summary[0][0]))

        with st.expander("Sample Prompt", expanded=False):
            st.write("For an alternatives investor interested in optimizing their portfolio, but also considering ESG concerns of their clients, what should be evaluated in company filings?")


################################################################
#### Extract Answer
################################################################
with tab_answer:
    st.header("Cortex-powered LLM Answer Extraction")

    question = st.text_input("Question")
    text_for_analysis = st.text_area("Content to Analyze", height=250)
    
    query = "select snowflake.ml.extract_answer(" \
        + clean_and_wrap(text_for_analysis) + "," \
        + clean_and_wrap(question) + ")"

    if text_for_analysis and question:

        # Display the resulting query
        with st.expander("Cortex Query", expanded=True):
            st.code(query, "sql")

        # Do the sentiment!
        summary = session.sql(query).collect()    
        with st.expander("Cortex Answer", expanded=True):
            st.write(str(summary[0][0]))



# INFO
# @author:  jeremy.lemmon@snowflake.com