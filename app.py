import streamlit as st
import re
import pymupdf

st.header("Billinator Chatbot")

if "payExtra" not in st.session_state:
    st.session_state["payExtra"] = False

if not st.session_state["payExtra"]:
    st.button("Waarom moet ik bijbetalen?", key="payExtra", on_click=lambda: st.session_state.update({"payExtra": True}))
else:
    st.write("Om deze vraag te beantwoorden, hebben we eerst jouw factuur nodig.")
    pdf = st.file_uploader("Upload je factuur", type=["pdf"])
    
    if pdf is not None:
        doc = pymupdf.open(stream=pdf.read(), filetype="pdf")
        out = open("output.txt", "wb") # create a text output
        for page in doc: # iterate the document pages
            text = page.get_text().encode("utf8")
            out.write(text) # write text of page
            out.write(bytes((12,))) # write page delimiter (form feed 0x0C)
        out.close()

        with open("output.txt", "r") as f:
            pdftext = f.read().split("\n")
            for i in range(len(pdftext) - 1):
                if pdftext[i].strip() == "Betaald" and pdftext[i+1].strip() == "Totaal":
                    section = pdftext[i+2].strip()
                    number = float(re.search(r'\d+(?:\.\d+)?(?:,\d+)?', section).group().replace(".", "").replace(",", "."))
                    st.write("U heeft " + str(number) + " euro voorschot betaald.")
                    break