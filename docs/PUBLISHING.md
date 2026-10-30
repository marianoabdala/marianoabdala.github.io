# Escribir y publicar

## Un archivo por post

Usá cualquier editor que guarde texto plano UTF-8 con extensión `.md` o `.markdown`. Un documento de Word o un enlace al editor no alcanza: exportá o copiá su contenido como Markdown.

Copiá `templates/post.md` fuera de esa carpeta y guardalo en `_posts/YYYY-MM-DD-slug.md`. Por ejemplo, `_posts/2026-10-30-una-idea.md`:

```yaml
---
layout: post
title: "Una idea: escribir con menos fricción"
date: 2026-10-30
lang: es
description: "Qué cambió en mi forma de escribir y por qué me resulta más simple."
---
```

Después de la segunda línea `---`, escribí el artículo. Usá `##` para secciones: el sitio agrega el título principal. `lang: en` sirve para posts en inglés; el contenido histórico conserva ese idioma.

La descripción aparece como extracto en la portada y en los metadatos para buscadores y redes. Si la omitís, se usa el primer párrafo. Mantenela breve; la portada recorta los extractos a 45 palabras. El título va entre comillas, especialmente si incluye `:`.

La URL del ejemplo será `/2026/10/30/una-idea.html`. **Después de publicar, no cambies la fecha ni el nombre del archivo**: podés corregir título y cuerpo sin cambiar la URL. No uses categorías para organizar direcciones; el esquema de URLs está fijado en la configuración.

El sitio usa UTC para conservar las URLs históricas. Preferí fechas sin hora, iguales a la del archivo. Dos posts antiguos tienen un día distinto en la URL por su hora original: no los renombres ni cambies la zona horaria del sitio.

## Imágenes y enlaces

Guardá las imágenes en `images/posts/slug/` y usá una ruta desde la raíz, con texto alternativo descriptivo:

```markdown
![Diagrama del flujo de publicación](/images/posts/una-idea/flujo.png)

[Otro artículo](/2016/06/09/nested-functions.html)
```

Usá HTTPS en recursos externos. El código se escribe entre tres acentos graves y el nombre del lenguaje, por ejemplo `swift`. Evitá incluir scripts o HTML cuando Markdown sea suficiente.

## Borradores

Podés escribir fuera del repositorio o guardar el texto en `_drafts/un-titulo.md`. Los borradores no se publican. Para verlos localmente, usá `bundle exec jekyll serve --drafts`. Al terminar, mové el archivo a `_posts` con el nombre y la fecha definitivos.

Este repositorio es público: un borrador subido a GitHub también es visible allí aunque no aparezca en el blog. Para un borrador privado, conservá el archivo en tu editor.

Las fechas futuras no se publican (`future: false`). No hay publicación programada: al llegar la fecha hace falta otra construcción del sitio. Lo más sencillo es fusionar el PR cuando estés listo.

## Publicar desde GitHub

1. Abrí `_posts` en GitHub y elegí **Add file → Upload files** o **Create new file**.
2. Subí el Markdown, elegí una rama nueva y creá el PR hacia `master`. Subí las imágenes a esa misma rama.
3. Esperá **Check site**. Revisa que el título, los enlaces, las imágenes y el extracto estén bien.
4. Si querés ver el diseño completo sin Ruby: en la ejecución de **Check site**, descargá `site-preview`, descomprimilo y, dentro de esa carpeta, ejecutá `python3 -m http.server 4000`. Abrí `http://localhost:4000`. No es un sitio de staging público.
5. Fusionar el PR es el paso que autoriza la publicación. Esperá el workflow **pages build and deployment**, luego abrí el artículo en el blog.

También funciona GitHub Desktop o Git: copiá los archivos en la misma estructura, confirmá los cambios en una rama, subila y abrí el PR.

Para corregir un post, editá el archivo existente y repetí el flujo. Para deshacer una publicación, usá **Revert** del PR y revisá/fusioná el PR de reversión. Esto crea otro despliegue.
