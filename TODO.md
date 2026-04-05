# Hello AI! Q&Aボット TODO

## 現状まとめ

- UI: Streamlit でスマホ向けに構築済み（濃紺テーマ、ヒーローカード、CTA ボタン等）
- RAG: Gemini 2.0 Flash + Supabase pgvector で FAQ 検索・回答
- 質問ログ: Supabase (PostgreSQL) に保存 + Gemini でカテゴリ自動分類
- イベント導線: コンペ・新歓・LINE・Instagram・X のリンク設置済み
- テーマ: `.streamlit/config.toml` でライトモード強制済み
- デプロイ: Streamlit Community Cloud で公開済み

## 完了済み

- [x] Streamlit + LangChain + Gemini で RAG チャットボットを構築
- [x] FAQ データ（faq_data.txt）にサークル情報・イベント・SNS を追加
- [x] スマホ前提の UI（ヒーローカード、サンプル質問、CTA ボタン）
- [x] 濃紺 `#003059` ベースのブランドカラー適用
- [x] 入力欄の赤枠を解消（影ベースに変更）
- [x] ダークモードでの表示崩れを `.streamlit/config.toml` で解決
- [x] イベント情報（コンペ・渋谷新歓・駒場対面）をフロント + FAQ に追加
- [x] LINE / Instagram / X の実 URL をフロントに設置
- [x] Supabase で質問ログ基盤を構築（テーブル定義 + RLS ポリシー）
- [x] Gemini によるカテゴリ自動分類（入会/イベント/活動内容/技術/運営/その他）
- [x] LLM 応答失敗時の例外ハンドリング
- [x] API キー未設定時のエラー表示
- [x] Supabase で質問ログ保存の実装
- [x] Streamlit Community Cloud にデプロイ・公開
- [x] InMemoryVectorStore → Supabase pgvector に移行
- [x] `reindex.py`（FAQ 再インデックススクリプト）を作成

## 最優先

- [x] Supabase に質問ログが正しく溜まっているか本番で確認する
- [x] `.env.example` を作成して、公開用の安全な環境変数テンプレートにする
- [x] `README.md` を最新の構成・デプロイ情報に合わせて書き直す

## 改善ループ（質問ログ活用）

- [ ] Supabase ダッシュボードでカテゴリ別の質問傾向を確認する運用を始める
- [ ] `is_in_faq = false` の質問を週次でレビューし、FAQ に追加する運用ルールを決める
- [ ] Streamlit マルチページで運営向け管理ダッシュボードを作る
  - カテゴリ別集計グラフ
  - FAQ 未対応の質問一覧
  - 日別の質問数推移
- [ ] 質問ログが数百件を超えたら、類似質問クラスタリング（Chroma 等）を導入する

## コード品質・保守性

- [x] `app.py` をファイル分割（`config.py` / `chain.py` / `db.py` / `ui.py`）
- [x] `README.md` を最新の構成に合わせて書き直す
- [x] FAQ データの更新手順を文書化する（`docs/faq_update_guide.md`）
- [x] `pytest` を導入してコア処理のテストを書く（15テスト）
- [x] 回答精度チューニング（`chunk_size=600` / `overlap=100` / `k=4` / プロンプト改善）

## 永続ベクトルストア（pgvector 移行済み）

- [x] Supabase pgvector に移行（`SupabaseVectorStore`）
- [x] DB を Supabase に一本化（質問ログ + ベクトル検索）
- [x] FAQ 更新時の再インデックススクリプト（`reindex.py`）を作成
- [x] `supabase_pgvector_setup.sql` を作成（テーブル + 検索関数 + RLS）

## 運用・安定化

- [ ] `requirements.txt` のバージョンをより固定寄りにする
- [ ] Streamlit Community Cloud の Secrets に環境変数が正しく設定されているか確認する
- [ ] Gemini API の無料枠上限を把握し、レート制限を検討する
- [ ] Supabase のログ量・テーブルサイズの監視ルールを決める
- [ ] 将来的に運営のみアクセスの管理ページには認証を入れる

## あると良い改善

- [ ] 回答に参照した FAQ チャンクの抜粋を表示する
- [ ] チャット履歴のクリアボタンを追加する
- [ ] FAQ データを `.txt` 以外（`.md` / `.csv`）でも読めるようにする
- [ ] 管理画面から FAQ を追加・編集できるようにする
- [ ] ユーザーが「役に立った / 立たなかった」をフィードバックできるようにする
