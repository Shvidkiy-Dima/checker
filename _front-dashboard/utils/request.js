import axios from "axios";

function request(config, callback, errback) {
  let token = localStorage.getItem("token");
  if (token) {
    config.headers = {
      ...(config.headers || {}),
      Authorization: "Token " + token,
    };
  }
  axios(config).then(
  (res) => callback(res), 
  (err) => {
    errback(err);
  });
}

export default request;
