import streamlit as st
from utils.scraper import get_serp_results, scrape_page, analyze_content
from utils.scoring import calculate_seo_score

st.title("🚀 SEO Research Tool")
keyword = st.text_input("Enter a keyword to analyze:")
user_content = st.text_area("Paste your content for scoring:")

if st.button("Run Analysis"):
    with st.spinner("Fetching SERP results..."):
        urls = get_serp_results(keyword)
        competitor_data = [analyze_content(scrape_page(url)) for url in urls]
    
    st.subheader("Top 10 Competitors Analyzed")
    st.write(urls)
    
    # Score user content
    if user_content:
        user_analysis = analyze_content(f"<html><body>{user_content}</body></html>")
        score = calculate_seo_score(user_analysis, competitor_data)
        st.metric("SEO Score", f"{score}/100")
        
        # Visualize gaps
        st.subheader("Missing Keywords")
        missing = set().union(*[d["keywords"] for d in competitor_data]) - set(user_analysis["keywords"])
        st.write(", ".join(missing))
