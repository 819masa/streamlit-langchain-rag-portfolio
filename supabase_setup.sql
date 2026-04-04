-- Supabase の SQL Editor で実行してください
-- Dashboard > SQL Editor > New query > 以下を貼り付けて Run

create table if not exists question_logs (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  question text not null,
  answer text not null,
  category text not null default 'その他',
  is_in_faq boolean not null default true
);

-- anon key でアプリから INSERT できるようにする
alter table question_logs enable row level security;

create policy "Allow anon insert"
  on question_logs
  for insert
  to anon
  with check (true);

create policy "Allow anon select"
  on question_logs
  for select
  to anon
  using (true);

-- カテゴリ別集計用のインデックス
create index if not exists idx_question_logs_category on question_logs (category);
create index if not exists idx_question_logs_created_at on question_logs (created_at);
