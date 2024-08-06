import axios from "axios";
import Swal from "sweetalert2";

window.axios = axios;

axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "csrftoken";

window.axios.interceptors.response.use(
  function(response) {
    return response;
  },
  function(error) {
    // if (error.response?.data?.message == 'CSRF token mismatch.') {
    //   Swal.fire(
    //     'Notification',
    //     'Your session has expired. Refresh the page to continue',
    //     'warning',
    //   );
    // }

    if (error.response?.status == 403) {
      Swal.fire("Restricted", error.response?.data?.message, "warning");
    }

    return Promise.reject(error);
  }
);