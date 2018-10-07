import nltk
import xlrd

#================================================================
# Memasukan seluruh sumber artikel ke list pada python dan di tokenisasi

temp = list()

book = xlrd.open_workbook("1301154265_DataSet.xlsx")
sh = book.sheet_by_index(0)

for i in range(sh.nrows):
    if (i > 0):
        temp.append(sh.cell_value(i,2))

allDataSet = ''.join(temp)

totalContent = nltk.word_tokenize(allDataSet.lower())

#======================================================================

# perhitungan count bigram

dictionary = {}
j = 0

for i in range((len(totalContent))-1):
    j = (i + 1)
    if (totalContent[i],totalContent[j]) in dictionary: # melakukan perhitungan kata bigram pada dictionary / count(w(i-1),w(i))
        dictionary[str(totalContent[i]), str(totalContent[j])] += 1
    else :
        dictionary[str(totalContent[i]), str(totalContent[j])] = 1

#======================================================================

# perhitungan count unigram

dictionary2 = {}

for token in totalContent: # melakukan perhitungan kata unigram pada dictionary2 / count(w(i))
    if token in dictionary2:
        dictionary2[token] += 1
    else:
        dictionary2[token] = 1

#======================================================================

# perhitungana probability

dictionary3 = {}

for i in range(len(totalContent)-1):
    j = (i+1)
    dictionary3[str(totalContent[i]),str(totalContent[j])] = dictionary[totalContent[i],totalContent[j]] / dictionary2[totalContent[i]]

# melakukan perhitungan Maximum Likelihood Estimate --> p(w(i)|w(i-1)) = count(w(i-1),w(i)) / count(w(i-1))

#=======================================================================

# memprediksi kata yang keluar selanjutnya dari inputan menggunakan probability

word = input("Masukan kata untuk di prediksi kemunculan selanjutnya : ").lower()
prediksi = ''
max = -9999999
for i in totalContent:
    if (word,i) in dictionary3.keys():
        if (max <= dictionary3[word,i]):
            max = dictionary3[word,i]
            prediksi = i

if (prediksi == ''):
    prediksi = 'null'

print(word,prediksi)

# melakukan pengecekan terhadap kata inputan dari user apabila 2 kata bigram terdapat pada dictionary
# maka akan dicari propbability tertingginya

#========================================================================

# hitung perplexity

def smoothingAddOne(arrayInput,dictionary):
    V = 0
    array = list()

    for i in dictionary: # menambahkan setiap count dengan angka 1 terhadap semua bigram
        dictionary[i] += 1


    for i in range(len(arrayInput)-1): # menambahkan kata yang tidak ada pada bigram
        j = (i+1)
        if (arrayInput[i],arrayInput[j]) in dictionary.keys():
            dictionary[str(arrayInput[i]),str(arrayInput[j])] += 1
        else :
            dictionary[str(arrayInput[i]), str(arrayInput[j])] = 1


    for token in arrayInput: # menambahkan kata yang tidak ada pada unigram
        if token in dictionary2:
            dictionary2[token] += 1
        else:
            dictionary2[token] = 1


    for i in range(len(arrayInput)): # perhitungan mencari nilai V
        count = 0
        for j in range(len(arrayInput)):
            if arrayInput[i] == arrayInput[j]:
                count += 1

        if (count == 1):
            V += 1
        else :
            if (len(array) == 0):
                array.append(arrayInput[i])
            else :
                if (arrayInput[i]) not in array:
                    array.append(arrayInput[i])

    V += len(array) # V merupakan -> distinct Vocabulary dari sekumpulan kata test


    for i in range(len(arrayInput) - 1): # melakukan perhitungan probability menggunakan rumus smoothing
        j = (i + 1)
        dictionary3[str(arrayInput[i]), str(arrayInput[j])] = ((dictionary[arrayInput[i], arrayInput[j]]) + 1) / ((dictionary2[arrayInput[i]]) + V)


    total = 1
    for i in range(len(arrayInput) - 1): # perhitungan perplexity dari smoothing
        j = (i + 1)
        if (arrayInput[i], arrayInput[j]) in dictionary3.keys():
            total = total * (1 / dictionary3[arrayInput[i], arrayInput[j]])

    hasil = total ** (1 /(len(tokenisasiInput)-1))

    return hasil

tempInput = input("Masukan kalimat untuk dihitung perplexity nya  : ").lower()

tokenisasiInput = nltk.word_tokenize(tempInput.lower())

total = 1

smoothing = False

for i in range(len(tokenisasiInput)-1):
    j = (i+1)
    if (tokenisasiInput[i],tokenisasiInput[j]) in dictionary3.keys():
        total = total * (1 / dictionary3[tokenisasiInput[i],tokenisasiInput[j]])
    else :
        print("Melakukan smoothing")
        print("Hasil Perplexity: ",smoothingAddOne(tokenisasiInput, dictionary))
        smoothing = True
        break

if not smoothing:
    print("Hasil Perplexity: ",total**(1/(len(tokenisasiInput)-1)))

#=======================================================================

# mengetahui hasil kemunculan kata bigram

all2Article = open("1301154265_Count_Artikel.txt","w+")

all2Article.write(str(dictionary)+"\n\n")

all2Article.close()

#=======================================================================