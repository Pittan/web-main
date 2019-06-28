'use strict'

import Vue from 'vue'
import VuePtero from 'vue-ptero'
import VueRouter from 'vue-router'
import VueI18n from 'vue-i18n'

import log from 'loglevel'

import 'normalize.css'
import './style.scss'

import { App } from './components'
import setupRouter from './router'
import messages from './locales'

// -------------------------------------------------------------------

if (DEBUG) {
  log.setLevel('trace')
} else {
  log.setLevel('warn')
}

Vue.use(VuePtero, { target: document.body })
Vue.use(VueRouter)
Vue.use(VueI18n)

// -------------------------------------------------------------------

export default new Vue({
  el: '.App',
  render: h => h(App),
  router: setupRouter(),

  // i18n
  locale: 'ja',
  messages,
})

