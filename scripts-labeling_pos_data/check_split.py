import re

text_1 = 'mirror-image 123123/456465-54654,4456\\12'
text_1_split = re.split(r'\s|/|,|-|\\', text_1)

print('text_1:',text_1)
print('text_1_split:',text_1_split)
