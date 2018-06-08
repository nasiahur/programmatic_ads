# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-12 11:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BrowsingHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column_name', models.IntegerField(choices=[(0, b'Show All'), (1, b'Incident'), (2, b'Host'), (3, b'User Name'), (6, b'Policy'), (7, b'Module'), (8, b'Verdict')], default=0)),
                ('column_value', models.CharField(default=b'', max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=64, unique=True)),
            ],
            options={
                'db_table': 'monitor_categories',
            },
        ),
        migrations.CreateModel(
            name='ContentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=64, unique=True)),
            ],
            options={
                'db_table': 'monitor_contenttype',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iid', models.IntegerField(db_index=True, default=0)),
                ('timestamp', models.DateTimeField()),
                ('date', models.DateField(db_index=True)),
                ('time', models.TimeField(db_index=True)),
                ('hour', models.IntegerField(db_index=True, default=0)),
                ('size', models.IntegerField(db_index=True, default=0)),
                ('size_approx', models.IntegerField(db_index=True, default=0)),
                ('scanflags', models.IntegerField(db_index=True, default=0)),
                ('trusted', models.IntegerField(db_index=True, default=0)),
                ('offensive', models.BooleanField(db_index=True, default=False)),
                ('unproductive', models.BooleanField(db_index=True, default=False)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traffic.ContentType')),
            ],
            options={
                'db_table': 'monitor_event',
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=254, unique=True)),
                ('category1', models.IntegerField()),
                ('category2', models.IntegerField()),
                ('category3', models.IntegerField()),
                ('category4', models.IntegerField()),
                ('category5', models.IntegerField()),
                ('category6', models.IntegerField()),
                ('category7', models.IntegerField()),
                ('category8', models.IntegerField()),
            ],
            options={
                'db_table': 'monitor_host',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254, unique=True)),
                ('enabled', models.BooleanField(default=True)),
                ('email', models.TextField()),
                ('comments', models.TextField()),
                ('schedule_min', models.CharField(default=b'*', max_length=64)),
                ('schedule_hour', models.CharField(default=b'*', max_length=64)),
                ('schedule_dom', models.CharField(default=b'*', max_length=64)),
                ('schedule_month', models.CharField(default=b'*', max_length=64)),
                ('schedule_dow', models.CharField(default=b'*', max_length=64)),
                ('template_type', models.CharField(default=b'*', max_length=255)),
                ('timeframe_type', models.CharField(choices=[(b'last_n_days', b'Last N days'), (b'last_n_weeks', b'Last N weeks'), (b'last_n_months', b'Last N months'), (b'from_to', b'Specific date interval')], default=b'last_n_days', max_length=64)),
                ('timeframe_value', models.IntegerField(default=30)),
                ('timeframe_from', models.DateField(blank=True, null=True)),
                ('timeframe_to', models.DateField(blank=True, null=True)),
                ('include_domains', models.TextField()),
                ('include_users', models.TextField()),
                ('include_policies', models.TextField()),
                ('include_categories', models.TextField()),
                ('exclude_domains', models.TextField()),
                ('exclude_users', models.TextField()),
                ('exclude_policies', models.TextField()),
                ('exclude_categories', models.TextField()),
                ('include_current', models.BooleanField(default=True)),
                ('limit_n_entries', models.IntegerField(default=50)),
                ('limit_n_drilldown', models.IntegerField(default=50)),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=64, unique=True)),
            ],
            options={
                'db_table': 'monitor_level',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=64, unique=True)),
            ],
            options={
                'db_table': 'monitor_member',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=16, unique=True)),
            ],
            options={
                'db_table': 'monitor_message',
            },
        ),
        migrations.CreateModel(
            name='Method',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=64, unique=True)),
            ],
            options={
                'db_table': 'monitor_method',
            },
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=64, unique=True)),
            ],
            options={
                'db_table': 'monitor_module',
            },
        ),
        migrations.CreateModel(
            name='Monitoring',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_interval', models.IntegerField(default=5)),
                ('history_normalize_names', models.BooleanField(default=True)),
                ('history_anonymize_names', models.BooleanField(default=False)),
                ('persistent_enable', models.BooleanField(default=True)),
                ('persistent_purge', models.IntegerField(default=30)),
                ('persistent_store_query', models.BooleanField(default=False)),
                ('persistent_store_path', models.BooleanField(default=False)),
                ('persistent_store_clean', models.BooleanField(default=False)),
                ('persistent_store_adblock', models.BooleanField(default=False)),
                ('persistent_store_privacy', models.BooleanField(default=False)),
                ('persistent_store_adult_heuristics', models.BooleanField(default=True)),
                ('persistent_store_adult_safesearch', models.BooleanField(default=False)),
                ('persistent_store_adult_youtube', models.BooleanField(default=False)),
                ('persistent_store_adult_phrases', models.BooleanField(default=True)),
                ('persistent_store_adult_image', models.BooleanField(default=True)),
                ('persistent_store_categories', models.BooleanField(default=True)),
                ('persistent_store_http_sanitation', models.BooleanField(default=True)),
                ('persistent_store_content_content_type', models.BooleanField(default=True)),
                ('persistent_store_content_charset', models.BooleanField(default=True)),
                ('persistent_store_content_transfer_encoding', models.BooleanField(default=True)),
                ('persistent_store_content_file_name', models.BooleanField(default=True)),
                ('persistent_store_content_file_type', models.BooleanField(default=True)),
                ('persistent_store_content_file_size', models.BooleanField(default=True)),
                ('persistent_store_apps', models.BooleanField(default=False)),
                ('persistent_store_sslbump', models.BooleanField(default=False)),
                ('realtime_enable', models.BooleanField(default=True)),
                ('realtime_store_query', models.BooleanField(default=True)),
                ('realtime_store_path', models.BooleanField(default=True)),
                ('realtime_store_clean', models.BooleanField(default=True)),
                ('realtime_store_adblock', models.BooleanField(default=True)),
                ('realtime_store_privacy', models.BooleanField(default=True)),
                ('realtime_store_adult_heuristics', models.BooleanField(default=True)),
                ('realtime_store_adult_safesearch', models.BooleanField(default=True)),
                ('realtime_store_adult_youtube', models.BooleanField(default=True)),
                ('realtime_store_adult_phrases', models.BooleanField(default=True)),
                ('realtime_store_adult_image', models.BooleanField(default=True)),
                ('realtime_store_categories', models.BooleanField(default=True)),
                ('realtime_store_http_sanitation', models.BooleanField(default=True)),
                ('realtime_store_content_content_type', models.BooleanField(default=True)),
                ('realtime_store_content_charset', models.BooleanField(default=True)),
                ('realtime_store_content_transfer_encoding', models.BooleanField(default=True)),
                ('realtime_store_content_file_name', models.BooleanField(default=True)),
                ('realtime_store_content_file_type', models.BooleanField(default=True)),
                ('realtime_store_content_file_size', models.BooleanField(default=True)),
                ('realtime_store_apps', models.BooleanField(default=True)),
                ('realtime_store_sslbump', models.BooleanField(default=True)),
                ('realtime_limit_record_count', models.IntegerField(default=10000)),
                ('accesslog_enable', models.BooleanField(default=False)),
                ('accesslog_store_query', models.BooleanField(default=False)),
                ('accesslog_store_path', models.BooleanField(default=False)),
                ('accesslog_store_clean', models.BooleanField(default=False)),
                ('accesslog_store_adblock', models.BooleanField(default=False)),
                ('accesslog_store_privacy', models.BooleanField(default=False)),
                ('accesslog_store_adult_heuristics', models.BooleanField(default=True)),
                ('accesslog_store_adult_safesearch', models.BooleanField(default=False)),
                ('accesslog_store_adult_youtube', models.BooleanField(default=False)),
                ('accesslog_store_adult_phrases', models.BooleanField(default=True)),
                ('accesslog_store_adult_image', models.BooleanField(default=True)),
                ('accesslog_store_categories', models.BooleanField(default=True)),
                ('accesslog_store_http_sanitation', models.BooleanField(default=True)),
                ('accesslog_store_content_content_type', models.BooleanField(default=True)),
                ('accesslog_store_content_charset', models.BooleanField(default=True)),
                ('accesslog_store_content_transfer_encoding', models.BooleanField(default=True)),
                ('accesslog_store_content_file_name', models.BooleanField(default=True)),
                ('accesslog_store_content_file_type', models.BooleanField(default=True)),
                ('accesslog_store_content_file_size', models.BooleanField(default=True)),
                ('accesslog_store_apps', models.BooleanField(default=False)),
                ('accesslog_store_sslbump', models.BooleanField(default=False)),
                ('syslog_enable', models.BooleanField(default=False)),
                ('syslog_store_query', models.BooleanField(default=False)),
                ('syslog_store_path', models.BooleanField(default=False)),
                ('syslog_store_clean', models.BooleanField(default=False)),
                ('syslog_store_adblock', models.BooleanField(default=False)),
                ('syslog_store_privacy', models.BooleanField(default=False)),
                ('syslog_store_adult_heuristics', models.BooleanField(default=True)),
                ('syslog_store_adult_safesearch', models.BooleanField(default=False)),
                ('syslog_store_adult_youtube', models.BooleanField(default=False)),
                ('syslog_store_adult_phrases', models.BooleanField(default=True)),
                ('syslog_store_adult_image', models.BooleanField(default=True)),
                ('syslog_store_categories', models.BooleanField(default=True)),
                ('syslog_store_http_sanitation', models.BooleanField(default=True)),
                ('syslog_store_content_content_type', models.BooleanField(default=True)),
                ('syslog_store_content_charset', models.BooleanField(default=True)),
                ('syslog_store_content_transfer_encoding', models.BooleanField(default=True)),
                ('syslog_store_content_file_name', models.BooleanField(default=True)),
                ('syslog_store_content_file_type', models.BooleanField(default=True)),
                ('syslog_store_content_file_size', models.BooleanField(default=True)),
                ('syslog_store_apps', models.BooleanField(default=False)),
                ('syslog_store_sslbump', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Param1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=64, unique=True)),
            ],
            options={
                'db_table': 'monitor_param1',
            },
        ),
        migrations.CreateModel(
            name='Param2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=254, unique=True)),
            ],
            options={
                'db_table': 'monitor_param2',
            },
        ),
        migrations.CreateModel(
            name='Path',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=254, unique=True)),
            ],
            options={
                'db_table': 'monitor_path',
            },
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=64, unique=True)),
            ],
            options={
                'db_table': 'monitor_policy',
            },
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
            ],
            options={
                'db_table': 'monitor_query',
            },
        ),
        migrations.CreateModel(
            name='Reporter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('smtp_username', models.CharField(blank=True, max_length=254)),
                ('smtp_password', models.CharField(blank=True, max_length=254)),
                ('smtp_server', models.CharField(blank=True, max_length=254)),
                ('smtp_port', models.IntegerField(default=587)),
                ('smtp_use_auth', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ScanFlags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=64, unique=True)),
            ],
            options={
                'db_table': 'monitor_scanflags',
            },
        ),
        migrations.CreateModel(
            name='Scheme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=16, unique=True)),
            ],
            options={
                'db_table': 'monitor_scheme',
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=254, unique=True)),
            ],
            options={
                'db_table': 'monitor_server',
            },
        ),
        migrations.CreateModel(
            name='SurfingNow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column_name', models.IntegerField(choices=[(0, b'Show All'), (1, b'Incident'), (2, b'Host'), (3, b'User Name'), (4, b'User IP'), (6, b'Policy'), (7, b'Module'), (8, b'Verdict')], default=0)),
                ('column_value', models.CharField(default=b'', max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Tld',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=254, unique=True)),
            ],
            options={
                'db_table': 'monitor_tld',
            },
        ),
        migrations.CreateModel(
            name='Traffic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='UserAgent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
            ],
            options={
                'db_table': 'monitor_useragent',
            },
        ),
        migrations.CreateModel(
            name='UserEui',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=64, unique=True)),
            ],
            options={
                'db_table': 'monitor_usereui',
            },
        ),
        migrations.CreateModel(
            name='UserIP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=64, unique=True)),
            ],
            options={
                'db_table': 'monitor_userip',
            },
        ),
        migrations.CreateModel(
            name='UserName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=64, unique=True)),
            ],
            options={
                'db_table': 'monitor_username',
            },
        ),
        migrations.CreateModel(
            name='Verdict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=64, unique=True)),
            ],
            options={
                'db_table': 'monitor_verdict',
            },
        ),
        migrations.CreateModel(
            name='WsMgrd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logging', models.IntegerField(choices=[(0, b'debug'), (1, b'info'), (2, b'warning'), (3, b'error')], default=1)),
                ('port', models.IntegerField(default=18888)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traffic.Host'),
        ),
        migrations.AddField(
            model_name='event',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traffic.Level'),
        ),
        migrations.AddField(
            model_name='event',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traffic.Member'),
        ),
        migrations.AddField(
            model_name='event',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traffic.Message'),
        ),
        migrations.AddField(
            model_name='event',
            name='method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traffic.Method'),
        ),
        migrations.AddField(
            model_name='event',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traffic.Module'),
        ),
        migrations.AddField(
            model_name='event',
            name='param1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traffic.Param1'),
        ),
        migrations.AddField(
            model_name='event',
            name='param2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traffic.Param2'),
        ),
        migrations.AddField(
            model_name='event',
            name='path',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traffic.Path'),
        ),
        migrations.AddField(
            model_name='event',
            name='policy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traffic.Policy'),
        ),
        migrations.AddField(
            model_name='event',
            name='query',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traffic.Query'),
        ),
        migrations.AddField(
            model_name='event',
            name='ref_host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ref_host_id', to='traffic.Host'),
        ),
        migrations.AddField(
            model_name='event',
            name='ref_scheme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ref_scheme_id', to='traffic.Scheme'),
        ),
        migrations.AddField(
            model_name='event',
            name='scheme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traffic.Scheme'),
        ),
        migrations.AddField(
            model_name='event',
            name='server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traffic.Server'),
        ),
        migrations.AddField(
            model_name='event',
            name='tld',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traffic.Tld'),
        ),
        migrations.AddField(
            model_name='event',
            name='user_agent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traffic.UserAgent'),
        ),
        migrations.AddField(
            model_name='event',
            name='user_eui',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traffic.UserEui'),
        ),
        migrations.AddField(
            model_name='event',
            name='user_ip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traffic.UserIP'),
        ),
        migrations.AddField(
            model_name='event',
            name='user_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traffic.UserName'),
        ),
        migrations.AddField(
            model_name='event',
            name='verdict',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traffic.Verdict'),
        ),
    ]