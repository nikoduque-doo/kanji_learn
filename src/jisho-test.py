from jisho_api.word import Word

r = Word.request('water')
print(type(r))