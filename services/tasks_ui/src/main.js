import {
    createApp
} from 'vue'
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import App from './App.vue'

import {
    Amplify
} from 'aws-amplify';
import awsExports from './aws-exports.js';

Amplify.configure(awsExports);

const app = createApp(App)

app.use(ElementPlus)
app.mount('#app')