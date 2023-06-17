import { ComputedRef, Ref } from 'vue'
export type LayoutKey = "default"
declare module "/Users/user/開発/fastapi_prototype/nuxt3-tailwind-auth-app/node_modules/nuxt/dist/pages/runtime/composables" {
  interface PageMeta {
    layout?: false | LayoutKey | Ref<LayoutKey> | ComputedRef<LayoutKey>
  }
}