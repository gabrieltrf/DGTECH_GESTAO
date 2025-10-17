# 🚀 GUIA COMPLETO - DEPLOY STREAMLIT + FIREBASE

## 📋 PRÉ-REQUISITOS

1. **Conta Google/Firebase** (gratuita)
2. **Python 3.11+** instalado
3. **Git** instalado
4. **Node.js** instalado (para Firebase CLI)

---

## 🎯 OPÇÕES DE HOSPEDAGEM

### Opção 1: Streamlit Cloud (RECOMENDADO - GRATUITO!)
**Prós**: Mais fácil, grátis, deploy automático
**Contras**: Limitado a 1GB RAM

### Opção 2: Firebase Hosting + Cloud Run
**Prós**: Escalável, profissional
**Contras**: Pode ter custo após limite grátis

### Opção 3: Heroku
**Prós**: Fácil, conhecido
**Contras**: Não é mais 100% grátis

---

## 🌐 OPÇÃO 1: STREAMLIT CLOUD (RECOMENDADO)

### Passo 1: Preparar Repositório GitHub

```bash
# 1. Inicializar Git (se ainda não fez)
cd C:\Users\gabri\Desktop\projetos\DGTECH_GESTAO
git init

# 2. Adicionar arquivos
git add .
git commit -m "Versão web com Streamlit"

# 3. Criar repositório no GitHub
# Vá em: https://github.com/new
# Nome: DGTECH_GESTAO
# Clique em "Create repository"

# 4. Conectar e enviar
git remote add origin https://github.com/SEU_USUARIO/DGTECH_GESTAO.git
git branch -M main
git push -u origin main
```

### Passo 2: Deploy no Streamlit Cloud

1. **Acesse**: https://share.streamlit.io/
2. **Login** com GitHub
3. **New app**
4. **Configurar**:
   - Repository: `SEU_USUARIO/DGTECH_GESTAO`
   - Branch: `main`
   - Main file path: `app_web.py`
5. **Deploy!** (leva 2-3 minutos)

### Passo 3: Acessar

Seu app estará em:
```
https://SEU_USUARIO-dgtech-gestao.streamlit.app
```

**PRONTO! ✅**

---

## 🔥 OPÇÃO 2: FIREBASE HOSTING + CLOUD RUN

### Passo 1: Instalar Firebase CLI

```bash
# Instalar Node.js primeiro (se não tiver)
# Download: https://nodejs.org/

# Instalar Firebase CLI
npm install -g firebase-tools

# Login no Firebase
firebase login
```

### Passo 2: Criar Projeto Firebase

```bash
# Ir para: https://console.firebase.google.com/
# Criar novo projeto: "dgtech-gestao"
# Habilitar Analytics (opcional)

# Inicializar Firebase no projeto
cd C:\Users\gabri\Desktop\projetos\DGTECH_GESTAO
firebase init

# Selecionar:
# - Hosting
# - Functions (Python)

# Configurar:
# - Projeto: dgtech-gestao
# - Public directory: public
# - Single-page app: No
# - Functions: Python 3.11
```

### Passo 3: Configurar Cloud Run

1. **Criar Dockerfile**:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements_web.txt .
RUN pip install --no-cache-dir -r requirements_web.txt

COPY . .

EXPOSE 8080

CMD ["streamlit", "run", "app_web.py", "--server.port=8080", "--server.address=0.0.0.0"]
```

2. **Build e Deploy**:

```bash
# Habilitar Cloud Run API
gcloud services enable run.googleapis.com

# Build da imagem
gcloud builds submit --tag gcr.io/dgtech-gestao/app

# Deploy no Cloud Run
gcloud run deploy dgtech-gestao \
  --image gcr.io/dgtech-gestao/app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Passo 4: Deploy

```bash
firebase deploy
```

**URL**: `https://dgtech-gestao.web.app`

---

## 🚀 OPÇÃO 3: HEROKU (ALTERNATIVA)

### Passo 1: Criar Conta

- Acesse: https://signup.heroku.com/
- Crie conta gratuita

### Passo 2: Instalar Heroku CLI

```bash
# Download: https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login
```

### Passo 3: Criar App

