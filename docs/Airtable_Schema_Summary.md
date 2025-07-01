# Airtable Database Schema Summary

_Last updated: 2025-07-01T22:17:03.527052Z_

---

## Table: 圃場データ (ID: tblwDA8dIHpDgYwgs)

### Fields:
- **圃場ID**: multilineText
- **エリア**: singleSelect
- **圃場名**: multilineText
- **面積(ha)**: number
- **作付詳細**: multipleRecordLinks
- **メモ**: singleLineText
- **肥料管理**: singleLineText
- **大豆作付計画**: singleLineText
- **大豆播種管理**: singleLineText
- **大豆播種管理 2**: singleLineText
- **作り方**: singleLineText

---

## Table: 作物マスター (ID: tblfhulTQGvSs6AyE)

### Fields:
- **作物名**: singleLineText
- **分類**: singleSelect
- **作付計画**: multipleRecordLinks
- **Crop Task Template**: multipleRecordLinks

---

## Table: 作付計画 (ID: tblvgn2sxSJUg9hyo)

### Fields:
- **ID**: singleLineText
- **播種回次**: number
- **作物マスター**: multipleRecordLinks
- **品種名**: singleSelect
- **播種予定日**: date
- **播種実施日**: date
- **播種量/枚数**: number
- **プラウ**: date
- **ディスクハロー**: date
- **石灰**: date
- **微量肥料**: date
- **パワーハロー**: date
- **畝立て**: date
- **定植予定日**: date
- **定植実施日**: date
- **定植予定日2**: date
- **定植実施日2**: date
- **定植本数**: singleLineText
- **圃場データ**: multipleRecordLinks
- **圃場名 (from 圃場データ)**: multipleLookupValues
- **面積(ha) (from 圃場データ)**: multipleLookupValues
- **作つけ面積 (ha)**: number
- **元肥計画 (肥料名 kg/10a)**: multilineText
- **カルチ 予定日**: date
- **カルチ 実施日**: date
- **除草**: date
- **防除1**: date
- **防除2**: date
- **防除3**: date
- **防除4**: date
- **防除5**: date
- **収穫予定**: date
- **資材使用量**: multilineText
- **作業タスク管理**: singleLineText
- **作業タスク**: singleLineText
- **作業タスク 2**: singleLineText
- **作業タスク 3**: multipleRecordLinks

---

## Table: Crop Task Template (ID: tblG2Scjxaes508SK)

### Fields:
- **タスク名**: singleLineText
- **作物マスター**: multipleRecordLinks
- **基準日**: singleSelect
- **オフセット(日)**: number

---

## Table: 作業タスク (ID: tbl9wyQyCmEayaAkB)

### Fields:
- **タスク名**: singleLineText
- **関連する作付計画**: multipleRecordLinks
- **圃場名 (from 圃場データ) (from 関連する作付計画)**: multipleLookupValues
- **ステータス**: singleSelect
- **予定日**: date
- **実施日**: date
- **使用資材**: multipleRecordLinks
- **資材名 (from 使用資材)**: multipleLookupValues
- **メモ**: aiText

---

## Table: 資材マスター (ID: tblWoWsK0V0b2gc3a)

### Fields:
- **資材名**: singleLineText
- **資材分類**: singleSelect
- **メーカー**: singleLineText
- **規格・容量**: singleLineText
- **単価**: currency
- **主成分**: singleLineText
- **適用作物**: singleLineText
- **施用方法**: singleLineText
- **保管場所**: singleLineText
- **メモ**: multilineText
- **作業タスク**: multipleRecordLinks

---

## Table: 資材使用ログ (ID: tblvQB3MM4Jr7f5oK)

### Fields:
- **使用日**: date
- **資材名**: singleLineText
- **圃場名**: singleLineText
- **作物名**: singleLineText
- **使用量**: number
- **単位**: singleLineText
- **単価**: currency
- **使用金額**: number
- **作業者**: singleLineText
- **作業内容**: singleLineText
- **メモ**: multilineText

---

## Table: 作業者マスター (ID: tbl5J09ZSM5y8YZf9)

### Fields:
- **作業者名**: singleLineText
- **役割**: singleSelect
- **所属**: singleLineText
- **電話番号**: phoneNumber
- **メール**: email
- **資格・免許**: singleLineText
- **メモ**: multilineText

---

## Table: ナレッジベース (ID: tblYgwLKYh7XlK08z)

### Fields:
- **タイトル**: singleLineText
- **カテゴリ**: singleSelect
- **詳細**: multilineText
- **登録日**: date
- **添付**: multipleAttachments

---

## Table: 収穫ログ (ID: tblU8EUlRGyNK9blV)

### Fields:
- **収穫日**: date
- **作物名**: singleLineText
- **圃場名**: singleLineText
- **サイズ**: singleSelect
- **収穫量(個)**: number
- **単価(円/個)**: currency
- **売上**: number
- **メモ**: multilineText

---
