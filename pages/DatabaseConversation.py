# ====================== New File Upload & SQL Functions ======================
import streamlit as st

# Initialize the chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


def extract_schema_from_file(uploaded_file):
    """Extract schema from uploaded file (CSV/Excel)"""
    import pandas as pd
    import io
    
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(io.StringIO(uploaded_file.getvalue().decode('utf-8')))
        elif uploaded_file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(io.BytesIO(uploaded_file.getvalue()))
        else:
            return None
        
        schema = []
        for column in df.columns:
            dtype = str(df[column].dtype)
            if dtype == 'object':
                dtype = 'TEXT'
            elif 'int' in dtype:
                dtype = 'INTEGER'
            elif 'float' in dtype:
                dtype = 'REAL'
            elif 'datetime' in dtype:
                dtype = 'TIMESTAMP'
            schema.append(f"{column} {dtype}")
        
        return {
            "columns": df.columns.tolist(),
            "schema": schema,
            "preview": df.head(3).to_dict('records')
        }
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None

def generate_sql_query(natural_language: str, schema_info: dict) -> str:
    """Convert natural language to SQL using LLM"""
    schema_prompt = f"""
    Available table schema:
    Columns: {', '.join(schema_info['columns'])}
    Data Types: {', '.join(schema_info['schema'])}
    
    Sample data: {schema_info['preview']}
    
    Convert this request to SQL: "{natural_language}"
    Return ONLY the SQL query with no additional explanation.
    """
    
    try:
        client = get_llm_client(st.session_state.llm_provider)
        if st.session_state.llm_provider == "Gemini":
            response = client.generate_content(schema_prompt)
            return response.text.strip()
        else:
            # Adapt for other providers as needed
            response = client.chat.completions.create(
                model="gpt-3.5-turbo" if st.session_state.llm_provider == "Groq" else "claude-3-opus",
                messages=[{"role": "user", "content": schema_prompt}],
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"SQL generation error: {str(e)}")
        return None

def execute_sql_on_data(uploaded_file, sql_query):
    """Execute SQL on uploaded data"""
    import pandas as pd
    import pandasql as ps
    import io
    
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(io.StringIO(uploaded_file.getvalue().decode('utf-8')))
        else:
            df = pd.read_excel(io.BytesIO(uploaded_file.getvalue()))
        
        result = ps.sqldf(sql_query, {'df': df})
        return result
    except Exception as e:
        st.error(f"SQL execution error: {str(e)}")
        return None

# ====================== Modified UI ======================

def show_file_upload_section():
    """File upload and SQL conversion interface"""
    st.sidebar.markdown("## 📁 File Upload")
    uploaded_file = st.sidebar.file_uploader(
        "Upload CSV/Excel for SQL analysis",
        type=['csv', 'xlsx', 'xls']
    )
    
    if uploaded_file:
        if 'file_schema' not in st.session_state or st.session_state.uploaded_file_name != uploaded_file.name:
            st.session_state.file_schema = extract_schema_from_file(uploaded_file)
            st.session_state.uploaded_file_name = uploaded_file.name
            st.session_state.uploaded_file = uploaded_file
        
        if st.session_state.file_schema:
            st.sidebar.success("File schema extracted successfully!")
            with st.sidebar.expander("View File Schema"):
                st.json(st.session_state.file_schema)
            
            st.sidebar.markdown("## 🔍 SQL Query Builder")
            sql_prompt = st.sidebar.text_area(
                "Ask about your data in natural language",
                "e.g., 'Show records where sales > 1000'"
            )
            
            if st.sidebar.button("Generate SQL"):
                if sql_prompt and not sql_prompt.startswith("e.g.,"):
                    sql_query = generate_sql_query(sql_prompt, st.session_state.file_schema)
                    if sql_query:
                        st.session_state.generated_sql = sql_query
                        st.sidebar.code(sql_query, language="sql")
                        
                        if st.sidebar.button("Execute Query"):
                            results = execute_sql_on_data(
                                st.session_state.uploaded_file,
                                sql_query
                            )
                            if results is not None:
                                st.session_state.sql_results = results
                                st.success("Query executed successfully!")
                                st.dataframe(results)
    else:
        if 'file_schema' in st.session_state:
            del st.session_state.file_schema
        if 'generated_sql' in st.session_state:
            del st.session_state.generated_sql

# ====================== Modified Main Interface ======================
if not st.session_state.get('login_successful', False):
    st.warning("You must log in to access this page.")
    st.stop()  # Stop execution here to prevent rendering the rest of the page

# Add to your existing UI setup
show_file_upload_section()

# Modify your existing chat interface to handle SQL queries
if prompt := st.chat_input("Ask Nexus anything..."):
    if 'file_schema' in st.session_state and any(keyword in prompt.lower() for keyword in ['data', 'table', 'select', 'where']):
        # Handle as a data question
        sql_query = generate_sql_query(prompt, st.session_state.file_schema)
        if sql_query:
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": f"Generated SQL:\n```sql\n{sql_query}\n```"
            })
            
            results = execute_sql_on_data(st.session_state.uploaded_file, sql_query)
            if results is not None:
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"Query Results:\n{results.to_markdown()}"
                })
    else:
        # Normal chat handling
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            client = get_llm_client(llm_provider)
            response = generate_response(llm_provider, client, prompt)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
