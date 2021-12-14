export const getEnv = () => {
    const VUE_CSP = "true"
    const VUE_MAPPING_PORT = "3000"
    const VUE_RUNNING_PORT = "3000"
    const VUE_X_FRAME_OPTIONS = "false"
    const VUE_FILTERING = "true"
    const VUE_APP_SERVER_IP_ADDRESS = "10.0.0.3"
    const VUE_CSP_DIRECTIVE = "img-src *"
    return {
        VUE_CSP : VUE_CSP,
        VUE_MAPPING_PORT : VUE_MAPPING_PORT,
        VUE_RUNNING_PORT : VUE_RUNNING_PORT,
        VUE_X_FRAME_OPTIONS : VUE_X_FRAME_OPTIONS,
        VUE_FILTERING : VUE_FILTERING,
        VUE_APP_SERVER_IP_ADDRESS : VUE_APP_SERVER_IP_ADDRESS,
        VUE_CSP_DIRECTIVE : VUE_CSP_DIRECTIVE,
    }
}