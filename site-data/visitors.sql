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


-- Feedback form: visitors can send, nobody can read from the page. Read it in Supabase: Table Editor -> feedback.
create table if not exists public.feedback (
  id bigint generated always as identity primary key,
  page text not null default 'iust-landscape',
  message text not null check (char_length(btrim(message)) between 1 and 2000),
  email text check (email is null or (char_length(email) <= 254 and email ~* '^[^@\s]+@[^@\s]+\.[^@\s]+$')),
  created_at timestamptz not null default now()
);
alter table public.feedback enable row level security;
create policy "send feedback" on public.feedback for insert to anon with check (page = 'iust-landscape');
grant insert (page, message, email) on public.feedback to anon;

-- At most 20 messages a minute in total, to stop floods. Runs as owner because visitors cannot read the table.
create or replace function public.feedback_throttle() returns trigger language plpgsql security definer set search_path = public as $$
begin
  if (select count(*) from feedback where created_at > now() - interval '1 minute') >= 20 then
    raise exception 'Too many messages, try again in a minute';
  end if;
  return new;
end $$;
revoke all on function public.feedback_throttle() from public;
create trigger feedback_throttle before insert on public.feedback for each row execute function public.feedback_throttle();

-- Visit log: one row per page view, with no IP address and no identifier. Read it in Supabase: Table Editor -> visit_log.
create table if not exists public.visit_log (
  id bigint generated always as identity primary key,
  page text not null default 'iust-landscape',
  at timestamptz not null default now(),
  referrer text check (char_length(referrer) <= 200),
  browser text check (char_length(browser) <= 30),
  os text check (char_length(os) <= 30),
  device text check (char_length(device) <= 20),
  screen text check (char_length(screen) <= 20),
  lang text check (char_length(lang) <= 20),
  tz text check (char_length(tz) <= 60)
);
alter table public.visit_log enable row level security;
create policy "log visit" on public.visit_log for insert to anon with check (page = 'iust-landscape');
grant insert (page, referrer, browser, os, device, screen, lang, tz) on public.visit_log to anon;

create or replace function public.visit_log_throttle() returns trigger language plpgsql security definer set search_path = public as $$
begin
  if (select count(*) from visit_log where at > now() - interval '1 minute') >= 300 then
    raise exception 'Too many visits logged this minute';
  end if;
  return new;
end $$;
revoke all on function public.visit_log_throttle() from public;
drop trigger if exists visit_log_throttle on public.visit_log;
create trigger visit_log_throttle before insert on public.visit_log for each row execute function public.visit_log_throttle();

-- Keep the log for 12 months, as the privacy notice says.
create extension if not exists pg_cron;
select cron.schedule('trim-visit-log', '0 3 * * *', $$delete from public.visit_log where at < now() - interval '12 months'$$);
