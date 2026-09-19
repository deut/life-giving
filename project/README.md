# Брендбук ГО «Життєдайна» — вихідні матеріали

Архів містить фінальний PDF, початковий PDF, скрипт складання та всі растрові ресурси, потрібні для відтворення поточної версії.

## Структура

- `outputs/zhyttiedaina_brandbook_page12_cream_qr.pdf` — фінальна версія документа.
- `work/pdfs/edited-source.pdf` — початковий PDF.
- `work/pdfs/edit_pdf.py` — скрипт складання документа.
- `work/pdfs/extracted/` — витягнуті та підготовлені логотипи й растрові елементи.
- `work/pdfs/qr-*.jpg` — оригінальні QR-зображення.
- `work/pdfs/qr-*.png` — підготовлені QR-картки.
- `fonts/` — використані Roboto Regular і Roboto Bold та текст ліцензії Apache 2.0.

## Відтворення PDF

Потрібен Python 3 із пакетами `Pillow`, `pypdf` і `reportlab`.

Запуск із кореня розпакованої папки:

```bash
python3 work/pdfs/edit_pdf.py
```

Результат буде записано в `outputs/zhyttiedaina_brandbook_page12_cream_qr.pdf`.

Шрифти Lobster і PT Serif на збережених оригінальних сторінках уже вбудовані в `edited-source.pdf`; окремі файли цих шрифтів для складання не потрібні.
