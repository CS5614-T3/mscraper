-- mastodon server info 
create table mastodon_server (
    server_id        bigserial primary key,
    domain           varchar(255) not null unique,   -- e.g. mastodon.social
    base_url         varchar(300) not null,          -- e.g. https://mastodon.social
    is_active        boolean not null default true,
    created_at       timestamptz not null default now(),
    updated_at       timestamptz not null default now()
);


-- mastodon oauth app info
create table oauth_app (
    app_id            bigserial primary key,
    server_id         bigint not null references mastodon_server(server_id),
    app_name          varchar(200) not null,
    client_id         text not null,
    client_secret     text not null,
    redirect_uri      text,
    scopes            varchar(500) not null,
    is_active         boolean not null default true,
    created_at        timestamptz not null default now(),
    updated_at        timestamptz not null default now(),

    constraint uq_oauth_app unique (server_id, app_name)
);


-- access_token manage (app token/user token : type classified)
create table access_token (
    token_id              bigserial primary key,
    app_id                bigint not null references oauth_app(app_id),
    token_type            varchar(20) not null check (token_type in ('app', 'user')),
    access_token          text not null unique,
    scope                 varchar(500) not null,
    mastodon_account_id   varchar(100),   -- if it is an user_token: account_id
    issued_at             timestamptz not null default now(),
    expires_at            timestamptz,
    revoked_at            timestamptz,
    is_active             boolean not null default true,
    created_at            timestamptz not null default now(),

    constraint ck_user_token_account
        check (
            (token_type = 'app' and mastodon_account_id is null)
            or
            (token_type = 'user' and mastodon_account_id is not null)
        )
);


-- token management resource
create table token_runtime (
    token_id            bigint primary key references access_token(token_id),
    last_called_at      timestamptz,
    last_success_at     timestamptz,
    last_status_code    integer,
    fail_count          integer not null default 0,
    notes               text,
    updated_at          timestamptz not null default now()
);