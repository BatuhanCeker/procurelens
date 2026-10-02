# Birlikte öğrenme planı

Kutular başlangıçta boş: kodun çalışması, konunun öğrenildiği anlamına gelmez.

## Ders 1 — Tablo ve ilişki
- [ ] suppliers, products ve purchase_orders tablolarını kendi cümlelerinle açıkla.
- [ ] Sipariş başlığı ile sipariş kaleminin neden ayrı olduğunu anlat.
- [ ] Primary key ve foreign key için projeden birer örnek göster.

İlk soru: Bir siparişte üç farklı ürün varsa purchase_orders ve order_lines
tablolarına kaçar kayıt yazılır? Neden?

## Ders 2 — SELECT ve WHERE
- [ ] Tüm ürünlerin sku ve name alanlarını listele.
- [ ] Yalnızca 2 numaralı tedarikçinin siparişlerini getir.
- [ ] 5 adetten fazla sipariş edilen kalemleri getir.

Örnek:
```sql
SELECT name FROM products WHERE id = 1;
```

SELECT görmek istediğin sütunu, FROM tabloyu, WHERE koşulu belirtir.
Bu sorgu ürünün adını döndürür; stoğunu söylemez.

## Ders 3 — JOIN ve raporlar
- [ ] Siparişin yanında tedarikçi adını getir.
- [ ] INNER JOIN ile LEFT JOIN farkını örnek vererek açıkla.
- [ ] SUM, GROUP BY ve HAVING kullanarak 5.000 TL üzerindeki siparişleri bul.
- [ ] Neden teslimat satırlarını doğrudan sipariş tutarı raporuna bağlamak
      kısmi teslimatlar arttıkça tutarı yanlış çoğaltabilir, açıkla.

## Ders 4 — Süreç ve test
- [ ] 4 klavyelik ikinci teslimatı ekle; stok ve durum değişimini doğrula.
- [ ] 5 klavye eklemeyi dene; engellenmesini ve geri almayı açıkla.
- [ ] Onaysız sipariş için mal kabulünün neden reddedildiğini anlat.
- [ ] Beklenen sonuç / gerçek sonuç içeren bir test kaydı yaz.

## Ders 5 — Kendi katkın
- [ ] Yeni bir hayali tedarikçi ve ürün ekle.
- [ ] O tedarikçiye yeni sipariş oluştur ve kısmi teslim al.
- [ ] Kendi SQL raporunu ekle ve beklenen sonucu hesaplayarak doğrula.
- [ ] Yaptığın değişikliği GitHub commit açıklamasında özetle.

## Ders 6 — ProcureLens raporu
- [ ] 18.000 TL açık tutarın hangi üç kalemden geldiğini hesapla.
- [ ] 2.000 TL gecikmiş tutarın neden toplam sipariş tutarı olmadığını anlat.
- [ ] Rapor tarihini 8 Ekim'e al ve PO-003'ün neden geciktiğini açıkla.
- [ ] `risk.sql` içindeki teslimat gruplamasının JOIN çoğalmasını nasıl engellediğini anlat.
- [ ] Ekrandaki takip önerisinin bir sıralama kuralı olduğunu, AI modeli olmadığını açıkla.

## Görüşmede hazır sayılma ölçütü
Üç temel sorguyu açıklayarak yazabilmek, kısmi teslimatı gösterebilmek ve
projenin sınırlarını dürüstçe anlatabilmek. Trigger ezberlemek gerekli değil.

## Cevap kontrolü (önce kendin dene)
İlk soru: bir sipariş başlığı, üç sipariş kalemi.
İkinci teslimat sonrası klavye stoğu 10, açık kalem yok, sipariş TAMAMLANDI.
