/* import EnvProvider from 'jvjr-docker-env'; */
window.VUE_APP_ROOT = "coucou"

export const getEnvironment = () => {
    console.log(window.VUE_APP_ROOT)
    /* console.log(EnvProvider.value('FILTERING')) */
}