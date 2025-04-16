# import streamlit as st
# import plotly.graph_objects as go
# from src.utils.db_connection import ArangoDB
# from src.llm.query_processor import QueryProcessor
# from src.visualization.chart_generator import ChartGenerator
# from src.streamlit.graph_analytics_ui import render_graph_analytics_ui
# from src.weather.weather_impact_ui import render_weather_impact_ui  # Import the new weather impact UI
# from dotenv import load_dotenv
# import traceback

# load_dotenv()

# def initialize_session_state():
#     """Initialize session state variables."""
#     if 'messages' not in st.session_state:
#         st.session_state.messages = []
#     if 'error_count' not in st.session_state:
#         st.session_state.error_count = 0
#     if 'query_history' not in st.session_state:
#         st.session_state.query_history = []

# def check_database_connection():
#     """Check if database connection is working."""
#     try:
#         db = ArangoDB()
#         db.db.collections()
#         return True
#     except Exception as e:
#         st.error(f"Database connection error: {str(e)}")
#         return False

# def process_query(query_processor: QueryProcessor, prompt: str) -> tuple:
#     """Process user query and return results."""
#     try:
#         # Generate and validate AQL
#         aql_query = query_processor.generate_aql(prompt)
#         st.session_state.query_history.append(aql_query)
        
#         # Execute query
#         results = query_processor.execute_query(aql_query)
        
#         # Generate explanation
#         explanation = query_processor.explain_results(results, prompt)
        
#         # Get visualization config
#         viz_config = query_processor.suggest_visualization(results)
        
#         return results, explanation, viz_config, None
#     except Exception as e:
#         error_msg = str(e)
#         st.session_state.error_count += 1
#         return None, None, None, error_msg

# def create_visualization(chart_generator: ChartGenerator, viz_config: dict) -> go.Figure:
#     """Create visualization with error handling."""
#     try:
#         return chart_generator.create_chart(viz_config)
#     except Exception as e:
#         return chart_generator._create_error_chart(str(e))

# def display_debug_info(show_debug: bool, aql_query: str = None):
#     """Display debug information if enabled."""
#     if show_debug and aql_query:
#         with st.expander("Debug Information"):
#             st.code(aql_query, language="sql")
#             st.write("Recent Query History:")
#             for idx, query in enumerate(st.session_state.query_history[-5:]):
#                 st.text(f"{idx + 1}. {query}")

# def main():
#     st.set_page_config(page_title="GeoGraph Guardian", page_icon="🌐", layout="wide")

#     # Apply custom styling
#     st.markdown("""
#     <style>
#     .stApp {
#         background-color: #1E1E1E;
#         color: #FFFFFF;
#     }
#     .chat-message {
#         padding: 1rem;
#         border-radius: 0.5rem;
#         margin-bottom: 1rem;
#         background-color: #2D2D2D;
#     }
#     .error-message {
#         background-color: #442222;
#         padding: 1rem;
#         border-radius: 0.5rem;
#         margin-bottom: 1rem;
#         border-left: 4px solid #ff4444;
#     }
#     .success-message {
#         background-color: #224422;
#         padding: 1rem;
#         border-radius: 0.5rem;
#         margin-bottom: 1rem;
#         border-left: 4px solid #44ff44;
#     }
#     .status-message {
#         background-color: #222244;
#         padding: 1rem;
#         border-radius: 0.5rem;
#         margin-bottom: 1rem;
#         border-left: 4px solid #4444ff;
#     }
#     </style>
#     """, unsafe_allow_html=True)

#     initialize_session_state()

#     # Create tabs for Chat, Graph Analytics, and Weather Impact Analysis
#     tab1, tab2, tab3 = st.tabs(["💬 Chat Assistant", "🧠 Graph Analytics", "🌦️ Weather Impact Analysis"])

#     # Settings and debug options in sidebar
#     with st.sidebar:
#         st.header("Settings")
#         show_debug = st.checkbox("Show Debug Information", value=False)
#         if st.button("Clear Chat History"):
#             st.session_state.messages = []
#             st.session_state.query_history = []
#             st.session_state.error_count = 0

