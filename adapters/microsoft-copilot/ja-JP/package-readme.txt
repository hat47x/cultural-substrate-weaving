cultural-substrate-weaving — Microsoft 365限定プロファイル

このパッケージは、Microsoft 365 Copilotの現行仕様に合わせた限定プロファイルです。

■ instructions.txt
Microsoft 365 CopilotのInstructionsへ設定する、自己完結した実行指示です。
このファイルに書かれた範囲だけを、エージェントの実行規則として扱います。

■ method-reference/
CSW全体の方法論を人間が確認するための参照資料です。情報を失わず保持するために同梱しています。
Agent BuilderやSharePointのKnowledgeへアップロードし、instructions.txtの続きを実行させるためのファイルではありません。

■ Microsoft 365 CopilotのKnowledge
利用者が分析対象とする業務資料、調査資料、組織内文書などを、事実のグラウンディングに使う場所です。
パッケージ内のmethod-reference/とは役割が異なります。

現在のMicrosoft 365版は、他の対応プラットフォームと同等の完全なCSW実行を保証しません。詳細な体系固有操作、Taihekiの特例、完全な長期研究プロトコルなど、instructions.txtに含まれない手順は、この限定プロファイルでは実行範囲外です。

利用方法と最新の制約:
https://github.com/hat47x/cultural-substrate-weaving/blob/main/docs/ja/platforms/microsoft-copilot.md

Microsoft 365向けアダプター再設計の追跡:
https://github.com/hat47x/cultural-substrate-weaving/issues/96
