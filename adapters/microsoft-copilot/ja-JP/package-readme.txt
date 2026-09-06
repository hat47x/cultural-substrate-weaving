cultural-substrate-weaving — Microsoft 365限定プロファイル

このパッケージは、Microsoft 365 Copilotの現行仕様に合わせた自己完結型のcomposite adapterです。

■ instructions.txt
Microsoft 365 CopilotのInstructionsへ設定する実行指示です。
CSWの文化体系探索・帰属保持・対象へのreturnに加え、独立Skillを呼べない環境でも最低限の材料統合を安全に行えるよう、親和統合コアの最小互換手順を埋め込んでいます。
これはCSW本体が材料統合アルゴリズムを所有するという意味ではなく、`affinity-synthesis`の完全実装やKJ法の公式実装を称するものでもありません。
また、完全な`iterative-inquiry-synthesis`の複数round管理を実装したとは扱いません。

■ method-reference/
CSW runtimeと関連する方法資料を、人間が確認するための参照です。分離Methodの研究内容を理解する補助資料を含む場合があります。
Agent BuilderやSharePointのKnowledgeへアップロードし、instructions.txtの続きを実行させるためのファイルではありません。

■ Microsoft 365 CopilotのKnowledge
利用者が分析対象とする業務資料、調査資料、組織内文書などを、対象側の事実グラウンディングに使う場所です。
パッケージ内のmethod-reference/とは役割が異なります。

現在のMicrosoft 365版は、他の対応プラットフォームと同等の完全なCSW／分離Method実行を保証しません。詳細な体系固有操作、Taihekiの特例、高度な長期研究設計、完全な親和統合representation／lineage、完全な複数round governanceなど、instructions.txtに含まれない手順は実行範囲外です。

利用方法と最新の制約:
https://github.com/hat47x/cultural-substrate-weaving/blob/main/docs/ja/platforms/microsoft-copilot.md

Microsoft 365向けアダプター再設計の追跡:
https://github.com/hat47x/cultural-substrate-weaving/issues/96
