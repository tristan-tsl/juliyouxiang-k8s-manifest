rm -rf /data/tristan/monitoring/grafana
mkdir -p /data/tristan/monitoring/grafana
chmod 777 /data/tristan/monitoring/grafana

docker cp a27abcd28349:/usr/share/grafana/conf/defaults.ini defaults.ini
cd /data/tristan/monitoring

访问: http://grafana.juliyouxiang.com

登录: admin/admin


导入模板

```
Grafana UI / Dashboards / Import`

- `Grafana.net Dashboard`: `8919`
- `Load`
- `Prometheus`: `prometheus`
- `Save & Open`
```