import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Malgun Gothic'

# 세션 상태에서 투표 데이터 관리
if 'vote_data' not in st.session_state:
    st.session_state.vote_data = pd.DataFrame({'항목': ['옵션 1', '옵션 2', '옵션 3'], '투표 수': [0, 0, 0]})
if 'selected_option' not in st.session_state:
    st.session_state.selected_option = None

# 앱 제목
st.title('실시간 투표 앱')

# 새 항목 추가 섹션
with st.form("new_item_form"):
    new_item = st.text_input('새 투표 항목을 추가하세요.')
    submit_new_item = st.form_submit_button('항목 추가')
    if submit_new_item and new_item:
        if new_item in st.session_state.vote_data['항목'].values:
            st.warning('이미 존재하는 항목입니다.')
        else:
            new_row = pd.DataFrame({'항목': [new_item], '투표 수': [0]})
            st.session_state.vote_data = pd.concat([st.session_state.vote_data, new_row], ignore_index=True)
            st.success(f"'{new_item}' 항목이 추가되었습니다.")

# 항목 제거 섹션
with st.form("remove_item_form"):
    remove_item = st.selectbox('제거할 투표 항목을 선택하세요.', st.session_state.vote_data['항목'])
    submit_remove_item = st.form_submit_button('항목 제거')
    if submit_remove_item:
        st.session_state.vote_data = st.session_state.vote_data[st.session_state.vote_data['항목'] != remove_item].reset_index(drop=True)
        if st.session_state.selected_option == remove_item:
            st.session_state.selected_option = None
        st.success(f"'{remove_item}' 항목이 제거되었습니다.")

# 투표 항목 선택
option = st.selectbox('어떤 옵션에 투표하시겠습니까?', st.session_state.vote_data['항목'])

# 투표 버튼
if st.button('투표'):
    if st.session_state.selected_option and st.session_state.vote_data.loc[st.session_state.vote_data['항목'] == st.session_state.selected_option, '투표 수'].iloc[0] > 0:
        st.session_state.vote_data.loc[st.session_state.vote_data['항목'] == st.session_state.selected_option, '투표 수'] -= 1
    st.session_state.vote_data.loc[st.session_state.vote_data['항목'] == option, '투표 수'] += 1
    st.session_state.selected_option = option
    st.success(f"'{option}'에 투표했습니다!")

# 투표 결과 표시
st.write('## 투표 결과')
st.table(st.session_state.vote_data)

# 투표 결과 그래프로 그리기
#fig, ax = plt.subplots()
#ax.bar(st.session_state.vote_data['항목'], st.session_state.vote_data['투표 수'], color='skyblue')
#plt.xticks(rotation=45, ha="right")
#plt.ylabel('votes')
#plt.title('voting results')
#st.pyplot(fig)
