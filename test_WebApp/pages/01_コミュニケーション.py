import openai
import streamlit as st
import os
from audio_recorder_streamlit import audio_recorder
import pandas as pd
import streamlit_authenticator as stauth

st.title("コミュニケーションに関する質問")

questions_dir = "./results/"
question_filenames = os.listdir(questions_dir)
question_filenames = [filename for filename in question_filenames if 'questions.csv' in filename]
print(question_filenames)

st.title("質問&アンケート")
st.caption("これからいくつかの質問に答えていただきます。その後、アンケートにご協力ください。")

# st.write("氏名を入力してください")
st.markdown("""
        ### 氏名を入力してください
        """)
Name = st.text_input('空欄なしで入力し、Enterを押してください','伊藤奈桜')
question_filenames_tmp = [filename for filename in question_filenames if Name in filename]

if len(question_filenames_tmp)==0:
    st.write("あなたの氏名と一致する職歴データが存在しません。担当者へお問い合わせください。")
else:
    tmp_filename = question_filenames_tmp[0]
    Q_csv = pd.read_csv(questions_dir+tmp_filename,index_col=0,encoding='cp932').T
    # st.write(Q_csv)
    # questions_comp = ['Q1:あなたの名前は？', 'Q2:あなたの職業は？', 'Q3:あなたの出身地は？']
    questions_comp = [Q_csv['result_comp_question'][0]]
    questions_deep = [Q_csv['result_deep_question'][0]]
    answers_C = {}
    answers_D = {}

    st.markdown("""
    ### 質問
    次の質問に、音声で回答してください。
    マイクボタンを押すと録音が始まります。ボタンを再度押すか、2秒間沈黙が続くと録音終了します。\n
    録音中はアイコンが赤くなります。うまくいかない場合、マイクをもう一度押してみてください。
    """)
    C_Q_n = 1
    for question in questions_comp:
        q_title = "質問 C-"+str(C_Q_n)
        st.write(f'<span style="color:blue">{q_title}</span>', unsafe_allow_html=True)
        if st.button(q_title+'の質問を表示する'):
            st.write(question)
        answer_audio = audio_recorder(text='　　　　　マイクを押して回答→', key=question, pause_threshold=2)
        answers_C[question] = answer_audio
        C_Q_n += 1
        st.write("\n")
    D_Q_n = 1
    for question in questions_deep:
        q_title = "質問 D-"+str(D_Q_n)
        st.write(f'<span style="color:blue">{q_title}</span>',unsafe_allow_html=True)
        if st.button(q_title+'の質問を表示する'):
            st.write(question)
        answer_audio = audio_recorder(text='　　　　　マイクを押して回答→',key=question,pause_threshold=2)
        answers_D[question] = answer_audio
        D_Q_n += 1
        st.write("\n")

    st.write("\n")
    st.markdown("""
            ### アンケート
            以上の質問について、アンケートに回答してください。
            """)
    st.write("\n")
    C_Q_n = 1
    for question, answer in answers_C.items():
        q_title = "質問 C-" + str(C_Q_n)
        st.write(f'<span style="color:blue">{q_title}</span>'+": "+question, unsafe_allow_html=True)
        # st.write(question)
        st.write("  あなたの回答:")
        st.audio(answer, format="audio/wav")
    D_Q_n = 1
    for question, answer in answers_D.items():
        q_title = "質問 D-" + str(D_Q_n)
        st.write(f'<span style="color:blue">{q_title}</span>'+": "+question, unsafe_allow_html=True)
        # st.write(question)
        st.write("  あなたの回答:")
        st.audio(answer, format="audio/wav")