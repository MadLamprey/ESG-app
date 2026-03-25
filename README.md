# ESG Edge

ESG Edge is a Streamlit-based frontend for an ESG analysis platform designed to help portfolio managers make more informed, sustainable investment decisions. The broader project positions ESG Edge as a hub for real-time ESG insights, news, portfolio-level summaries, and company-specific analysis.

The application provides two main user experiences:
- **Edge Chat**: a chatbot interface for asking ESG-related questions
- **Edge Dashboard**: a portfolio dashboard showing ESG score breakdowns, stock-level comparisons, and relevant news feeds
- 
## Features

### 1. ESG Chat Interface
The app includes a chat-based interface called **Trailblazers ESG Analyzer**, where users can ask questions and receive answers through an AWS Bedrock agent integration. The interface stores chat history in Streamlit session state and displays user and assistant messages side by side.

### 2. Portfolio Dashboard
The dashboard page allows users to query portfolio data and view:
- portfolio-level **Environmental, Social, and Governance** scores
- company-level ESG scores in tabular form
- bar charts for E, S, and G metrics
- a scrolling panel of trending news related to portfolio companies

### 3. News Integration
The application uses the NewsAPI service to retrieve recent news articles relevant to companies in the portfolio, helping users connect ESG scores with current developments.

### 4. AWS Bedrock Agent Integration
The frontend connects to AWS Bedrock agents for both chatbot responses and dashboard data retrieval. In the project presentation, the solution is described as combining a chatbot, a dashboard, a knowledge base, and retrieval-backed querying to support ESG research workflows.

## Project Context

ESG Edge was built to address three main pain points for portfolio managers:
- ESG research is **time consuming**
- ESG data often has **quality and readability issues**
- it is difficult to judge **materiality and relevance** across ESG metrics

The proposed solution is a one-stop platform that combines:
- a reliable chatbot for ESG queries
- a portfolio dashboard
- ESG score breakdowns
- dynamic investment analysis
- news analysis for case-by-case interpretation of how news may affect ESG scores
