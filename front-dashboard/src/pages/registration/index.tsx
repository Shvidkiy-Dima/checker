import React from "react";
import { Redirect, Link } from "react-router-dom";
import { Form, Input, Button, Checkbox, Row, Col, Card, Alert } from "antd";
import { UserOutlined, LockOutlined } from "@ant-design/icons";
import "./login.css";
import {Routes} from "../../enums/routes.enum";
import {ApiRegistration} from "../../api/auth";

export default function Registration() {
  const [error, setError] = React.useState<Array<string>>([]);
  const [Sent, SetSent] = React.useState(false)


  async function ProcessRegistration(value: any) {
    let {password, password2} = value;

    if (password !== password2) {
      setError(["Passwords mistmach!"]);
      return
    }
    try {
      await ApiRegistration(value)
      SetSent(true)
    } catch (err: any) {
      let errors = []
      if (err.response) {
        setError(err.response.data.non_field_errors ? err.response.data.non_field_errors : Object.values(err.response.data));
      } else {
        setError([err.message])
      }
    }


  }



    if (Sent) {
      return (
          <div style={{height: "100%"}}>
            <Row justify="center" align="middle">
              <Col>
                <Card
                    title=" "
                    bordered={false}
                    style={{marginTop: "40%"}}
                >
                  <h1>We send confirmation email. Please check your mail</h1>
                </Card>
              </Col>
            </Row>
          </div>
      )
    }

    return (
        <div style={{height: "100%"}}>
          <Row justify="center" align="middle">
            <Col>
              <Card
                  title=" "
                  bordered={true}
                  style={{width: 400, marginTop: "40%"}}
              >
                <Form
                    name="normal_login"
                    className="login-form"
                    onFinish={ProcessRegistration}
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
                        prefix={<UserOutlined className="site-form-item-icon"/>}
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
                        prefix={<LockOutlined className="site-form-item-icon"/>}
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
                        prefix={<LockOutlined className="site-form-item-icon"/>}
                        type="password"
                        placeholder="Password again"
                    />
                  </Form.Item>
                  <Form.Item>
                    <Button
                        type="primary"
                        htmlType="submit"
                        className="login-form-button"
                    >
                      Registration
                    </Button>
                    <Link to={`/${Routes.Login}`}>Already have account?</Link>
                  </Form.Item>

                  {error.map((e, i) => <Alert message={e} type="error"
                                              key={i}/>)}
                </Form>
              </Card>
            </Col>
          </Row>
        </div>
    );
}
