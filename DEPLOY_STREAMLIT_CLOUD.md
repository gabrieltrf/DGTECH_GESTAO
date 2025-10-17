# 🚀 DEPLOY NO STREAMLIT CLOUD - PASSO A PASSO

## ✅ PASSO 1: Preparar o Repositório GitHub

### 1.1 - Fazer Commit das Mudanças

```bash
# Adicionar todos os arquivos
git add .

# Fazer commit
git commit -m "Deploy: App web completo com gestão de produtos, vendas e financeiro"

# Enviar para GitHub
git push origin main
```

---

## ✅ PASSO 2: Acessar Streamlit Cloud

### 2.1 - Ir para o Site
🔗 **https://share.streamlit.io/**

### 2.2 - Fazer Login
- Clique em **"Sign up"** ou **"Sign in"**
- Use sua conta **GitHub** (é mais fácil!)
- Autorize o acesso ao Streamlit

---

## ✅ PASSO 3: Criar o App

### 3.1 - Clicar em "New app"
- No canto superior direito
- Botão azul/roxo

### 3.2 - Configurar o Deploy

Preencha os campos:

```
Repository: gabrieltrf/DGTECH_GESTAO
Branch: main
Main file path: app_web.py
App URL (optional): dgtech-gestao (ou o nome que quiser)
```

### 3.3 - Advanced Settings (Opcional)

Se quiser configurar:
- **Python version:** 3.13 (ou deixar automático)
- **Secrets:** Por enquanto não precisa

---

## ✅ PASSO 4: Deploy!

### 4.1 - Clicar em "Deploy!"
- Vai começar a instalar as dependências
- Vai levar **2-3 minutos**

### 4.2 - Acompanhar o Progresso
Você verá:
```
🔄 Installing dependencies...
📦 Installing streamlit...
📦 Installing plotly...
📦 Installing pandas...
...
✅ App is running!
```

---

## ✅ PASSO 5: Acessar o App

### 5.1 - URL Gerada
Seu app estará em:
```
https://dgtech-gestao.streamlit.app
```
(ou o nome que você escolheu)

### 5.2 - Compartilhar
- Copie a URL
- Compartilhe com sua equipe
- Todos acessarão os **mesmos dados**!

---

## 🎉 PRONTO!

Agora você tem:
- ✅ App na nuvem
- ✅ Acesso de qualquer lugar
- ✅ Funciona no celular
- ✅ Mesmos dados para todos
- ✅ 100% GRÁTIS!

---

## 🔧 Atualizações Futuras

Quando quiser atualizar o app:

```bash
# 1. Fazer mudanças no código
# 2. Fazer commit
git add .
git commit -m "Atualização: nova funcionalidade"
git push origin main

# 3. Streamlit detecta automaticamente e atualiza!
✅ Deploy automático em 2 minutos
```

---

## ⚙️ Configurações Úteis

### Gerenciar o App
- **Dashboard:** https://share.streamlit.io/
- **Logs:** Ver erros em tempo real
- **Settings:** Mudar configurações
- **Delete:** Excluir o app

### Limites do Plano Grátis
```
✅ Apps ilimitados (públicos)
✅ 1GB RAM
✅ 1 CPU compartilhado
✅ Banda ilimitada
⚠️ App hiberna após 7 dias sem uso
   (acorda automaticamente quando acessar)
```

---

## 🐛 Troubleshooting

### Erro: "Requirements not found"
```bash
# Verificar se requirements_web.txt existe
ls requirements_web.txt

# Se não existir, criar:
pip freeze > requirements_web.txt
```

### Erro: "Module not found"
```bash
# Adicionar a dependência em requirements_web.txt
# Fazer commit e push
git add requirements_web.txt
git commit -m "Fix: adicionar dependência"
git push
```

### App não carrega
```bash
# Ver logs no dashboard do Streamlit Cloud
# Procurar por erros em vermelho
# Corrigir e fazer push
```

---

## 📱 IMPORTANTE: Banco de Dados

### Como Funciona
- O arquivo `database.db` vai para a nuvem
- **Todos compartilham o mesmo banco**
- Dados persistem entre sessões

### ⚠️ Atenção
- Se você **deletar e recriar o app**, perde os dados
- Faça **backups** regularmente (botão em Configurações)
- Para produção séria, considere Firebase/PostgreSQL

### Fazer Backup
```bash
# No app (aba Configurações):
1. Clicar em "Baixar Backup"
2. Salvar arquivo .db
3. Guardar em local seguro
```

---

## 🎯 Próximos Passos Opcionais

### 1. Domínio Personalizado
```
Ao invés de: dgtech-gestao.streamlit.app
Usar: gestao.suaempresa.com.br

💰 Precisa: Plano pago do Streamlit (~$20/mês)
```

### 2. Autenticação
```python
# Adicionar login com senha
# Ver: streamlit-authenticator
pip install streamlit-authenticator
```

### 3. Migrar para Firebase
```
# Para dados mais seguros e escaláveis
# Ver: MELHORIAS_PARA_REVENDA.md
```

---

## 📞 Suporte

### Documentação
- Streamlit: https://docs.streamlit.io/deploy
- Community: https://discuss.streamlit.io/

### Problemas Comuns
- **App lento?** Normal no plano grátis (1 CPU)
- **Hibernou?** Acesse que ele acorda em 30s
- **Erro 500?** Ver logs no dashboard

---

## ✅ CHECKLIST DE DEPLOY

Antes de fazer deploy:

- [x] Código testado localmente ✅
- [x] requirements_web.txt atualizado ✅
- [x] .streamlit/config.toml criado ✅
- [x] .gitignore configurado ✅
- [x] Commit feito
- [ ] Push para GitHub
- [ ] Deploy no Streamlit Cloud
- [ ] Testar URL gerada
- [ ] Compartilhar com equipe

---

## 🎉 VAMOS LÁ!

**Comando para começar:**

```bash
git add .
git commit -m "Deploy: App completo no Streamlit Cloud"
git push origin main
```

**Depois:**
1. Ir para https://share.streamlit.io/
2. Sign in com GitHub
3. New app
4. Configurar
5. Deploy!

**Tempo total: 5 minutos** ⏱️

---

**Boa sorte! 🚀**
