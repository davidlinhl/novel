# novel

supervisord conf
```
[program:novel]
directory=/root/py/novel
command=python3 main.py
user=root
autostart=true
autorestart=true
redirect_stderr=true
stderr_logfile=/root/py/log/novel_err.log
stdout_logfile=/root/py/log/novel_out.log
```
