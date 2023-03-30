import streamlit as st

def colored_header(
    label: str = "",
    description: str = ""
):
    """
    Shows a header with a colored underline and an optional description.
    """
    st.markdown(label)
    st.write(
        f'<hr style="background-color: #ff4d4d; margin-top: 0;'
        ' margin-bottom: 0; height: 3px; border: none; border-radius: 3px;">',
        unsafe_allow_html=True,
    )
    if description:
        st.caption(description)

    st.write('')