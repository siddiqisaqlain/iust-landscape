-- Visitor counter for the IUST landscape page. Run once in Supabase: SQL Editor -> New query -> Run.
create table if not exists public.site_counters (id text primary key, n bigint not null default 0);
insert into public.site_counters (id) values ('iust-landscape') on conflict do nothing;
-- No policies: the table is closed to the public; visitors can only go through count_visit.
alter table public.site_counters enable row level security;

create or replace function public.count_visit(page text, bump boolean default true)
returns bigint language sql security definer set search_path = public as $$
  update site_counters set n = n + case when bump then 1 else 0 end where id = page returning n;
$$;
revoke all on function public.count_visit(text, boolean) from public;
grant execute on function public.count_visit(text, boolean) to anon;

-- Visitor chat: anyone can read and post; nobody can edit or delete from the page (moderate in the Supabase table editor).
create table if not exists public.chat_messages (
  id bigint generated always as identity primary key,
  page text not null default 'iust-landscape',
  name text not null check (char_length(btrim(name)) between 1 and 40),
  body text not null check (char_length(btrim(body)) between 1 and 500),
  created_at timestamptz not null default now()
);
alter table public.chat_messages enable row level security;
create policy "read chat" on public.chat_messages for select to anon using (true);
create policy "post chat" on public.chat_messages for insert to anon with check (page = 'iust-landscape');
grant select on public.chat_messages to anon;
grant insert (page, name, body) on public.chat_messages to anon;

-- At most 30 messages a minute across the page, to stop floods.
create or replace function public.chat_throttle() returns trigger language plpgsql set search_path = public as $$
begin
  if (select count(*) from chat_messages where created_at > now() - interval '1 minute') >= 30 then
    raise exception 'Chat is busy, try again in a minute';
  end if;
  return new;
end $$;
drop trigger if exists chat_throttle on public.chat_messages;
create trigger chat_throttle before insert on public.chat_messages for each row execute function public.chat_throttle();

alter publication supabase_realtime add table public.chat_messages;
