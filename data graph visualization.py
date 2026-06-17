import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Data Visualization Dashboard", layout="wide")
st.title("Data Visualization Dashboard")

uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.success("Dataset Loaded Successfully")
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows", df.shape[0])
    c2.metric("Columns", df.shape[1])
    c3.metric("Missing Values", df.isnull().sum().sum())
    c4.metric("Duplicates", df.duplicated().sum())

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    chart_type = st.sidebar.selectbox(
        "Choose Visualization",
        [
            "Histogram",
            "Box Plot",
            "Scatter Plot",
            "Line Chart",
            "Bar Chart",
            "Pie Chart",
            "Violin Plot",
            "Area Chart",
            "Correlation Heatmap",
            "Pair Plot"
        ]
    )

    if chart_type == "Histogram":
        col = st.selectbox("Select Numeric Column", numeric_cols)
        fig = px.histogram(df, x=col, nbins=30, title=f"Histogram of {col}")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Box Plot":
        col = st.selectbox("Select Numeric Column", numeric_cols)
        fig = px.box(df, y=col, title=f"Box Plot of {col}")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Scatter Plot":
        x = st.selectbox("X Axis", numeric_cols)
        y = st.selectbox("Y Axis", numeric_cols, index=min(1, len(numeric_cols)-1))
        color = st.selectbox("Color By", [None] + categorical_cols)
        fig = px.scatter(df, x=x, y=y, color=color, title=f"{x} vs {y}")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Line Chart":
        x = st.selectbox("X Axis", df.columns)
        y = st.selectbox("Y Axis", numeric_cols)
        fig = px.line(df, x=x, y=y, title=f"{y} over {x}")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Bar Chart":
        x = st.selectbox("Category", categorical_cols)
        y = st.selectbox("Numeric Value", numeric_cols)
        agg = st.selectbox("Aggregation", ["sum", "mean", "count"])

        if agg == "sum":
            chart_df = df.groupby(x)[y].sum().reset_index()
        elif agg == "mean":
            chart_df = df.groupby(x)[y].mean().reset_index()
        else:
            chart_df = df.groupby(x)[y].count().reset_index()

        fig = px.bar(chart_df, x=x, y=y, title=f"{agg.upper()} of {y} by {x}")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Pie Chart":
        col = st.selectbox("Select Category", categorical_cols)
        pie_data = df[col].value_counts().reset_index()
        pie_data.columns = [col, "Count"]
        fig = px.pie(pie_data, names=col, values="Count", title=f"{col} Distribution")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Violin Plot":
        num = st.selectbox("Numeric Column", numeric_cols)
        cat = st.selectbox("Category Column", categorical_cols)
        fig = px.violin(df, y=num, x=cat, box=True, title=f"{num} Distribution by {cat}")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Area Chart":
        x = st.selectbox("X Axis", df.columns)
        y = st.selectbox("Y Axis", numeric_cols)
        fig = px.area(df, x=x, y=y, title=f"Area Chart of {y}")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Correlation Heatmap":
        if len(numeric_cols) >= 2:
            corr = df[numeric_cols].corr()
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)
        else:
            st.warning("Need at least 2 numeric columns.")

    elif chart_type == "Pair Plot":
        if len(numeric_cols) >= 2:
            selected = st.multiselect("Select Columns", numeric_cols, default=numeric_cols[:4])
            if len(selected) > 1:
                fig = sns.pairplot(df[selected])
                st.pyplot(fig.figure)
            else:
                st.warning("Select at least 2 columns.")
        else:
            st.warning("Need multiple numeric columns.")
else:
    st.info("Upload a CSV file to start visualization.")