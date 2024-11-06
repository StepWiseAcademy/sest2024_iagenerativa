# instala a fnm (Fast Node Manager, ou Gestor Rápido de Node)
winget install Schniz.fnm --accept-package-agreements --accept-source-agreements
# configurar o ambiente da fnm
fnm env --use-on-cd | Out-String | Invoke-Expression
# decarregar e instalar a Node.js
fnm use --install-if-missing 16