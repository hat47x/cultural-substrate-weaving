# Framework corpus eighteenth wave — 2026-10-05

Status: candidate-quality expansion / no runtime adoption

## Decision

古代ギリシア・ローマ系の記憶術として伝わる method of loci / loci and imagines を、profile-readyの研究候補として追加する。

今回取り込むのは「記憶力を高める秘訣」ではない。CSWで検討する構造核は、**安定した順序付きの場所（index）と、そこへ結び付ける可変内容を分け、同じ順序を再走査して欠落や入れ替わりを局所化する**ことである。

*Rhetorica ad Herennium* Book III は、背景・場所を比較的持続する足場、imageをそこへ配置する可変要素として記述し、場所の順序と識別可能性を重視する。Quintilianも *Institutio Oratoria* XI.2 で、区別しやすい場所を順に固定し、sign/imageを割り当て、同じ経路をたどって内容を取り出す方法を説明している。同時に、連続した文章の逐語的記憶などには負荷が大きいという限界も述べている。

## Why this fills a real corpus gap

現行portfolioには、情報の保持や経路に関わる候補が複数ある。

- Vedic recitation pathas は、同じ言語列を異なる規則的recitationで再表現し、境界や順序の保持を検査する。
- Inka khipu は、物理的なattachment hierarchy、位置、複数channelを持つ記録構造として扱う。
- Marshallese wave navigation は、固定したglobal mapよりも、実環境のcueやdisturbanceへ戻りながらrouteを更新する。
- mandala系は、空間的位置そのものに体系固有の役割や意味がある。

method of loci が追加する候補操作はこれらと異なり、**意味を持つtarget構造とは別に、再利用できる安定したindexを置き、現在の内容だけをそこへrebindingする**ことである。

この区別は、長い移行計画、運用手順、review packetなどで「どこまで確認したか」「どの位置で内容が抜けたか」を局所化する探索に使える可能性がある。

## Strong counter-hypothesis

一方、この候補には強い反証可能性がある。

de-binding後に残るものが、

1. 番号を振る。
2. 順に見る。
3. 空欄を見つける。

だけなら、普通のnumbered checklistで十分である。

その場合、method of lociをruntimeへ持ち込む理由はない。文化体系を使ったという事実や、古い技法であるという事実を付加価値へ変換しない。

したがって今回のprofile-ready化は「有効と判定した」という意味ではなく、**普通のchecklistと公平に比較できるほど構造核・出典・停止条件が明確になった**という意味である。

## Historical boundary

- *Rhetorica ad Herennium* は匿名作品であり、現在の著者帰属としてCicero名義に戻さない。
- Simonidesの逸話は古代修辞学における起源物語として扱い、一人の発明者を歴史事実として確定しない。
- 古代ローマの修辞的記憶術、中世・ルネサンスのars memoriae、現代の"memory palace"を一つの不変手順へ畳まない。
- place/imageによって思い出せた内容が正しいとは限らない。target-side evidenceは別途必要である。
- 空間上の近接をtarget側の意味的・因果的近接へ変換しない。

## Target-return value

worked exampleでは、長文のmigration planを12個のstable checkpointへ一時的にbindし、restore rehearsalとpost-rollback verificationの空白を局所化する。

ただし最終成果物に必要なのはL4/L12という記憶術上のラベルではなく、

- restore rehearsalのEvidenceが本当に存在するか。
- rollback後の健全性を何で確認するか。

というtarget-side質問である。

negative exampleでは、順序を持たないinterview断片へL1/L2/...を与えると、人工的な順序と隣接関係を作るためnon-activationとする。

## Runtime decision

runtimeへは採用しない。

次に比較すべきもの:

- ordinary numbered checklist / outline;
- Vedic recitation pathas;
- Inka khipu record structure;
- Marshallese wave navigation.

特にordinary checklistに対して、追加のtarget-supportedな問い、欠落局所化、再binding上の差が残らない場合は、候補をruntime queueから外す。

広範なefficacy benchmarkはまだ開始しない。
