# Zerously

Blog de Mariano Abdala: [zerously.com](https://zerously.com). Jekyll + Markdown + GitHub Pages, sin CMS.

## Publicar, sin instalar nada

1. Copiá [templates/post.md](templates/post.md) y escribí en cualquier editor de texto o Markdown.
2. Guardalo como `YYYY-MM-DD-un-titulo-corto.md`. Completá título, fecha, idioma y descripción. La fecha debe ser real y no futura.
3. En GitHub, abrí `_posts` → **Add file → Upload files** (o **Create new file** para pegar el texto). Subí el archivo a una **rama nueva** y abrí un pull request hacia `master`.
4. Revisá el texto, los cambios y la validación **Check site**. Si agregás imágenes, subilas en la misma rama a `images/posts/un-titulo-corto/`.
5. Al aprobar y fusionar el PR, GitHub Pages publica automáticamente desde `master`. Esperá a que termine **pages build and deployment**.

La vista Markdown de GitHub sirve para revisar el texto; no reproduce el diseño del blog. El workflow del PR adjunta el sitio construido como `site-preview`. También podés previsualizarlo localmente.

[Guía de escritura y publicación](docs/PUBLISHING.md) · [Configuración, diagnóstico y HTTPS pendiente](docs/MAINTENANCE.md)

`read.me.md` es la página personal pública en `/read-me/`; este README documenta el repositorio y no se publica.

## Vista previa local (opcional)

Con Ruby y Bundler instalados:

```sh
bundle install
bundle exec jekyll serve
```

Abrí `http://127.0.0.1:4000`. Para construir y comprobar los enlaces históricos, RSS y metadatos:

```sh
bundle exec jekyll build
python3 script/check_site.py
```

El `Gemfile` fija las versiones principales compatibles con [GitHub Pages](https://pages.github.com/versions/). El despliegue sigue usando el constructor administrado de Pages. No se necesita Node, un editor particular ni una cuenta adicional.
