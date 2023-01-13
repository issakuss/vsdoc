# External Filters
This docker installs external filters:

- pantable
- pandocker-lua-filters

# pantable

https://github.com/ickc/pantable

You can embed csv file as a table.

```table
---
caption: 'Kore ga kyapusyon'
alignment: LRRL
table-width: 2/3
markdown: True
include: report/table.csv
---
```

## pandocker-lua-filters

This includes various filters

### docx-comment

You can comment on a sentences [comments]{.comment-start}like this[]{.comment-end}.

### docx-pagebreak-toc.lua

This filter breaks page...

\newpage

Like this.
