import type { NavigationGuard } from 'vue-router'
export type MiddlewareKey = string
declare module "/Users/user/開発/fastapi_proto/fastapi_prototype/nuxt3-tailwind-auth-app/node_modules/nuxt/dist/pages/runtime/composables" {
  interface PageMeta {
    middleware?: MiddlewareKey | NavigationGuard | Array<MiddlewareKey | NavigationGuard>
  }
}