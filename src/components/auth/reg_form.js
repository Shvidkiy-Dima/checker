import React from "react";
import { Redirect, Link } from "react-router-dom";
import { InputHook } from "../../utils/hooks";
import request from "../../utils/request";
import { Form, Input, Button, Checkbox, Row, Col, Card, Alert } from "antd";
import { UserOutlined, LockOutlined } from "@ant-design/icons";
import "./login.css";

export default function LoginForm({ auth}) {
  const [error, setError] = React.useState([]);
  const [Sended, SetSended] = React.useState(false)


  function DoReg(value) {
    console.log(value)
    let { password, password2, email } = value;   
    console.log(password != password2)
    if (password != password2) {
      setError(["Passwords mistmach!"]);
      return
    }
    request(
      {
        method: "post",
        url: "api/auth/sign-up/",
        data: { email: email, password: password },
      },
      (res) => {
          SetSended(true)
      },
      (err) => {
        console.log(err.response)
        let errors = []
        if (err.response) {
          setError(err.response.data.non_field_errors ? err.response.data.non_field_errors :  Object.values(err.response.data));          
        }
        else{
          setError([err.message])
        }
      }
    );
  }


  if (auth === true){
    return <Redirect to="/dashboard" />
  }


  if (Sended === true){

    return (
      <div style={{ height: "100%"}}>
      <Row justify="center" align="center">
        <Col>
          <Card
            title=" "
            bordered={false}
            style={{marginTop: "40%" }}
          >
            <h1>We send confirmation email. Please check your mail</h1>
          </Card>
        </Col>
      </Row>
    </div>

    )

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

                  {error.map((e, i)=><Alert message={e} type="error" key={i} />)}
                </Form>
              </Card>
            </Col>
          </Row>
        </div>
  );
}
