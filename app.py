import streamlit as st
import altair as alt
import boto3
import base64
import random
import json
from datetime import datetime
from newsapi import NewsApiClient
from streamlit_option_menu import option_menu

# Initialize News API client
newsapi = NewsApiClient(api_key='449d276efdec4379911e49ee9355a651')
session = boto3.session.Session('us-east-1')
bedrock_agent_client = boto3.client('bedrock-agent', region_name='us-east-1')
bedrock_agent_runtime_client = boto3.client('bedrock-agent-runtime', region_name='us-east-1', aws_access_key_id='AKIAQ3EGSKIHRPD4V56K', aws_secret_access_key='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')

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .stTextInput input {{
        background: url("data:image/png;base64,{bin_str}") no-repeat center center fixed;
        background-size: cover;
        color: white;
        border: 1px solid white;
    }}
    .stTextInput input::placeholder {{
        color: rgba(255, 255, 255, 0.7);
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

def set_styles():
    st.markdown(
        """
        <style>
        .thin-divider {
            border: 1px solid white;
            margin: 0;
            width: 100%;
        }
        .thick-divider {
            padding: 0;
            border: none;
            border-top: 3px solid white;
            margin: 0;
        }
        .header {
            text-align: center;
            padding: 0px;
            font-family: 'Montserrat', sans-serif;
            font-weight: 1000;
        }
        .desc {
            border: 1px solid white;
            text-align: center;
            padding: 20px;
            font-family: 'Montserrat', sans-serif;
            font-size: 100%;
        }
        .stChatMessage {
            background-color: transparent;
            border-radius: 10px;
            border: 1px solid white;
            padding: 10px;
            margin: 10px;
        }
        .answer-score {
            display: flex;
            flex-direction: row;
            align-items: center;
            gap: 10px;
        }
        .esg-score {
            display: flex;
            flex-direction: row;
            align-items: center;
            gap: 5px;
        }
        .arrow {
            border: solid;
            border-width: 0 3px 3px 0;
            display: inline-block;
            padding: 3px;
        }
        .up {
            border-color: #3eff00;
            transform: rotate(-135deg);
            -webkit-transform: rotate(-135deg);
        }
        .down {
            border-color: #ff0000;
            transform: rotate(45deg);
            -webkit-transform: rotate(45deg);
        }
        .news {
            width: 200px;
        }
        .news-bar {
            height: 400px;
            overflow-y: auto;
            border: 1px solid white;
            padding: 10px;
            display: flex;
            flex-direction: column;
            font-size: 10px;
        }
        .news-item {
            margin: 10px;
            text-align: left;
            font-size: 12px;

            a {
                color: #6699CC
            }
        }
        .news-header {
            text-align: center;
            font-family: 'Montserrat', sans-serif;
            font-weight: 500;
            font-size: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def fetch_answer(question):
    response = bedrock_agent_runtime_client.invoke_agent(
        inputText=question,
        agentId='78GAXQITLL',
        agentAliasId='6ZXSBNSZGR',
        sessionId='1234'
    )
    final_answer = None
    event_stream = response['completion']
    try:
        for event in event_stream:
            if 'chunk' in event:
                data = event['chunk']['bytes']
                final_answer = data.decode('utf8')
                print(final_answer[:final_answer.find('<sources>')])
            elif 'trace' in event:
                print(event['trace'])
            else: 
                raise Exception("unexpected event.", event)
    except Exception as e:
        raise Exception("unexpected event.",e)
    
    col1, col2 = st.columns([2, 2])
    with col1:
        st.markdown(f"<div class='stChatMessage'>{question}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='stChatMessage'>{final_answer}</div>", unsafe_allow_html=True)
        
    st.markdown("<script>scrollToBottom();</script>", unsafe_allow_html=True)
    # return final_answer without sources
    return final_answer[:(final_answer.find('<sources>') - 10)]

def main_page():
    title = f"<h1 class='header'>Trailblazers ESG Analyzer</h1></br><p class='desc'>Gain comprehensive ESG insights for companies that you are interested in, empowering you to make informed decisions. Start a chat below to learn more!</p></br>"
    st.write(title, unsafe_allow_html=True)
    st.markdown('<hr class="thick-divider">', unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "show_file_uploader" not in st.session_state:
        st.session_state.show_file_uploader = False

    for i in range(0, len(st.session_state.messages), 2):
        user_message = st.session_state.messages[i]
        assistant_message = st.session_state.messages[i+1] if i+1 < len(st.session_state.messages) else None

        col1, col2 = st.columns([2, 2])
        with col1:
            st.markdown(f"<div class='stChatMessage'>{user_message['content']}</div>", unsafe_allow_html=True)
        if assistant_message:
            with col2:
                st.markdown(f"<div class='stChatMessage'>{assistant_message['content']}</div>", unsafe_allow_html=True)
    
    if st.session_state.show_file_uploader:
        uploaded_files = st.file_uploader("File Uploader", type=["csv"], accept_multiple_files=True, key="uploader")
    else:
        uploaded_files = None

    prompt = st.chat_input("What is up?")

    if prompt:
        question = prompt
        st.session_state.messages.append({"role": "user", "content": question})
        final_answer = fetch_answer(question)
        st.session_state.messages.append({"role": "assistant", "content": final_answer})

    if uploaded_files:
        uploaded_file_names = [uploaded_file.name for uploaded_file in uploaded_files]
        st.session_state.messages.append({"role": "user", "content": f"Files uploaded: {', '.join(uploaded_file_names)}"})

def fetch_trending_news(stocks):
    news = []
    for stock in stocks:
        articles = newsapi.get_everything(q=stock, language='en', sort_by='relevancy')
        for article in articles['articles']:
            if len(article['title']) > 70:
                title = f"{article['title'][:70]}..."
            else:
                title = article['title']
            news.append({
                'title': title,
                'url': article['url'],
                'source': article['source']['name'],
                'publishedAt': article['publishedAt']
            })
    news = sorted(news, key=lambda x: x['publishedAt'], reverse=True)
    return news

def fetch_data(dashboard_agent_runtime_client, inputText="What is my portfolio?"):
    response = dashboard_agent_runtime_client.invoke_agent(
        inputText=inputText,
        agentId='O7WDUFVTUK',
        agentAliasId='TEYUNEU0XC',
        sessionId='1234'
    )
    event_stream = response['completion']
    final_answer = None
    try:
        for event in event_stream:
            if 'chunk' in event:
                data = event['chunk']['bytes']
                final_answer = data.decode('utf8')
            elif 'trace' in event:
                print(event['trace'])
            else: 
                raise Exception("unexpected event.", event)
    except Exception as e:
        raise Exception("unexpected event.", e)
    
    return final_answer

def portfolio_page():
    try:
        title = f"<h1 class='header'>My Portfolio</h1></br>"
        st.write(title, unsafe_allow_html=True)
        st.divider()
        response = None
        stocks = ['Disney', 'Apple', 'Tesla', 'Microsoft']
        e_scores = [random.randint(0, 100) for _ in range(4)]
        s_scores = [random.randint(0, 100) for _ in range(4)]
        g_scores = [random.randint(0, 100) for _ in range(4)]
        overall_e_score = random.randint(0, 100)
        overall_s_score = random.randint(0, 100)
        overall_g_score = random.randint(0, 100)

        if "res_e" not in st.session_state:
            st.session_state.res_e = None
        if "res_s" not in st.session_state:
            st.session_state.res_s = None
        if "res_g" not in st.session_state:
            st.session_state.res_g = None

        prompt = st.chat_input("What is up?")
        if prompt:
            dashboard_agent_runtime_client = boto3.client('bedrock-agent-runtime', region_name='us-east-1', aws_access_key_id='AKIAQ3EGSKIHRPD4V56K', aws_secret_access_key='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')
            response = fetch_data(dashboard_agent_runtime_client, prompt)
            if response.startswith('{'):
                response = json.loads(response)
                stocks = list(map(lambda n: n['company'], response['individual_companies']))
                e_scores = list(map(lambda n: round(n['environmental_score']), response['individual_companies']))
                s_scores = list(map(lambda n: round(n['social_score']), response['individual_companies']))
                g_scores = list(map(lambda n: round(n['governance_score']), response['individual_companies']))
                overall_e_score = response['portfolio']['environmental_score']
                overall_s_score = response['portfolio']['social_score']
                overall_g_score = response['portfolio']['governance_score']

                cols = st.columns([1, 5, 1, 5, 1, 5])
                with cols[0]:
                    st.markdown(
                        '''
                            <div class="divider-vertical-line"></div>
                            <style>
                                .divider-vertical-line {
                                    border-right: 2px solid white;
                                    height: 320px;
                                    margin: auto;
                                }
                            </style>
                        ''',
                        unsafe_allow_html=True
                    )
                with cols[1]:
                    if st.session_state.res_e:
                        cols[1].metric("Environment", overall_e_score, overall_e_score - st.session_state.res_e)
                    else:
                        cols[1].metric("Environment", overall_e_score)
                        st.session_state.res_e = overall_e_score
                with cols[2]:
                    st.markdown(
                        '''
                            <div class="divider-vertical-line"></div>
                            <style>
                                .divider-vertical-line {
                                    border-right: 2px solid white;
                                    height: 320px;
                                    margin: auto;
                                }
                            </style>
                        ''',
                        unsafe_allow_html=True
                    )
                with cols[3]:
                    if st.session_state.res_s:
                        cols[3].metric("Social", overall_s_score, overall_s_score - st.session_state.res_s)
                    else:
                        cols[3].metric("Social", overall_s_score)
                        st.session_state.res_s = overall_s_score
                with cols[4]:
                    st.markdown(
                        '''
                            <div class="divider-vertical-line"></div>
                            <style>
                                .divider-vertical-line {
                                    border-right: 2px solid white;
                                    height: 90px;
                                    margin: auto;
                                }
                            </style>
                        ''',
                        unsafe_allow_html=True
                    )
                with cols[5]:
                    if st.session_state.res_g:
                        cols[5].metric("Governance", overall_g_score, overall_g_score - st.session_state.res_g)
                    else:
                        cols[5].metric("Governance", overall_g_score)
                        st.session_state.res_g = overall_g_score
                
                st.divider()

                data = {
                    "Stocks": stocks,
                    "Environment": e_scores,
                    "Social": s_scores,
                    "Governance": g_scores
                }

                if "data" not in st.session_state:
                    st.session_state.data = data

                cols = st.columns([5, 1, 5])
                with cols[0]:
                    st.table(data)

                    source = alt.pd.DataFrame(data)
                    bars_e = alt.Chart(source).mark_bar().encode(
                        x='Stocks',
                        y='Environment'
                    ).properties(
                        title="Environment",
                        background="transparent",
                        height=200
                    ).configure_axis(disable=True)
                    bars_s = alt.Chart(source).mark_bar().encode(
                        x='Stocks',
                        y='Social'
                    ).properties(
                        title="Social",
                        background="transparent",
                        height=200
                    ).configure_axis(disable=True)
                    bars_g = alt.Chart(source).mark_bar().encode(
                        x='Stocks',
                        y='Governance'
                    ).properties(
                        title="Governance",
                        background="transparent",
                        height=200
                    ).configure_axis(disable=True)

                    cols1 = st.columns(3)
                    with cols1[0]:
                        st.altair_chart(bars_e, use_container_width=True, theme=None)
                    with cols1[1]:
                        st.altair_chart(bars_s, use_container_width=True, theme=None)
                    with cols1[2]:
                        st.altair_chart(bars_g, use_container_width=True, theme=None)
                
                with cols[1]:
                    st.markdown(
                        '''
                            <div class="divider-vertical"></div>
                            <style>
                                .divider-vertical {
                                    border-right: 2px solid white;
                                    height: 460px;
                                    margin: auto;
                                }
                            </style>
                        ''',
                        unsafe_allow_html=True
                    )
                    
                with cols[2]:
                        news = fetch_trending_news(stocks)
                        news_bar = "<div class='news'><div class='news-header'>Trending News</div>"
                        news_html = ""
                        for article in news:
                            news_html += f"""
                                <div class="news-item">
                                    <a href="{article['url']}" target="_blank"><strong>{article['title'][:50]}</strong></a><br>
                                    <small>{article['source']} - {datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').strftime("%H:%M %d/%m/%Y")}</small>
                                </div><hr class="thin-divider">"""
                        news_bar += '<div class="news-bar">'
                        news_bar += news_html
                        news_bar += "</div></div>"
                        st.markdown(news_bar, unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='stChatMessage'>{response}</div>", unsafe_allow_html=True)
    except Exception as e:
        print(e)

def main():
    st.set_page_config(page_title="ESG Edge", layout="centered", initial_sidebar_state="collapsed")
    set_background("./images/wallpaper.jpeg")
    set_styles()

    with st.sidebar:
        st.sidebar.title("ESG Edge", )
        selection = option_menu(
            menu_title=None,
            options=["Home", "My Portfolio"],
            icons=["chat", "graph-up"],
            default_index=0
        )

    if selection == "Edge Chat":
        main_page()
    elif selection == "Edge Dashboard":
        portfolio_page()

if __name__ == "__main__":
    main()
