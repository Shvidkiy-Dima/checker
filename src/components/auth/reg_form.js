import React from "react";
import { Redirect, Link } from "react-router-dom";
import { InputHook } from "../../utils/hooks";
import request from "../../utils/request";
import { Form, Input, Button, Checkbox, Row, Col, Card, Alert } from "antd";
import { UserOutlined, LockOutlined } from "@ant-design/icons";
import "./login.css";

export default function LoginForm({ auth, login }) {
  let [error, setError] = React.useState("");

  function DoReg(value) {
    setError("");
    let password = value.password;
    let password2 = value.password2;
    if (password !== password2) {
      setError("Passwords mistmach");
    }
    // setError("");
    // request(
    //   {
    //     method: "post",
    //     url: "api/auth/sign-in/",
    //     data: { email: email_input.value, password: pass_input.value },
    //   },
    //   (res) => {
    //     localStorage.setItem("token", res.data.token);
    //     login(true);
    //   },
    //   (err) => {
    //     setError(err.response ? err.response.data.detail : err.message);
    //   }
    // );
  }


  if (auth === true){
    return <Redirect to="/dashboard" />
  }

  return (
        <div style={{ height: "100%"}}>
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
                  onFinish={DoReg}
                >
                  <Form.Item
                    name="email"
                    rules={[
                      {
                        type: "email",
                        required: true,
                        message: "Please input your email!",
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
                  <Form.Item
                    name="password2"
                    rules={[
                      {
                        required: true,
                        message: "Please input your Password again!",
                      },
                    ]}
                  >
                    <Input
                      prefix={<LockOutlined className="site-form-item-icon" />}
                      type="password"
                      placeholder="Password again"
                    />
                  </Form.Item>
                  <Form.Item>
                    <Button
                      type="danger"
                      htmlType="submit"
                      className="login-form-button"
                    >
                      Registration
                    </Button>
                    <Link to="/login">Already have account?</Link>
                  </Form.Item>

                  {error ? <Alert message={error} type="error" /> : ""}
                </Form>
              </Card>
            </Col>
          </Row>
        </div>
  );
}
