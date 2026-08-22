# ai-plugins

Публичный маркетплейс агентных плагинов и скиллов. Скиллы следуют открытому
[стандарту Agent Skills](https://agentskills.io/specification) (папка +
`SKILL.md` с frontmatter) и работают в Claude Code, OpenAI Codex и других
агентах, принявших стандарт.

В этом репозитории — только текстовые инструкции скиллов и вшитые ссылки на
релизы. Исполняемые файлы здесь не хранятся: скилл сам скачивает бинари под
вашу платформу из публичных релизов и проверяет контрольные суммы.

## Установка

**Claude Code:**

```
/plugin marketplace add Akurganow/ai-plugins
/plugin install hp@ai-plugins
```

**Codex:** скопируйте папку скилла в каталог скиллов Codex:

```
git clone https://github.com/Akurganow/ai-plugins /tmp/ai-plugins
mkdir -p ~/.codex/skills
cp -r /tmp/ai-plugins/plugins/hp/skills/hp ~/.codex/skills/hp
```

(путь каталога скиллов сверяйте с актуальной документацией Codex по Agent
Skills — формат `SKILL.md` одинаковый). **Другие совместимые агенты:** так
же — папка скилла целиком в каталог скиллов агента.

## Плагины

| Плагин | Что делает | Статус |
|---|---|---|
| `hp` | Личный вероятностный дашборд: интересы → измеримые вопросы → вероятности рынков предсказаний → markdown-дашборд | заготовка, релиз готовится |

## Устройство

```
.claude-plugin/marketplace.json   каталог маркетплейса (Claude Code)
plugins/<имя>/
  .claude-plugin/plugin.json      манифест плагина (версия — по ней едут обновления)
  skills/<имя>/SKILL.md           скилл по стандарту Agent Skills
```

Версии плагинов бампаются при каждом изменении — без бампа `version` в
`plugin.json` установленные копии не получат обновление.
