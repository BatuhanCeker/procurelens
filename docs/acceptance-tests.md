# Kabul senaryoları ve doğrulama

Ortam: Python / SQLite, hayali veriler. Gerçek müşteri kabulü değildir.
Otomatik sonuçlar `python3 -m unittest -v` ile yeniden üretilebilir.

| No | Senaryo | Beklenen sonuç | Gerçekleşen sonuç / kanıt |
|---|---|---|---|
| UAT-01 | 10 klavye siparişinden 6'sını teslim al | Stok 6, kalan 4 | Geçti: test_initial_stock_open_orders_and_totals |
| UAT-02 | Kalan 4 klavyeyi teslim al | Stok 10, sipariş tamamlandı | Geçti: test_partial_then_complete |
| UAT-03 | Kalan 4 yerine 5 teslim al | Hata; yeni belge geri alınır | Geçti: test_overdelivery_rolls_back_receipt |
| UAT-04 | Taslak siparişe teslimat ekle | İşlem reddedilir | Geçti: test_draft_receipt_rejected |
| UAT-05 | Aynı belge referansını tekrar gir | İşlem reddedilir | Geçti: test_duplicate_reference_rejected |
| UAT-06 | 5 Ekim kontrol raporunu çalıştır | 3 açık sipariş, 18.000 TL | Geçti: test_snapshot_values_and_priority |
| UAT-07 | Teslim günü bugün olan siparişi incele | Gecikme 0, bugün bekleniyor | Geçti: test_due_today_is_not_overdue |
| UAT-08 | Aynı kaleme ikinci kısmi teslimatı ekle | Sipariş tutarı çoğalmaz | Geçti: test_multiple_deliveries_do_not_multiply_order_value |
| UAT-09 | Rapor tarihinden sonraki teslimatı ekle | Erken tarihte kalan miktar değişmez | Geçti: test_future_receipt_does_not_reduce_snapshot_balance |
| UAT-10 | HTML raporda Gecikmiş filtresine bas | Yalnızca PO-001 görünür | Tarayıcıda doğrulandı: 1 açık kalem |
| UAT-11 | Tümü filtresine dön | Üç kalem tekrar görünür | Tarayıcıda doğrulandı: 3 açık kalem |

18 otomatik test, yukarıdaki kabul senaryoları ve ilave veri bütünlüğü kontrollerini kapsar.
Ekran görüntüsü: `demo/preview.jpg`.

Yeni tasarım kontrolleri: ürün aramasında klavye tek satır; tutara göre sıralamada PO-003 (12.000 TL) ilk sırada. Tarayıcıda doğrulandı.
