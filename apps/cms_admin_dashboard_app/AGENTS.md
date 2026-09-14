# cms_admin_dashboard_app - Admin Dashboard Frontend

This directory contains the source code for the Admin Dashboard of the Catechism Management System (CMS)

# Tech stack

**Languages**: HTML, Typescript, SCSS

**Frameworks and Libraries**
- Vue 3
- Nuxt v4 (SPA mode - ssr: false)
- NuxtUI v4 as the UI library
- @nuxtjs/i18n for i18n
- ESLint for linting

# Coding guidelines
- Do not hard code display strings, always use 18n.
- The folder app/generated-client contains the client and SDK for interacting with the backend api (generated using hey-api cli from the backend).

# References
The following can be referred to when needed
- [Nuxt documentation](https://nuxt.com/llms.txt)
- [NuxtUI Documentation](https://ui.nuxt.com/llms.txt)