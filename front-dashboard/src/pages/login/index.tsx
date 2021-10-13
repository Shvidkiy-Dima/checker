import React from "react";
import {useDispatch} from "react-redux";
import {Link} from "react-router-dom";
import { Form, Input, Button, Row, Col, Card, Alert} from "antd";
import { UserOutlined, LockOutlined } from "@ant-design/icons";
import {IRequestLogin} from "../../interfaces/auth";
import {ApiLogin} from "../../api/auth";
import {ApiGetProfile} from "../../api/profile";
import {SetProfileAction} from "../../store/actions/profile";
import {Routes} from "../../enums/routes.enum";


export default function Login() {
  const [error, setError] = React.useState<Array<string>>([]);
  const dispatch = useDispatch()

  async function ProcessLogin(values: IRequestLogin) {
    setError([]);
    try{
      const {data} = await ApiLogin(values)
      localStorage.setItem('token', data.token);
      const { data: profileData } = await ApiGetProfile();
      dispatch(SetProfileAction(profileData));
    }
    catch (err: any) {
        localStorage.removeItem('token')
        setError(err?.response ? err?.response?.data?.non_field_errors : [err?.message])
    }
  }


  return (
    <div style={{ height: "100%", overflow: "hidden" }}>
      <Row justify="center">
        <Col>
          <Card
            title="Sing in to your account"
            bordered={false}
            style={{ width: 600, marginTop: "40%", textAlign: "center" }}
            headStyle={{
              textAlign: "center",
              fontSize: "2em",
              fontFamily: "Nunito",
            }}
          >
            <Form
              name="normal_login"
              className="login-form"
              onFinish={(values) => ProcessLogin(values)}
              style={{ margin: "auto" }}
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
                  htmlType="submit"
                  className="login-form-button"
                >
                  Log in
                </Button>

                <Link to={`/${Routes.Registration}`} style={{marginLeft: 10}}>Or register now</Link>
              </Form.Item>
              {error.map((e, i)=><Alert message={e} type="error" key={i} />)}
            </Form>
          </Card>
        </Col>
     </Row>
    </div>
  );
}