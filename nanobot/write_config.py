import json

config = {
  "agents": {
    "defaults": {
      "workspace": "./workspace",
      "model": "coder-model",
      "provider": "custom",
      "maxTokens": 8192,
      "contextWindowTokens": 65536,
      "temperature": 0.1,
      "maxToolIterations": 40,
      "reasoningEffort": None,
      "timezone": "UTC"
    }
  },
  "channels": {
    "sendProgress": True,
    "sendToolHints": False,
    "sendMaxRetries": 3,
    "dingtalk": {
      "enabled": False,
      "clientId": "",
      "clientSecret": "",
      "allowFrom": []
    },
    "discord": {
      "enabled": False,
      "token": "",
      "allowFrom": [],
      "gatewayUrl": "wss://gateway.discord.gg/?v=10&encoding=json",
      "intents": 37377,
      "groupPolicy": "mention"
    },
    "email": {
      "enabled": False,
      "consentGranted": False,
      "imapHost": "",
      "imapPort": 993,
      "imapUsername": "",
      "imapPassword": "",
      "imapMailbox": "INBOX",
      "imapUseSsl": True,
      "smtpHost": "",
      "smtpPort": 587,
      "smtpUsername": "",
      "smtpPassword": "",
      "smtpUseTls": True,
      "smtpUseSsl": False,
      "fromAddress": "",
      "autoReplyEnabled": True,
      "pollIntervalSeconds": 30,
      "markSeen": True,
      "maxBodyChars": 12000,
      "subjectPrefix": "Re: ",
      "allowFrom": []
    },
    "feishu": {
      "enabled": False,
      "appId": "",
      "appSecret": "",
      "encryptKey": "",
      "verificationToken": "",
      "allowFrom": [],
      "reactEmoji": "THUMBSUP",
      "groupPolicy": "mention",
      "replyToMessage": False
    },
    "mochat": {
      "enabled": False,
      "baseUrl": "https://mochat.io",
      "socketUrl": "",
      "socketPath": "/socket.io",
      "socketDisableMsgpack": False,
      "socketReconnectDelayMs": 1000,
      "socketMaxReconnectDelayMs": 10000,
      "socketConnectTimeoutMs": 10000,
      "refreshIntervalMs": 30000,
      "watchTimeoutMs": 25000,
      "watchLimit": 100,
      "retryDelayMs": 500,
      "maxRetryAttempts": 0,
      "clawToken": "",
      "agentUserId": "",
      "sessions": [],
      "panels": [],
      "allowFrom": [],
      "mention": {
        "requireInGroups": False
      },
      "groups": {},
      "replyDelayMode": "non-mention",
      "replyDelayMs": 120000
    },
    "qq": {
      "enabled": False,
      "appId": "",
      "secret": "",
      "allowFrom": [],
      "msgFormat": "plain",
      "mediaDir": "",
      "downloadChunkSize": 262144,
      "downloadMaxBytes": 209715200
    },
    "slack": {
      "enabled": False,
      "mode": "socket",
      "webhookPath": "/slack/events",
      "botToken": "",
      "appToken": "",
      "userTokenReadOnly": True,
      "replyInThread": True,
      "reactEmoji": "eyes",
      "doneEmoji": "white_check_mark",
      "allowFrom": [],
      "groupPolicy": "mention",
      "groupAllowFrom": [],
      "dm": {
        "enabled": True,
        "policy": "open",
        "allowFrom": []
      }
    },
    "telegram": {
      "enabled": False,
      "token": "",
      "allowFrom": [],
      "proxy": None,
      "replyToMessage": False,
      "reactEmoji": "👀",
      "groupPolicy": "mention",
      "connectionPoolSize": 32,
      "poolTimeout": 5.0,
      "streaming": True
    },
    "wecom": {
      "enabled": False,
      "botId": "",
      "secret": "",
      "allowFrom": [],
      "welcomeMessage": ""
    },
    "weixin": {
      "enabled": False,
      "allowFrom": [],
      "baseUrl": "https://ilinkai.weixin.qq.com",
      "cdnBaseUrl": "https://novac2c.cdn.weixin.qq.com/c2c",
      "routeTag": None,
      "token": "",
      "stateDir": "",
      "pollTimeout": 35
    },
    "whatsapp": {
      "enabled": False,
      "bridgeUrl": "ws://localhost:3001",
      "bridgeToken": "",
      "allowFrom": [],
      "groupPolicy": "open"
    }
  },
  "providers": {
    "custom": {
      "apiKey": "lab7-secret-key",
      "apiBase": "http://localhost:42005/v1",
      "extraHeaders": None
    },
    "azureOpenai": {
      "apiKey": "",
      "apiBase": None,
      "extraHeaders": None
    },
    "anthropic": {
      "apiKey": "",
      "apiBase": None,
      "extraHeaders": None
    },
    "openai": {
      "apiKey": "",
      "apiBase": None,
      "extraHeaders": None
    },
    "openrouter": {
      "apiKey": "",
      "apiBase": None,
      "extraHeaders": None
    },
    "deepseek": {
      "apiKey": "",
      "apiBase": None,
      "extraHeaders": None
    },
    "groq": {
      "apiKey": "",
      "apiBase": None,
      "extraHeaders": None
    },
    "zhipu": {
      "apiKey": "",
      "apiBase": None,
      "extraHeaders": None
    },
    "dashscope": {
      "apiKey": "",
      "apiBase": None,
      "extraHeaders": None
    },
    "vllm": {
      "apiKey": "",
      "apiBase": None,
      "extraHeaders": None
    },
    "ollama": {
      "apiKey": "",
      "apiBase": None,
      "extraHeaders": None
    },
    "ovms": {
      "apiKey": "",
      "apiBase": None,
      "extraHeaders": None
    },
    "gemini": {
      "apiKey": "",
      "apiBase": None,
      "extraHeaders": None
    },
    "moonshot": {
      "apiKey": "",
      "apiBase": None,
      "extraHeaders": None
    },
    "minimax": {
      "apiKey": "",
      "apiBase": None,
      "extraHeaders": None
    },
    "mistral": {
      "apiKey": "",
      "apiBase": None,
      "extraHeaders": None
    },
    "stepfun": {
      "apiKey": "",
      "apiBase": None,
      "extraHeaders": None
    },
    "aihubmix": {
      "apiKey": "",
      "apiBase": None,
      "extraHeaders": None
    },
    "siliconflow": {
      "apiKey": "",
      "apiBase": None,
      "extraHeaders": None
    },
    "volcengine": {
      "apiKey": "",
      "apiBase": None,
      "extraHeaders": None
    },
    "volcengineCodingPlan": {
      "apiKey": "",
      "apiBase": None,
      "extraHeaders": None
    },
    "byteplus": {
      "apiKey": "",
      "apiBase": None,
      "extraHeaders": None
    },
    "byteplusCodingPlan": {
      "apiKey": "",
      "apiBase": None,
      "extraHeaders": None
    }
  },
  "gateway": {
    "host": "0.0.0.0",
    "port": 18790,
    "heartbeat": {
      "enabled": True,
      "intervalS": 1800,
      "keepRecentMessages": 8
    }
  },
  "tools": {
    "web": {
      "proxy": None,
      "search": {
        "provider": "brave",
        "apiKey": "",
        "baseUrl": "",
        "maxResults": 5
      }
    },
    "exec": {
      "enable": True,
      "timeout": 60,
      "pathAppend": ""
    },
    "restrictToWorkspace": False,
    "mcpServers": {
      "lms": {
        "command": "python",
        "args": ["-m", "mcp_lms"],
        "env": {
          "NANOBOT_LMS_BACKEND_URL": "http://localhost:42002",
          "NANOBOT_LMS_API_KEY": "lab7-secret-key"
        }
      }
    }
  }
}

with open('config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
print('Config written successfully')
