import streamlit as st
import altair as alt
import base64
import random
from datetime import datetime
from newsapi import NewsApiClient
from streamlit_option_menu import option_menu

# Initialize News API client
newsapi = NewsApiClient(api_key='172888f1419444b7aa01139b6309fad8')

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
    prev_esg_score = random.randint(0, 100)
    evaluated_esg_score = random.randint(0, 100)
    analysis = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam nec purus nec nunc tincidunt aliquam. Nullam nec purus nec nunc tincidunt aliquam. Nullam nec purus nec nunc tincidunt aliquam. Nullam nec purus nec nunc tincidunt aliquam."

    arrow_class = ""
    if evaluated_esg_score > prev_esg_score:
        arrow_class = "up"
    elif evaluated_esg_score < prev_esg_score:
        arrow_class = "down"

    return prev_esg_score, evaluated_esg_score, analysis, arrow_class

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
        prev_score, new_score, analysis, arrow_class = fetch_answer(question)
        arrow_html = f"<i class='arrow {arrow_class}'></i>" if arrow_class else ""
        answer = f"""
        <div style="margin-top: 10px;">
            <div class="answer-score">
            <p class="esg-score"><strong>Computed ESG Score:  </strong> {new_score}  {arrow_html} </p>
            <p>[prev: {prev_score}]</p>
            </div>
            <p><strong>Analysis:</strong> {analysis}</p>
        </div>
        """
        st.session_state.messages.append({"role": "assistant", "content": answer})

        col1, col2 = st.columns([2, 2])
        with col1:
            st.markdown(f"<div class='stChatMessage'>{question}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='stChatMessage'>{answer}</div>", unsafe_allow_html=True)

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

def portfolio_page(curr_score, prev_score):
    title = f"<h1 class='header'>My Portfolio</h1></br>"
    st.write(title, unsafe_allow_html=True)
    st.divider()
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
        cols[1].metric("Environment", curr_score['e'], curr_score['e'] - prev_score['e'])
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
        cols[3].metric("Social", curr_score['s'], curr_score['s'] - prev_score['s'])
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
        cols[5].metric("Governance", curr_score['g'], curr_score['g'] - prev_score['g'])
    
    st.divider()

    stocks = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA"]
    data = {
        "Stocks": stocks,
        "Environment": [random.randint(0, 100) for _ in range(5)],
        "Social": [random.randint(0, 100) for _ in range(5)],
        "Governance": [random.randint(0, 100) for _ in range(5)]
    }

    cols = st.columns([5, 1, 2])
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

def main():
    st.set_page_config(page_title="ESG Analyzer", layout="centered", initial_sidebar_state="collapsed")
    set_background("./images/wallpaper.jpeg")
    set_styles()

    with st.sidebar:
        st.sidebar.title("ESG Analyzer")
        selection = option_menu(
            menu_title=None,
            options=["Home", "My Portfolio"],
            icons=["chat", "graph-up"],
            default_index=0
        )

    if selection == "Home":
        main_page()
    elif selection == "My Portfolio":
        curr_score = {"e": random.randint(0, 100), "s": random.randint(0, 100), "g": random.randint(0, 100)}
        prev_score = {"e": random.randint(0, 100), "s": random.randint(0, 100), "g": random.randint(0, 100)}
        portfolio_page(curr_score, prev_score)

if __name__ == "__main__":
    main()
