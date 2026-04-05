-- pgvector 拡張を有効化
create extension if not exists vector
with
  schema extensions;

-- FAQ ドキュメント用テーブル
create table if not exists documents (
  id bigserial primary key,
  content text,
  metadata jsonb,
  embedding extensions.vector(768)
);

-- 類似度検索関数
create or replace function match_documents (
  query_embedding extensions.vector(768),
  match_count int default null,
  filter jsonb default '{}'
) returns table (
  id bigint,
  content text,
  metadata jsonb,
  similarity float
)
language plpgsql
as $$
#variable_conflict use_column
begin
  return query
  select
    id,
    content,
    metadata,
    1 - (documents.embedding <=> query_embedding) as similarity
  from documents
  where metadata @> filter
  order by documents.embedding <=> query_embedding
  limit match_count;
end;
$$;

-- RLS（行レベルセキュリティ）
alter table documents enable row level security;

create policy "Allow anon select on documents"
  on documents
  for select
  to anon
  with check (true);

create policy "Allow service_role full access on documents"
  on documents
  for all
  to service_role
  using (true)
  with check (true);
