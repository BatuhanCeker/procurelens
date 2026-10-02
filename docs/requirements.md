# Satın alma ve stok: ihtiyaç analizi

Bu çalışma hayali bir işletmenin kişisel eğitim projesidir; gerçek müşteri verisi içermez.

## İhtiyaç
Satın alma ekibi siparişleri, depo ekibi gelen ürünleri takip etmek istiyor.
Kısmi teslimatlar kaybolmamalı ve yanlışlıkla siparişten fazla ürün kabul edilmemeli.

## Kapsam ve kabul kriterleri
1. Tedarikçi ve ürün ana verileri tanımlanabilir.
2. Pozitif miktar ve birim fiyatla, en az bir kalem içeren taslak sipariş oluşturulur.
3. Taslak onaylanmadan mal kabulü yapılamaz.
4. Sipariş kalemi kısmen veya tamamen teslim alınabilir; sipariş miktarı aşılamaz.
5. Her mal kabulü tek işlem içinde teslimat başlığı ve kalemlerini oluşturur. Kalemler aynı zamanda stok giriş hareketleridir; hata olursa işlem geri alınır.
6. Aynı teslimat referansıyla tekrar kayıt açılması engellenir.
7. Sipariş durumu TASLAK → ONAYLI → KISMI_TESLIM → TAMAMLANDI şeklinde ilerler.
8. Stok ve açık sipariş raporları gerçek kayıtlardan SQL ile üretilir.
9. Teslim tarihi sipariş tarihinden önce olamaz; geçersiz takvim tarihleri reddedilir.
10. Teslim tarihi rapor tarihinden önce olan açık ve onaylı kalemler gecikmiştir.
    Termin günü gelen kalemler ayrı bir 'bugün bekleniyor' grubundadır.
11. Açık tutar, kalan miktar × birim fiyattır. Aynı kaleme birden fazla teslimat
    yapılması rapor tutarlarını çoğaltmaz.
12. Takip önceliği: önce gecikme günü azalan, sonra açık tutar azalan.
    Liste filtrelenebilir, sonuç CSV olarak aktarılabilir.

## Bilinçli sınırlar
Yalnızca tam adetli ürünler ve TRY kullanılır. Fiyatlar tam kuruş olarak saklanır.
Başlangıç stoğu sıfırdır. Stok çıkışı, iade, fatura, ödeme, vergi, çoklu depo,
yetkilendirme ve eşzamanlı çok kullanıcılı sunucu bu sürüme dahil değildir.
Onay, bir iş akışı adımıdır; kullanıcı kimliği doğrulanmaz.

## Gerçek müşteriye sorulacak sorular
- Siparişleri kim, hangi tutar sınırına kadar onaylıyor?
- Kısmi veya fazla teslimata izin var mı?
- Teslimat numarası hangi kapsamda benzersiz?
- Adet dışında kg/metre gibi birimler var mı?
- Hasarlı ürün veya iade stoğu nasıl etkiliyor?

Bu örnekte fazla teslimat yasaktır; teslimat referansı sipariş başına benzersizdir.
