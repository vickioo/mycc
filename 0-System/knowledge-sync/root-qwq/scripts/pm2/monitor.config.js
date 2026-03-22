module.exports = {
  apps: [
    {
      name: '5min-report',
      script: '/root/air/qwq/scripts/5min-report.sh',
      args: 'daemon',
      interpreter: 'bash',
      restart_delay: 5000,
      max_restarts: 5,
      min_uptime: '30s',
      error_file: '/tmp/pm2-5min-report.err.log',
      out_file: '/tmp/pm2-5min-report.out.log',
      log_file: '/tmp/pm2-5min-report.log',
      time: true,
      env: {
        NOTIFICATION_MODE: 'dingtalk'
      }
    },
    {
      name: 'continuous-monitor',
      script: '/root/air/qwq/scripts/continuous-monitor.sh',
      interpreter: 'bash',
      restart_delay: 5000,
      max_restarts: 5,
      min_uptime: '30s',
      error_file: '/tmp/pm2-continuous-monitor.err.log',
      out_file: '/tmp/pm2-continuous-monitor.out.log',
      log_file: '/tmp/pm2-continuous-monitor.log',
      time: true
    }
  ]
};
