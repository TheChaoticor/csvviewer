import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page title and layout
st.set_page_config(page_title="CSV File Viewer", layout="wide")
st.title("📜 CSV File Viewer")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    # Load data
    df = pd.read_csv(uploaded_file)
    
    # Sidebar filters
    st.sidebar.header("🔍 Filter Data")
    selected_column = st.sidebar.selectbox("Select Column to Filter", ["None"] + df.columns.tolist())
    search_query = st.sidebar.text_input("Search Query")
    
    # Apply filters
    if selected_column != "None" and search_query:
        df = df[df[selected_column].astype(str).str.contains(search_query, case=False, na=False)]
    
    # Display summary statistics
    with st.expander("📊 Show Data Summary"):
        st.write(df.describe())
    
    # Data visualization
    st.sidebar.header("📈 Data Visualization")
    if st.sidebar.checkbox("Show Charts"):
        chart_type = st.sidebar.selectbox("Select Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart"])
        x_axis = st.sidebar.selectbox("Select X-axis", df.columns.tolist())
        y_axis = st.sidebar.selectbox("Select Y-axis", df.columns.tolist())
        
        fig, ax = plt.subplots()
        if chart_type == "Bar Chart":
            sns.barplot(x=df[x_axis], y=df[y_axis], ax=ax)
        elif chart_type == "Line Chart":
            sns.lineplot(x=df[x_axis], y=df[y_axis], ax=ax)
        elif chart_type == "Scatter Plot":
            sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax)
        elif chart_type == "Pie Chart":
            df.groupby(x_axis)[y_axis].sum().plot.pie(autopct="%1.1f%%", ax=ax)
        st.pyplot(fig)
    
    # Display table with relevant columns
    st.write("### 📌 Data Preview")
    st.dataframe(df, height=600, use_container_width=True, hide_index=True)
    
    # Download button for filtered data
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", csv, "filtered_data.csv", "text/csv")
    
    st.success("✅ Uploaded file successfully displayed!")
else:
    st.info("📂 Please upload a CSV file to preview its content.")
