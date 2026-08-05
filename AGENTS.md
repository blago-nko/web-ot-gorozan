# Инструкции для ИИ-агентов

> **ВАЖНО:** Этот файл обязателен к прочтению для всех ИИ-агентов
> (Claude, GPT, Gemini и др.), работающих с этим репозиторием.

## 🌩️ Облачная разработка (Cloud-Only Development)

Вся разработка в экосистеме blago-nko ведётся **исключительно в облаке**.

### Обязательные правила

1. **ЗАПРЕЩЕНО:**
   - Локальная разработка на рабочей машине
   - Клонирование репозиториев на локальный диск (`git clone`)
   - Использование локальных IDE (VS Code, IntelliJ и т.д.)
   - Локальные коммиты и push (`git commit`, `git push`)

2. **ОБЯЗАТЕЛЬНО:**
   - Google Colab или Jupyter notebooks для всей разработки
   - GitHub API для всех изменений файлов
   - Personal Access Tokens для аутентификации
   - Обработка всех данных в памяти (RAM), без сохранения на диск

### Причины

- Единая точка входа для всех изменений
- Автоматическое логирование всех действий через GitHub API
- Возможность аудита через GitHub Actions
- Безопасность: токены не сохраняются локально
- Воспроизводимость: все изменения через API

### Рабочий процесс

```python
# Стандартный шаблон для Colab notebook
import requests
import base64

GITHUB_TOKEN = "ваш_токен"  # https://github.com/settings/tokens
OWNER = "blago-nko"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "Content-Type": "application/json"
}

def read_file(repo, path):
    url = f"https://api.github.com/repos/{OWNER}/{repo}/contents/{path}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return base64.b64decode(resp.json()['content']).decode('utf-8')
    return None

def write_file(repo, path, content, message):
    url = f"https://api.github.com/repos/{OWNER}/{repo}/contents/{path}"
    sha_resp = requests.get(url, headers=HEADERS)
    sha = sha_resp.json().get('sha') if sha_resp.status_code == 200 else None
    data = {
        "message": message,
        "content": base64.b64encode(content.encode('utf-8')).decode('utf-8'),
        "branch": "main"
    }
    if sha:
        data["sha"] = sha
    resp = requests.put(url, headers=HEADERS, json=data)
    return resp.status_code in [200, 201]
```

### Безопасность токенов

- Никогда не коммитьте токены в репозиторий
- Создавайте токены с минимальными правами (`repo` + `workflow`)
- Удаляйте токены после завершения работы

### Примеры задач

✅ **Правильно:**
- Чтение/запись файлов через GitHub API
- Создание PR через GitHub API
- Анализ кода в памяти Colab

❌ **Неправильно:**
- `git clone` на локальную машину
- `git commit` из локального терминала
- Сохранение файлов на локальный диск

---

**Дата утверждения:** 6 августа 2026 г.
**Версия:** 1.0
**Статус:** Активен
