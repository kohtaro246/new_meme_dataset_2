
for i in range(1, 24001):
    with open('meme_items_24000.txt', mode='a') as f:
        i_str = str(i) + '\n'
        f.write(i_str)