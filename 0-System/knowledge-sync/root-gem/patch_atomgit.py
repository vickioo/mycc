import os
import re

# 1. Patch config/settings.py
settings_path = '/root/free-claude-code/config/settings.py'
with open(settings_path, 'r') as f:
    settings_code = f.read()

if 'atomgit_api_key' not in settings_code:
    settings_code = settings_code.replace(
        'silicon_flow_api_key: str | None = Field(default=None, env="SILICONFLOW_API_KEY")',
        'silicon_flow_api_key: str | None = Field(default=None, env="SILICONFLOW_API_KEY")\n    atomgit_api_key: str | None = Field(default=None, env="ATOMGIT_API_KEY")'
    )
    with open(settings_path, 'w') as f:
        f.write(settings_code)

# 2. Create providers/atomgit
os.makedirs('/root/free-claude-code/providers/atomgit', exist_ok=True)
with open('/root/free-claude-code/providers/atomgit/__init__.py', 'w') as f:
    f.write('from .client import AtomGitProvider, ATOMGIT_BASE_URL\n__all__ = ["AtomGitProvider", "ATOMGIT_BASE_URL"]\n')

with open('/root/free-claude-code/providers/atomgit/client.py', 'w') as f:
    f.write('''from providers.base import ProviderConfig
from providers.openai_compat import OpenAICompatibleProvider

ATOMGIT_BASE_URL = "https://api.gitcode.com/api/v1"

class AtomGitProvider(OpenAICompatibleProvider):
    def __init__(self, config: ProviderConfig):
        super().__init__(
            config,
            provider_name="ATOMGIT",
            base_url=config.base_url or ATOMGIT_BASE_URL,
            api_key=config.api_key,
        )
''')

# 3. Patch providers/__init__.py
providers_init = '/root/free-claude-code/providers/__init__.py'
with open(providers_init, 'r') as f:
    providers_code = f.read()

if 'AtomGitProvider' not in providers_code:
    providers_code = providers_code.replace('from .scnet import SCNETProvider', 'from .scnet import SCNETProvider\nfrom .atomgit import AtomGitProvider')
    providers_code = providers_code.replace('"SCNETProvider",', '"SCNETProvider",\n    "AtomGitProvider",')
    with open(providers_init, 'w') as f:
        f.write(providers_code)

# 4. Patch api/dependencies.py
deps_path = '/root/free-claude-code/api/dependencies.py'
with open(deps_path, 'r') as f:
    deps_code = f.read()

if 'provider_type == "atomgit"' not in deps_code:
    deps_code = deps_code.replace('from providers.scnet import SCNET_BASE_URL, SCNETProvider', 'from providers.scnet import SCNET_BASE_URL, SCNETProvider\nfrom providers.atomgit import ATOMGIT_BASE_URL, AtomGitProvider')
    
    atomgit_block = """    elif provider_type == "atomgit":
        if not settings.atomgit_api_key or not settings.atomgit_api_key.strip():
            raise ValueError(
                "ATOMGIT_API_KEY is not set. Add it to your .env file."
            )
        config = _create_provider_config(settings, ATOMGIT_BASE_URL)
        config.api_key = settings.atomgit_api_key
        return AtomGitProvider(config)
"""
    deps_code = deps_code.replace('    else:\n        raise ValueError(', f'{atomgit_block}    else:\n        raise ValueError(')
    with open(deps_path, 'w') as f:
        f.write(deps_code)

print("Patch successful.")
