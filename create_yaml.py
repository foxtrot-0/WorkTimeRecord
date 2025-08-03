# usage:
#  python create_yaml.py

import csv
import yaml
#from streamlit_authenticator.utilities.hasher import Masher
import streamlit_authenticator as stauth

users_csv_path = "usersetting.csv"
config_yaml_path = "config.yaml"



## ユーザー設定の一覧が記述されたデータを読み込み
with open(users_csv_path, "r") as f:
    csvreader = csv.DictReader(f)
    users = list(csvreader)

## yaml 設定一覧が記述されたデータを読み込み
with open(config_yaml_path,"r") as f:
    yaml_data = yaml.safe_load(f)

## パスワードのハッシュ化
users_dict = {}
for user in users:
    print("pass:" + user["password"])
    #user["password"] = stauth.Hasher([user["password"]]).generate()[0]
    user["password"] = stauth.Hasher.hash(user["password"])
    tmp_dict = {
        "name": user["name"],
        "password": user["password"],
        "email": user["email"],
    }
    users_dict[user["id"]] = tmp_dict

## yaml 書き込み
yaml_data["credentials"]["usernames"] = users_dict
with open(config_yaml_path, "w") as f:
    yaml.dump(yaml_data, f)
    print("完了")
