import React from "react";
import { Redirect, Link } from "react-router-dom";
import { InputHook } from "../../utils/hooks";
import request from "../../utils/request";
import { Form, Input, Button, Checkbox, Row, Col, Card, Alert } from "antd";
import { UserOutlined, LockOutlined } from "@ant-design/icons";
import "./login.css";

export default function LoginForm({ auth, login }) {
  let [error, setError] = React.useState("");

  function DoLogin(value) {
    setError("");
    console.log(value);
    let { password, email } = value;
    console.log(password, email);
    request(
      {
        method: "post",
        url: "api/auth/sign-in/",
        data: { email: email, password: password },
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

  if (auth === true){
    return <Redirect to="/dashboard" />
  }

  return (
        <div style={{ height: "100%", backgroundColor: "rgb(208, 219, 228)" }}>
          <Row justify="center" align="center">
            <Col>
              <Card
                title=" "
                bordered={true}
                style={{ width: 400, marginTop: "40%" }}
              >
                <Form
                  name="normal_login"
                  className="login-form"
                  onFinish={DoLogin}
                >
                  <Form.Item
                    name="email"
                    rules={[
                      {
                        type: "email",
                        required: true,
                        message: "Please input your Email!",
                      },
                    ]}
                  >
                    <Input
                      prefix={<UserOutlined className="site-form-item-icon" />}
                      placeholder="Email"
                    />
                  </Form.Item>
                  <Form.Item
                    name="password"
                    rules={[
                      {
                        required: true,
                        message: "Please input your Password!",
                      },
                    ]}
                  >
                    <Input
                      prefix={<LockOutlined className="site-form-item-icon" />}
                      type="password"
                      placeholder="Password"
                    />
                  </Form.Item>
                  <Form.Item>
                    <Button
                      type="danger"
                      htmlType="submit"
                      className="login-form-button"
                    >
                      Log in
                    </Button>
                    <Link to="/registration">Or register now!</Link>
                  </Form.Item>
                  {error ? <Alert message={error} type="error" /> : ""}
                </Form>
              </Card>
            </Col>
          </Row>
        </div>
  );
}
