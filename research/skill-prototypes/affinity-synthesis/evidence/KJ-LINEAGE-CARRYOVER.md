# KJ lineage carry-over from monolithic CSW

Status: migration evidence inventory
Date: 2026-09-06

## Purpose

現行 `src/ja-JP/methods/integration.md` をthin connectionへ置換するとき、KJ法の系譜・参照文献・商標注意がCSWから消えるだけにならないよう、Layer 1側へ移管対象として保存する。

このファイルは2026-09-06時点の**現行CSW canonicalに既に記載されている情報のcarry-over inventory**である。公開promotion前には一次資料・公式情報で再確認する。

## Legacy source inventory

現行CSWは、KJ法系統について次を主参照としている。

- 川喜田二郎『KJ法：渾沌をして語らしめる』中央公論社、1986年。
- 川喜田二郎『発想法：創造性開発のために』中公新書136、1967年。
- 川喜田二郎『続・発想法：KJ法の展開と応用』中公新書210、1970年。

現行CSWは、第三者が読める札、分類名ではない表札、A型図解とB型文章化の区別を重視してきた。

また、現行文書では、一般に流通している簡略な紹介だけを記憶から補うと原型から離れるおそれがあるため、判断に迷う場合は原典・関連技術へ戻る方針を置いている。

## Trademark carry-over note

現行CSW canonicalは、KJ法が株式会社川喜田研究所の登録商標であることと、商標登録第4867036号という記載を含んでいる。

この情報はLayer 1公開時の名称・説明・disclaimer設計に関係するため、CSW thin化の際に削除して終わりにしない。

公開promotion前に、権利者の公式情報または公的商標情報で現行状態を再確認する。

## Relationship to current Layer-1 dossier

`evidence/dossier.md` は既に、

- KJ法
- 親和図法
- 質的統合法
- 04理論
- 核融合法
- 外部Agent Skillから採用／不採用としたmechanism

を分離して記録している。

本carry-overは、monolithic CSWにしか残っていないlegacy source detailをLayer 1側で見失わないための補助inventoryである。

## Promotion action

Layer 1を公開候補へ昇格するときは、少なくとも次を行う。

1. 上記書誌を一次資料または信頼できる書誌情報で再確認する。
2. KJ法の商標状態・表記を公式／公的情報で再確認する。
3. `affinity-synthesis` が公式KJ法実装や完全再現ではないことを維持する。
4. 系譜由来の技法と、生成AI向けに追加した補正を混同しない。
5. 再確認後、必要な情報だけを `evidence/dossier.md` または公開documentationへ統合する。
