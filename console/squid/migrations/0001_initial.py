# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-12 11:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AclDefault',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allowed_src', models.TextField(blank=True)),
                ('denied_src', models.TextField(blank=True)),
                ('additional_sslports', models.CharField(blank=True, max_length=254)),
                ('additional_safeports', models.CharField(blank=True, max_length=254)),
                ('advanced_acl', models.TextField(blank=True)),
                ('advanced_access', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Administrative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cache_mgr', models.CharField(blank=True, default=b'webmaster', max_length=200)),
                ('httpd_suppress_version_string', models.BooleanField(default=False)),
                ('visible_hostname', models.CharField(blank=True, default=b'proxy.example.lan', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='AuthAd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('realm', models.CharField(max_length=254)),
                ('dc1addr', models.CharField(max_length=254)),
                ('dc2addr', models.CharField(blank=True, max_length=254)),
                ('base_dn', models.CharField(max_length=254)),
                ('bind_user', models.CharField(max_length=254)),
                ('bind_pass', models.CharField(max_length=254)),
                ('lookup_mode', models.IntegerField(choices=[(389, b'LDAP over port 389 (default)'), (636, b'LDAPS over port 636 (encrypted)'), (3268, b'Global Catalog LDAP over port 3268 (multi-domain)'), (3269, b'Global Catalog LDAPS over port 3269 (multi-domain, encrypted)')], default=389)),
                ('cachetime', models.IntegerField(default=300)),
                ('timeout', models.IntegerField(default=10)),
                ('ldap_enable', models.BooleanField(default=False)),
                ('ldap_title', models.CharField(default=b'Squid Proxy', max_length=254)),
                ('ldap_credsttl', models.IntegerField(default=5)),
                ('ldap_helper_verbose', models.BooleanField(default=False)),
                ('ldap_helper_total', models.IntegerField(default=20)),
                ('ldap_helper_idle', models.IntegerField(default=10)),
                ('ldap_helper_startup', models.IntegerField(default=5)),
                ('ntlm_enable', models.BooleanField(default=False)),
                ('ntlm_helper_verbose', models.BooleanField(default=False)),
                ('ntlm_helper_total', models.IntegerField(default=20)),
                ('ntlm_helper_idle', models.IntegerField(default=10)),
                ('ntlm_helper_startup', models.IntegerField(default=5)),
                ('krb5_enable', models.BooleanField(default=False)),
                ('krb5_spn', models.CharField(max_length=254)),
                ('krb5_use_gssnoname', models.BooleanField(default=False)),
                ('krb5_no_replay_cache', models.BooleanField(default=False)),
                ('krb5_helper_verbose', models.BooleanField(default=False)),
                ('krb5_helper_total', models.IntegerField(default=70)),
                ('krb5_helper_idle', models.IntegerField(default=25)),
                ('krb5_helper_startup', models.IntegerField(default=10)),
            ],
        ),
        migrations.CreateModel(
            name='AuthLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enable', models.BooleanField(default=False)),
                ('resolve_ip_as_user_name', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='AuthLabelUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=254, unique=True)),
                ('user_ip', models.CharField(blank=True, max_length=254)),
                ('user_mac', models.CharField(blank=True, max_length=254)),
                ('comment', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='AuthLocalDb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enable', models.BooleanField(default=False)),
                ('title', models.CharField(default=b'Squid Proxy', max_length=254)),
                ('helper_verbose', models.BooleanField(default=False)),
                ('helper_total', models.IntegerField(default=20)),
                ('helper_idle', models.IntegerField(default=10)),
                ('helper_startup', models.IntegerField(default=5)),
            ],
        ),
        migrations.CreateModel(
            name='AuthPseudoAd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enable', models.BooleanField(default=False)),
                ('server1', models.CharField(max_length=254)),
                ('port1', models.IntegerField(default=8443)),
                ('server2', models.CharField(blank=True, max_length=254)),
                ('port2', models.IntegerField(default=8443)),
                ('token', models.CharField(blank=True, max_length=254)),
                ('positive_ttl', models.IntegerField(default=600)),
                ('negative_ttl', models.IntegerField(default=300)),
                ('helper_verbose', models.BooleanField(default=False)),
                ('helper_total', models.IntegerField(default=20)),
                ('helper_idle', models.IntegerField(default=10)),
                ('helper_startup', models.IntegerField(default=5)),
            ],
        ),
        migrations.CreateModel(
            name='AuthRadius',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enable', models.BooleanField(default=False)),
                ('server', models.CharField(max_length=254)),
                ('secret', models.CharField(max_length=254)),
                ('title', models.CharField(default=b'Squid Proxy', max_length=254)),
                ('helper_verbose', models.BooleanField(default=False)),
                ('helper_total', models.IntegerField(default=20)),
                ('helper_idle', models.IntegerField(default=10)),
                ('helper_startup', models.IntegerField(default=5)),
            ],
        ),
        migrations.CreateModel(
            name='BumpMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(choices=[(0, b'Only selected HTTPS domains'), (1, b'All HTTPS domains, except specified')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='DiskCache',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enabled', models.BooleanField(default=False)),
                ('cache_replacement_policy', models.CharField(choices=[(b'lru', b'lru'), (b'heap GDSF', b'heap GDSF'), (b'heap LFUDA', b'heap LFUDA'), (b'heap LRU', b'heap LRU')], default=b'lru', max_length=32)),
                ('minimum_object_size', models.IntegerField(default=0)),
                ('maximum_object_size', models.IntegerField(default=4096)),
                ('cache_type', models.CharField(choices=[(b'ufs', b'ufs')], default=b'ufs', max_length=32)),
                ('ufs_mb', models.IntegerField(default=100)),
                ('ufs_l1', models.IntegerField(default=16)),
                ('ufs_l2', models.IntegerField(default=256)),
            ],
        ),
        migrations.CreateModel(
            name='Dns',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dns_timeout', models.IntegerField(default=30)),
                ('dns_nameservers', models.CharField(blank=True, default=b'', max_length=200)),
                ('dns_v4_first', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExcludeAdvanced',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_sslbump', models.TextField(blank=True)),
                ('value_adaptation', models.TextField(blank=True)),
                ('value_auth', models.TextField(blank=True)),
                ('value_cache', models.TextField(blank=True)),
                ('value_urlrewrite', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExcludeCategories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exclude_adult_themes_sexuality', models.BooleanField(default=False)),
                ('exclude_advertising', models.BooleanField(default=False)),
                ('exclude_alcohol_tobacco', models.BooleanField(default=False)),
                ('exclude_anime_manga_webcomic', models.BooleanField(default=False)),
                ('exclude_arts_society_culture', models.BooleanField(default=False)),
                ('exclude_automotive', models.BooleanField(default=False)),
                ('exclude_banking_insurance_finance', models.BooleanField(default=True)),
                ('exclude_blogs_personal', models.BooleanField(default=False)),
                ('exclude_business_services_industry', models.BooleanField(default=False)),
                ('exclude_classifieds_auctions', models.BooleanField(default=False)),
                ('exclude_content_delivery_networks', models.BooleanField(default=False)),
                ('exclude_cracks_hacking_illegal', models.BooleanField(default=False)),
                ('exclude_dating', models.BooleanField(default=False)),
                ('exclude_drugs', models.BooleanField(default=False)),
                ('exclude_ecommerce_shopping', models.BooleanField(default=False)),
                ('exclude_education_science_research', models.BooleanField(default=False)),
                ('exclude_entertainment_humor_hobby', models.BooleanField(default=False)),
                ('exclude_expired_parked', models.BooleanField(default=False)),
                ('exclude_fashion_beauty_cosmetics', models.BooleanField(default=False)),
                ('exclude_file_storage', models.BooleanField(default=False)),
                ('exclude_food_dining_restaurants', models.BooleanField(default=False)),
                ('exclude_forums_message_boards', models.BooleanField(default=False)),
                ('exclude_gambling', models.BooleanField(default=False)),
                ('exclude_games', models.BooleanField(default=False)),
                ('exclude_generic_non_categorized', models.BooleanField(default=False)),
                ('exclude_government', models.BooleanField(default=True)),
                ('exclude_hate_discrimination_violence', models.BooleanField(default=False)),
                ('exclude_health_medicine_fitness', models.BooleanField(default=True)),
                ('exclude_jobs_employment_career', models.BooleanField(default=False)),
                ('exclude_messaging_chat', models.BooleanField(default=False)),
                ('exclude_movies', models.BooleanField(default=False)),
                ('exclude_music_radio', models.BooleanField(default=False)),
                ('exclude_network_infrastructure', models.BooleanField(default=True)),
                ('exclude_news_media', models.BooleanField(default=False)),
                ('exclude_nudity_pornography', models.BooleanField(default=False)),
                ('exclude_p2p_file_sharing', models.BooleanField(default=False)),
                ('exclude_photo_sharing', models.BooleanField(default=False)),
                ('exclude_politics', models.BooleanField(default=False)),
                ('exclude_portals', models.BooleanField(default=False)),
                ('exclude_proxy_anonymizer', models.BooleanField(default=False)),
                ('exclude_real_estate_home_interior', models.BooleanField(default=False)),
                ('exclude_religious', models.BooleanField(default=False)),
                ('exclude_search_engines', models.BooleanField(default=False)),
                ('exclude_social_networking', models.BooleanField(default=False)),
                ('exclude_software_technology_hardware', models.BooleanField(default=False)),
                ('exclude_sports', models.BooleanField(default=False)),
                ('exclude_television', models.BooleanField(default=False)),
                ('exclude_travel', models.BooleanField(default=False)),
                ('exclude_user_tracking', models.BooleanField(default=False)),
                ('exclude_video_sharing', models.BooleanField(default=False)),
                ('exclude_weapons', models.BooleanField(default=False)),
                ('exclude_webmail', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ExcludeContentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=254, unique=True)),
                ('comment', models.TextField(blank=True)),
                ('bypass_adaptation', models.BooleanField(default=True)),
                ('bypass_cache', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['value'],
            },
        ),
        migrations.CreateModel(
            name='ExcludeDomainIp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=254, unique=True)),
                ('comment', models.TextField(blank=True)),
                ('bypass_adaptation', models.BooleanField(default=True)),
                ('bypass_sslbump', models.BooleanField(default=True)),
                ('bypass_auth', models.BooleanField(default=True)),
                ('bypass_cache', models.BooleanField(default=True)),
                ('bypass_urlrewrite', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['value'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExcludeDomainName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=254, unique=True)),
                ('comment', models.TextField(blank=True)),
                ('bypass_adaptation', models.BooleanField(default=True)),
                ('bypass_sslbump', models.BooleanField(default=True)),
                ('bypass_auth', models.BooleanField(default=True)),
                ('bypass_cache', models.BooleanField(default=True)),
                ('bypass_urlrewrite', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['value'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExcludeDomainRange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=254, unique=True)),
                ('comment', models.TextField(blank=True)),
                ('bypass_adaptation', models.BooleanField(default=True)),
                ('bypass_sslbump', models.BooleanField(default=True)),
                ('bypass_auth', models.BooleanField(default=True)),
                ('bypass_cache', models.BooleanField(default=True)),
                ('bypass_urlrewrite', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['value'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExcludeDomainSubnet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=254, unique=True)),
                ('comment', models.TextField(blank=True)),
                ('bypass_adaptation', models.BooleanField(default=True)),
                ('bypass_sslbump', models.BooleanField(default=True)),
                ('bypass_auth', models.BooleanField(default=True)),
                ('bypass_cache', models.BooleanField(default=True)),
                ('bypass_urlrewrite', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['value'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExcludeSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=254, unique=True)),
                ('comment', models.TextField(blank=True)),
                ('bypass_adaptation', models.BooleanField(default=True)),
                ('bypass_sslbump', models.BooleanField(default=True)),
                ('bypass_auth', models.BooleanField(default=True)),
                ('bypass_cache', models.BooleanField(default=True)),
                ('bypass_urlrewrite', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['value'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExcludeUserAgent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=254, unique=True)),
                ('comment', models.TextField(blank=True)),
                ('bypass_adaptation', models.BooleanField(default=True)),
                ('bypass_sslbump', models.BooleanField(default=True)),
                ('bypass_auth', models.BooleanField(default=True)),
                ('bypass_cache', models.BooleanField(default=True)),
                ('bypass_urlrewrite', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['value'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExcludeUserIp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=254, unique=True)),
                ('comment', models.TextField(blank=True)),
                ('bypass_adaptation', models.BooleanField(default=True)),
                ('bypass_sslbump', models.BooleanField(default=True)),
                ('bypass_auth', models.BooleanField(default=True)),
                ('bypass_cache', models.BooleanField(default=True)),
                ('bypass_urlrewrite', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['value'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExcludeUserName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=254, unique=True)),
                ('comment', models.TextField(blank=True)),
                ('bypass_adaptation', models.BooleanField(default=True)),
                ('bypass_sslbump', models.BooleanField(default=True)),
                ('bypass_auth', models.BooleanField(default=True)),
                ('bypass_cache', models.BooleanField(default=True)),
                ('bypass_urlrewrite', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['value'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExcludeUserRange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=254, unique=True)),
                ('comment', models.TextField(blank=True)),
                ('bypass_adaptation', models.BooleanField(default=True)),
                ('bypass_sslbump', models.BooleanField(default=True)),
                ('bypass_auth', models.BooleanField(default=True)),
                ('bypass_cache', models.BooleanField(default=True)),
                ('bypass_urlrewrite', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['value'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExcludeUserSubnet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=254, unique=True)),
                ('comment', models.TextField(blank=True)),
                ('bypass_adaptation', models.BooleanField(default=True)),
                ('bypass_sslbump', models.BooleanField(default=True)),
                ('bypass_auth', models.BooleanField(default=True)),
                ('bypass_cache', models.BooleanField(default=True)),
                ('bypass_urlrewrite', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['value'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LogSection',
            fields=[
                ('section_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=200)),
                ('comment', models.CharField(blank=True, default=b'', max_length=200)),
                ('level', models.IntegerField(choices=[(0, b'Fatal'), (1, b'Errors'), (2, b'Warnings'), (3, b'Informational'), (6, b'Debug'), (9, b'Debug (Verbose)')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='MemoryCache',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cache_mem', models.IntegerField(default=256)),
                ('maximum_object_size_in_memory', models.IntegerField(default=512)),
                ('memory_replacement_policy', models.CharField(choices=[(b'lru', b'lru'), (b'heap GDSF', b'heap GDSF'), (b'heap LFUDA', b'heap LFUDA'), (b'heap LRU', b'heap LRU')], default=b'lru', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Miscellaneous',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forwarded_for', models.IntegerField(choices=[(0, b'off'), (1, b'on (default)'), (2, b'transparent'), (3, b'truncate'), (4, b'delete')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('explicit_address', models.CharField(blank=True, default=b'', max_length=200)),
                ('explicit_port', models.IntegerField(default=3128)),
                ('enable_proxy_proto', models.BooleanField(default=False)),
                ('proxy_hosts', models.CharField(blank=True, default=b'', max_length=200)),
                ('intercept_mode', models.IntegerField(choices=[(0, b'Not Configured / Disabled'), (1, b'Cisco WCCP Redirect'), (2, b'Default Gateway Proxy')], default=0)),
                ('intercept_address', models.CharField(blank=True, default=b'', max_length=200)),
                ('intercept_port_http', models.IntegerField(default=3126)),
                ('intercept_port_https', models.IntegerField(default=3127)),
                ('wccp2_router', models.CharField(blank=True, default=b'', max_length=200)),
                ('wccp2_password', models.CharField(blank=True, default=b'', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='RefreshPattern',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insensitive', models.BooleanField(default=True)),
                ('regex', models.TextField()),
                ('min_time', models.IntegerField(default=0)),
                ('percent', models.IntegerField(default=20)),
                ('max_time', models.IntegerField(default=0)),
                ('override_expire', models.BooleanField(default=False)),
                ('override_lastmod', models.BooleanField(default=False)),
                ('reload_into_ims', models.BooleanField(default=False)),
                ('ignore_reload', models.BooleanField(default=False)),
                ('ignore_no_store', models.BooleanField(default=False)),
                ('ignore_must_revalidate', models.BooleanField(default=False)),
                ('ignore_private', models.BooleanField(default=False)),
                ('ignore_auth', models.BooleanField(default=False)),
                ('max_stale', models.BooleanField(default=False)),
                ('max_stale_nn', models.IntegerField(default=0)),
                ('refresh_ims', models.BooleanField(default=False)),
                ('store_stale', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['regex'],
            },
        ),
        migrations.CreateModel(
            name='SslErrorDomain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=254, unique=True)),
                ('comment', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['value'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SslErrorIp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=254, unique=True)),
                ('comment', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['value'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SslErrorSubnet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=254, unique=True)),
                ('comment', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['value'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SslIntermediateCert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_num', models.CharField(max_length=254)),
                ('subject_keyid', models.CharField(max_length=254, unique=True)),
                ('subject', models.CharField(max_length=254)),
                ('common_name', models.CharField(max_length=254)),
                ('alt_names', models.CharField(max_length=254)),
                ('valid_from', models.CharField(max_length=254)),
                ('valid_until', models.CharField(max_length=254)),
                ('issuer', models.CharField(max_length=254)),
                ('pem', models.TextField()),
            ],
            options={
                'ordering': ['subject'],
            },
        ),
        migrations.CreateModel(
            name='SslTargetDomain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=254, unique=True)),
                ('comment', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['value'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SslTargetIp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=254, unique=True)),
                ('comment', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['value'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SslTargetSubnet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=254, unique=True)),
                ('comment', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['value'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TroubleShooting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loglevel_section_all', models.IntegerField(choices=[(0, b'Fatal'), (1, b'Errors'), (2, b'Warnings'), (3, b'Informational'), (6, b'Debug'), (9, b'Debug (Verbose)')], default=1)),
            ],
        ),
    ]
