import xlsxwriter, random

workbook = xlsxwriter.Workbook(r'C:\Users\Antho\Desktop\IRF.xlsx')
worksheet = workbook.add_worksheet()

BGIS1 = ['Bowser', 'Delph', 'Goodbear', 'Gore', 'Harper', 'Hensel', 'Hernandez', 'Moyer', 'Simonyi', 'Smith', 'Taylor']
BGIS2 = ['Gomez', 'Ruddy', 'Ferrer', 'Abarca', 'Carrillo', 'Cederbloom', 'Valerino', 'Diamond', 'Hairfield', 'Torre', 'OConnor', 'Villareal', 'Valdez', 'Sroka', 'Ryan', 'Morgan']

worksheet.write(0,0, 'Annex')
worksheet.write(0,1, 'Lesson ID')
worksheet.write(0,2, 'Class')
worksheet.write(0,3, 'Instructor')
worksheet.write(0,4, 'Date')

s1 = 1
s2 = 1
s3 = 1
s4 = 1
list1 = []
list2 = []
list3 = []
list4 = []
list5 = []
list6 = []

while s1 < 100:
    shuffle = random.choice(BGIS2)
    list1.append(shuffle)

    shuffle = random.choice(BGIS2)
    list2.append(shuffle)

    shuffle = random.choice(BGIS2)
    list3.append(shuffle)

    s1 += 1

for (a,b,c) in zip(list1,list2,list3):
    while a == b or a == c or b == c:
        a = random.choice(BGIS2)
        if b == c:
            b = random.choice(BGIS2)
    list4.append(a)
    list5.append(b)
    list6.append(c)

for v in list4:
    worksheet.write(s2,5,v)
    s2 +=1
for v in list5:
    worksheet.write(s3,6,v)
    s3 += 1
for v in list6:
    worksheet.write(s4,7,v)
    s4 += 1

workbook.close()


