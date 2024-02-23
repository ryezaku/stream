import streamlit as st
import pandas as pd
import base64
from io import BytesIO
from lingua import Language, LanguageDetectorBuilder

# Initialize the language detector with the desired languages
languages = [Language.ENGLISH, Language.MALAY, Language.CHINESE, Language.TAMIL]
detector = LanguageDetectorBuilder.from_languages(*languages).build()

def process_excel(input_file):
    df = pd.read_excel(input_file)
    english_rows = []
    non_english_rows = []
    
    for i in range(len(df)):
        text = df.loc[i]['name']
        try:
            language = detector.detect_language_of(str(text))
            if language == Language.ENGLISH:
                english_rows.append(df.loc[i])
            else:
                non_english_rows.append(df.loc[i])
        except Exception as e:
            # Handle exception if needed
            pass
    
    df_english = pd.DataFrame(english_rows)
    df_non_english = pd.DataFrame(non_english_rows)
    
    return df_english, df_non_english

def get_excel_download_link(df, file_name="processed_data.xlsx"):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Processed Data')
    
    excel_data = output.getvalue()
    b64 = base64.b64encode(excel_data).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{file_name}">Download {file_name}</a>'
    return href

def main():
    st.title('Excel File Processor')
    uploaded_file = st.file_uploader("Upload an Excel file", type="xlsx")

    if uploaded_file is not None:
        processed_df_english, processed_df_non_english = process_excel(uploaded_file)
        
        # Display processed data
        st.write("English Rows:")
        st.dataframe(processed_df_english)
        
        st.write("Non-English Rows:")
        st.dataframe(processed_df_non_english)

        # Download links
        st.markdown(get_excel_download_link(processed_df_english, "english_rows.xlsx"), unsafe_allow_html=True)
        st.markdown(get_excel_download_link(processed_df_non_english, "non_english_rows.xlsx"), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
