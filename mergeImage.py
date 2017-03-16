# -*- coding:utf-8 -*-


from PIL import Image

#横向合成
def mergei(files, output_file):
    tot = len(files)
    img = Image.open(files[0])
    w, h = img.size[0], img.size[1]
    merge_img = Image.new('RGB', (w * tot, h), 0xffffff)
    i = 0
    for f in files:
        print(f)
        img = Image.open(f)
        merge_img.paste(img, (i, 0))
        i += w
    merge_img.save(output_file)

#纵向合成
def mergej(files, output_file):
    tot = len(files)
    img = Image.open(files[0])
    w, h = img.size[0], img.size[1]
    merge_img = Image.new('RGB', (w, h * tot), 0xffffff)
    j = 0
    for f in files:
        print(f)
        img = Image.open(f)
        merge_img.paste(img, (0, j))
        j += h
    merge_img.save(output_file)



arr = ['1.jpg', '2.jpg', '3.jpg', '4.jpg']
mergei(arr,"m.png")



print("this is a test for VIM!!!")
print("i like coding for VIM!")