#     # Check database connection
#     if not check_database_connection():
#         return

#     # Chat Interface Tab
#     with tab1:
#         st.title("🤖 GeoGraph Guardian")
#         st.markdown("##### Supply Chain Analysis Assistant")

#         # Display chat history
#         for message in st.session_state.messages:
#             with st.chat_message(message["role"]):
#                 if message["role"] == "user":
#                     st.markdown(message["content"])
#                 else:
#                     if "error" in message:
#                         st.markdown(f"""<div class="error-message">{message["content"]}</div>""", 
#                                 unsafe_allow_html=True)
#                     else:
#                         st.markdown(f"""<div class="chat-message">{message["content"]}</div>""", 
#                                 unsafe_allow_html=True)
#                         if "visualization" in message:
#                             st.plotly_chart(message["visualization"], use_container_width=True)

#         # Chat input and processing
#         if prompt := st.chat_input("Ask about your supply chain..."):
#             st.session_state.messages.append({"role": "user", "content": prompt})
#             with st.chat_message("user"):
#                 st.markdown(prompt)

#             # Process query with status indicators
#             with st.status("Processing query...", expanded=True) as status:
#                 try:
#                     processor = QueryProcessor()
#                     chart_generator = ChartGenerator()
                    
#                     # Generate and execute query
#                     status.write("🧠 Analyzing query...")
#                     results, explanation, viz_config, error = process_query(processor, prompt)
                    
#                     if error:
#                         status.update(label="❌ Error occurred", state="error")
#                         with st.chat_message("assistant"):
#                             st.markdown(f"""<div class="error-message">
#                                 Error Details:<br>
#                                 {error}<br><br>
#                                 Please try rephrasing your question or check the debug information.
#                                 </div>""", unsafe_allow_html=True)
                            
#                             st.session_state.messages.append({
#                                 "role": "assistant",
#                                 "content": error,
#                                 "error": True
#                             })
#                     else:
#                         # Create visualization
#                         status.write("📊 Generating visualization...")
#                         fig = create_visualization(chart_generator, viz_config)
                        
#                         status.update(label="✅ Analysis complete", state="complete")
                        
#                         # Display results
#                         with st.chat_message("assistant"):
#                             st.markdown(f"""<div class="success-message">{explanation}</div>""", 
#                                     unsafe_allow_html=True)
#                             st.plotly_chart(fig, use_container_width=True)
                            
#                             st.session_state.messages.append({
#                                 "role": "assistant",
#                                 "content": explanation,
#                                 "visualization": fig
#                             })

#                     # Show debug information if enabled
#                     display_debug_info(show_debug, st.session_state.query_history[-1] 
#                                     if st.session_state.query_history else None)

#                 except Exception as e:
#                     status.update(label="❌ Error occurred", state="error")
#                     error_msg = f"""**System Error:**\n```\n{str(e)}\n{traceback.format_exc()}\n```"""
                    
#                     with st.chat_message("assistant"):
#                         st.markdown(f"""<div class="error-message">{error_msg}</div>""", 
#                                 unsafe_allow_html=True)
                        
#                         st.session_state.messages.append({
#                             "role": "assistant",
#                             "content": error_msg,
#                             "error": True
#                         })

#     # Graph Analytics Tab
#     with tab2:
#         render_graph_analytics_ui()
    
#     # Weather Impact Analysis Tab
#     with tab3:
#         render_weather_impact_ui()

# if __name__ == "__main__":
#     main()



import streamlit as st
import plotly.graph_objects as go
from src.utils.db_connection import ArangoDB
from src.llm.query_processor import QueryProcessor
from src.visualization.chart_generator import ChartGenerator
from src.streamlit.graph_analytics_ui import render_graph_analytics_ui
from src.weather.weather_impact_ui import render_weather_impact_ui  # Import the new weather impact UI
from dotenv import load_dotenv
import traceback
import base64

load_dotenv()