```bash
cd C:\Users\gabri\Desktop\projetos\DGTECH_GESTAO

# Criar app
heroku create dgtech-gestao

# Adicionar buildpack Python
heroku buildpacks:set heroku/python

# Deploy
git push heroku main
```

**URL**: `https://dgtech-gestao.herokuapp.com`

---

## 🎨 CUSTOMIZAÇÕES PÓS-DEPLOY

### Domínio Personalizado

#### Streamlit Cloud:
- Settings → Custom domain
- Adicionar: `gestao.seusite.com.br`

#### Firebase:
```bash
firebase hosting:channel:deploy production --domain=gestao.seusite.com.br
```

### Variáveis de Ambiente

#### Streamlit Cloud:
1. Settings → Secrets
2. Adicionar:
```toml
[database]
host = "seu_host"
user = "seu_user"
password = "sua_senha"
```

#### Firebase:
```bash
firebase functions:config:set database.host="seu_host"
```

---

## 📊 MONITORAMENTO

### Streamlit Cloud:
- Analytics integrado
- Logs em tempo real
- Métricas de uso

### Firebase:
- Firebase Console → Analytics
- Cloud Run → Logs
- Performance Monitoring

---

## 💰 CUSTOS

### Streamlit Cloud:
```
✅ Grátis para sempre
Limite: 1GB RAM, 1 CPU
Apps ilimitados (públicos)
```

### Firebase (Spark - Grátis):
```
✅ 10GB Hosting
✅ 360MB/dia Cloud Run
✅ 125K invocações/mês

Após limite: ~$0.40/GB
```

### Heroku:
```
⚠️ Não é mais 100% grátis
Dynos pagos: $7/mês
```

**RECOMENDAÇÃO: Streamlit Cloud** (mais fácil e grátis!)

---

## 🔧 TROUBLESHOOTING

### Erro: Module not found
```bash
# Adicionar no requirements_web.txt
pip freeze > requirements_web.txt
```

### Erro: Port already in use
```bash
# Streamlit usa porta 8501 por padrão
streamlit run app_web.py --server.port=8080
```

### Erro: Database locked
```python
# Usar SQLite em modo WAL
# No database.py, adicionar:
conn.execute('PRAGMA journal_mode=WAL')
```

### App muito lento
```python
# Adicionar cache
import streamlit as st

@st.cache_data
def load_data():
    return db.listar_produtos()
```

---

## 📱 TESTAR LOCALMENTE

```bash
# Instalar dependências
pip install -r requirements_web.txt

# Rodar localmente
streamlit run app_web.py

# Abrir browser em:
# http://localhost:8501
```

---

## 🎯 CHECKLIST FINAL

Antes de fazer deploy:

- [ ] Git configurado
- [ ] Repositório no GitHub
- [ ] requirements_web.txt atualizado
- [ ] .streamlit/config.toml criado
- [ ] app_web.py testado localmente
- [ ] Variáveis de ambiente configuradas
- [ ] Banco de dados preparado

---

## 🚀 DEPLOY EM 5 MINUTOS

### Via Streamlit Cloud (MAIS RÁPIDO):

```bash
# 1. Push para GitHub
git add .
git commit -m "Deploy web"
git push origin main

# 2. Ir para: https://share.streamlit.io/
# 3. New app → Conectar repo → Deploy!
# 4. PRONTO! ✅
```

**Tempo total: 5 minutos**

---

## 📚 RECURSOS EXTRAS

### Documentação:
- Streamlit: https://docs.streamlit.io/
- Firebase: https://firebase.google.com/docs/
- Heroku: https://devcenter.heroku.com/

### Tutoriais em Vídeo:
- Streamlit Cloud: https://www.youtube.com/watch?v=HKoOBiAaHGg
- Firebase Hosting: https://www.youtube.com/watch?v=jsRVHeQd5kU

### Comunidade:
- Forum Streamlit: https://discuss.streamlit.io/
- Stack Overflow: Tag `streamlit`

---

## 🎉 SUCESSO!

Seu sistema agora está na nuvem! 🌐

**Acesse de qualquer lugar:**
- 💻 Desktop
- 📱 Celular
- 🖥️ Tablet

**Compartilhe com:**
- 👥 Equipe
- 📊 Clientes
- 🏢 Empresa

---

**Desenvolvido com ❤️ | DGTECH GESTÃO v2.0 Web**
