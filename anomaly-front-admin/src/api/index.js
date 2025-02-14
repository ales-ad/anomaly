import axios from 'axios'
import useAuthStore from '@/store/auth'

const config = {
  headers: { 'content-type': 'application/json' }
}

export class RequestService {
  constructor () {
    this.call = axios.create(config)

    this.call.interceptors.request.use(request => {
      return request
    })

    this.call.interceptors.response.use(
      response => {
        return response
      },
      async (error) => {

        if (error.response.status === 401) {
          throw new Error('TokenExpired')
        }
        let errorMsg = error
        if (error.response && error.response.data && error.response.data.error) errorMsg = error.response.data.error.name

        throw new Error(errorMsg)
      }
    )
  }

  async sendRest (arg, baseURLApi = process.env.VUE_APP_BACKEND_URL) {

    const { method, url, params = {}, data = {}, headers = {}, timeout = 0 } = arg
    const logged = localStorage.getItem('access_token')

    if (logged) {
      headers.Authorization = 'Bearer ' + logged
    }

    const config = {
      method,
      url,
      baseURL: baseURLApi,
      params,
      data,
      headers,
      timeout
    }
    let response = null;
    try {
       response = await this.call.request(config)
      if (response.data.detail) {
        return response.data.detail
      } else {
        return response.data
      }
    } catch (error) {

      const auth = useAuthStore();

      if (error.message === 'TokenExpiredErr' || error.message === 'InvalidTokenErr') {
        try {
          if (url !== '/users/token/refresh') {

            auth.logout()

            window.location.href = '/login'
            //await useAuthStore.dispatch('auth/refresh')
            //return await this.sendRest(arg, baseURLApi)
          } else {
            throw new Error(error.message)
          }
        } catch (e) {
          console.log(e)
          auth.logout()

          window.location.href = '/login'
        }
      }
      throw new Error(error.message)
      // return
    }
  }
}

export default new RequestService()
