# novel
This project aims to provide a online novel reader service. Users can login and upload their novels or just documents, the site will keep track of the reading process and together with Baidu APP's TTS service, the content can be read to the user. 

Implemented with python tornado.


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
