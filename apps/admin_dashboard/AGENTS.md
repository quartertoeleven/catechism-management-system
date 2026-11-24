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
- For dialog:
  - Use skeleton loadiA use ng when opening dialog if there's a need to load data (from API for example). Skeleton structure should looks similar to the form structure in the dialog.
  - When submitting the dialog: the primary button should show loading state, other buttons and the forms should be disabled (on the UForm level)
  - If the operation failed, do not close the dialog automatically.
- For main table on a page:
  - Use skeleton loading when loading data. The skeleton should has the same number of columns as the table

# References

Please ALWAYS use the documents listed in this section BEFORE digging into the code for documentation of a certain component.

- [Nuxt documentation](https://nuxt.com/llms.txt)
- [NuxtUI Documentation](https://ui.nuxt.com/llms.txt)
- [TanStack Table](https://tanstack.com/table/latest/llms.txt)