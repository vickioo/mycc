module.exports = {
  apps: [
    {
      name: 'cc-clash-tunnel',
      script: '/root/cc-clash-tunnel.sh',
      args: 'start',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '100M',
      exec_mode: 'fork',
      kill_timeout: 3000,
      wait_ready: false,
      listen_timeout: 5000,
      merge_logs: true,
      restart_delay: 3000
    },
    {
      name: 'cc-clash-watchdog',
      script: '/root/cc-clash-watchdog.sh',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '50M',
      merge_logs: true,
      kill_timeout: 3000,
      restart_delay: 5000
    }
  ]
};
