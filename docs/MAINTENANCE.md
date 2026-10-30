# Configuración y mantenimiento

## Decisión

Se conserva Jekyll, Kramdown, `master`, `CNAME` (`zerously.com`), las imágenes, los 12 posts y `/read-me/`. No hay migración de contenido ni CMS. Los posts históricos permanecen idénticos, byte por byte; Read.me solo cambia sus enlaces internos de HTTP a HTTPS.

La portada agrega extractos; las plantillas usan navegación visible, enlace para saltar al contenido, foco de teclado y una columna legible. Las fuentes son locales al dispositivo. Se retira la carga global de Universal Analytics; no se incorpora un servicio nuevo. El embed histórico de Twitter permanece en el post que lo contiene.

SEO usa `jekyll-seo-tag` y `jekyll-sitemap`, compatibles con Pages: títulos, descripciones, canonical HTTPS, Open Graph, JSON-LD, sitemap y robots. El RSS sigue en `/feed.xml`, ahora incluye todos los posts y links HTTPS. Los GUID históricos se mantienen en HTTP para evitar que lectores RSS los interpreten como artículos nuevos; son identificadores, no recursos cargados por la página.

## Publicación actual comprobada

Revisión del 30 de octubre de 2026, base `c857d2bd97e62a3fc973a05cd06d250c5ba67794`:

- El repositorio es público, su rama predeterminada es `master` y Pages está habilitado.
- La última ejecución visible es **pages build and deployment**, evento `dynamic`, rama `master`, resultado exitoso, 11 de mayo de 2026: https://github.com/marianoabdala/marianoabdala.github.io/actions/runs/25687756457.
- No había un workflow de despliegue propio en el repositorio. El flujo observado corresponde a la publicación administrada desde una rama.
- La configuración privada de Settings → Pages no pudo inspeccionarse. No se cambiaron sus opciones, DNS ni el dominio.

Se mantiene ese despliegue: es suficiente para Jekyll y evita una migración innecesaria. `.github/workflows/check-site.yml` **solo construye, verifica y adjunta una vista previa** en PRs; no tiene permisos ni pasos de despliegue. No cambiar la fuente a “GitHub Actions” con este workflow: faltaría el despliegue. En Pages debe conservarse la fuente existente; verificar `master` y `/(root)` antes de fusionar.

## HTTPS: resolver antes de fusionar este PR

El chequeo público observó:

- HTTP responde 200, sin redirigir a HTTPS.
- HTTPS falla la validación: el certificado servido no coincide con `zerously.com`.
- El registro A observado es `192.30.252.153`, una dirección histórica de Pages. No se observó AAAA. `www` apunta a `marianoabdala.github.io`.

No basta cambiar `url` en Jekyll: eso prepara los enlaces y metadatos, pero no emite certificados. No publicar esta versión hasta confirmar que el dominio funciona con HTTPS.

Con autorización para modificar la configuración de producción:

1. En Settings → Pages, confirmar que el dominio es `zerously.com`, la fuente actual y el diagnóstico DNS.
2. En el proveedor DNS, comparar los registros existentes con la [configuración oficial vigente para dominios raíz](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site#configuring-an-apex-domain). Corregir solo lo necesario, sin tocar MX/TXT ni otros servicios. No se presupone acceso al proveedor DNS.
3. Esperar la validación del dominio y la emisión de un certificado válido. Si sigue pendiente, seguir el [diagnóstico oficial de HTTPS](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https).
4. Activar **Enforce HTTPS** y comprobar dominio raíz, `www`, redirección HTTP, `/read-me/`, `/feed.xml` y un post.
5. Solo entonces aprobar/fusionar la renovación visual.

No se ha desplegado este cambio. El PR queda en borrador hasta revisión y resolución de HTTPS.

## URLs y comprobaciones

`_data/legacy_posts.json` registra los 12 archivos originales, sus hashes y las URLs obtenidas del sitio publicado. En particular, `view-with-tag` vive en `/2016/07/21/` e `introduction-to-frp-pt2` en `/2016/03/25/`, aunque los archivos tengan otra fecha. `Etc/UTC` conserva ese comportamiento.

`script/check_site.py` comprueba esos archivos y rutas, enlaces internos y recursos locales, estructura básica accesible, canonical HTTPS, JSON-LD, sitemap, RSS y exclusión de documentos internos. No valida servicios externos ni reemplaza una revisión visual o con lector de pantalla. Si más adelante se edita intencionalmente un post histórico, actualizar su hash en el manifiesto después de revisar el contenido, conservando la URL.
