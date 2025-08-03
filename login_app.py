# usage:
# source .venv/bin/activate
# streamlit run login_app.py [ARGUMENTS]

# ref
# [Streamlit Authenticator を使ってログイン画面を用意 \#Python \- Qiita](https://qiita.com/bassan/items/ed6d821e5ef680a20872) # xline
# ヘッダ部分の不要なボタンを消す。 # xline
# [StreamlitのスタイリングTips \#Python \- Qiita](https://qiita.com/papasim824/items/af2d18f3802e632ffa80) # xline
# 複数ページ # xline
# [Streamlitで認証機能付きマルチページWebアプリを作成する方法 \#Webアプリケーション \- Qiita](https://qiita.com/CodeTea_Ping999/items/bb77b5c20de18f4d7c26) # xline

# ~/.streamlit/config.toml,
# [browser]
#gatherUsageStats = false

# 
# access
# Local URL: http://localhost:8501
# Network URL: http://172.17.12.213:8501 # xline

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

import datetime

import const

HIDE_ST_STYLE = """
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
				        .appview-container .main .block-container{
                            padding-top: 1rem;
                            padding-right: 3rem;
                            padding-left: 3rem;
                            padding-bottom: 1rem;
                        }  
                        .reportview-container {
                            padding-top: 0rem;
                            padding-right: 3rem;
                            padding-left: 3rem;
                            padding-bottom: 0rem;
                        }
                        header[data-testid="stHeader"] {
                            z-index: -1;
                        }
                        div[data-testid="stToolbar"] {
                        z-index: 100;
                        }
                        div[data-testid="stDecoration"] {
                        z-index: 100;
                        }
                </style>
"""


## ユーザー設定読み込み
yaml_path = "config.yaml"

with open(yaml_path) as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    credentials=config['credentials'],
    cookie_name=config['cookie']['name'],
    cookie_key=config['cookie']['key'],
    cookie_expiry_days=config['cookie']['expiry_days'],
)

## UI 
authenticator.login()
# ヘッダのデプロイボタンを消す。
st.markdown(HIDE_ST_STYLE, unsafe_allow_html=True)

# st.session_state.xxxxはリロードしても引き継がれる変数として利用できる。
# pages/page1.pyがある場合、
# from pages import page1
# page1.show_page()で用意した表示用のメソッドを呼び出す。ページ分けしても、pythonの仕組みで別ファイルをimportして呼び出すだけ。
# 
# trueの場合、認証済み
if st.session_state["authentication_status"]:
#    st.set_page_config(page_title="Page Title", layout="wide")

    ## ログイン成功
    with st.sidebar:
        st.markdown(f'## Welcome *{st.session_state["name"]}*')
        authenticator.logout('Logout', 'sidebar')
        st.divider()
    st.write('# ログインしました!')
    dt_now = datetime.datetime.now()
    dtstr = dt_now.strftime('%Y/%m/%d/ %H:%M')
    if st.button('勤務開始'):
        #dtsrt = dt_now.strftime('%Y/%m/%d/ %H:%M:%S')
        st.write('# 開始しました')
        with open(const.TIME_RECORD_FILE, 'a') as f:
            print(dtstr + ',勤務開始', file=f)
    if st.button('勤務終了'):
        st.write('# 終了しました')
        with open(const.TIME_RECORD_FILE, 'a') as f:
            print(dtstr + ',勤務終了', file=f)
    if st.button('出勤'):
        #dtsrt = dt_now.strftime('%Y/%m/%d/ %H:%M:%S')
        st.write('# 出勤しました')
        with open(const.TIME_RECORD_FILE, 'a') as f:
            print(dtstr + ',出勤', file=f)
    if st.button('退勤'):
        st.write('# 退勤しました')
        with open(const.TIME_RECORD_FILE, 'a') as f:
            print(dtstr + ',退勤', file=f)


elif st.session_state["authentication_status"] is False:
    ## ログイン失敗
    st.error('Username/password is incorrect')

elif st.session_state["authentication_status"] is None:
    ## デフォルト
    st.warning('Please enter your username and password')
