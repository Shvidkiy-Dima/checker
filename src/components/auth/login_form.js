import React from "react";
import { Redirect } from "react-router-dom";
import { InputHook } from "../../utils/hooks";
import request from "../../utils/request";

export default function LoginForm({ auth, login }) {
  let email_input = InputHook("");
  let pass_input = InputHook("");
  let [error, setError] = React.useState("");

  function DoLogin(event) {
    event.preventDefault();
    setError("");
    request(
      {
        method: "post",
        url: "api/auth/sign-in/",
        data: { email: email_input.value, password: pass_input.value },
      },
      (res) => {
        localStorage.setItem("token", res.data.token);
        login(true);
      },
      (err) => {
        setError(err.response ? err.response.data.detail : err.message);
      }
    );
  }

  return (
    <div>
      {auth === true ? (
        <Redirect to="/dashboard" />
      ) : (
        <div>
          <form onSubmit={DoLogin}>
            <h3>Login</h3>
            <div className="form-group">
              <input
                placeholder="Enter email"
                type="text"
                className="form-control"
                required={true}
                name="email"
                {...email_input.el}
              />
            </div>

            <div className="form-group">
              <input
                type="password"
                className="form-control"
                placeholder="Enter password"
                required={true}
                name="password"
                {...pass_input.el}
              />
            </div>
            <button
              type="submit"
              className="btn btn-sm btn-primary btn-block text-uppercase"
            >
              Login
            </button>

            {error ? (
              <small id="passwordHelp" class="text-danger">
                {error}
              </small>
            ) : (
              <p />
            )}
          </form>
        </div>
      )}
    </div>
  );
}
