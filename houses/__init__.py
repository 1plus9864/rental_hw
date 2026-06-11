def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.fields['username'].help_text = '請輸入登入帳號'

    self.fields['password1'].help_text = '''
密碼至少 8 個字元，
不可全部為數字，
不可與帳號過於相似。
'''

    self.fields['password2'].help_text = '再次輸入密碼確認'