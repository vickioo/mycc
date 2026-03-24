module.exports = {
  apps: [
    {
      name: 'cc2wechat-daemon',
      script: '/home/vicki/air/mycc/.claude/skills/mycc/scripts/node_modules/.bin/tsx',
      args: 'src/index.ts start',
      cwd: '/home/vicki/air/mycc/.claude/skills/mycc/scripts',
      interpreter: 'none',
      watch: false,
      autorestart: true,
      max_restarts: 10,
      restart_delay: 5000,
      min_uptime: '10s',
      env: { NODE_ENV: 'production' },
      error_file: '/home/vicki/air/mycc/.claude/skills/mycc/scripts/pm2-error.log',
      out_file: '/home/vicki/air/mycc/.claude/skills/mycc/scripts/pm2-out.log',
      time: true,
    },
    {
      name: 'cc-keepalive',
      script: '/usr/bin/python3',
      args: '/home/vicki/air/mycc/.claude/skills/mycc/scripts/src/tasks/cc-keepalive.py start',
      cwd: '/home/vicki/air/mycc/.claude/skills/mycc/scripts/src/tasks',
      interpreter: 'none',
      watch: false,
      autorestart: false,   // 守护进程有自己内置的重启逻辑
      max_restarts: 3,
      env: { NODE_ENV: 'production' },
      error_file: '/tmp/cc-keepalive.log',
      out_file: '/tmp/cc-keepalive.log',
      time: true,
    },
  ],
};
