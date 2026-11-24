import { client } from '~/generated-client/client.gen'

const LOGIN_PATH = '/login'
const RETURN_TO_QUERY = 'return_to'
const UNAUTHORIZED_STATUS = 401

export default defineNuxtPlugin(() => {
  const route = useRoute()
  const { resetSession } = useAuth()

  client.setConfig({
    onResponse: async ({ response }) => {
      if (response.status !== UNAUTHORIZED_STATUS) {
        return
      }

      resetSession()

      if (route.path === LOGIN_PATH) {
        return
      }

      await navigateTo({
        path: LOGIN_PATH,
        query: { [RETURN_TO_QUERY]: route.fullPath }
      })
    }
  })
})
