import random
from timeit import default_timer as timer

def randomrestart(): # 8 vezirin satranç tahtasındaki konumlarını rastgele belirleyip döndüren fonksiyon
    konumlar = []    # Her sütuna 1 en fazla 1 vezir gelecek şekilde kodlandı.
    for i in range(8):
        a = random.randint(1, 8)
        konumlar.append(a)
    return konumlar

def skorhesaplama(konumlar): # Satranç tahtası üzerindeki vezirlerin toplam kesişme sayısını döndüren fonksiyon
    skor = 0
    caprazlar = 0
    duzler = 0
    kesisenler = []
    for i in range(len(konumlar)):
        for j in range(len(konumlar)):
            if i == j:
                continue
            if konumlar[i] == konumlar[j]:
                duzler += 1
                continue
            if (konumlar[i]-konumlar[j])/(i-j) == 1 or (konumlar[i]-konumlar[j])/(i-j) == -1:
                konum = []
                caprazlar += 1
                konum.append(konumlar[i])
                konum.append(konumlar[j])
                konum.append(i)
                konum.append(j)
                kesisenler.append(konum)
    skor = int((caprazlar + duzler) / 2)
    return skor

def eniyiSkoruYap(konumX): # Mevcut konumdan 1 vezirin yerini değiştirerek kesişme sayısının en aza ineceği konumu
                           # ve bu hareketten sonraki kesişme sayısını döndüren fonksiyon
    eniyiskor = skorhesaplama(konumX)
    k1 = konumX[0]
    k2 = konumX[1]
    k3 = konumX[2]
    k4 = konumX[3]
    k5 = konumX[4]
    k6 = konumX[5]
    k7 = konumX[6]
    k8 = konumX[7]

    degisecekKordinat = [0, 1]  #Sütun ve satır (0-7, 1-8 olacak şekilde)
    konumNew = konumX

    eniyiKonum = []
    eniyiKonum.append(k1)
    eniyiKonum.append(k2)
    eniyiKonum.append(k3)
    eniyiKonum.append(k4)
    eniyiKonum.append(k5)
    eniyiKonum.append(k6)
    eniyiKonum.append(k7)
    eniyiKonum.append(k8)

    for i in range(8):
        for j in range(8):
            konumNew[i] = j+1
            if skorhesaplama(konumNew) < eniyiskor:
                eniyiskor = skorhesaplama(konumNew)
                degisecekKordinat[0] = i
                degisecekKordinat[1] = j+1
        konumNew[i] = eniyiKonum[i]

    eniyiKonum[degisecekKordinat[0]] = degisecekKordinat[1]
    return eniyiKonum, eniyiskor  #Bir vezirin yerini değiştirerek elde edilebilecek en iyi konumu döndürür.

cozulenProblem = 0

randomrestartSayilari = []
veziryerdegistirmeSayilari = []
gecenSureler = []

while cozulenProblem < 25:
    konum = randomrestart()
    skor = skorhesaplama(konum)
    print("Başlangıç Konumu = ", konum)
    print("Kesişme sayısı = ", skor)

    randomrestartSayisi = 0
    toplamVezirYerDegistirme = 0

    start = timer()
    while True:
        if eniyiSkoruYap(konum)[1] < skor: # Daha iyi bir kesişme skoru var ise vezirleri o konuma getiriyor.
            konum = eniyiSkoruYap(konum)[0]
            skor = skorhesaplama(konum)
            toplamVezirYerDegistirme += 1
            print("Bir sonraki en iyi konum = ", konum)
            print("Kesişme sayısı = ", skor)
            print("Vezir Yer Değiştirme = ", toplamVezirYerDegistirme)

        else:
            if skor == 0:  # Kesişme sayısı 0 'a ulaşır ise içerideki while'i bitirerek en başa dönüyor.
                cozulenProblem += 1
                end = timer()
                gecensure = (end - start)
                gecenSureler.append(gecensure)
                break
            else: # Kesişme sayısı 0'a ulaşmadıysa randomrestart ile rastgele bir konum elde edip işlemlere bu konumdan devam ediyor.
                konum = randomrestart()
                skor = skorhesaplama(konum)
                randomrestartSayisi += 1
                print("Random Restart Atıldı!")
                continue

    randomrestartSayilari.append(randomrestartSayisi)
    veziryerdegistirmeSayilari.append(toplamVezirYerDegistirme)
    print("Çözülen Problem = ", cozulenProblem)
    print("-----------------------------------")


# 25 çözüm için bazı değerler ile oluşturulan tablo
print("    Yer Değiştirme Sayısı    Random Restart Sayısı     İşlem Süreleri")
print("    ---------------------    ---------------------     ---------------")
for i in range(25):
    if i < 9:
        print(i+1, "-", "       ", veziryerdegistirmeSayilari[i],
              " "*(23 - len(str(veziryerdegistirmeSayilari[i]))), randomrestartSayilari[i],
              " "*(19 - len(str(randomrestartSayilari[i]))), format(gecenSureler[i], ".4f"))
    else:
        print(i + 1, "-", "      ", veziryerdegistirmeSayilari[i],
              " " * (23 - len(str(veziryerdegistirmeSayilari[i]))), randomrestartSayilari[i],
              " " * (19 - len(str(randomrestartSayilari[i]))), format(gecenSureler[i], ".4f"))

print("Ortalama =  ", end="")
print(format(sum(veziryerdegistirmeSayilari)/25, ".1f"), end="")
print(" "*(25-len(format(sum(veziryerdegistirmeSayilari)/25, ".1f"))), end="")
print(format(sum(randomrestartSayilari)/25, ".1f"), end="")
print(" "*(21-len(format(sum(randomrestartSayilari)/25, ".1f"))), end="")
print(format(sum(gecenSureler)/25, ".4f"))
