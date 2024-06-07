import pandas as pd

# Đọc dữ liệu từ file .pkl
df = pd.read_pickle("df.pkl")

# Chuyển đổi các ký tự escape trở lại thành ký tự gốc
df['Description'] = df['Description'].str.replace('\\t', '\t')
df['Description'] = df['Description'].str.replace('\\n', '\n')
df['Description'] = df['Description'].str.replace('\\r', '\r')
df['Description'] = df['Description'].str.replace("&nbsp;", "").replace("<br> <br>", " ")

df['Requirements'] = df['Requirements'].str.replace('\\t', '\t')
df['Requirements'] = df['Requirements'].str.replace('\\n', '\n')
df['Requirements'] = df['Requirements'].str.replace('\\r', '\r')
df['Requirements'] = df['Requirements'].str.replace("&nbsp;", "").replace("<br> <br>", " ")

# Tạo định dạng HTML cho cột Description
df['Description'] = df['Description'].str.replace('\r\n\r\n', '<br>').str.replace('\r\n', '<br>').str.replace('\n', '<br>').str.replace('\r', '<br>').str.replace('<br><br>', '<p>').str.replace('<br>', '<br>')

df['Requirements'] = df['Requirements'].str.replace('\r\n\r\n', '<br>').str.replace('\r\n', '<br>').str.replace('\n', '<br>').str.replace('\r', '<br>').str.replace('<br><br>', '<p>').str.replace('<br>', '<br>')

# Lưu lại dữ liệu đã được chuyển đổi
df.to_pickle("df_html.pkl")

df2 = pd.read_pickle("df_html.pkl")

print(df2.iloc[3000])
print(df2.iloc[3000].Requirements)