def initialize_session_state():
    """Initialize session state variables."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'error_count' not in st.session_state:
        st.session_state.error_count = 0
    if 'query_history' not in st.session_state:
        st.session_state.query_history = []

def check_database_connection():
    """Check if database connection is working."""
    try:
        db = ArangoDB()
        db.db.collections()
        return True
    except Exception as e:
        st.error(f"Database connection error: {str(e)}")
        return False

def process_query(query_processor: QueryProcessor, prompt: str) -> tuple:
    """Process user query and return results."""
    try:
        # Generate and validate AQL
        aql_query = query_processor.generate_aql(prompt)
        st.session_state.query_history.append(aql_query)
        
        # Execute query
        results = query_processor.execute_query(aql_query)
        
        # Generate explanation
        explanation = query_processor.explain_results(results, prompt)
        
        # Get visualization config
        viz_config = query_processor.suggest_visualization(results)
        
        return results, explanation, viz_config, None
    except Exception as e:
        error_msg = str(e)
        st.session_state.error_count += 1
        return None, None, None, error_msg

def create_visualization(chart_generator: ChartGenerator, viz_config: dict) -> go.Figure:
    """Create visualization with error handling."""
    try:
        return chart_generator.create_chart(viz_config)
    except Exception as e:
        return chart_generator._create_error_chart(str(e))

def display_debug_info(show_debug: bool, aql_query: str = None):
    """Display debug information if enabled."""
    if show_debug and aql_query:
        with st.expander("Debug Information"):
            st.code(aql_query, language="sql")
            st.write("Recent Query History:")
            for idx, query in enumerate(st.session_state.query_history[-5:]):
                st.text(f"{idx + 1}. {query}")

def main():
    
    st.set_page_config(page_title="GeoGraph Guardian", page_icon="🌐", layout="wide")

    # Apply custom styling
    # st.markdown("""
    # <style>
    # .stApp {
    #     background-color: #1E1E1E;
    #     color: #FFFFFF;
    # }
    # .chat-message {
    #     padding: 1rem;
    #     border-radius: 0.5rem;
    #     margin-bottom: 1rem;
    #     background-color: #2D2D2D;
    # }
    # .error-message {
    #     background-color: #442222;
    #     padding: 1rem;
    #     border-radius: 0.5rem;
    #     margin-bottom: 1rem;
    #     border-left: 4px solid #ff4444;
    # }
    # .success-message {
    #     background-color: #224422;
    #     padding: 1rem;
    #     border-radius: 0.5rem;
    #     margin-bottom: 1rem;
    #     border-left: 4px solid #44ff44;
    # }
    # .status-message {
    #     background-color: #222244;
    #     padding: 1rem;
    #     border-radius: 0.5rem;
    #     margin-bottom: 1rem;
    #     border-left: 4px solid #4444ff;
    # }
    # </style>
    # """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    body {
        font-family: 'Arial', sans-serif;
    }
    [data-testid="stSidebar"] {
        background: #aceaff;
        padding: 25px;
        border-right: 4px solid rgb(0, 192, 174);
        color: #000000 !important;
    }
    [data-testid="stSidebarContent"] {
        background: #aceaff;
        color: #000000 !important;
        font-size: 16px;
    }
    .stButton > button {
        border-radius: 10px;
        background: rgb(118, 210, 255);
        color: black;
        font-weight: bold;
        padding: 10px 20px;
        transition: 0.3s;
        border: none;
    }
    .stButton > button:hover {
        background: rgb(118, 210, 255);
        transform: scale(1.05);
    }
    .stTextArea textarea {
        background: #aceaff;
        color: black !important;
        border-radius: 8px;
    }
    .metric-card {
        background: #aceaff;
        padding: 20px;
        border-radius: 12px;
        color: black;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        margin: 10px 0;
        box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

    

    initialize_session_state()

    # Create tabs for Chat, Graph Analytics, and Weather Impact Analysis
    tab1, tab2, tab3 = st.tabs(["💬 Chat Assistant", "🧠 Graph Analytics", "🌦️ Weather Impact Analysis"])

    # Settings and debug options in sidebar
    with st.sidebar:
        #st.image("/home/kdn-admin/Documents/Intern-Exploratory-Projects/Team/ANKIT-SASHWAT/geograph-guardian/src/streamlit/logo.png", width=120)
        # st.markdown(
        #     """
        #     <style>
        #         .top-left-logo {
        #             position: fixed;
        #             top: 10px;
        #             left: 10px;
        #             z-index: 100;
        #         }
        #     </style>
        #     <div class="top-left-logo">
        #         <img src="/home/kdn-admin/Documents/Intern-Exploratory-Projects/Team/ANKIT-SASHWAT/geograph-guardian/src/streamlit/logo.png" width="200">
        #     </div>
        #     """,
        #     unsafe_allow_html=True
        # )


        # Read and encode image to base64
        with open("src/streamlit/logo.png", "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode()

        # Inject CSS and HTML
        st.markdown(
            f"""
            <style>
                .top-left-logo {{
                    position: fixed;
                    top: 10px;
                    left: 10px;
                    z-index: 100;
                }}
            </style>
            <div class="top-left-logo">
                <img src="data:image/png;base64,{encoded_image}" width="160">
            </div>
            """,
            unsafe_allow_html=True
        )

        st.header("Settings")
        show_debug = st.checkbox("Show Debug Information", value=False)
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.session_state.query_history = []
            st.session_state.error_count = 0

    # Check database connection
    if not check_database_connection():
        return

    # Chat Interface Tab
    with tab1:
        st.title("💬 Chat Assistant")
        st.markdown("##### LLM-powered conversational agent for Supply Chain")

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                if message["role"] == "user":
                    st.markdown(message["content"])
                else:
                    if "error" in message:
                        st.markdown(f"""<div class="error-message">{message["content"]}</div>""", 
                                unsafe_allow_html=True)
                    else:
                        st.markdown(f"""<div class="chat-message">{message["content"]}</div>""", 
                                unsafe_allow_html=True)
                        if "visualization" in message:
                            st.plotly_chart(message["visualization"], use_container_width=True)

        # Chat input and processing
        if prompt := st.chat_input("Ask about your supply chain..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Process query with status indicators
            with st.status("Processing query...", expanded=True) as status:
                try:
                    processor = QueryProcessor()
                    chart_generator = ChartGenerator()
                    
                    # Generate and execute query
                    status.write("🧠 Analyzing query...")
                    results, explanation, viz_config, error = process_query(processor, prompt)
                    
                    if error:
                        status.update(label="❌ Error occurred", state="error")
                        with st.chat_message("assistant"):
                            st.markdown(f"""<div class="error-message">
                                Error Details:<br>
                                {error}<br><br>
                                Please try rephrasing your question or check the debug information.
                                </div>""", unsafe_allow_html=True)
                            
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": error,
                                "error": True
                            })
                    else:
                        # Create visualization
                        status.write("📊 Generating visualization...")
                        fig = create_visualization(chart_generator, viz_config)
                        
                        status.update(label="✅ Analysis complete", state="complete")
                        
                        # Display results
                        with st.chat_message("assistant"):
                            st.markdown(f"""<div class="success-message">{explanation}</div>""", 
                                    unsafe_allow_html=True)
                            st.plotly_chart(fig, use_container_width=True)
                            
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": explanation,
                                "visualization": fig
                            })

                    # Show debug information if enabled
                    display_debug_info(show_debug, st.session_state.query_history[-1] 
                                    if st.session_state.query_history else None)

                except Exception as e:
                    status.update(label="❌ Error occurred", state="error")
                    error_msg = f"""**System Error:**\n```\n{str(e)}\n{traceback.format_exc()}\n```"""
                    
                    with st.chat_message("assistant"):
                        st.markdown(f"""<div class="error-message">{error_msg}</div>""", 
                                unsafe_allow_html=True)
                        
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": error_msg,
                            "error": True
                        })

    # Graph Analytics Tab
    with tab2:
        render_graph_analytics_ui()
    
    # Weather Impact Analysis Tab
    with tab3:
        render_weather_impact_ui()

if __name__ == "__main__":
    main()