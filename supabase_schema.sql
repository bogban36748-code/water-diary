-- Дневник воды: схема для SQL Editor в Supabase
create table if not exists public.water_log (
    id          bigint generated always as identity primary key,
    amount      integer not null check (amount > 0 and amount <= 5000), -- мл
    date        date    not null default current_date,
    created_at  timestamptz not null default now()
);

create index if not exists water_log_date_idx on public.water_log (date);

-- Включаем RLS: без политик anon-ключ не увидит ни одной строки
alter table public.water_log enable row level security;

-- Учебные политики для анонимного ключа (приложение без авторизации).
-- ВНИМАНИЕ: в реальном проекте с пользователями политики делают по auth.uid().
create policy "anon read"   on public.water_log for select to anon using (true);
create policy "anon insert" on public.water_log for insert to anon with check (true);
create policy "anon update" on public.water_log for update to anon using (true) with check (true);
create policy "anon delete" on public.water_log for delete to anon using (true);
