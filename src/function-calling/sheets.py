from googleapiclient.discovery import build
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path

# 認証とAPIクライアントの作成
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# 認証情報の読み込み
def get_credentials():
    # サービスアカウントのJSONファイルのパスを指定
    SERVICE_ACCOUNT_FILE = './sheet_credential.json'
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets'
    ]

    # サービスアカウントの資格情報を取得
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    return credentials

# スプレッドシートIDと範囲の設定
SPREADSHEET_ID = '1vSgc-VRZ6f4xqMQC-UThm_XiGIZyZBO-CB_KsIwtpJo'  # スプレッドシートIDを指定
RANGE_NAME = 'シート1!A1:C3'  # 書き込み範囲を指定

# 書き込むデータ
values = [
    ["名前", "年齢", "職業"],
    ["田中太郎", "27", "エンジニア"],
    ["山田花子", "25", "デザイナー"]
]
data = {
    'values': values
}

def main():
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)

    # APIリクエストを送信してデータを書き込み
    sheet = service.spreadsheets()
    result = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption='RAW',
        body=data
    ).execute()

    print(f"{result.get('updatedCells')} cells updated.")

if __name__ == '__main__':
    main()
