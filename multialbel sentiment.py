# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 20:11:30 2019

@author: HP
"""

import xlrd
from nltk.tokenize import RegexpTokenizer
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn import svm
from sklearn.model_selection import cross_val_predict

def load_dataset(FileLoc):
    ulasan = []
    dayatarik = []
    akses = []
    akomodasi = []
    harga = []
    sarana = []
    pelayanan = []
    workbook = xlrd.open_workbook(FileLoc)
    sheet = workbook.sheet_by_index(0)
    count = 0
    for i in range(3,sheet.nrows):
        ulasan.append(str(sheet.cell_value(i,1)))
        dayatarik.append(str(sheet.cell_value(i,2)))
        akses.append(str(sheet.cell_value(i,3)))
        akomodasi.append(str(sheet.cell_value(i,4)))
        harga.append(str(sheet.cell_value(i,5)))
        sarana.append(str(sheet.cell_value(i,6)))
        pelayanan.append(str(sheet.cell_value(i,7)))
        count += 1
        print(count, "data inserted")
    return ulasan,dayatarik,akses,akomodasi,harga,sarana,pelayanan

def preprocess(data):
    cleanData = []
    tokenizer = RegexpTokenizer(r'\w+')
    factory_stopwords = StopWordRemoverFactory()
    stopwords = factory_stopwords.get_stop_words()
    factory_stemmer = StemmerFactory()
    stemmer = factory_stemmer.create_stemmer()
    count = 0
    for i in range(len(data)):
        lowerText = data[i].lower()#Case folding
        tokenizedText = tokenizer.tokenize(lowerText)#Punctual removal and tokenization
        swRemovedText = []#Stopwords removal
        for j in range(len(tokenizedText)):
            if tokenizedText[j] not in stopwords:
                swRemovedText.append(tokenizedText[j])
        stemmedText = []
        for k in range(len(swRemovedText)):#Stemming
            stemmedText.append(stemmer.stem(swRemovedText[k]))
        cleanData.append(stemmedText)
        count += 1
        print(count, "data cleaned")
    return cleanData

def bagi_ulasan(ulasan,label):
    newUlasan = []
    newLabel = []
    for i in range(len(label)):
        if label[i] != '-' and label[i] != '':
            newUlasan.append(ulasan[i])
            newLabel.append(label[i])
    return newUlasan,newLabel

def make_bow(data):
    allWord = []
    for i in range(len(data)):
        for d in (data[i]):
            if d not in allWord:
                allWord.append(d)
    vector = []
    for i in range(len(data)):
        tempVector = []
        for word in allWord:
            valueVector = 0
            for d in data[i]:
                if word == d:
                    valueVector += 1
            tempVector.append(valueVector)
        vector.append(tempVector)
    return vector

def svm_classifier(data,label):
    clf = svm.SVC(kernel='linear')
    result = cross_val_predict(clf,data,label,cv=2)#ini kfold cross validation, ubah angka 2 buat ganti nilai k fold
    result = result.tolist()
    acc = 0
    pos = 0
    neg = 0
    for i in range(len(result)):
        if result[i] == label[i]:
            acc += 1
        if result[i] == '1.0':
            pos += 1
        if result[i] == '-1.0':
            neg += 1
    acc = acc / len(result)
    return acc, pos, neg

ulasan,dayatarik,akses,akomodasi,harga,sarana,pelayanan = load_dataset('datasetpariwisata.xlsx')
cleanData = preprocess(ulasan)

ulasanDt,dayatarik = bagi_ulasan(cleanData,dayatarik)
ulasanAks,akses = bagi_ulasan(cleanData,akses)
ulasanAkm,akomodasi = bagi_ulasan(cleanData,akomodasi)
ulasanHrg,harga = bagi_ulasan(cleanData,harga)
ulasanSrn,sarana = bagi_ulasan(cleanData,sarana)
ulasanPly,pelayanan = bagi_ulasan(cleanData,pelayanan)

vectorDt = make_bow(ulasanDt)
vectorAks = make_bow(ulasanAks)
vectorAkm = make_bow(ulasanAkm)
vectorHrg = make_bow(ulasanHrg)
vectorSrn = make_bow(ulasanSrn)
vectorPly = make_bow(ulasanPly)


accDt,posDt,negDt = svm_classifier(vectorDt,dayatarik)
accAks,posAks,negAks = svm_classifier(vectorAks,akses)
accAkm,posAkm,negAkm = svm_classifier(vectorAkm,akomodasi)
accHrg,posHrg,negHrg = svm_classifier(vectorHrg,harga)
accSrn,posSrn,negSrn = svm_classifier(vectorSrn,sarana)
accPly,posPly,negPly = svm_classifier(vectorPly,pelayanan)

print("Daya tarik:", accDt)
print("Akses:", accAks)
print("Akomodasi:", accAkm)
print("Harga:", accHrg)
print("Sarana:", accSrn)
print("Pelayanan:", accPly)

jum = accDt + accAks + accAkm + accHrg + accSrn + accPly
print("Rata-rata:",jum/6)


#Note: akurasi rata-rata menyusul ya, setelah label akomodasinya gak positif semua































