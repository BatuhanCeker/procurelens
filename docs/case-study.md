# Vaka çalışması: satın alma teslimat takibi

## Problem ve kullanıcı
Hayali bir işletmede satın alma uzmanı açık siparişleri takip ediyor.
Bir siparişin kısmen teslim alınması, siparişin tamamlandığı anlamına gelmiyor.
Kullanıcının sorusu: “Bugün hangi tedarikçiyi aramalıyım ve ne kadarlık ürün bekliyorum?”

## Çözüm
Sipariş ve mal kabul kayıtlarını ilişkisel tablolarla ayır; kalem bazında teslimatı
topla; kalan miktarı ve tutarı hesapla. Onaylı ve açık kalemleri raporla.
Gecikme günü azalan, ardından açık tutar azalan sıralama ile ilk takibi belirle.
Bu bir iş kuralıdır; yapay zekâ veya teslimat tahmin modeli değildir.

## Örnek sonuç — 5 Ekim 2026 senaryosu
Bu tarih senaryonun rapor tarihidir; gerçek gün veya canlı müşteri verisi değildir.

| Sipariş | Kalan | Açık tutar | Durum | Aksiyon |
|---|---:|---:|---|---|
| PO-001 | 4 klavye | 2.000 TL | 3 gün gecikmiş | Yeni teslim tarihini teyit et |
| PO-003 | 3 monitör | 12.000 TL | Bugün bekleniyor | Depo ve tedarikçiyle teslimatı kontrol et |
| PO-004 | 20 fare | 4.000 TL | Planlı | Planlanan tarihe göre takip et |

Toplam açık tutar 18.000 TL. Taslak PO-002 ve tamamlanmış PO-005 dahil değildir.
Bu tutar fatura borcu veya işletmenin zarar tahmini değildir.

## Veri tasarımı ve dikkat edilen hata
Bir sipariş kalemi iki kez kısmen teslim edildiğinde, doğrudan JOIN ile
sipariş tutarını toplamak aynı tutarı iki kere sayabilir. `risk.sql` teslimatı
önce kalem bazında gruplar, sonra siparişle birleştirir. Çoklu teslimat testi
bu hataya karşı kontrol sağlar.

## Ölçülebilir doğrulama
- Kontrol toplamı: 2.000 + 12.000 + 4.000 = 18.000 TL.
- Termin günü gecikmiş sayılmaz; ertesi gün bir gün gecikme oluşur.
- Sonradan tarihli teslimat rapor tarihindeki bakiyeyi azaltmaz.
- Filtre yalnızca listeyi değiştirir; göstergeler raporun tamamını anlatır.
- Tekrarlanan teslimat, fazla teslimat ve onaysız mal kabulü reddedilir.

Gerçek işletmede zaman veya maliyet tasarrufu ölçülmedi. Performans artışı
yüzdesi veya müşteri kullanımı iddiası yoktur. Kullanıcı kabulü henüz gerçek
kullanıcıyla yapılmadı; örnek kabul senaryoları teknik olarak doğrulandı.

## Sınırlar ve sonraki adımlar
Statik rapor; canlı veritabanına bağlı arayüz değildir. Geçmiş onay durumları
tutulmadığından rapor, geçmişe dönük tam denetim kaydı sunmaz. Sonraki mantıklı
adımlar: onay geçmişi, iade, depo çıkışı ve kullanıcı yetkileri.
